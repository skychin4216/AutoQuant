#!/usr/bin/env python
"""
AutoQuant 龙头股筛选工具 - 命令行版
无需GUI，直接运行筛选和分析
默认只分析主板股票
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from autoquant.dragon_filter import create_dragon_filter, FinancialData, DragonStockFilter, StockFilterConfig
from autoquant.data import DataFeed, CSVDataSource

# 数据目录
DATA_DIR = 'E:\\workspace\\AutoQuant\\data'
DEFAULT_START_DATE = '2025-01-01'
DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d')

def load_stock_data(main_board_only=True):
    """加载本地数据，默认只加载主板股票"""
    print("📂 加载本地数据...")
    feed = DataFeed(source='csv', data_dir=DATA_DIR)
    symbols = feed.get_symbols()
    
    # 主板股票过滤
    if main_board_only:
        symbols = [s for s in symbols if DragonStockFilter.is_main_board(s)]
        print(f"   主板股票: {len(symbols)} 只")
    else:
        print(f"   全部股票: {len(symbols)} 只")
    
    return feed, symbols

def run_screening(index_type='a500', main_board_only=True):
    """运行龙头股筛选"""
    print("\n" + "=" * 60)
    print(f"龙头股筛选 ({index_type.upper()})")
    if main_board_only:
        print("【主板股票模式】只分析主板股票")
    print("=" * 60)
    
    # 创建筛选器
    filter = create_dragon_filter(index_type)
    
    # 设置主板股票过滤（默认启用）
    filter.config.main_board_only = main_board_only
    
    # 使用宽松的筛选条件
    filter.config.min_market_cap = 30  # 降低市值要求
    filter.config.min_roe = 10  # 降低ROE要求
    filter.config.roe_years = 2  # 减少达标年数
    filter.config.profit_growth_years = 2
    filter.config.max_debt_ratio = 60
    filter.config.pe_threshold = 50
    filter.config.pb_threshold = 8
    
    # 加载数据（默认只加载主板股票）
    feed, symbols = load_stock_data(main_board_only)
    
    # 获取可用的符号 - 优先使用本地数据中的股票
    available_symbols = [s for s in symbols if '.' in s]  # A股格式
    
    # 模拟财务数据
    stocks = []
    for symbol in available_symbols:
        data = feed.get_price(symbol, DEFAULT_START_DATE, DEFAULT_END_DATE)
        if not data.empty:
            latest = data.iloc[-1]
            close = latest['close']
            
            # 根据价格估算市值
            market_cap = close * 1e8 / 10  # 简单估算
            
            stock = FinancialData(
                symbol=symbol,
                market_cap=market_cap / 1e8,  # 转换为亿
                roe=[15, 16, 17],  # 降低ROE要求
                net_profit=[5, 6, 7],
                operating_cash_flow=[5.5, 6.5, 7.5],
                revenue=[30, 35, 40],
                gross_margin=[25, 26, 27],
                debt_ratio=40,
                pe=20,
                pb=3.0,
                listing_days=365 * 2,
                is_st=False,
                is_paused=False
            )
            stocks.append(stock)
    
    # 执行筛选
    if not stocks:
        print("❌ 没有可用数据")
        return []
    
    print(f"\n📊 初始股票数: {len(stocks)}")
    filtered, stats = filter.run_full_filter(stocks)
    
    print("\n筛选结果:")
    print(f"  第一层(排雷): {stats.get('layer1', len(stocks))} 只")
    print(f"  第二层(龙头): {stats.get('layer2', len(stocks))} 只")
    print(f"  第三层(财务): {stats.get('layer3', len(stocks))} 只")
    print(f"  第四层(估值): {stats.get('layer4', len(stocks))} 只")
    
    return filtered

def display_results(filtered_stocks):
    """显示筛选结果"""
    print("\n" + "=" * 60)
    print("龙头股列表")
    print("=" * 60)
    
    if not filtered_stocks:
        print("没有符合条件的数据")
        return
    
    print(f"{'代码':<12} {'市值(亿)':<12} {'ROE':<10} {'PE':<10} {'PB':<10}")
    print("-" * 60)
    
    for stock in filtered_stocks:
        print(f"{stock.symbol:<12} {stock.market_cap:<12.2f} {stock.roe[-1]:<10.1f} {stock.pe:<10.1f} {stock.pb:<10.1f}")
    
    print("-" * 60)
    print(f"共 {len(filtered_stocks)} 只")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║         AutoQuant 龙头股筛选工具 v1.0                    ║
║         漏斗式四层筛选: 排雷→龙头→财务→估值              ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # 运行筛选
    filtered = run_screening('a500')
    
    # 显示结果
    display_results(filtered)
    
    print("\n✅ 筛选完成!")
    print(f"📂 数据目录: {DATA_DIR}")
    print(f"📅 日期范围: {DEFAULT_START_DATE} ~ {DEFAULT_END_DATE}")

if __name__ == "__main__":
    main()
    input("\n按Enter键退出...")