import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Optional, List
from loguru import logger


class PerformanceAnalyzer:
    def __init__(self, results: pd.DataFrame):
        self.results = results
        self.metrics = {}
        self._calculate_metrics()

    def _calculate_metrics(self):
        if self.results is None or self.results.empty:
            return
        
        df = self.results.copy()
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        df['returns'] = df['total_assets'].pct_change().dropna()
        df['cumulative_return'] = (1 + df['returns']).cumprod()
        df['rolling_max'] = df['total_assets'].cummax()
        df['drawdown'] = (df['total_assets'] - df['rolling_max']) / df['rolling_max']
        
        total_return = df['cumulative_return'].iloc[-1] - 1
        days = (df.index[-1] - df.index[0]).days
        if days > 0:
            if total_return < -1.0:
                annualized_return = -1.0
            else:
                annualized_return = (1 + total_return) ** (365 / days) - 1
        else:
            annualized_return = 0
        
        volatility = df['returns'].std() * np.sqrt(252)
        sharpe_ratio = (df['returns'].mean() / df['returns'].std()) * np.sqrt(252) if df['returns'].std() > 0 else 0
        
        downside_returns = df['returns'][df['returns'] < 0]
        sortino_ratio = (df['returns'].mean() / downside_returns.std()) * np.sqrt(252) if downside_returns.std() > 0 else 0
        
        max_drawdown = df['drawdown'].min()
        
        winning_days = (df['returns'] > 0).sum()
        total_days = len(df['returns'].dropna())
        win_rate = winning_days / total_days if total_days > 0 else 0
        
        profit_factor = df['returns'][df['returns'] > 0].sum() / abs(df['returns'][df['returns'] < 0].sum()) if df['returns'][df['returns'] < 0].sum() != 0 else float('inf')
        
        self.metrics = {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_days': total_days,
            'winning_days': winning_days,
            'losing_days': total_days - winning_days,
            'avg_daily_return': df['returns'].mean(),
            'std_daily_return': df['returns'].std(),
            'best_day': df['returns'].max(),
            'worst_day': df['returns'].min(),
        }

    def get_metrics(self) -> Dict:
        return self.metrics

    def print_summary(self):
        print("=" * 60)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Total Return:              {self.metrics.get('total_return', 0):.2%}")
        print(f"Annualized Return:         {self.metrics.get('annualized_return', 0):.2%}")
        print(f"Annualized Volatility:     {self.metrics.get('volatility', 0):.2%}")
        print(f"Sharpe Ratio:              {self.metrics.get('sharpe_ratio', 0):.2f}")
        print(f"Sortino Ratio:             {self.metrics.get('sortino_ratio', 0):.2f}")
        print(f"Max Drawdown:              {self.metrics.get('max_drawdown', 0):.2%}")
        print(f"Win Rate:                  {self.metrics.get('win_rate', 0):.2%}")
        print(f"Profit Factor:             {self.metrics.get('profit_factor', 0):.2f}")
        print(f"Total Trading Days:        {self.metrics.get('total_days', 0):,}")
        print(f"Winning Days:              {self.metrics.get('winning_days', 0):,}")
        print(f"Losing Days:               {self.metrics.get('losing_days', 0):,}")
        print(f"Average Daily Return:      {self.metrics.get('avg_daily_return', 0):.2%}")
        print(f"Best Day:                  {self.metrics.get('best_day', 0):.2%}")
        print(f"Worst Day:                 {self.metrics.get('worst_day', 0):.2%}")
        print("=" * 60)

    def plot_equity_curve(self, title: str = 'Equity Curve'):
        if self.results.empty:
            logger.warning("No results to plot")
            return
        
        df = self.results.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_assets'], mode='lines', name='Equity'))
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_assets'].cummax(), mode='lines', name='Peak', line=dict(color='green', dash='dash')))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Portfolio Value',
            template='plotly_dark',
            height=500
        )
        fig.show()

    def plot_drawdown(self, title: str = 'Drawdown'):
        if self.results.empty:
            logger.warning("No results to plot")
            return
        
        df = self.results.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['drawdown'] = (df['total_assets'] - df['total_assets'].cummax()) / df['total_assets'].cummax()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['drawdown'], mode='lines', fill='tozeroy', name='Drawdown'))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Drawdown',
            template='plotly_dark',
            height=400
        )
        fig.show()

    def plot_returns_distribution(self, title: str = 'Daily Returns Distribution'):
        if self.results.empty:
            logger.warning("No results to plot")
            return
        
        df = self.results.copy()
        df['returns'] = df['total_assets'].pct_change().dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df['returns'], nbinsx=50, name='Returns'))
        
        fig.update_layout(
            title=title,
            xaxis_title='Daily Return',
            yaxis_title='Frequency',
            template='plotly_dark',
            height=400
        )
        fig.show()

    def plot_monthly_returns(self, title: str = 'Monthly Returns Heatmap'):
        if self.results.empty:
            logger.warning("No results to plot")
            return
        
        df = self.results.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['returns'] = df['total_assets'].pct_change()
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        
        monthly_returns = df.groupby(['year', 'month'])['returns'].sum().unstack()
        
        fig = go.Figure(data=go.Heatmap(
            z=monthly_returns.values,
            x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y=monthly_returns.index.astype(str),
            colorscale='RdYlGn',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Month',
            yaxis_title='Year',
            template='plotly_dark',
            height=500
        )
        fig.show()

    def generate_full_report(self, save_path: Optional[str] = None):
        self.print_summary()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Equity Curve', 'Drawdown', 'Returns Distribution', 'Performance Metrics'),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        df = self.results.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['returns'] = df['total_assets'].pct_change().dropna()
        df['drawdown'] = (df['total_assets'] - df['total_assets'].cummax()) / df['total_assets'].cummax()
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_assets'], mode='lines', name='Equity'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_assets'].cummax(), mode='lines', name='Peak', line=dict(dash='dash')), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['drawdown'], mode='lines', fill='tozeroy', name='Drawdown'), row=1, col=2)
        
        fig.add_trace(go.Histogram(x=df['returns'], nbinsx=30, name='Returns'), row=2, col=1)
        
        metrics_df = pd.DataFrame(list(self.metrics.items()), columns=['Metric', 'Value'])
        metrics_df['Value'] = metrics_df.apply(
            lambda row: f"{row['Value']:.2%}" if 'return' in row['Metric'].lower() or 'rate' in row['Metric'].lower() or 'drawdown' in row['Metric'].lower() else f"{row['Value']:.2f}",
            axis=1
        )
        fig.add_trace(go.Table(
            header=dict(values=['Metric', 'Value'], fill_color='darkblue'),
            cells=dict(values=[metrics_df['Metric'], metrics_df['Value']], fill_color='darkslategray')
        ), row=2, col=2)
        
        fig.update_layout(
            height=800,
            title_text="Strategy Performance Report",
            template='plotly_dark'
        )
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"Report saved to {save_path}")
        
        fig.show()


