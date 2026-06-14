#!/usr/bin/env python
"""
AutoQuant AI因子研究框架启动脚本
独立运行 Qlib 研究框架，集成龙头股筛选功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 初始化龙头股筛选器
from autoquant.dragon_filter import create_dragon_filter
dragon_filter = create_dragon_filter('a500')

def main():
    try:
        from autoquant.qlib_integration import QlibResearch, download_qlib_data
        
        print("=" * 60)
        print("AutoQuant AI因子研究框架")
        print("=" * 60)
        
        # Check if data exists
        data_path = os.path.join(os.path.expanduser("~"), ".qlib", "qlib_data", "cn")
        if not os.path.exists(data_path):
            print(f"Data not found at: {data_path}")
            choice = input("Download Qlib data? (y/n): ").strip().lower()
            if choice == 'y':
                download_qlib_data()
        
        # Initialize Qlib
        research = QlibResearch()
        research.init()
        
        # Example usage
        print("\n1. Getting stock list...")
        stocks = research.get_stock_list(market="csi500")
        print(f"   CSI 500 stocks: {len(stocks)}")
        
        print("\n2. Getting price data...")
        data = research.get_price_data(["SH600519"], "2020-01-01", "2023-01-01")
        print(f"   Price data shape: {data.shape}")
        
        print("\n3. Getting Alpha158 factors...")
        factors = research.get_alpha_factors(["SH600519"], "2020-01-01", "2020-01-31")
        print(f"   Factor data shape: {factors.shape}")
        print(f"   Factor columns: {list(factors.columns)[:5]}...")
        
        print("\n" + "=" * 60)
        print("Qlib research completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install Qlib first:")
        print("pip install qlib")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()