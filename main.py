#!/usr/bin/env python3
"""
Post-Quantum File Encryption Toolkit - Main CLI Entry Point

A command-line interface for encrypting and decrypting files using
hybrid post-quantum cryptography (ML-KEM-768 + AES-256-GCM + optional ML-DSA-87).
"""

import argparse
import sys
from pathlib import Path

from key_manager import generate_pqc_keys
from encryptor import encrypt_file_hybrid
from decryptor import decrypt_file_hybrid


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Post-Quantum File Encryption Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate keys for a user
  python main.py keygen alice

  # Encrypt a file (without signature)
  python main.py encrypt document.pdf keys/alice/alice_kem_public.key

  # Encrypt a file (with signature)
  python main.py encrypt document.pdf keys/alice/alice_kem_public.key \\
      --signer-key keys/alice/alice_dss_private.key

  # Decrypt a file (without signature verification)
  python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key

  # Decrypt a file (with signature verification)
  python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \\
      --signer-key keys/alice/alice_dss_public.key
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # ===== KEY GENERATION COMMAND =====
    keygen_parser = subparsers.add_parser(
        'keygen',
        help='Generate PQC key pairs (ML-KEM-768 and ML-DSA-87)'
    )
    keygen_parser.add_argument(
        'user_id',
        type=str,
        help='Unique identifier for the user (e.g., "alice", "bob")'
    )
    keygen_parser.add_argument(
        '--key-dir',
        type=str,
        default='keys',
        help='Directory to store keys (default: "keys")'
    )
    
    # ===== ENCRYPTION COMMAND =====
    encrypt_parser = subparsers.add_parser(
        'encrypt',
        help='Encrypt a file using hybrid PQC encryption'
    )
    encrypt_parser.add_argument(
        'filepath',
        type=str,
        help='Path to the file to encrypt'
    )
    encrypt_parser.add_argument(
        'recipient_key',
        type=str,
        help="Path to recipient's public KEM key"
    )
    encrypt_parser.add_argument(
        '--signer-key',
        type=str,
        default=None,
        help="Path to signer's private DSS key (optional, for signing)"
    )
    
    # ===== DECRYPTION COMMAND =====
    decrypt_parser = subparsers.add_parser(
        'decrypt',
        help='Decrypt a file encrypted with hybrid PQC encryption'
    )
    decrypt_parser.add_argument(
        'encrypted_filepath',
        type=str,
        help='Path to the encrypted .pqc file'
    )
    decrypt_parser.add_argument(
        'recipient_key',
        type=str,
        help="Path to recipient's private KEM key"
    )
    decrypt_parser.add_argument(
        '--signer-key',
        type=str,
        default=None,
        help="Path to signer's public DSS key (optional, for signature verification)"
    )
    decrypt_parser.add_argument(
        '--require-signature',
        action='store_true',
        help='Reject files that are not signed or cannot be signature-verified'
    )
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'keygen':
        try:
            generate_pqc_keys(args.user_id, args.key_dir)
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'encrypt':
        try:
            # Validate file exists
            if not Path(args.filepath).exists():
                print(f"[ERROR] File not found: {args.filepath}", file=sys.stderr)
                sys.exit(1)
            
            # Validate recipient key exists
            if not Path(args.recipient_key).exists():
                print(f"[ERROR] Recipient key not found: {args.recipient_key}", file=sys.stderr)
                sys.exit(1)
            
            # Validate signer key if provided
            if args.signer_key and not Path(args.signer_key).exists():
                print(f"[ERROR] Signer key not found: {args.signer_key}", file=sys.stderr)
                sys.exit(1)
            
            encrypt_file_hybrid(args.filepath, args.recipient_key, args.signer_key)
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'decrypt':
        try:
            # Validate encrypted file exists
            if not Path(args.encrypted_filepath).exists():
                print(f"[ERROR] Encrypted file not found: {args.encrypted_filepath}", file=sys.stderr)
                sys.exit(1)
            
            # Validate recipient key exists
            if not Path(args.recipient_key).exists():
                print(f"[ERROR] Recipient key not found: {args.recipient_key}", file=sys.stderr)
                sys.exit(1)
            
            # Validate signer key if provided
            if args.signer_key and not Path(args.signer_key).exists():
                print(f"[ERROR] Signer key not found: {args.signer_key}", file=sys.stderr)
                sys.exit(1)
            
            result = decrypt_file_hybrid(
                args.encrypted_filepath,
                args.recipient_key,
                args.signer_key,
                require_signature=args.require_signature,
                return_metadata=True
            )
            if isinstance(result, tuple):
                _, metadata = result
                signature_present = metadata.get('signature_present')
                signature_verified = metadata.get('signature_verified')
                
                if signature_present and signature_verified:
                    print("[OK] Digital signature verified.")
                elif signature_present and not args.signer_key:
                    print("[INFO] File is signed but no signer public key was provided.")
                elif not signature_present:
                    print("[INFO] File was not signed.")
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

