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
