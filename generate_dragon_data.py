#!/usr/bin/env python
"""
生成龙头股数据 - 带中文描述
数据范围: 2025-01-01 至今
保存目录: E:\workspace\AutoQuant\data
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 数据目录
DATA_DIR = 'E:\\workspace\\AutoQuant\\data'

# 龙头股列表（带中文描述）
MAINBOARD_STOCKS = {
    # 沪市主板
    '600519.SH': '贵州茅台-白酒龙头',
    '601318.SH': '中国平安-保险龙头',
    '600036.SH': '招商银行-银行龙头',
    '601888.SH': '中国中免-免税龙头',
    
    # 深市主板
    '000858.SZ': '五粮液-白酒龙头',
    '000333.SZ': '美的集团-家电龙头',
    '002594.SZ': '比亚迪-新能源车龙头',  # 注意：002属于中小板，已并入主板
}

# 其他股票（非主板，用于对比）
OTHER_STOCKS = {
    '300750.SZ': '宁德时代-电池龙头(创业板)',
}

# 美股龙头
US_STOCKS = {
    'AAPL': '苹果-科技龙头(美股)',
    'MSFT': '微软-科技龙头(美股)',
    'GOOGL': '谷歌-科技龙头(美股)',
    'AMZN': '亚马逊-电商龙头(美股)',
    'TSLA': '特斯拉-新能源车龙头(美股)',
    'NVDA': '英伟达-芯片龙头(美股)',
    'META': 'Meta-社交龙头(美股)',
    'JPM': '摩根大通-银行龙头(美股)',
}

def generate_stock_data(symbol, name, start_date='2025-01-01', days=500):
    """生成模拟股票数据"""
    dates = pd.date_range(start=start_date, periods=days, freq='D')
    
    # 根据股票类型设置不同的基础价格和波动率
    if '茅台' in name or '五粮液' in name:
        base_price = 1800
        volatility = 0.02
    elif '宁德时代' in name or '比亚迪' in name:
        base_price = 200
        volatility = 0.03
    elif symbol.startswith(('AAPL', 'MSFT', 'GOOGL')):
        base_price = 150
        volatility = 0.02
    elif symbol.startswith(('NVDA', 'TSLA')):
        base_price = 200
        volatility = 0.04
    else:
        base_price = 50
        volatility = 0.02
    
    # 生成价格序列
    np.random.seed(hash(symbol) % 10000)
    returns = np.random.normal(0.001, volatility, days)
    prices = base_price * np.exp(np.cumsum(returns))
    
    # 生成OHLCV数据
    data = pd.DataFrame({
        'date': dates,
        'open': prices * (1 + np.random.uniform(-0.01, 0.01, days)),
        'high': prices * (1 + np.random.uniform(0, 0.02, days)),
        'low': prices * (1 + np.random.uniform(-0.02, 0, days)),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, days),
    })
    
    # 添加技术指标
    data['returns'] = data['close'].pct_change()
    data['volatility'] = data['returns'].rolling(20).std()
    data['sma_20'] = data['close'].rolling(20).mean()
    data['sma_60'] = data['close'].rolling(60).mean()
    data['rsi'] = calculate_rsi(data['close'])
    
    return data

def calculate_rsi(prices, period=14):
    """计算RSI指标"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def save_stock_data(symbol, name, data):
    """保存股票数据到CSV，文件名包含中文描述"""
    # 创建文件名：代码_中文描述.csv
    filename = f"{symbol}_{name}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    # 保存数据
    data.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"✅ 已保存: {filename}")
    return filepath

def main():
    """主函数"""
    print("=" * 60)
    print("龙头股数据生成器")
    print("=" * 60)
    
    # 创建数据目录
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"📁 创建数据目录: {DATA_DIR}")
    
    # 计算日期范围
    start_date = '2025-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    days = (datetime.now() - datetime(2025, 1, 1)).days + 1
    
    print(f"📅 数据范围: {start_date} ~ {end_date} ({days}天)")
    print()
    
    # 生成主板龙头股数据
    print("【主板龙头股】")
    print("-" * 40)
    for symbol, name in MAINBOARD_STOCKS.items():
        data = generate_stock_data(symbol, name, start_date, days)
        save_stock_data(symbol, name, data)
    
    print()
    
    # 生成非主板股票数据（用于对比）
    print("【非主板股票】")
    print("-" * 40)
    for symbol, name in OTHER_STOCKS.items():
        data = generate_stock_data(symbol, name, start_date, days)
        save_stock_data(symbol, name, data)
    
    print()
    
    # 生成美股龙头数据
    print("【美股龙头】")
    print("-" * 40)
    for symbol, name in US_STOCKS.items():
        data = generate_stock_data(symbol, name, start_date, days)
        save_stock_data(symbol, name, data)
    
    print()
    print("=" * 60)
    print(f"✅ 完成！共生成 {len(MAINBOARD_STOCKS) + len(OTHER_STOCKS) + len(US_STOCKS)} 只股票数据")
    print(f"📂 数据目录: {DATA_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()