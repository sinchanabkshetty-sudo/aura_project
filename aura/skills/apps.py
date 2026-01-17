# aura/skills/apps.py
import os, glob, shutil, subprocess, difflib, json, re

# ---------- Cache ----------
CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache"))
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, "apps_index.json")

# Start Menu shortcut locations
START_MENU_DIRS = [
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
    os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
]

# Common EXE locations (shallow scan)
EXE_DIRS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.expandvars(r"%LOCALAPPDATA%"),
]

# Aliases to improve matches (“vs code” → “visual studio code”, etc.)
ALIASES = {
    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "ms edge": "microsoft edge",
    "edge": "microsoft edge",
    "word": "microsoft word",
    "excel": "microsoft excel",
    "power point": "powerpoint",
    "powerpoint": "powerpoint",
    "snipping tool": "snipping tool",
    "screen snip": "snipping tool",
    "whatsapp": "whatsapp",
    "whats app": "whatsapp",
    "store": "microsoft store",
    "microsoft store": "microsoft store",
    "clock": "clock",
    "paint": "paint",
    "calculator": "calculator",
    "canva": "canva",
    "telegram": "telegram",
    "spotify": "spotify",
    "notepad": "notepad",
    "cmd": "command prompt",
    "command prompt": "command prompt",
    "terminal": "windows terminal",
    "copilot": "copilot",
    "onedrive": "onedrive",
}

def _normalize(name: str) -> str:
    name = name.lower().strip()
    # collapse multiple spaces
    name = re.sub(r"\s+", " ", name)
    # apply alias if present
    return ALIASES.get(name, name)

def _load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_cache(index: dict):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _powershell(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["powershell", "-NoLogo", "-NoProfile", "-Command", cmd],
        capture_output=True, text=True, shell=True
    )

def _index_start_menu_shortcuts(index: dict):
    for base in START_MENU_DIRS:
        if not os.path.isdir(base):
            continue
        for lnk in glob.glob(os.path.join(base, "**", "*.lnk"), recursive=True):
            display = os.path.splitext(os.path.basename(lnk))[0]
            key = _normalize(display)
            # prefer friendlier names (don’t overwrite if already set via exact name)
            index.setdefault(key, {"kind": "lnk", "path": lnk, "display": display})

def _index_common_exes(index: dict):
    for base in EXE_DIRS:
        if not os.path.isdir(base):
            continue
        # shallow scan to keep it fast
        for exe in glob.glob(os.path.join(base, "*", "*.exe")):
            display = os.path.splitext(os.path.basename(exe))[0]
            key = _normalize(display)
            # don’t override Start Menu friendly names
            index.setdefault(key, {"kind": "exe", "path": exe, "display": display})

def _index_uwp_apps(index: dict):
    """
    Use PowerShell Get-StartApps to grab UWP (Store) apps.
    We’ll store: display -> AUMID and launch via shell:AppsFolder.
    """
    ps = _powershell("Get-StartApps | Select-Object Name, AppID | ConvertTo-Json -Depth 2")
    if ps.returncode != 0 or not ps.stdout.strip():
        return
    try:
        data = json.loads(ps.stdout)
        # Get-StartApps returns either a dict or list depending on count
        items = data if isinstance(data, list) else [data]
        for item in items:
            name = str(item.get("Name", "")).strip()
            appid = str(item.get("AppID", "")).strip()
            if not name or not appid:
                continue
            key = _normalize(name)
            # don’t override LNK names; UWP goes in as fallback
            index.setdefault(key, {"kind": "uwp", "appid": appid, "display": name})
    except Exception:
        pass

def index_apps() -> str:
    """
    Build a merged index of:
      - Start Menu (.lnk) shortcuts
      - Common EXE files (shallow)
      - UWP / Store apps (Get-StartApps)
    """
    index = {}
    _index_start_menu_shortcuts(index)
    _index_common_exes(index)
    _index_uwp_apps(index)
    _save_cache(index)
    return f"Indexed {len(index)} apps. Try: open chrome, open snipping tool, open visual studio code."

def _ensure_index() -> dict:
    idx = _load_cache()
    if idx:
        return idx
    index_apps()
    return _load_cache()

def _launch_lnk(path: str) -> bool:
    try:
        os.startfile(path)
        return True
    except Exception:
        # Fallback: PowerShell Start-Process
        ps = _powershell(f"Start-Process -FilePath '{path}'")
        return ps.returncode == 0

def _launch_exe(path: str) -> bool:
    try:
        subprocess.Popen([path], shell=True)
        return True
    except Exception:
        return False

def _launch_uwp(appid: str) -> bool:
    """
    Launch UWP via shell:AppsFolder\AUMID using powershell explorer.exe
    """
    # Try explorer shell path
    cmd = f"Start-Process explorer.exe 'shell:AppsFolder\\{appid}'"
    ps = _powershell(cmd)
    return ps.returncode == 0

def open_application_any(target: str) -> str:
    """
    Fuzzy-open any app:
      - Exact name match
      - Alias match
      - Fuzzy match against index keys
      - PATH executables as last resort
    """
    if not target:
        return "Please specify the application to open."

    original = target
    target = _normalize(target)

    index = _ensure_index()

    # 1) Direct hit
    if target in index:
        meta = index[target]
        kind = meta["kind"]
        if kind == "lnk" and _launch_lnk(meta["path"]):
            return f"Opening {meta['display']}."
        if kind == "exe" and _launch_exe(meta["path"]):
            return f"Opening {meta['display']}."
        if kind == "uwp" and _launch_uwp(meta["appid"]):
            return f"Opening {meta['display']}."
        return f"Found {meta['display']} but failed to launch."

    # 2) Fuzzy match
    candidates = difflib.get_close_matches(target, list(index.keys()), n=1, cutoff=0.6)
    if candidates:
        best = candidates[0]
        meta = index[best]
        kind = meta["kind"]
        if kind == "lnk" and _launch_lnk(meta["path"]):
            return f"Opening {meta['display']}."
        if kind == "exe" and _launch_exe(meta["path"]):
            return f"Opening {meta['display']}."
        if kind == "uwp" and _launch_uwp(meta["appid"]):
            return f"Opening {meta['display']}."
        return f"Found {meta['display']} but failed to launch."

    # 3) Last resort: PATH (e.g., notepad, calc)
    path = shutil.which(original) or shutil.which(target)
    if path and _launch_exe(path):
        return f"Opening {os.path.basename(path)}."

    return "I couldn’t find that app. Say “reindex apps” once and try again."
