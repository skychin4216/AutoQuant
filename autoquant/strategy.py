import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from loguru import logger
import talib


class SignalType:
    LONG = 1
    SHORT = -1
    HOLD = 0


class BaseStrategy(ABC):
    def __init__(self, params: Optional[Dict] = None):
        self.params = params or {}
        self.signals = []
        self.position = 0
        self.name = self.__class__.__name__

    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> int:
        pass

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        results = []
        self.position = 0
        
        for idx, row in data.iterrows():
            signal = self.generate_signal(data.iloc[:idx+1])
            self.signals.append(signal)
            
            if signal == SignalType.LONG and self.position <= 0:
                self.position = 1
            elif signal == SignalType.SHORT and self.position >= 0:
                self.position = -1
            elif signal == SignalType.HOLD:
                pass
            
            results.append({
                'date': row['date'],
                'signal': signal,
                'position': self.position,
                'close': row['close'],
                'symbol': row.get('symbol', '')
            })
        
        return pd.DataFrame(results)

    def get_params(self) -> Dict:
        return self.params

    def set_params(self, params: Dict):
        self.params.update(params)


class SMAStrategy(BaseStrategy):
    def __init__(self, params: Optional[Dict] = None):
        default_params = {'short_window': 20, 'long_window': 60}
        default_params.update(params or {})
        super().__init__(default_params)

    def generate_signal(self, data: pd.DataFrame) -> int:
        if len(data) < self.params['long_window']:
            return SignalType.HOLD
        
        short_sma = data['close'].rolling(window=self.params['short_window']).mean().iloc[-1]
        long_sma = data['close'].rolling(window=self.params['long_window']).mean().iloc[-1]
        
        if short_sma > long_sma and self.position <= 0:
            return SignalType.LONG
        elif short_sma < long_sma and self.position >= 0:
            return SignalType.SHORT
        return SignalType.HOLD


