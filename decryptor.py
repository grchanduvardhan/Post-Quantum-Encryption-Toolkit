"""
Decryption Module for Post-Quantum Cryptography Toolkit

This module implements hybrid decryption:
- ML-KEM-768 for key decapsulation
- ML-DSA-87 (optional) for signature verification
- AES-256-GCM for bulk file decryption
"""

import struct
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


# File format constants (must match encryptor.py)
PQC_FILE_MAGIC = b'PQC1'
ALGORITHM_KEM_MLKEM768 = 0x01
ALGORITHM_DSS_MLDSA87 = 0x02
ALGORITHM_SYM_AES256GCM = 0x03


def _get_pqc_library():
    """Get the appropriate PQC library based on what's available."""
    try:
        from quantcrypt import kem, dss
        return ('quantcrypt', kem, dss)
    except ImportError:
        try:
            from pqcrypto.kem.kyber768 import generate_keypair, encrypt, decrypt
            from pqcrypto.sign.dilithium3 import generate_keypair as dss_keygen, sign, verify
            return ('pqcrypto', None, None)
        except ImportError:
            try:
                from kyber import Kyber768
                from dilithium import Dilithium3
                return ('kyber_dilithium', Kyber768(), Dilithium3())
            except ImportError:
                raise ImportError(
                    "No PQC library found. Please install one of:\n"
                    "  - quantcrypt: pip install quantcrypt\n"
                    "  - pqcrypto: pip install pqcrypto\n"
                    "  - kyber and dilithium: pip install kyber dilithium"
                )


def _decapsulate_key(private_kem_key: bytes, kem_ciphertext: bytes) -> bytes:
    """
    Decapsulate the shared secret using ML-KEM-768.
    
    Args:
        private_kem_key: Recipient's private KEM key
        kem_ciphertext: KEM ciphertext (encapsulated key)
    
    Returns:
        Recovered shared secret used as AES session key (32 bytes)
    """
    lib_type, kem_module, dss_module = _get_pqc_library()
    
    if lib_type == 'quantcrypt':
        # quantcrypt API
        try:
            kem_instance = kem_module.MLKEM_768()
            shared_secret = kem_instance.decaps(private_kem_key, kem_ciphertext)
        except Exception as e:
            raise ValueError(f"quantcrypt MLKEM_768 failed: {e}. The library may be missing required binaries.")
        # Ensure we have 32 bytes for AES-256
        if len(shared_secret) >= 32:
            return shared_secret[:32]
        else:
            # Use HKDF to derive 32 bytes
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'pqc-aes-key',
                backend=default_backend()
            )
            return hkdf.derive(shared_secret)
    
    elif lib_type == 'pqcrypto':
        # pqcrypto API - decapsulation
        from pqcrypto.kem.kyber768 import decapsulate
        shared_secret = decapsulate(private_kem_key, kem_ciphertext)
        # Ensure 32 bytes
        return shared_secret[:32] if len(shared_secret) >= 32 else shared_secret + b'\x00' * (32 - len(shared_secret))
    
    elif lib_type == 'kyber_dilithium':
        # kyber package API
        shared_secret = kem_module.decapsulate(private_kem_key, kem_ciphertext)
        # Ensure 32 bytes
        return shared_secret[:32] if len(shared_secret) >= 32 else shared_secret + b'\x00' * (32 - len(shared_secret))
    
    else:
        raise ValueError(f"Unsupported library type: {lib_type}")


def _verify_signature(public_dss_key: bytes, data: bytes, signature: bytes) -> bool:
    """
    Verify a digital signature using ML-DSA-87.
    
    Args:
        public_dss_key: Signer's public DSS key
        data: Data that was signed
        signature: Digital signature to verify
    
    Returns:
        True if signature is valid, False otherwise
    """
    lib_type, kem_module, dss_module = _get_pqc_library()
    
    if lib_type == 'quantcrypt':
        try:
            dss_instance = dss_module.MLDSA_87()
            return dss_instance.verify(public_dss_key, data, signature)
        except Exception as e:
            raise ValueError(f"quantcrypt MLDSA_87 failed: {e}. The library may be missing required binaries.")
    
    elif lib_type == 'pqcrypto':
        from pqcrypto.sign.dilithium3 import verify
        try:
            verify(public_dss_key, data, signature)
            return True
        except:
            return False
    
    elif lib_type == 'kyber_dilithium':
        return dss_module.verify(public_dss_key, data, signature)
    
    else:
        raise ValueError(f"Unsupported library type: {lib_type}")


