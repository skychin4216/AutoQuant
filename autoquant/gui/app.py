import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import threading
from datetime import datetime
from typing import Optional, Dict, List
import pandas as pd
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QSpinBox,
    QDoubleSpinBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QSplitter, QGroupBox, QFormLayout, QProgressBar, QMessageBox,
    QFileDialog, QDateEdit, QCheckBox, QListWidget, QListWidgetItem,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCursor

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from autoquant.data import DataFeed
from autoquant.strategy import StrategyEngine, BaseStrategy, SignalType
from autoquant.backtest import BackTestEngine
from autoquant.analyzer import PerformanceAnalyzer


class AIAssistant:
    """AI助手类 - 支持多种AI API"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = 'openai'):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY', '')
        self.provider = provider
        self.conversation_history = []
        self.system_prompt = """你是AutoQuant量化交易系统的AI助手。你具备以下能力：

1. **策略生成**: 根据用户描述自动生成量化策略代码
2. **参数优化**: 建议策略参数并进行优化
3. **市场分析**: 分析市场趋势和交易机会
4. **回测解释**: 解释回测结果和绩效指标
5. **风险管理**: 提供风险控制建议

当用户请求创建策略时，请返回完整的Python代码，格式如下：
```python
class StrategyName(BaseStrategy):
    def __init__(self, params=None):
        # 初始化参数
        pass
    
    def generate_signal(self, data):
        # 交易逻辑
        return SignalType.LONG / SignalType.SHORT / SignalType.HOLD
```

请用中文回复，保持专业和友好。"""
    
    def chat(self, user_message: str) -> str:
        """发送消息到AI并获取回复"""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        try:
            if self.provider == 'openai' and self.api_key:
                return self._call_openai()
            elif self.provider == 'anthropic' and self.api_key:
                return self._call_anthropic()
            else:
                return self._local_response(user_message)
        except Exception as e:
            return f"AI调用失败: {str(e)}\n\n请设置API密钥或使用本地模式。"
    
    def _call_openai(self) -> str:
        """调用OpenAI API"""
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        reply = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply
    
    def _call_anthropic(self) -> str:
        """调用Anthropic Claude API"""
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        reply = response.content[0].text
        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply
    
    def _local_response(self, user_message: str) -> str:
        """本地模式 - 模拟AI回复"""
        # 检测用户意图并生成相应回复
        if '策略' in user_message or 'strategy' in user_message.lower():
            if '均线' in user_message or 'sma' in user_message.lower():
                return """好的，我为您生成一个均线交叉策略：

```python
class SMACrossStrategy(BaseStrategy):
    def __init__(self, params=None):
        default_params = {'short_window': 10, 'long_window': 30}
        default_params.update(params or {})
        super().__init__(default_params)
    
    def generate_signal(self, data):
        if len(data) < self.params['long_window']:
            return SignalType.HOLD
        
        short_sma = data['close'].rolling(self.params['short_window']).mean().iloc[-1]
        long_sma = data['close'].rolling(self.params['long_window']).mean().iloc[-1]
        
        if short_sma > long_sma:
            return SignalType.LONG
        elif short_sma < long_sma:
            return SignalType.SHORT
        return SignalType.HOLD
```

您可以在策略面板中点击"添加策略"来使用这个策略。"""
            
            elif '动量' in user_message or 'momentum' in user_message.lower():
                return """好的，我为您生成一个动量策略：

```python
class MomentumStrategy(BaseStrategy):
    def __init__(self, params=None):
        default_params = {'lookback': 20, 'threshold': 0.02}
        default_params.update(params or {})
        super().__init__(default_params)
    
    def generate_signal(self, data):
        if len(data) < self.params['lookback']:
            return SignalType.HOLD
        
        momentum = (data['close'].iloc[-1] / data['close'].iloc[-self.params['lookback']] - 1)
        
        if momentum > self.params['threshold']:
            return SignalType.LONG
        elif momentum < -self.params['threshold']:
            return SignalType.SHORT
        return SignalType.HOLD
```

