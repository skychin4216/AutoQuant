"""
Qlib Integration Module
Provides access to Qlib quantitative research framework and RD-Agent
"""

import sys
import os
from typing import Optional, Dict, Any, List
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

try:
    import qlib
    from qlib.data import D
    from qlib.config import REG_CN
    from qlib.contrib.model import LGBModel, XGBModel
    from qlib.contrib.data.handler import Alpha158
    from qlib.contrib.strategy import TopkDropoutStrategy
    from qlib.workflow import R
    from qlib.workflow.record_temp import SignalRecord, PortAnaRecord
    from qlib.utils import init_instance_by_config
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False
    logger.warning("Qlib not installed, research features disabled")


class QlibResearch:
    """Qlib Research Interface"""
    
    def __init__(self):
        if not QLIB_AVAILABLE:
            raise ImportError("Qlib not installed")
        
        self.initialized = False
        self.data_path = None
    
    def init(self, data_path: str = None, region: str = "cn"):
        """Initialize Qlib"""
        if self.initialized:
            return
        
        self.data_path = data_path or os.path.join(os.path.expanduser("~"), ".qlib", "qlib_data", region)
        
        try:
            qlib.init(
                provider_uri=self.data_path,
                region=REG_CN if region == "cn" else region
            )
            self.initialized = True
            logger.info(f"Qlib initialized with data path: {self.data_path}")
        except Exception as e:
            logger.error(f"Qlib initialization failed: {e}")
            raise
    
    def get_stock_list(self, market: str = "all") -> List[str]:
        """Get list of stocks"""
        if not self.initialized:
            self.init()
        
        return D.instruments(market=market)
    
    def get_price_data(self, symbols: List[str], start_date: str, 
                       end_date: str, fields: List[str] = None) -> pd.DataFrame:
        """Get price data"""
        if not self.initialized:
            self.init()
        
        fields = fields or ["open", "close", "high", "low", "volume"]
        return D.features(symbols, fields, start_date=start_date, end_date=end_date)
    
    def get_factor_data(self, symbols: List[str], start_date: str, 
                        end_date: str) -> pd.DataFrame:
        """Get factor data using Alpha158"""
        if not self.initialized:
            self.init()
        
        handler = Alpha158(
            instruments=symbols,
            start_time=start_date,
            end_time=end_date
        )
        return handler.fetch()
    
    def train_model(self, config: Dict[str, Any]) -> Any:
        """Train a model"""
        if not self.initialized:
            self.init()
        
        try:
            model = init_instance_by_config(config)
            model.fit()
            logger.info("Model training completed")
            return model
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise
    
    def run_backtest(self, model, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run backtest with Qlib"""
        if not self.initialized:
            self.init()
        
        try:
            strategy = init_instance_by_config(strategy_config)
            pred_score = model.predict()
            
            with R.start(experiment_name="backtest"):
                sr = SignalRecord(signal=pred_score)
                sr.generate()
                
                par = PortAnaRecord(
                    strategy=strategy,
                    signal=pred_score
                )
                par.generate()
                
                report = par.report
                return report
        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            raise
    
    def get_alpha_factors(self, symbols: List[str], start_date: str, 
                         end_date: str) -> pd.DataFrame:
        """Get Alpha158 factors"""
        if not self.initialized:
            self.init()
        
        handler = Alpha158(
            instruments=symbols,
            start_time=start_date,
            end_time=end_date
        )
        return handler.fetch()
    
    def optimize_params(self, model_config: Dict[str, Any], 
                       param_grid: Dict[str, List[Any]]) -> Dict[str, Any]:
        """Optimize model parameters"""
        if not self.initialized:
            self.init()
        
        best_params = None
        best_score = float('-inf')
        
        for params in self._generate_param_combinations(param_grid):
            try:
                config = model_config.copy()
                config["kwargs"].update(params)
                
                model = init_instance_by_config(config)
                model.fit()
                
                score = model.score()
                if score > best_score:
                    best_score = score
                    best_params = params
            except Exception as e:
                logger.warning(f"Parameter combination failed: {e}")
        
        return best_params
    
    def _generate_param_combinations(self, param_grid: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Generate all parameter combinations"""
        from itertools import product
        
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        
        combinations = []
        for combo in product(*values):
            combinations.append(dict(zip(keys, combo)))
        
        return combinations


class RDAGentResearch:
    """RD-Agent Research Assistant"""
    
    def __init__(self):
        if not QLIB_AVAILABLE:
            raise ImportError("Qlib not installed")
        
        self.qlib_research = QlibResearch()
    
    def init(self, data_path: str = None):
        """Initialize RD-Agent"""
        self.qlib_research.init(data_path)
    
    def analyze_stock(self, symbol: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Analyze a single stock"""
        data = self.qlib_research.get_price_data([symbol], start_date, end_date)
        
        analysis = {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "total_return": float((data["close"].iloc[-1] / data["close"].iloc[0]) - 1),
            "volatility": float(data["close"].pct_change().std() * np.sqrt(252)),
            "max_drawdown": float(self._calculate_max_drawdown(data["close"])),
            "avg_volume": float(data["volume"].mean()),
            "data_points": len(data)
        }
        
        return analysis
    
    def factor_analysis(self, symbols: List[str], start_date: str, 
                        end_date: str) -> pd.DataFrame:
        """Perform factor analysis"""
        factors = self.qlib_research.get_alpha_factors(symbols, start_date, end_date)
        return factors.corr()
    
    def strategy_research(self, symbols: List[str], start_date: str, 
                         end_date: str) -> Dict[str, Any]:
        """Run strategy research"""
        # Get factor data
        handler = Alpha158(
            instruments=symbols,
            start_time=start_date,
            end_time=end_date
        )
        
        data = handler.fetch()
        
        # Train model
        model_config = {
            "class": "LGBModel",
            "kwargs": {
                "loss": "mse",
                "colsample_bytree": 0.8,
                "learning_rate": 0.05,
                "n_estimators": 100,
                "num_leaves": 31,
                "reg_alpha": 0.1,
                "reg_lambda": 0.1,
                "subsample": 0.8
            }
        }
        
        model = self.qlib_research.train_model(model_config)
        
        # Run backtest
        strategy_config = {
            "class": "TopkDropoutStrategy",
            "kwargs": {
                "topk": 50,
                "n_drop": 5,
                "signal": model.predict(),
                "universe": symbols
            }
        }
        
        report = self.qlib_research.run_backtest(model, strategy_config)
        return report
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Calculate max drawdown"""
        cumulative = (1 + prices.pct_change()).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return float(drawdown.min())


def download_qlib_data():
    """Download Qlib data"""
    if not QLIB_AVAILABLE:
        print("Qlib not installed")
        return
    
    try:
        from qlib.data.download import download_data
        
        download_data(
            region="cn",
            download_path=os.path.join(os.path.expanduser("~"), ".qlib", "qlib_data", "cn")
        )
        print("Qlib data downloaded successfully")
    except Exception as e:
        logger.error(f"Failed to download Qlib data: {e}")


if __name__ == "__main__":
    # Example usage
    if QLIB_AVAILABLE:
        research = QlibResearch()
        research.init()
        
        # Get stock list
        stocks = research.get_stock_list(market="csi500")
        print(f"CSI 500 stocks: {len(stocks)}")
        
        # Get price data
        data = research.get_price_data(["SH600519"], "2020-01-01", "2023-01-01")
        print(f"Price data shape: {data.shape}")