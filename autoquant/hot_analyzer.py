"""
热门板块和热门股票分析器
通过交易数据动态统计2025年至今的热门板块和热门股票

参考DeepSeek的板块热点排名算法:
1. 动量得分 - 短期涨跌幅
2. 资金得分 - 成交量变化
3. 相对强度得分 - 相对基准指数的表现
4. Z-score标准化计算综合得分

分析维度:
1. 行业动量 - 计算各行业近N日累计涨跌幅
2. 资金流向 - 成交量短期vs长期对比
3. 相对强度 - 相对沪深300的表现
4. 成交额排名 - 统计成交额TOP股票
5. 连板统计 - 统计连续涨停股票
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from loguru import logger

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning("akshare not installed, using simulated data")


@dataclass
class HotStock:
    """热门股票数据结构"""
    symbol: str
    name: str
    sector: str  # 所属板块
    sub_sector: str  # 子板块
    
    # 价格指标
    close: float  # 最新收盘价
    change_pct: float  # 涨跌幅%
    turnover_rate: float  # 换手率%
    
    # 成交指标
    volume: float  # 成交量
    amount: float  # 成交额(万元)
    amount_rank: int  # 成交额排名
    
    # 动量指标
    momentum_5d: float  # 5日动量
    momentum_10d: float  # 10日动量
    momentum_20d: float  # 20日动量
    
    # 连板统计
    consecutive_up: int  # 连续涨停天数
    consecutive_down: int  # 连续跌停天数
    
    # 热度评分
    hot_score: float  # 综合热度评分(0-100)
    
    # 板块排名
    sector_rank: int  # 板块内排名


@dataclass
class HotSector:
    """热门板块数据结构"""
    sector: str  # 板块名称
    sub_sector: str  # 子板块名称
    
    # 板块指标
    sector_change_pct: float  # 板块涨跌幅%
    sector_momentum_5d: float  # 5日动量
    sector_momentum_10d: float  # 10日动量
    sector_momentum_20d: float  # 20日动量
    
    # 成交指标
    sector_amount: float  # 板块总成交额(亿元)
    sector_amount_rank: int  # 成交额排名
    
    # 资金流向
    net_inflow: float  # 净流入(亿元)
    net_inflow_rank: int  # 净流入排名
    
    # 板块热度
    sector_hot_score: float  # 板块热度评分(0-100)
    
    # DeepSeek评分因子
    momentum_score: float  # 动量得分
    fund_score: float  # 资金得分
    relative_strength: float  # 相对强度得分
    composite_score: float  # 综合得分(Z-score)
    
    # 板块内热门股票
    hot_stocks: List[HotStock] = field(default_factory=list)


class SectorHotRanker:
    """
    板块热点排名器 - 参考DeepSeek算法
    
    使用akshare获取真实的板块数据，通过三个因子计算综合得分:
    1. 动量得分 - 短期涨跌幅
    2. 资金得分 - 成交量短期vs长期对比
    3. 相对强度得分 - 相对沪深300的表现
    
    使用方法:
    >>> ranker = SectorHotRanker(lookback_days=20, rank_days=5)
    >>> top_sectors = ranker.get_top_sectors(n=20)
    """
    
    def __init__(self, end_date: str = None, lookback_days: int = 20, rank_days: int = 5):
        """
        初始化板块热点排名器
        
        Args:
            end_date: 结束日期，格式YYYYMMDD（默认最新交易日）
            lookback_days: 回溯天数（默认20日）
            rank_days: 排名计算天数（默认5日）
        """
        if end_date:
            self.end_date = datetime.strptime(end_date, "%Y%m%d").date()
        else:
            self.end_date = datetime.today().date()
        
        self.lookback_days = lookback_days
        self.rank_days = rank_days
        self.benchmark_data = None
        
        logger.info(f"SectorHotRanker initialized: end_date={self.end_date}, lookback={lookback_days}, rank={rank_days}")
    
    def get_sector_data(self) -> Dict[str, pd.DataFrame]:
        """
        步骤1：获取所有板块的历史行情数据（申万一级行业）
        
        Returns:
            板块数据字典 {板块名称: DataFrame}
        """
        if not AKSHARE_AVAILABLE:
            logger.warning("akshare not available, returning simulated sector data")
            return self._get_simulated_sector_data()
        
        print(f"正在获取 {self.lookback_days} 个交易日的板块数据...")
        
        all_data = {}
        try:
            # 获取申万一级行业列表
            sector_info = ak.sw_index_spot()
            
            for code, name in zip(sector_info['指数代码'], sector_info['指数名称']):
                try:
                    # 获取板块日线数据
                    daily = ak.index_daily(symbol=code)
                    daily['trade_date'] = pd.to_datetime(daily['date'])
                    daily.set_index('trade_date', inplace=True)
                    
                    # 过滤到结束日期
                    mask = daily.index <= pd.Timestamp(self.end_date)
                    all_data[name] = daily[mask].tail(self.lookback_days)
                except Exception as e:
                    logger.warning(f"Failed to get data for {name}: {e}")
                    continue
            
            logger.info(f"Successfully loaded {len(all_data)} sectors")
        except Exception as e:
            logger.error(f"Failed to get sector info: {e}")
            return self._get_simulated_sector_data()
        
        return all_data
    
    def _get_simulated_sector_data(self) -> Dict[str, pd.DataFrame]:
        """
        生成模拟板块数据（当akshare不可用时）
        
        Returns:
            模拟板块数据
        """
        # 申万一级行业主要板块
        sectors = [
            '通信', '电子', '计算机', '传媒', '电力设备',
            '有色金属', '钢铁', '基础化工', '建筑材料', '机械设备',
            '汽车', '家用电器', '食品饮料', '医药生物', '银行',
            '非银金融', '房地产', '商贸零售', '社会服务', '交通运输'
        ]
        
        all_data = {}
        dates = pd.date_range(end=self.end_date, periods=self.lookback_days, freq='D')
        
        for sector in sectors:
            # 生成模拟数据
            np.random.seed(hash(sector) % 10000)
            base_price = 1000
            returns = np.random.normal(0.002, 0.02, self.lookback_days)
            close = base_price * np.exp(np.cumsum(returns))
            volume = np.random.randint(100000, 1000000, self.lookback_days)
            
            df = pd.DataFrame({
                'close': close,
                'vol': volume,
                'amount': close * volume
            }, index=dates)
            
            all_data[sector] = df
        
        return all_data
    
    def get_benchmark_data(self) -> pd.DataFrame:
        """
        获取基准指数(沪深300)数据
        
        Returns:
            沪深300数据DataFrame
        """
        if self.benchmark_data is not None:
            return self.benchmark_data
        
        if not AKSHARE_AVAILABLE:
            # 模拟沪深300数据
            dates = pd.date_range(end=self.end_date, periods=self.lookback_days + 10, freq='D')
            np.random.seed(42)
            base_price = 4000
            returns = np.random.normal(0.001, 0.01, len(dates))
            close = base_price * np.exp(np.cumsum(returns))
            
            self.benchmark_data = pd.DataFrame({'close': close}, index=dates)
            return self.benchmark_data
        
        try:
            benchmark = ak.index_daily(symbol="000300")
            benchmark.set_index(pd.to_datetime(benchmark['date']), inplace=True)
            self.benchmark_data = benchmark
            return benchmark
        except Exception as e:
            logger.error(f"Failed to get benchmark data: {e}")
            return self._get_simulated_sector_data()['银行']  # 用模拟数据替代
    
    def calculate_momentum(self, sector_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        步骤2：为每个板块计算动量、资金、相对强度因子
        
        Args:
            sector_data: 板块数据字典
        
        Returns:
            评分DataFrame
        """
        # 获取基准数据
        benchmark = self.get_benchmark_data()
        bench_ret = benchmark['close'].pct_change(self.rank_days).dropna()
        
        scores = []
        for name, df in sector_data.items():
            if df.empty or len(df) < self.rank_days:
                continue
            
            # 因子1: 短期动量得分
            momentum = df['close'].pct_change(self.rank_days).iloc[-1]
            
            # 因子2: 资金热度得分（成交量短期vs长期）
            vol_mean_short = df['vol'].tail(self.rank_days).mean()
            vol_mean_long = df['vol'].tail(self.lookback_days).mean()
            fund_flow = (vol_mean_short / vol_mean_long - 1) if vol_mean_long > 0 else 0
            
            # 因子3: 相对强度得分（相对沪深300）
            try:
                sector_ret = df['close'].pct_change(self.rank_days).iloc[-1]
                bench_ret_day = bench_ret[bench_ret.index <= pd.Timestamp(self.end_date)].iloc[-1]
                relative_strength = sector_ret - bench_ret_day
            except (IndexError, KeyError):
                relative_strength = 0
            
            scores.append({
                '板块名称': name,
                '动量得分': momentum,
                '资金得分': fund_flow,
                '相对强度得分': relative_strength
            })
        
        return pd.DataFrame(scores)
    
    def rank_by_score(self, scores_df: pd.DataFrame) -> pd.DataFrame:
        """
        步骤3：综合打分并排序（Z-score标准化）
        
        Args:
            scores_df: 评分DataFrame
        
        Returns:
            排序后的评分DataFrame
        """
        if scores_df.empty:
            return scores_df
        
        # 对每个因子进行Z-score标准化
        for col in ['动量得分', '资金得分', '相对强度得分']:
            if col in scores_df.columns and scores_df[col].std() != 0:
                scores_df[f'{col}_z'] = (scores_df[col] - scores_df[col].mean()) / scores_df[col].std()
            else:
                scores_df[f'{col}_z'] = 0
        
        # 3个因子等权重计算综合得分
        scores_df['综合得分'] = (
            scores_df['动量得分_z'] + 
            scores_df['资金得分_z'] + 
            scores_df['相对强度得分_z']
        ) / 3
        
        return scores_df.sort_values('综合得分', ascending=False)
    
    def get_top_sectors(self, n: int = 20) -> pd.DataFrame:
        """
        主流程：执行并返回热门板块Top N
        
        Args:
            n: 返回数量（默认20）
        
        Returns:
            热门板块排名DataFrame
        """
        sector_data = self.get_sector_data()
        scores_df = self.calculate_momentum(sector_data)
        ranked_df = self.rank_by_score(scores_df)
        
        print(f"\n热门板块排名(基于近{self.rank_days}个交易日动量, {self.lookback_days}日资金对比)")
        print("=" * 70)
        
        return ranked_df[['板块名称', '动量得分', '资金得分', '相对强度得分', '综合得分']].head(n)
    
    def print_top_sectors(self, n: int = 20):
        """
        打印热门板块排名
        
        Args:
            n: 显示数量（默认20）
        """
        top_sectors = self.get_top_sectors(n)
        
        print(f"\n{'排名':<6} {'板块名称':<15} {'动量得分':<12} {'资金得分':<12} {'相对强度':<12} {'综合得分':<10}")
        print("-" * 70)
        
        for i, (_, row) in enumerate(top_sectors.iterrows(), 1):
            print(f"{i:<6} {row['板块名称']:<15} {row['动量得分']:<12.4f} {row['资金得分']:<12.4f} {row['相对强度得分']:<12.4f} {row['综合得分']:<10.4f}")
        
        print("-" * 70)
        print(f"共 {len(top_sectors)} 个热门板块")


