# AURA Professional Deployment Guide

Follow these steps to run and manage AURA like a pro.

## 🏁 Quick Start
The easiest way to start AURA with all features (login, auto-login, and AI panel) enabled:

```powershell
python run.py
```

---

## 🛠 Project Structure (Core Files)
| File | Purpose |
| :--- | :--- |
| **`run.py`** | **The Main Entry Point.** Run this to start the app. |
| **`aura_panel.py`** | The main AI interface & Voice UI. |
| **`aura_login.py`** | Secure user authentication (MySQL). |
| **`aura/`** | The core engine, skills (filesystem, email), and mic fixes. |
| **`test_engine.py`** | Professional test suite for command routing. |
| **`test_audio_handoff.py`** | Stress test for voice reliability. |

---

## ⚙️ Professional Configuration
AURA is designed to be highly configurable via the following files:

### 1. Database & Security (`.env`)
Ensure your MySQL credentials are set in the root `.env` file for persistent history and user management.

### 2. Contacts (`data/contacts.json`)
AURA uses this to find people when you say "Message Sinchana" or "Call Dad".

### 3. Email Settings (`data/email_config.json`)
Configure your SMTP server here to enable AURA to send emails on your behalf.

---

## 🧪 Verification Commands
Before presenting or deploying, run these to ensure 100% stability:

```powershell
# 1. Verify AI Command Logic
python test_engine.py

# 2. Verify Audio Stability
python test_audio_handoff.py

# 3. Initialize/Reset Database
python init_db.py
```

---

## 🚀 Desktop Shortcut (Professional Launch)
To create a high-performance desktop launch script, save this as `Launch_AURA.bat`:

```batch
@echo off
title AURA Voice Assistant
cd /d "%~dp0"
echo Starting AURA Professional Engine...
python run.py
pause
```
