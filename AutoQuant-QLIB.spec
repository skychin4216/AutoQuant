# -*- mode: python ; coding: utf-8 -*-
"""
AutoQuant AI因子研究框架 - PyInstaller Spec
"""

block_cipher = None

a = Analysis(
    ['run_qlib.py'],
    pathex=['e:\\workspace\\AutoQuant'],
    binaries=[],
    datas=[
        ('autoquant', 'autoquant'),
    ],
    hiddenimports=[
        'qlib',
        'qlib.data',
        'qlib.contrib',
        'qlib.workflow',
        'lightgbm',
        'xgboost',
        'pandas',
        'numpy',
        'scipy',
        'sklearn',
        'loguru',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'wx', 'gtk', 'matplotlib', 'PyQt5', 'vnpy'],
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
    name='AutoQuant-AI因子研究框架',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)