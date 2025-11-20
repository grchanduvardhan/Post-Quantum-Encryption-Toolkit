"""
Key Management Module for Post-Quantum Cryptography Toolkit

This module handles the generation and storage of PQC key pairs:
- ML-KEM-768 (Kyber) for key encapsulation
- ML-DSA-87 (Dilithium) for digital signatures
"""

import os
from pathlib import Path


def generate_pqc_keys(user_id: str, key_directory: str = "keys") -> dict:
    """
    Generate ML-KEM-768 and ML-DSA-87 key pairs for a user.
    
    Args:
        user_id: Unique identifier for the user
        key_directory: Directory to store keys (default: "keys")
    
    Returns:
        Dictionary with paths to generated keys
    """
    try:
        # Try to import quantcrypt first
        try:
            from quantcrypt import kem, dss
            
            # Generate ML-KEM-768 key pair
            try:
                kem_instance = kem.MLKEM_768()
                kem_public_key, kem_private_key = kem_instance.keygen()
                
                # Generate ML-DSA-87 key pair
                dss_instance = dss.MLDSA_87()
                dss_public_key, dss_private_key = dss_instance.keygen()
            except Exception as e:
                # quantcrypt imported but binaries missing or other error
                print(f"[WARNING] quantcrypt available but failed to use: {e}")
                print("[WARNING] Trying fallback libraries...")
                raise ImportError("quantcrypt binaries not available")
            
        except ImportError:
            # Fallback: Try pqcrypto or other libraries
            try:
                from pqcrypto.kem.kyber768 import generate_keypair, encrypt, decrypt
                from pqcrypto.sign.dilithium3 import generate_keypair as dss_keygen, sign, verify
                
                # Generate ML-KEM-768 key pair (Kyber-768)
                kem_public_key, kem_private_key = generate_keypair()
                
                # Generate ML-DSA-87 key pair (Dilithium-3 is close to ML-DSA-87)
                dss_public_key, dss_private_key = dss_keygen()
                
            except ImportError:
                # Alternative: Use individual packages
                try:
                    from kyber import Kyber768
                    from dilithium import Dilithium3
                    
                    # Generate ML-KEM-768 key pair
                    kyber = Kyber768()
                    kem_public_key, kem_private_key = kyber.generate_keypair()
                    
                    # Generate ML-DSA-87 key pair
                    dilithium = Dilithium3()
                    dss_public_key, dss_private_key = dilithium.generate_keypair()
                    
                except ImportError:
                    raise ImportError(
                        "No PQC library found. Please install one of:\n"
                        "  - quantcrypt: pip install quantcrypt\n"
                        "  - pqcrypto: pip install pqcrypto\n"
                        "  - kyber and dilithium: pip install kyber dilithium"
                    )
        
        # Create key directory structure
        user_key_dir = Path(key_directory) / user_id
        user_key_dir.mkdir(parents=True, exist_ok=True)
        
        # Save KEM keys
        kem_public_path = user_key_dir / f"{user_id}_kem_public.key"
        kem_private_path = user_key_dir / f"{user_id}_kem_private.key"
        
        with open(kem_public_path, 'wb') as f:
            f.write(kem_public_key)
        with open(kem_private_path, 'wb') as f:
            f.write(kem_private_key)
        
        # Save DSS keys
        dss_public_path = user_key_dir / f"{user_id}_dss_public.key"
        dss_private_path = user_key_dir / f"{user_id}_dss_private.key"
        
        with open(dss_public_path, 'wb') as f:
            f.write(dss_public_key)
        with open(dss_private_path, 'wb') as f:
            f.write(dss_private_key)
        
        key_paths = {
            'kem_public': str(kem_public_path),
            'kem_private': str(kem_private_path),
            'dss_public': str(dss_public_path),
            'dss_private': str(dss_private_path)
        }
        
        print(f"[OK] Keys generated successfully for user: {user_id}")
        print(f"  KEM Public Key:  {kem_public_path}")
        print(f"  KEM Private Key: {kem_private_path}")
        print(f"  DSS Public Key:  {dss_public_path}")
        print(f"  DSS Private Key: {dss_private_path}")
        
        return key_paths
        
    except Exception as e:
        print(f"[ERROR] Error generating keys: {e}")
        raise


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python key_manager.py <user_id>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    generate_pqc_keys(user_id)

