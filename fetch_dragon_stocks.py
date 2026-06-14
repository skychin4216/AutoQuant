"""
简化版龙头股数据获取脚本
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 默认配置
DEFAULT_START_DATE = '2025-01-01'
DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d')
DATA_DIR = 'E:\\workspace\\AutoQuant\\data'

def create_simulation_data():
    """创建模拟龙头股数据"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    stocks = [
        # 美股
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM',
        # A股
        '600519.SH', '000858.SZ', '601318.SH', '600036.SH',
        '000333.SZ', '002594.SZ', '300750.SZ', '601888.SH'
    ]
    
    # 生成日期范围
    dates = pd.date_range(start=DEFAULT_START_DATE, end=DEFAULT_END_DATE, freq='D')
    
    for idx, symbol in enumerate(stocks):
        print(f"[{idx+1}/{len(stocks)}] 生成 {symbol}...", end=' ')
        
        try:
            # 设置随机种子确保可重复
            np.random.seed(idx * 1000 + len(symbol))
            
            # 基础价格根据股票类型设置
            if symbol.endswith('.SH') or symbol.endswith('.SZ'):
                base_price = 80 + np.random.rand() * 300  # A股价格区间
            else:
                base_price = 50 + np.random.rand() * 400  # 美股价格区间
            
            prices = []
            current_price = base_price
            
            for date in dates:
                # 跳过周末
                if date.weekday() >= 5:
                    continue
                
                # 随机波动（带趋势）
                trend = np.random.normal(0.0005, 0.001)  # 轻微上涨趋势
                change = np.random.normal(trend, 0.015)
                current_price = max(current_price * (1 + change), base_price * 0.5)
                
                # 生成OHLC
                open_price = current_price * (1 + np.random.normal(0, 0.003))
                high_price = max(current_price, open_price) * (1 + np.random.uniform(0, 0.015))
                low_price = min(current_price, open_price) * (1 - np.random.uniform(0, 0.015))
                
                prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(current_price, 2),
                    'volume': int(np.random.uniform(5000000, 50000000))
                })
            
            df = pd.DataFrame(prices)
            df['date'] = pd.to_datetime(df['date'])
            
            # 计算指标
            df['returns'] = df['close'].pct_change()
            df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
            df['volatility'] = df['returns'].rolling(window=20).std() * np.sqrt(252)
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['sma_60'] = df['close'].rolling(window=60).mean()
            
            df = df.dropna()
            
            # 保存
            file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
            df.to_csv(file_path, index=False)
            print(f"✓ ({len(df)} 条)")
            
        except Exception as e:
            print(f"✗ {str(e)}")
    
    print(f"\n完成! 共 {len(stocks)} 只股票")

if __name__ == "__main__":
    print("=" * 60)
    print("龙头股数据生成工具")
    print("=" * 60)
    print(f"日期范围: {DEFAULT_START_DATE} ~ {DEFAULT_END_DATE}")
    print(f"保存目录: {DATA_DIR}")
    print("-" * 60)
    
    create_simulation_data()
    
    # 显示结果
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.csv')])
    print(f"\n📁 数据文件列表 ({len(files)} 个):")
    for f in files:
        size = os.path.getsize(os.path.join(DATA_DIR, f)) / 1024
        print(f"  - {f} ({size:.1f} KB)")
    
    print(f"\n🎉 数据生成完成!")