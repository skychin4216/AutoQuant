import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from loguru import logger
from .strategy import BaseStrategy, StrategyEngine, SignalType


class Position:
    def __init__(self):
        self.quantity = 0
        self.avg_cost = 0.0
        self.current_price = 0.0

    @property
    def value(self):
        return self.quantity * self.current_price

    @property
    def profit(self):
        if self.quantity == 0:
            return 0.0
        return (self.current_price - self.avg_cost) * self.quantity

    @property
    def profit_pct(self):
        if self.avg_cost == 0:
            return 0.0
        return (self.current_price - self.avg_cost) / self.avg_cost


class Portfolio:
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.history = []

    def get_position(self, symbol: str) -> Position:
        if symbol not in self.positions:
            self.positions[symbol] = Position()
        return self.positions[symbol]

    def update_price(self, symbol: str, price: float):
        if symbol in self.positions:
            self.positions[symbol].current_price = price

    def buy(self, symbol: str, price: float, quantity: int, commission: float = 0.0):
        cost = price * quantity + commission
        if cost > self.cash:
            logger.warning(f"Insufficient cash to buy {quantity} shares of {symbol}")
            return False
        
        self.cash -= cost
        position = self.get_position(symbol)
        
        if position.quantity == 0:
            position.avg_cost = price
        else:
            position.avg_cost = (position.avg_cost * position.quantity + price * quantity) / (position.quantity + quantity)
        
        position.quantity += quantity
        position.current_price = price
        return True

    def sell(self, symbol: str, price: float, quantity: int, commission: float = 0.0):
        position = self.get_position(symbol)
        if quantity > position.quantity:
            logger.warning(f"Insufficient shares to sell {quantity} of {symbol}")
            return False
        
        revenue = price * quantity - commission
        self.cash += revenue
        position.quantity -= quantity
        
        if position.quantity == 0:
            position.avg_cost = 0.0
        
        return True

    @property
    def total_assets(self):
        positions_value = sum(pos.value for pos in self.positions.values())
        return self.cash + positions_value

    @property
    def total_profit(self):
        return self.total_assets - self.initial_capital

    @property
    def total_profit_pct(self):
        if self.initial_capital == 0:
            return 0.0
        return self.total_profit / self.initial_capital

    def record(self, date):
        self.history.append({
            'date': date,
            'cash': self.cash,
            'total_assets': self.total_assets,
            'total_profit': self.total_profit,
            'total_profit_pct': self.total_profit_pct,
        })

    def get_history(self) -> pd.DataFrame:
        return pd.DataFrame(self.history)


