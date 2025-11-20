"""
Post-Quantum Encryption Toolkit - Web Application
Flask-based web interface for the PQC encryption toolkit
"""

import os
import json
import base64
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import tempfile
import shutil

from key_manager import generate_pqc_keys
from encryptor import encrypt_file_hybrid
from decryptor import decrypt_file_hybrid

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['KEYS_FOLDER'] = 'keys'
app.config['TEMP_FOLDER'] = 'temp'

# Create necessary directories
for folder in [app.config['UPLOAD_FOLDER'], app.config['KEYS_FOLDER'], app.config['TEMP_FOLDER']]:
    Path(folder).mkdir(exist_ok=True)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/keys/generate', methods=['POST'])
def api_generate_keys():
    """Generate PQC key pairs for a user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', '').strip()
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID is required'}), 400
        
        # Sanitize user ID
        user_id = secure_filename(user_id)
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid user ID'}), 400
        
        # Generate keys
        key_paths = generate_pqc_keys(user_id, app.config['KEYS_FOLDER'])
        
        # Read keys as base64 for download
        keys_data = {}
        for key_type, key_path in key_paths.items():
            with open(key_path, 'rb') as f:
                keys_data[key_type] = {
                    'filename': Path(key_path).name,
                    'data': base64.b64encode(f.read()).decode('utf-8')
                }
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'keys': keys_data,
            'message': f'Keys generated successfully for {user_id}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/keys/list', methods=['GET'])
def api_list_keys():
    """List all available key pairs"""
    try:
        keys_dir = Path(app.config['KEYS_FOLDER'])
        users = []
        
        if keys_dir.exists():
            for user_dir in keys_dir.iterdir():
                if user_dir.is_dir():
                    user_id = user_dir.name
                    keys = {}
                    for key_file in user_dir.glob('*.key'):
                        key_type = key_file.stem.replace(f'{user_id}_', '').replace('_', '-')
                        keys[key_type] = {
                            'filename': key_file.name,
                            'size': key_file.stat().st_size,
                            'path': str(key_file.relative_to(keys_dir))
                        }
                    
                    if keys:
                        users.append({
                            'user_id': user_id,
                            'keys': keys
                        })
        
        return jsonify({'success': True, 'users': users})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/keys/download/<path:key_path>', methods=['GET'])
def api_download_key(key_path):
    """Download a key file"""
    try:
        # Security: ensure path is within keys folder
        full_path = Path(app.config['KEYS_FOLDER']) / key_path
        keys_folder = Path(app.config['KEYS_FOLDER']).resolve()
        
        if not full_path.resolve().is_relative_to(keys_folder):
            return jsonify({'success': False, 'error': 'Invalid path'}), 400
        
        if not full_path.exists():
            return jsonify({'success': False, 'error': 'Key file not found'}), 404
        
        return send_file(
            str(full_path),
            as_attachment=True,
            download_name=full_path.name
        )
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    """Encrypt a file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Get recipient public key
        recipient_key_file = request.files.get('recipient_key')
        if not recipient_key_file:
            return jsonify({'success': False, 'error': 'Recipient public key is required'}), 400
        
        # Get optional signer private key
        signer_key_file = request.files.get('signer_key')
        
        # Save uploaded files temporarily
        temp_dir = Path(tempfile.mkdtemp(dir=app.config['TEMP_FOLDER']))
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            input_file = temp_dir / filename
            file.save(str(input_file))
            
            # Save recipient key
            recipient_key_path = temp_dir / 'recipient_kem_public.key'
            recipient_key_file.save(str(recipient_key_path))
            
            # Save signer key if provided
            signer_key_path = None
            if signer_key_file and signer_key_file.filename:
                signer_key_path = temp_dir / 'signer_dss_private.key'
                signer_key_file.save(str(signer_key_path))
            
            # Encrypt file
            encrypted_path = encrypt_file_hybrid(
                str(input_file),
                str(recipient_key_path),
                str(signer_key_path) if signer_key_path else None
            )
            
            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = base64.b64encode(f.read()).decode('utf-8')
            
            return jsonify({
                'success': True,
                'filename': Path(encrypted_path).name,
                'data': encrypted_data,
                'message': 'File encrypted successfully',
                'signature_attached': bool(signer_key_path)
            })
        
        finally:
            # Cleanup temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    except RequestEntityTooLarge:
        return jsonify({'success': False, 'error': 'File too large (max 100MB)'}), 413
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """Decrypt a file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Get recipient private key
        recipient_key_file = request.files.get('recipient_key')
        if not recipient_key_file:
            return jsonify({'success': False, 'error': 'Recipient private key is required'}), 400
        
        # Get optional signer public key
        signer_key_file = request.files.get('signer_key')
        
        require_signature = request.form.get('require_signature', 'false').lower() == 'true'
        
        # Save uploaded files temporarily
        temp_dir = Path(tempfile.mkdtemp(dir=app.config['TEMP_FOLDER']))
        
        try:
            # Save uploaded encrypted file
            filename = secure_filename(file.filename)
            encrypted_file = temp_dir / filename
            file.save(str(encrypted_file))
            
            # Save recipient key
            recipient_key_path = temp_dir / 'recipient_kem_private.key'
            recipient_key_file.save(str(recipient_key_path))
            
            # Save signer key if provided
            signer_key_path = None
            if signer_key_file and signer_key_file.filename:
                signer_key_path = temp_dir / 'signer_dss_public.key'
                signer_key_file.save(str(signer_key_path))
            
            # Decrypt file
            decrypted_result = decrypt_file_hybrid(
                str(encrypted_file),
                str(recipient_key_path),
                str(signer_key_path) if signer_key_path else None,
                require_signature=require_signature,
                return_metadata=True
            )
            
            if isinstance(decrypted_result, tuple):
                decrypted_path, metadata = decrypted_result
            else:
                decrypted_path = decrypted_result
                metadata = {
                    'signature_present': False,
                    'signature_verified': None
                }
            
            # Read decrypted file
            with open(decrypted_path, 'rb') as f:
                decrypted_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Determine original filename
            original_filename = Path(decrypted_path).name
            
            return jsonify({
                'success': True,
                'filename': original_filename,
                'data': decrypted_data,
                'message': 'File decrypted successfully',
                'signature': metadata
            })
        
        finally:
            # Cleanup temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    except RequestEntityTooLarge:
        return jsonify({'success': False, 'error': 'File too large (max 100MB)'}), 413
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    try:
        # Try to import PQC library
        try:
            from quantcrypt import kem, dss
            pqc_status = 'quantcrypt available'
        except ImportError:
            pqc_status = 'PQC library check needed'
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'pqc_library': pqc_status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Post-Quantum Encryption Toolkit - Web Application")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