class HotStockAnalyzer:
    """
    热门股票分析器
    
    通过交易数据动态统计热门板块和热门股票
    
    使用方法:
    >>> analyzer = HotStockAnalyzer(data_dir='E:\\workspace\\AutoQuant\\data')
    >>> hot_sectors = analyzer.get_hot_sectors(top_n=5)
    >>> hot_stocks = analyzer.get_hot_stocks(top_n=10)
    """
    
    # 行业分类映射（A股主要行业）
    SECTOR_MAPPING = {
        # 科技板块
        '光通信': ['300308', '300502', '002281', '002475', '300620'],
        '半导体': ['002371', '603501', '688981', '688525', '603986', '002049'],
        '存储': ['603986', '688525', '002077'],
        'AI算力': ['300308', '300502', '002230', '688787'],
        
        # 新能源板块
        '新能源车': ['002594', '300750', '002460', '002466', '002475'],
        '锂电池': ['002460', '300750', '002466', '002756'],
        '光伏': ['601012', '002459', '300274', '688599'],
        
        # 有色金属板块
        '稀土': ['600111', '000831', '002497'],
        '锂矿': ['002460', '002466', '300750'],
        '钼矿': ['603993', '002475'],
        '有色金属': ['601899', '603799', '600456', '000960'],
        
        # 消费板块
        '白酒': ['600519', '000858', '000568', '002304'],
        '家电': ['000333', '000651', '600690'],
        '免税': ['601888', '000333'],
        
        # 金融板块
        '银行': ['600036', '601318', '601166', '600016'],
        '保险': ['601318', '601601', '000627'],
        
        # 医药板块
        '医药': ['300760', '002007', '600276', '000538'],
        '中药': ['600276', '000538', '002007'],
    }
    
    def __init__(self, data_dir: str = 'E:\\workspace\\AutoQuant\\data', 
                 start_date: str = '2025-01-01',
                 end_date: str = None):
        """
        初始化热门股票分析器
        
        Args:
            data_dir: 数据目录
            start_date: 开始日期（默认2025-01-01）
            end_date: 结束日期（默认最新交易日）
        """
        self.data_dir = data_dir
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        
        self.stock_data = {}  # 股票数据缓存
        self.sector_data = {}  # 板块数据缓存
        
        logger.info(f"HotStockAnalyzer initialized: {start_date} ~ {end_date}")
    
    def load_stock_data(self, symbol: str) -> pd.DataFrame:
        """加载单只股票数据"""
        import os
        
        # 构建文件路径（支持带中文描述的文件名）
        for f in os.listdir(self.data_dir):
            if f.endswith('.csv') and f.startswith(symbol.split('.')[0]):
                file_path = os.path.join(self.data_dir, f)
                data = pd.read_csv(file_path)
                data['date'] = pd.to_datetime(data['date'])
                data['symbol'] = symbol
                
                # 计算涨跌幅
                data['change_pct'] = data['close'].pct_change() * 100
                
                # 计算换手率（模拟）
                if 'volume' in data.columns and 'close' in data.columns:
                    # 模拟流通市值 = close * volume * 10
                    data['turnover_rate'] = data['volume'] / (data['close'] * data['volume'].mean() * 10) * 100
                
                # 计算成交额
                data['amount'] = data['close'] * data['volume'] / 10000  # 万元
                
                return data
        
        return pd.DataFrame()
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """加载所有股票数据"""
        import os
        
        if self.stock_data:
            return self.stock_data
        
        symbols = []
        for f in os.listdir(self.data_dir):
            if f.endswith('.csv'):
                symbol = f.split('_')[0]
                symbols.append(symbol)
        
        for symbol in symbols:
            data = self.load_stock_data(symbol)
            if not data.empty:
                self.stock_data[symbol] = data
        
        logger.info(f"Loaded {len(self.stock_data)} stocks data")
        return self.stock_data
    
    def calculate_momentum(self, data: pd.DataFrame, days: int = 20) -> float:
        """
        计算动量指标
        
        Args:
            data: 股票数据
            days: 计算天数
        
        Returns:
            动量值（累计涨跌幅）
        """
        if len(data) < days:
            days = len(data)
        
        recent_data = data.tail(days)
        if recent_data.empty or 'change_pct' not in recent_data.columns:
            return 0.0
        
        momentum = recent_data['change_pct'].sum()
        return momentum
    
    def calculate_consecutive_up(self, data: pd.DataFrame) -> int:
        """
        计算连续涨停天数
        
        Args:
            data: 股票数据
        
        Returns:
            连续涨停天数
        """
        if 'change_pct' not in data.columns:
            return 0
        
        # 涨停标准：涨幅>=9.9%
        recent = data.tail(30)
        consecutive = 0
        for pct in reversed(recent['change_pct'].values):
            if pct >= 9.9:
                consecutive += 1
            else:
                break
        
        return consecutive
    
    def get_stock_sector(self, symbol: str) -> Tuple[str, str]:
        """
        获取股票所属板块
        
        Args:
            symbol: 股票代码
        
        Returns:
            (板块, 子板块)
        """
        code = symbol.split('.')[0]
        
        for sector, stocks in self.SECTOR_MAPPING.items():
            if code in stocks:
                # 子板块细分
                if '光通信' in sector or 'AI算力' in sector:
                    return '科技', sector
                elif '半导体' in sector or '存储' in sector:
                    return '科技', sector
                elif '新能源车' in sector or '锂电池' in sector or '光伏' in sector:
                    return '新能源', sector
                elif '稀土' in sector or '锂矿' in sector or '钼矿' in sector or '有色金属' in sector:
                    return '有色金属', sector
                elif '白酒' in sector or '家电' in sector or '免税' in sector:
                    return '消费', sector
                elif '银行' in sector or '保险' in sector:
                    return '金融', sector
                elif '医药' in sector or '中药' in sector:
                    return '医药', sector
                return sector, sector
        
        return '其他', '其他'
    
    def calculate_hot_score(self, stock_data: pd.DataFrame, symbol: str) -> float:
        """
        计算股票热度评分
        
        评分维度:
        - 动量权重: 40%
        - 成交额权重: 30%
        - 换手率权重: 20%
        - 连板权重: 10%
        
        Args:
            stock_data: 股票数据
            symbol: 股票代码
        
        Returns:
            热度评分(0-100)
        """
        score = 0.0
        
        # 1. 动量评分 (40%)
        momentum_20 = self.calculate_momentum(stock_data, 20)
        momentum_score = min(max(momentum_20, -20), 20) / 20 * 40  # -20%~20% 映射到 0~40
        score += momentum_score
        
        # 2. 成交额评分 (30%)
        recent_amount = stock_data.tail(5)['amount'].mean() if 'amount' in stock_data.columns else 0
        amount_score = min(recent_amount / 10000, 30)  # 成交额映射到 0~30
        score += amount_score
        
        # 3. 换手率评分 (20%)
        recent_turnover = stock_data.tail(5)['turnover_rate'].mean() if 'turnover_rate' in stock_data.columns else 0
        turnover_score = min(recent_turnover / 10, 20)  # 换手率映射到 0~20
        score += turnover_score
        
        # 4. 连板评分 (10%)
        consecutive = self.calculate_consecutive_up(stock_data)
        consecutive_score = min(consecutive * 2, 10)  # 连板天数映射到 0~10
        score += consecutive_score
        
        return round(score, 2)
    
    def get_hot_stocks(self, top_n: int = 10, sector: str = None) -> List[HotStock]:
        """
        获取热门股票
        
        Args:
            top_n: 返回数量
            sector: 指定板块（可选）
        
        Returns:
            热门股票列表
        """
        all_data = self.load_all_data()
        hot_stocks = []
        
        for symbol, data in all_data.items():
            # 过滤日期范围
            data = data[(data['date'] >= self.start_date) & (data['date'] <= self.end_date)]
            if data.empty:
                continue
            
            # 获取板块
            main_sector, sub_sector = self.get_stock_sector(symbol)
            
            # 如果指定板块，则过滤
            if sector and main_sector != sector and sub_sector != sector:
                continue
            
            # 计算指标
            latest = data.iloc[-1]
            momentum_5d = self.calculate_momentum(data, 5)
            momentum_10d = self.calculate_momentum(data, 10)
            momentum_20d = self.calculate_momentum(data, 20)
            consecutive_up = self.calculate_consecutive_up(data)
            hot_score = self.calculate_hot_score(data, symbol)
            
            # 获取股票名称
            name = self._get_stock_name(symbol)
            
            stock = HotStock(
                symbol=symbol,
                name=name,
                sector=main_sector,
                sub_sector=sub_sector,
                close=latest.get('close', 0),
                change_pct=latest.get('change_pct', 0),
                turnover_rate=latest.get('turnover_rate', 0),
                volume=latest.get('volume', 0),
                amount=latest.get('amount', 0),
                amount_rank=0,  # 后续计算
                momentum_5d=momentum_5d,
                momentum_10d=momentum_10d,
                momentum_20d=momentum_20d,
                consecutive_up=consecutive_up,
                consecutive_down=0,
                hot_score=hot_score,
                sector_rank=0  # 后续计算
            )
            
            hot_stocks.append(stock)
        
        # 按热度评分排序
        hot_stocks.sort(key=lambda x: x.hot_score, reverse=True)
        
        # 设置排名
        for i, stock in enumerate(hot_stocks[:top_n]):
            stock.amount_rank = i + 1
        
        return hot_stocks[:top_n]
    
    def get_hot_sectors(self, top_n: int = 5) -> List[HotSector]:
        """
        获取热门板块
        
        Args:
            top_n: 返回数量
        
        Returns:
            热门板块列表
        """
        all_data = self.load_all_data()
        
        # 按板块聚合数据
        sector_stocks = {}
        for symbol, data in all_data.items():
            main_sector, sub_sector = self.get_stock_sector(symbol)
            
            key = (main_sector, sub_sector)
            if key not in sector_stocks:
                sector_stocks[key] = []
            sector_stocks[key].append((symbol, data))
        
        # 计算板块指标
        hot_sectors = []
        for (main_sector, sub_sector), stocks in sector_stocks.items():
            # 计算板块平均涨跌幅
            sector_changes = []
            sector_momentum_5d = []
            sector_momentum_10d = []
            sector_momentum_20d = []
            sector_amounts = []
            sector_scores = []
            
            hot_stocks_in_sector = []
            
            for symbol, data in stocks:
                data = data[(data['date'] >= self.start_date) & (data['date'] <= self.end_date)]
                if data.empty:
                    continue
                
                latest = data.iloc[-1]
                sector_changes.append(latest.get('change_pct', 0))
                sector_momentum_5d.append(self.calculate_momentum(data, 5))
                sector_momentum_10d.append(self.calculate_momentum(data, 10))
                sector_momentum_20d.append(self.calculate_momentum(data, 20))
                sector_amounts.append(data['amount'].sum() if 'amount' in data.columns else 0)
                
                # 计算股票热度
                hot_score = self.calculate_hot_score(data, symbol)
                sector_scores.append(hot_score)
                
                # 创建热门股票对象
                name = self._get_stock_name(symbol)
                stock = HotStock(
                    symbol=symbol,
                    name=name,
                    sector=main_sector,
                    sub_sector=sub_sector,
                    close=latest.get('close', 0),
                    change_pct=latest.get('change_pct', 0),
                    turnover_rate=latest.get('turnover_rate', 0),
                    volume=latest.get('volume', 0),
                    amount=latest.get('amount', 0),
                    amount_rank=0,
                    momentum_5d=self.calculate_momentum(data, 5),
                    momentum_10d=self.calculate_momentum(data, 10),
                    momentum_20d=self.calculate_momentum(data, 20),
                    consecutive_up=self.calculate_consecutive_up(data),
                    consecutive_down=0,
                    hot_score=hot_score,
                    sector_rank=0
                )
                hot_stocks_in_sector.append(stock)
            
            if not sector_changes:
                continue
            
            # 板块指标
            sector_change_pct = np.mean(sector_changes)
            avg_momentum_5d = np.mean(sector_momentum_5d)
            avg_momentum_10d = np.mean(sector_momentum_10d)
            avg_momentum_20d = np.mean(sector_momentum_20d)
            total_amount = np.sum(sector_amounts) / 100000000  # 亿元
            avg_score = np.mean(sector_scores)
            
            # 板块热度评分
            sector_hot_score = (
                min(max(avg_momentum_20d, -20), 20) / 20 * 40 +  # 动量
                min(total_amount / 100, 30) +  # 成交额
                min(avg_score / 100, 30)  # 股票平均热度
            )
            
            # 按热度排序板块内股票
            hot_stocks_in_sector.sort(key=lambda x: x.hot_score, reverse=True)
            for i, stock in enumerate(hot_stocks_in_sector[:5]):
                stock.sector_rank = i + 1
            
            sector = HotSector(
                sector=main_sector,
                sub_sector=sub_sector,
                sector_change_pct=round(sector_change_pct, 2),
                sector_momentum_5d=round(avg_momentum_5d, 2),
                sector_momentum_10d=round(avg_momentum_10d, 2),
                sector_momentum_20d=round(avg_momentum_20d, 2),
                sector_amount=round(total_amount, 2),
                sector_amount_rank=0,
                net_inflow=0,  # 需要额外数据
                net_inflow_rank=0,
                sector_hot_score=round(sector_hot_score, 2),
                hot_stocks=hot_stocks_in_sector[:5]
            )
            
            hot_sectors.append(sector)
        
        # 按板块热度排序
        hot_sectors.sort(key=lambda x: x.sector_hot_score, reverse=True)
        
        # 设置排名
        for i, sector in enumerate(hot_sectors[:top_n]):
            sector.sector_amount_rank = i + 1
        
        return hot_sectors[:top_n]
    
    def _get_stock_name(self, symbol: str) -> str:
        """从文件名获取股票名称"""
        import os
        
        for f in os.listdir(self.data_dir):
            if f.endswith('.csv') and f.startswith(symbol.split('.')[0]):
                # 文件名格式: 600519.SH_贵州茅台-白酒龙头.csv
                parts = f.replace('.csv', '').split('_')
                if len(parts) >= 2:
                    name_desc = parts[1]
                    # 分离名称和描述
                    if '-' in name_desc:
                        return name_desc.split('-')[0]
                    elif '(' in name_desc:
                        return name_desc.split('(')[0]
                    return name_desc
        
        return symbol
    
    def print_hot_sectors(self, top_n: int = 5):
        """打印热门板块报告"""
        hot_sectors = self.get_hot_sectors(top_n)
        
        print("=" * 70)
        print(f"热门板块分析报告 ({self.start_date} ~ {self.end_date})")
        print("=" * 70)
        
        for i, sector in enumerate(hot_sectors, 1):
            print(f"\n【TOP {i}】{sector.sector} - {sector.sub_sector}")
            print(f"  板块涨跌幅: {sector.sector_change_pct}%")
            print(f"  20日动量: {sector.sector_momentum_20d}%")
            print(f"  板块成交额: {sector.sector_amount}亿元")
            print(f"  板块热度: {sector.sector_hot_score}")
            print(f"  板块内热门股票:")
            
            for stock in sector.hot_stocks[:3]:
                print(f"    - {stock.symbol} {stock.name}: 热度{stock.hot_score}, 动量{stock.momentum_20d}%")
        
        print("\n" + "=" * 70)
    
    def print_hot_stocks(self, top_n: int = 10, sector: str = None):
        """打印热门股票报告"""
        hot_stocks = self.get_hot_stocks(top_n, sector)
        
        print("=" * 70)
        print(f"热门股票分析报告 ({self.start_date} ~ {self.end_date})")
        if sector:
            print(f"筛选板块: {sector}")
        print("=" * 70)
        
        print(f"\n{'排名':<6} {'代码':<12} {'名称':<10} {'板块':<10} {'热度':<8} {'20日动量':<10} {'成交额(万)':<12}")
        print("-" * 70)
        
        for stock in hot_stocks:
            print(f"{stock.amount_rank:<6} {stock.symbol:<12} {stock.name:<10} {stock.sub_sector:<10} {stock.hot_score:<8} {stock.momentum_20d:<10.2f}% {stock.amount:<12.0f}")
        
        print("-" * 70)
        print(f"共 {len(hot_stocks)} 只热门股票")


# 使用示例
if __name__ == '__main__':
    analyzer = HotStockAnalyzer(
        data_dir='E:\\workspace\\AutoQuant\\data',
        start_date='2025-01-01',
        end_date=datetime.now().strftime('%Y-%m-%d')
    )
    
    # 打印热门板块
    analyzer.print_hot_sectors(top_n=5)
    
    # 打印热门股票
    analyzer.print_hot_stocks(top_n=10)