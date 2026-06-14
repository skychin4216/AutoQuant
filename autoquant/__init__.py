from .data import DataFeed
from .strategy import StrategyEngine, BaseStrategy
from .backtest import BackTestEngine
from .risk import RiskEngine
from .analyzer import PerformanceAnalyzer
from .dragon_filter import (
    DragonStockFilter, 
    StockFilterConfig, 
    FinancialData, 
    IndustryMomentumAnalyzer,
    create_dragon_filter
)
from .hot_analyzer import (
    HotStockAnalyzer,
    HotStock,
    HotSector
)

# vn.py Integration
try:
    from .vnpy_integration import VnpyTrader, VnpyConfig, VnpyCTAStrategy, run_vnpy_gui
    VNPY_AVAILABLE = True
except ImportError:
    VNPY_AVAILABLE = False

# Qlib Integration  
try:
    from .qlib_integration import QlibResearch, RDAGentResearch, download_qlib_data
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False

__all__ = [
    'DataFeed',
    'StrategyEngine',
    'BaseStrategy',
    'BackTestEngine',
    'RiskEngine',
    'PerformanceAnalyzer',
    # Dragon Stock Filter
    'DragonStockFilter',
    'StockFilterConfig',
    'FinancialData',
    'IndustryMomentumAnalyzer',
    'create_dragon_filter',
    # Hot Stock Analyzer
    'HotStockAnalyzer',
    'HotStock',
    'HotSector',
    # vn.py
    'VnpyTrader',
    'VnpyConfig',
    'VnpyCTAStrategy',
    'run_vnpy_gui',
    'VNPY_AVAILABLE',
    # Qlib
    'QlibResearch',
    'RDAGentResearch',
    'download_qlib_data',
    'QLIB_AVAILABLE',
]

__version__ = '1.0.0'