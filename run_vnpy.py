#!/usr/bin/env python
"""
AutoQuant 实盘交易终端启动脚本
独立运行 vn.py 交易终端，集成龙头股筛选功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 初始化龙头股筛选器
from autoquant.dragon_filter import create_dragon_filter
dragon_filter = create_dragon_filter('a500')

def main():
    try:
        from autoquant.vnpy_integration import run_vnpy_gui
        run_vnpy_gui()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install vn.py first:")
        print("pip install vnpy vnpy_ctp")
        sys.exit(1)

if __name__ == "__main__":
    main()