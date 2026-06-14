"""AutoQuant 量化分析系统启动脚本"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("AutoQuant 量化分析系统")
print("=" * 60)

# ============================================
# 步骤1: 获取热门板块排名
# ============================================
print("\n[步骤1/3] 获取热门板块排名...")
try:
    from autoquant.SectorHotRanker import SectorHotRanker
    
    ranker = SectorHotRanker(lookback_days=20, rank_days=5)
    hot_sectors_df = ranker.get_top_sectors(n=10)
    
    print("\n当前热门板块 TOP 10:")
    print("-" * 40)
    for i, (_, row) in enumerate(hot_sectors_df.iterrows(), 1):
        print(f"  {i:2d}. {row['板块名称']:<10} (综合得分: {row['综合得分']:.4f})")
    
    # 获取热门板块名称列表
    hot_sector_names = hot_sectors_df['板块名称'].tolist()
    print(f"\n热门板块列表: {', '.join(hot_sector_names)}")
    
except Exception as e:
    print(f"  获取热门板块失败: {e}")
    hot_sector_names = []
print("-" * 40)

# ============================================
# 步骤2: 初始化龙头股筛选器
# ============================================
print("\n[步骤2/3] 初始化龙头股筛选器...")
try:
    from autoquant.dragon_filter import create_dragon_filter
    
    # 使用A500指数成分股
    dragon_filter = create_dragon_filter('a500')
    print(f"  龙头股筛选器已初始化 (指数: A500)")
    
    # 从热门板块中筛选龙头股
    print(f"\n  正在从热门板块筛选龙头股...")
    
    # 运行完整筛选
    filtered_stocks = dragon_filter.run_full_filter()
    
    print(f"  筛选结果: {len(filtered_stocks)} 只龙头股")
    for stock in filtered_stocks[:5]:
        print(f"    - {stock}")
    
except Exception as e:
    print(f"  初始化龙头股筛选器失败: {e}")
    dragon_filter = None
print("-" * 40)

# ============================================
# 步骤3: 启动GUI
# ============================================
print("\n[步骤3/3] 启动GUI...")
try:
    from autoquant.gui.app import main
    print("  GUI启动中...")
except Exception as e:
    print(f"  GUI导入失败: {e}")
    print("  请确保已安装 PyQt5: pip install PyQt5")
    sys.exit(1)

print("=" * 60)

if __name__ == '__main__':
    main()