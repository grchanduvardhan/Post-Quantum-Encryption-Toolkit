
# 🛡️ Post-Quantum File Encryption Toolkit

A comprehensive, hybrid cryptosystem toolkit for encrypting and decrypting files using **Post-Quantum Cryptography (PQC)**. This implementation leverages NIST-recommended PQC algorithms to provide robust, quantum-resistant file protection.

✨ **Now includes a beautiful web interface!** Use the modern web app for an intuitive, user-friendly experience, or use the powerful CLI for automation and scripting.

---

## 🛠️ Technology Stack

| Component | Technology / Algorithm | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core implementation |
| **PQC Library** | `quantcrypt`, `pqcrypto`, or individual packages | Post-Quantum Cryptography Primitives |
| **Symmetric Cipher** | `cryptography` (AES-256-GCM) | Bulk file encryption |
| **Key Exchange (KEM)** | **ML-KEM-768 (Kyber-768)** | Key Encapsulation Mechanism |
| **Digital Signature (DSS)** | **ML-DSA-87 (Dilithium-3)** | Integrity and Authentication |

---

## 📦 Installation

1.  **Clone or download this repository:**

    ```bash
    git clone [https://github.com/YourUsername/your-repo-name.git](https://github.com/YourUsername/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install a PQC library** (choose one option):

    ```bash
    # Option 1: Recommended - quantcrypt
    pip install quantcrypt

    # Option 2: Alternative - pqcrypto
    # pip install pqcrypto

    # Option 3: Fallback - Individual packages
    # pip install kyber dilithium
    ```
    > 📝 **Note**: The toolkit includes fallback mechanisms. If the primary library (`quantcrypt`) fails, the toolkit will automatically attempt to use other available PQC libraries.

---

## ✅ Verification

Ensure everything is working correctly by running the comprehensive test script:

```bash
python test_pqc_toolkit.py
````

This test will:

  * ✅ Verify PQC library functionality (ML-KEM-768 and ML-DSA-87).
  * ✅ Test all core toolkit modules (`key_manager`, `encryptor`, `decryptor`).
  * ✅ Run a complete encryption/decryption workflow.

If all tests pass, you are ready to use the toolkit\!

-----

## 🌐 Web Application (Recommended)

The web app provides a modern, user-friendly interface for all encryption and decryption tasks.

### Quick Start (Web App)

1.  **Start the web server:**

    ```bash
    python start_web.py
    ```

2.  **Open your browser:**

    Navigate to `http://localhost:5000`

3.  **Features:**

      * **Key Management**: Generate key pairs for multiple users.
      * **Drag-and-Drop**: Easily upload files for encryption.
      * **Mode Selection**: Choose between **Confidential Encryption** or **Authentication Encryption (Digital Signature)**.
      * **Signature Enforcement**: Toggle verification requirements during decryption.

See the dedicated guide for detailed web application documentation: **[WEB\_APP\_GUIDE.md](https://www.google.com/search?q=WEB_APP_GUIDE.md)**

-----

## 🚀 CLI Usage

The Command Line Interface (CLI) is perfect for scripting and automation.

### 1\. Generate Key Pairs

Generates ML-KEM-768 (KEM) and ML-DSA-87 (DSS) key pairs for a user.

```bash
python main.py keygen <user_id>
```

**Example:**

```bash
python main.py keygen alice
```

This creates the following structure in the `keys/` directory:

```
keys/
└── alice/
    ├── alice_kem_public.key   # For recipient to receive encrypted files
    ├── alice_kem_private.key  # For recipient to decrypt files
    ├── alice_dss_public.key   # For others to verify Alice's signature
    └── alice_dss_private.key  # For Alice to sign files
```

### 2\. Encrypt a File

Encrypts a file using the **recipient's public KEM key**. Optionally, a **signer's private DSS key** can be used to sign the encrypted file for authentication.

```bash
python main.py encrypt <filepath> <recipient_public_kem_key> [--signer-key <signer_private_dss_key>]
```

| Mode | Command Example | Output |
| :--- | :--- | :--- |
| **Confidentiality Only** | `python main.py encrypt doc.pdf keys/alice/alice_kem_public.key` | `doc.pdf.pqc` |
| **Confidentiality & Signature** | `python main.py encrypt doc.pdf keys/alice/alice_kem_public.key --signer-key keys/bob/bob_dss_private.key` | `doc.pdf.pqc` |

### 3\. Decrypt a File

Decrypts a file using the **recipient's private KEM key**.

```bash
python main.py decrypt <encrypted_filepath> <recipient_private_kem_key> [--signer-key <signer_public_dss_key>] [--require-signature]
```

| Mode | Command Example | Result |
| :--- | :--- | :--- |
| **Decryption Only** | `python main.py decrypt doc.pqc keys/alice/alice_kem_private.key` | `doc-decrypted.pdf` |
| **Decryption & Verify** | `python main.py decrypt doc.pqc keys/alice/alice_kem_private.key --signer-key keys/bob/bob_dss_public.key` | Verifies signature, then decrypts. |
| **Verify & Enforce** | `python main.py decrypt doc.pqc ... --signer-key ... --require-signature` | **Rejects** file if unsigned or invalid signature. |

-----

## 📁 File Format (`.pqc`)

The encrypted file format is structured to ensure robust and verifiable security:

| Component | Size (Bytes) | Description |
| :--- | :--- | :--- |
| **Magic Number** | 4 | `PQC1` to identify the file format. |
| **Metadata Header** | $\approx 13$ | Algorithm flags, lengths, and the 12-byte **Nonce** for AES-GCM. |
| **ML-KEM-768 Ciphertext** | Variable | Encrypted session key for the file. |
| **AES-256 GCM Tag** | 16 | Authentication tag for the bulk data. |
| **ML-DSA-87 Signature** | Variable | **(Optional)** Digital signature over the entire envelope. |
| **AES-256 Ciphertext** | Variable | The bulk encrypted file data. |

> **Security Note**: When signatures are used, the signer protects the **entire encrypted envelope** (header, KEM ciphertext, GCM tag, and AES ciphertext) to provide tamper-evident authenticity and provenance.

-----

## 🔒 Security Features

  * **Hybrid Encryption**: Leverages slow, quantum-resistant KEM for the small session key and fast, traditional AES-256-GCM for bulk file encryption.
  * **Authenticated Encryption**: AES-256-GCM provides both **Confidentiality** and **Authenticity** for the file contents.
  * **Digital Signatures**: ML-DSA-87 signatures cover the entire encrypted payload for **Integrity** and **Provenance**.
  * **Quantum-Resistant**: Uses NIST-standardized algorithms (Kyber-768 and Dilithium-3).

-----

## ⚠️ Important Notes

1.  **Key Security**: Private keys must be kept absolutely secure. Loss of a private key results in permanent data loss for encrypted files.
2.  **File Size**: The use of AES-256-GCM ensures efficient, high-performance encryption for files of any size.
3.  **Trust**: Always verify signatures when decrypting files from untrusted sources.

## 📚 References

  * [NIST Post-Quantum Cryptography Standardization](https://csrc.nist.gov/projects/post-quantum-cryptography)
  * [ML-KEM (Kyber) Documentation](https://pq-crystals.org/kyber/)
  * [ML-DSA (Dilithium) Documentation](https://pq-crystals.org/dilithium/)

-----

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! Feel free to open a pull request.

## 📄 License

This project is provided as-is for educational and research purposes.

-----

Would you like me to help you create an initial `WEB_APP_GUIDE.md` based on the features you described, or generate a sample `requirements.txt` file?