def decrypt_file_hybrid(
    encrypted_filepath: str,
    recipient_private_kem_key_path: str,
    signer_public_dss_key_path: str = None,
    *,
    require_signature: bool = False,
    return_metadata: bool = False
) -> str | tuple[str, dict]:
    """
    Decrypt a file encrypted with hybrid post-quantum cryptography.
    
    Args:
        encrypted_filepath: Path to the encrypted .pqc file
        recipient_private_kem_key_path: Path to recipient's private KEM key
        signer_public_dss_key_path: Optional path to signer's public DSS key
    
    Returns:
        Path to the decrypted file
    """
    # Read encrypted file
    encrypted_path = Path(encrypted_filepath)
    if not encrypted_path.exists():
        raise FileNotFoundError(f"Encrypted file not found: {encrypted_filepath}")
    
    with open(encrypted_path, 'rb') as f:
        # Read magic number
        magic = f.read(4)
        if magic != PQC_FILE_MAGIC:
            raise ValueError(f"Invalid file format: expected PQC magic number, got {magic.hex()}")
        
        # Read metadata header
        algorithms_byte = struct.unpack('>B', f.read(1))[0]
        kem_ct_len = struct.unpack('>I', f.read(4))[0]
        gcm_tag_len = struct.unpack('>I', f.read(4))[0]
        sig_len = struct.unpack('>I', f.read(4))[0]
        nonce = f.read(12)
        
        # Read KEM ciphertext
        kem_ciphertext = f.read(kem_ct_len)
        
        # Read GCM tag
        gcm_tag = f.read(gcm_tag_len)
        
        # Read signature (if present)
        signature = None
        if sig_len > 0:
            signature = f.read(sig_len)
        
        # Read AES ciphertext
        aes_ciphertext = f.read()
    
    # ===== PQC PHASE (KEM) =====
    # Read recipient's private KEM key
    with open(recipient_private_kem_key_path, 'rb') as f:
        recipient_private_kem_key = f.read()
    
    # Decapsulate the AES session key
    aes_key = _decapsulate_key(recipient_private_kem_key, kem_ciphertext)
    
    # ===== PQC PHASE (DSS - Optional) =====
    signature_present = signature is not None
    signature_verified = None
    
    if signature_present:
        signature_payload = struct.pack(
            '>BII12s',
            algorithms_byte,
            kem_ct_len,
            gcm_tag_len,
            nonce
        ) + kem_ciphertext + gcm_tag + aes_ciphertext
        
        if signer_public_dss_key_path:
            with open(signer_public_dss_key_path, 'rb') as f:
                signer_public_dss_key = f.read()
            
            # Verify signature
            if not _verify_signature(signer_public_dss_key, signature_payload, signature):
                raise ValueError("[ERROR] Signature verification failed! File may be corrupted or tampered with.")
            signature_verified = True
            print("[OK] Signature verified successfully")
        elif require_signature:
            raise ValueError("[ERROR] Signature verification required but no signer public key provided.")
        else:
            print("[WARNING] File contains signature but no public key provided for verification")
            signature_verified = False
    elif require_signature:
        raise ValueError("[ERROR] Signature verification required but the encrypted file is not signed.")
    
    # ===== SYMMETRIC PHASE =====
    # Decrypt using AES-256-GCM
    aesgcm = AESGCM(aes_key)
    
    # Reconstruct ciphertext with tag for GCM decryption
    ciphertext_with_tag = aes_ciphertext + gcm_tag
    
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}. The file may be corrupted or the key may be incorrect.")
    
    # ===== WRITE OUTPUT FILE =====
    # Determine original extension (remove .pqc)
    if encrypted_path.suffix == '.pqc':
        # Try to extract original extension from filename
        # Format: filename.ext.pqc -> filename-decrypted.ext
        stem = encrypted_path.stem  # filename.ext
        if '.' in stem:
            # Has original extension
            parts = stem.rsplit('.', 1)
            original_ext = '.' + parts[1]
            output_name = parts[0] + '-decrypted' + original_ext
        else:
            # No original extension
            output_name = stem + '-decrypted'
    else:
        output_name = encrypted_path.stem + '-decrypted'
    
    output_path = encrypted_path.parent / output_name
    
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    print(f"[OK] File decrypted successfully: {output_path}")
    print(f"  Decrypted size: {len(plaintext)} bytes")
    
    if return_metadata:
        return str(output_path), {
            'signature_present': signature_present,
            'signature_verified': signature_verified,
            'require_signature': require_signature
        }
    
    return str(output_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python decryptor.py <encrypted_filepath> <recipient_private_kem_key_path> [signer_public_dss_key_path]")
        sys.exit(1)
    
    encrypted_filepath = sys.argv[1]
    recipient_key = sys.argv[2]
    signer_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    decrypt_file_hybrid(encrypted_filepath, recipient_key, signer_key)

