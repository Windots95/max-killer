import os
import sys
import time
import random
import ctypes
import signal
import winreg
import threading
import subprocess
import urllib.request
import math

# WINDOWS CORE GRAPHICS & SYSTEM CONSTANTS
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

# GDI GRAPHICS BRUSHES & OPERATIONS
PATINVERT = 0x5A0049
SRCINVERT = 0x660046
SRCCOPY = 0xCC0020

# VERIFIED CORE PNG TEMPLATE POOL
PNG_ASSET_URLS = [
    "https://static.wikia.nocookie.net/max-design-pro/images/c/c4/TWIDDLE_4.webp",
    "https://static.wikia.nocookie.net/max-design-pro/images/d/df/320_sin_t%C3%ADtulo_20240827155040.png"
]

LOCAL_DIR = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "SupremeMaxGDI")
os.makedirs(LOCAL_DIR, exist_ok=True)
LOCAL_PNGS = []

# AUTO CHROME PATH DETECTION
CHROME_EXE = "chrome"
for path in [r"C:\Program Files\Google\Chrome\Application\chrome.exe", 
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")]:
    if os.path.exists(path):
        CHROME_EXE = path
        break

# PERFORMANCE CONTROL STRUCT
speed_multiplier = 1.0

CREEPY_NOTE = """
AFTER ALL OF THE WASTED YEARS...
THE ENTIRE SCREEN BELONGS TO MAX AND JIMMY NOW.

DO NOT ATTEMPT TO INTERRUPT THE RITUAL.
THE ROTATION WILL ONLY ACCELERATE.

""" + ("MAX AND JIMMY " * 300)

def set_creepy_notepad_font():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Notepad", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "lfFaceName", 0, winreg.REG_SZ, "Chiller")
        winreg.SetValueEx(key, "iFontSize", 0, winreg.REG_DWORD, 48)
        winreg.CloseKey(key)
    except Exception:
        pass

def launch_initial_notepad_warning():
    set_creepy_notepad_font()
    note_path = os.path.join(LOCAL_DIR, "MAX_WARNING.txt")
    try:
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(CREEPY_NOTE)
        p = subprocess.Popen(["notepad.exe", note_path])
        p.wait()
    except Exception:
        pass

def get_screen_resolution():
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)
    return width, height

def move_all_windows_and_boxes():
    """Locates Chrome windows AND native message boxes, making them slip and bounce across coordinates."""
    scr_w, scr_h = get_screen_resolution()
    
    def enum_window_callback(hwnd, lparam):
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
            title = buffer.value
            
            # Catching Chrome windows, our custom note, or our generated message boxes
            if "core_max_" in title or "Chrome" in title or "MAX DESIGN" in title or "TWIDDLE" in title:
                new_x = random.randint(0, int(scr_w - 500))
                new_y = random.randint(0, int(scr_h - 400))
                ctypes.windll.user32.MoveWindow(hwnd, new_x, new_y, 650, 450, True)
        return True

    while True:
        ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_window_callback), 0)
        time.sleep(max(0.05, 0.6 / speed_multiplier))

