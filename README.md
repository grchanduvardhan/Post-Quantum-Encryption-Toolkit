# Post-Quantum File Encryption Toolkit

A comprehensive toolkit for encrypting and decrypting files using **Post-Quantum Cryptography (PQC)** with a hybrid cryptosystem approach. This implementation uses NIST-recommended PQC algorithms to provide quantum-resistant encryption.

**✨ Now includes a beautiful web interface!** Use the modern web app for an intuitive, user-friendly experience, or use the CLI for automation and scripting.

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **PQC Library**: Supports multiple libraries (quantcrypt, pqcrypto, or individual kyber/dilithium packages)
- **Symmetric Encryption**: `cryptography` library (AES-256-GCM)

## 🔐 Algorithms

- **Key Encapsulation Mechanism (KEM)**: ML-KEM-768 (Kyber-768) for key exchange
- **Digital Signature Scheme (DSS)**: ML-DSA-87 (Dilithium-3) for optional integrity and authentication
- **Symmetric Cipher**: AES-256-GCM for bulk file encryption

## 📦 Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install a PQC library** (choose one):
   ```bash
   # Option 1: Try quantcrypt (if available)
   pip install quantcrypt
   # Note: quantcrypt may require additional binary dependencies.
   # If you get "Failed to import clean binaries" errors, try:
   # - Reinstalling: pip uninstall quantcrypt && pip install quantcrypt
   # - Or use one of the alternatives below
   
   # Option 2: Try pqcrypto
   pip install pqcrypto
   
   # Option 3: Individual packages
   pip install kyber dilithium
   ```

   **Note**: The toolkit includes fallback mechanisms to work with different PQC libraries. If quantcrypt fails due to missing binaries, the toolkit will automatically try other available libraries.

## ✅ Verification

After installation, verify everything works:

```bash
python test_pqc_toolkit.py
```

This comprehensive test will:
- ✅ Verify PQC library is working (ML-KEM-768 and ML-DSA-87)
- ✅ Test all toolkit modules
- ✅ Run a complete encryption/decryption workflow

If all tests pass, you're ready to use the toolkit!

## 🌐 Web Application

The toolkit includes a modern web interface for easy file encryption and decryption.

### Quick Start (Web App)

1. **Start the web server:**
   ```bash
   python start_web.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

3. **Use the interface:**
   - Generate key pairs with the Key Management tab
   - Encrypt files with drag-and-drop file uploads
   - Choose between **Confidential Encryption** or **Authentication Encryption (Digital Signature)**
   - Decrypt files with automatic downloads
   - Select **Confidential** or **Authentication** mode when decrypting and enforce signature verification with the toggle

See [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) for detailed web application documentation.

## 🚀 CLI Usage

### 1. Generate Key Pairs

Generate ML-KEM-768 and ML-DSA-87 key pairs for a user:

```bash
python main.py keygen <user_id>
```

Example:
```bash
python main.py keygen alice
```

This creates a directory structure:
```
keys/
└── alice/
    ├── alice_kem_public.key
    ├── alice_kem_private.key
    ├── alice_dss_public.key
    └── alice_dss_private.key
```

### 2. Encrypt a File

Encrypt a file using the recipient's public KEM key:

```bash
python main.py encrypt <filepath> <recipient_public_kem_key> [--signer-key <signer_private_dss_key>]
```

**Without signature**:
```bash
python main.py encrypt document.pdf keys/alice/alice_kem_public.key
```

**With signature** (for authentication):
```bash
python main.py encrypt document.pdf keys/alice/alice_kem_public.key \
    --signer-key keys/alice/alice_dss_private.key
```

The encrypted file will be saved as `<original_filename>.pqc`.

### 3. Decrypt a File

Decrypt a file using the recipient's private KEM key:

```bash
python main.py decrypt <encrypted_filepath> <recipient_private_kem_key> [--signer-key <signer_public_dss_key>] [--require-signature]
```

**Without signature verification**:
```bash
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key
```

**With signature verification**:
```bash
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \
    --signer-key keys/alice/alice_dss_public.key
