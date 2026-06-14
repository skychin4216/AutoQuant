"""AutoQuant 量化分析系统启动脚本"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 初始化龙头股筛选器
from autoquant.dragon_filter import create_dragon_filter

# 全局龙头股筛选器实例
dragon_filter = create_dragon_filter('a500')

from autoquant.gui.app import main

if __name__ == '__main__':
    main()