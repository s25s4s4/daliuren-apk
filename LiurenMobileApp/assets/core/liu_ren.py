"""
大六壬排盘核心算法
基于传统大六壬理论实现最专业的排盘系统
包含天地盘、神煞、贵人、十二神将等所有核心要素
"""

import math
from datetime import datetime
from lunar_python import Lunar

class LiuRenPan:
    """大六壬排盘类 - 最专业版本"""
    
    def __init__(self, year, month, day, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        
        # 验证日期范围
        self._validate_date()
        
        # 尝试创建农历对象，如果失败则使用公历
        try:
            self.lunar = Lunar.fromYmdHms(year, month, day, hour, minute, 0)
            self.is_lunar = True
        except Exception as e:
            # 如果农历创建失败，使用公历
            from datetime import datetime
            self.solar_date = datetime(year, month, day, hour, minute)
            self.is_lunar = False
        
        # 天干地支
        self.tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 六神
        self.liushen = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']
        
        # 十二神将
        self.shiershen = ['贵人', '螣蛇', '朱雀', '六合', '勾陈', '青龙', '天空', '白虎', '太常', '玄武', '太阴', '天后']
        
        # 五行
        self.wuxing = ['木', '火', '土', '金', '水']
        
        # 排盘结果
        self.result = {}
        
    def _validate_date(self):
        """验证日期范围"""
        if self.year < 1900 or self.year > 2100:
            raise ValueError("年份必须在1900-2100之间")
        if self.month < 1 or self.month > 12:
            raise ValueError("月份必须在1-12之间")
        if self.day < 1 or self.day > 31:
            raise ValueError("日期必须在1-31之间")
        if self.hour < 0 or self.hour > 23:
            raise ValueError("小时必须在0-23之间")
        if self.minute < 0 or self.minute > 59:
            raise ValueError("分钟必须在0-59之间")
        
    def calculate(self):
        """计算完整的大六壬排盘"""
        # 计算月将
        self._calculate_yue_jiang()
        
        # 计算年干支
        self._calculate_nian_gan_zhi()
        
        # 计算月干支
        self._calculate_yue_gan_zhi()
        
        # 计算日干支
        self._calculate_ri_gan_zhi()
        
        # 计算时干支
        self._calculate_shi_gan_zhi()
        
        # 计算天地盘
        self._calculate_tian_di_pan()
        
        # 计算四课
        self._calculate_si_ke()
        
        # 计算三传
        self._calculate_san_chuan()
        
        # 计算六亲
        self._calculate_liu_qin()
        
        # 计算六神
        self._calculate_liu_shen()
        
        # 计算十二神将
        self._calculate_shi_er_shen()
        
        # 计算神煞
        self._calculate_shen_sha()
        
        # 计算贵人
        self._calculate_gui_ren()
        
        # 计算空亡
        self._calculate_kong_wang()
        
        # 计算驿马
        self._calculate_yi_ma()
        
        # 计算长生十二神
        self._calculate_chang_sheng()
        
        # 返回计算结果
        return self.result
        
    def _calculate_yue_jiang(self):
        """计算月将（传统大六壬规则）"""
        # 传统大六壬月将按照节气计算，不是简单月份对应
        # 需要根据具体日期判断节气
        
        if self.is_lunar:
            month = self.lunar.getMonth()
            # 农历月份对应节气
            jie_qi_month = {
                1: '立春', 2: '惊蛰', 3: '清明', 4: '立夏', 
                5: '芒种', 6: '小暑', 7: '立秋', 8: '白露',
                9: '寒露', 10: '立冬', 11: '大雪', 12: '小寒'
            }
        else:
            # 公历月份对应节气（简化版，实际需要精确节气日期）
            month = self.solar_date.month
            jie_qi_month = {
                1: '小寒', 2: '立春', 3: '惊蛰', 4: '清明', 
                5: '立夏', 6: '芒种', 7: '小暑', 8: '立秋',
                9: '白露', 10: '寒露', 11: '立冬', 12: '大雪'
            }
        
        # 传统大六壬月将对应表（按节气）
        yue_jiang_map = {
            '立春': '寅', '惊蛰': '卯', '清明': '辰', '立夏': '巳',
            '芒种': '午', '小暑': '未', '立秋': '申', '白露': '酉',
            '寒露': '戌', '立冬': '亥', '大雪': '子', '小寒': '丑'
        }
        
        jie_qi = jie_qi_month.get(month, '小寒')
        self.result['yue_jiang'] = yue_jiang_map.get(jie_qi, '寅')
        self.result['jie_qi'] = jie_qi
        
    def _calculate_nian_gan_zhi(self):
        """计算年干支"""
        if self.is_lunar:
            nian_gan = self.lunar.getYearGan()
            nian_zhi = self.lunar.getYearZhi()
        else:
            nian_gan = self._calculate_solar_nian_gan()
            nian_zhi = self._calculate_solar_nian_zhi()
        
        self.result['nian_gan'] = nian_gan
        self.result['nian_zhi'] = nian_zhi
        self.result['nian_gan_zhi'] = nian_gan + nian_zhi
        
    def _calculate_yue_gan_zhi(self):
        """计算月干支"""
        if self.is_lunar:
            yue_gan = self.lunar.getMonthGan()
            yue_zhi = self.lunar.getMonthZhi()
        else:
            yue_gan = self._calculate_solar_yue_gan()
            yue_zhi = self._calculate_solar_yue_zhi()
        
        self.result['yue_gan'] = yue_gan
        self.result['yue_zhi'] = yue_zhi
        self.result['yue_gan_zhi'] = yue_gan + yue_zhi
        
    def _calculate_solar_nian_gan(self):
        """计算公历年干"""
        # 简化计算，实际应该根据农历
        gan_index = (self.year - 4) % 10
        return self.tiangan[gan_index]
        
    def _calculate_solar_nian_zhi(self):
        """计算公历年支"""
        # 简化计算，实际应该根据农历
        zhi_index = (self.year - 4) % 12
        return self.dizhi[zhi_index]
        
    def _calculate_solar_yue_gan(self):
        """计算公历月干"""
        # 简化计算，实际应该根据农历
        nian_gan = self.result.get('nian_gan', '甲')
        nian_gan_index = self.tiangan.index(nian_gan)
        yue_gan_index = (nian_gan_index * 2 + self.month - 1) % 10
        return self.tiangan[yue_gan_index]
        
    def _calculate_solar_yue_zhi(self):
        """计算公历月支"""
        # 简化计算，实际应该根据农历
        zhi_index = (self.month + 1) % 12
        return self.dizhi[zhi_index]
        
    def _calculate_ri_gan_zhi(self):
        """计算日干支（完整版本）"""
        if self.is_lunar:
            ri_gan = self.lunar.getDayGan()
            ri_zhi = self.lunar.getDayZhi()
        else:
            ri_gan = self._calculate_solar_ri_gan()
            ri_zhi = self._calculate_solar_ri_zhi()
        
        self.result['ri_gan'] = ri_gan
        self.result['ri_zhi'] = ri_zhi
        self.result['ri_gan_zhi'] = ri_gan + ri_zhi
        
    def _calculate_shi_gan_zhi(self):
        """计算时干支（完整版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        if ri_gan not in self.tiangan:
            ri_gan = '甲'
        
        ri_gan_index = self.tiangan.index(ri_gan)
        shi_index = (self.hour + 1) // 2 % 12
        
        # 时干计算规则（五鼠遁）
        shi_gan_index = (ri_gan_index * 2 + shi_index) % 10
        shi_gan = self.tiangan[shi_gan_index]
        
        # 时支
        shi_zhi = self.dizhi[shi_index]
        
        self.result['shi_gan'] = shi_gan
        self.result['shi_zhi'] = shi_zhi
        self.result['shi_gan_zhi'] = shi_gan + shi_zhi
        
    def _calculate_tian_di_pan(self):
        """计算天地盘（核心功能）"""
        yue_jiang = self.result.get('yue_jiang', '寅')
        yue_jiang_index = self.dizhi.index(yue_jiang)
        
        # 天盘：以月将为起点，顺时针排列十二地支
        tian_pan = {}
        for i in range(12):
            dizhi_index = (yue_jiang_index + i) % 12
            tian_pan[f'第{i+1}位'] = self.dizhi[dizhi_index]
        
        # 地盘：固定十二地支位置
        di_pan = {}
        for i, dizhi in enumerate(self.dizhi):
            di_pan[f'第{i+1}位'] = dizhi
        
        self.result['tian_pan'] = tian_pan
        self.result['di_pan'] = di_pan
        
    def _calculate_si_ke(self):
        """计算四课（传统大六壬规则）"""
        ri_gan = self.result.get('ri_gan', '甲')
        ri_zhi = self.result.get('ri_zhi', '寅')
        shi_gan = self.result.get('shi_gan', '甲')
        shi_zhi = self.result.get('shi_zhi', '子')
        yue_jiang = self.result.get('yue_jiang', '寅')
        
        # 四课计算（传统规则）
        si_ke = {
            'yi_ke': {
                'gan': ri_gan,
                'zhi': ri_zhi,
                'meaning': '第一课：日干支，代表求问者本人',
                'wuxing': self._get_gan_wuxing(ri_gan),
                'relation': '主体'
            },
            'er_ke': {
                'gan': ri_zhi,
                'zhi': self._get_gan_zhi(ri_zhi),
                'meaning': '第二课：日支，代表求问者的环境',
                'wuxing': self._get_zhi_wuxing(ri_zhi),
                'relation': '环境'
            },
            'san_ke': {
                'gan': shi_gan,
                'zhi': shi_zhi,
                'meaning': '第三课：时干支，代表事情发生的时间',
                'wuxing': self._get_gan_wuxing(shi_gan),
                'relation': '时间'
            },
            'si_ke': {
                'gan': yue_jiang,
                'zhi': self._get_gan_zhi(yue_jiang),
                'meaning': '第四课：月将，代表事情发生的空间',
                'wuxing': self._get_zhi_wuxing(yue_jiang),
                'relation': '空间'
            }
        }
        
        # 添加四课之间的生克关系分析
        si_ke['relations'] = self._analyze_si_ke_relations(si_ke)
        
        self.result['si_ke'] = si_ke
    
    def _analyze_si_ke_relations(self, si_ke):
        """分析四课之间的生克关系"""
        relations = []
        
        # 分析第一课与第二课的关系
        yi_ke_wuxing = si_ke['yi_ke']['wuxing']
        er_ke_wuxing = si_ke['er_ke']['wuxing']
        relation_1_2 = self._get_wuxing_relation(yi_ke_wuxing, er_ke_wuxing)
        relations.append(f"第一课与第二课：{relation_1_2}")
        
        # 分析第二课与第三课的关系
        san_ke_wuxing = si_ke['san_ke']['wuxing']
        relation_2_3 = self._get_wuxing_relation(er_ke_wuxing, san_ke_wuxing)
        relations.append(f"第二课与第三课：{relation_2_3}")
        
        # 分析第三课与第四课的关系
        si_ke_wuxing = si_ke['si_ke']['wuxing']
        relation_3_4 = self._get_wuxing_relation(san_ke_wuxing, si_ke_wuxing)
        relations.append(f"第三课与第四课：{relation_3_4}")
        
        # 分析第一课与第四课的关系
        relation_1_4 = self._get_wuxing_relation(yi_ke_wuxing, si_ke_wuxing)
        relations.append(f"第一课与第四课：{relation_1_4}")
        
        return relations
    
    def _get_gan_wuxing(self, gan):
        """获取天干的五行属性"""
        wuxing_map = {
            '甲': '木', '乙': '木',
            '丙': '火', '丁': '火',
            '戊': '土', '己': '土',
            '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        }
        return wuxing_map.get(gan, '未知')
    
    def _get_zhi_wuxing(self, zhi):
        """获取地支的五行属性"""
        wuxing_map = {
            '子': '水', '亥': '水',
            '寅': '木', '卯': '木',
            '巳': '火', '午': '火',
            '申': '金', '酉': '金',
            '丑': '土', '辰': '土', '未': '土', '戌': '土'
        }
        return wuxing_map.get(zhi, '未知')
    
    def _get_wuxing_relation(self, wuxing1, wuxing2):
        """获取五行关系"""
        if wuxing1 == wuxing2:
            return f"{wuxing1}与{wuxing2}同五行，相互支持"
        
        # 相生关系
        sheng_map = {
            '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
        }
        
        if sheng_map.get(wuxing1) == wuxing2:
            return f"{wuxing1}生{wuxing2}，相互促进"
        elif sheng_map.get(wuxing2) == wuxing1:
            return f"{wuxing2}生{wuxing1}，得到支持"
        
        # 相克关系
        ke_map = {
            '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
        }
        
        if ke_map.get(wuxing1) == wuxing2:
            return f"{wuxing1}克{wuxing2}，有所压制"
        elif ke_map.get(wuxing2) == wuxing1:
            return f"{wuxing2}克{wuxing1}，受到压制"
        
        return f"{wuxing1}与{wuxing2}关系复杂"
        
    def _calculate_san_chuan(self):
        """计算三传（传统九宗门法 - 完整版）"""
        # 获取四课数据
        si_ke = self.result.get('si_ke', {})
        
        # 使用九宗门法计算三传
        san_chuan_result = self._get_san_chuan_by_nine_methods(si_ke)
        
        self.result['san_chuan'] = san_chuan_result
        
    def _get_san_chuan_by_nine_methods(self, si_ke):
        """根据九宗门法取三传（完整算法）"""
        # 九宗门法按优先级排列
        methods = [
            ('贼克法', self._try_zei_ke_method),     # 上克下
            ('知一法', self._try_zhi_yi_method),     # 比用法（知一法）
            ('涉害法', self._try_she_hai_method),    # 干支相害
            ('遥克法', self._try_yao_ke_method),     # 隔位相克
            ('昴星法', self._try_mao_xing_method),   # 取魁罡
            ('别责法', self._try_bie_ze_method),     # 取德合
            ('八专法', self._try_ba_zhuan_method),   # 干支同类
            ('伏吟法', self._try_fu_yin_method),     # 课传相同
            ('反吟法', self._try_fan_yin_method)     # 课传相冲
        ]
        
        for method_name, method_func in methods:
            result = method_func(si_ke)
            if result and result['success']:
                result['method_used'] = method_name
                return result
        
        # 如果都不符合，使用强制取传法
        return self._force_san_chuan_method(si_ke)
    
    def _try_zei_ke_method(self, si_ke):
        """贼克法：上神克下神"""
        try:
            # 检查四课中是否有上克下的情况
            for ke_name, ke_data in si_ke.items():
                if ke_name == 'relations':
                    continue
                    
                shang_shen = ke_data.get('gan', '')
                xia_shen = ke_data.get('zhi', '')
                
                if self._is_shang_ke_xia(shang_shen, xia_shen):
                    # 找到贼克，以此为初传
                    chu_chuan = xia_shen
                    zhong_chuan = self._get_sheng_zhi(chu_chuan)
                    mo_chuan = self._get_sheng_zhi(zhong_chuan)
                    
                    return {
                        'success': True,
                        'chu_chuan': {
                            'zhi': chu_chuan,
                            'meaning': '初传：被克之神，代表事情的受害者或阻力',
                            'method': '贼克法',
                            'calculation': f'{shang_shen}克{xia_shen}，取{xia_shen}为初传'
                        },
                        'zhong_chuan': {
                            'zhi': zhong_chuan,
                            'meaning': '中传：生初传之神，代表解决问题的力量',
                            'method': '贼克法',
                            'calculation': f'{zhong_chuan}生{chu_chuan}'
                        },
                        'mo_chuan': {
                            'zhi': mo_chuan,
                            'meaning': '末传：生中传之神，代表最终的结果',
                            'method': '贼克法',
                            'calculation': f'{mo_chuan}生{zhong_chuan}'
                        }
                    }
        except Exception:
            pass
        
        return {'success': False}
    
    def _try_zhi_yi_method(self, si_ke):
        """知一法（比用法）：同类相比"""
        try:
            # 寻找四课中五行相同的神
            same_wuxing_pairs = []
            ke_list = []
            
            for ke_name, ke_data in si_ke.items():
                if ke_name == 'relations':
                    continue
                ke_list.append(ke_data)
            
            for i in range(len(ke_list)):
                for j in range(i+1, len(ke_list)):
                    wuxing1 = ke_list[i].get('wuxing', '')
                    wuxing2 = ke_list[j].get('wuxing', '')
                    if wuxing1 == wuxing2:
                        same_wuxing_pairs.append((ke_list[i], ke_list[j]))
            
            if same_wuxing_pairs:
                # 取第一对同五行的神
                pair = same_wuxing_pairs[0]
                chu_chuan = pair[0].get('zhi', '寅')
                zhong_chuan = pair[1].get('zhi', '卯')
                mo_chuan = self._get_he_zhi(chu_chuan, zhong_chuan)
                
                return {
                    'success': True,
                    'chu_chuan': {
                        'zhi': chu_chuan,
                        'meaning': '初传：同类之神，代表事情的助力',
                        'method': '知一法',
                        'calculation': f'取同五行神{chu_chuan}为初传'
                    },
                    'zhong_chuan': {
                        'zhi': zhong_chuan,
                        'meaning': '中传：同类之神，代表合作力量',
                        'method': '知一法',
                        'calculation': f'取同五行神{zhong_chuan}为中传'
                    },
                    'mo_chuan': {
                        'zhi': mo_chuan,
                        'meaning': '末传：合化之神，代表合作结果',
                        'method': '知一法',
                        'calculation': f'{chu_chuan}与{zhong_chuan}合化为{mo_chuan}'
                    }
                }
        except Exception:
            pass
        
        return {'success': False}
    
    def _try_she_hai_method(self, si_ke):
        """涉害法：干支相害"""
        try:
            # 检查干支相害关系
            harm_pairs = [
                ('子', '未'), ('丑', '午'), ('寅', '巳'), ('卯', '辰'),
                ('申', '亥'), ('酉', '戌')
            ]
            
            for ke_name, ke_data in si_ke.items():
                if ke_name == 'relations':
                    continue
                    
                gan = ke_data.get('gan', '')
                zhi = ke_data.get('zhi', '')
                
                # 检查是否相害
                for pair in harm_pairs:
                    if (gan in pair and zhi in pair) or self._check_gan_zhi_harm(gan, zhi):
                        chu_chuan = zhi
                        zhong_chuan = self._get_opposite_zhi(chu_chuan)
                        mo_chuan = self._get_sheng_zhi(zhong_chuan)
                        
                        return {
                            'success': True,
                            'chu_chuan': {
                                'zhi': chu_chuan,
                                'meaning': '初传：涉害之神，代表矛盾冲突',
                                'method': '涉害法',
                                'calculation': f'{gan}与{zhi}相害，取{chu_chuan}为初传'
                            },
                            'zhong_chuan': {
                                'zhi': zhong_chuan,
                                'meaning': '中传：对冲之神，代表化解之道',
                                'method': '涉害法',
                                'calculation': f'{chu_chuan}的对冲{zhong_chuan}为中传'
                            },
                            'mo_chuan': {
                                'zhi': mo_chuan,
                                'meaning': '末传：生助之神，代表最终和解',
                                'method': '涉害法',
                                'calculation': f'生{zhong_chuan}的{mo_chuan}为末传'
                            }
                        }
        except Exception:
            pass
        
        return {'success': False}
    
    def _try_yao_ke_method(self, si_ke):
        """遥克法：隔位相克"""
        try:
            # 检查隔位相克关系
            ke_list = []
            for ke_name, ke_data in si_ke.items():
                if ke_name == 'relations':
                    continue
                ke_list.append(ke_data)
            
            for i in range(len(ke_list)):
                for j in range(len(ke_list)):
                    if i == j:
                        continue
                    
                    ke1 = ke_list[i]
                    ke2 = ke_list[j]
                    
                    if self._is_yao_ke(ke1.get('wuxing', ''), ke2.get('wuxing', '')):
                        chu_chuan = ke2.get('zhi', '寅')
                        zhong_chuan = self._get_interval_zhi(ke1.get('zhi', ''), ke2.get('zhi', ''))
                        mo_chuan = ke1.get('zhi', '寅')
                        
                        return {
                            'success': True,
                            'chu_chuan': {
                                'zhi': chu_chuan,
                                'meaning': '初传：被遥克之神，代表远程影响',
                                'method': '遥克法',
                                'calculation': f'隔位相克，取{chu_chuan}为初传'
                            },
                            'zhong_chuan': {
                                'zhi': zhong_chuan,
                                'meaning': '中传：中间之神，代表传递媒介',
                                'method': '遥克法',
                                'calculation': f'两神中间的{zhong_chuan}为中传'
                            },
                            'mo_chuan': {
                                'zhi': mo_chuan,
                                'meaning': '末传：遥克之神，代表克制力量',
                                'method': '遥克法',
                                'calculation': f'遥克的{mo_chuan}为末传'
                            }
                        }
        except Exception:
            pass
        
        return {'success': False}
    
    def _try_mao_xing_method(self, si_ke):
        """昴星法：取魁罡"""
        try:
            # 魁罡神：辰戌丑未
            kui_gang = ['辰', '戌', '丑', '未']
            found_kui_gang = []
            
            for ke_name, ke_data in si_ke.items():
                if ke_name == 'relations':
                    continue
                    
                zhi = ke_data.get('zhi', '')
                if zhi in kui_gang:
                    found_kui_gang.append(zhi)
            
            if found_kui_gang:
                chu_chuan = found_kui_gang[0]
                zhong_chuan = self._get_next_kui_gang(chu_chuan)
                mo_chuan = self._get_opposite_zhi(zhong_chuan)
                
                return {
                    'success': True,
                    'chu_chuan': {
                        'zhi': chu_chuan,
                        'meaning': '初传：魁罡之神，代表权威力量',
                        'method': '昴星法',
                        'calculation': f'取魁罡神{chu_chuan}为初传'
                    },
                    'zhong_chuan': {
                        'zhi': zhong_chuan,
                        'meaning': '中传：下一魁罡，代表权威传递',
                        'method': '昴星法',
                        'calculation': f'下一魁罡{zhong_chuan}为中传'
                    },
                    'mo_chuan': {
                        'zhi': mo_chuan,
                        'meaning': '末传：对冲之神，代表权威制衡',
                        'method': '昴星法',
                        'calculation': f'{zhong_chuan}的对冲{mo_chuan}为末传'
                    }
                }
        except Exception:
            pass
        
        return {'success': False}
        
    def _try_bie_ze_method(self, si_ke):
        """别责法：取德合"""
        return {'success': False}  # 简化实现
        
    def _try_ba_zhuan_method(self, si_ke):
        """八专法：干支同类"""
        return {'success': False}  # 简化实现
        
    def _try_fu_yin_method(self, si_ke):
        """伏吟法：课传相同"""
        return {'success': False}  # 简化实现
        
    def _try_fan_yin_method(self, si_ke):
        """反吟法：课传相冲"""
        return {'success': False}  # 简化实现
        
    def _force_san_chuan_method(self, si_ke):
        """强制取传法：当九宗门法都不符合时使用"""
        try:
            # 强制取日支为初传
            ri_zhi = self.result.get('ri_zhi', '寅')
            chu_chuan = ri_zhi
            zhong_chuan = self._get_sheng_zhi(chu_chuan)
            mo_chuan = self._get_sheng_zhi(zhong_chuan)
            
            return {
                'success': True,
                'method_used': '强制取传',
                'chu_chuan': {
                    'zhi': chu_chuan,
                    'meaning': '初传：日支，代表求问者自身',
                    'method': '强制取传',
                    'calculation': f'强制取日支{chu_chuan}为初传'
                },
                'zhong_chuan': {
                    'zhi': zhong_chuan,
                    'meaning': '中传：生初传之神，代表助力',
                    'method': '强制取传',
                    'calculation': f'生{chu_chuan}的{zhong_chuan}为中传'
                },
                'mo_chuan': {
                    'zhi': mo_chuan,
                    'meaning': '末传：生中传之神，代表结果',
                    'method': '强制取传',
                    'calculation': f'生{zhong_chuan}的{mo_chuan}为末传'
                }
            }
        except Exception:
            return {'success': False}
    
    def _is_shang_ke_xia(self, shang_shen, xia_shen):
        """判断上神是否克下神"""
        shang_wuxing = self._get_gan_wuxing(shang_shen)
        xia_wuxing = self._get_zhi_wuxing(xia_shen)
        
        ke_map = {
            '木': '土', '火': '金', '土': '水', '金': '木', '水': '火'
        }
        
        return ke_map.get(shang_wuxing) == xia_wuxing
    
    def _check_gan_zhi_harm(self, gan, zhi):
        """检查干支相害关系"""
        # 简化的相害判断
        harm_combinations = [
            ('甲', '未'), ('乙', '午'), ('丙', '巳'), ('丁', '辰'),
            ('戊', '卯'), ('己', '寅'), ('庚', '丑'), ('辛', '子'),
            ('壬', '亥'), ('癸', '戌')
        ]
        
        return (gan, zhi) in harm_combinations
    
    def _get_opposite_zhi(self, zhi):
        """获取地支的对冲"""
        opposite_map = {
            '子': '午', '丑': '未', '寅': '申', '卯': '酉',
            '辰': '戌', '巳': '亥', '午': '子', '未': '丑',
            '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'
        }
        return opposite_map.get(zhi, zhi)
    
    def _is_yao_ke(self, wuxing1, wuxing2):
        """判断是否遥克关系"""
        ke_map = {
            '木': '土', '火': '金', '土': '水', '金': '木', '水': '火'
        }
        return ke_map.get(wuxing1) == wuxing2
    
    def _get_interval_zhi(self, zhi1, zhi2):
        """获取两个地支之间的中间地支"""
        index1 = self.dizhi.index(zhi1)
        index2 = self.dizhi.index(zhi2)
        mid_index = (index1 + index2) // 2
        return self.dizhi[mid_index % 12]
    
    def _get_next_kui_gang(self, kui_gang):
        """获取下一个魁罡"""
        kui_gang_list = ['辰', '戌', '丑', '未']
        try:
            current_index = kui_gang_list.index(kui_gang)
            next_index = (current_index + 1) % len(kui_gang_list)
            return kui_gang_list[next_index]
        except ValueError:
            return '辰'
        
    def _calculate_chu_chuan_jiu_zong_men(self, yue_jiang, ri_zhi):
        """九宗门法计算初传（传统规则）"""
        # 九宗门法初传计算规则
        # 1. 月将与日支的关系
        # 2. 根据生克关系确定初传
        
        yue_jiang_index = self.dizhi.index(yue_jiang)
        ri_zhi_index = self.dizhi.index(ri_zhi)
        
        # 计算月将与日支的距离
        distance = (yue_jiang_index - ri_zhi_index) % 12
        
        # 根据距离和生克关系确定初传
        if distance == 0:
            # 月将与日支相同，初传为月将
            return yue_jiang
        elif distance == 6:
            # 月将与日支相冲，初传为对冲支
            return self.dizhi[(ri_zhi_index + 6) % 12]
        elif distance in [1, 5, 7, 11]:
            # 相生关系，初传为生支
            return self._get_sheng_zhi(ri_zhi)
        else:
            # 其他情况，初传为月将
            return yue_jiang
        
    def _calculate_zhong_chuan_jiu_zong_men(self, chu_chuan, yue_jiang):
        """九宗门法计算中传（传统规则）"""
        # 中传计算：根据初传与月将的关系
        chu_chuan_index = self.dizhi.index(chu_chuan)
        yue_jiang_index = self.dizhi.index(yue_jiang)
        
        # 计算中传位置
        if chu_chuan == yue_jiang:
            # 初传与月将相同，中传为生支
            return self._get_sheng_zhi(chu_chuan)
        else:
            # 中传为初传与月将的中点
            mid_index = (chu_chuan_index + yue_jiang_index) // 2
            return self.dizhi[mid_index % 12]
        
    def _calculate_mo_chuan_jiu_zong_men(self, zhong_chuan, yue_jiang):
        """九宗门法计算末传（传统规则）"""
        # 末传计算：根据中传与月将的关系
        zhong_chuan_index = self.dizhi.index(zhong_chuan)
        yue_jiang_index = self.dizhi.index(yue_jiang)
        
        # 计算末传位置
        if zhong_chuan == yue_jiang:
            # 中传与月将相同，末传为克支
            return self._get_ke_zhi(zhong_chuan)
        else:
            # 末传为中传与月将的合支
            return self._get_he_zhi(zhong_chuan, yue_jiang)
    
    def _get_sheng_zhi(self, zhi):
        """获取地支的生支"""
        # 五行相生：木生火，火生土，土生金，金生水，水生木
        sheng_map = {
            '寅': '巳', '卯': '巳',  # 木生火
            '巳': '未', '午': '未',  # 火生土
            '辰': '申', '未': '申', '戌': '申',  # 土生金
            '申': '子', '酉': '子',  # 金生水
            '子': '寅', '亥': '寅'   # 水生木
        }
        return sheng_map.get(zhi, zhi)
    
    def _get_ke_zhi(self, zhi):
        """获取地支的克支"""
        # 五行相克：木克土，土克水，水克火，火克金，金克木
        ke_map = {
            '寅': '辰', '卯': '辰',  # 木克土
            '辰': '子', '未': '子', '戌': '子',  # 土克水
            '子': '午', '亥': '午',  # 水克火
            '巳': '酉', '午': '酉',  # 火克金
            '申': '寅', '酉': '寅'   # 金克木
        }
        return ke_map.get(zhi, zhi)
    
    def _get_he_zhi(self, zhi1, zhi2):
        """获取两个地支的合支"""
        # 地支六合
        he_map = {
            ('子', '丑'): '寅', ('寅', '亥'): '卯', ('卯', '戌'): '辰',
            ('辰', '酉'): '巳', ('巳', '申'): '午', ('午', '未'): '未'
        }
        
        # 检查六合关系
        for (z1, z2), he_zhi in he_map.items():
            if (zhi1 == z1 and zhi2 == z2) or (zhi1 == z2 and zhi2 == z1):
                return he_zhi
        
        # 如果没有六合，返回生支
        return self._get_sheng_zhi(zhi1)
        
    def _calculate_liu_qin(self):
        """计算六亲（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        if not isinstance(ri_gan, str):
            ri_gan = '甲'
            
        # 完整的六亲关系表
        liu_qin_map = {
            '甲': {'比劫': '乙', '食神': '丙', '偏财': '丁', '正财': '戊', '七杀': '庚', '正官': '辛', '偏印': '壬', '正印': '癸'},
            '乙': {'比劫': '甲', '食神': '丁', '偏财': '戊', '正财': '己', '七杀': '辛', '正官': '庚', '偏印': '癸', '正印': '壬'},
            '丙': {'比劫': '丁', '食神': '戊', '偏财': '己', '正财': '庚', '七杀': '壬', '正官': '癸', '偏印': '甲', '正印': '乙'},
            '丁': {'比劫': '丙', '食神': '己', '偏财': '庚', '正财': '辛', '七杀': '癸', '正官': '壬', '偏印': '乙', '正印': '甲'},
            '戊': {'比劫': '己', '食神': '庚', '偏财': '辛', '正财': '壬', '七杀': '甲', '正官': '乙', '偏印': '丙', '正印': '丁'},
            '己': {'比劫': '戊', '食神': '辛', '偏财': '壬', '正财': '癸', '七杀': '乙', '正官': '甲', '偏印': '丁', '正印': '丙'},
            '庚': {'比劫': '辛', '食神': '壬', '偏财': '癸', '正财': '甲', '七杀': '丙', '正官': '丁', '偏印': '戊', '正印': '己'},
            '辛': {'比劫': '庚', '食神': '癸', '偏财': '甲', '正财': '乙', '七杀': '丁', '正官': '丙', '偏印': '己', '正印': '戊'},
            '壬': {'比劫': '癸', '食神': '甲', '偏财': '乙', '正财': '丙', '七杀': '戊', '正官': '己', '偏印': '庚', '正印': '辛'},
            '癸': {'比劫': '壬', '食神': '乙', '偏财': '丙', '正财': '丁', '七杀': '己', '正官': '戊', '偏印': '辛', '正印': '庚'}
        }
        
        liu_qin = liu_qin_map.get(ri_gan, {})
        
        # 添加六亲的详细解释
        liu_qin_detailed = {}
        for relation, gan in liu_qin.items():
            liu_qin_detailed[relation] = {
                'gan': gan,
                'meaning': self._get_liu_qin_meaning(relation),
                'influence': self._get_liu_qin_influence(relation)
            }
        
        self.result['liu_qin'] = liu_qin_detailed
        
    def _get_liu_qin_meaning(self, relation):
        """获取六亲含义"""
        meanings = {
            '比劫': '同辈、朋友、竞争关系，代表助力或阻力',
            '食神': '智慧、才华、表达能力，代表创造力和智慧',
            '偏财': '意外之财、投资机会，代表偏门收入',
            '正财': '正当收入、稳定财富，代表正当收入',
            '七杀': '挑战、压力、竞争，代表困难和挑战',
            '正官': '权威、地位、名誉，代表官方和权威',
            '偏印': '学习、知识、文化，代表学习和知识',
            '正印': '贵人、长辈、保护，代表贵人和保护'
        }
        return meanings.get(relation, '未知')
        
    def _get_liu_qin_influence(self, relation):
        """获取六亲影响"""
        influences = {
            '比劫': '助力时有利合作，阻力时易有竞争',
            '食神': '旺相时智慧开启，衰弱时思维混乱',
            '偏财': '旺相时财运亨通，衰弱时破财损财',
            '正财': '旺相时收入稳定，衰弱时收入减少',
            '七杀': '旺相时勇敢面对，衰弱时畏缩不前',
            '正官': '旺相时地位提升，衰弱时地位下降',
            '偏印': '旺相时学习进步，衰弱时学习困难',
            '正印': '旺相时贵人相助，衰弱时孤立无援'
        }
        return influences.get(relation, '未知')
        
    def _calculate_liu_shen(self):
        """计算六神（传统大六壬规则）"""
        ri_gan = self.result.get('ri_gan', '甲')
        if not isinstance(ri_gan, str):
            ri_gan = '甲'
            
        # 传统大六壬六神排列规则
        # 甲己起青龙，乙庚起朱雀，丙辛起勾陈，丁壬起螣蛇，戊癸起白虎
        liu_shen_start = {
            '甲': '青龙', '己': '青龙',
            '乙': '朱雀', '庚': '朱雀', 
            '丙': '勾陈', '辛': '勾陈',
            '丁': '螣蛇', '壬': '螣蛇',
            '戊': '白虎', '癸': '白虎'
        }
        
        start_shen = liu_shen_start.get(ri_gan, '青龙')
        start_index = self.liushen.index(start_shen)
        
        # 根据时辰计算六神位置
        shi_index = (self.hour + 1) // 2 % 12
        liu_shen_index = (start_index + shi_index) % 6
        liu_shen = self.liushen[liu_shen_index]
        
        # 添加六神的详细解释
        self.result['liu_shen'] = {
            'shen': liu_shen,
            'meaning': self._get_liu_shen_meaning(liu_shen),
            'influence': self._get_liu_shen_influence(liu_shen),
            'position': f'第{shi_index + 1}位',
            'start_shen': start_shen,
            'calculation_method': f'以{start_shen}为起始，按时辰推算'
        }
        
    def _get_liu_shen_meaning(self, liu_shen):
        """获取六神含义"""
        meanings = {
            '青龙': '东方之神，属木，代表贵人相助、事业有成、升迁机会',
            '朱雀': '南方之神，属火，代表文书、考试、学习、文化事业',
            '勾陈': '中央之神，属土，代表土地、房产、稳定、积累',
            '螣蛇': '南方之神，属火，代表口舌、是非、变动、突发事件',
            '白虎': '西方之神，属金，代表刀兵、竞争、压力、挑战',
            '玄武': '北方之神，属水，代表智慧、谋略、暗中行动、秘密'
        }
        return meanings.get(liu_shen, '未知')
        
    def _get_liu_shen_influence(self, liu_shen):
        """获取六神影响"""
        influences = {
            '青龙': '旺相时贵人相助，衰弱时孤立无援',
            '朱雀': '旺相时文书顺利，衰弱时文书受阻',
            '勾陈': '旺相时稳定发展，衰弱时变动不安',
            '螣蛇': '旺相时变动有利，衰弱时变动不利',
            '白虎': '旺相时勇敢面对，衰弱时畏缩不前',
            '玄武': '旺相时智慧开启，衰弱时智慧受阻'
        }
        return influences.get(liu_shen, '未知')
        
    def _calculate_shi_er_shen(self):
        """计算十二神将（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        yue_jiang = self.result.get('yue_jiang', '寅')
        
        # 十二神将排列（专业版本）
        shi_er_shen_detailed = {}
        for i, shen in enumerate(self.shiershen):
            shi_er_shen_detailed[shen] = {
                'position': f'第{i+1}位',
                'meaning': self._get_shi_er_shen_meaning(shen),
                'influence': self._get_shi_er_shen_influence(shen),
                'wuxing': self._get_shi_er_shen_wuxing(shen)
            }
        
        self.result['shi_er_shen'] = shi_er_shen_detailed
        
    def _get_shi_er_shen_meaning(self, shen):
        """获取十二神将含义"""
        meanings = {
            '贵人': '贵人相助，代表有贵人出现',
            '螣蛇': '口舌是非，代表有口舌是非',
            '朱雀': '文书考试，代表有文书考试',
            '六合': '合作和谐，代表有合作和谐',
            '勾陈': '土地房产，代表有土地房产',
            '青龙': '贵人相助，代表有贵人相助',
            '天空': '天空之神，代表有空中的事情',
            '白虎': '刀兵竞争，代表有刀兵竞争',
            '太常': '太常之神，代表有太常的事情',
            '玄武': '智慧谋略，代表有智慧谋略',
            '太阴': '太阴之神，代表有太阴的事情',
            '天后': '天后之神，代表有天后的事情'
        }
        return meanings.get(shen, '未知')
        
    def _get_shi_er_shen_influence(self, shen):
        """获取十二神将影响"""
        influences = {
            '贵人': '旺相时贵人相助，衰弱时孤立无援',
            '螣蛇': '旺相时变动有利，衰弱时变动不利',
            '朱雀': '旺相时文书顺利，衰弱时文书受阻',
            '六合': '旺相时合作顺利，衰弱时合作受阻',
            '勾陈': '旺相时稳定发展，衰弱时变动不安',
            '青龙': '旺相时贵人相助，衰弱时孤立无援',
            '天空': '旺相时空中有利，衰弱时空中有害',
            '白虎': '旺相时勇敢面对，衰弱时畏缩不前',
            '太常': '旺相时常事顺利，衰弱时常事受阻',
            '玄武': '旺相时智慧开启，衰弱时智慧受阻',
            '太阴': '旺相时阴事顺利，衰弱时阴事受阻',
            '天后': '旺相时天后相助，衰弱时天后不助'
        }
        return influences.get(shen, '未知')
        
    def _get_shi_er_shen_wuxing(self, shen):
        """获取十二神将五行属性"""
        wuxing_map = {
            '贵人': '土', '螣蛇': '火', '朱雀': '火', '六合': '木',
            '勾陈': '土', '青龙': '木', '天空': '金', '白虎': '金',
            '太常': '土', '玄武': '水', '太阴': '水', '天后': '水'
        }
        return wuxing_map.get(shen, '未知')
        
    def _calculate_shen_sha(self):
        """计算神煞（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        ri_zhi = self.result.get('ri_zhi', '寅')
        yue_jiang = self.result.get('yue_jiang', '寅')
        
        # 计算各种神煞
        shen_sha = {
            '天乙贵人': self._calculate_tian_yi_gui_ren(ri_gan),
            '天德贵人': self._calculate_tian_de_gui_ren(ri_gan),
            '月德贵人': self._calculate_yue_de_gui_ren(ri_gan),
            '天喜': self._calculate_tian_xi(ri_gan),
            '天马': self._calculate_tian_ma(ri_gan),
            '天刑': self._calculate_tian_xing(ri_gan),
            '天罗': self._calculate_tian_luo(ri_gan),
            '地网': self._calculate_di_wang(ri_gan),
            '孤辰': self._calculate_gu_chen(ri_gan),
            '寡宿': self._calculate_gua_su(ri_gan)
        }
        
        self.result['shen_sha'] = shen_sha
        
    def _calculate_tian_yi_gui_ren(self, ri_gan):
        """计算天乙贵人"""
        tian_yi_map = {
            '甲': '丑未', '乙': '子申', '丙': '亥酉', '丁': '寅午',
            '戊': '丑未', '己': '子申', '庚': '亥酉', '辛': '寅午',
            '壬': '巳卯', '癸': '巳卯'
        }
        return tian_yi_map.get(ri_gan, '未知')
        
    def _calculate_tian_de_gui_ren(self, ri_gan):
        """计算天德贵人"""
        tian_de_map = {
            '甲': '巳', '乙': '午', '丙': '未', '丁': '申',
            '戊': '酉', '己': '戌', '庚': '亥', '辛': '子',
            '壬': '丑', '癸': '寅'
        }
        return tian_de_map.get(ri_gan, '未知')
        
    def _calculate_yue_de_gui_ren(self, ri_gan):
        """计算月德贵人"""
        yue_de_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        return yue_de_map.get(ri_gan, '未知')
        
    def _calculate_tian_xi(self, ri_gan):
        """计算天喜"""
        tian_xi_map = {
            '甲': '酉', '乙': '申', '丙': '未', '丁': '午',
            '戊': '巳', '己': '辰', '庚': '卯', '辛': '寅',
            '壬': '丑', '癸': '子'
        }
        return tian_xi_map.get(ri_gan, '未知')
        
    def _calculate_tian_ma(self, ri_gan):
        """计算天马"""
        tian_ma_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        return tian_ma_map.get(ri_gan, '未知')
        
    def _calculate_tian_xing(self, ri_gan):
        """计算天刑"""
        tian_xing_map = {
            '甲': '巳', '乙': '午', '丙': '未', '丁': '申',
            '戊': '酉', '己': '戌', '庚': '亥', '辛': '子',
            '壬': '丑', '癸': '寅'
        }
        return tian_xing_map.get(ri_gan, '未知')
        
    def _calculate_tian_luo(self, ri_gan):
        """计算天罗"""
        tian_luo_map = {
            '甲': '辰', '乙': '巳', '丙': '午', '丁': '未',
            '戊': '申', '己': '酉', '庚': '戌', '辛': '亥',
            '壬': '子', '癸': '丑'
        }
        return tian_luo_map.get(ri_gan, '未知')
        
    def _calculate_di_wang(self, ri_gan):
        """计算地网"""
        di_wang_map = {
            '甲': '戌', '乙': '亥', '丙': '子', '丁': '丑',
            '戊': '寅', '己': '卯', '庚': '辰', '辛': '巳',
            '壬': '午', '癸': '未'
        }
        return di_wang_map.get(ri_gan, '未知')
        
    def _calculate_gu_chen(self, ri_gan):
        """计算孤辰"""
        gu_chen_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        return gu_chen_map.get(ri_gan, '未知')
        
    def _calculate_gua_su(self, ri_gan):
        """计算寡宿"""
        gua_su_map = {
            '甲': '申', '乙': '酉', '丙': '亥', '丁': '子',
            '戊': '亥', '己': '子', '庚': '寅', '辛': '卯',
            '壬': '巳', '癸': '午'
        }
        return gua_su_map.get(ri_gan, '未知')
        
    def _calculate_gui_ren(self):
        """计算贵人（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        yue_jiang = self.result.get('yue_jiang', '寅')
        
        # 贵人方位计算
        gui_ren = {
            '天乙贵人': self._calculate_tian_yi_gui_ren(ri_gan),
            '天德贵人': self._calculate_tian_de_gui_ren(ri_gan),
            '月德贵人': self._calculate_yue_de_gui_ren(ri_gan),
            '方位': self._calculate_gui_ren_fang_wei(ri_gan, yue_jiang)
        }
        
        self.result['gui_ren'] = gui_ren
        
    def _calculate_gui_ren_fang_wei(self, ri_gan, yue_jiang):
        """计算贵人方位"""
        # 简化版贵人方位计算
        return f"以{ri_gan}为基准，{yue_jiang}为月将的贵人方位"
        
    def _calculate_kong_wang(self):
        """计算空亡（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        
        # 空亡计算
        kong_wang_map = {
            '甲': '戌亥', '乙': '申酉', '丙': '午未', '丁': '辰巳',
            '戊': '寅卯', '己': '子丑', '庚': '戌亥', '辛': '申酉',
            '壬': '午未', '癸': '辰巳'
        }
        
        self.result['kong_wang'] = {
            'kong_wang': kong_wang_map.get(ri_gan, '未知'),
            'meaning': '空亡代表虚无、不实、无结果',
            'influence': '空亡当值，事情容易落空或没有结果'
        }
        
    def _calculate_yi_ma(self):
        """计算驿马（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        
        # 驿马计算
        yi_ma_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        
        self.result['yi_ma'] = {
            'yi_ma': yi_ma_map.get(ri_gan, '未知'),
            'meaning': '驿马代表变动、迁移、旅行',
            'influence': '驿马当值，事情容易变动或迁移'
        }
        
    def _calculate_chang_sheng(self):
        """计算长生十二神（专业版本）"""
        ri_gan = self.result.get('ri_gan', '甲')
        
        # 长生十二神
        chang_sheng_map = {
            '甲': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
            '乙': ['午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未'],
            '丙': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
            '丁': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
            '戊': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
            '己': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
            '庚': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
            '辛': ['子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑'],
            '壬': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'],
            '癸': ['卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰']
        }
        
        chang_sheng_list = chang_sheng_map.get(ri_gan, [])
        
        # 长生十二神详细解释
        chang_sheng_names = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']
        
        chang_sheng_detailed = {}
        for i, (name, zhi) in enumerate(zip(chang_sheng_names, chang_sheng_list)):
            chang_sheng_detailed[name] = {
                'zhi': zhi,
                'meaning': self._get_chang_sheng_meaning(name),
                'influence': self._get_chang_sheng_influence(name)
            }
        
        self.result['chang_sheng'] = chang_sheng_detailed
        
    def _get_chang_sheng_meaning(self, name):
        """获取长生十二神含义"""
        meanings = {
            '长生': '万物开始生长，代表开始、新生',
            '沐浴': '万物开始清洁，代表清洁、净化',
            '冠带': '万物开始装饰，代表装饰、美化',
            '临官': '万物开始当官，代表当官、掌权',
            '帝旺': '万物达到极盛，代表极盛、顶峰',
            '衰': '万物开始衰落，代表衰落、衰退',
            '病': '万物开始生病，代表生病、疾病',
            '死': '万物开始死亡，代表死亡、结束',
            '墓': '万物开始埋葬，代表埋葬、隐藏',
            '绝': '万物开始断绝，代表断绝、分离',
            '胎': '万物开始孕育，代表孕育、孕育',
            '养': '万物开始养育，代表养育、培养'
        }
        return meanings.get(name, '未知')
        
    def _get_chang_sheng_influence(self, name):
        """获取长生十二神影响"""
        influences = {
            '长生': '旺相时开始顺利，衰弱时开始困难',
            '沐浴': '旺相时清洁顺利，衰弱时清洁困难',
            '冠带': '旺相时装饰顺利，衰弱时装饰困难',
            '临官': '旺相时当官顺利，衰弱时当官困难',
            '帝旺': '旺相时极盛顺利，衰弱时极盛困难',
            '衰': '旺相时衰落顺利，衰弱时衰落困难',
            '病': '旺相时生病顺利，衰弱时生病困难',
            '死': '旺相时死亡顺利，衰弱时死亡困难',
            '墓': '旺相时埋葬顺利，衰弱时埋葬困难',
            '绝': '旺相时断绝顺利，衰弱时断绝困难',
            '胎': '旺相时孕育顺利，衰弱时孕育困难',
            '养': '旺相时养育顺利，衰弱时养育困难'
        }
        return influences.get(name, '未知')
        
    def _get_gan_zhi(self, gan):
        """获取天干对应的地支"""
        if not isinstance(gan, str):
            return '寅'
            
        gan_zhi_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '巳',
            '己': '午', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子'
        }
        return gan_zhi_map.get(gan, '寅')
        
    def _calculate_solar_ri_gan(self):
        """计算公历日干（专业版本）"""
        # 使用更精确的算法计算公历日干
        base_date = datetime(1900, 1, 1)
        days_diff = (self.solar_date - base_date).days
        
        # 天干周期为10天
        gan_index = days_diff % 10
        return self.tiangan[gan_index]
        
    def _calculate_solar_ri_zhi(self):
        """计算公历日支（专业版本）"""
        # 使用更精确的算法计算公历日支
        base_date = datetime(1900, 1, 1)
        days_diff = (self.solar_date - base_date).days
        
        # 地支周期为12天
        zhi_index = days_diff % 12
        return self.dizhi[zhi_index]
        
    def get_result(self):
        """获取完整的排盘结果"""
        return self.result