def run_max_jimmy_gdi_effects():
    """Pure system-level GDI render pipe. Alternates red and blue visual anomalies and viewport rotations."""
    scr_w, scr_h = get_screen_resolution()
    
    # Get direct handle to raw screen device context (DC = 0)
    hdc = ctypes.windll.user32.GetDC(0)
    
    # Create custom native colorful solid styling brushes
    red_brush = ctypes.windll.gdi32.CreateSolidBrush(0x0000FF)  # Win32 Color: BGR (Red = FF)
    blue_brush = ctypes.windll.gdi32.CreateSolidBrush(0xFF0000) # Win32 Color: BGR (Blue = FF0000)
    
    rotation_angle = 0.0
    
    while True:
        try:
            # Effect Style 1: Flash Red and Blue blocks randomly
            chosen_brush = random.choice([red_brush, blue_brush])
            ctypes.windll.gdi32.SelectObject(hdc, chosen_brush)
            
            x1 = random.randint(0, scr_w)
            y1 = random.randint(0, scr_h)
            w1 = random.randint(100, int(scr_w / 2))
            h1 = random.randint(100, int(scr_h / 2))
            
            # Invert or color overlay specific patches
            ctypes.windll.gdi32.PatBlt(hdc, x1, y1, w1, h1, PATINVERT)
            
            # Effect Style 2: Max's Reality Rotation (Screen desktop layout pixel stretching/shifting)
            if random.random() < 0.3:
                shift_offset = int(math.sin(rotation_angle) * (20 * speed_multiplier))
                # Shifts screen horizontal and vertical lines to simulate an unstable screen rotation
                ctypes.windll.gdi32.BitBlt(hdc, shift_offset, 0, scr_w, scr_h, hdc, 0, 0, SRCINVERT)
                ctypes.windll.gdi32.BitBlt(hdc, 0, shift_offset, scr_w, scr_h, hdc, 0, 0, SRCINVERT)
                
            rotation_angle += 0.1 * speed_multiplier
            time.sleep(max(0.01, 0.1 / speed_multiplier))
            
        except Exception:
            pass

def download_assets():
    print("[*] Gathering core Max & Jimmy resources...")
    for i, url in enumerate(PNG_ASSET_URLS):
        local_path = os.path.join(LOCAL_DIR, f"core_max_{i}.png")
        try:
            urllib.request.urlretrieve(url, local_path)
            LOCAL_PNGS.append(local_path)
        except Exception:
            pass

def change_wallpaper():
    if not LOCAL_PNGS:
        return
    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, random.choice(LOCAL_PNGS), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
    except Exception:
        pass

def speak_tts_line(text):
    try:
        ps_command = f'Add-Type -AssemblyName System.Speech; $val = New-Object System.Speech.Synthesis.SpeechSynthesizer; $val.Speak("{text}")'
        subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps_command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def spawn_popup_box():
    titles = ["MAX DESIGN PRO", "TWIDDLEFINGER", "SYSTEM OVERRIDE"]
    msgs = ["You can't leave this program after all of the wasted years!", "Try to close this window! I bet you can't!"]
    def worker():
        ctypes.windll.user32.MessageBoxW(0, random.choice(msgs), random.choice(titles), 0x10 | 0x40000)
    threading.Thread(target=worker, daemon=True).start()

def open_background_chrome_window():
    if not LOCAL_PNGS:
        return
    try:
        subprocess.Popen([CHROME_EXE, "--new-window", "--no-activate", random.choice(LOCAL_PNGS)], creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception:
        pass

def trigger_attempted_close_penalty():
    global speed_multiplier
    speed_multiplier += 2.0  # Speeds up window dancing AND GDI flickering cycles instantly
    speak_tts_line("Max and Jimmy are getting faster.")
    spawn_popup_box()

def main_loop():
    # Run the window movement, GDI shaders, and voice processors on separated system pipelines
    threading.Thread(target=move_all_windows_and_boxes, daemon=True).start()
    threading.Thread(target=run_max_jimmy_gdi_effects, daemon=True).start()
    threading.Thread(target=lambda: [speak_tts_line("You can't escape this program.") or time.sleep(5) for _ in iter(int, 1)], daemon=True).start()
    
    while True:
        try:
            change_wallpaper()
            spawn_popup_box()
            open_background_chrome_window()
            time.sleep(random.uniform(2.5, 5.0))
        except KeyboardInterrupt:
            trigger_attempted_close_penalty()
            time.sleep(0.5)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: trigger_attempted_close_penalty())
    signal.signal(signal.SIGTERM, lambda s, f: trigger_attempted_close_penalty())

    download_assets()
    launch_initial_notepad_warning()
    main_loop()