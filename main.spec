# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/atki7/Programs/python/HuntStatsLogger/src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/atki7/Programs/python/HuntStatsLogger/assets', 'assets/'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/App.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/Connection.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/GroupBox.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/Hunter.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/HuntHistory.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/Logger.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/Mainframe.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/Settings.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/src/TitleBar.py', '.'), ('C:/Users/atki7/Programs/python/HuntStatsLogger/.venv/Lib', 'Lib/')],
    hiddenimports=['xmltodict','json','sqlite3','PyQt5'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)