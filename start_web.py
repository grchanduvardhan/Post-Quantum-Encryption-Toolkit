#!/usr/bin/env python3
"""
Startup script for the Post-Quantum Encryption Toolkit Web Application
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing = []
    
    try:
        import flask
    except ImportError:
        missing.append("Flask")
    
    try:
        import cryptography
    except ImportError:
        missing.append("cryptography")
    
    try:
        import quantcrypt
    except ImportError:
        missing.append("quantcrypt")
    
    if missing:
        print("\n❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n📦 Install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\nOr install individually:")
        for dep in missing:
            print(f"   pip install {dep.lower()}")
        return False
    
    return True

def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("Post-Quantum Encryption Toolkit - Web Application")
    print("="*70)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("\n⚠️  Warning: Python 3.10+ recommended")
        print(f"   Current version: {sys.version}")
    
    print("\n✅ All dependencies installed")
    print("\n🚀 Starting web server...")
    print("   Open your browser and navigate to: http://localhost:5000")
    print("\n   Press Ctrl+C to stop the server\n")
    
    # Import and run the app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

