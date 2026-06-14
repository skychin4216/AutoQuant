# AutoQuant 代码架构与测试文档

## 1. 项目概述

AutoQuant 是一个基于 Python 的量化交易分析平台，支持龙头股筛选、板块热度分析、策略回测等功能。

**数据时间范围**: 2024-01-01 至 2026-06-14

## 2. 核心模块

### 2.1 龙头股筛选模块

| 文件 | 说明 |
|------|------|
| `autoquant/hot_sector_config.py` | 板块配置 - 10大科技板块41子板块，81只龙头股 |
| `autoquant/dragon_filter.py` | 四层漏斗筛选器 |
| `autoquant/LeaderStockPool.py` | 股票池管理 |
| `autoquant/SectorHotRanker.py` | 板块热度排名 |

### 2.2 板块配置 (hot_sector_config.py)

```python
from autoquant.hot_sector_config import HOT_SECTOR_CONFIG, get_main_board_leaders

# 获取所有板块配置
print(HOT_SECTOR_CONFIG.keys())
# ['稀缺小金属', '有色金属', '半导体', 'AI算力', '光通信', 'PCB', '电网设备', '氦气', '新能源', '存储']

# 获取主板龙头股
leaders = get_main_board_leaders()
for code, info in leaders.items():
    print(f"{code}: {info['name']} ({info['sector']}-{info['sub_sector']})")
```

### 2.3 四层漏斗筛选 (dragon_filter.py)

```python
from autoquant.dragon_filter import DragonStockFilter

# 创建筛选器
filter = DragonStockFilter()

# 执行筛选
filtered_stocks, stats = filter.run_full_filter()

print(f"筛选结果: {len(filtered_stocks)} 只龙头股")
for stock in filtered_stocks:
    print(f"  {stock.symbol} {stock.name}")
```

### 2.4 板块热度排名 (SectorHotRanker.py)

```python
from autoquant.SectorHotRanker import SectorHotRanker

# 创建排名器
ranker = SectorHotRanker(end_date='20260614', lookback_days=60, rank_days=5)

# 获取热门板块
hot_sectors = ranker.get_top_sectors(n=10)
print(hot_sectors)
```

## 3. 热门板块结构

### AI硬件供应链主线
```
稀缺小金属(钨钼铌钒钛稀土)
    ↓
有色金属(锂铜铝)
    ↓
半导体(设备/设计/封测/国产替代)
    ↓
AI算力(国产算力/超算/GPU服务器)
    ↓
光通信(光模块/光芯片/铜缆)
    ↓
PCB(服务器PCB/HDI/IC载板)
    ↓
电网设备(特高压/储能)
    ↓
氦气(稀有气体)
    ↓
新能源(锂电/光伏/绿电)
    ↓
存储(HBM/国产存储)
```

### 板块详情

| 板块 | 子板块数 | 主板龙头股数 |
|------|---------|-------------|
| 稀缺小金属 | 6 | 30 |
| 有色金属 | 3 | 15 |
| 半导体 | 4 | 20 |
| AI算力 | 3 | 15 |
| 光通信 | 5 | 25 |
| PCB | 5 | 25 |
| 电网设备 | 5 | 25 |
| 氦气 | 2 | 10 |
| 新能源 | 5 | 25 |
| 存储 | 3 | 15 |
| **合计** | **41** | **81** |

## 4. 测试方法

### 4.1 测试龙头股筛选

```bash
# 测试筛选器
python test_filter_v2.py

# 输出示例:
# 筛选结果: 52 只龙头股
# 📊 光通信
#   📁 光模块
#     ✅ 002281.SZ 光迅科技
#     ✅ 603083.SH 剑桥科技
#     ✅ 000988.SZ 华工科技
```

### 4.2 测试板块配置

```bash
# 打印板块配置
python -c "from autoquant.hot_sector_config import print_sector_config; print_sector_config()"
```

### 4.3 编译exe

```bash
# 编译GUI版本
pyinstaller run_gui.py --name AutoQuant --distpath dist --add-data "autoquant;autoquant" -w

# 编译命令行版本
pyinstaller run_screen.py --name AutoQuant-龙头股筛选 --distpath dist --add-data "autoquant;autoquant" -c
```

## 5. 文件结构

```
e:\workspace\AutoQuant\
├── autoquant/                    # 核心代码包
│   ├── hot_sector_config.py      # 板块配置
│   ├── dragon_filter.py          # 龙头股筛选器
│   ├── LeaderStockPool.py        # 股票池管理
│   ├── SectorHotRanker.py        # 板块排名
│   ├── data.py                   # 数据加载
│   ├── strategy.py               # 策略
│   ├── backtest.py               # 回测
│   ├── risk.py                   # 风险管理
│   ├── gui/                      # GUI模块
│   │   └── app.py
│   ├── vnpy_integration.py       # vn.py集成
│   └── qlib_integration.py       # Qlib集成
├── data/                         # 数据目录
│   ├── 002281.SZ_光迅科技-光通信龙头.csv
│   ├── 002371.SZ_北方华创-半导体设备龙头.csv
│   └── ...
├── dist/                         # 编译输出目录
│   └── AutoQuant-策略分析平台.exe
├── run_gui.py                    # GUI入口
├── run_screen.py                 # 命令行入口
└── test_filter_v2.py            # 测试脚本
```

## 6. 运行要求

- Python 3.13+
- PyQt5
- pandas
- numpy
- yfinance
- matplotlib
- ta (技术分析)

## 7. 编译exe

已编译的exe位于 `dist/` 目录:

| exe文件 | 大小 | 说明 |
|---------|------|------|
| AutoQuant-策略分析平台.exe | ~175MB | GUI版本，支持AI对话 |
| AutoQuant-龙头股筛选.exe | ~184MB | 命令行版本，专注龙头股筛选 |

编译命令:
```bash
# 使用spec文件
pyinstaller AutoQuant-GUI.spec --clean --distpath dist

# 或直接编译
pyinstaller run_gui.py --name AutoQuant --distpath dist --add-data "autoquant;autoquant" -w
```

## 8. 数据说明

数据文件存储在 `E:\workspace\AutoQuant\data\`，包含:
- A股主板龙头股历史数据 (2024-01-01 起)
- 美股科技龙头数据
- 板块热度排名数据

数据来源:
- AKShare (实时)
- Yahoo Finance (美股)
- 本地模拟数据 (当在线数据不可用时)
