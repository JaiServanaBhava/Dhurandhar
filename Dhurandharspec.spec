# =============================================================================
#  lab_security_monitor.spec  —  v3.0
#  PyInstaller spec — single hidden-console .exe, no pystray required.
#  Run:  python -m PyInstaller lab_security_monitor.spec --clean --noconfirm
# =============================================================================

block_cipher = None

a = Analysis(
    ['lab_security_monitor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'winreg',
        'ctypes',
        'ctypes.wintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pystray', 'PIL', 'pillow',
        'matplotlib', 'numpy', 'scipy', 'pandas',
        'PyQt5', 'wx', 'gi', 'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Dhurandhar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # no console window — silent background process
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,      # always prompt UAC on launch
    icon='shield.ico',
)
