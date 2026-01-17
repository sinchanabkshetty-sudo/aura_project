---
description: How to run AURA the professional way
---

# 🚀 Running AURA: Professional Guide

To run AURA professionally, you should use the centralized entry point and environment management tools.

### 1. Launching AURA
The preferred way to start AURA is using the `run.py` script. This script handles:
- Loading environment variables (`.env`)
- Checking for saved user sessions (Auto-login)
- Orchestrating the UI transition from Login to the main AI Panel

**Command:**
```powershell
python run.py
```

### 2. Startup Automation (Windows)
To have AURA start automatically with your PC:
1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Create a shortcut to a batch file with the following content:
```batch
@echo off
cd /d "C:\VEDANSH\shravya'project\myproject"
python run.py
```

### 3. Maintenance and Verification
Use the following professional verification tools included in the project:
- **`test_engine.py`**: Verifies the AI command routing logic.
- **`test_audio_handoff.py`**: Validates microphone stability and the "Hey AURA" wake word listener.
- **`init_db.py`**: Resets or initializes the MySQL user and history database.

### 4. Configuration
- **`.env`**: Store your database credentials and API keys here.
- **`data/contacts.json`**: Manage the contacts AURA can message or call.
- **`data/email_config.json`**: Configure SMTP settings for voice-based emailing.
