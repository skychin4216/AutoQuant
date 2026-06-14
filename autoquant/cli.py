import click
import pandas as pd
from loguru import logger

from .data import DataFeed
from .strategy import StrategyEngine
from .backtest import BackTestEngine
from .risk import RiskEngine
from .analyzer import PerformanceAnalyzer, StrategyComparator


@click.group()
def main():
    """AutoQuant - Advanced Quantitative Trading Framework"""
    pass


@main.command()
@click.option('--source', default='yahoo', help='Data source: yahoo, tushare, akshare, csv')
@click.option('--symbol', default='AAPL', help='Stock symbol')
@click.option('--start-date', default='2020-01-01', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', default='2023-12-31', help='End date (YYYY-MM-DD)')
@click.option('--frequency', default='D', help='Frequency: D, W, M')
@click.option('--output', default=None, help='Output CSV file path')
def fetch_data(source, symbol, start_date, end_date, frequency, output):
    """Fetch historical price data"""
    logger.info(f"Fetching data for {symbol} from {source}")
    feed = DataFeed(source=source)
    data = feed.get_price(symbol, start_date, end_date, frequency)
    
    if not data.empty:
        logger.info(f"Fetched {len(data)} rows")
        print(data.head())
        
        if output:
            feed.save_to_csv(data, symbol, data_dir='data')
            logger.info(f"Data saved to {output}")
    else:
        logger.warning("No data fetched")


@main.command()
@click.option('--strategy', default='sma', help='Strategy name: sma, macd, rsi, bollinger, crossover, multifactor')
@click.option('--symbol', default='AAPL', help='Stock symbol')
@click.option('--start-date', default='2020-01-01', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', default='2023-12-31', help='End date (YYYY-MM-DD)')
@click.option('--capital', default=100000, help='Initial capital')
@click.option('--commission', default=0.001, help='Commission rate')
@click.option('--slippage', default=0.0005, help='Slippage rate')
@click.option('--plot', is_flag=True, help='Plot results')
def backtest(strategy, symbol, start_date, end_date, capital, commission, slippage, plot):
    """Run backtest with specified strategy"""
    logger.info(f"Running backtest: {strategy} on {symbol}")
    
    feed = DataFeed(source='yahoo')
    data = feed.get_price(symbol, start_date, end_date)
    
    if data.empty:
        logger.error("No data available")
        return
    
    engine = BackTestEngine(initial_capital=capital)
    engine.set_commission(commission)
    engine.set_slippage(slippage)
    
    strategy_engine = StrategyEngine()
    strat = strategy_engine.create_strategy(strategy)
    
    results = engine.run(data, strat)
    summary = engine.get_summary()
    
    logger.info("Backtest completed")
    analyzer = PerformanceAnalyzer(results)
    analyzer.print_summary()
    
    if plot:
        analyzer.plot_equity_curve()
        analyzer.plot_drawdown()


@main.command()
@click.option('--symbols', default='AAPL,GOOGL,MSFT', help='Comma-separated stock symbols')
@click.option('--start-date', default='2020-01-01', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', default='2023-12-31', help='End date (YYYY-MM-DD)')
def compare_strategies(symbols, start_date, end_date):
    """Compare multiple strategies"""
    symbols_list = [s.strip() for s in symbols.split(',')]
    
    feed = DataFeed(source='yahoo')
    results_dict = {}
    
    for symbol in symbols_list:
        data = feed.get_price(symbol, start_date, end_date)
        if not data.empty:
            engine = BackTestEngine(initial_capital=100000)
            strat = StrategyEngine().create_strategy('sma')
            results = engine.run(data, strat)
            results_dict[symbol] = results
    
    if results_dict:
        comparator = StrategyComparator(results_dict)
        comparator.print_comparison_summary()
        comparator.plot_comparison()


@main.command()
def list_strategies():
    """List available strategies"""
    engine = StrategyEngine()
    strategies = engine.get_available_strategies()
    print("Available strategies:")
    for strategy in strategies:
        print(f"  - {strategy}")


@main.command()
@click.option('--symbol', default='AAPL', help='Stock symbol')
@click.option('--start-date', default='2020-01-01', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', default='2023-12-31', help='End date (YYYY-MM-DD)')
def risk_analysis(symbol, start_date, end_date):
    """Run risk analysis"""
    feed = DataFeed(source='yahoo')
    data = feed.get_price(symbol, start_date, end_date)
    
    if data.empty:
        logger.error("No data available")
        return
    
    risk_engine = RiskEngine()
    risk_engine.apply_default_rules()
    
    engine = BackTestEngine(initial_capital=100000)
    strat = StrategyEngine().create_strategy('sma')
    results = engine.run(data, strat)
    
    for idx, row in results.iterrows():
        risk_engine.set_portfolio_value(row['total_assets'])
        risk_engine.add_daily_pnl(row['total_assets'] - results.iloc[max(0, idx-1)]['total_assets'] if idx > 0 else 0)
    
    risk_report = risk_engine.generate_risk_report()
    print("Risk Report:")
    print(f"  Portfolio Value: {risk_report['portfolio_value']:.2f}")
    print(f"  Peak Value: {risk_report['peak_value']:.2f}")
    print(f"  Risk Metrics:")
    for metric, value in risk_report['metrics'].items():
        print(f"    {metric}: {value:.4f}")


if __name__ == '__main__':
    main()