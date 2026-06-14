"""
龙头股票池管理器
基于热门板块动态管理龙头股票池

功能:
1. 通过SectorHotRanker获取热门板块
2. 从热门板块中筛选符合条件的龙头股
3. 动态更新股票池
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from loguru import logger

try:
    from .SectorHotRanker import SectorHotRanker
    from .dragon_filter import DragonStockFilter, StockFilterConfig
    from .data import DataFeed
    SECTOR_RANKER_AVAILABLE = True
except ImportError:
    SECTOR_RANKER_AVAILABLE = False
    logger.warning("SectorHotRanker not available")


class LeaderStockPool:
    """
    龙头股票池管理器
    
    基于热门板块动态管理龙头股票池
    
    使用方法:
    >>> pool = LeaderStockPool()
    >>> pool.refresh()  # 获取最新热门板块和龙头股
    >>> top_stocks = pool.get_top_stocks(n=10)
    """
    
    def __init__(self, 
                 data_dir: str = 'E:\\workspace\\AutoQuant\\data',
                 top_sectors: int = 10,
                 top_stocks: int = 20,
                 lookback_days: int = 20,
                 rank_days: int = 5):
        """
        初始化龙头股票池管理器
        
        Args:
            data_dir: 数据目录
            top_sectors: 热门板块数量
            top_stocks: 龙头股数量
            lookback_days: 回溯天数
            rank_days: 排名计算天数
        """
        self.data_dir = data_dir
        self.top_sectors = top_sectors
        self.top_stocks = top_stocks
        self.lookback_days = lookback_days
        self.rank_days = rank_days
        
        self.hot_sectors = []  # 热门板块列表
        self.stock_pool = []  # 股票池
        self.stock_scores = {}  # 股票评分
        
        self.last_update = None  # 最后更新时间
        
        logger.info(f"LeaderStockPool initialized: top_sectors={top_sectors}, top_stocks={top_stocks}")
    
    def refresh(self) -> Dict:
        """
        刷新龙头股票池
        
        步骤:
        1. 通过SectorHotRanker获取热门板块
        2. 从数据目录加载股票数据
        3. 筛选符合条件的龙头股
        4. 按热度评分排序
        
        Returns:
            包含热门板块和龙头股的字典
        """
        result = {
            'hot_sectors': [],
            'stock_pool': [],
            'stock_scores': {},
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 步骤1: 获取热门板块
        print("正在获取热门板块...")
        if SECTOR_RANKER_AVAILABLE:
            try:
                ranker = SectorHotRanker(
                    lookback_days=self.lookback_days,
                    rank_days=self.rank_days
                )
                hot_sectors_df = ranker.get_top_sectors(n=self.top_sectors)
                self.hot_sectors = hot_sectors_df['板块名称'].tolist()
                result['hot_sectors'] = self.hot_sectors
                print(f"获取到 {len(self.hot_sectors)} 个热门板块")
            except Exception as e:
                logger.error(f"Failed to get hot sectors: {e}")
                self.hot_sectors = []
        else:
            # 使用默认板块
            self.hot_sectors = ['通信', '电子', '计算机', '有色金属', '电力设备']
            print(f"使用默认板块: {self.hot_sectors}")
        
        # 步骤2: 加载股票数据
        print("正在加载股票数据...")
        feed = DataFeed(source='csv', data_dir=self.data_dir)
        symbols = feed.get_symbols()
        print(f"加载了 {len(symbols)} 只股票")
        
        # 步骤3: 筛选龙头股
        print("正在筛选龙头股...")
        dragon_filter = DragonStockFilter()
        
        scored_stocks = []
        
        for symbol in symbols:
            try:
                data = feed.get_data(symbol)
                if data.empty:
                    continue
                
                # 计算股票热度评分
                score = self._calculate_stock_score(data)
                
                # 检查是否符合龙头股条件
                is_dragon = self._is_dragon_stock(symbol, data, dragon_filter)
                
                if is_dragon:
                    scored_stocks.append({
                        'symbol': symbol,
                        'score': score,
                        'is_hot_sector': self._is_in_hot_sectors(symbol)
                    })
                    
            except Exception as e:
                logger.warning(f"Failed to process {symbol}: {e}")
                continue
        
        # 步骤4: 排序并选择TOP股票
        # 优先选择热门板块的龙头股
        scored_stocks.sort(key=lambda x: (
            x['is_hot_sector'],  # 热门板块优先
            x['score']  # 然后按热度评分
        ), reverse=True)
        
        self.stock_pool = [s['symbol'] for s in scored_stocks[:self.top_stocks]]
        self.stock_scores = {s['symbol']: s['score'] for s in scored_stocks}
        
        result['stock_pool'] = self.stock_pool
        result['stock_scores'] = self.stock_scores
        self.last_update = datetime.now()
        
        print(f"筛选出 {len(self.stock_pool)} 只龙头股")
        
        return result
    
    def _calculate_stock_score(self, data: pd.DataFrame) -> float:
        """
        计算股票热度评分
        
        Args:
            data: 股票数据
        
        Returns:
            热度评分
        """
        if data.empty or len(data) < 20:
            return 0.0
        
        # 近20日动量
        momentum_20d = data['close'].pct_change(20).iloc[-1] if len(data) >= 20 else 0
        
        # 近5日动量
        momentum_5d = data['close'].pct_change(5).iloc[-1] if len(data) >= 5 else 0
        
        # 成交量变化
        vol_change = data['volume'].pct_change().iloc[-1] if 'volume' in data.columns else 0
        
        # 综合评分
        score = (momentum_20d * 0.4 + momentum_5d * 0.3 + vol_change * 0.3) * 100
        
        return round(score, 2)
    
    def _is_dragon_stock(self, symbol: str, data: pd.DataFrame, 
                         dragon_filter: DragonStockFilter) -> bool:
        """
        检查是否为龙头股
        
        Args:
            symbol: 股票代码
            data: 股票数据
            dragon_filter: 龙头股筛选器
        
        Returns:
            是否为龙头股
        """
        # 基础条件: 主板股票
        if not dragon_filter.is_main_board(symbol):
            return False
        
        # 基础条件: 数据充足
        if len(data) < 60:  # 至少3个月数据
            return False
        
        # 计算财务指标
        latest = data.iloc[-1]
        
        # 简单筛选条件
        # 1. 涨幅为正
        if data['close'].pct_change(20).iloc[-1] < 0:
            return False
        
        # 2. 成交量活跃
        if 'volume' in data.columns:
            vol_ma5 = data['volume'].tail(5).mean()
            vol_ma20 = data['volume'].tail(20).mean()
            if vol_ma5 < vol_ma20 * 0.8:
                return False
        
        return True
    
    def _is_in_hot_sectors(self, symbol: str) -> bool:
        """
        检查股票是否属于热门板块
        
        Args:
            symbol: 股票代码
        
        Returns:
            是否属于热门板块
        """
        # 板块映射
        sector_map = {
            '光通信': ['300308', '300502', '002281'],
            '电子': ['002371', '603501', '688981'],
            '计算机': ['002230', '688787'],
            '有色金属': ['601899', '603799', '600456'],
            '通信': ['002281'],
            '存储': ['603986', '688525'],
            '半导体': ['002371', '603501', '688981', '603986'],
            '锂电池': ['002460', '300750'],
        }
        
        code = symbol.split('.')[0]
        
        for sector, stocks in sector_map.items():
            if sector in self.hot_sectors and code in stocks:
                return True
        
        return False
    
    def get_top_stocks(self, n: int = 10, hot_sector_only: bool = False) -> List[str]:
        """
        获取TOP N龙头股
        
        Args:
            n: 返回数量
            hot_sector_only: 是否只返回热门板块的股票
        
        Returns:
            龙头股代码列表
        """
        if not self.stock_pool:
            self.refresh()
        
        if hot_sector_only:
            return [s for s in self.stock_pool if self._is_in_hot_sectors(s)][:n]
        
        return self.stock_pool[:n]
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        获取股票详细信息
        
        Args:
            symbol: 股票代码
        
        Returns:
            股票信息字典
        """
        return {
            'symbol': symbol,
            'score': self.stock_scores.get(symbol, 0),
            'in_hot_sector': self._is_in_hot_sectors(symbol),
            'hot_sectors': [s for s in self.hot_sectors if self._is_in_hot_sectors(symbol)]
        }
    
    def print_report(self):
        """打印龙头股票池报告"""
        print("\n" + "=" * 70)
        print("龙头股票池报告")
        print("=" * 70)
        
        print(f"\n更新时间: {self.last_update}")
        
        print(f"\n热门板块 TOP {self.top_sectors}:")
        print("-" * 40)
        for i, sector in enumerate(self.hot_sectors, 1):
            print(f"  {i:2d}. {sector}")
        
        print(f"\n龙头股票池 TOP {self.top_stocks}:")
        print("-" * 70)
        print(f"{'排名':<6} {'代码':<15} {'评分':<12} {'热门板块':<20}")
        print("-" * 70)
        
        for i, symbol in enumerate(self.stock_pool, 1):
            info = self.get_stock_info(symbol)
            hot_sectors = ', '.join(info['hot_sectors']) if info['hot_sectors'] else '-'
            print(f"{i:<6} {symbol:<15} {info['score']:<12.2f} {hot_sectors:<20}")
        
        print("-" * 70)
        print(f"共 {len(self.stock_pool)} 只龙头股")
        print("=" * 70)


# 使用示例
if __name__ == '__main__':
    pool = LeaderStockPool(
        data_dir='E:\\workspace\\AutoQuant\\data',
        top_sectors=10,
        top_stocks=20
    )
    
    # 刷新股票池
    pool.refresh()
    
    # 打印报告
    pool.print_report()
    
    # 获取TOP 10龙头股
    top_stocks = pool.get_top_stocks(n=10)
    print(f"\nTOP 10龙头股: {top_stocks}")