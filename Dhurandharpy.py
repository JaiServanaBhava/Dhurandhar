"""
=============================================================================
 DHURANDHAR  v3.0  —  USB & Mobile Detection with Self-Installation
 - Runs silently in background (no tray icon, no admin panel)
 - AUTO-INSTALLS to All-Users Startup folder on first launch!
 - Detects USB drives AND Mobile Phones (MTP/PTP) → full-screen flashing lock
 - Persistent State Check: Re-locks immediately if PC was shut down while locked!
 - Start Menu / taskbar / Win key / Alt+F4 all blocked while locked
 - Keyboard FIX: Entry box receives alphanumeric inputs natively!
 - Unlock: type password  23173cm005  and press Enter
 - Admin shortcut: Ctrl+Shift+5 stops the monitor silently
 - Admin shortcut: Ctrl+Shift+Esc completely closes the application
=============================================================================
"""

import sys, os, json, time, threading, ctypes, ctypes.wintypes, subprocess, shutil
import tkinter as tk
from pathlib import Path
from datetime import datetime
import hashlib

# ── Paths ──────────────────────────────────────────────────────────────────
if getattr(sys, "frozen", False):
    CURRENT_EXE = Path(sys.executable)
    SCRIPT_DIR = CURRENT_EXE.parent
else:
    CURRENT_EXE = Path(__file__)
    SCRIPT_DIR = CURRENT_EXE.parent

# Official deployment targets branded to Dhurandhar
TARGET_DIR      = Path(r"C:\Dhurandhar")
TARGET_EXE      = TARGET_DIR / "Dhurandhar.exe"
LOG_FILE        = TARGET_DIR / "dhurandhar_log.txt"
STATE_FILE      = TARGET_DIR / "dhurandhar_state.json"
SCAN_INTERVAL   = 2   

# ── Password & Configurations ─────────────────────────────────────────────
PASSWORD        = "23173cm005"
PASSWORD_HASH   = hashlib.sha256(PASSWORD.encode()).hexdigest()

FLASH_COLORS = [
    "#FFD700", "#FF8C00", "#FFD700", "#FF4500",
    "#FFD700", "#FF8C00", "#FFFF00", "#FF4500",
]

_global_monitor_ref = None

# ===========================================================================
# AUTOMATIC SELF-INSTALLATION LOGIC
# ===========================================================================

def auto_install_to_startup():
    """
    If the EXE is running from a temporary location (like a USB or C:\ root drive),
    it automatically copies itself to C:\Dhurandhar and creates the Startup shortcut.
    """
    if not getattr(sys, "frozen", False):
        return

    # 1. Create target directory if it doesn't exist
    if not TARGET_DIR.exists():
        try:
            TARGET_DIR.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    # 2. If we aren't running from the official folder, copy ourselves there
    if CURRENT_EXE.resolve() != TARGET_EXE.resolve():
        try:
            shutil.copy2(str(CURRENT_EXE), str(TARGET_EXE))
        except Exception as e:
            with open("dhurandhar_install_error.txt", "w") as f:
                f.write(f"Failed to copy exe: {str(e)}")

    # 3. Target the system-wide All Users Startup folder natively (Common Startup)
    startup_folder = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
    shortcut_path = os.path.join(startup_folder, "Dhurandhar.lnk")

    if not os.path.exists(shortcut_path):
        ps_cmd = (
            f"$ws = New-Object -ComObject WScript.Shell; "
            f"$sc = $ws.CreateShortcut('{shortcut_path}'); "
            f"$sc.TargetPath = '{str(TARGET_EXE)}'; "
            f"$sc.WorkingDirectory = '{str(TARGET_DIR)}'; "
            f"$sc.Description = 'Dhurandhar System Monitor'; "
            f"$sc.Save()"
        )
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], startupinfo=startupinfo)
        except Exception:
            pass

        # Launch the official installed instance in the background and kill this temporary one
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", str(TARGET_EXE), None, None, 1)
            os._exit(0)
        except Exception:
            pass

# ===========================================================================
# LOGGING
# ===========================================================================

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        if not TARGET_DIR.exists():
            TARGET_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line)
    except Exception:
        pass

# ===========================================================================
# PERSISTENT LOCK STATE MANAGER
# ===========================================================================

def _load_state() -> dict:
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {"locked": False, "reason": ""}

def _save_state(locked: bool, reason: str = ""):
    try:
        if not TARGET_DIR.exists():
            TARGET_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump({"locked": locked, "reason": reason}, f)
    except Exception:
        pass

def mark_locked(reason: str):
    _save_state(True, reason)

