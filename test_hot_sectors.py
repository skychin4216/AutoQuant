"""
测试热门板块排名器 - TOP 20
"""
import pandas as pd
import numpy as np
from datetime import datetime

# 创建模拟板块数据
lookback_days = 20
end_date = datetime.now().date()

# 申万一级行业 + 热门细分板块
sectors = [
    '通信', '电子', '计算机', '传媒', '电力设备',
    '有色金属', '钢铁', '基础化工', '建筑材料', '机械设备',
    '汽车', '家用电器', '食品饮料', '医药生物', '银行',
    '非银金融', '房地产', '商贸零售', '社会服务', '交通运输',
    '光通信', '存储', '半导体', 'AI算力', '锂电池', '光伏', '稀土', '钼矿'
]

dates = pd.date_range(end=end_date, periods=lookback_days, freq='D')
all_data = {}

for sector in sectors:
    np.random.seed(hash(sector) % 10000)
    base_price = 1000
    
    # 热门细分板块给予更高的动量
    if sector in ['光通信', '存储', '半导体', 'AI算力', '锂电池', '光伏', '稀土', '钼矿']:
        returns = np.random.normal(0.005, 0.02, lookback_days)
    else:
        returns = np.random.normal(0.002, 0.02, lookback_days)
    
    close = base_price * np.exp(np.cumsum(returns))
    volume = np.random.randint(100000, 1000000, lookback_days)
    
    all_data[sector] = pd.DataFrame({
        'close': close,
        'vol': volume,
        'amount': close * volume
    }, index=dates)

# 计算评分（参考DeepSeek算法）
rank_days = 5
scores = []

# 模拟基准数据
bench_ret = 0.001

for name, df in all_data.items():
    momentum = df['close'].pct_change(rank_days).iloc[-1]
    vol_mean_short = df['vol'].tail(rank_days).mean()
    vol_mean_long = df['vol'].tail(lookback_days).mean()
    fund_flow = (vol_mean_short / vol_mean_long - 1) if vol_mean_long > 0 else 0
    relative_strength = momentum - bench_ret
    
    scores.append({
        '板块名称': name,
        '动量得分': momentum,
        '资金得分': fund_flow,
        '相对强度得分': relative_strength
    })

scores_df = pd.DataFrame(scores)

# Z-score标准化
for col in ['动量得分', '资金得分', '相对强度得分']:
    if scores_df[col].std() != 0:
        scores_df[col + '_z'] = (scores_df[col] - scores_df[col].mean()) / scores_df[col].std()
    else:
        scores_df[col + '_z'] = 0

scores_df['综合得分'] = (scores_df['动量得分_z'] + scores_df['资金得分_z'] + scores_df['相对强度得分_z']) / 3
ranked_df = scores_df.sort_values('综合得分', ascending=False)

print()
print('=' * 70)
print('热门板块排名 TOP 20 (参考DeepSeek算法)')
print('=' * 70)
print()

header = '排名    板块名称        动量得分      资金得分      相对强度      综合得分'
print(header)
print('-' * 70)

for i, (_, row) in enumerate(ranked_df.head(20).iterrows(), 1):
    line = f'{i:<6}  {row["板块名称"]:<12}  {row["动量得分"]:<10.4f}  {row["资金得分"]:<10.4f}  {row["相对强度得分"]:<10.4f}  {row["综合得分"]:<8.4f}'
    print(line)

print('-' * 70)
print()

# 检查光通信板块
print('光通信板块排名:')
for i, (_, row) in enumerate(ranked_df.iterrows(), 1):
    if row['板块名称'] == '光通信':
        print(f'  光通信板块排在第 {i} 位！')
        break

print()
print('=' * 70)