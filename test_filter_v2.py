"""测试新版龙头股筛选"""
from autoquant.dragon_filter import DragonStockFilter
from autoquant.hot_sector_config import get_main_board_leaders, HOT_SECTOR_CONFIG
import numpy as np

print("=" * 80)
print("龙头股筛选测试 - 按板块子板块分类")
print("=" * 80)

# 创建筛选器
filter = DragonStockFilter()

# 执行筛选
filtered_stocks, stats = filter.run_full_filter()

print(f"\n筛选统计:")
print(f"  第一层（全局排雷）: {stats.get('layer1', 0)} 只")
print(f"  第二层（龙头定位）: {stats.get('layer2', 0)} 只")
print(f"  第三层（基本盘）: {stats.get('layer3', 0)} 只")
print(f"  第四层（择优对比）: {stats.get('layer4', 0)} 只")

print(f"\n筛选结果: {len(filtered_stocks)} 只龙头股")
print("-" * 80)

# 获取主板龙头股信息
main_board_leaders = get_main_board_leaders()

# 按板块分类显示
sector_stocks = {}
for stock in filtered_stocks:
    symbol = stock.symbol
    if symbol in main_board_leaders:
        info = main_board_leaders[symbol]
        sector = info['sector']
        sub_sector = info['sub_sector']
        
        if sector not in sector_stocks:
            sector_stocks[sector] = {}
        if sub_sector not in sector_stocks[sector]:
            sector_stocks[sector][sub_sector] = []
        
        sector_stocks[sector][sub_sector].append({
            'symbol': symbol,
            'name': info['name'],
            'market_cap': stock.market_cap,
            'roe': np.mean(stock.roe)
        })

# 打印结果
for sector in HOT_SECTOR_CONFIG.keys():
    if sector in sector_stocks:
        print(f"\n📊 {sector}")
        for sub_sector, stocks in sector_stocks[sector].items():
            print(f"  📁 {sub_sector}")
            for stock in stocks:
                print(f"    ✅ {stock['symbol']} {stock['name']} (市值:{stock['market_cap']:.0f}亿, ROE:{stock['roe']:.1f}%)")

print("\n" + "=" * 80)