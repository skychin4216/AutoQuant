import pandas as pd
import numpy as np
import yfinance as yf
import tushare as ts
import akshare as ak
import os
from datetime import datetime, timedelta
from loguru import logger
from typing import Optional, Dict, List, Union
from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def get_price(self, symbol: str, start_date: str, end_date: str, frequency: str = 'D') -> pd.DataFrame:
        pass

    @abstractmethod
    def get_symbols(self, market: str = 'stock') -> List[str]:
        pass


class YahooDataSource(DataSource):
    def get_price(self, symbol: str, start_date: str, end_date: str, frequency: str = 'D') -> pd.DataFrame:
        freq_map = {'D': '1d', 'W': '1wk', 'M': '1mo', '60min': '1h', '30min': '30m', '15min': '15m'}
        interval = freq_map.get(frequency, '1d')
        
        try:
            data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()
            
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            data['symbol'] = symbol
            data['date'] = data.index
            return data.reset_index(drop=True)
        except Exception as e:
            logger.error(f"Error fetching data from Yahoo: {e}")
            return pd.DataFrame()

    def get_symbols(self, market: str = 'stock') -> List[str]:
        return ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']


class TushareDataSource(DataSource):
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('TUSHARE_TOKEN')
        if self.token:
            ts.set_token(self.token)
        self.pro = ts.pro_api()

    def get_price(self, symbol: str, start_date: str, end_date: str, frequency: str = 'D') -> pd.DataFrame:
        freq_map = {'D': 'D', 'W': 'W', 'M': 'M'}
        freq = freq_map.get(frequency, 'D')
        
        try:
            data = self.pro.daily(ts_code=symbol, start_date=start_date, end_date=end_date)
            if data.empty:
                data = self.pro.weekly(ts_code=symbol, start_date=start_date, end_date=end_date) if freq == 'W' else data
                data = self.pro.monthly(ts_code=symbol, start_date=start_date, end_date=end_date) if freq == 'M' else data
            
            if not data.empty:
                data = data[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
                data = data.rename(columns={'vol': 'volume', 'trade_date': 'date'})
                data['date'] = pd.to_datetime(data['date'])
                data['symbol'] = symbol
                return data.sort_values('date').reset_index(drop=True)
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching data from Tushare: {e}")
            return pd.DataFrame()

    def get_symbols(self, market: str = 'stock') -> List[str]:
        try:
            data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code')
            return data['ts_code'].tolist()
        except Exception as e:
            logger.error(f"Error getting symbols from Tushare: {e}")
            return []


class AKShareDataSource(DataSource):
    def get_price(self, symbol: str, start_date: str, end_date: str, frequency: str = 'D') -> pd.DataFrame:
        try:
            freq_map = {'D': 'daily', 'W': 'weekly', 'M': 'monthly'}
            freq = freq_map.get(frequency, 'daily')
            
            data = ak.stock_zh_a_hist(symbol=symbol.split('.')[0], period=freq, start_date=start_date, end_date=end_date)
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()
            
            data = data[['日期', '开盘', '最高', '最低', '收盘', '成交量']]
            data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            data['date'] = pd.to_datetime(data['date'])
            data['symbol'] = symbol
            return data.sort_values('date').reset_index(drop=True)
        except Exception as e:
            logger.error(f"Error fetching data from AKShare: {e}")
            return pd.DataFrame()

    def get_symbols(self, market: str = 'stock') -> List[str]:
        try:
            data = ak.stock_zh_a_spot()
            return data['代码'].tolist()
        except Exception as e:
            logger.error(f"Error getting symbols from AKShare: {e}")
            return []


class CSVDataSource(DataSource):
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir

    def get_price(self, symbol: str, start_date: str, end_date: str, frequency: str = 'D') -> pd.DataFrame:
        try:
            file_path = os.path.join(self.data_dir, f"{symbol}.csv")
            if not os.path.exists(file_path):
                logger.warning(f"CSV file not found: {file_path}")
                return pd.DataFrame()
            
            data = pd.read_csv(file_path)
            data['date'] = pd.to_datetime(data['date'])
            
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            data = data[(data['date'] >= start_dt) & (data['date'] <= end_dt)]
            
            data['symbol'] = symbol
            return data[['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']].reset_index(drop=True)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return pd.DataFrame()

    def get_symbols(self, market: str = 'stock') -> List[str]:
        if not os.path.exists(self.data_dir):
            return []
        return [f.replace('.csv', '') for f in os.listdir(self.data_dir) if f.endswith('.csv')]


class DataFeed:
    def __init__(self, source: str = 'yahoo', **kwargs):
        self.source_map = {
            'yahoo': YahooDataSource,
            'tushare': TushareDataSource,
            'akshare': AKShareDataSource,
            'csv': CSVDataSource,
        }
        self.source = source.lower()
        self.datasource = self._create_datasource(**kwargs)
        logger.info(f"DataFeed initialized with {self.source} source")

    def _create_datasource(self, **kwargs) -> DataSource:
        if self.source not in self.source_map:
            raise ValueError(f"Unsupported data source: {self.source}")
        return self.source_map[self.source](**kwargs)

    def get_price(self, symbol: str, start_date: str, end_date: str, frequency: str = 'D') -> pd.DataFrame:
        return self.datasource.get_price(symbol, start_date, end_date, frequency)

    def get_prices(self, symbols: List[str], start_date: str, end_date: str, frequency: str = 'D') -> Dict[str, pd.DataFrame]:
        result = {}
        for symbol in symbols:
            data = self.get_price(symbol, start_date, end_date, frequency)
            if not data.empty:
                result[symbol] = data
            else:
                logger.warning(f"No data for {symbol}")
        return result

    def get_symbols(self, market: str = 'stock') -> List[str]:
        return self.datasource.get_symbols(market)

    def save_to_csv(self, data: pd.DataFrame, symbol: str, data_dir: str = 'data'):
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f"{symbol}.csv")
        data.to_csv(file_path, index=False)
        logger.info(f"Data saved to {file_path}")

    @staticmethod
    def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        df['volatility'] = df['returns'].rolling(window=20).std() * np.sqrt(252)
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_60'] = df['close'].rolling(window=60).mean()
        df['atr'] = df[['high', 'low', 'close']].apply(
            lambda x: max(x['high'] - x['low'], abs(x['high'] - x['close'].shift(1)), abs(x['low'] - x['close'].shift(1))),
            axis=1
        ).rolling(window=14).mean()
        return df.dropna()