这个策略会在价格在lookback期内上涨超过threshold时买入，下跌超过threshold时卖出。"""
            
            else:
                return """我可以帮您创建多种量化策略：

1. **均线交叉策略** - SMA/EMA交叉
2. **动量策略** - 价格动量突破
3. **均值回归策略** - 统计套利
4. **趋势跟踪策略** - 趋势识别
5. **多因子策略** - 综合多个指标

请告诉我您想要什么类型的策略，我会为您生成代码。"""
        
        elif '回测' in user_message or 'backtest' in user_message.lower():
            return """回测功能说明：

1. 在左侧面板选择策略
2. 设置初始资金、股票代码、日期范围
3. 点击"开始回测"按钮
4. 查看右侧的绩效报告和图表

我可以帮您：
- 解释回测结果
- 优化策略参数
- 分析绩效指标
- 提供改进建议

请问您想了解什么？"""
        
        elif '参数' in user_message or 'optimize' in user_message.lower():
            return """参数优化建议：

对于均线策略，建议的参数范围：
- short_window: 5-20天
- long_window: 20-60天

对于RSI策略：
- period: 10-20天
- overbought: 70-80
- oversold: 20-30

您可以在策略参数面板中调整这些参数，然后运行回测查看效果。"""
        
        else:
            return """我是AutoQuant的AI助手，可以帮您：

✅ **创建策略** - 描述您的交易想法，我生成代码
✅ **优化参数** - 分析最佳参数组合
✅ **解释结果** - 解读回测绩效指标
✅ **风险建议** - 提供风控建议

