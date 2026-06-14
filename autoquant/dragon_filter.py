"""
龙头股筛选算法模块
实现机构级别的漏斗式股票筛选逻辑
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class StockFilterConfig:
    """股票筛选配置"""
    # 第一层：全局排雷
    exclude_st: bool = True
    exclude_paused: bool = True
    min_listing_days: int = 90  # 上市至少3个月
    
    # 主板股票过滤（默认只分析主板）
    main_board_only: bool = True  # 只分析主板股票
    
    # 第二层：龙头定位
    index_constituents: List[str] = None  # 指数成分股列表
    
    # 第三层：财务硬指标
    min_market_cap: float = 50  # 最小市值（亿）
    min_roe: float = 15.0  # ROE最低要求
    roe_years: int = 3  # ROE连续达标年数
    require_positive_profit: bool = True
    profit_growth_years: int = 3  # 利润连续增长年数
    max_debt_ratio: float = 50.0  # 资产负债率上限
    require_cash_flow: bool = True  # 经营现金流 > 净利润
    
    # 第四层：择优对比
    pe_threshold: float = 30.0  # PE上限
    pb_threshold: float = 5.0  # PB上限
    industry_comparison: bool = True  # 行业内对比


@dataclass
class FinancialData:
    """财务数据"""
    symbol: str
    market_cap: float  # 市值（亿）
    roe: List[float]  # ROE历史数据（年度）
    net_profit: List[float]  # 净利润（亿）
    operating_cash_flow: List[float]  # 经营现金流（亿）
    revenue: List[float]  # 营收（亿）
    gross_margin: List[float]  # 毛利率
    debt_ratio: float  # 资产负债率
    pe: float  # 市盈率
    pb: float  # 市净率
    listing_days: int  # 上市天数
    is_st: bool  # 是否ST
    is_paused: bool  # 是否停牌


class DragonStockFilter:
    """龙头股筛选器"""
    
    # 主板股票代码规则
    # 沪市主板: 600xxx, 601xxx, 603xxx (不含688科创板)
    # 深市主板: 000xxx, 001xxx (不含002已合并、300创业板、688科创板)
    MAIN_BOARD_PREFIXES = ['600', '601', '603', '000', '001']
    
    def __init__(self, config: StockFilterConfig = None):
        self.config = config or StockFilterConfig()
    
    @staticmethod
    def is_main_board(symbol: str) -> bool:
        """
        判断是否为主板股票
        
        主板股票规则:
        - 沪市主板: 600xxx, 601xxx, 603xxx
        - 深市主板: 000xxx, 001xxx
        
        排除:
        - 科创板: 688xxx
        - 创业板: 300xxx
        - 北交所: 8xxxxx, 4xxxxx
        """
        # 处理不同格式的股票代码
        code = symbol.split('.')[0] if '.' in symbol else symbol
        code = code.lstrip('0') if len(code) > 3 else code  # 去除前导0
        
        # 检查前缀
        for prefix in DragonStockFilter.MAIN_BOARD_PREFIXES:
            if symbol.startswith(prefix):
                return True
        
        # 特殊处理：SH/SZ后缀格式
        if '.SH' in symbol or '.SZ' in symbol:
            pure_code = symbol.split('.')[0]
            for prefix in DragonStockFilter.MAIN_BOARD_PREFIXES:
                if pure_code.startswith(prefix):
                    return True
        
        return False
    
    def filter_layer1_global(self, stocks: List[FinancialData]) -> List[FinancialData]:
        """
        第一层：全局排雷
        排除ST、*ST、停牌及上市不满3个月的次新股
        新增：主板股票过滤（可选）
        """
        filtered = []
        for stock in stocks:
            if self.config.exclude_st and stock.is_st:
                continue
            if self.config.exclude_paused and stock.is_paused:
                continue
            if stock.listing_days < self.config.min_listing_days:
                continue
            # 主板股票过滤
            if self.config.main_board_only and not self.is_main_board(stock.symbol):
                continue
            filtered.append(stock)
        
        logger.info(f"第一层筛选完成: {len(stocks)} -> {len(filtered)}")
        return filtered
    
    def filter_layer2_index_constituents(self, stocks: List[FinancialData]) -> List[FinancialData]:
        """
        第二层：龙头定位
        锁定主流指数成分股（中证A500、中证500、沪深300等）
        """
        if not self.config.index_constituents:
            logger.info("未设置指数成分股，跳过第二层筛选")
            return stocks
        
        filtered = [stock for stock in stocks 
                   if stock.symbol in self.config.index_constituents]
        
        logger.info(f"第二层筛选完成: {len(stocks)} -> {len(filtered)}")
        return filtered
    
    def filter_layer3_financial(self, stocks: List[FinancialData]) -> List[FinancialData]:
        """
        第三层：基本盘（财务硬指标）
        
        盈利能力：ROE连续3-5年高于15%，扣非净利润，经营现金流>净利润
        成长能力：营收与净利润双增，连续3年正增长
        健康度：毛利率稳定、资产负债率低于50%
        """
        filtered = []
        
        for stock in stocks:
            # 市值门槛
            if stock.market_cap < self.config.min_market_cap:
                continue
            
            # ROE连续达标
            valid_roe_years = sum(1 for r in stock.roe if r >= self.config.min_roe)
            if valid_roe_years < self.config.roe_years:
                continue
            
            # 净利润连续增长
            if self.config.require_positive_profit:
                positive_growth = 0
                for i in range(1, len(stock.net_profit)):
                    if stock.net_profit[i] > stock.net_profit[i-1]:
                        positive_growth += 1
                if positive_growth < self.config.profit_growth_years - 1:
                    continue
            
            # 资产负债率
            if stock.debt_ratio > self.config.max_debt_ratio:
                continue
            
            # 经营现金流验证
            if self.config.require_cash_flow:
                if len(stock.operating_cash_flow) > 0 and len(stock.net_profit) > 0:
                    recent_cash = stock.operating_cash_flow[-1] if stock.operating_cash_flow else 0
                    recent_profit = stock.net_profit[-1] if stock.net_profit else 0
                    if recent_cash < recent_profit:
                        continue
            
            filtered.append(stock)
        
        logger.info(f"第三层筛选完成: {len(stocks)} -> {len(filtered)}")
        return filtered
    
    def filter_layer4_valuation(self, stocks: List[FinancialData]) -> List[FinancialData]:
        """
        第四层：择优对比（估值与排名）
        PB-ROE矩阵、行业内横向对比
        """
        filtered = []
        
        for stock in stocks:
            # 估值筛选
            if stock.pe > self.config.pe_threshold:
                continue
            if stock.pb > self.config.pb_threshold:
                continue
            filtered.append(stock)
        
        # 行业内排序
        if self.config.industry_comparison and len(filtered) > 0:
            filtered = self._rank_by_industry(filtered)
        
        logger.info(f"第四层筛选完成: {len(stocks)} -> {len(filtered)}")
        return filtered
    
    def _rank_by_industry(self, stocks: List[FinancialData]) -> List[FinancialData]:
        """
        行业内排序
        综合ROE、成长、估值等指标进行排名
        """
        # 简化版：按ROE/PB比值排序（性价比）
        scored_stocks = []
        for stock in stocks:
            avg_roe = np.mean(stock.roe) if stock.roe else 0
            score = avg_roe / (stock.pb if stock.pb > 0 else 1)
            scored_stocks.append((stock, score))
        
        # 按得分降序排列，取前N个
        scored_stocks.sort(key=lambda x: x[1], reverse=True)
        return [stock for stock, score in scored_stocks]
    
    def run_full_filter(self, stocks: List[FinancialData]) -> Tuple[List[FinancialData], Dict[str, int]]:
        """
        执行完整的漏斗式筛选
        """
        stats = {}
        
        # 第一层：全局排雷
        result = self.filter_layer1_global(stocks)
        stats['layer1'] = len(result)
        
        # 第二层：龙头定位
        result = self.filter_layer2_index_constituents(result)
        stats['layer2'] = len(result)
        
        # 第三层：基本盘
        result = self.filter_layer3_financial(result)
        stats['layer3'] = len(result)
        
        # 第四层：择优对比
        result = self.filter_layer4_valuation(result)
        stats['layer4'] = len(result)
        
        logger.info(f"筛选完成: {len(stocks)} -> {len(result)}")
        return result, stats
    
    def get_top_stocks(self, stocks: List[FinancialData], top_n: int = 20) -> List[FinancialData]:
        """
        获取筛选后的龙头股列表
        """
        filtered, _ = self.run_full_filter(stocks)
        return filtered[:top_n]


class IndustryMomentumAnalyzer:
    """行业动量分析器"""
    
    def __init__(self):
        pass
    
    def calculate_industry_momentum(self, industry_data: Dict[str, pd.Series]) -> pd.Series:
        """
        计算行业动量
        返回各行业近20日累计涨跌幅排名
        """
        momentum = {}
        for industry, prices in industry_data.items():
            if len(prices) >= 20:
                recent_20 = prices[-20:]
                momentum[industry] = (recent_20.iloc[-1] / recent_20.iloc[0]) - 1
        
        return pd.Series(momentum).sort_values(ascending=False)
    
    def get_hot_industries(self, industry_data: Dict[str, pd.Series], top_n: int = 5) -> List[str]:
        """
        获取热门行业
        """
        momentum = self.calculate_industry_momentum(industry_data)
        return momentum.head(top_n).index.tolist()


def create_dragon_filter(index_type: str = 'a500') -> DragonStockFilter:
    """
    创建预设配置的龙头股筛选器
    
    index_type: 'a500' | '500' | '300'
    """
    config = StockFilterConfig()
    
    # 根据指数类型设置不同的筛选标准
    if index_type == 'a500':
        # 中证A500：行业均衡，覆盖各行业龙头
        config.min_market_cap = 80
        config.min_roe = 12.0
        config.roe_years = 3
    elif index_type == '500':
        # 中证500：高成长性"隐形冠军"
        config.min_market_cap = 50
        config.min_roe = 10.0
        config.roe_years = 2
    elif index_type == '300':
        # 沪深300：大盘蓝筹，稳健底仓
        config.min_market_cap = 200
        config.min_roe = 15.0
        config.roe_years = 4
    else:
        # 默认配置
        config.min_market_cap = 50
        config.min_roe = 15.0
        config.roe_years = 3
    
    return DragonStockFilter(config)


# 示例使用
if __name__ == "__main__":
    # 创建模拟数据
    mock_stocks = [
        FinancialData(
            symbol='SH600519',
            market_cap=2500,
            roe=[25, 28, 26],
            net_profit=[450, 500, 550],
            operating_cash_flow=[480, 520, 580],
            revenue=[1000, 1100, 1200],
            gross_margin=[90, 91, 92],
            debt_ratio=20,
            pe=25,
            pb=4.5,
            listing_days=3650,
            is_st=False,
            is_paused=False
        ),
        FinancialData(
            symbol='SZ000858',
            market_cap=1800,
            roe=[22, 24, 23],
            net_profit=[300, 350, 400],
            operating_cash_flow=[320, 360, 420],
            revenue=[800, 900, 1000],
            gross_margin=[85, 86, 87],
            debt_ratio=25,
            pe=28,
            pb=5.0,
            listing_days=3000,
            is_st=False,
            is_paused=False
        ),
        FinancialData(
            symbol='SH601318',
            market_cap=3500,
            roe=[18, 19, 20],
            net_profit=[600, 650, 700],
            operating_cash_flow=[620, 680, 720],
            revenue=[2000, 2200, 2400],
            gross_margin=[35, 36, 37],
            debt_ratio=45,
            pe=15,
            pb=2.5,
            listing_days=4000,
            is_st=False,
            is_paused=False
        ),
        # ST股票（应被排除）
        FinancialData(
            symbol='SH600001',
            market_cap=30,
            roe=[5, 3, -10],
            net_profit=[5, 3, -10],
            operating_cash_flow=[4, 2, -5],
            revenue=[50, 45, 40],
            gross_margin=[20, 18, 15],
            debt_ratio=70,
            pe=100,
            pb=8.0,
            listing_days=2000,
            is_st=True,
            is_paused=False
        ),
        # 次新股（应被排除）
        FinancialData(
            symbol='SH688001',
            market_cap=40,
            roe=[20, 22],
            net_profit=[2, 3],
            operating_cash_flow=[1, 2],
            revenue=[10, 15],
            gross_margin=[40, 42],
            debt_ratio=30,
            pe=50,
            pb=6.0,
            listing_days=60,  # 上市仅60天
            is_st=False,
            is_paused=False
        )
    ]
    
    # 创建筛选器
    filter = create_dragon_filter('a500')
    
    # 设置指数成分股（模拟）
    filter.config.index_constituents = ['SH600519', 'SZ000858', 'SH601318', 'SH688001']
    
    # 执行筛选
    result, stats = filter.run_full_filter(mock_stocks)
    
    print("=" * 60)
    print("龙头股筛选结果")
    print("=" * 60)
    print(f"初始股票数: {len(mock_stocks)}")
    print(f"各层筛选结果: {stats}")
    print(f"最终筛选结果: {len(result)} 只")
    print("-" * 60)
    
    for stock in result:
        print(f"{stock.symbol}: 市值={stock.market_cap}亿, ROE={stock.roe[-1]}%, PE={stock.pe}, PB={stock.pb}")
    
    print("=" * 60)