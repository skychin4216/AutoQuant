import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from autoquant.data import DataFeed
from autoquant.strategy import SMAStrategy, MACDStrategy
from autoquant.backtest import BackTestEngine, Portfolio, Position


class TestPosition:
    def test_position_initialization(self):
        pos = Position()
        assert pos.quantity == 0
        assert pos.avg_cost == 0.0
        assert pos.value == 0.0

    def test_position_value(self):
        pos = Position()
        pos.quantity = 100
        pos.current_price = 50.0
        assert pos.value == 5000.0

    def test_position_profit(self):
        pos = Position()
        pos.quantity = 100
        pos.avg_cost = 40.0
        pos.current_price = 50.0
        assert pos.profit == 1000.0
        assert pos.profit_pct == 0.25


class TestPortfolio:
    def test_portfolio_initialization(self):
        portfolio = Portfolio(initial_capital=100000)
        assert portfolio.cash == 100000
        assert portfolio.total_assets == 100000

    def test_portfolio_buy(self):
        portfolio = Portfolio(initial_capital=100000)
        result = portfolio.buy('AAPL', 50.0, 100, commission=50.0)
        assert result is True
        assert portfolio.cash == 100000 - 50*100 - 50
        assert portfolio.get_position('AAPL').quantity == 100

    def test_portfolio_sell(self):
        portfolio = Portfolio(initial_capital=100000)
        portfolio.buy('AAPL', 50.0, 100, commission=50.0)
        result = portfolio.sell('AAPL', 60.0, 100, commission=60.0)
        assert result is True
        assert portfolio.get_position('AAPL').quantity == 0


class TestBackTestEngine:
    def create_test_data(self, days=100):
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(days)]
        prices = np.linspace(50, 60, days)
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices,
            'volume': 1000000,
            'symbol': 'TEST'
        })
        return data

    def test_backtest_run(self):
        data = self.create_test_data(days=100)
        engine = BackTestEngine(initial_capital=100000)
        strategy = SMAStrategy(params={'short_window': 10, 'long_window': 20})
        
        results = engine.run(data, strategy)
        
        assert not results.empty
        assert 'total_assets' in results.columns
        assert len(results) == len(data)

    def test_backtest_summary(self):
        data = self.create_test_data(days=100)
        engine = BackTestEngine(initial_capital=100000)
        strategy = SMAStrategy()
        
        engine.run(data, strategy)
        summary = engine.get_summary()
        
        assert 'total_return' in summary
        assert 'sharpe_ratio' in summary
        assert 'max_drawdown' in summary

    def test_multiple_strategies(self):
        data = self.create_test_data(days=100)
        engine = BackTestEngine(initial_capital=100000)
        
        results = engine.run_multiple_strategies(data, ['sma', 'macd'])
        
        assert 'sma' in results
        assert 'macd' in results
        assert not results['sma'].empty


class TestDataFeed:
    def test_yahoo_data_source(self):
        feed = DataFeed(source='yahoo')
        data = feed.get_price('AAPL', '2023-01-01', '2023-01-10')
        
        assert 'open' in data.columns
        assert 'close' in data.columns
        assert 'volume' in data.columns

    def test_preprocess_data(self):
        feed = DataFeed(source='yahoo')
        data = feed.get_price('AAPL', '2023-01-01', '2023-02-01')
        
        processed = feed.preprocess_data(data)
        
        assert 'returns' in processed.columns
        assert 'sma_20' in processed.columns
        assert 'atr' in processed.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])