def mark_unlocked():
    _save_state(False, "")

def was_locked_on_shutdown() -> tuple:
    s = _load_state()
    return s.get("locked", False), s.get("reason", "USB drive inserted")

# ===========================================================================
# ADMIN RIGHTS
# ===========================================================================

def check_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def elevate_and_restart():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join(f'"{a}"' for a in sys.argv),
        None, 1
    )

# ===========================================================================
# HARDWARE DETECTION LOGIC (USB + MOBILE PHONES)
# ===========================================================================

def get_connected_hardware_fingerprint() -> set:
    devices = set()
    try:
        cmd = 'powershell -NoProfile -Command "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like \'USB*\' -or $_.Class -eq \'WPD\' } | Select-Object -ExpandProperty InstanceId"'
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        output = subprocess.check_output(cmd, startupinfo=startupinfo, text=True, shell=True)
        for line in output.splitlines():
            line = line.strip()
            if line:
                devices.add(line)
    except Exception as e:
        log(f"Error querying hardware: {str(e)}")
    return devices

def eject_removable_drives():
    GENERIC_READ  = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ  = 0x1
    FILE_SHARE_WRITE = 0x2
    OPEN_EXISTING    = 3
    IOCTL_STORAGE_EJECT_MEDIA = 0x2D4808
    k32 = ctypes.windll.kernel32
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter == 'C':
            continue
        path = f"{letter}:\\"
        if k32.GetDriveTypeW(path) not in (2, 3):
            continue
        h = k32.CreateFileW(
            f"\\\\.\\{letter}:", GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None
        )
        if h == ctypes.wintypes.HANDLE(-1).value:
            continue
        bytes_returned = ctypes.c_ulong(0)
        k32.DeviceIoControl(h, IOCTL_STORAGE_EJECT_MEDIA, None, 0, None, 0, ctypes.byref(bytes_returned), None)
        k32.CloseHandle(h)

# ===========================================================================
# TARGETED WIN32 HOOK — Blocks ONLY the Windows Start Menu Button cleanly
# ===========================================================================

_hook_handle    = None
_hook_thread    = None
_blocking_keys  = False

WH_KEYBOARD_LL = 13
VK_LWIN        = 0x5B   # Left Windows Key
VK_RWIN        = 0x5C   # Right Windows Key

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
_hook_callback_ref = None

def _keyboard_hook(nCode, wParam, lParam):
    global _blocking_keys
    if _blocking_keys and nCode >= 0:
        vk = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong))[0]
        # ONLY swallow Left Windows and Right Windows keys (Start Menu remains completely blocked).
        # Standard alphabets, control pipelines, numbers, and backspace pass safely through.
        if vk in (VK_LWIN, VK_RWIN):
            return 1
    return ctypes.windll.user32.CallNextHookEx(_hook_handle, nCode, wParam, lParam)

def install_keyboard_hook():
    global _hook_handle, _hook_callback_ref
    cb = HOOKPROC(_keyboard_hook)
    _hook_callback_ref = cb
    _hook_handle = ctypes.windll.user32.SetWindowsHookExA(WH_KEYBOARD_LL, cb, None, 0)

def uninstall_keyboard_hook():
    global _hook_handle
    if _hook_handle:
        ctypes.windll.user32.UnhookWindowsHookEx(_hook_handle)
        _hook_handle = None

def _hook_message_pump():
    install_keyboard_hook()
    msg = ctypes.wintypes.MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

def start_hook_thread():
    global _hook_thread
    _hook_thread = threading.Thread(target=_hook_message_pump, daemon=True, name="KeyboardHook")
    _hook_thread.start()

# ===========================================================================
# LOCK SCREEN UI
# ===========================================================================

