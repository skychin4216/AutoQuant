import pandas as pd
import numpy as np
from typing import Dict, Optional, List, Tuple
from loguru import logger
from abc import ABC, abstractmethod


class RiskRule(ABC):
    def __init__(self, params: Optional[Dict] = None):
        self.params = params or {}
        self.violations = []

    @abstractmethod
    def check(self, portfolio_value: float, position_value: float, position_count: int, **kwargs) -> bool:
        pass

    def record_violation(self, reason: str):
        self.violations.append(reason)

    def get_violations(self) -> List[str]:
        return self.violations


class MaxPositionRule(RiskRule):
    def __init__(self, max_position_pct: float = 0.1):
        super().__init__({'max_position_pct': max_position_pct})

    def check(self, portfolio_value: float, position_value: float, **kwargs) -> bool:
        if portfolio_value == 0:
            return True
        
        position_pct = position_value / portfolio_value
        if position_pct > self.params['max_position_pct']:
            self.record_violation(f"Position exceeds {self.params['max_position_pct']*100}% of portfolio")
            return False
        return True


class MaxDrawdownRule(RiskRule):
    def __init__(self, max_drawdown: float = 0.2):
        super().__init__({'max_drawdown': max_drawdown})

    def check(self, portfolio_value: float, peak_value: float, **kwargs) -> bool:
        if peak_value == 0:
            return True
        
        drawdown = (peak_value - portfolio_value) / peak_value
        if drawdown > self.params['max_drawdown']:
            self.record_violation(f"Drawdown exceeds {self.params['max_drawdown']*100}%")
            return False
        return True


class MaxPositionCountRule(RiskRule):
    def __init__(self, max_positions: int = 10):
        super().__init__({'max_positions': max_positions})

    def check(self, position_count: int, **kwargs) -> bool:
        if position_count > self.params['max_positions']:
            self.record_violation(f"Position count exceeds {self.params['max_positions']}")
            return False
        return True


class DiversificationRule(RiskRule):
    def __init__(self, min_assets: int = 5, max_concentration: float = 0.3):
        super().__init__({'min_assets': min_assets, 'max_concentration': max_concentration})

    def check(self, position_count: int, weights: Optional[List[float]] = None, **kwargs) -> bool:
        if position_count < self.params['min_assets']:
            self.record_violation(f"Insufficient diversification: only {position_count} assets")
            return False
        
        if weights:
            max_weight = max(weights)
            if max_weight > self.params['max_concentration']:
                self.record_violation(f"Concentration exceeds {self.params['max_concentration']*100}%")
                return False
        
        return True


class VolatilityRule(RiskRule):
    def __init__(self, max_volatility: float = 0.4):
        super().__init__({'max_volatility': max_volatility})

    def check(self, volatility: float, **kwargs) -> bool:
        if volatility > self.params['max_volatility']:
            self.record_violation(f"Volatility exceeds {self.params['max_volatility']*100}%")
            return False
        return True


class SectorLimitRule(RiskRule):
    def __init__(self, sector_limits: Optional[Dict[str, float]] = None):
        super().__init__({'sector_limits': sector_limits or {}})

    def check(self, sector_weights: Optional[Dict[str, float]] = None, **kwargs) -> bool:
        if not sector_weights:
            return True
        
        for sector, weight in sector_weights.items():
            limit = self.params['sector_limits'].get(sector, 0.3)
            if weight > limit:
                self.record_violation(f"{sector} sector exceeds {limit*100}% limit")
                return False
        
        return True


class LiquidityRule(RiskRule):
    def __init__(self, min_volume: int = 1000000, max_slippage: float = 0.01):
        super().__init__({'min_volume': min_volume, 'max_slippage': max_slippage})

    def check(self, volume: float = 0, slippage: float = 0, **kwargs) -> bool:
        if volume < self.params['min_volume']:
            self.record_violation(f"Volume {volume} below minimum {self.params['min_volume']}")
            return False
        
        if slippage > self.params['max_slippage']:
            self.record_violation(f"Slippage {slippage*100}% exceeds {self.params['max_slippage']*100}%")
            return False
        
        return True