请告诉我您需要什么帮助？"""


class AIThread(QThread):
    """AI调用线程"""
    response_signal = pyqtSignal(str)
    
    def __init__(self, ai_assistant: AIAssistant, message: str):
        super().__init__()
        self.ai_assistant = ai_assistant
        self.message = message
    
    def run(self):
        response = self.ai_assistant.chat(self.message)
        self.response_signal.emit(response)


class ChatWidget(QWidget):
    """AI对话窗口"""
    
    def __init__(self, ai_assistant: AIAssistant):
        super().__init__()
        self.ai_assistant = ai_assistant
        self.ai_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 聊天历史显示
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont('Microsoft YaHei', 10))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.chat_display, 1)
        
        # 输入区域
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入您的问题或策略需求...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field, 1)
        
        self.send_button = QPushButton("发送")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(QWidget())  # 占位
        layout.addLayout(input_layout)
        
        # 添加欢迎消息
        self.add_message("AI助手", "欢迎使用AutoQuant AI助手！我可以帮您创建策略、优化参数、分析回测结果。请问有什么可以帮助您的？", "#4ec9b0")
    
    def add_message(self, sender: str, message: str, color: str = "#d4d4d4"):
        """添加消息到聊天显示"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"""
        <div style="margin: 5px 0;">
            <span style="color: {color}; font-weight: bold;">{sender}</span>
            <span style="color: #808080; font-size: 9px;"> [{timestamp}]</span>
        </div>
        <div style="margin-left: 10px; color: #d4d4d4; white-space: pre-wrap;">{message}</div>
        <hr style="border: none; border-top: 1px solid #3c3c3c; margin: 5px 0;">
        """
        self.chat_display.append(formatted_message)
        self.chat_display.moveCursor(QTextCursor.End)
    
    def send_message(self):
        """发送用户消息"""
        message = self.input_field.text().strip()
        if not message:
            return
        
        self.add_message("您", message, "#569cd6")
        self.input_field.clear()
        self.input_field.setDisabled(True)
        self.send_button.setDisabled(True)
        
        # 启动AI线程
        self.ai_thread = AIThread(self.ai_assistant, message)
        self.ai_thread.response_signal.connect(self.handle_response)
        self.ai_thread.start()
    
    def handle_response(self, response: str):
        """处理AI响应"""
        self.add_message("AI助手", response, "#4ec9b0")
        self.input_field.setDisabled(False)
        self.send_button.setDisabled(False)


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib图表画布"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.fig.patch.set_facecolor('#1e1e1e')
        self.axes.set_facecolor('#1e1e1e')
        self.axes.tick_params(colors='#d4d4d4')
        self.axes.spines['bottom'].set_color('#3c3c3c')
        self.axes.spines['top'].set_color('#3c3c3c')
        self.axes.spines['left'].set_color('#3c3c3c')
        self.axes.spines['right'].set_color('#3c3c3c')
    
    def plot_equity(self, data: pd.DataFrame):
        """绘制收益曲线"""
        self.axes.clear()
        self.axes.plot(data['date'], data['total_assets'], color='#4ec9b0', linewidth=2)
        self.axes.fill_between(data['date'], data['total_assets'], alpha=0.3, color='#4ec9b0')
        self.axes.set_title('收益曲线', color='#d4d4d4')
        self.axes.set_xlabel('日期', color='#d4d4d4')
        self.axes.set_ylabel('资产价值', color='#d4d4d4')
        self.axes.grid(True, alpha=0.3)
        self.draw()
    
    def plot_drawdown(self, data: pd.DataFrame):
        """绘制回撤图"""
        self.axes.clear()
        drawdown = (data['total_assets'] - data['total_assets'].cummax()) / data['total_assets'].cummax()
        self.axes.plot(data['date'], drawdown, color='#f14c4c', linewidth=2)
        self.axes.fill_between(data['date'], drawdown, alpha=0.3, color='#f14c4c')
        self.axes.set_title('最大回撤', color='#d4d4d4')
        self.axes.set_xlabel('日期', color='#d4d4d4')
        self.axes.set_ylabel('回撤', color='#d4d4d4')
        self.axes.grid(True, alpha=0.3)
        self.draw()


class BacktestThread(QThread):
    """回测线程"""
    finished_signal = pyqtSignal(pd.DataFrame, dict)
    progress_signal = pyqtSignal(int)
    
    def __init__(self, data: pd.DataFrame, strategy: BaseStrategy, initial_capital: float):
        super().__init__()
        self.data = data
        self.strategy = strategy
        self.initial_capital = initial_capital
    
    def run(self):
        engine = BackTestEngine(initial_capital=self.initial_capital)
        results = engine.run(self.data, self.strategy)
        summary = engine.get_summary()
        self.finished_signal.emit(results, summary)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.ai_assistant = AIAssistant()
        self.strategy_engine = StrategyEngine()
        self.current_strategy = None
        self.backtest_results = None
        self.backtest_thread = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("AutoQuant - 智能量化交易系统")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
            QGroupBox {
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:disabled {
                background-color: #3c3c3c;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                padding: 5px;
            }
            QDateEdit {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                padding: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #d4d4d4;
                padding: 8px 20px;
                border: 1px solid #3c3c3c;
            }
            QTabBar::tab:selected {
                background-color: #0e639c;
            }
            QTableWidget {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                gridline-color: #3c3c3c;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                padding: 5px;
                border: 1px solid #3c3c3c;
            }
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #0e639c;
            }
        """)
        
        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(350)
        
        # 策略选择
        strategy_group = QGroupBox("策略设置")
        strategy_layout = QFormLayout()
        
        self.strategy_combo = QComboBox()
        for name in self.strategy_engine.get_available_strategies():
            self.strategy_combo.addItem(name)
        self.strategy_combo.currentTextChanged.connect(self.on_strategy_changed)
        strategy_layout.addRow("策略类型:", self.strategy_combo)
        
        # 参数设置
        self.param_short = QSpinBox()
        self.param_short.setRange(1, 100)
        self.param_short.setValue(20)
        strategy_layout.addRow("短期窗口:", self.param_short)
        
        self.param_long = QSpinBox()
        self.param_long.setRange(1, 200)
        self.param_long.setValue(60)
        strategy_layout.addRow("长期窗口:", self.param_long)
        
        strategy_group.setLayout(strategy_layout)
        left_layout.addWidget(strategy_group)
        
        # 回测设置
        backtest_group = QGroupBox("回测设置")
        backtest_layout = QFormLayout()
        
        self.symbol_input = QLineEdit("AAPL")
        backtest_layout.addRow("股票代码:", self.symbol_input)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate(2020, 1, 1))
        backtest_layout.addRow("开始日期:", self.start_date)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate(2023, 12, 31))
        backtest_layout.addRow("结束日期:", self.end_date)
        
        self.capital_input = QDoubleSpinBox()
        self.capital_input.setRange(1000, 10000000)
        self.capital_input.setValue(100000)
        self.capital_input.setPrefix("$ ")
        backtest_layout.addRow("初始资金:", self.capital_input)
        
        self.commission_input = QDoubleSpinBox()
        self.commission_input.setRange(0, 0.01)
        self.commission_input.setValue(0.001)
        self.commission_input.setDecimals(4)
        backtest_layout.addRow("佣金率:", self.commission_input)
        
        backtest_group.setLayout(backtest_layout)
        left_layout.addWidget(backtest_group)
        
        # 数据源设置
        data_group = QGroupBox("数据源")
        data_layout = QFormLayout()
        
        self.data_source_combo = QComboBox()
        self.data_source_combo.addItems(['yahoo', 'csv'])
        data_layout.addRow("数据源:", self.data_source_combo)
        
        self.load_data_btn = QPushButton("加载CSV数据")
        self.load_data_btn.clicked.connect(self.load_csv_data)
        data_layout.addRow(self.load_data_btn)
        
        data_group.setLayout(data_layout)
        left_layout.addWidget(data_group)
        
        # 股票筛选设置
        filter_group = QGroupBox("股票筛选")
        filter_layout = QFormLayout()
        
        # 主板股票过滤复选框（默认勾选）
        self.main_board_checkbox = QCheckBox("只分析主板股票")
        self.main_board_checkbox.setChecked(True)  # 默认勾选
        self.main_board_checkbox.setToolTip(
            "主板股票:\n"
            "- 沪市主板: 600xxx, 601xxx, 603xxx\n"
            "- 深市主板: 000xxx, 001xxx\n\n"
            "排除:\n"
            "- 科创板 (688xxx)\n"
            "- 创业板 (300xxx)\n"
            "- 北交所 (8xxxxx)"
        )
        filter_layout.addRow(self.main_board_checkbox)
        
        # 指数选择
        self.index_combo = QComboBox()
        self.index_combo.addItems(['中证A500', '中证500', '沪深300', '全市场'])
        self.index_combo.setToolTip("选择参考指数成分股作为筛选范围")
        filter_layout.addRow("参考指数:", self.index_combo)
        
        # 获取主板股票按钮
        self.fetch_mainboard_btn = QPushButton("获取主板股票列表")
        self.fetch_mainboard_btn.clicked.connect(self.fetch_mainboard_stocks)
        filter_layout.addRow(self.fetch_mainboard_btn)
        
        # 显示当前股票数量
        self.stock_count_label = QLabel("主板股票: 0 只")
        filter_layout.addRow(self.stock_count_label)
        
        filter_group.setLayout(filter_layout)
        left_layout.addWidget(filter_group)
        
        # 操作按钮
        button_group = QGroupBox("操作")
        button_layout = QVBoxLayout()
        
        self.run_backtest_btn = QPushButton("▶ 开始回测")
        self.run_backtest_btn.clicked.connect(self.run_backtest)
        button_layout.addWidget(self.run_backtest_btn)
        
        self.compare_btn = QPushButton("📊 策略对比")
        self.compare_btn.clicked.connect(self.compare_strategies)
        button_layout.addWidget(self.compare_btn)
        
        self.export_btn = QPushButton("💾 导出结果")
        self.export_btn.clicked.connect(self.export_results)
        button_layout.addWidget(self.export_btn)
        
        button_group.setLayout(button_layout)
        left_layout.addWidget(button_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel)
        
        # 右侧主区域
        right_panel = QTabWidget()
        
        # AI对话标签页
        self.chat_widget = ChatWidget(self.ai_assistant)
        right_panel.addTab(self.chat_widget, "🤖 AI助手")
        
        # 回测结果标签页
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        
        # 绩效指标表格
        self.metrics_table = QTableWidget()
        self.metrics_table.setColumnCount(2)
        self.metrics_table.setHorizontalHeaderLabels(['指标', '数值'])
        self.metrics_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.metrics_table)
        
        # 图表区域
        charts_splitter = QSplitter(Qt.Horizontal)
        
        self.equity_canvas = MatplotlibCanvas(self, width=5, height=3)
        charts_splitter.addWidget(self.equity_canvas)
        
        self.drawdown_canvas = MatplotlibCanvas(self, width=5, height=3)
        charts_splitter.addWidget(self.drawdown_canvas)
        
        results_layout.addWidget(charts_splitter)
        right_panel.addTab(results_widget, "📈 回测结果")
        
        # 策略列表标签页
        strategies_widget = QWidget()
        strategies_layout = QVBoxLayout(strategies_widget)
        
        self.strategy_list = QListWidget()
        for name in self.strategy_engine.get_available_strategies():
            self.strategy_list.addItem(name)
        strategies_layout.addWidget(self.strategy_list)
        
        self.add_strategy_btn = QPushButton("从AI添加策略")
        self.add_strategy_btn.clicked.connect(self.add_strategy_from_ai)
        strategies_layout.addWidget(self.add_strategy_btn)
        
        right_panel.addTab(strategies_widget, "📋 策略列表")
        
        main_layout.addWidget(right_panel, 1)
        
        # 状态栏
        self.statusBar().showMessage("就绪 | AutoQuant v1.0.0")
    
    def on_strategy_changed(self, strategy_name: str):
        """策略改变时更新参数"""
        self.current_strategy = self.strategy_engine.create_strategy(strategy_name)
        params = self.current_strategy.get_params()
        
        if 'short_window' in params:
            self.param_short.setValue(params['short_window'])
        if 'long_window' in params:
            self.param_long.setValue(params['long_window'])
    
    def load_csv_data(self):
        """加载CSV数据文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择CSV文件", "", "CSV Files (*.csv)")
        if file_path:
            self.statusBar().showMessage(f"已加载: {file_path}")
    
    def fetch_mainboard_stocks(self):
        """获取主板股票列表"""
        from autoquant.dragon_filter import DragonStockFilter
        
        # 获取数据目录中的所有股票
        data_dir = 'E:\\workspace\\AutoQuant\\data'
        feed = DataFeed(source='csv', data_dir=data_dir)
        all_symbols = feed.get_symbols()
        
        # 根据主板过滤选项筛选
        main_board_only = self.main_board_checkbox.isChecked()
        
        if main_board_only:
            mainboard_symbols = [s for s in all_symbols if DragonStockFilter.is_main_board(s)]
            self.stock_count_label.setText(f"主板股票: {len(mainboard_symbols)} 只")
            self.statusBar().showMessage(f"已获取 {len(mainboard_symbols)} 只主板股票")
            
            # 显示股票列表
            if mainboard_symbols:
                stock_list_msg = "主板股票列表:\n" + "\n".join(mainboard_symbols[:20])
                if len(mainboard_symbols) > 20:
                    stock_list_msg += f"\n... 共 {len(mainboard_symbols)} 只"
                QMessageBox.information(self, "主板股票", stock_list_msg)
        else:
            self.stock_count_label.setText(f"全部股票: {len(all_symbols)} 只")
            self.statusBar().showMessage(f"已获取 {len(all_symbols)} 只全部股票")
    
    def run_backtest(self):
        """运行回测"""
        self.run_backtest_btn.setDisabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 获取设置
        strategy_name = self.strategy_combo.currentText()
        params = {
            'short_window': self.param_short.value(),
            'long_window': self.param_long.value(),
        }
        
        symbol = self.symbol_input.text()
        start_date = self.start_date.date().toString('yyyy-MM-dd')
        end_date = self.end_date.date().toString('yyyy-MM-dd')
        capital = self.capital_input.value()
        
        self.statusBar().showMessage(f"正在获取 {symbol} 数据...")
        
        # 获取数据
        try:
            feed = DataFeed(source=self.data_source_combo.currentText())
            data = feed.get_price(symbol, start_date, end_date)
            
            if data.empty:
                QMessageBox.warning(self, "警告", "无法获取数据，请检查股票代码或日期范围")
                self.run_backtest_btn.setDisabled(False)
                self.progress_bar.setVisible(False)
                return
            
            # 创建策略
            strategy = self.strategy_engine.create_strategy(strategy_name, params)
            
            self.statusBar().showMessage(f"正在运行 {strategy_name} 回测...")
            self.progress_bar.setValue(50)
            
            # 启动回测线程
            self.backtest_thread = BacktestThread(data, strategy, capital)
            self.backtest_thread.finished_signal.connect(self.on_backtest_finished)
            self.backtest_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"回测失败: {str(e)}")
            self.run_backtest_btn.setDisabled(False)
            self.progress_bar.setVisible(False)
    
    def on_backtest_finished(self, results: pd.DataFrame, summary: dict):
        """回测完成处理"""
        self.backtest_results = results
        
        # 更新绩效表格
        self.metrics_table.setRowCount(len(summary))
        for i, (key, value) in enumerate(summary.items()):
            self.metrics_table.setItem(i, 0, QTableWidgetItem(key))
            if isinstance(value, float):
                if 'return' in key or 'rate' in key or 'drawdown' in key:
                    self.metrics_table.setItem(i, 1, QTableWidgetItem(f"{value:.2%}"))
                else:
                    self.metrics_table.setItem(i, 1, QTableWidgetItem(f"{value:.2f}"))
            else:
                self.metrics_table.setItem(i, 1, QTableWidgetItem(str(value)))
        
        # 绘制图表
        self.equity_canvas.plot_equity(results)
        self.drawdown_canvas.plot_drawdown(results)
        
        self.progress_bar.setValue(100)
        self.run_backtest_btn.setDisabled(False)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage(f"回测完成 | 总收益: {summary.get('total_return', 0):.2%}")
    
    def compare_strategies(self):
        """对比多个策略"""
        QMessageBox.information(self, "策略对比", "请在AI助手对话框中输入：\n'对比所有策略' 来运行策略对比")
    
    def export_results(self):
        """导出回测结果"""
        if self.backtest_results is None:
            QMessageBox.warning(self, "警告", "没有可导出的结果")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "保存结果", "", "CSV Files (*.csv)")
        if file_path:
            self.backtest_results.to_csv(file_path, index=False)
            self.statusBar().showMessage(f"已导出: {file_path}")
    
    def add_strategy_from_ai(self):
        """从AI添加策略"""
        QMessageBox.information(self, "添加策略", "请在AI助手对话框中描述您想要的策略，AI会为您生成代码")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 设置深色主题
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(212, 212, 212))
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
    palette.setColor(QPalette.ToolTipBase, QColor(212, 212, 212))
    palette.setColor(QPalette.ToolTipText, QColor(212, 212, 212))
    palette.setColor(QPalette.Text, QColor(212, 212, 212))
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ButtonText, QColor(212, 212, 212))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(14, 99, 156))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()