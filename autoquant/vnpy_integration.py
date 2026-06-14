"""
vn.py Integration Module
Provides access to vn.py trading framework for live trading
"""

import sys
import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

try:
    from vnpy.event import EventEngine
    from vnpy.trader.engine import MainEngine
    from vnpy.trader.ui import MainWindow, create_qapp
    from vnpy.gateway import ctp
    VNPY_AVAILABLE = True
except ImportError:
    VNPY_AVAILABLE = False
    logger.warning("vn.py not installed, live trading features disabled")


@dataclass
class VnpyConfig:
    """vn.py Configuration"""
    gateway_name: str = "ctp"
    gateway_module: str = "vnpy_ctp"
    username: str = ""
    password: str = ""
    broker_id: str = ""
    td_address: str = ""
    md_address: str = ""
    product: str = "simnow"


class VnpyTrader:
    """vn.py Trading Interface"""
    
    def __init__(self):
        if not VNPY_AVAILABLE:
            raise ImportError("vn.py not installed")
        
        self.event_engine = None
        self.main_engine = None
        self.main_window = None
        self.app = None
    
    def init(self, config: VnpyConfig):
        """Initialize vn.py engine"""
        self.app = create_qapp()
        self.event_engine = EventEngine()
        self.main_engine = MainEngine(self.event_engine)
        
        # Add CTP gateway
        try:
            self.main_engine.add_gateway(ctp.CtpGateway)
            logger.info("CTP gateway added successfully")
        except Exception as e:
            logger.error(f"Failed to add CTP gateway: {e}")
        
        # Add apps
        self.main_engine.add_app("cta")
        self.main_engine.add_app("portfolio")
        logger.info("vn.py initialized successfully")
    
    def connect(self, config: VnpyConfig):
        """Connect to trading gateway"""
        if not self.main_engine:
            self.init(config)
        
        setting = {
            "username": config.username,
            "password": config.password,
            "brokerid": config.broker_id,
            "tdaddress": config.td_address,
            "mdaddress": config.md_address,
            "product": config.product,
            "auth_code": "",
            "appid": ""
        }
        
        try:
            self.main_engine.connect(setting, "CTP")
            logger.info("Connected to CTP gateway")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def start_gui(self):
        """Start vn.py GUI"""
        if not self.main_engine:
            raise RuntimeError("vn.py not initialized")
        
        self.main_window = MainWindow(self.main_engine, self.event_engine)
        self.main_window.showMaximized()
        self.app.exec()
    
    def get_account_balance(self) -> Optional[Dict[str, float]]:
        """Get account balance"""
        if not self.main_engine:
            return None
        
        accounts = self.main_engine.get_all_accounts()
        if accounts:
            return {acc.accountid: float(acc.balance) for acc in accounts}
        return None
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions"""
        if not self.main_engine:
            return []
        
        positions = self.main_engine.get_all_positions()
        result = []
        for pos in positions:
            result.append({
                "symbol": pos.symbol,
                "direction": pos.direction.value,
                "quantity": pos.volume,
                "avg_cost": pos.price,
                "current_price": pos.last_price,
                "pnl": pos.pnl
            })
        return result
    
    def send_order(self, symbol: str, direction: str, price: float, 
                   volume: int, order_type: str = "limit") -> str:
        """Send trading order"""
        if not self.main_engine:
            raise RuntimeError("vn.py not initialized")
        
        from vnpy.trader.constant import Direction, OrderType
        
        dir_map = {"buy": Direction.LONG, "sell": Direction.SHORT}
        type_map = {"limit": OrderType.LIMIT, "market": OrderType.MARKET}
        
        order = self.main_engine.send_order(
            symbol=symbol,
            direction=dir_map[direction.lower()],
            type=type_map[order_type.lower()],
            price=price,
            volume=volume
        )
        
        return order.orderid
    
    def close(self):
        """Close connection"""
        if self.main_engine:
            self.main_engine.close()
            logger.info("vn.py connection closed")


class VnpyCTAStrategy:
    """CTA Strategy Wrapper for vn.py"""
    
    def __init__(self, strategy_name: str, class_name: str):
        self.strategy_name = strategy_name
        self.class_name = class_name
        self.vt_symbol = ""
        self.volume = 1
        self.parameters = {}
    
    def set_parameters(self, params: Dict[str, Any]):
        """Set strategy parameters"""
        self.parameters = params
    
    def set_symbol(self, vt_symbol: str):
        """Set trading symbol"""
        self.vt_symbol = vt_symbol
    
    def to_setting(self) -> Dict[str, Any]:
        """Convert to vn.py setting format"""
        return {
            "strategy_name": self.strategy_name,
            "class_name": self.class_name,
            "vt_symbol": self.vt_symbol,
            "volume": self.volume,
            **self.parameters
        }


def run_vnpy_gui():
    """Run standalone vn.py GUI"""
    if not VNPY_AVAILABLE:
        print("vn.py not installed, please install with: pip install vnpy vnpy_ctp")
        return
    
    try:
        # Create default config for SimNow
        config = VnpyConfig(
            username="",
            password="",
            broker_id="9999",
            td_address="tcp://180.168.146.187:10001",
            md_address="tcp://180.168.146.187:10002",
            product="simnow"
        )
        
        trader = VnpyTrader()
        trader.init(config)
        trader.start_gui()
    except Exception as e:
        logger.error(f"Failed to run vn.py GUI: {e}")


if __name__ == "__main__":
    run_vnpy_gui()