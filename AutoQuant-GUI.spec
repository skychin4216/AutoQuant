# -*- mode: python ; coding: utf-8 -*-
"""
AutoQuant 策略分析平台 - PyInstaller Spec
"""

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=['e:\\workspace\\AutoQuant'],
    binaries=[],
    datas=[
        ('autoquant', 'autoquant'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
        'pandas',
        'numpy',
        'yfinance',
        'ta',
        'loguru',
        'click',
        'pydantic',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'wx', 'gtk', 'vnpy', 'qlib'],
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
    name='AutoQuant-策略分析平台',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)