# aura/system_handlers.py

import os
import subprocess
import time
import ctypes
import pyautogui
import webbrowser
import psutil
import wikipedia
import random
import glob


class SystemHandler:
    """
    Core system + app control for AURA.
    Used by command handlers, smart_search, wake-word listener, etc.
    """

    WIFI_NAME = "Wi-Fi"  # your WiFi name
    MUSIC_FOLDER = r"C:\Users\Public\Music"  # change to your music folder

    # --------------------------------------------------------
    #  OPEN SYSTEM / USER APPLICATIONS
    # --------------------------------------------------------
    def open_app(self, app_name):
        """Open Windows system apps, Settings pages, Office, or external apps."""

        app_name = app_name.lower().strip()

        # SYSTEM APPLICATIONS
        system_apps = {
            "settings": "ms-settings:",
            "wifi settings": "ms-settings:network-wifi",
            "bluetooth settings": "ms-settings:bluetooth",
            "display settings": "ms-settings:display",
            "sound settings": "ms-settings:sound",
            "power settings": "ms-settings:powersleep",
            "windows update": "ms-settings:windowsupdate",
            "task manager": "Taskmgr.exe",
            "control panel": "control.exe",
            "device manager": "devmgmt.msc",
            "file explorer": "explorer.exe",
            "explorer": "explorer.exe",
            "this pc": "explorer.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "camera": "microsoft.windows.camera:",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "snipping tool": "SnippingTool.exe",
            "voice recorder": "ms-settings:apps-volume",
        }

        # COMMON USER & OFFICE APPS
        custom_apps = {
            # Browsers
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",

            # Editor / IDE
            "notepad": "notepad.exe",
            "vscode": "code.exe",
            "vs code": "code.exe",

            # Music
            "spotify": "spotify.exe",

            # Office
            "word": "winword.exe",
            "ms word": "winword.exe",
            "microsoft word": "winword.exe",
            "excel": "excel.exe",
            "microsoft excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "ms powerpoint": "powerpnt.exe",
            "microsoft powerpoint": "powerpnt.exe",
            "outlook": "outlook.exe",
        }

        all_apps = {**system_apps, **custom_apps}

        # If known app
        if app_name in all_apps:
            target = all_apps[app_name]
            try:
                os.startfile(target)
                return f"🚀 Opening {app_name}..."
            except:
                try:
                    subprocess.Popen(target)
                    return f"🚀 Opening {app_name}..."
                except Exception as e:
                    return f"❌ Cannot open {app_name}: {e}"

        # Try as executable
        try:
            os.startfile(app_name)
            return f"🚀 Opening {app_name}..."
        except:
            try:
                subprocess.Popen(app_name)
                return f"🚀 Opening {app_name}..."
            except Exception as e:
                return f"❌ Unknown application '{app_name}'. Error: {e}"

    # --------------------------------------------------------
    # CLOSE APPLICATIONS
    # --------------------------------------------------------
    def close_app(self, app_name):
        """Close applications by killing their process."""
        app_name = app_name.lower().strip()

        known_procs = {
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "spotify": "spotify.exe",
            "notepad": "notepad.exe",
            "calculator": "Calculator.exe",
            "paint": "mspaint.exe",
            "vscode": "Code.exe",
            "vs code": "Code.exe",
            "word": "WINWORD.EXE",
            "microsoft word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
        }

        proc_name = known_procs.get(app_name, app_name)
        closed = False

        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == proc_name.lower():
                    proc.kill()
                    closed = True
            except:
                pass

        if closed:
            return f"🛑 Closed {app_name}"
        return f"⚠️ {app_name} was not running"

    # --------------------------------------------------------
    # BROWSER SEARCH: GOOGLE & YOUTUBE
    # --------------------------------------------------------
    def open_google(self, query):
        query = query.strip()
        if not query:
            return "❌ Empty search query."
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"🔎 Searching Google for '{query}'..."

    def open_youtube(self, query):
        query = query.strip()
        if not query:
            return "❌ Empty YouTube query."
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"📺 Searching YouTube for '{query}'..."

    # --------------------------------------------------------
    # WIKIPEDIA ANSWERING
    # --------------------------------------------------------
    def ask_wikipedia(self, question):
        question = question.strip()
        if not question:
            return "❌ Empty question."

        try:
            summary = wikipedia.summary(question, sentences=2)
            return f"📘 {summary}"
        except:
            return self.open_google(question)

    # --------------------------------------------------------
    # LOCAL MUSIC PLAYER
    # --------------------------------------------------------
    def play_local_music(self):
        try:
            patterns = ["*.mp3", "*.wav", "*.m4a", "*.flac"]
            files = []
            for p in patterns:
                files.extend(glob.glob(os.path.join(self.MUSIC_FOLDER, p)))

            if not files:
                return f"❌ No music found in {self.MUSIC_FOLDER}. Update MUSIC_FOLDER path."

            track = random.choice(files)
            os.startfile(track)
            return f"🎵 Playing: {os.path.basename(track)}"

        except Exception as e:
            return f"❌ Could not play music: {e}"

    # --------------------------------------------------------
    # WIFI CONTROL
    # --------------------------------------------------------
    def wifi_on(self):
        os.system(f'netsh interface set interface "{self.WIFI_NAME}" admin=enable')
        return "📶 Wi-Fi ON"

    def wifi_off(self):
        os.system(f'netsh interface set interface "{self.WIFI_NAME}" admin=disable')
        return "📵 Wi-Fi OFF"

    # --------------------------------------------------------
    # BLUETOOTH
    # --------------------------------------------------------
    def bluetooth_on(self):
        os.system("powershell Start-Service bthserv")
        return "🔵 Bluetooth ON"

    def bluetooth_off(self):
        os.system("powershell Stop-Service bthserv")
        return "⚪ Bluetooth OFF"

    # --------------------------------------------------------
    # AIRPLANE MODE
    # --------------------------------------------------------
    def airplane_on(self):
        os.system(
            r'powershell "Set-ItemProperty -Path HKLM:\System\CurrentControlSet\Control\RadioManagement\SystemRadioState -Name RadioEnable -Value 0"'
        )
        return "✈️ Airplane Mode ON"

    def airplane_off(self):
        os.system(
            r'powershell "Set-ItemProperty -Path HKLM:\System\CurrentControlSet\Control\RadioManagement\SystemRadioState -Name RadioEnable -Value 1"'
        )
        return "🟢 Airplane Mode OFF"

    # --------------------------------------------------------
    # HOTSPOT
    # --------------------------------------------------------
    def hotspot_on(self):
        os.system('netsh wlan set hostednetwork mode=allow ssid=AURA_Hotspot key=12345678')
        os.system('netsh wlan start hostednetwork')
        return "📡 Hotspot ON"

    def hotspot_off(self):
        os.system('netsh wlan stop hostednetwork')
        return "📡 Hotspot OFF"

    # --------------------------------------------------------
    # BRIGHTNESS
    # --------------------------------------------------------
    def brightness_set(self, percent):
        try:
            subprocess.call(
                f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{percent})",
                shell=True,
            )
            return f"🔆 Brightness set to {percent}%"
        except:
            return "❌ Unable to change brightness"

    def brightness_up(self):
        pyautogui.press("brightnessup")
        return "🔆 Brightness increased"

    def brightness_down(self):
        pyautogui.press("brightnessdown")
        return "🔅 Brightness decreased"

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------
    def volume_set(self, percent):
        return f"🔊 Volume set to {percent}% (approx)"

    # --------------------------------------------------------
    # DARK / LIGHT MODE
    # --------------------------------------------------------
    def dark_mode(self):
        os.system(
            r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f'
        )
        return "🌙 Dark mode ON"

    def light_mode(self):
        os.system(
            r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 1 /f'
        )
        return "🌞 Light mode ON"

    # --------------------------------------------------------
    # MICROPHONE
    # --------------------------------------------------------
    def mic_mute(self):
        os.system(
            r"powershell ""(Get-AudioDevice -List | ?{$_.Type -eq 'Recording'}).Mute = $true"""
        )
        return "🎤 Microphone muted"

    def mic_unmute(self):
        os.system(
            r"powershell ""(Get-AudioDevice -List | ?{$_.Type -eq 'Recording'}).Mute = $false"""
        )
        return "🎤 Microphone unmuted"

    # --------------------------------------------------------
    # BATTERY SAVER
    # --------------------------------------------------------
    def battery_saver_on(self):
        os.system("powercfg /setdcvalueindex scheme_current sub_energy saver 1")
        return "🔋 Battery saver ON"

    def battery_saver_off(self):
        os.system("powercfg /setdcvalueindex scheme_current sub_energy saver 0")
        return "🔋 Battery saver OFF"

    # --------------------------------------------------------
    # POWER CONTROLS
    # --------------------------------------------------------
    def lock_system(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "🔒 Locked"

    def shutdown(self):
        os.system("shutdown /s /t 3")
        return "⚠️ Shutting down..."

    def restart(self):
        os.system("shutdown /r /t 3")
        return "🔄 Restarting..."

    def sleep_mode(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "😴 Sleeping..."

    # --------------------------------------------------------
    # CHROME TAB CONTROL
    # --------------------------------------------------------
    def chrome_new_tab(self):
        pyautogui.hotkey('ctrl', 't')
        return "🆕 New Chrome tab opened."

    def chrome_close_tab(self):
        pyautogui.hotkey('ctrl', 'w')
        return "❌ Chrome tab closed."

    def chrome_next_tab(self):
        pyautogui.hotkey('ctrl', 'tab')
        return "➡️ Next tab."

    def chrome_prev_tab(self):
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        return "⬅️ Previous tab."
