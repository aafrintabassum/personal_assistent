import subprocess
import os
import platform

# Windows installed app paths
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "vscode": r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "code": r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify": "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify",
    "paint": r"C:\Windows\System32\mspaint.exe",
    "instagram": "shell:AppsFolder\\Facebook.InstagramBeta_8xx8rvfyw5nnt!App",
    "linkedin": "shell:AppsFolder\\7EE7776C.LinkedInforWindows_w1wdnht996gqy!App",
    "whatsapp": "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
    "youtube": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "explorer": r"C:\Windows\explorer.exe",
    "cmd": r"C:\Windows\System32\cmd.exe"
}


def open_app(app_name):
    """Open installed applications properly"""

    app_name = app_name.lower().strip()

    if app_name not in APP_PATHS:
        return f"{app_name} is not installed or not configured."

    path = APP_PATHS[app_name]

    try:
        # For Microsoft Store apps
        if path.startswith("shell:"):
            subprocess.run(
                ['explorer.exe', path],
                shell=True
            )
        else:
            # For .exe apps
            subprocess.Popen(path)

        return f"Opening {app_name}"

    except Exception as e:
        print("Open error:", e)
        return f"Failed to open {app_name}"