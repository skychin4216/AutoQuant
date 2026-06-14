"""
测试龙头股筛选 - 光通信板块"易中天"组合
"""

from autoquant.dragon_filter import DragonStockFilter, HOT_SECTOR_LEADERS
import numpy as np

print('=' * 70)
print('龙头股筛选测试')
print('=' * 70)

# 创建筛选器
filter = DragonStockFilter()

# 执行筛选
filtered_stocks, stats = filter.run_full_filter()

print('\n筛选统计:')
print(f'  第一层（全局排雷）: {stats.get("layer1", 0)} 只')
print(f'  第二层（龙头定位）: {stats.get("layer2", 0)} 只')
print(f'  第三层（基本盘）: {stats.get("layer3", 0)} 只')
print(f'  第四层（择优对比）: {stats.get("layer4", 0)} 只')

print(f'\n筛选结果: {len(filtered_stocks)} 只龙头股')
print('-' * 70)

# 按板块分类显示
hot_sector_stocks = [s for s in filtered_stocks if s.symbol in HOT_SECTOR_LEADERS]
other_stocks = [s for s in filtered_stocks if s.symbol not in HOT_SECTOR_LEADERS]

print(f'\n热门板块龙头股: {len(hot_sector_stocks)} 只')
for stock in hot_sector_stocks:
    print(f'  ✅ {stock.symbol} (市值:{stock.market_cap}亿, ROE:{np.mean(stock.roe):.1f}%)')

print(f'\n其他主板龙头股: {len(other_stocks)} 只')
for stock in other_stocks[:5]:
    print(f'  ✅ {stock.symbol} (市值:{stock.market_cap}亿, ROE:{np.mean(stock.roe):.1f}%)')

print('-' * 70)

# 检查光通信板块
print('\n光通信板块龙头股 - "易中天"组合:')
for symbol in ['300308.SZ', '300502.SZ', '300393.SZ']:
    found = any(s.symbol == symbol for s in filtered_stocks)
    status = '✅ 已筛选' if found else '❌ 未筛选'
    print(f'  {symbol} {status}')

print('=' * 70)