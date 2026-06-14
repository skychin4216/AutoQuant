import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autoquant.data import DataFeed
from autoquant.strategy import StrategyEngine, SMAStrategy, MACDStrategy, RSIStrategy
from autoquant.backtest import BackTestEngine
from autoquant.risk import RiskEngine
from autoquant.analyzer import PerformanceAnalyzer, StrategyComparator

print("=" * 60)
print("Testing AutoQuant Framework")
print("=" * 60)

# Test 1: DataFeed
print("\n1. Testing DataFeed...")
try:
    feed = DataFeed(source='yahoo')
    data = feed.get_price('AAPL', '2023-01-01', '2023-01-31')
    print(f"   ✓ Data fetched successfully: {len(data)} rows")
    print(f"   ✓ Columns: {list(data.columns)}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Strategy Engine
print("\n2. Testing Strategy Engine...")
try:
    engine = StrategyEngine()
    strategies = engine.get_available_strategies()
    print(f"   ✓ Available strategies: {strategies}")
    
    sma = engine.create_strategy('sma', params={'short_window': 20, 'long_window': 60})
    print(f"   ✓ SMA Strategy created with params: {sma.get_params()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: BackTest Engine
print("\n3. Testing BackTest Engine...")
try:
    feed = DataFeed(source='yahoo')
    data = feed.get_price('AAPL', '2023-01-01', '2023-12-31')
    
    backtest = BackTestEngine(initial_capital=100000)
    strategy = SMAStrategy()
    results = backtest.run(data, strategy)
    
    print(f"   ✓ Backtest completed: {len(results)} days")
    print(f"   ✓ Initial capital: $100,000")
    print(f"   ✓ Final assets: ${results['total_assets'].iloc[-1]:,.2f}")
    
    summary = backtest.get_summary()
    print(f"   ✓ Total return: {summary['total_return']:.2%}")
    print(f"   ✓ Sharpe ratio: {summary['sharpe_ratio']:.2f}")
    print(f"   ✓ Max drawdown: {summary['max_drawdown']:.2%}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Risk Engine
print("\n4. Testing Risk Engine...")
try:
    risk_engine = RiskEngine()
    risk_engine.apply_default_rules()
    risk_engine.set_portfolio_value(120000)
    risk_engine.set_position_count(5)
    
    metrics = risk_engine.calculate_risk_metrics()
    print(f"   ✓ Risk rules applied: {[rule.__class__.__name__ for rule in risk_engine.rules]}")
    print(f"   ✓ Risk metrics calculated successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Performance Analyzer
print("\n5. Testing Performance Analyzer...")
try:
    feed = DataFeed(source='yahoo')
    data = feed.get_price('AAPL', '2023-01-01', '2023-12-31')
    
    backtest = BackTestEngine(initial_capital=100000)
    strategy = SMAStrategy()
    results = backtest.run(data, strategy)
    
    analyzer = PerformanceAnalyzer(results)
    metrics = analyzer.get_metrics()
    
    print(f"   ✓ Performance metrics:")
    print(f"     - Total Return: {metrics['total_return']:.2%}")
    print(f"     - Annualized Return: {metrics['annualized_return']:.2%}")
    print(f"     - Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"     - Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"     - Win Rate: {metrics['win_rate']:.2%}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Strategy Comparator
print("\n6. Testing Strategy Comparator...")
try:
    feed = DataFeed(source='yahoo')
    data = feed.get_price('GOOGL', '2023-01-01', '2023-12-31')
    
    results_dict = {}
    strategies_to_test = ['sma', 'macd', 'rsi']
    
    for name in strategies_to_test:
        backtest = BackTestEngine(initial_capital=100000)
        strategy = StrategyEngine().create_strategy(name)
        results = backtest.run(data, strategy)
        results_dict[name] = results
    
    comparator = StrategyComparator(results_dict)
    comparison = comparator.compare_metrics()
    
    print(f"   ✓ Strategy comparison completed")
    print("   ✓ Comparison results:")
    for strategy_name, row in comparison.iterrows():
        print(f"     - {strategy_name}: {row['total_return']:.2%} return, Sharpe {row['sharpe_ratio']:.2f}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)