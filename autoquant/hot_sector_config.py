"""
2025年热门板块及子板块龙头股配置
每个子板块筛选3只主板龙头股

板块结构:
- 光通信
  - 光芯片: 源杰科技(688498)、长光华芯(688048)、仕佳光子(688313)
  - 光材料: 天通股份(600330)、博创科技(300548)
  - 光模块: 光迅科技(002281)、剑桥科技(603083)、华工科技(000988)
  
- 存储
  - 存储芯片: 兆易创新(603986)、北京君正(300223)
  - 存储模组: 澜起科技(688008)、聚辰股份(688123)
  
- 半导体
  - 半导体设备: 北方华创(002371)、中微公司(688012)
  - 半导体设计: 韦尔股份(603501)、卓胜微(300782)
  
- 稀土
  - 稀土资源: 北方稀土(600111)、中国稀土(000831)
  - 稀土永磁: 金力永磁(300748)、正海磁材(300224)
"""

# 2025年热门板块及子板块龙头股（主板优先，创业板备用）
HOT_SECTOR_CONFIG = {
    '光通信': {
        'desc': 'AI算力光模块产业链',
        'sub_sectors': {
            '光芯片': {
                'desc': '高速光芯片国产替代',
                'leaders': {
                    '688498.SH': {'name': '源杰科技', 'exchange': '科创板'},
                    '688048.SH': {'name': '长光华芯', 'exchange': '科创板'},
                    '688313.SH': {'name': '仕佳光子', 'exchange': '科创板'},
                }
            },
            '光材料': {
                'desc': '光通信材料',
                'leaders': {
                    '600330.SH': {'name': '天通股份', 'exchange': '主板'},
                    '300548.SH': {'name': '博创科技', 'exchange': '创业板'},
                    '002281.SZ': {'name': '光迅科技', 'exchange': '主板'},  # 光器件+光模块
                }
            },
            '光模块': {
                'desc': '800G光模块全球领先',
                'leaders': {
                    '002281.SZ': {'name': '光迅科技', 'exchange': '主板'},
                    '603083.SH': {'name': '剑桥科技', 'exchange': '主板'},
                    '000988.SZ': {'name': '华工科技', 'exchange': '主板'},
                }
            },
            '光纤光缆': {
                'desc': '光纤预制棒+光缆',
                'leaders': {
                    '600487.SH': {'name': '亨通光电', 'exchange': '主板'},
                    '601869.SH': {'name': '长飞光纤', 'exchange': '主板'},
                    '002491.SZ': {'name': '通鼎互联', 'exchange': '主板'},
                }
            }
        }
    },
    '存储': {
        'desc': 'HBM+国产存储芯片',
        'sub_sectors': {
            '存储芯片': {
                'desc': 'DRAM+NAND Flash',
                'leaders': {
                    '603986.SH': {'name': '兆易创新', 'exchange': '主板'},
                    '688008.SH': {'name': '澜起科技', 'exchange': '科创板'},
                    '300223.SZ': {'name': '北京君正', 'exchange': '创业板'},
                }
            },
            '存储模组': {
                'desc': '模组+主控芯片',
                'leaders': {
                    '688123.SH': {'name': '聚辰股份', 'exchange': '科创板'},
                    '300782.SZ': {'name': '卓胜微', 'exchange': '创业板'},
                    '002049.SZ': {'name': '紫光国微', 'exchange': '主板'},
                }
            }
        }
    },
    '半导体': {
        'desc': '国产替代核心领域',
        'sub_sectors': {
            '半导体设备': {
                'desc': '晶圆制造设备',
                'leaders': {
                    '002371.SZ': {'name': '北方华创', 'exchange': '主板'},
                    '688012.SH': {'name': '中微公司', 'exchange': '科创板'},
                    '688396.SH': {'name': '华润微', 'exchange': '科创板'},
                }
            },
            '半导体设计': {
                'desc': 'IC设计',
                'leaders': {
                    '603501.SH': {'name': '韦尔股份', 'exchange': '主板'},
                    '688521.SH': {'name': '芯原股份', 'exchange': '科创板'},
                    '002230.SZ': {'name': '科大讯飞', 'exchange': '主板'},
                }
            },
            '封装测试': {
                'desc': '先进封装',
                'leaders': {
                    '600584.SH': {'name': '长电科技', 'exchange': '主板'},
                    '002185.SZ': {'name': '华天科技', 'exchange': '主板'},
                    '600667.SH': {'name': '太极实业', 'exchange': '主板'},
                }
            }
        }
    },
    '稀土': {
        'desc': '稀缺资源+战略金属',
        'sub_sectors': {
            '稀土资源': {
                'desc': '稀土矿开采',
                'leaders': {
                    '600111.SH': {'name': '北方稀土', 'exchange': '主板'},
                    '000831.SZ': {'name': '中国稀土', 'exchange': '主板'},
                    '002756.SZ': {'name': '永兴材料', 'exchange': '主板'},
                }
            },
            '稀土永磁': {
                'desc': '钕铁硼磁材',
                'leaders': {
                    '300748.SZ': {'name': '金力永磁', 'exchange': '创业板'},
                    '300224.SZ': {'name': '正海磁材', 'exchange': '创业板'},
                    '002460.SZ': {'name': '赣锋锂业', 'exchange': '主板'},
                }
            }
        }
    },
    '有色金属': {
        'desc': '工业金属+贵金属',
        'sub_sectors': {
            '铜': {
                'desc': '铜矿+铜加工',
                'leaders': {
                    '601899.SH': {'name': '紫金矿业', 'exchange': '主板'},
                    '600547.SH': {'name': '山东黄金', 'exchange': '主板'},
                    '000878.SZ': {'name': '云南铜业', 'exchange': '主板'},
                }
            },
            '钼': {
                'desc': '稀缺小金属',
                'leaders': {
                    '603993.SH': {'name': '洛阳钼业', 'exchange': '主板'},
                    '600456.SH': {'name': '宝钛股份', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                }
            },
            '铝': {
                'desc': '电解铝+铝加工',
                'leaders': {
                    '601600.SH': {'name': '中国铝业', 'exchange': '主板'},
                    '000807.SZ': {'name': '云铝股份', 'exchange': '主板'},
                    '002532.SZ': {'name': '天山铝业', 'exchange': '主板'},
                }
            }
        }
    },
    '新能源': {
        'desc': '锂电+光伏+风电',
        'sub_sectors': {
            '锂电': {
                'desc': '锂电池产业链',
                'leaders': {
                    '002594.SZ': {'name': '比亚迪', 'exchange': '主板'},
                    '300750.SZ': {'name': '宁德时代', 'exchange': '创业板'},
                    '002460.SZ': {'name': '赣锋锂业', 'exchange': '主板'},
                }
            },
            '光伏': {
                'desc': '光伏产业链',
                'leaders': {
                    '601012.SH': {'name': '隆基绿能', 'exchange': '主板'},
                    '002459.SZ': {'name': '晶澳科技', 'exchange': '主板'},
                    '600438.SH': {'name': '通威股份', 'exchange': '主板'},
                }
            },
            '风电': {
                'desc': '风电设备',
                'leaders': {
                    '601615.SH': {'name': '明阳智能', 'exchange': '主板'},
                    '002202.SZ': {'name': '金风科技', 'exchange': '主板'},
                    '600905.SH': {'name': '三峡能源', 'exchange': '主板'},
                }
            }
        }
    },
    '消费': {
        'desc': '食品饮料+家电',
        'sub_sectors': {
            '白酒': {
                'desc': '高端白酒',
                'leaders': {
                    '600519.SH': {'name': '贵州茅台', 'exchange': '主板'},
                    '000858.SZ': {'name': '五粮液', 'exchange': '主板'},
                    '000568.SZ': {'name': '泸州老窖', 'exchange': '主板'},
                }
            },
            '家电': {
                'desc': '白电+小家电',
                'leaders': {
                    '000333.SZ': {'name': '美的集团', 'exchange': '主板'},
                    '000651.SZ': {'name': '格力电器', 'exchange': '主板'},
                    '600690.SH': {'name': '海尔智家', 'exchange': '主板'},
                }
            }
        }
    }
}


def get_all_leaders(exchange_filter: str = None) -> dict:
    """
    获取所有龙头股
    
    Args:
        exchange_filter: 过滤交易所类型 ('主板', '创业板', '科创板', None=全部)
    
    Returns:
        龙头股字典 {代码: 信息}
    """
    all_leaders = {}
    
    for sector, sector_info in HOT_SECTOR_CONFIG.items():
        for sub_sector, sub_info in sector_info['sub_sectors'].items():
            for code, info in sub_info['leaders'].items():
                if exchange_filter is None or info['exchange'] == exchange_filter:
                    all_leaders[code] = {
                        **info,
                        'sector': sector,
                        'sub_sector': sub_sector,
                        'sub_sector_desc': sub_info['desc']
                    }
    
    return all_leaders


def get_main_board_leaders() -> dict:
    """获取主板龙头股"""
    return get_all_leaders('主板')


def print_sector_config():
    """打印板块配置"""
    print("=" * 80)
    print("2025年热门板块及子板块龙头股配置")
    print("=" * 80)
    
    for sector, sector_info in HOT_SECTOR_CONFIG.items():
        print(f"\n📊 {sector} - {sector_info['desc']}")
        print("-" * 60)
        
        for sub_sector, sub_info in sector_info['sub_sectors'].items():
            print(f"  📁 {sub_sector} ({sub_info['desc']})")
            
            leaders = sub_info['leaders']
            # 每行显示3只
            leader_list = list(leaders.items())
            for i in range(0, len(leader_list), 3):
                row = leader_list[i:i+3]
                line = "    "
                for code, info in row:
                    exchange_mark = "🅰️" if info['exchange'] == '主板' else "🅱️" if info['exchange'] == '创业板' else "🅲"
                    line += f"{exchange_mark} {code} {info['name']} | "
                print(line.rstrip(" |"))
    
    print("\n" + "=" * 80)
    print("主板龙头股统计:")
    main_board = get_main_board_leaders()
    print(f"  主板龙头股: {len(main_board)} 只")
    print("=" * 80)


if __name__ == '__main__':
    print_sector_config()