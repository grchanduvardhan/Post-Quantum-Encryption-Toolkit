"""
Encryption Module for Post-Quantum Cryptography Toolkit

This module implements hybrid encryption:
- AES-256-GCM for bulk file encryption
- ML-KEM-768 for key encapsulation
- ML-DSA-87 (optional) for digital signatures
"""

import os
import struct
from pathlib import Path
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


# File format constants
PQC_FILE_MAGIC = b'PQC1'  # Magic number for .pqc files
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
            return ('pqcrypto', None, None)  # Will handle differently
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


def _encapsulate_key(public_kem_key: bytes) -> Tuple[bytes, bytes]:
    """
    Encapsulate a key using ML-KEM-768 (generates shared secret).
    
    Args:
        public_kem_key: Recipient's public KEM key
    
    Returns:
        Tuple of (KEM ciphertext, shared_secret that will be used as AES key)
    """
    lib_type, kem_module, dss_module = _get_pqc_library()
    
    if lib_type == 'quantcrypt':
        # quantcrypt API - encapsulation generates shared secret
        try:
            kem_instance = kem_module.MLKEM_768()
            ciphertext, shared_secret = kem_instance.encaps(public_kem_key)
        except Exception as e:
            raise ValueError(f"quantcrypt MLKEM_768 failed: {e}. The library may be missing required binaries.")
        # Ensure we have 32 bytes for AES-256
        if len(shared_secret) >= 32:
            aes_key = shared_secret[:32]
        else:
            # Use HKDF to derive 32-byte key
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'pqc-aes-key',
                backend=default_backend()
            )
            aes_key = hkdf.derive(shared_secret)
        return ciphertext, aes_key
    
    elif lib_type == 'pqcrypto':
        # pqcrypto API - encapsulation
        from pqcrypto.kem.kyber768 import encapsulate
        ciphertext, shared_secret = encapsulate(public_kem_key)
        # Ensure 32 bytes
        aes_key = shared_secret[:32] if len(shared_secret) >= 32 else shared_secret + b'\x00' * (32 - len(shared_secret))
        return ciphertext, aes_key
    
    elif lib_type == 'kyber_dilithium':
        # kyber package API
        ciphertext, shared_secret = kem_module.encapsulate(public_kem_key)
        # Ensure 32 bytes
        aes_key = shared_secret[:32] if len(shared_secret) >= 32 else shared_secret + b'\x00' * (32 - len(shared_secret))
        return ciphertext, aes_key
    
    else:
        raise ValueError(f"Unsupported library type: {lib_type}")


def _sign_data(private_dss_key: bytes, data: bytes) -> bytes:
    """
    Sign data using ML-DSA-87.
    
    Args:
        private_dss_key: Signer's private DSS key
        data: Data to sign
    
    Returns:
        Digital signature
    """
    lib_type, kem_module, dss_module = _get_pqc_library()
    
    if lib_type == 'quantcrypt':
        try:
            dss_instance = dss_module.MLDSA_87()
            return dss_instance.sign(private_dss_key, data)
        except Exception as e:
            raise ValueError(f"quantcrypt MLDSA_87 failed: {e}. The library may be missing required binaries.")
    
    elif lib_type == 'pqcrypto':
        from pqcrypto.sign.dilithium3 import sign
        return sign(private_dss_key, data)
    
    elif lib_type == 'kyber_dilithium':
        return dss_module.sign(private_dss_key, data)
    
    else:
        raise ValueError(f"Unsupported library type: {lib_type}")


def encrypt_file_hybrid(
    filepath: str,
    recipient_public_kem_key_path: str,
    signer_private_dss_key_path: str = None
) -> str:
    """
    Encrypt a file using hybrid post-quantum cryptography.
    
    Args:
        filepath: Path to the file to encrypt
        recipient_public_kem_key_path: Path to recipient's public KEM key
        signer_private_dss_key_path: Optional path to signer's private DSS key
    
    Returns:
        Path to the encrypted .pqc file
    """
    # Read input file
    input_path = Path(filepath)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    
    # Read recipient's public KEM key
    with open(recipient_public_kem_key_path, 'rb') as f:
        recipient_public_kem_key = f.read()
    
    # ===== PQC PHASE (KEM) =====
    # Encapsulate using ML-KEM-768 to generate shared secret (used as AES key)
    kem_ciphertext, aes_key = _encapsulate_key(recipient_public_kem_key)
    
    # ===== SYMMETRIC PHASE =====
    # Generate random 12-byte nonce for GCM
    nonce = os.urandom(12)
    
    # Encrypt file using AES-256-GCM with the shared secret as the key
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    # Extract ciphertext and tag (GCM tag is appended to ciphertext)
    # GCM tag is 16 bytes, so ciphertext[:-16] is the actual ciphertext
    # and ciphertext[-16:] is the tag
    aes_ciphertext = ciphertext[:-16]
    gcm_tag = ciphertext[-16:]
    
    # ===== ALGORITHM FLAGS =====
    algorithms_byte = ALGORITHM_KEM_MLKEM768 | ALGORITHM_SYM_AES256GCM
    
    # ===== PQC PHASE (DSS - Optional) =====
    signature = None
    if signer_private_dss_key_path:
        with open(signer_private_dss_key_path, 'rb') as f:
            signer_private_dss_key = f.read()
        algorithms_byte |= ALGORITHM_DSS_MLDSA87
        
        signature_payload = struct.pack(
            '>BII12s',
            algorithms_byte,
            len(kem_ciphertext),
            len(gcm_tag),
            nonce
        ) + kem_ciphertext + gcm_tag + aes_ciphertext
        
        signature = _sign_data(signer_private_dss_key, signature_payload)
    
    # ===== CREATE OUTPUT FILE =====
    output_path = input_path.with_suffix(input_path.suffix + '.pqc')
    
    with open(output_path, 'wb') as f:
        # Write magic number
        f.write(PQC_FILE_MAGIC)
        
        # Write metadata header
        # Format: [magic(4)] [algorithms(1)] [kem_ct_len(4)] [tag_len(4)] [sig_len(4)] [nonce(12)]
        f.write(struct.pack('>B', algorithms_byte))  # Algorithm flags
        f.write(struct.pack('>I', len(kem_ciphertext)))  # KEM ciphertext length
        f.write(struct.pack('>I', len(gcm_tag)))  # GCM tag length (should be 16)
        f.write(struct.pack('>I', len(signature) if signature else 0))  # Signature length
        f.write(nonce)  # 12-byte nonce
        
        # Write KEM ciphertext
        f.write(kem_ciphertext)
        
        # Write GCM tag
        f.write(gcm_tag)
        
        # Write signature (if present)
        if signature:
            f.write(signature)
        
        # Write AES ciphertext
        f.write(aes_ciphertext)
    
    print(f"[OK] File encrypted successfully: {output_path}")
    print(f"  Original size: {len(plaintext)} bytes")
    print(f"  Encrypted size: {output_path.stat().st_size} bytes")
    
    return str(output_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python encryptor.py <filepath> <recipient_public_kem_key_path> [signer_private_dss_key_path]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    recipient_key = sys.argv[2]
    signer_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    encrypt_file_hybrid(filepath, recipient_key, signer_key)