```

**Require signature (reject unsigned files)**:
```bash
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \
    --signer-key keys/alice/alice_dss_public.key --require-signature
```

The decrypted file will be saved as `<original_filename>-decrypted.<original_extension>`.

## 📁 File Format

The `.pqc` encrypted file format contains:

1. **Magic Number** (4 bytes): `PQC1`
2. **Metadata Header**:
   - Algorithm flags (1 byte)
   - KEM ciphertext length (4 bytes)
   - GCM tag length (4 bytes)
   - Signature length (4 bytes)
   - Nonce (12 bytes)
3. **ML-KEM-768 Ciphertext Key**
4. **AES-256 GCM Tag** (16 bytes)
5. **ML-DSA-87 Signature** (if used)
6. **AES-256 Ciphertext** (encrypted file data)

When signatures are enabled, the signer protects the metadata header (algorithm flags, lengths, nonce) together with the KEM ciphertext, GCM tag, and AES ciphertext to provide tamper-evident authenticity.

## 🔒 Security Features

- **Hybrid Encryption**: Combines post-quantum KEM with symmetric encryption for efficiency
- **Authenticated Encryption**: AES-256-GCM provides both confidentiality and authenticity
- **Digital Signatures**: ML-DSA-87 signatures now cover the entire encrypted envelope for provenance
- **Signature Enforcement**: CLI flag and web toggle can reject unsigned or unverifiable files
- **Quantum-Resistant**: Uses NIST-standardized post-quantum algorithms

## 📝 Supported File Types

The toolkit treats all files as raw binary streams, making it compatible with any file type:
- Text files: `.txt`, `.json`, `.xml`, `.csv`
- Documents: `.pdf`, `.docx`, `.xlsx`
- Images: `.jpg`, `.png`
- And any other binary file format

## 🏗️ Project Structure

```
.
├── app.py               # Flask web application
├── start_web.py         # Web server startup script
├── main.py              # CLI entry point
├── key_manager.py       # Key generation and management
├── encryptor.py         # Hybrid encryption implementation
├── decryptor.py         # Hybrid decryption implementation
├── templates/          # Web interface templates
│   └── index.html      # Main web UI
├── static/             # Web interface assets
│   ├── style.css       # Modern styling
│   └── script.js       # Frontend JavaScript
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── WEB_APP_GUIDE.md    # Web application guide
```

## ⚠️ Important Notes

1. **Key Security**: Keep private keys secure and never share them. Store them in a safe location.

2. **Backup**: Always maintain backups of your keys. Loss of private keys means permanent loss of access to encrypted files.

3. **Library Compatibility**: The toolkit supports multiple PQC libraries. If one doesn't work on your platform, try another option.

4. **File Size**: Large files are efficiently encrypted using AES-256-GCM, with only the session key protected by post-quantum cryptography.

5. **Signature Verification**: Always verify signatures when decrypting files from untrusted sources to ensure authenticity and integrity.

## 🐛 Troubleshooting

### "No PQC library found" Error

Install one of the supported PQC libraries:
```bash
pip install quantcrypt
# or
pip install pqcrypto
# or
pip install kyber dilithium
```

### "Signature verification failed" Error

- Ensure you're using the correct public DSS key that corresponds to the private key used for signing
- The file may have been tampered with or corrupted

### "Decryption failed" Error

- Verify you're using the correct private KEM key that corresponds to the public key used for encryption
- The encrypted file may be corrupted

## 📚 References

- [NIST Post-Quantum Cryptography Standardization](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [ML-KEM (Kyber)](https://pq-crystals.org/kyber/)
- [ML-DSA (Dilithium)](https://pq-crystals.org/dilithium/)

## 📄 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Disclaimer**: This toolkit is for educational and research purposes. For production use, ensure proper security audits and key management practices.

#   P o s t - Q u a n t u m - E n c r y p t i o n - T o o l k i t  
 