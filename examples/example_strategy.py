from autoquant import DataFeed, StrategyEngine, BackTestEngine, PerformanceAnalyzer

def run_sma_strategy():
    feed = DataFeed(source='yahoo')
    data = feed.get_price('AAPL', '2020-01-01', '2023-12-31')
    
    engine = BackTestEngine(initial_capital=100000)
    engine.set_commission(0.001)
    engine.set_slippage(0.0005)
    
    strategy_engine = StrategyEngine()
    strategy = strategy_engine.create_strategy('sma', params={'short_window': 20, 'long_window': 60})
    
    results = engine.run(data, strategy)
    
    analyzer = PerformanceAnalyzer(results)
    analyzer.print_summary()
    
    return results, analyzer

def run_multiple_strategies():
    feed = DataFeed(source='yahoo')
    data = feed.get_price('GOOGL', '2020-01-01', '2023-12-31')
    
    strategies = ['sma', 'macd', 'rsi', 'bollinger', 'multifactor']
    results_dict = {}
    
    for name in strategies:
        engine = BackTestEngine(initial_capital=100000)
        strategy = StrategyEngine().create_strategy(name)
        results = engine.run(data, strategy)
        results_dict[name] = results
        
        analyzer = PerformanceAnalyzer(results)
        print(f"\n--- {name.upper()} Strategy Results ---")
        analyzer.print_summary()
    
    return results_dict

if __name__ == '__main__':
    print("=" * 60)
    print("Running SMA Strategy Example")
    print("=" * 60)
    run_sma_strategy()
    
    print("\n" + "=" * 60)
    print("Running Multiple Strategies Comparison")
    print("=" * 60)
    run_multiple_strategies()