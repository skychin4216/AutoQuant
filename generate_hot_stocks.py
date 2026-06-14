"""
光通信板块龙头股数据生成脚本
生成"易中天"组合（中际旭创、新易盛、天孚通信）的模拟数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_optical_communication_data():
    """生成光通信板块龙头股数据"""
    
    # 光通信板块龙头股 - "易中天"组合
    stocks = {
        '300308.SZ': {
            'name': '中际旭创',
            'desc': '光模块龙头-800G光模块全球领先',
            'sector': '光通信',
            'sub_sector': '光模块',
            'base_price': 150,  # 2025年初价格
            'growth_rate': 0.008  # 高成长性
        },
        '300502.SZ': {
            'name': '新易盛',
            'desc': '光模块龙头-LPO技术领先',
            'sector': '光通信',
            'sub_sector': '光模块',
            'base_price': 80,
            'growth_rate': 0.007
        },
        '300393.SZ': {
            'name': '天孚通信',
            'desc': '光器件龙头-CPO技术领先',
            'sector': '光通信',
            'sub_sector': '光器件',
            'base_price': 120,
            'growth_rate': 0.006
        },
        # 存储板块龙头
        '603986.SH': {
            'name': '兆易创新',
            'desc': '存储芯片龙头-国产替代',
            'sector': '存储',
            'sub_sector': '存储芯片',
            'base_price': 100,
            'growth_rate': 0.005
        },
        # 半导体板块龙头
        '002371.SZ': {
            'name': '北方华创',
            'desc': '半导体设备龙头-国产替代',
            'sector': '半导体',
            'sub_sector': '半导体设备',
            'base_price': 300,
            'growth_rate': 0.006
        },
        '603501.SH': {
            'name': '韦尔股份',
            'desc': '半导体设计龙头-CIS芯片',
            'sector': '半导体',
            'sub_sector': '半导体设计',
            'base_price': 100,
            'growth_rate': 0.005
        },
        # AI算力板块龙头
        '002230.SZ': {
            'name': '科大讯飞',
            'desc': 'AI算力龙头-语音识别',
            'sector': 'AI算力',
            'sub_sector': 'AI应用',
            'base_price': 50,
            'growth_rate': 0.006
        },
        # 锂电池板块龙头
        '002460.SZ': {
            'name': '赣锋锂业',
            'desc': '锂电池龙头-锂矿资源',
            'sector': '锂电池',
            'sub_sector': '锂矿',
            'base_price': 60,
            'growth_rate': 0.005
        },
        # 稀土板块龙头
        '600111.SH': {
            'name': '北方稀土',
            'desc': '稀土龙头-全球最大稀土企业',
            'sector': '稀土',
            'sub_sector': '稀土资源',
            'base_price': 30,
            'growth_rate': 0.004
        }
    }
    
    # 生成日期范围：2025-01-01 到今天
    start_date = datetime(2025, 1, 1)
    end_date = datetime.now()
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data_dir = 'E:\\workspace\\AutoQuant\\data'
    os.makedirs(data_dir, exist_ok=True)
    
    print("=" * 70)
    print("生成2025年热门板块龙头股数据")
    print("=" * 70)
    
    for symbol, info in stocks.items():
        np.random.seed(hash(symbol) % 10000)
        
        # 生成价格数据（高成长性）
        n_days = len(dates)
        returns = np.random.normal(info['growth_rate'], 0.03, n_days)
        close = info['base_price'] * np.exp(np.cumsum(returns))
        
        # 生成成交量（活跃）
        base_volume = 1000000 if symbol.startswith('6') else 500000
        volume = np.random.randint(base_volume, base_volume * 3, n_days)
        
        # 生成OHLCV数据
        high = close * (1 + np.abs(np.random.normal(0, 0.01, n_days)))
        low = close * (1 - np.abs(np.random.normal(0, 0.01, n_days)))
        open_price = close * (1 + np.random.normal(0, 0.005, n_days))
        
        # 创建DataFrame
        df = pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume,
            'amount': close * volume / 10000,  # 万元
            'sector': info['sector'],
            'sub_sector': info['sub_sector']
        })
        
        # 计算技术指标
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(20).std()
        df['sma_5'] = df['close'].rolling(5).mean()
        df['sma_10'] = df['close'].rolling(10).mean()
        df['sma_20'] = df['close'].rolling(20).mean()
        df['momentum_5d'] = df['close'].pct_change(5)
        df['momentum_10d'] = df['close'].pct_change(10)
        df['momentum_20d'] = df['close'].pct_change(20)
        
        # 模拟财务指标（龙头股财务指标优秀）
        df['roe'] = 18 + np.random.normal(0, 2, n_days)  # ROE > 15%
        df['profit_growth'] = 20 + np.random.normal(0, 5, n_days)  # 净利润增长 > 15%
        df['debt_ratio'] = 30 + np.random.normal(0, 5, n_days)  # 资产负债率 < 50%
        
        # 保存文件
        filename = f"{symbol}_{info['name']}-{info['desc']}.csv"
        filepath = os.path.join(data_dir, filename)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        print(f"✅ {symbol} {info['name']} ({info['sector']}) - {n_days}天数据")
    
    print("=" * 70)
    print(f"数据保存到: {data_dir}")
    print("=" * 70)
    
    return stocks

if __name__ == '__main__':
    stocks = generate_optical_communication_data()
    
    print("\n光通信板块龙头股 - '易中天'组合:")
    print("-" * 40)
    for symbol in ['300308.SZ', '300502.SZ', '300393.SZ']:
        info = stocks[symbol]
        print(f"  {symbol} {info['name']} - {info['desc']}")