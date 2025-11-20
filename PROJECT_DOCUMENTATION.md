# Post-Quantum Encryption Toolkit - Complete Project Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Post-Quantum Algorithms](#post-quantum-algorithms)
4. [Project Architecture](#project-architecture)
5. [How the Project Works](#how-the-project-works)
6. [Architecture Diagrams](#architecture-diagrams)
7. [Flow Diagrams](#flow-diagrams)
8. [File Format Specification](#file-format-specification)

---

## Project Overview

The **Post-Quantum Encryption Toolkit** is a comprehensive file encryption/decryption system designed to protect data against future quantum computer attacks. It implements a hybrid cryptosystem that combines post-quantum cryptography (PQC) with classical symmetric encryption for optimal security and performance.

### Key Features

- **Quantum-Resistant Encryption**: Uses NIST-standardized post-quantum algorithms
- **Hybrid Cryptosystem**: Combines PQC key exchange with AES-256-GCM for efficiency
- **Dual Interface**: Web application (Flask) and Command-Line Interface (CLI)
- **Digital Signatures**: Enforceable ML-DSA-87 signatures covering the entire encrypted envelope for authentication
- **Web Modes**: UI toggles let users pick Confidential-only encryption or add Authentication Encryption (digital signature) on demand
- **Multi-Library Support**: Works with multiple PQC library implementations

---

## Technologies Used

### Backend Technologies

#### 1. **Python 3.10+**
   - Primary programming language
   - Provides cryptographic primitives and libraries

#### 2. **Flask 3.0+**
   - Web framework for the web application
   - Handles HTTP requests, routing, and file uploads
   - Provides RESTful API endpoints

#### 3. **Werkzeug 3.0+**
   - WSGI utility library (used by Flask)
   - Handles secure file uploads and path validation
   - Provides security utilities

#### 4. **Cryptography Library (cryptography>=41.0.0)**
   - Provides AES-256-GCM symmetric encryption
   - Implements HKDF (HMAC-based Key Derivation Function)
   - Handles secure random number generation

#### 5. **Post-Quantum Cryptography Libraries** (One of the following)
   - **quantcrypt** (Primary): Comprehensive PQC library with ML-KEM-768 and ML-DSA-87
   - **pqcrypto**: Alternative PQC library
   - **kyber + dilithium**: Individual packages for KEM and DSS

### Frontend Technologies

#### 1. **HTML5**
   - Semantic markup for web interface
   - File input elements for uploads

#### 2. **CSS3**
   - Modern styling with gradients and glassmorphism
   - Responsive design for multiple devices
   - Font Awesome icons integration

#### 3. **JavaScript (Vanilla)**
   - Client-side form handling
   - AJAX requests to Flask API
   - File download management
   - Dynamic UI updates

### Development Tools

#### 1. **argparse**
   - Command-line argument parsing for CLI

#### 2. **pathlib**
   - Modern file path handling

#### 3. **struct**
   - Binary data packing/unpacking for file format

#### 4. **base64**
   - Encoding/decoding for web API responses

---

## Post-Quantum Algorithms

### 1. ML-KEM-768 (Module-Lattice Key Encapsulation Mechanism)

**Also Known As**: Kyber-768

**Type**: Key Encapsulation Mechanism (KEM)

**Purpose**: Secure key exchange that is resistant to quantum computer attacks

**Security Level**: 
- NIST Security Level 3 (equivalent to AES-192)
- Resistant to both classical and quantum attacks

**How It Works**:
- Based on **Module-Learning-with-Errors (MLWE)** problem
- Uses lattice-based cryptography
- Generates a shared secret between two parties without direct key transmission

**Key Sizes**:
- Public Key: ~1,184 bytes
- Private Key: ~2,400 bytes
- Ciphertext: ~1,088 bytes
- Shared Secret: 32 bytes (derived for AES-256)

**Usage in Project**:
- **Encryption**: Encapsulates a shared secret using recipient's public key
- **Decryption**: Decapsulates the shared secret using recipient's private key
- The shared secret becomes the AES-256 session key

**NIST Standardization**: 
- Selected as the primary KEM algorithm in NIST PQC Standardization (FIPS 203)

---

### 2. ML-DSA-87 (Module-Lattice Digital Signature Algorithm)

**Also Known As**: Dilithium-3

**Type**: Digital Signature Scheme (DSS)

**Purpose**: Provides digital signatures for authentication and non-repudiation

**Security Level**:
- NIST Security Level 3
- Quantum-resistant signature scheme

**How It Works**:
- Based on **Module-Learning-with-Errors (MLWE)** and **Module-Small Integer Solution (MSIS)** problems
- Uses lattice-based cryptography
- Provides unforgeable signatures

**Key Sizes**:
- Public Key: ~1,952 bytes
- Private Key: ~4,000 bytes
- Signature: ~3,293 bytes

**Usage in Project**:
- **Encryption**: Signs the encrypted data using signer's private key (optional)
- **Decryption**: Verifies the signature using signer's public key (optional)
- Provides integrity and authenticity verification

**NIST Standardization**:
- Selected as the primary signature algorithm in NIST PQC Standardization (FIPS 204)

---

### 3. AES-256-GCM (Classical Symmetric Encryption)

**Type**: Authenticated Encryption with Associated Data (AEAD)

**Purpose**: Efficient bulk file encryption

**Note**: This is **NOT** a post-quantum algorithm, but is used for performance

**How It Works**:
- AES-256 (Advanced Encryption Standard) with 256-bit keys
- GCM (Galois/Counter Mode) provides authenticated encryption
- Combines encryption and authentication in one operation

**Why Hybrid Approach?**
- Post-quantum algorithms are slower for large files
- AES-256-GCM is extremely fast for bulk encryption
- Only the small session key is protected by post-quantum cryptography
- Provides best of both worlds: quantum-resistance + performance

---

## Project Architecture

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Post-Quantum Encryption Toolkit               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────┐         ┌──────────────────────┐      │
│  │   Web Interface      │         │   CLI Interface      │      │
│  │   (Flask App)        │         │   (main.py)          │      │
│  └──────────┬───────────┘         └──────────┬───────────┘      │
│             │                                 │                  │
│             └──────────────┬──────────────────┘                  │
│                            │                                     │
│                  ┌─────────▼──────────┐                          │
│                  │   Core Modules    │                          │
│                  └─────────┬──────────┘                          │
│                            │                                     │
│        ┌───────────────────┼───────────────────┐                 │
│        │                   │                   │                 │
│  ┌─────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐         │
│  │  Key       │    │  Encryptor   │    │  Decryptor   │         │
│  │  Manager  │    │              │    │              │         │
│  └─────┬──────┘    └──────┬───────┘    └──────┬───────┘         │
│        │                   │                   │                 │
│        └───────────────────┼───────────────────┘                 │
│                            │                                     │
│                  ┌─────────▼──────────┐                          │
│                  │  PQC Libraries     │                          │
│                  │  (quantcrypt/      │                          │
│                  │   pqcrypto/         │                          │
│                  │   kyber+dilithium) │                          │
│                  └────────────────────┘                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Module Structure

```
Post-Quantum Encryption Toolkit/
│
├── app.py                    # Flask web application
├── start_web.py             # Web server startup script
├── main.py                  # CLI entry point
│
├── Core Modules:
│   ├── key_manager.py       # Key generation (ML-KEM-768 & ML-DSA-87)
│   ├── encryptor.py         # Hybrid encryption implementation
│   └── decryptor.py         # Hybrid decryption implementation
│
├── Web Interface:
│   ├── templates/
│   │   └── index.html       # Main web UI
│   └── static/
│       ├── style.css        # Styling
│       └── script.js        # Frontend JavaScript
│
├── Data Directories:
│   ├── keys/                # Generated key pairs storage
│   ├── uploads/             # Temporary file uploads
│   └── temp/                # Temporary processing files
│
└── Dependencies:
    └── requirements.txt      # Python package dependencies
```

### Component Responsibilities

#### 1. **key_manager.py**
- Generates ML-KEM-768 key pairs (public/private)
- Generates ML-DSA-87 key pairs (public/private)
- Stores keys in organized directory structure
- Supports multiple PQC library backends

#### 2. **encryptor.py**
- Implements hybrid encryption workflow
- Uses ML-KEM-768 for key encapsulation
- Uses AES-256-GCM for file encryption
- Optionally signs with ML-DSA-87
- Creates `.pqc` file format

#### 3. **decryptor.py**
- Implements hybrid decryption workflow
- Uses ML-KEM-768 for key decapsulation
- Uses AES-256-GCM for file decryption
- Optionally verifies ML-DSA-87 signatures
- Parses `.pqc` file format

#### 4. **app.py** (Web Interface)
- Flask web server
- RESTful API endpoints
- File upload/download handling
- Key management UI

#### 5. **main.py** (CLI Interface)
- Command-line argument parsing
- Orchestrates key generation, encryption, decryption
- User-friendly CLI interface

---

## How the Project Works

### Complete Workflow

#### Phase 1: Key Generation

```
User → key_manager.py → PQC Library → Key Pairs
```

1. User provides a unique identifier (e.g., "alice")
2. `key_manager.py` calls the PQC library
3. **ML-KEM-768 key generation**:
   - Generates public key (can be shared)
   - Generates private key (must be kept secret)
4. **ML-DSA-87 key generation**:
   - Generates public key (can be shared)
   - Generates private key (must be kept secret)
5. Keys are saved to `keys/<user_id>/` directory

#### Phase 2: Encryption Process

```
Plaintext File → Hybrid Encryption → Encrypted .pqc File
```

**Step-by-Step Encryption**:

1. **Read Input File**
   - Read the plaintext file to be encrypted

2. **Key Encapsulation (ML-KEM-768)**
   ```
   Recipient's Public KEM Key + Randomness
   → ML-KEM-768 Encapsulation
   → KEM Ciphertext + Shared Secret (32 bytes)
   ```
   - The shared secret will become the AES-256 key

3. **Symmetric Encryption (AES-256-GCM)**
   ```
   Plaintext File + Shared Secret (AES Key) + Random Nonce
   → AES-256-GCM Encryption
   → AES Ciphertext + GCM Authentication Tag (16 bytes)
   ```

4. **Optional Digital Signature (ML-DSA-87)**
   ```
   Header Metadata + KEM Ciphertext + GCM Tag + AES Ciphertext + Signer's Private DSS Key
   → ML-DSA-87 Signing
   → Digital Signature
   ```

5. **Create .pqc File**
   - Assemble all components into binary format
   - Save as `<filename>.pqc`

#### Phase 3: Decryption Process

```
Encrypted .pqc File → Hybrid Decryption → Plaintext File
```

**Step-by-Step Decryption**:

1. **Parse .pqc File**
   - Read magic number (verify format)
   - Extract metadata (sizes, nonce, algorithm flags)
   - Extract KEM ciphertext, GCM tag, signature, AES ciphertext

2. **Key Decapsulation (ML-KEM-768)**
   ```
   KEM Ciphertext + Recipient's Private KEM Key
   → ML-KEM-768 Decapsulation
   → Recovered Shared Secret (32 bytes)
   ```

3. **Optional Signature Verification (ML-DSA-87)**
   ```
   Header Metadata + KEM Ciphertext + GCM Tag + AES Ciphertext + Signature + Signer's Public DSS Key
   → ML-DSA-87 Verification
   → Valid/Invalid (raises error if invalid; `--require-signature` / web toggle can enforce presence)
   ```

4. **Symmetric Decryption (AES-256-GCM)**
   ```
   AES Ciphertext + GCM Tag + Shared Secret (AES Key) + Nonce
   → AES-256-GCM Decryption
   → Plaintext File
   ```

5. **Save Decrypted File**
   - Save as `<original_filename>-decrypted.<extension>`

---

## Architecture Diagrams

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
├──────────────────────────────┬──────────────────────────────────────┤
│                              │                                      │
│    ┌──────────────────┐      │      ┌──────────────────┐           │
│    │  Web Browser     │      │      │  Terminal/CLI     │           │
│    │  (HTML/CSS/JS)   │      │      │  (Command Line)   │           │
│    └────────┬─────────┘      │      └────────┬─────────┘           │
│             │                │               │                      │
│             │ HTTP Requests  │               │ CLI Commands         │
│             │                │               │                      │
└─────────────┼────────────────┼───────────────┼──────────────────────┘
              │                │               │
              ▼                ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                              │
├──────────────────────────────┬──────────────────────────────────────┤
│                              │                                      │
│    ┌──────────────────┐      │      ┌──────────────────┐           │
│    │   Flask Web App  │      │      │   CLI Handler     │           │
│    │   (app.py)       │      │      │   (main.py)      │           │
│    │                  │      │      │                  │           │
│    │  - Routes        │      │      │  - Argparse      │           │
│    │  - API Endpoints │      │      │  - Validation    │           │
│    │  - File Handling │      │      │  - Orchestration │           │
│    └────────┬─────────┘      │      └────────┬─────────┘           │
│             │                │               │                      │
└─────────────┼────────────────┼───────────────┼──────────────────────┘
              │                │               │
              └────────────────┼───────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        CORE MODULES LAYER                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Key        │  │  Encryptor   │  │  Decryptor   │             │
│  │   Manager    │  │              │  │              │             │
│  │              │  │              │  │              │             │
│  │ - Key Gen    │  │ - KEM        │  │ - KEM        │             │
│  │ - Storage    │  │   Encaps     │  │   Decaps     │             │
│  │ - Management │  │ - AES Encrypt│  │ - AES Decrypt│             │
│  │              │  │ - DSS Sign    │  │ - DSS Verify │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                 │                 │                      │
└─────────┼─────────────────┼─────────────────┼──────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CRYPTOGRAPHY LIBRARIES LAYER                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  PQC Libraries   │  │  Cryptography    │  │  Standard        │ │
│  │                  │  │  Library         │  │  Library         │ │
│  │ - quantcrypt     │  │                  │  │                  │ │
│  │ - pqcrypto       │  │ - AES-256-GCM    │  │ - struct         │ │
│  │ - kyber          │  │ - HKDF           │  │ - base64         │ │
│  │ - dilithium      │  │ - Random         │  │ - pathlib        │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Module Interaction Diagram

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ 1. Generate Keys Request
       ▼
┌─────────────────┐
│  key_manager.py │
│                 │
│  generate_pqc_  │
│  keys()         │
└────┬────────────┘
     │
     │ 2. Call PQC Library
     ▼
┌─────────────────┐
│  PQC Library    │
│  (quantcrypt/   │
│   pqcrypto)     │
│                 │
│  - ML-KEM-768   │
│    keygen()     │
│  - ML-DSA-87    │
│    keygen()     │
└────┬────────────┘
     │
     │ 3. Return Key Pairs
     ▼
┌─────────────────┐
│  key_manager.py │
│                 │
│  Save keys to   │
│  keys/<user>/   │
└─────────────────┘

┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ 4. Encrypt File Request
       ▼
┌─────────────────┐
│  encryptor.py   │
│                 │
│  encrypt_file_  │
│  hybrid()       │
└────┬────────────┘
     │
     │ 5. Read Recipient's Public KEM Key
     │
     │ 6. ML-KEM-768 Encapsulation
     ▼
┌─────────────────┐
│  PQC Library    │
│                 │
│  ML-KEM-768     │
│  encaps()       │
│                 │
│  Returns:       │
│  - Ciphertext   │
│  - Shared Secret│
└────┬────────────┘
     │
     │ 7. Use Shared Secret as AES Key
     │
     │ 8. AES-256-GCM Encryption
     ▼
┌─────────────────┐
│  Cryptography   │
│  Library        │
│                 │
│  AESGCM.encrypt()│
│                 │
│  Returns:       │
│  - Ciphertext   │
│  - GCM Tag      │
└────┬────────────┘
     │
     │ 9. Optional: ML-DSA-87 Signing
     │
     │ 10. Assemble .pqc File
     ▼
┌─────────────────┐
│  encryptor.py   │
│                 │
│  Write .pqc     │
│  file format    │
└─────────────────┘
```

---

## Flow Diagrams

### Complete Encryption Flow

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │  Read Plaintext File   │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Read Recipient's       │
         │ Public KEM Key         │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ ML-KEM-768             │
         │ Encapsulation          │
         │                        │
         │ Input: Public Key      │
         │ Output:                │
         │  - KEM Ciphertext      │
         │  - Shared Secret       │
         │    (32 bytes)          │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Derive AES-256 Key     │
         │ from Shared Secret     │
         │ (Use HKDF if needed)    │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Generate Random Nonce  │
         │ (12 bytes for GCM)     │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ AES-256-GCM Encryption │
         │                        │
         │ Input:                 │
         │  - Plaintext           │
         │  - AES Key (32 bytes)  │
         │  - Nonce (12 bytes)    │
         │                        │
         │ Output:                │
         │  - AES Ciphertext      │
         │  - GCM Tag (16 bytes)  │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Optional: Sign with    │
         │ ML-DSA-87?            │
         └────────────┬───────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
          YES                  NO
            │                   │
            ▼                   ▼
   ┌──────────────┐    ┌──────────────┐
   │ Read Signer's│    │ Skip Signing │
   │ Private DSS  │    │              │
   │ Key          │    │              │
   └──────┬───────┘    └──────┬───────┘
          │                   │
          ▼                   │
   ┌──────────────┐           │
   │ ML-DSA-87    │           │
   │ Signing      │           │
   │              │           │
   │ Input:       │           │
   │  - AES       │           │
   │    Ciphertext│           │
   │  - Private   │           │
   │    DSS Key   │           │
   │              │           │
   │ Output:      │           │
   │  - Signature │           │
   └──────┬───────┘           │
          │                   │
          └─────────┬─────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ Assemble .pqc File      │
         │                        │
         │ Format:                │
         │  1. Magic (4 bytes)    │
         │  2. Metadata Header    │
         │  3. KEM Ciphertext     │
         │  4. GCM Tag            │
         │  5. Signature (if any) │
         │  6. AES Ciphertext     │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Write .pqc File       │
         │ <filename>.pqc        │
         └────────────┬───────────┘
                      │
                      ▼
                     END
```

### Complete Decryption Flow

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │ Read .pqc File         │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Verify Magic Number    │
         │ (Must be "PQC1")       │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Parse File Header      │
         │                        │
         │ Extract:               │
         │  - Algorithm flags     │
         │  - KEM CT length       │
         │  - GCM tag length      │
         │  - Signature length    │
         │  - Nonce (12 bytes)    │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Extract Components    │
         │                        │
         │  - KEM Ciphertext      │
         │  - GCM Tag            │
         │  - Signature (if any) │
         │  - AES Ciphertext     │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Read Recipient's       │
         │ Private KEM Key        │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ ML-KEM-768             │
         │ Decapsulation          │
         │                        │
         │ Input:                 │
         │  - KEM Ciphertext      │
         │  - Private KEM Key     │
         │                        │
         │ Output:                │
         │  - Shared Secret       │
         │    (32 bytes)          │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Derive AES-256 Key     │
         │ from Shared Secret     │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Signature Present?     │
         └────────────┬───────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
          YES                  NO
            │                   │
            ▼                   │
   ┌──────────────┐             │
   │ Read Signer's│             │
   │ Public DSS   │             │
   │ Key          │             │
   └──────┬───────┘             │
          │                     │
          ▼                     │
   ┌──────────────┐             │
   │ ML-DSA-87    │             │
   │ Verification │             │
   │              │             │
   │ Input:       │             │
   │  - AES       │             │
   │    Ciphertext│             │
   │  - Signature │             │
   │  - Public    │             │
   │    DSS Key   │             │
   │              │             │
   │ Output:      │             │
   │  - Valid/    │             │
   │    Invalid   │             │
   └──────┬───────┘             │
          │                     │
          ▼                     │
   ┌──────────────┐             │
   │ Signature    │             │
   │ Valid?       │             │
   └──────┬───────┘             │
          │                     │
    ┌─────┴─────┐               │
    │           │               │
   YES         NO               │
    │           │               │
    │           ▼               │
    │   ┌──────────────┐        │
    │   │ Raise Error  │        │
    │   │ (Tampered!)  │        │
    │   └──────────────┘        │
    │                           │
    └───────────┬───────────────┘
                │
                ▼
         ┌────────────────────────┐
         │ AES-256-GCM Decryption │
         │                        │
         │ Input:                 │
         │  - AES Ciphertext      │
         │  - GCM Tag            │
         │  - AES Key (32 bytes)  │
         │  - Nonce (12 bytes)    │
         │                        │
         │ Output:                │
         │  - Plaintext File      │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Write Decrypted File  │
         │ <filename>-decrypted  │
         │   .<extension>        │
         └────────────┬───────────┘
                      │
                      ▼
                     END
```

### Key Generation Flow

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │ User Provides User ID  │
         │ (e.g., "alice")        │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ key_manager.py         │
         │ generate_pqc_keys()    │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Detect PQC Library    │
         │ (quantcrypt/pqcrypto/ │
         │  kyber+dilithium)     │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ ML-KEM-768 Key Gen     │
         │                        │
         │ PQC Library:           │
         │  keygen()              │
         │                        │
         │ Output:                │
         │  - Public KEM Key      │
         │    (~1,184 bytes)      │
         │  - Private KEM Key    │
         │    (~2,400 bytes)      │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ ML-DSA-87 Key Gen      │
         │                        │
         │ PQC Library:           │
         │  keygen()              │
         │                        │
         │ Output:                │
         │  - Public DSS Key      │
         │    (~1,952 bytes)      │
         │  - Private DSS Key     │
         │    (~4,000 bytes)      │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Save Keys to Disk     │
         │                        │
         │ Directory Structure:  │
         │  keys/<user_id>/      │
         │    ├── <user>_kem_    │
         │    │   public.key     │
         │    ├── <user>_kem_    │
         │    │   private.key    │
         │    ├── <user>_dss_    │
         │    │   public.key     │
         │    └── <user>_dss_    │
         │        private.key    │
         └────────────┬───────────┘
                      │
                      ▼
                     END
```

### Web Application Request Flow

```
                    CLIENT (Browser)
                         │
                         │ HTTP Request
                         ▼
         ┌───────────────────────────────┐
         │      Flask Web Server         │
         │      (app.py)                 │
         └───────────────┬───────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  /api/keys/  │  │ /api/encrypt │  │ /api/decrypt │
│  generate    │  │              │  │              │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ key_manager  │  │  encryptor    │  │  decryptor   │
│ .py          │  │  .py          │  │  .py          │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │      PQC Libraries            │
         │      Cryptography Library     │
         └───────────────┬───────────────┘
                         │
                         │ Process
                         ▼
         ┌───────────────────────────────┐
         │      Flask Response            │
         │      (JSON/File Download)      │
         └───────────────┬───────────────┘
                         │
                         │ HTTP Response
                         ▼
                    CLIENT (Browser)
```

---

## File Format Specification

### .pqc File Format

The encrypted file format is a binary structure that contains all necessary components for decryption:

```
┌─────────────────────────────────────────────────────────────┐
│                    .pqc File Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Offset  │  Size   │  Component        │  Description        │
├──────────┼─────────┼──────────────────┼─────────────────────┤
│  0x0000  │  4      │  Magic Number    │  "PQC1" (0x50514331)│
│  0x0004  │  1      │  Algorithm Flags │  Bit flags:         │
│          │         │                  │  - Bit 0: ML-KEM-768 │
│          │         │                  │  - Bit 1: ML-DSA-87 │
│          │         │                  │  - Bit 2: AES-256   │
│  0x0005  │  4      │  KEM CT Length   │  Length of KEM      │
│          │         │                  │  ciphertext (bytes) │
│  0x0009  │  4      │  GCM Tag Length  │  Length of GCM tag │
│          │         │                  │  (usually 16)      │
│  0x000D  │  4      │  Signature Length│  Length of signature│
│          │         │                  │  (0 if not signed)  │
│  0x0011  │  12     │  Nonce           │  Random nonce for   │
│          │         │                  │  AES-GCM            │
│  0x001D  │  var    │  KEM Ciphertext  │  ML-KEM-768         │
│          │         │                  │  encapsulated key   │
│          │         │                  │  (~1,088 bytes)     │
│  var     │  16     │  GCM Tag         │  AES-GCM             │
│          │         │                  │  authentication tag │
│  var     │  var    │  Signature       │  ML-DSA-87 signature│
│          │         │                  │  (if present,       │
│          │         │                  │   ~3,293 bytes)     │
│  var     │  var    │  AES Ciphertext  │  Encrypted file     │
│          │         │                  │  content            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Binary Layout Example

For a file with signature:
```
[Magic: 4 bytes] [Flags: 1 byte] [KEM_CT_Len: 4 bytes] 
[GCM_Tag_Len: 4 bytes] [Sig_Len: 4 bytes] [Nonce: 12 bytes]
[KEM_Ciphertext: variable] [GCM_Tag: 16 bytes] 
[Signature: variable] [AES_Ciphertext: variable]
```

For a file without signature:
```
[Magic: 4 bytes] [Flags: 1 byte] [KEM_CT_Len: 4 bytes] 
[GCM_Tag_Len: 4 bytes] [Sig_Len: 0] [Nonce: 12 bytes]
[KEM_Ciphertext: variable] [GCM_Tag: 16 bytes] 
[AES_Ciphertext: variable]
```

### File Format Constants

```python
PQC_FILE_MAGIC = b'PQC1'              # Magic number identifier
ALGORITHM_KEM_MLKEM768 = 0x01          # ML-KEM-768 flag
ALGORITHM_DSS_MLDSA87 = 0x02           # ML-DSA-87 flag
ALGORITHM_SYM_AES256GCM = 0x03         # AES-256-GCM flag
```

---

## Security Considerations

### Hybrid Cryptosystem Benefits

1. **Quantum Resistance**: The session key is protected by post-quantum cryptography
2. **Performance**: Large files are encrypted efficiently with AES-256-GCM
3. **Authenticity**: GCM mode provides authentication, preventing tampering
4. **Non-Repudiation**: Optional ML-DSA-87 signatures provide proof of origin

### Key Management Best Practices

1. **Private Keys**: Never share or transmit private keys
2. **Key Storage**: Store keys in secure, encrypted storage
3. **Key Backup**: Maintain secure backups of private keys
4. **Key Rotation**: Periodically generate new key pairs

### Threat Model

This toolkit protects against:
- **Future Quantum Attacks**: Post-quantum algorithms resist quantum computers
- **Classical Attacks**: AES-256-GCM provides strong classical security
- **Tampering**: GCM authentication and optional signatures detect modifications
- **Replay Attacks**: Random nonces prevent replay attacks

---

## API Reference

### Web API Endpoints

#### 1. Generate Keys
```
POST /api/keys/generate
Content-Type: application/json

Request Body:
{
  "user_id": "alice"
}

Response:
{
  "success": true,
  "user_id": "alice",
  "keys": {
    "kem_public": {...},
    "kem_private": {...},
    "dss_public": {...},
    "dss_private": {...}
  }
}
```

#### 2. List Keys
```
GET /api/keys/list

Response:
{
  "success": true,
  "users": [
    {
      "user_id": "alice",
      "keys": {...}
    }
  ]
}
```

#### 3. Encrypt File
```
POST /api/encrypt
Content-Type: multipart/form-data

Form Data:
- file: <file to encrypt>
- recipient_key: <public KEM key>
- signer_key: <private DSS key> (optional)

Response:
{
  "success": true,
  "filename": "document.pdf.pqc",
  "data": "<base64 encoded file>"
}
```

#### 4. Decrypt File
```
POST /api/decrypt
Content-Type: multipart/form-data

Form Data:
- file: <encrypted .pqc file>
- recipient_key: <private KEM key>
- signer_key: <public DSS key> (optional)

Response:
{
  "success": true,
  "filename": "document-decrypted.pdf",
  "data": "<base64 encoded file>"
}
```

---

## Conclusion

The Post-Quantum Encryption Toolkit provides a comprehensive solution for quantum-resistant file encryption. By combining NIST-standardized post-quantum algorithms (ML-KEM-768 and ML-DSA-87) with efficient classical encryption (AES-256-GCM), it offers both security and performance.

The hybrid approach ensures that:
- **Small session keys** are protected by post-quantum cryptography
- **Large files** are encrypted efficiently with AES-256-GCM
- **Authentication** is provided through GCM tags and optional signatures
- **Future-proof** security against quantum computer attacks

This toolkit is suitable for protecting sensitive data that needs to remain secure even in the era of quantum computing.

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Project**: Post-Quantum Encryption Toolkit