class MACDStrategy(BaseStrategy):
    def __init__(self, params: Optional[Dict] = None):
        default_params = {'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9}
        default_params.update(params or {})
        super().__init__(default_params)

    def generate_signal(self, data: pd.DataFrame) -> int:
        if len(data) < self.params['slowperiod'] + self.params['signalperiod']:
            return SignalType.HOLD
        
        macd, signal, _ = talib.MACD(
            data['close'].values,
            fastperiod=self.params['fastperiod'],
            slowperiod=self.params['slowperiod'],
            signalperiod=self.params['signalperiod']
        )
        
        if macd[-1] > signal[-1] and macd[-2] <= signal[-2]:
            return SignalType.LONG
        elif macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
            return SignalType.SHORT
        return SignalType.HOLD


class RSIStrategy(BaseStrategy):
    def __init__(self, params: Optional[Dict] = None):
        default_params = {'period': 14, 'overbought': 70, 'oversold': 30}
        default_params.update(params or {})
        super().__init__(default_params)

    def generate_signal(self, data: pd.DataFrame) -> int:
        if len(data) < self.params['period']:
            return SignalType.HOLD
        
        rsi = talib.RSI(data['close'].values, timeperiod=self.params['period'])
        
        if rsi[-1] < self.params['oversold'] and self.position <= 0:
            return SignalType.LONG
        elif rsi[-1] > self.params['overbought'] and self.position >= 0:
            return SignalType.SHORT
        return SignalType.HOLD


class BollingerBandStrategy(BaseStrategy):
    def __init__(self, params: Optional[Dict] = None):
        default_params = {'period': 20, 'std_dev': 2}
        default_params.update(params or {})
        super().__init__(default_params)

    def generate_signal(self, data: pd.DataFrame) -> int:
        if len(data) < self.params['period']:
            return SignalType.HOLD
        
        sma = data['close'].rolling(window=self.params['period']).mean()
        std = data['close'].rolling(window=self.params['period']).std()
        upper_band = sma + self.params['std_dev'] * std
        lower_band = sma - self.params['std_dev'] * std
        
        if data['close'].iloc[-1] < lower_band.iloc[-1] and self.position <= 0:
            return SignalType.LONG
        elif data['close'].iloc[-1] > upper_band.iloc[-1] and self.position >= 0:
            return SignalType.SHORT
        return SignalType.HOLD


class CrossoverStrategy(BaseStrategy):
    def __init__(self, params: Optional[Dict] = None):
        default_params = {'fast_ema': 12, 'slow_ema': 26}
        default_params.update(params or {})
        super().__init__(default_params)

    def generate_signal(self, data: pd.DataFrame) -> int:
        if len(data) < self.params['slow_ema']:
            return SignalType.HOLD
        
        fast_ema = talib.EMA(data['close'].values, timeperiod=self.params['fast_ema'])
        slow_ema = talib.EMA(data['close'].values, timeperiod=self.params['slow_ema'])
        
        if fast_ema[-1] > slow_ema[-1] and fast_ema[-2] <= slow_ema[-2]:
            return SignalType.LONG
        elif fast_ema[-1] < slow_ema[-1] and fast_ema[-2] >= slow_ema[-2]:
            return SignalType.SHORT
        return SignalType.HOLD


class MultiFactorStrategy(BaseStrategy):
    def __init__(self, params: Optional[Dict] = None):
        default_params = {
            'rsi_period': 14,
            'sma_short': 20,
            'sma_long': 60,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9
        }
        default_params.update(params or {})
        super().__init__(default_params)

    def generate_signal(self, data: pd.DataFrame) -> int:
        if len(data) < max(self.params.values()):
            return SignalType.HOLD
        
        scores = []
        
        rsi = talib.RSI(data['close'].values, timeperiod=self.params['rsi_period'])[-1]
        if rsi < 30:
            scores.append(1)
        elif rsi > 70:
            scores.append(-1)
        
        short_sma = data['close'].rolling(window=self.params['sma_short']).mean().iloc[-1]
        long_sma = data['close'].rolling(window=self.params['sma_long']).mean().iloc[-1]
        if short_sma > long_sma:
            scores.append(1)
        else:
            scores.append(-1)
        
        macd, signal, _ = talib.MACD(
            data['close'].values,
            fastperiod=self.params['macd_fast'],
            slowperiod=self.params['macd_slow'],
            signalperiod=self.params['macd_signal']
        )
        if macd[-1] > signal[-1]:
            scores.append(1)
        else:
            scores.append(-1)
        
        total_score = sum(scores)
        
        if total_score >= 2 and self.position <= 0:
            return SignalType.LONG
        elif total_score <= -2 and self.position >= 0:
            return SignalType.SHORT
        return SignalType.HOLD


class StrategyEngine:
    STRATEGIES = {
        'sma': SMAStrategy,
        'macd': MACDStrategy,
        'rsi': RSIStrategy,
        'bollinger': BollingerBandStrategy,
        'crossover': CrossoverStrategy,
        'multifactor': MultiFactorStrategy,
    }

    def __init__(self):
        self.strategies = {}

    def register_strategy(self, name: str, strategy_class: type):
        if not issubclass(strategy_class, BaseStrategy):
            raise ValueError("Strategy class must inherit from BaseStrategy")
        self.STRATEGIES[name] = strategy_class
        logger.info(f"Registered strategy: {name}")

    def create_strategy(self, name: str, params: Optional[Dict] = None) -> BaseStrategy:
        if name not in self.STRATEGIES:
            raise ValueError(f"Unknown strategy: {name}")
        return self.STRATEGIES[name](params)

    def get_available_strategies(self) -> List[str]:
        return list(self.STRATEGIES.keys())

    def run_strategy(self, strategy_name: str, data: pd.DataFrame, params: Optional[Dict] = None) -> pd.DataFrame:
        strategy = self.create_strategy(strategy_name, params)
        logger.info(f"Running {strategy_name} strategy with params: {strategy.get_params()}")
        return strategy.run(data)

    def run_multiple_strategies(self, strategy_names: List[str], data: pd.DataFrame, params_dict: Optional[Dict[str, Dict]] = None) -> Dict[str, pd.DataFrame]:
        results = {}
        params_dict = params_dict or {}
        
        for name in strategy_names:
            params = params_dict.get(name)
            results[name] = self.run_strategy(name, data, params)
        
        return results
