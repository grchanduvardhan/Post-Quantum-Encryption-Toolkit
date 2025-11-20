🚀 Post-Quantum File Encryption Toolkit

A comprehensive toolkit for encrypting and decrypting files using Post-Quantum Cryptography (PQC) with a hybrid cryptosystem approach.
This implementation uses NIST-recommended PQC algorithms to provide quantum-resistant encryption.

✨ Now includes a beautiful web interface!
Choose between the modern browser-based UI or the automated command-line interface.

🛠️ Technology Stack

Language: Python 3.10+

PQC Libraries: Supports quantcrypt, pqcrypto, or standalone kyber / dilithium packages

Symmetric Encryption: AES-256-GCM via cryptography library

🔐 Algorithms Used
Purpose	Algorithm	Standard
Key Encapsulation Mechanism (KEM)	ML-KEM-768 (Kyber-768)	NIST PQC
Digital Signatures (Optional)	ML-DSA-87 (Dilithium-3)	NIST PQC
Symmetric Encryption	AES-256-GCM	Industry Standard
📦 Installation
1. Clone the Repository
git clone <repo-url>
cd <repo-name>

2. Install Dependencies
pip install -r requirements.txt

3. Install a PQC Library

Pick one option:

# Option 1: Try quantcrypt (if supported on your system)
pip install quantcrypt

# Option 2: pqcrypto (stable alternative)
pip install pqcrypto

# Option 3: Individual PQC packages
pip install kyber dilithium


✔️ The toolkit automatically switches between available PQC libraries.
✔️ If quantcrypt shows "Failed to import clean binaries", use options 2 or 3.

✅ Verification

Run the full test suite:

python test_pqc_toolkit.py


This test verifies:

ML-KEM-768 functionality

ML-DSA-87 signing & verification

End-to-end encryption & decryption workflow

Toolkit module integrity

If all tests pass → Toolkit ready to use.

🌐 Web Application

A polished web interface is included.

Start the Web Server:
python start_web.py

Access the UI:

Open in your browser:
http://localhost:5000

Features:

Generate KEM & DSS key pairs

Drag-and-drop file encryption

Confidential or authenticated encryption

Automatic signed-envelope verification

Toggle: Require Signature for strict verification

One-click decryption and download

See WEB_APP_GUIDE.md for detailed instructions.

🚀 Command-Line Usage (CLI)
1. 🔑 Generate Key Pairs
python main.py keygen <user_id>


Example:

python main.py keygen alice


Generated structure:

keys/
└── alice/
    ├── alice_kem_public.key
    ├── alice_kem_private.key
    ├── alice_dss_public.key
    └── alice_dss_private.key

2. 🔒 Encrypt a File
python main.py encrypt <filepath> <recipient_public_kem_key> [--signer-key <signer_private_dss_key>]

Without Signature:
python main.py encrypt document.pdf keys/alice/alice_kem_public.key

With Signature:
python main.py encrypt document.pdf keys/alice/alice_kem_public.key \
    --signer-key keys/alice/alice_dss_private.key


Output file → document.pdf.pqc

3. 🔓 Decrypt a File
python main.py decrypt <encrypted_filepath> <recipient_private_kem_key> \
    [--signer-key <signer_public_dss_key>] [--require-signature]

Basic Decryption:
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key

Verify Signature:
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \
    --signer-key keys/alice/alice_dss_public.key

Enforce Signature (reject unsigned files):
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \
    --signer-key keys/alice/alice_dss_public.key --require-signature


Decrypted output → document-decrypted.pdf

📁 Encrypted File Format (.pqc)

The encrypted file contains:

Magic Number: PQC1 (4 bytes)

Metadata Header

Algorithm flags (1 byte)

KEM ciphertext length (4 bytes)

GCM tag length (4 bytes)

Signature length (4 bytes)

Nonce (12 bytes)

KEM Ciphertext (ML-KEM-768)

AES-GCM Tag (16 bytes)

Signature (ML-DSA-87) (if used)

AES-256-GCM Ciphertext

Signatures protect the entire encrypted envelope including the metadata.

🔒 Security Features

Hybrid PQC + AES-GCM scheme

Authenticated encryption

Post-quantum secure digital signatures

Signature-enforced decryption

Quantum-resistant and NIST-standardized

Library fallback support

📝 Supported File Types

Works with any file type:

.txt, .csv, .json

.pdf, .docx, .xlsx

Images: .jpg, .png

Binaries: .exe, .zip, .tar

All files are processed as raw binary streams.

🏗️ Project Structure
.
├── app.py                # Flask web application
├── start_web.py          # Web server launcher
├── main.py               # CLI entry point
├── key_manager.py        # Key generation & storage
├── encryptor.py          # Encryption implementation
├── decryptor.py          # Decryption implementation
├── templates/
│   └── index.html        # Web UI
├── static/
│   ├── style.css         # Web styling
│   └── script.js         # Frontend JS
├── requirements.txt
├── README.md
└── WEB_APP_GUIDE.md

⚠️ Important Notes

Never share private keys.

Back up all private keys — losing them means losing access to encrypted data.

Compatibility depends on the installed PQC library.

AES-256-GCM ensures fast encryption for large files.

Always verify signatures from untrusted sources.

🐛 Troubleshooting
❌ "No PQC library found"

Install any supported library:

pip install quantcrypt
pip install pqcrypto
pip install kyber dilithium

❌ "Signature verification failed"

Wrong DSS public key

File modified or corrupted

❌ "Decryption failed"

Wrong private KEM key

Encrypted file corrupted

📚 References

NIST PQC Standardization

ML-KEM (Kyber)

ML-DSA (Dilithium)

📄 License

This project is provided for educational and research purposes.

🤝 Contributing

Contributions, issues, and feature requests are welcome!

If you want, I can also:

✅ Add shields/badges
✅ Add a banner or ASCII art
✅ Add installation GIFs
✅ Make a professional project logo
