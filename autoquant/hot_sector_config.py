"""
2025-2026年热门板块及子板块龙头股配置（扩展版）

时间范围: 2024-01-01 至 2026-06-14（最新交易日）

2024-2026年热门科技板块（AI硬件供应链）:
- 稀缺小金属: 钨、钼、铌、钒、钛、稀土（涨幅最大）
- 有色金属: 锂、铜、铝
- 半导体: 设备、设计、封测、国产替代
- AI算力: 超算、GPU、国产算力、算力芯片
- 光通信: 光模块、光芯片、銅纜高速連接
- PCB: 服務器PCB、HDI板、IC載板
- 電網設備: 特高壓、智能電網、儲能
- 氦氣: 稀有氣體
- 新能源: 鋰電、光伏、綠電
- 存儲: HBM、國產存儲

每個子板塊: 主板 TOP 5（實際取3只）
"""

# 2025年热门板块及子板块龙头股（主板优先，每个子板块5只）
HOT_SECTOR_CONFIG = {
    # ============================================
    # 稀缺小金属（涨幅最大）
    # ============================================
    '稀缺小金属': {
        'desc': '战略资源，国产替代',
        'sub_sectors': {
            '钨': {
                'desc': '硬质合金原材料',
                'leaders': {
                    '601969.SH': {'name': '海南矿业', 'exchange': '主板'},
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                    '002378.SZ': {'name': '章源钨业', 'exchange': '主板'},
                }
            },
            '钼': {
                'desc': '特种钢添加剂',
                'leaders': {
                    '603993.SH': {'name': '洛阳钼业', 'exchange': '主板'},
                    '600456.SH': {'name': '宝钛股份', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                    '002378.SZ': {'name': '章源钨业', 'exchange': '主板'},
                }
            },
            '铌': {
                'desc': '超导材料、半导体',
                'leaders': {
                    '600456.SH': {'name': '宝钛股份', 'exchange': '主板'},
                    '601969.SH': {'name': '海南矿业', 'exchange': '主板'},
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                    '601258.SH': {'name': '庞大集团', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                }
            },
            '钒': {
                'desc': '储能电池材料',
                'leaders': {
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                    '601969.SH': {'name': '海南矿业', 'exchange': '主板'},
                    '002378.SZ': {'name': '章源钨业', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                }
            },
            '钛': {
                'desc': '航空航天、医疗',
                'leaders': {
                    '600456.SH': {'name': '宝钛股份', 'exchange': '主板'},
                    '000545.SZ': {'name': '金浦钛业', 'exchange': '主板'},
                    '002136.SZ': {'name': '安纳达', 'exchange': '主板'},
                    '601969.SH': {'name': '海南矿业', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                }
            },
            '稀土': {
                'desc': '永磁材料、芯片',
                'leaders': {
                    '600111.SH': {'name': '北方稀土', 'exchange': '主板'},
                    '000831.SZ': {'name': '中国稀土', 'exchange': '主板'},
                    '002756.SZ': {'name': '永兴材料', 'exchange': '主板'},
                    '600259.SH': {'name': '广晟有色', 'exchange': '主板'},
                    '600549.SH': {'name': '厦门钨业', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 有色金属
    # ============================================
    '有色金属': {
        'desc': '工业金属+贵金属',
        'sub_sectors': {
            '锂': {
                'desc': '锂电池核心材料',
                'leaders': {
                    '002460.SZ': {'name': '赣锋锂业', 'exchange': '主板'},
                    '002466.SZ': {'name': '天齐锂业', 'exchange': '主板'},
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                    '002756.SZ': {'name': '永兴材料', 'exchange': '主板'},
                    '002074.SZ': {'name': '国轩高科', 'exchange': '主板'},
                }
            },
            '铜': {
                'desc': '电力、建筑用铜',
                'leaders': {
                    '601899.SH': {'name': '紫金矿业', 'exchange': '主板'},
                    '000878.SZ': {'name': '云南铜业', 'exchange': '主板'},
                    '600547.SH': {'name': '山东黄金', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                }
            },
            '铝': {
                'desc': '电解铝、汽车轻量化',
                'leaders': {
                    '601600.SH': {'name': '中国铝业', 'exchange': '主板'},
                    '000807.SZ': {'name': '云铝股份', 'exchange': '主板'},
                    '002532.SZ': {'name': '天山铝业', 'exchange': '主板'},
                    '601702.SH': {'name': '华峰铝业', 'exchange': '主板'},
                    '002501.SZ': {'name': '利源精制', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 半导体（国产替代核心）
    # ============================================
    '半导体': {
        'desc': '国产替代，AI算力基础',
        'sub_sectors': {
            '半导体设备': {
                'desc': '晶圆制造设备',
                'leaders': {
                    '002371.SZ': {'name': '北方华创', 'exchange': '主板'},
                    '688012.SH': {'name': '中微公司', 'exchange': '科创板'},
                    '688396.SH': {'name': '华润微', 'exchange': '科创板'},
                    '688581.SH': {'name': '富乐德', 'exchange': '科创板'},
                    '688125.SH': {'name': '华海清科', 'exchange': '科创板'},
                }
            },
            '半导体设计': {
                'desc': 'IC设计',
                'leaders': {
                    '603501.SH': {'name': '韦尔股份', 'exchange': '主板'},
                    '002230.SZ': {'name': '科大讯飞', 'exchange': '主板'},
                    '688521.SH': {'name': '芯原股份', 'exchange': '科创板'},
                    '688256.SH': {'name': '寒武纪', 'exchange': '科创板'},
                    '688981.SH': {'name': '中芯国际', 'exchange': '科创板'},
                }
            },
            '半导体封测': {
                'desc': '先进封装、Chiplet',
                'leaders': {
                    '600584.SH': {'name': '长电科技', 'exchange': '主板'},
                    '002185.SZ': {'name': '华天科技', 'exchange': '主板'},
                    '600667.SH': {'name': '太极实业', 'exchange': '主板'},
                    '603228.SH': {'name': '晶方科技', 'exchange': '主板'},
                    '002156.SZ': {'name': '通富微电', 'exchange': '主板'},
                }
            },
            '国产替代': {
                'desc': 'EDA、光刻机、材料',
                'leaders': {
                    '688521.SH': {'name': '芯原股份', 'exchange': '科创板'},
                    '688008.SH': {'name': '澜起科技', 'exchange': '科创板'},
                    '688396.SH': {'name': '华润微', 'exchange': '科创板'},
                    '688981.SH': {'name': '中芯国际', 'exchange': '科创板'},
                    '002371.SZ': {'name': '北方华创', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # AI算力（2024-2025最大主线）
    # ============================================
    'AI算力': {
        'desc': '大模型训练，推理算力',
        'sub_sectors': {
            '国产算力': {
                'desc': '华为昇腾、寒武纪',
                'leaders': {
                    '002230.SZ': {'name': '科大讯飞', 'exchange': '主板'},
                    '688256.SH': {'name': '寒武纪', 'exchange': '科创板'},
                    '688787.SH': {'name': '海天瑞声', 'exchange': '科创板'},
                    '688521.SH': {'name': '芯原股份', 'exchange': '科创板'},
                    '603019.SH': {'name': '中科曙光', 'exchange': '主板'},
                }
            },
            '超算/数据中心': {
                'desc': '高性能计算',
                'leaders': {
                    '603019.SH': {'name': '中科曙光', 'exchange': '主板'},
                    '000977.SZ': {'name': '浪潮信息', 'exchange': '主板'},
                    '600588.SH': {'name': '用友网络', 'exchange': '主板'},
                    '002410.SZ': {'name': '广联达', 'exchange': '主板'},
                    '688787.SH': {'name': '海天瑞声', 'exchange': '科创板'},
                }
            },
            'GPU/服务器': {
                'desc': 'AI服务器',
                'leaders': {
                    '000977.SZ': {'name': '浪潮信息', 'exchange': '主板'},
                    '603019.SH': {'name': '中科曙光', 'exchange': '主板'},
                    '000938.SZ': {'name': '紫光股份', 'exchange': '主板'},
                    '603019.SH': {'name': '中科曙光', 'exchange': '主板'},
                    '002230.SZ': {'name': '科大讯飞', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 光通信（英伟达供应链）
    # ============================================
    '光通信': {
        'desc': 'AI算力基础设施',
        'sub_sectors': {
            '光模块': {
                'desc': '800G光模块全球领先',
                'leaders': {
                    '002281.SZ': {'name': '光迅科技', 'exchange': '主板'},
                    '603083.SH': {'name': '剑桥科技', 'exchange': '主板'},
                    '000988.SZ': {'name': '华工科技', 'exchange': '主板'},
                    '300308.SZ': {'name': '中际旭创', 'exchange': '创业板'},
                    '300502.SZ': {'name': '新易盛', 'exchange': '创业板'},
                }
            },
            '光纤光缆': {
                'desc': '光纤预制棒',
                'leaders': {
                    '600487.SH': {'name': '亨通光电', 'exchange': '主板'},
                    '601869.SH': {'name': '长飞光纤', 'exchange': '主板'},
                    '002491.SZ': {'name': '通鼎互联', 'exchange': '主板'},
                    '600198.SH': {'name': '大唐电信', 'exchange': '主板'},
                    '002093.SZ': {'name': '国脉科技', 'exchange': '主板'},
                }
            },
            '光芯片': {
                'desc': '高速光芯片国产替代',
                'leaders': {
                    '688498.SH': {'name': '源杰科技', 'exchange': '科创板'},
                    '688048.SH': {'name': '长光华芯', 'exchange': '科创板'},
                    '688313.SH': {'name': '仕佳光子', 'exchange': '科创板'},
                    '002281.SZ': {'name': '光迅科技', 'exchange': '主板'},
                    '603083.SH': {'name': '剑桥科技', 'exchange': '主板'},
                }
            },
            '光材料': {
                'desc': '光学材料',
                'leaders': {
                    '600330.SH': {'name': '天通股份', 'exchange': '主板'},
                    '300548.SH': {'name': '博创科技', 'exchange': '创业板'},
                    '002281.SZ': {'name': '光迅科技', 'exchange': '主板'},
                    '603083.SH': {'name': '剑桥科技', 'exchange': '主板'},
                    '000988.SZ': {'name': '华工科技', 'exchange': '主板'},
                }
            },
            '铜缆高速连接': {
                'desc': '英伟达GB200铜缆连接',
                'leaders': {
                    '603803.SH': {'name': '瑞斯康达', 'exchange': '主板'},
                    '002463.SZ': {'name': '沪电股份', 'exchange': '主板'},
                    '603228.SH': {'name': '晶方科技', 'exchange': '主板'},
                    '300735.SZ': {'name': '光弘科技', 'exchange': '创业板'},
                    '002916.SZ': {'name': '深南电路', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # PCB（英伟达供应链）
    # ============================================
    'PCB': {
        'desc': '印制电路板，AI服务器核心材料',
        'sub_sectors': {
            '服务器PCB': {
                'desc': 'AI服务器PCB',
                'leaders': {
                    '002463.SZ': {'name': '沪电股份', 'exchange': '主板'},
                    '002916.SZ': {'name': '深南电路', 'exchange': '主板'},
                    '603186.SH': {'name': '华正新材', 'exchange': '主板'},
                    '603228.SH': {'name': '晶方科技', 'exchange': '主板'},
                    '002288.SZ': {'name': '超华科技', 'exchange': '主板'},
                }
            },
            'HDI板': {
                'desc': '高密度互联板',
                'leaders': {
                    '002916.SZ': {'name': '深南电路', 'exchange': '主板'},
                    '002463.SZ': {'name': '沪电股份', 'exchange': '主板'},
                    '000823.SZ': {'name': '超声电子', 'exchange': '主板'},
                    '603186.SH': {'name': '华正新材', 'exchange': '主板'},
                    '603228.SH': {'name': '晶方科技', 'exchange': '主板'},
                }
            },
            'IC载板': {
                'desc': '先进封装载板',
                'leaders': {
                    '002916.SZ': {'name': '深南电路', 'exchange': '主板'},
                    '600584.SH': {'name': '长电科技', 'exchange': '主板'},
                    '002185.SZ': {'name': '华天科技', 'exchange': '主板'},
                    '603228.SH': {'name': '晶方科技', 'exchange': '主板'},
                    '002156.SZ': {'name': '通富微电', 'exchange': '主板'},
                }
            },
            '电子布': {
                'desc': '玻璃纤维布',
                'leaders': {
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                    '601965.SH': {'name': '中国汽研', 'exchange': '主板'},
                    '600699.SH': {'name': '均胜电子', 'exchange': '主板'},
                    '002048.SZ': {'name': '宁波华翔', 'exchange': '主板'},
                    '000338.SZ': {'name': '潍柴动力', 'exchange': '主板'},
                }
            },
            '铜箔': {
                'desc': '锂电铜箔、覆铜板',
                'leaders': {
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                    '000878.SZ': {'name': '云南铜业', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                    '603186.SH': {'name': '华正新材', 'exchange': '主板'},
                    '002288.SZ': {'name': '超华科技', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 电网设备
    # ============================================
    '电网设备': {
        'desc': '特高压、智能电网',
        'sub_sectors': {
            '特高压': {
                'desc': '特高压输电设备',
                'leaders': {
                    '601179.SH': {'name': '中国西电', 'exchange': '主板'},
                    '600312.SH': {'name': '平高电气', 'exchange': '主板'},
                    '600406.SH': {'name': '国电南瑞', 'exchange': '主板'},
                    '002028.SZ': {'name': '思源电气', 'exchange': '主板'},
                    '600089.SH': {'name': '特变电工', 'exchange': '主板'},
                }
            },
            '智能电网': {
                'desc': '配电自动化',
                'leaders': {
                    '600406.SH': {'name': '国电南瑞', 'exchange': '主板'},
                    '002028.SZ': {'name': '思源电气', 'exchange': '主板'},
                    '600312.SH': {'name': '平高电气', 'exchange': '主板'},
                    '601179.SH': {'name': '中国西电', 'exchange': '主板'},
                    '002450.SZ': {'name': '康得新', 'exchange': '主板'},
                }
            },
            '储能': {
                'desc': '电化学储能',
                'leaders': {
                    '002594.SZ': {'name': '比亚迪', 'exchange': '主板'},
                    '002074.SZ': {'name': '国轩高科', 'exchange': '主板'},
                    '300750.SZ': {'name': '宁德时代', 'exchange': '创业板'},
                    '002460.SZ': {'name': '赣锋锂业', 'exchange': '主板'},
                    '002466.SZ': {'name': '天齐锂业', 'exchange': '主板'},
                }
            },
            '变压器': {
                'desc': '电力变压器',
                'leaders': {
                    '600089.SH': {'name': '特变电工', 'exchange': '主板'},
                    '601179.SH': {'name': '中国西电', 'exchange': '主板'},
                    '002028.SZ': {'name': '思源电气', 'exchange': '主板'},
                    '600312.SH': {'name': '平高电气', 'exchange': '主板'},
                    '002534.SZ': {'name': '杭锅股份', 'exchange': '主板'},
                }
            },
            '电线电缆': {
                'desc': '电力电缆',
                'leaders': {
                    '600487.SH': {'name': '亨通光电', 'exchange': '主板'},
                    '601869.SH': {'name': '长飞光纤', 'exchange': '主板'},
                    '002491.SZ': {'name': '通鼎互联', 'exchange': '主板'},
                    '600973.SH': {'name': '宝胜股份', 'exchange': '主板'},
                    '000682.SZ': {'name': '东方电子', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 氦气（稀缺资源）
    # ============================================
    '氦气': {
        'desc': '稀有气体，半导体/航天',
        'sub_sectors': {
            '氦气资源': {
                'desc': '氦气开采',
                'leaders': {
                    '601969.SH': {'name': '海南矿业', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                    '000831.SZ': {'name': '中国稀土', 'exchange': '主板'},
                }
            },
            '稀有气体': {
                'desc': '氖气、氪气、氙气',
                'leaders': {
                    '601969.SH': {'name': '海南矿业', 'exchange': '主板'},
                    '600497.SH': {'name': '驰宏锌锗', 'exchange': '主板'},
                    '600111.SH': {'name': '北方稀土', 'exchange': '主板'},
                    '601168.SH': {'name': '西部矿业', 'exchange': '主板'},
                    '002176.SZ': {'name': '江特电机', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 新能源（绿电）
    # ============================================
    '新能源': {
        'desc': '锂电+光伏+绿电',
        'sub_sectors': {
            '锂电': {
                'desc': '动力电池',
                'leaders': {
                    '002594.SZ': {'name': '比亚迪', 'exchange': '主板'},
                    '300750.SZ': {'name': '宁德时代', 'exchange': '创业板'},
                    '002460.SZ': {'name': '赣锋锂业', 'exchange': '主板'},
                    '002466.SZ': {'name': '天齐锂业', 'exchange': '主板'},
                    '002074.SZ': {'name': '国轩高科', 'exchange': '主板'},
                }
            },
            '光伏': {
                'desc': '光伏产业链',
                'leaders': {
                    '601012.SH': {'name': '隆基绿能', 'exchange': '主板'},
                    '600438.SH': {'name': '通威股份', 'exchange': '主板'},
                    '002459.SZ': {'name': '晶澳科技', 'exchange': '主板'},
                    '601919.SH': {'name': '中远海控', 'exchange': '主板'},
                    '600900.SH': {'name': '长江电力', 'exchange': '主板'},
                }
            },
            '绿电': {
                'desc': '风电+水电+核电',
                'leaders': {
                    '600900.SH': {'name': '长江电力', 'exchange': '主板'},
                    '601615.SH': {'name': '明阳智能', 'exchange': '主板'},
                    '002202.SZ': {'name': '金风科技', 'exchange': '主板'},
                    '600905.SH': {'name': '三峡能源', 'exchange': '主板'},
                    '601985.SH': {'name': '中国核电', 'exchange': '主板'},
                }
            },
            '风电': {
                'desc': '风电设备',
                'leaders': {
                    '601615.SH': {'name': '明阳智能', 'exchange': '主板'},
                    '002202.SZ': {'name': '金风科技', 'exchange': '主板'},
                    '600905.SH': {'name': '三峡能源', 'exchange': '主板'},
                    '601016.SH': {'name': '节能风电', 'exchange': '主板'},
                    '600483.SH': {'name': '福能股份', 'exchange': '主板'},
                }
            },
            '储能': {
                'desc': '储能系统',
                'leaders': {
                    '300750.SZ': {'name': '宁德时代', 'exchange': '创业板'},
                    '002074.SZ': {'name': '国轩高科', 'exchange': '主板'},
                    '002460.SZ': {'name': '赣锋锂业', 'exchange': '主板'},
                    '002594.SZ': {'name': '比亚迪', 'exchange': '主板'},
                    '600406.SH': {'name': '国电南瑞', 'exchange': '主板'},
                }
            },
        }
    },
    
    # ============================================
    # 存储
    # ============================================
    '存储': {
        'desc': 'HBM+国产存储',
        'sub_sectors': {
            '存储芯片': {
                'desc': 'DRAM+NAND',
                'leaders': {
                    '603986.SH': {'name': '兆易创新', 'exchange': '主板'},
                    '688008.SH': {'name': '澜起科技', 'exchange': '科创板'},
                    '300223.SZ': {'name': '北京君正', 'exchange': '创业板'},
                    '688123.SH': {'name': '聚辰股份', 'exchange': '科创板'},
                    '002049.SZ': {'name': '紫光国微', 'exchange': '主板'},
                }
            },
            'HBM': {
                'desc': '高带宽内存',
                'leaders': {
                    '688008.SH': {'name': '澜起科技', 'exchange': '科创板'},
                    '603986.SH': {'name': '兆易创新', 'exchange': '主板'},
                    '688123.SH': {'name': '聚辰股份', 'exchange': '科创板'},
                    '002049.SZ': {'name': '紫光国微', 'exchange': '主板'},
                    '300223.SZ': {'name': '北京君正', 'exchange': '创业板'},
                }
            },
            '存储模组': {
                'desc': '模组+主控',
                'leaders': {
                    '688123.SH': {'name': '聚辰股份', 'exchange': '科创板'},
                    '300782.SZ': {'name': '卓胜微', 'exchange': '创业板'},
                    '002049.SZ': {'name': '紫光国微', 'exchange': '主板'},
                    '603986.SH': {'name': '兆易创新', 'exchange': '主板'},
                    '688008.SH': {'name': '澜起科技', 'exchange': '科创板'},
                }
            },
        }
    },
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


def get_stock_count() -> dict:
    """获取各板块股票数量统计"""
    stats = {}
    for sector, sector_info in HOT_SECTOR_CONFIG.items():
        stats[sector] = {
            'desc': sector_info['desc'],
            'sub_sectors': {}
        }
        for sub_sector, sub_info in sector_info['sub_sectors'].items():
            stats[sector]['sub_sectors'][sub_sector] = {
                'desc': sub_info['desc'],
                'count': len(sub_info['leaders'])
            }
    return stats


def print_sector_config():
    """打印板块配置"""
    stats = get_stock_count()
    
    print("=" * 80)
    print("2025-2026年热门板块及子板块龙头股配置（AI硬件供应链）")
    print("数据时间: 2024-01-01 至 2026-06-14")
    print("=" * 80)
    
    total_stocks = 0
    total_sub_sectors = 0
    
    for sector, info in stats.items():
        sub_count = len(info['sub_sectors'])
        total_sub_sectors += sub_count
        
        print(f"\n📊 {sector} - {info['desc']} ({sub_count}个子板块)")
        print("-" * 60)
        
        for sub_sector, sub_info in info['sub_sectors'].items():
            count = sub_info['count']
            total_stocks += count
            leaders = list(HOT_SECTOR_CONFIG[sector]['sub_sectors'][sub_sector]['leaders'].items())
            
            print(f"  📁 {sub_sector} ({sub_info['desc']}) - {count}只")
            
            # 每行显示3只
            for i in range(0, len(leaders), 3):
                row = leaders[i:i+3]
                line = "    "
                for code, info in row:
                    exchange_mark = "🅰️" if info['exchange'] == '主板' else "🅱️" if info['exchange'] == '创业板' else "🅲"
                    line += f"{exchange_mark} {code} {info['name']} | "
                print(line.rstrip(" |"))
    
    print("\n" + "=" * 80)
    print(f"主板龙头股统计:")
    print(f"  板块数量: {len(HOT_SECTOR_CONFIG)} 个")
    print(f"  子板块数量: {total_sub_sectors} 个")
    print(f"  主板龙头股: {len(get_main_board_leaders())} 只")
    print("=" * 80)


if __name__ == '__main__':
    print_sector_config()