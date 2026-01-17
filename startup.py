"""
AURA Startup Manager
Handles first-time setup and launches wake word listener
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_requirements():
    """
    Check if all required packages are installed
    """
    print("🔍 Checking requirements...")
    
    required = [
        'speech_recognition',
        'pyaudio',
        'pyttsx3'
    ]
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            print(f"   Installing {package}...")
            os.system(f"{sys.executable} -m pip install {package}")

def first_time_setup():
    """
    First time setup - create necessary files and directories
    """
    print("\n🎯 AURA First Time Setup")
    print("=" * 50)
    
    # Create necessary directories
    dirs = ['logs', 'data', 'models']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created/verified {dir_name}/ folder")
    
    # Create config file if needed
    config_file = Path("aura_config.json")
    if not config_file.exists():
        import json
        config = {
            "wake_word": "aura",
            "voice_enabled": True,
            "language": "en-US"
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        print("✅ Created aura_config.json")
    
    print("\n✅ Setup complete!")

def start_wake_word_listener():
    """
    Start the wake word listener
    """
    print("\n🎤 Starting Wake Word Listener...")
    print("=" * 50)
    
    #try:
        #subprocess.Popen([sys.executable, 'wake_word_listener.py'])
        #print("✅ Wake Word Listener started!")
        #print("\n📢 Say 'AURA' to activate the application")
        
    #except Exception as e:
        #print(f"❌ Error starting listener: {e}")
        #sys.exit(1)

def add_to_startup(system_type=None):
    """
    Add AURA to system startup (optional)
    """
    if system_type is None:
        system_type = platform.system()
    
    print("\n⚙️  Startup Configuration")
    print("=" * 50)
    
    if system_type == "Windows":
        print("💡 To add AURA to Windows startup:")
        print("   1. Press Win + R")
        print("   2. Type: shell:startup")
        print("   3. Create shortcut to startup.py")
        print("   4. AURA will start automatically!")
        
    elif system_type == "Linux":
        print("💡 To add AURA to Linux startup:")
        print("   Add to ~/.bashrc or ~/.profile:")
        print("   python3 ~/AURA_PROJECT/startup.py &")
        
    elif system_type == "Darwin":  # macOS
        print("💡 To add AURA to macOS startup:")
        print("   Create Launch Agent in:")
        print("   ~/Library/LaunchAgents/com.aura.plist")

def main():
    """
    Main startup routine
    """
    print("\n" + "=" * 50)
    print("🚀 AURA Startup Manager")
    print("=" * 50)
    
    # Check requirements
    check_requirements()
    
    # First time setup
    first_time_setup()
    
    # Start wake word listener
    start_wake_word_listener()
    
    # Suggest startup config
    add_to_startup()
    
    print("\n✅ AURA is ready!")
    print("💡 Say 'AURA' to activate\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Startup cancelled by user")
        sys.exit(0)
