// JavaScript for Post-Quantum Encryption Toolkit Web Interface

// Tab switching
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });

    // Load existing keys on page load
    loadKeys();

    // Initialize mode toggles
    setupModeToggles();
});

function setupModeToggles() {
    const encryptRadios = document.querySelectorAll('input[name="encrypt-mode"]');
    const encryptSignerGroup = document.getElementById('encrypt-signer-group');
    const encryptSignerInput = document.getElementById('encrypt-signer-key');

    if (encryptRadios.length && encryptSignerGroup) {
        const updateEncryptMode = () => {
            const selected = document.querySelector('input[name="encrypt-mode"]:checked');
            const mode = selected ? selected.value : 'confidential';
            const authenticated = mode === 'authenticated';
            encryptSignerGroup.classList.toggle('hidden', !authenticated);
            if (!authenticated && encryptSignerInput) {
                encryptSignerInput.value = '';
            }
        };
        encryptRadios.forEach(radio => radio.addEventListener('change', updateEncryptMode));
        updateEncryptMode();
    }

    const decryptRadios = document.querySelectorAll('input[name="decrypt-mode"]');
    const decryptSignerGroup = document.getElementById('decrypt-signer-group');
    const decryptSignerInput = document.getElementById('decrypt-signer-key');
    const decryptRequireGroup = document.getElementById('decrypt-require-group');
    const decryptRequireInput = document.getElementById('decrypt-require-signature');

    if (decryptRadios.length && decryptSignerGroup && decryptRequireGroup) {
        const updateDecryptMode = () => {
            const selected = document.querySelector('input[name="decrypt-mode"]:checked');
            const mode = selected ? selected.value : 'confidential';
            const authenticated = mode === 'authenticated';
            decryptSignerGroup.classList.toggle('hidden', !authenticated);
            decryptRequireGroup.classList.toggle('hidden', !authenticated);
            if (!authenticated) {
                if (decryptSignerInput) {
                    decryptSignerInput.value = '';
                }
                if (decryptRequireInput) {
                    decryptRequireInput.checked = false;
                }
            } else if (decryptRequireInput) {
                decryptRequireInput.checked = true;
            }
        };
        decryptRadios.forEach(radio => radio.addEventListener('change', updateDecryptMode));
        updateDecryptMode();
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    // Add icon based on type
    const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : type === 'warning' ? '⚠' : 'ℹ';
    notification.innerHTML = `<span>${icon}</span> ${message}`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}

// Download file helper
function downloadFile(data, filename) {
    const blob = new Blob([data], { type: 'application/octet-stream' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Generate Keys
async function generateKeys() {
    const userIdInput = document.getElementById('user-id');
    const userId = userIdInput.value.trim();

    if (!userId) {
        showNotification('Please enter a User ID', 'error');
        return;
    }

    const generateBtn = event.target;
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';

    try {
        const response = await fetch('/api/keys/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId })
        });

        const data = await response.json();

        if (data.success) {
            showNotification(data.message, 'success');
            userIdInput.value = '';

            // Download all keys
            for (const [keyType, keyData] of Object.entries(data.keys)) {
                const keyBytes = Uint8Array.from(atob(keyData.data), c => c.charCodeAt(0));
                downloadFile(keyBytes, keyData.filename);
            }

            // Reload keys list
            setTimeout(() => loadKeys(), 1000);
        } else {
            showNotification(data.error || 'Failed to generate keys', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-plus-circle"></i> Generate Keys';
    }
}

// Load Keys List
async function loadKeys() {
    const keysList = document.getElementById('keys-list');
    keysList.innerHTML = '<div class="loading">Loading keys...</div>';

    try {
        const response = await fetch('/api/keys/list');
        const data = await response.json();

        if (data.success) {
            if (data.users.length === 0) {
                keysList.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-key"></i>
                        <p>No keys generated yet</p>
                        <p style="font-size: 0.9rem; margin-top: 10px;">Generate your first key pair above</p>
                    </div>
                `;
            } else {
                keysList.innerHTML = data.users.map(user => `
                    <div class="key-item">
                        <div class="key-item-header">
                            <h3><i class="fas fa-user"></i> ${user.user_id}</h3>
                            <div class="key-buttons">
                                ${Object.entries(user.keys).map(([keyType, keyInfo]) => `
                                    <button class="key-btn" onclick="downloadKey('${keyInfo.path}')">
                                        <i class="fas fa-download"></i> ${keyType.replace('-', ' ')}
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        } else {
            keysList.innerHTML = '<div class="empty-state"><p>Error loading keys</p></div>';
        }
    } catch (error) {
        keysList.innerHTML = '<div class="empty-state"><p>Error: ' + error.message + '</p></div>';
    }
}

// Download Key
async function downloadKey(keyPath) {
    try {
        const response = await fetch(`/api/keys/download/${keyPath}`);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = keyPath.split('/').pop();
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            showNotification('Key downloaded successfully', 'success');
        } else {
            const data = await response.json();
            showNotification(data.error || 'Failed to download key', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

// Encrypt File
async function encryptFile(event) {
    event.preventDefault();

    const fileInput = document.getElementById('encrypt-file');
    const recipientKeyInput = document.getElementById('encrypt-recipient-key');
    const signerKeyInput = document.getElementById('encrypt-signer-key');
    const encryptModeInput = document.querySelector('input[name="encrypt-mode"]:checked');
    const encryptMode = encryptModeInput ? encryptModeInput.value : 'confidential';
    const submitBtn = event.target.querySelector('button[type="submit"]');

    if (!fileInput.files[0] || !recipientKeyInput.files[0]) {
        showNotification('Please select a file and recipient key', 'error');
        return;
    }

    const authenticatedEncryption = encryptMode === 'authenticated';
    if (authenticatedEncryption && !signerKeyInput.files[0]) {
        showNotification('Please select a signer private key for authentication encryption', 'error');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Encrypting...';

    try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('recipient_key', recipientKeyInput.files[0]);
        if (authenticatedEncryption && signerKeyInput.files[0]) {
            formData.append('signer_key', signerKeyInput.files[0]);
        }

        const response = await fetch('/api/encrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            const signatureMsg = data.signature_attached
                ? ' Digital signature attached.'
                : ' No digital signature added.';
            showNotification(`${data.message}${signatureMsg}`, 'success');
            
            // Download encrypted file
            const encryptedBytes = Uint8Array.from(atob(data.data), c => c.charCodeAt(0));
            downloadFile(encryptedBytes, data.filename);

            // Reset form
            event.target.reset();
        } else {
            showNotification(data.error || 'Encryption failed', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-lock"></i> Encrypt File';
    }
}

// Decrypt File
async function decryptFile(event) {
    event.preventDefault();

    const fileInput = document.getElementById('decrypt-file');
    const recipientKeyInput = document.getElementById('decrypt-recipient-key');
    const signerKeyInput = document.getElementById('decrypt-signer-key');
    const requireSignatureInput = document.getElementById('decrypt-require-signature');
    const decryptModeInput = document.querySelector('input[name="decrypt-mode"]:checked');
    const decryptMode = decryptModeInput ? decryptModeInput.value : 'confidential';
    const submitBtn = event.target.querySelector('button[type="submit"]');

    if (!fileInput.files[0] || !recipientKeyInput.files[0]) {
        showNotification('Please select an encrypted file and your private key', 'error');
        return;
    }

    const authenticatedDecrypt = decryptMode === 'authenticated';
    if (authenticatedDecrypt && !signerKeyInput.files[0]) {
        showNotification('Please provide the signer public key for authentication decryption', 'error');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Decrypting...';

    try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('recipient_key', recipientKeyInput.files[0]);
        if (authenticatedDecrypt && signerKeyInput.files[0]) {
            formData.append('signer_key', signerKeyInput.files[0]);
        }
        const shouldRequireSignature = authenticatedDecrypt ? true : requireSignatureInput.checked;
        formData.append('require_signature', shouldRequireSignature ? 'true' : 'false');

        const response = await fetch('/api/decrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            let notificationType = 'success';
            let signatureMessage = '';
            if (data.signature) {
                if (data.signature.signature_present && data.signature.signature_verified) {
                    signatureMessage = ' Signature verified.';
                } else if (data.signature.signature_present && data.signature.signature_verified === false) {
                    signatureMessage = ' Signature present but not verified.';
                    notificationType = signerKeyInput.files[0] ? 'warning' : 'info';
                } else if (!data.signature.signature_present) {
                    signatureMessage = ' File is not digitally signed.';
                    notificationType = requireSignatureInput.checked ? 'warning' : 'info';
                }
            }
            showNotification(`${data.message}${signatureMessage}`, notificationType);
            
            // Download decrypted file
            const decryptedBytes = Uint8Array.from(atob(data.data), c => c.charCodeAt(0));
            downloadFile(decryptedBytes, data.filename);

            // Reset form
            event.target.reset();
        } else {
            showNotification(data.error || 'Decryption failed', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-unlock"></i> Decrypt File';
    }
}

