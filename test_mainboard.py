#!/usr/bin/env python
"""测试主板股票过滤功能"""
import sys
sys.path.insert(0, 'e:\\workspace\\AutoQuant')

from autoquant.dragon_filter import DragonStockFilter

# 测试股票代码
test_symbols = [
    '600519.SH',  # 沪市主板 - 茅台
    '601318.SH',  # 沪市主板 - 平安
    '000858.SZ',  # 深市主板 - 五粮液
    '300750.SZ',  # 创业板 - 宁德时代 (应排除)
    '688001.SH',  # 科创板 (应排除)
    'AAPL',       # 美股 (应排除)
]

print("主板股票过滤测试:")
print("=" * 40)
for symbol in test_symbols:
    result = DragonStockFilter.is_main_board(symbol)
    status = "✅ 主板" if result else "❌ 非主板"
    print(f"{symbol}: {status}")
print("=" * 40)