class StrategyComparator:
    def __init__(self, results_dict: Dict[str, pd.DataFrame]):
        self.results_dict = results_dict
        self.analyzers = {name: PerformanceAnalyzer(results) for name, results in results_dict.items()}

    def compare_metrics(self) -> pd.DataFrame:
        metrics_list = []
        for name, analyzer in self.analyzers.items():
            metrics = analyzer.get_metrics()
            metrics['strategy'] = name
            metrics_list.append(metrics)
        
        df = pd.DataFrame(metrics_list)
        df.set_index('strategy', inplace=True)
        return df[['total_return', 'annualized_return', 'sharpe_ratio', 'max_drawdown', 'win_rate']]

    def plot_comparison(self):
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Equity Curves', 'Drawdowns'))
        
        for name, analyzer in self.analyzers.items():
            df = analyzer.results.copy()
            df['date'] = pd.to_datetime(df['date'])
            df['drawdown'] = (df['total_assets'] - df['total_assets'].cummax()) / df['total_assets'].cummax()
            
            fig.add_trace(go.Scatter(x=df['date'], y=df['total_assets'], mode='lines', name=name), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['date'], y=df['drawdown'], mode='lines', name=name), row=1, col=2)
        
        fig.update_layout(
            height=500,
            title_text="Strategy Comparison",
            template='plotly_dark'
        )
        fig.show()

    def print_comparison_summary(self):
        comparison_df = self.compare_metrics()
        print("=" * 80)
        print("STRATEGY COMPARISON SUMMARY")
        print("=" * 80)
        print(comparison_df.to_string(formatters={
            'total_return': '{:.2%}'.format,
            'annualized_return': '{:.2%}'.format,
            'sharpe_ratio': '{:.2f}'.format,
            'max_drawdown': '{:.2%}'.format,
            'win_rate': '{:.2%}'.format,
        }))
        print("=" * 80)