class LockScreen:
    def __init__(self, reason: str, on_unlock):
        self.reason     = reason
        self.on_unlock  = on_unlock
        self.root       = None
        self._flash_idx = 0
        self._flash_job = None
        self._canvas    = None
        self._bg_rect   = None
        self._pw_var    = None
        self._pw_entry  = None
        self._err_label = None

    def show(self):
        global _blocking_keys
        _blocking_keys = True

        self.root = tk.Tk()
        root = self.root
        root.attributes("-fullscreen", True)
        root.attributes("-topmost",    True)
        root.overrideredirect(True)
        root.configure(bg="#FFD700")
        root.resizable(False, False)

        # Intercept desktop navigation sequences safely
        for seq in ("<Alt-F4>", "<Alt-Tab>", "<Escape>", "<Control-Escape>", "<Alt-Escape>"):
            root.bind(seq, lambda e: "break")
        root.protocol("WM_DELETE_WINDOW", lambda: None)

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()

        c = tk.Canvas(root, width=sw, height=sh, bg="#FFD700", highlightthickness=0)
        c.pack(fill="both", expand=True)
        self._canvas = c
        self._bg_rect = c.create_rectangle(0, 0, sw, sh, fill="#FFD700", outline="")

        c.create_text(sw // 2, sh // 2 - 220, text="⚠", font=("Segoe UI", 110, "bold"), fill="#1a1a00", tags="txt")
        c.create_text(sw // 2, sh // 2 - 90, text="UNAUTHORIZED DEVICE DETECTED", font=("Impact", 46, "bold"), fill="#1a1a00", tags="txt")

        reason_short = (self.reason[:120] + "…") if len(self.reason) > 120 else self.reason
        c.create_text(sw // 2, sh // 2 - 25, text=reason_short, font=("Courier New", 13), fill="#330000", tags="txt")
        c.create_text(sw // 2, sh // 2 + 28, text="Enter Admin Password below to unlock Dhurandhar:", font=("Segoe UI", 15, "bold"), fill="#1a1a00", tags="txt")

        self._pw_var = tk.StringVar()
        pw_frame = tk.Frame(root, bg="#1a1a00", padx=3, pady=3)
        pw_frame.place(relx=0.5, rely=0.5, anchor="center", y=int(sh * 0.10))

        inner = tk.Frame(pw_frame, bg="#fff8dc")
        inner.pack()

        tk.Label(inner, text="🔑  Admin Password:", font=("Segoe UI", 12, "bold"), fg="#1a1a00", bg="#fff8dc").pack(pady=(8, 2))
        
        # Alphanumeric Entry field with native focus and input processing
        self._pw_entry = tk.Entry(inner, textvariable=self._pw_var, show="●", font=("Courier New", 16), bg="#1a1a00", fg="#FFD700", insertbackground="#FFD700", relief="flat", bd=0, width=24)
        self._pw_entry.pack(padx=20, pady=6, ipady=8)
        
        # Focus enforcement controls to allow persistent text streams
        root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
        self._pw_entry.focus_force()

        self._err_label = tk.Label(inner, text="", font=("Segoe UI", 10, "bold"), fg="#cc0000", bg="#fff8dc")
        self._err_label.pack(pady=(0, 4))

        tk.Button(inner, text="  UNLOCK SYSTEM  ", command=self._attempt_unlock, bg="#1a6b00", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=14, pady=8, cursor="hand2", activebackground="#145200", activeforeground="white").pack(pady=(2, 12))
        self._pw_entry.bind("<Return>", lambda e: self._attempt_unlock())

        ts = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        c.create_text(sw - 16, sh - 16, text=ts, font=("Courier New", 11), fill="#555500", anchor="se", tags="txt")

        self._flash()
        self._enforce_focus()
        root.mainloop()
        _blocking_keys = False

    def force_close_ui(self):
        """Used by administrative hotkeys to clear window handles securely."""
        try:
            if self._flash_job:
                self.root.after_cancel(self._flash_job)
            self.root.destroy()
        except Exception:
            pass

    def _flash(self):
        if not (self.root and self.root.winfo_exists()):
            return
        colour = FLASH_COLORS[self._flash_idx % len(FLASH_COLORS)]
        self._flash_idx += 1
        try:
            self._canvas.itemconfig(self._bg_rect, fill=colour)
            self.root.configure(bg=colour)
        except Exception:
            pass
        self._flash_job = self.root.after(350, self._flash)

    def _enforce_focus(self):
        if not (self.root and self.root.winfo_exists()):
            return
        try:
            self.root.lift()
            self.root.attributes("-topmost", True)
            self._pw_entry.focus_set()
        except Exception:
            pass
        self.root.after(400, self._enforce_focus)

    def _attempt_unlock(self):
        entered = self._pw_var.get()
        if hashlib.sha256(entered.encode()).hexdigest() == PASSWORD_HASH:
            log("Dhurandhar unlocked — correct password entered.")
            mark_unlocked()
            if self._flash_job:
                self.root.after_cancel(self._flash_job)
            self.root.destroy()
            if self.on_unlock:
                self.on_unlock()
        else:
            log("Incorrect unlock password attempt.")
            self._err_label.config(text="✗  Incorrect password — try again")
            self._pw_var.set("")
            self._pw_entry.focus_set()

# ===========================================================================
# BACKGROUND MONITOR ENGINE
# ===========================================================================

class USBMonitor:
    def __init__(self):
        self._stop_event   = threading.Event()
        self._lock_active  = False
        self._known_fingerprint = set()
        self.current_lock_ui = None

    def start(self):
        self._known_fingerprint = get_connected_hardware_fingerprint()
        t = threading.Thread(target=self._loop, daemon=True, name="USBMonitor")
        t.start()
        log("Dhurandhar hardware monitor active (USB + MTP Devices).")

    def stop(self):
        self._stop_event.set()
        log("Dhurandhar monitor stopped by admin shortcut.")
        if self.current_lock_ui:
            self.current_lock_ui.force_close_ui()

    def register_admin_hotkey(self):
        def _wait_for_hotkey():
            MOD_CONTROL = 0x0002
            MOD_SHIFT   = 0x0004
            VK_5        = 0x35
            VK_ESC      = 0x1B
            user32      = ctypes.windll.user32
            HOTKEY_STOP = 9001
            HOTKEY_EXIT = 9002

            user32.RegisterHotKey(None, HOTKEY_STOP, MOD_CONTROL | MOD_SHIFT, VK_5)
            user32.RegisterHotKey(None, HOTKEY_EXIT, MOD_CONTROL | MOD_SHIFT, VK_ESC)

            msg = ctypes.wintypes.MSG()
            WM_HOTKEY = 0x0312
            while not self._stop_event.is_set():
                result = user32.PeekMessageW(ctypes.byref(msg), None, WM_HOTKEY, WM_HOTKEY, 1)
                if result and msg.message == WM_HOTKEY:
                    if msg.wParam == HOTKEY_STOP:
                        mark_unlocked()
                        self.stop()
                        break
                    elif msg.wParam == HOTKEY_EXIT:
                        log("Dhurandhar force-closed by admin shortcut (Ctrl+Shift+Esc).")
                        user32.UnregisterHotKey(None, HOTKEY_STOP)
                        user32.UnregisterHotKey(None, HOTKEY_EXIT)
                        os._exit(0)
                time.sleep(0.2)

            user32.UnregisterHotKey(None, HOTKEY_STOP)
            user32.UnregisterHotKey(None, HOTKEY_EXIT)

        t = threading.Thread(target=_wait_for_hotkey, daemon=True, name="HotkeyWatcher")
        t.start()

    def _loop(self):
        while not self._stop_event.is_set():
            if not self._lock_active:
                self._check_hardware()
            time.sleep(SCAN_INTERVAL)

    def _check_hardware(self):
        current_fingerprint = get_connected_hardware_fingerprint()
        new_devices = current_fingerprint - self._known_fingerprint
        if new_devices:
            reason = "Unauthorized USB storage or Mobile phone connected!"
            log(f"Violation! New hardware detected: {list(new_devices)}")
            eject_removable_drives()
            self._trigger_lock(reason)
        self._known_fingerprint = current_fingerprint

    def _trigger_lock(self, reason: str):
        self._lock_active = True
        mark_locked(reason)
        threading.Thread(target=self._run_lock, args=(reason,), daemon=True, name="LockScreen").start()

    def _run_lock(self, reason: str):
        def on_unlock():
            self._lock_active = False
            self._known_fingerprint = get_connected_hardware_fingerprint()
        
        self.current_lock_ui = LockScreen(reason, on_unlock)
        self.current_lock_ui.show()

# ===========================================================================
# MAIN EXECUTION ENTRY POINT
# ===========================================================================

def main():
    global _global_monitor_ref
    if not check_admin():
        elevate_and_restart()
        return

    # Self-deploy directly to Startup folders if executed outside C:\Dhurandhar\
    auto_install_to_startup()

    log("=" * 60)
    log("Dhurandhar security service initialized.")

    # 1. Read persistent disk state from previous session
    was_locked, last_reason = was_locked_on_shutdown()
    
    monitor = USBMonitor()
    _global_monitor_ref = monitor
    monitor.start()
    monitor.register_admin_hotkey()
    start_hook_thread()

    # 2. Enforce immediate re-locking if previous session was killed unlawfully
    if was_locked:
        log(f"Resuming lock from previous session. Reason: {last_reason}")
        lock_done = threading.Event()
        
        def resume_unlock():
            lock_done.set()
            monitor._known_fingerprint = get_connected_hardware_fingerprint()
            monitor._lock_active = False

        monitor._lock_active = True
        monitor.current_lock_ui = LockScreen(f"[Previous session] {last_reason}", resume_unlock)
        monitor.current_lock_ui.show()

    try:
        while not monitor._stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    log("Dhurandhar security service exiting.")

if __name__ == "__main__":
    main()