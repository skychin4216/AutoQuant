# -*- mode: python ; coding: utf-8 -*-
"""
AutoQuant 实盘交易终端 - PyInstaller Spec
"""

block_cipher = None

a = Analysis(
    ['run_vnpy.py'],
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
        'vnpy',
        'vnpy.trader',
        'vnpy.gateway',
        'vnpy_ctp',
        'pandas',
        'numpy',
        'loguru',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'wx', 'gtk', 'matplotlib', 'qlib'],
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
    name='AutoQuant-实盘交易终端',
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