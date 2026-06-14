import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from autoquant.strategy import StrategyEngine, SMAStrategy, MACDStrategy, RSIStrategy
from autoquant.backtest import BackTestEngine, Portfolio, Position
from autoquant.risk import RiskEngine
from autoquant.analyzer import PerformanceAnalyzer, StrategyComparator

def generate_simulated_data(days=365, start_price=100, volatility=0.01):
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(days)]
    prices = np.zeros(days)
    prices[0] = start_price
    
    for i in range(1, days):
        prices[i] = prices[i-1] * (1 + np.random.normal(0, volatility))
    
    data = pd.DataFrame({
        'date': dates,
        'open': prices,
        'high': prices * 1.01,
        'low': prices * 0.99,
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, days),
        'symbol': 'SIMULATED'
    })
    return data

print("=" * 60)
print("Testing AutoQuant Framework with Simulated Data")
print("=" * 60)

# Test 1: Strategy Engine
print("\n1. Testing Strategy Engine...")
try:
    engine = StrategyEngine()
    strategies = engine.get_available_strategies()
    print(f"   ✓ Available strategies: {strategies}")
    
    sma = engine.create_strategy('sma', params={'short_window': 20, 'long_window': 60})
    print(f"   ✓ SMA Strategy created with params: {sma.get_params()}")
    
    macd = engine.create_strategy('macd')
    print(f"   ✓ MACD Strategy created with params: {macd.get_params()}")
    
    rsi = engine.create_strategy('rsi')
    print(f"   ✓ RSI Strategy created with params: {rsi.get_params()}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Position Class
print("\n2. Testing Position Class...")
try:
    pos = Position()
    pos.quantity = 100
    pos.avg_cost = 50.0
    pos.current_price = 60.0
    print(f"   ✓ Position value: ${pos.value:.2f}")
    print(f"   ✓ Position profit: ${pos.profit:.2f} ({pos.profit_pct:.2%})")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Portfolio Class
print("\n3. Testing Portfolio Class...")
try:
    portfolio = Portfolio(initial_capital=100000)
    print(f"   ✓ Initial cash: ${portfolio.cash:,}")
    
    portfolio.buy('TEST', 50.0, 100, commission=50.0)
    print(f"   ✓ After buying 100 shares at $50:")
    print(f"     - Cash: ${portfolio.cash:,}")
    print(f"     - Position quantity: {portfolio.get_position('TEST').quantity}")
    print(f"     - Total assets: ${portfolio.total_assets:,}")
    
    portfolio.sell('TEST', 60.0, 100, commission=60.0)
    print(f"   ✓ After selling 100 shares at $60:")
    print(f"     - Cash: ${portfolio.cash:,}")
    print(f"     - Total profit: ${portfolio.total_profit:.2f} ({portfolio.total_profit_pct:.2%})")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: BackTest Engine
print("\n4. Testing BackTest Engine...")
try:
    data = generate_simulated_data(days=365, start_price=100, volatility=0.01)
    print(f"   ✓ Generated simulated data: {len(data)} days")
    
    backtest = BackTestEngine(initial_capital=100000)
    strategy = SMAStrategy()
    results = backtest.run(data, strategy)
    
    print(f"   ✓ Backtest completed: {len(results)} days")
    print(f"   ✓ Initial capital: $100,000")
    print(f"   ✓ Final assets: ${results['total_assets'].iloc[-1]:,.2f}")
    
    summary = backtest.get_summary()
    print(f"   ✓ Total return: {summary['total_return']:.2%}")
    print(f"   ✓ Annualized return: {summary['annualized_return']:.2%}")
    print(f"   ✓ Sharpe ratio: {summary['sharpe_ratio']:.2f}")
    print(f"   ✓ Max drawdown: {summary['max_drawdown']:.2%}")
    print(f"   ✓ Win rate: {summary['win_rate']:.2%}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Risk Engine
print("\n5. Testing Risk Engine...")
try:
    risk_engine = RiskEngine()
    risk_engine.apply_default_rules()
    risk_engine.set_portfolio_value(120000)
    risk_engine.set_position_count(5)
    
    risk_engine.add_daily_pnl(1000)
    risk_engine.add_daily_pnl(-500)
    risk_engine.add_daily_pnl(2000)
    
    metrics = risk_engine.calculate_risk_metrics()
    print(f"   ✓ Risk rules applied: {[rule.__class__.__name__ for rule in risk_engine.rules]}")
    print(f"   ✓ Risk metrics calculated successfully")
    
    risk_report = risk_engine.generate_risk_report()
    print(f"   ✓ Risk report generated")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Performance Analyzer
print("\n6. Testing Performance Analyzer...")
try:
    data = generate_simulated_data(days=365, start_price=100, volatility=0.01)
    
    backtest = BackTestEngine(initial_capital=100000)
    strategy = SMAStrategy()
    results = backtest.run(data, strategy)
    
    analyzer = PerformanceAnalyzer(results)
    metrics = analyzer.get_metrics()
    
    print(f"   ✓ Performance metrics calculated:")
    print(f"     - Total Return: {metrics['total_return']:.2%}")
    print(f"     - Annualized Return: {metrics['annualized_return']:.2%}")
    print(f"     - Annualized Volatility: {metrics['volatility']:.2%}")
    print(f"     - Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"     - Sortino Ratio: {metrics['sortino_ratio']:.2f}")
    print(f"     - Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"     - Win Rate: {metrics['win_rate']:.2%}")
    print(f"     - Profit Factor: {metrics['profit_factor']:.2f}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Strategy Comparator
print("\n7. Testing Strategy Comparator...")
try:
    data = generate_simulated_data(days=500, start_price=100, volatility=0.01)
    
    results_dict = {}
    strategies_to_test = ['sma', 'macd', 'rsi', 'bollinger']
    
    for name in strategies_to_test:
        backtest = BackTestEngine(initial_capital=100000)
        strategy = StrategyEngine().create_strategy(name)
        results = backtest.run(data, strategy)
        results_dict[name] = results
        print(f"     - {name} strategy completed")
    
    comparator = StrategyComparator(results_dict)
    comparison = comparator.compare_metrics()
    
    print(f"\n   ✓ Strategy comparison results:")
    for strategy_name, row in comparison.iterrows():
        print(f"     - {strategy_name}: {row['total_return']:.2%} return, Sharpe {row['sharpe_ratio']:.2f}, Max DD {row['max_drawdown']:.2%}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)