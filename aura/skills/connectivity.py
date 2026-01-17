# aura/skills/connectivity.py
import subprocess

def toggle_wifi(on: bool):
    cmd = "netsh interface set interface Wi-Fi admin=enable" if on else "netsh interface set interface Wi-Fi admin=disable"
    subprocess.run(cmd, shell=True)
    return f"Turning Wi-Fi {'on' if on else 'off'}."

def toggle_bluetooth(on: bool):
    # needs admin; also device name can vary
    ps = "(Get-PnpDevice -FriendlyName '*Bluetooth*' | Enable-PnpDevice -Confirm:$false)" if on else "(Get-PnpDevice -FriendlyName '*Bluetooth*' | Disable-PnpDevice -Confirm:$false)"
    subprocess.run(f"powershell -Command \"{ps}\"", shell=True)
    return f"Turning Bluetooth {'on' if on else 'off'}."