class RiskEngine:
    def __init__(self):
        self.rules: List[RiskRule] = []
        self.portfolio_value = 0.0
        self.peak_value = 0.0
        self.position_count = 0
        self.daily_pnl = []

    def add_rule(self, rule: RiskRule):
        self.rules.append(rule)
        logger.info(f"Added risk rule: {rule.__class__.__name__}")

    def remove_rule(self, rule_type: type):
        self.rules = [r for r in self.rules if not isinstance(r, rule_type)]

    def set_portfolio_value(self, value: float):
        self.portfolio_value = value
        if value > self.peak_value:
            self.peak_value = value

    def set_position_count(self, count: int):
        self.position_count = count

    def add_daily_pnl(self, pnl: float):
        self.daily_pnl.append(pnl)

    def check_all_rules(self, **kwargs) -> Tuple[bool, List[str]]:
        violations = []
        all_passed = True
        
        for rule in self.rules:
            result = rule.check(
                portfolio_value=self.portfolio_value,
                position_count=self.position_count,
                peak_value=self.peak_value,
                **kwargs
            )
            if not result:
                violations.extend(rule.get_violations())
                all_passed = False
        
        return all_passed, violations

    def check_trade(self, trade_value: float, **kwargs) -> Tuple[bool, List[str]]:
        temp_value = self.portfolio_value + trade_value
        temp_count = self.position_count + 1
        
        violations = []
        all_passed = True
        
        for rule in self.rules:
            result = rule.check(
                portfolio_value=temp_value,
                position_value=trade_value,
                position_count=temp_count,
                peak_value=self.peak_value,
                **kwargs
            )
            if not result:
                violations.extend(rule.get_violations())
                all_passed = False
        
        return all_passed, violations

    def calculate_risk_metrics(self) -> Dict[str, float]:
        if not self.daily_pnl:
            return {}
        
        pnl_series = pd.Series(self.daily_pnl)
        
        var_95 = -np.percentile(pnl_series, 5)
        
        metrics = {
            'daily_volatility': pnl_series.std() * np.sqrt(252),
            'var_95': var_95,
            'cvar_95': -pnl_series[pnl_series <= -var_95].mean(),
            'max_drawdown': self._calculate_max_drawdown(),
            'sharpe_ratio': self._calculate_sharpe_ratio(pnl_series),
            'sortino_ratio': self._calculate_sortino_ratio(pnl_series),
        }
        
        return metrics

    def _calculate_max_drawdown(self) -> float:
        if not self.daily_pnl:
            return 0.0
        
        equity = np.cumsum(self.daily_pnl)
        peak = np.maximum.accumulate(equity)
        drawdown = (peak - equity) / peak
        return drawdown.max() if len(drawdown) > 0 else 0.0

    def _calculate_sharpe_ratio(self, pnl_series: pd.Series, risk_free_rate: float = 0.02) -> float:
        returns = pnl_series / self.portfolio_value if self.portfolio_value > 0 else pnl_series
        excess_returns = returns - risk_free_rate / 252
        return excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() > 0 else 0.0

    def _calculate_sortino_ratio(self, pnl_series: pd.Series, risk_free_rate: float = 0.02) -> float:
        returns = pnl_series / self.portfolio_value if self.portfolio_value > 0 else pnl_series
        excess_returns = returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]
        downside_std = downside_returns.std()
        return excess_returns.mean() / downside_std * np.sqrt(252) if downside_std > 0 else 0.0

    def generate_risk_report(self) -> Dict:
        report = {
            'risk_rules': [rule.__class__.__name__ for rule in self.rules],
            'violations': [],
            'metrics': self.calculate_risk_metrics(),
            'portfolio_value': self.portfolio_value,
            'peak_value': self.peak_value,
            'position_count': self.position_count,
        }
        
        for rule in self.rules:
            report['violations'].extend(rule.get_violations())
        
        return report

    def apply_default_rules(self):
        self.add_rule(MaxPositionRule(max_position_pct=0.1))
        self.add_rule(MaxDrawdownRule(max_drawdown=0.2))
        self.add_rule(MaxPositionCountRule(max_positions=10))
        self.add_rule(DiversificationRule(min_assets=5, max_concentration=0.3))
        self.add_rule(VolatilityRule(max_volatility=0.4))
        logger.info("Applied default risk rules")
