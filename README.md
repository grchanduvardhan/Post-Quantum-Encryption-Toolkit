Here is the **complete README in pure Markdown format** — clean, aligned, ready to copy-paste directly into GitHub.

---

````markdown
# 🚀 Post-Quantum File Encryption Toolkit

A comprehensive toolkit for encrypting and decrypting files using **Post-Quantum Cryptography (PQC)** with a hybrid cryptosystem approach.  
This implementation uses **NIST-recommended PQC algorithms** to provide **quantum-resistant encryption**.

✨ **Now includes a beautiful web interface!**  
Choose between the modern browser-based UI or the automated command-line interface.

---

## 🛠️ Technology Stack

- **Language:** Python 3.10+
- **PQC Libraries:** Supports `quantcrypt`, `pqcrypto`, or standalone `kyber` / `dilithium`
- **Symmetric Encryption:** AES-256-GCM (`cryptography`)

---

## 🔐 Algorithms Used

| Purpose | Algorithm | Standard |
|--------|-----------|----------|
| Key Encapsulation Mechanism (KEM) | **ML-KEM-768 (Kyber-768)** | NIST PQC |
| Digital Signatures (Optional) | **ML-DSA-87 (Dilithium-3)** | NIST PQC |
| Symmetric Encryption | **AES-256-GCM** | Industry Standard |

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repo-url>
cd <repo-name>
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install a PQC Library (choose one)

```bash
# Option 1: quantcrypt (if supported on your system)
pip install quantcrypt

# Option 2: pqcrypto (stable)
pip install pqcrypto

# Option 3: Individual PQC implementations
pip install kyber dilithium
```

> ✔️ Toolkit automatically switches between available PQC libraries.
> ✔️ If `quantcrypt` fails to load binaries, use Option 2 or 3.

---

## ✅ Verification

Run full test suite:

```bash
python test_pqc_toolkit.py
```

This verifies:

* ML-KEM-768 functionality
* ML-DSA-87 signing & verification
* End-to-end encryption/decryption
* All toolkit modules

If all tests pass → **Toolkit ready to use**.

---

# 🌐 Web Application

A polished, modern web interface is included.

### Start the Web Server

```bash
python start_web.py
```

### Open in Browser

```
http://localhost:5000
```

### Web Features

* Generate KEM & DSS key pairs
* Drag-and-drop file encryption
* Confidential or authenticated encryption
* Signature verification toggle
* Automatic decryption & file download

➡️ See **WEB_APP_GUIDE.md** for full documentation.

---

# 🚀 CLI Usage

---

## 1. 🔑 Generate Key Pairs

```bash
python main.py keygen <user_id>
```

Example:

```bash
python main.py keygen alice
```

Generated structure:

```
keys/
└── alice/
    ├── alice_kem_public.key
    ├── alice_kem_private.key
    ├── alice_dss_public.key
    └── alice_dss_private.key
```

---

## 2. 🔒 Encrypt a File

```bash
python main.py encrypt <filepath> <recipient_public_kem_key> [--signer-key <signer_private_dss_key>]
```

### Without Signature

```bash
python main.py encrypt document.pdf keys/alice/alice_kem_public.key
```

### With Signature

```bash
python main.py encrypt document.pdf keys/alice/alice_kem_public.key \
    --signer-key keys/alice/alice_dss_private.key
```

Result file → `document.pdf.pqc`

---

## 3. 🔓 Decrypt a File

```bash
python main.py decrypt <encrypted_filepath> <recipient_private_kem_key> \
    [--signer-key <signer_public_dss_key>] [--require-signature]
```

### Basic Decryption

```bash
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key
```

### Verify Signature

```bash
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \
    --signer-key keys/alice/alice_dss_public.key
```

### Enforce Signature (Reject unsigned files)

```bash
python main.py decrypt document.pdf.pqc keys/alice/alice_kem_private.key \
    --signer-key keys/alice/alice_dss_public.key --require-signature
```

Decrypted file → `document-decrypted.pdf`

---

# 📁 Encrypted File Format (`.pqc`)

The `.pqc` file contains:

1. **Magic Number:** `PQC1`
2. **Metadata Header:**

   * Algorithm flags (1 byte)
   * KEM ciphertext length (4 bytes)
   * GCM tag length (4 bytes)
   * Signature length (4 bytes)
   * Nonce (12 bytes)
3. **ML-KEM-768 Ciphertext**
4. **AES-GCM Tag (16 bytes)**
5. **ML-DSA-87 Signature (optional)**
6. **AES-256-GCM Ciphertext**

Signatures protect the entire encrypted envelope including metadata.

---

# 🔒 Security Features

* Hybrid PQC + AES-GCM encryption
* Authenticated encryption
* Post-quantum digital signatures
* Signature enforcement toggle
* Quantum-resistant (NIST standardized)
* Automatic library fallback system

---

# 📝 Supported File Types

Supports **all file types**, including:

* `.txt`, `.json`, `.csv`
* `.pdf`, `.docx`, `.xlsx`
* `.jpg`, `.png`
* Binaries: `.exe`, `.zip`, `.tar`, etc.

All files handled as raw binary data.

---

# 🏗️ Project Structure

```
.
├── app.py                # Flask web application
├── start_web.py          # Web server launcher
├── main.py               # CLI entry point
├── key_manager.py        # Key generation & management
├── encryptor.py          # Hybrid encryption module
├── decryptor.py          # Hybrid decryption module
├── templates/
│   └── index.html        # Web UI
├── static/
│   ├── style.css         # UI styling
│   └── script.js         # Frontend logic
├── requirements.txt
├── README.md
└── WEB_APP_GUIDE.md
```

---

# ⚠️ Important Notes

1. **Never share private keys.**
2. **Backup private keys** — without them, decryption is impossible.
3. PQC library support varies by OS; multiple fallback options included.
4. AES-GCM ensures efficient encryption for large files.
5. Always verify signatures from untrusted sources.

---

# 🐛 Troubleshooting

### ❌ "No PQC library found"

Install:

```bash
pip install quantcrypt
pip install pqcrypto
pip install kyber dilithium
```

### ❌ "Signature verification failed"

* Wrong DSS public key
* File corrupted
* File tampered with

### ❌ "Decryption failed"

* Wrong private KEM key
* File corrupted

---

# 📚 References

* NIST PQC Project
* ML-KEM (Kyber)
* ML-DSA (Dilithium)

---

# 📄 License

This project is provided **for educational and research purposes**.

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome!

```

---

If you want, I can also generate:

✅ Shields/badges  
✅ A banner/logo  
✅ A professional project description summary  
✅ A screenshot section  

Just tell me!
```
