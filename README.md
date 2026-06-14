# AutoQuant

Advanced Quantitative Trading Framework with AI-Powered GUI.

## Features

- **🤖 AI Assistant**: Intelligent chatbot for strategy creation and optimization
- **🖥️ Modern GUI**: PyQt5-based desktop application with dark theme
- **📊 Data Visualization**: Real-time equity curves and drawdown charts
- **Multi-Data Source Support**: Yahoo Finance, Tushare, AKShare, CSV files
- **Strategy Engine**: SMA, MACD, RSI, Bollinger Bands, Multi-Factor strategies
- **Backtesting**: Full event-driven backtesting with commission and slippage
- **Risk Management**: Position limits, drawdown control, diversification rules
- **Performance Analysis**: Sharpe ratio, Sortino ratio, max drawdown, win rate, etc.
- **CLI Interface**: Easy command-line access to all features
- **📦 One-Click Packaging**: Build standalone executable for Windows

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

## Quick Start

### Using GUI Application

```bash
# Run the GUI application
python run_gui.py
```

The GUI includes:
- **AI Assistant Tab**: Chat with AI to create strategies, optimize parameters
- **Backtest Results Tab**: View performance metrics and charts
- **Strategy List Tab**: Manage and compare strategies

### Using CLI

```bash
# Fetch data
autoquant fetch-data --symbol AAPL --start-date 2020-01-01 --end-date 2023-12-31

# Run backtest
autoquant backtest --strategy sma --symbol AAPL --capital 100000

# Compare strategies
autoquant compare-strategies --symbols AAPL,GOOGL,MSFT

# List available strategies
autoquant list-strategies
```

### Using Python API

```python
from autoquant import DataFeed, StrategyEngine, BackTestEngine, PerformanceAnalyzer

# Fetch data
feed = DataFeed(source='yahoo')
data = feed.get_price('AAPL', '2020-01-01', '2023-12-31')

# Run backtest
engine = BackTestEngine(initial_capital=100000)
strategy = StrategyEngine().create_strategy('sma')
results = engine.run(data, strategy)

# Analyze results
analyzer = PerformanceAnalyzer(results)
analyzer.print_summary()
analyzer.plot_equity_curve()
```

## Project Structure

```
autoquant/
├── __init__.py          # Module exports
├── data.py              # DataFeed and data sources
├── strategy.py          # Strategy engine and strategy implementations
├── backtest.py          # Backtesting engine
├── risk.py              # Risk management engine
├── analyzer.py          # Performance analysis
└── cli.py               # Command-line interface

examples/
└── example_strategy.py  # Example usage

tests/
└── test_backtest.py     # Unit tests

requirements.txt         # Dependencies
setup.py                 # Package setup
```

## Available Strategies

| Strategy | Description | Parameters |
|----------|-------------|------------|
| `sma` | Simple Moving Average Crossover | short_window, long_window |
| `macd` | MACD Indicator | fastperiod, slowperiod, signalperiod |
| `rsi` | RSI Overbought/Oversold | period, overbought, oversold |
| `bollinger` | Bollinger Bands | period, std_dev |
| `crossover` | EMA Crossover | fast_ema, slow_ema |
| `multifactor` | Multi-Factor Combination | rsi_period, sma_short, sma_long, macd_fast, macd_slow, macd_signal |

## Performance Metrics

- Total Return
- Annualized Return
- Annualized Volatility
- Sharpe Ratio
- Sortino Ratio
- Max Drawdown
- Win Rate
- Profit Factor

## Risk Rules

- Max Position Size (10% of portfolio)
- Max Drawdown (20%)
- Max Position Count (10 positions)
- Diversification (minimum 5 assets)
- Volatility Limit (40%)

## License

MIT License

## Contributing

Contributions are welcome! Please submit a pull request or open an issue.

## Building Executable

To build a standalone Windows executable:

```bash
# Run the build script
build_exe.bat

# Or manually
pyinstaller AutoQuant.spec --clean
```

The executable will be created in `dist/AutoQuant.exe`.

## vn.py Integration

vn.py is a professional quantitative trading framework for live trading.

### Features
- CTP gateway support for futures trading
- CTA strategy engine
- Real-time position and account management

### Quick Start

```bash
# Run vn.py standalone
python run_vnpy.py

# Or use in code
from autoquant import VnpyTrader, VnpyConfig

trader = VnpyTrader()
config = VnpyConfig(
    username="your_username",
    password="your_password",
    broker_id="9999",
    td_address="tcp://180.168.146.187:10001",
    md_address="tcp://180.168.146.187:10002"
)
trader.init(config)
trader.connect(config)
trader.start_gui()
```

## Qlib (RD-Agent) Integration

Qlib is an AI-powered quantitative research framework from Microsoft.

### Features
- Alpha158 factor library
- ML model training and prediction
- Factor analysis and backtesting
- RD-Agent research assistant

### Quick Start

```bash
# Run Qlib standalone
python run_qlib.py

# Or use in code
from autoquant import QlibResearch, RDAGentResearch

# Initialize
research = QlibResearch()
research.init()

# Get stock list
stocks = research.get_stock_list(market="csi500")

# Get factor data
factors = research.get_alpha_factors(["SH600519"], "2020-01-01", "2023-01-01")

# Run strategy research
rd_agent = RDAGentResearch()
report = rd_agent.strategy_research(stocks[:10], "2020-01-01", "2023-01-01")
```

### Download Qlib Data

```bash
python -c "from autoquant import download_qlib_data; download_qlib_data()"
```

## AI Configuration

To use AI features with OpenAI or Anthropic:

```bash
# Set API key (OpenAI)
export OPENAI_API_KEY=your_api_key

# Or set in the application settings
```

Without API keys, the AI assistant operates in local mode with simulated responses.
