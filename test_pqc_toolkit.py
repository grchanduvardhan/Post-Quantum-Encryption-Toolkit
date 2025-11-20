"""
Test script to verify PQC Toolkit functionality
This script tests the complete workflow: key generation, encryption, and decryption
"""

import os
import sys
from pathlib import Path

def test_pqc_library():
    """Test if a PQC library is available and working."""
    print("=" * 60)
    print("Testing PQC Library Availability")
    print("=" * 60)
    
    # Test quantcrypt
    try:
        from quantcrypt import kem, dss
        print("[OK] quantcrypt imported successfully")
        
        # Test ML-KEM-768
        try:
            kem_instance = kem.MLKEM_768()
            pub_key, priv_key = kem_instance.keygen()
            print(f"[OK] ML-KEM-768 key generation works! (pub: {len(pub_key)} bytes, priv: {len(priv_key)} bytes)")
            
            # Test encapsulation
            ciphertext, shared_secret = kem_instance.encaps(pub_key)
            print(f"[OK] ML-KEM-768 encapsulation works! (ciphertext: {len(ciphertext)} bytes)")
            
            # Test decapsulation
            recovered_secret = kem_instance.decaps(priv_key, ciphertext)
            if recovered_secret == shared_secret:
                print("[OK] ML-KEM-768 decapsulation works! Shared secrets match.")
            else:
                print("[ERROR] Decapsulated secret doesn't match!")
                return False
                
        except Exception as e:
            print(f"[ERROR] ML-KEM-768 test failed: {e}")
            return False
        
        # Test ML-DSA-87
        try:
            dss_instance = dss.MLDSA_87()
            pub_key, priv_key = dss_instance.keygen()
            print(f"[OK] ML-DSA-87 key generation works! (pub: {len(pub_key)} bytes, priv: {len(priv_key)} bytes)")
            
            # Test signing
            message = b"Test message for signature"
            signature = dss_instance.sign(priv_key, message)
            print(f"[OK] ML-DSA-87 signing works! (signature: {len(signature)} bytes)")
            
            # Test verification
            is_valid = dss_instance.verify(pub_key, message, signature)
            if is_valid:
                print("[OK] ML-DSA-87 verification works! Signature is valid.")
            else:
                print("[ERROR] Signature verification failed!")
                return False
                
        except Exception as e:
            print(f"[ERROR] ML-DSA-87 test failed: {e}")
            return False
        
        print("\n[SUCCESS] quantcrypt library is fully functional!")
        return True
        
    except ImportError as e:
        print(f"[ERROR] quantcrypt not available: {e}")
        print("\nPlease install a working PQC library:")
        print("  pip install quantcrypt")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def test_toolkit_modules():
    """Test if all toolkit modules can be imported."""
    print("\n" + "=" * 60)
    print("Testing Toolkit Modules")
    print("=" * 60)
    
    modules = ['key_manager', 'encryptor', 'decryptor', 'main']
    all_ok = True
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"[OK] {module_name}.py imported successfully")
        except ImportError as e:
            print(f"[ERROR] Failed to import {module_name}: {e}")
            all_ok = False
        except Exception as e:
            print(f"[ERROR] Error importing {module_name}: {e}")
            all_ok = False
    
    return all_ok


def test_full_workflow():
    """Test the complete encryption/decryption workflow."""
    print("\n" + "=" * 60)
    print("Testing Complete Workflow")
    print("=" * 60)
    
    try:
        from key_manager import generate_pqc_keys
        from encryptor import encrypt_file_hybrid
        from decryptor import decrypt_file_hybrid
        
        # Create test directory
        test_dir = Path("test_workflow")
        test_dir.mkdir(exist_ok=True)
        
        # Step 1: Generate keys
        print("\n[1/4] Generating keys for test user...")
        try:
            key_paths = generate_pqc_keys("testuser", str(test_dir / "keys"))
            print("[OK] Keys generated successfully")
        except Exception as e:
            print(f"[ERROR] Key generation failed: {e}")
            return False
        
        # Step 2: Create a test file
        print("\n[2/4] Creating test file...")
        test_file = test_dir / "test_document.txt"
        test_content = b"This is a test document for post-quantum encryption.\nIt contains multiple lines of text.\nTesting encryption and decryption workflow."
        test_file.write_bytes(test_content)
        print(f"[OK] Test file created: {test_file} ({len(test_content)} bytes)")
        
        # Step 3: Encrypt the file
        print("\n[3/4] Encrypting test file...")
        try:
            encrypted_path = encrypt_file_hybrid(
                str(test_file),
                key_paths['kem_public'],
                key_paths['dss_private']  # With signature
            )
            print(f"[OK] File encrypted: {encrypted_path}")
            
            # Verify encrypted file exists
            if not Path(encrypted_path).exists():
                print("[ERROR] Encrypted file not found!")
                return False
            
            encrypted_size = Path(encrypted_path).stat().st_size
            print(f"[OK] Encrypted file size: {encrypted_size} bytes")
            
        except Exception as e:
            print(f"[ERROR] Encryption failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 4: Decrypt the file
        print("\n[4/4] Decrypting test file...")
        try:
            decrypted_path = decrypt_file_hybrid(
                encrypted_path,
                key_paths['kem_private'],
                key_paths['dss_public']  # Verify signature
            )
            print(f"[OK] File decrypted: {decrypted_path}")
            
            # Verify decrypted file exists
            if not Path(decrypted_path).exists():
                print("[ERROR] Decrypted file not found!")
                return False
            
            # Verify content matches
            decrypted_content = Path(decrypted_path).read_bytes()
            if decrypted_content == test_content:
                print("[OK] Decrypted content matches original!")
                print(f"[OK] Decrypted file size: {len(decrypted_content)} bytes")
            else:
                print("[ERROR] Decrypted content doesn't match original!")
                print(f"Original length: {len(test_content)}, Decrypted length: {len(decrypted_content)}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Decryption failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Complete workflow test passed!")
        print("=" * 60)
        print(f"\nTest files are in: {test_dir.absolute()}")
        print("You can manually inspect the files if needed.")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Post-Quantum Encryption Toolkit - Test Suite")
    print("=" * 60)
    
    # Test 1: PQC Library
    if not test_pqc_library():
        print("\n[STOPPED] PQC library is not working.")
        print("Please follow the instructions in INSTALL_PQC_LIBRARY.md")
        return 1
    
    # Test 2: Toolkit Modules
    if not test_toolkit_modules():
        print("\n[STOPPED] Toolkit modules have errors.")
        return 1
    
    # Test 3: Full Workflow
    if not test_full_workflow():
        print("\n[STOPPED] Workflow test failed.")
        return 1
    
    print("\n" + "=" * 60)
    print("[ALL TESTS PASSED] Your PQC Toolkit is fully functional!")
    print("=" * 60)
    print("\nYou can now use the toolkit:")
    print("  python main.py keygen <user_id>")
    print("  python main.py encrypt <file> <public_key>")
    print("  python main.py decrypt <encrypted_file> <private_key>")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

