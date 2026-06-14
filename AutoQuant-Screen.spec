# -*- mode: python ; coding: utf-8 -*-
"""
AutoQuant 命令行工具 - PyInstaller Spec
"""

block_cipher = None

a = Analysis(
    ['run_screen.py'],
    pathex=['e:\\workspace\\AutoQuant'],
    binaries=[],
    datas=[
        ('autoquant', 'autoquant'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'pandas',
        'numpy',
        'yfinance',
        'ta',
        'loguru',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'wx', 'gtk', 'PyQt5'],
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
    name='AutoQuant-龙头股筛选',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)