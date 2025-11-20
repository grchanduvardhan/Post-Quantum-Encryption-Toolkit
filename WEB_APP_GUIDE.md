# Post-Quantum Encryption Toolkit - Web Application Guide

## 🌐 Web Application Overview

The Post-Quantum Encryption Toolkit now includes a beautiful, modern web interface that makes it easy to encrypt and decrypt files using post-quantum cryptography without using the command line.

## 🚀 Quick Start

### 1. Install Dependencies

Make sure you have Python 3.12 and the virtual environment activated:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install web dependencies
pip install -r requirements.txt
```

### 2. Start the Web Server

**Option A: Using the startup script (recommended)**
```powershell
python start_web.py
```

**Option B: Direct Flask command**
```powershell
python app.py
```

### 3. Open in Browser

Once the server starts, open your web browser and navigate to:
```
http://localhost:5000
```

## 📱 Features

### 1. **Key Management Tab**
- **Generate New Key Pairs**: Create ML-KEM-768 and ML-DSA-87 key pairs for any user
- **View Existing Keys**: See all generated key pairs in one place
- **Download Keys**: Download individual keys with one click

### 2. **Encrypt Tab**
- **File Upload**: Select any file to encrypt (up to 100MB)
- **Recipient Key**: Upload the recipient's public KEM key
- **Modes**:
  - **Confidential Encryption**: Encrypt without attaching a signature
  - **Authentication Encryption**: Add a digital signature using your private DSS key
- **Automatic Download**: Encrypted file downloads automatically after encryption

### 3. **Decrypt Tab**
- **Encrypted File Upload**: Select a `.pqc` encrypted file
- **Private Key**: Upload your private KEM key
- **Modes**:
  - **Confidential Decryption**: Skip verification for speed or offline files
  - **Authentication Decryption**: Verify the signature using the signer's public DSS key with an optional **Require valid digital signature** toggle
- **Automatic Download**: Decrypted file downloads automatically after decryption

## 🎨 User Interface

The web interface features:
- **Modern Design**: Beautiful gradient backgrounds and glassmorphism effects
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Intuitive Navigation**: Easy-to-use tabs for different operations
- **Real-time Feedback**: Notifications for success, errors, and warnings
- **File Management**: Automatic file downloads and organized key storage

## 🔒 Security Features

- **Secure File Handling**: Files are processed in temporary directories and cleaned up automatically
- **Path Validation**: All file paths are validated to prevent directory traversal attacks
- **Size Limits**: Maximum file size of 100MB to prevent resource exhaustion
- **Key Isolation**: Each user's keys are stored in separate directories

## 📋 Usage Examples

### Example 1: Generate Keys for Alice

1. Go to **Key Management** tab
2. Enter "alice" in the User ID field
3. Click **Generate Keys**
4. All four keys (KEM public/private, DSS public/private) will download automatically

### Example 2: Encrypt a File for Bob

1. Go to **Encrypt** tab
2. Select the file you want to encrypt
3. Upload Bob's public KEM key (`bob_kem_public.key`)
4. Choose **Confidential** or **Authentication** mode
5. (If Authentication) Upload your private DSS key to sign the file
6. Click **Encrypt File**
7. The encrypted `.pqc` file will download automatically

### Example 3: Decrypt a File

1. Go to **Decrypt** tab
2. Select the encrypted `.pqc` file
3. Upload your private KEM key
4. Select **Confidential** or **Authentication** mode
5. (If Authentication) Upload the signer's public DSS key and decide whether to require the signature
6. Click **Decrypt File**
7. The decrypted file will download automatically

## 🛠️ Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla, no frameworks)
- **File Handling**: Werkzeug for secure file uploads
- **API**: RESTful API endpoints for all operations

### API Endpoints

- `GET /` - Main web interface
- `POST /api/keys/generate` - Generate new key pairs
- `GET /api/keys/list` - List all existing keys
- `GET /api/keys/download/<path>` - Download a key file
- `POST /api/encrypt` - Encrypt a file
- `POST /api/decrypt` - Decrypt a file
- `GET /api/health` - Health check endpoint

### File Structure

```
.
├── app.py                 # Flask web application
├── start_web.py          # Startup script
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── style.css         # Modern styling
│   └── script.js         # Frontend JavaScript
├── uploads/              # Temporary upload directory
├── keys/                 # Key storage directory
└── temp/                 # Temporary processing directory
```

## ⚙️ Configuration

You can modify these settings in `app.py`:

- **Port**: Change `port=5000` to use a different port
- **Host**: Change `host='0.0.0.0'` to restrict access
- **Max File Size**: Change `MAX_CONTENT_LENGTH` (default: 100MB)
- **Debug Mode**: Set `debug=False` for production

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install Flask
```

### "Port 5000 already in use"
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "File too large" error
Increase the max file size in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB
```

### Keys not showing up
- Make sure keys are in the `keys/` directory
- Check browser console for JavaScript errors
- Verify the Flask server is running

## 🔐 Security Best Practices

1. **Never share private keys**: Private keys should never be uploaded or shared
2. **Use HTTPS in production**: For production use, set up HTTPS/SSL
3. **Restrict access**: Don't expose the server to the public internet without proper security
4. **Regular cleanup**: The `temp/` directory is cleaned automatically, but you can manually clean it if needed
5. **Backup keys**: Always backup your keys in a secure location

## 📝 Notes

- The web application uses the same encryption/decryption modules as the CLI tool
- All encrypted files are compatible between web and CLI versions
- Keys generated via web interface can be used with CLI and vice versa
- The web server runs in debug mode by default (change for production)

## 🎯 Next Steps

1. **Production Deployment**: Set up proper WSGI server (gunicorn, uWSGI)
2. **HTTPS**: Configure SSL/TLS certificates
3. **Authentication**: Add user authentication if needed
4. **Database**: Store key metadata in a database
5. **Cloud Storage**: Integrate with cloud storage for file handling

---

**Enjoy using the Post-Quantum Encryption Toolkit Web Interface!** 🚀

