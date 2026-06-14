# -*- mode: python ; coding: utf-8 -*-
"""
AutoQuant 打包脚本
使用 PyInstaller 将应用打包成 exe
"""

import sys
import os

block_cipher = None

a = Analysis(
    ['autoquant/gui/app.py'],
    pathex=['e:\\workspace\\AutoQuant'],
    binaries=[],
    datas=[
        ('autoquant', 'autoquant'),
        ('README.md', '.'),
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
        'talib',
        'openai',
        'anthropic',
        'autoquant.data',
        'autoquant.strategy',
        'autoquant.backtest',
        'autoquant.risk',
        'autoquant.analyzer',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'wx', 'gtk'],
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
    name='AutoQuant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI应用不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)