class BackTestEngine:
    def __init__(self, initial_capital: float = 100000.0):
        self.portfolio = Portfolio(initial_capital)
        self.strategy_engine = StrategyEngine()
        self.results = None
        self.commission_rate = 0.001
        self.slippage_rate = 0.0005

    def set_commission(self, rate: float):
        self.commission_rate = rate

    def set_slippage(self, rate: float):
        self.slippage_rate = rate

    def _calculate_price_with_slippage(self, price: float, signal: int) -> float:
        if signal == SignalType.LONG:
            return price * (1 + self.slippage_rate)
        elif signal == SignalType.SHORT:
            return price * (1 - self.slippage_rate)
        return price

    def run(self, data: pd.DataFrame, strategy: BaseStrategy) -> pd.DataFrame:
        logger.info(f"Starting backtest with strategy: {strategy.name}")
        logger.info(f"Initial capital: {self.portfolio.initial_capital}")
        
        symbol = data['symbol'].iloc[0] if 'symbol' in data.columns else 'UNKNOWN'
        
        for idx, row in data.iterrows():
            date = row['date']
            close_price = row['close']
            
            self.portfolio.update_price(symbol, close_price)
            
            signal = strategy.generate_signal(data.iloc[:idx+1])
            price_with_slippage = self._calculate_price_with_slippage(close_price, signal)
            
            if signal == SignalType.LONG:
                position = self.portfolio.get_position(symbol)
                if position.quantity <= 0:
                    if position.quantity < 0:
                        self.cover_short(symbol, price_with_slippage)
                    self.go_long(symbol, price_with_slippage)
            
            elif signal == SignalType.SHORT:
                position = self.portfolio.get_position(symbol)
                if position.quantity >= 0:
                    if position.quantity > 0:
                        self.sell_long(symbol, price_with_slippage)
                    self.go_short(symbol, price_with_slippage)
            
            self.portfolio.record(date)
        
        self.results = self.portfolio.get_history()
        logger.info(f"Backtest completed. Final assets: {self.portfolio.total_assets:.2f}")
        logger.info(f"Total profit: {self.portfolio.total_profit:.2f} ({self.portfolio.total_profit_pct:.2%})")
        
        return self.results

    def go_long(self, symbol: str, price: float):
        max_quantity = int(self.portfolio.cash / (price * (1 + self.commission_rate)))
        if max_quantity > 0:
            commission = price * max_quantity * self.commission_rate
            self.portfolio.buy(symbol, price, max_quantity, commission)
            logger.debug(f"BUY {max_quantity} shares of {symbol} at {price:.2f}")

    def sell_long(self, symbol: str, price: float):
        position = self.portfolio.get_position(symbol)
        if position.quantity > 0:
            commission = price * position.quantity * self.commission_rate
            self.portfolio.sell(symbol, price, position.quantity, commission)
            logger.debug(f"SELL {position.quantity} shares of {symbol} at {price:.2f}")

    def go_short(self, symbol: str, price: float):
        max_quantity = int(self.portfolio.cash / (price * (1 + self.commission_rate)))
        if max_quantity > 0:
            commission = price * max_quantity * self.commission_rate
            revenue = price * max_quantity - commission
            self.portfolio.cash += revenue
            position = self.portfolio.get_position(symbol)
            position.quantity -= max_quantity
            position.avg_cost = price
            position.current_price = price
            logger.debug(f"SHORT {max_quantity} shares of {symbol} at {price:.2f}")

    def cover_short(self, symbol: str, price: float):
        position = self.portfolio.get_position(symbol)
        if position.quantity < 0:
            quantity = -position.quantity
            commission = price * quantity * self.commission_rate
            cost = price * quantity + commission
            self.portfolio.cash -= cost
            position.quantity = 0
            position.avg_cost = 0.0
            logger.debug(f"COVER {quantity} shares of {symbol} at {price:.2f}")

    def run_multiple_strategies(self, data: pd.DataFrame, strategy_names: list) -> Dict[str, pd.DataFrame]:
        results = {}
        for name in strategy_names:
            strategy = self.strategy_engine.create_strategy(name)
            self.portfolio = Portfolio(self.portfolio.initial_capital)
            results[name] = self.run(data, strategy)
        return results

    def get_summary(self) -> Dict:
        if self.results is None:
            return {}
        
        returns = self.results['total_profit_pct'].pct_change().dropna()
        
        summary = {
            'initial_capital': self.portfolio.initial_capital,
            'final_assets': self.portfolio.total_assets,
            'total_profit': self.portfolio.total_profit,
            'total_return': self.portfolio.total_profit_pct,
            'annualized_return': self._calculate_annualized_return(),
            'max_drawdown': self._calculate_max_drawdown(),
            'sharpe_ratio': self._calculate_sharpe_ratio(returns),
            'sortino_ratio': self._calculate_sortino_ratio(returns),
            'win_rate': self._calculate_win_rate(),
            'profit_factor': self._calculate_profit_factor(),
            'total_trades': self._calculate_total_trades(),
        }
        
        return summary

    def _calculate_annualized_return(self) -> float:
        if self.results is None or len(self.results) < 2:
            return 0.0
        
        days = (self.results['date'].iloc[-1] - self.results['date'].iloc[0]).days
        if days == 0:
            return 0.0
        
        total_return = self.portfolio.total_profit_pct
        if total_return < -1.0:
            return -1.0
        return (1 + total_return) ** (365 / days) - 1

    def _calculate_max_drawdown(self) -> float:
        if self.results is None:
            return 0.0
        
        equity_curve = self.results['total_assets']
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        return drawdown.min()

    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        if returns.empty:
            return 0.0
        
        excess_returns = returns - risk_free_rate / 252
        return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

    def _calculate_sortino_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        if returns.empty:
            return 0.0
        
        excess_returns = returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]
        if downside_returns.empty:
            return 0.0
        
        downside_std = downside_returns.std()
        return excess_returns.mean() / downside_std * np.sqrt(252)

    def _calculate_win_rate(self) -> float:
        if self.results is None:
            return 0.0
        
        returns = self.results['total_profit_pct'].dropna()
        if len(returns) == 0:
            return 0.0
        
        winning_days = (returns > 0).sum()
        return winning_days / len(returns)

    def _calculate_profit_factor(self) -> float:
        if self.results is None:
            return 0.0
        
        returns = self.results['total_profit_pct'].dropna()
        if len(returns) == 0:
            return 0.0
        
        gross_profit = returns[returns > 0].sum()
        gross_loss = abs(returns[returns < 0].sum())
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
        
        return gross_profit / gross_loss

    def _calculate_total_trades(self) -> int:
        if self.results is None:
            return 0
        
        positions = self.results['total_assets'].diff().fillna(0)
        trades = positions[positions != 0].count()
        return int(trades / 2)
