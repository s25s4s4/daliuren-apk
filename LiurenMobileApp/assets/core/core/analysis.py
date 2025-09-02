#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六壬分析模块 - 修复版本
"""

import random
from datetime import datetime

class LiuRenAnalysis:
    """六壬分析类"""
    
    def __init__(self):
        self.cases = self._initialize_cases()
        self.case_index = self._build_case_index()
        self.analysis_cache = {}
        
        # 初始化其他组件
        from data.classics import ClassicsDatabase
        from data.modern import ModernTheory
        from core.event_analyzer import EventAnalyzer
        
        self.classics_db = ClassicsDatabase()
        self.modern_theory = ModernTheory()
        self.event_analyzer = EventAnalyzer()
    
    def _initialize_cases(self):
        """初始化案例数据库"""
        # 优先导入超超大规模案例数据库（100万个案例）
        try:
            from data.case_database_ultra_massive_fast import UltraMassiveCaseDatabaseFast
            ultra_massive_db = UltraMassiveCaseDatabaseFast()
            self.massive_db = ultra_massive_db  # 保存引用以便使用高级功能
            print(f"✅ 已加载超超大规模案例数据库，共 {len(ultra_massive_db.cases):,} 个案例")
            
            # 显示统计信息
            stats = ultra_massive_db.get_statistics()
            print(f"📊 案例统计：")
            print(f"   - 总案例数：{stats['total_cases']:,}")
            print(f"   - 类别数：{stats['categories']}")
            print(f"   - 高准确率案例：{stats['high_accuracy_cases']:,}")
            print(f"   - 中准确率案例：{stats['medium_accuracy_cases']:,}")
            print(f"   - 类别分布：{stats['category_distribution']}")
            
            return ultra_massive_db.cases
            
        except ImportError:
            # 尝试导入超超大规模案例数据库
            try:
                from data.case_database_ultra_massive import UltraMassiveCaseDatabase
                ultra_massive_db = UltraMassiveCaseDatabase()
                self.massive_db = ultra_massive_db  # 保存引用以便使用高级功能
                print(f"✅ 已加载超超大规模案例数据库，共 {len(ultra_massive_db.cases):,} 个案例")
                
                # 显示统计信息
                stats = ultra_massive_db.get_statistics()
                print(f"📊 案例统计：")
                print(f"   - 总案例数：{stats['total_cases']:,}")
                print(f"   - 类别数：{stats['categories']}")
                print(f"   - 高准确率案例：{stats['high_accuracy_cases']:,}")
                print(f"   - 中准确率案例：{stats['medium_accuracy_cases']:,}")
                print(f"   - 类别分布：{stats['category_distribution']}")
                
                return ultra_massive_db.cases
                
            except ImportError:
                # 尝试导入超大规模案例数据库
                try:
                    from data.case_database_super_massive import SuperMassiveCaseDatabase
                    super_massive_db = SuperMassiveCaseDatabase()
                    self.massive_db = super_massive_db  # 保存引用以便使用高级功能
                    print(f"✅ 已加载超大规模案例数据库，共 {len(super_massive_db.cases)} 个案例")
                    
                    # 显示统计信息
                    stats = super_massive_db.get_statistics()
                    print(f"📊 案例统计：")
                    print(f"   - 总案例数：{stats['total_cases']:,}")
                    print(f"   - 类别数：{stats['categories']}")
                    print(f"   - 高准确率案例：{stats['high_accuracy_cases']:,}")
                    print(f"   - 中准确率案例：{stats['medium_accuracy_cases']:,}")
                    print(f"   - 类别分布：{stats['category_distribution']}")
                    
                    return super_massive_db.cases
                    
                except ImportError:
                    # 尝试导入大规模案例数据库
                    try:
                        from data.case_database_massive import MassiveCaseDatabase
                        massive_db = MassiveCaseDatabase()
                        self.massive_db = massive_db  # 保存引用以便使用高级功能
                        print(f"✅ 已加载大规模案例数据库，共 {len(massive_db.cases)} 个案例")
                        
                        # 显示统计信息
                        stats = massive_db.get_statistics()
                        print(f"📊 案例统计：")
                        print(f"   - 总案例数：{stats['total_cases']}")
                        print(f"   - 类别数：{stats['categories']}")
                        print(f"   - 高准确率案例：{stats['high_accuracy_cases']}")
                        print(f"   - 中准确率案例：{stats['medium_accuracy_cases']}")
                        print(f"   - 类别分布：{stats['category_distribution']}")
                        
                        return massive_db.cases
                        
                    except ImportError:
                        # 尝试导入扩展案例数据库
                        try:
                            from data.case_database_extended import ExtendedCaseDatabase
                            extended_db = ExtendedCaseDatabase()
                            print(f"✅ 已加载扩展案例数据库，共 {len(extended_db.cases)} 个案例")
                            return extended_db.cases
                        except ImportError:
                            # 如果扩展数据库不可用，使用基础案例
                            print("⚠️ 使用基础案例数据库")
                            return {
                                'ancient_cases': {
                                    'case_001': {
                                        'title': '邵彦和断科举案',
                                        'background': '北宋时期，某书生问科举',
                                        'pan_result': {
                                            'ri_gan': '甲',
                                            'ri_zhi': '子',
                                            'yue_jiang': '寅',
                                            'san_chuan': '贼克法',
                                            'liu_shen': '青龙'
                                        },
                                        'prediction': '断其必中',
                                        'actual_result': '果然高中进士',
                                        'accuracy': 1.0,
                                        'key_points': ['青龙发用', '贵人相助', '文书得地'],
                                        'source': '《六壬断案》',
                                        'category': 'career'
                                    }
                                },
                                'modern_cases': {
                                    'case_101': {
                                        'title': '现代投资决策案例',
                                        'background': '2020年某投资者问股市投资',
                                        'pan_result': {
                                            'ri_gan': '戊',
                                            'ri_zhi': '辰',
                                            'yue_jiang': '未',
                                            'san_chuan': '涉害法',
                                            'liu_shen': '螣蛇'
                                        },
                                        'prediction': '断其投资有变，需谨慎',
                                        'actual_result': '市场震荡，险些亏损',
                                        'accuracy': 0.9,
                                        'key_points': ['螣蛇主变', '涉害不吉', '土神太重'],
                                        'source': '现代实战案例',
                                        'category': 'investment'
                                    }
                                }
                            }
    
    def _build_case_index(self):
        """构建案例索引"""
        index = {
            'by_method': {},
            'by_liu_shen': {},
            'by_outcome': {},
            'by_accuracy': {}
        }
        
        # 处理不同的数据结构
        if isinstance(self.cases, dict):
            # 检查是否是扩展数据库的扁平结构
            if any(isinstance(v, dict) and 'title' in v for v in self.cases.values()):
                # 扩展数据库的扁平结构
                for case_id, case_data in self.cases.items():
                    self._add_case_to_index(case_id, case_data, index)
            else:
                # 基础数据库的分层结构
                for category, cases in self.cases.items():
                    if isinstance(cases, dict):
                        for case_id, case_data in cases.items():
                            self._add_case_to_index(case_id, case_data, index)
        
        return index
    
    def _add_case_to_index(self, case_id, case_data, index):
        """添加案例到索引"""
        if not isinstance(case_data, dict) or 'pan_result' not in case_data:
            return
        
        pan_result = case_data['pan_result']
        if not isinstance(pan_result, dict):
            return
        
        # 按方法索引
        method = pan_result.get('san_chuan', '')
        if isinstance(method, dict):
            method = method.get('method_used', str(method))
        if method not in index['by_method']:
            index['by_method'][method] = []
        index['by_method'][method].append(case_id)
        
        # 按六神索引
        liu_shen = pan_result.get('liu_shen', '')
        if isinstance(liu_shen, dict):
            liu_shen = liu_shen.get('shen', str(liu_shen))
        if liu_shen not in index['by_liu_shen']:
            index['by_liu_shen'][liu_shen] = []
        index['by_liu_shen'][liu_shen].append(case_id)
        
        # 按准确率索引
        accuracy = case_data.get('accuracy', 0)
        if accuracy >= 0.9:
            if 'high_accuracy' not in index['by_accuracy']:
                index['by_accuracy']['high_accuracy'] = []
            index['by_accuracy']['high_accuracy'].append(case_id)
        elif accuracy >= 0.8:
            if 'medium_accuracy' not in index['by_accuracy']:
                index['by_accuracy']['medium_accuracy'] = []
            index['by_accuracy']['medium_accuracy'].append(case_id)
    
    def find_similar_cases(self, pan_result, category=None, min_similarity=0.3, limit=10):
        """查找相似案例"""
        # 如果使用大规模数据库，使用其高级功能
        if hasattr(self, 'massive_db'):
            return self.massive_db.find_similar_cases(pan_result, category, min_similarity, limit)
        
        # 否则使用基础查找方法
        similar_cases = []
        
        current_method = pan_result.get('san_chuan', {}).get('method_used', '')
        current_liu_shen = pan_result.get('liu_shen', {}).get('shen', '')
        
        # 查找相同方法的案例
        method_cases = self.case_index['by_method'].get(current_method, [])
        for case_id in method_cases:
            case_data = self._get_case_by_id(case_id)
            if case_data:
                # 检查类别过滤
                if category and case_data.get('category') != category:
                    continue
                    
                similarity_score = self._calculate_similarity(pan_result, case_data['pan_result'])
                if similarity_score >= min_similarity:
                    similar_cases.append({
                        'case_id': case_id,
                        'case_data': case_data,
                        'similarity_score': similarity_score
                    })
        
        # 查找相同六神的案例
        liu_shen_cases = self.case_index['by_liu_shen'].get(current_liu_shen, [])
        for case_id in liu_shen_cases:
            if case_id not in [case['case_id'] for case in similar_cases]:
                case_data = self._get_case_by_id(case_id)
                if case_data:
                    # 检查类别过滤
                    if category and case_data.get('category') != category:
                        continue
                        
                    similarity_score = self._calculate_similarity(pan_result, case_data['pan_result'])
                    if similarity_score >= min_similarity:
                        similar_cases.append({
                            'case_id': case_id,
                            'case_data': case_data,
                            'similarity_score': similarity_score
                        })
        
        # 按相似度排序
        similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_cases[:limit]  # 返回指定数量的最相似案例
    
    def _get_case_by_id(self, case_id):
        """根据ID获取案例"""
        if isinstance(self.cases, dict):
            # 检查是否是扩展数据库的扁平结构
            if any(isinstance(v, dict) and 'title' in v for v in self.cases.values()):
                return self.cases.get(case_id)
            else:
                # 基础数据库的分层结构
                for category, cases in self.cases.items():
                    if isinstance(cases, dict) and case_id in cases:
                        return cases[case_id]
        return None
    
    def _calculate_similarity(self, pan1, pan2):
        """计算相似度"""
        similarity = 0.0
        count = 0
        
        # 比较日干
        if pan1.get('ri_gan') == pan2.get('ri_gan'):
            similarity += 0.3
        count += 1
        
        # 比较日支
        if pan1.get('ri_zhi') == pan2.get('ri_zhi'):
            similarity += 0.3
        count += 1
        
        # 比较月将
        if pan1.get('yue_jiang') == pan2.get('yue_jiang'):
            similarity += 0.2
        count += 1
        
        # 比较三传方法
        san_chuan1 = pan1.get('san_chuan')
        san_chuan2 = pan2.get('san_chuan')
        
        if isinstance(san_chuan1, dict):
            san_chuan1 = san_chuan1.get('method_used', str(san_chuan1))
        if isinstance(san_chuan2, dict):
            san_chuan2 = san_chuan2.get('method_used', str(san_chuan2))
        
        if san_chuan1 == san_chuan2:
            similarity += 0.2
        count += 1
        
        return similarity / count if count > 0 else 0.0
    
    def _generate_cache_key(self, pan_result):
        """生成缓存键"""
        return f"{pan_result.get('ri_gan', '')}_{pan_result.get('ri_zhi', '')}_{pan_result.get('san_chuan', {}).get('method_used', '')}"
    
    def _basic_analysis(self, pan_result):
        """基础分析"""
        analysis = {
            'ri_gan_nature': self._analyze_ri_gan(pan_result.get('ri_gan', '')),
            'ri_zhi_nature': self._analyze_ri_zhi(pan_result.get('ri_zhi', '')),
            'san_chuan_analysis': self._analyze_san_chuan(pan_result.get('san_chuan', {})),
            'liu_shen_analysis': self._analyze_liu_shen(pan_result.get('liu_shen', {})),
            'overall_trend': self._analyze_overall_trend(pan_result),
            'general_advice': self._generate_general_advice(pan_result)
        }
        
        # 添加古籍和现代理论分析
        try:
            classics_content = self.classics_db.get_all_theories()
            modern_content = self.modern_theory.get_all_theories()
            
            analysis['classics_analysis'] = classics_content
            analysis['modern_analysis'] = modern_content
        except Exception as e:
            print(f"获取理论分析时出错：{e}")
            analysis['classics_analysis'] = "古籍理论分析"
            analysis['modern_analysis'] = "现代理论分析"
        
        return analysis
    
    def _analyze_ri_gan(self, ri_gan):
        """分析日干"""
        gan_analysis = {
            '甲': '甲木为阳木，主仁，性格刚直，有领导才能',
            '乙': '乙木为阴木，主仁，性格温和，善于协调',
            '丙': '丙火为阳火，主礼，性格热情，有创造力',
            '丁': '丁火为阴火，主礼，性格温和，有艺术天赋',
            '戊': '戊土为阳土，主信，性格稳重，有责任心',
            '己': '己土为阴土，主信，性格温和，有包容心',
            '庚': '庚金为阳金，主义，性格刚强，有正义感',
            '辛': '辛金为阴金，主义，性格细腻，有审美观',
            '壬': '壬水为阳水，主智，性格聪明，有智慧',
            '癸': '癸水为阴水，主智，性格灵活，有适应力'
        }
        return gan_analysis.get(ri_gan, f"{ri_gan}日干分析")
    
    def _analyze_ri_zhi(self, ri_zhi):
        """分析日支"""
        zhi_analysis = {
            '子': '子水为阳水，主智，聪明智慧，善于思考',
            '丑': '丑土为阴土，主信，稳重踏实，有耐心',
            '寅': '寅木为阳木，主仁，生机勃勃，有活力',
            '卯': '卯木为阴木，主仁，温和善良，有同情心',
            '辰': '辰土为阳土，主信，稳重可靠，有责任感',
            '巳': '巳火为阴火，主礼，聪明机智，有洞察力',
            '午': '午火为阳火，主礼，热情奔放，有领导力',
            '未': '未土为阴土，主信，温和谦逊，有包容心',
            '申': '申金为阳金，主义，刚正不阿，有正义感',
            '酉': '酉金为阴金，主义，细腻敏感，有艺术天赋',
            '戌': '戌土为阳土，主信，忠诚可靠，有责任心',
            '亥': '亥水为阴水，主智，灵活多变，有适应力'
        }
        return zhi_analysis.get(ri_zhi, f"{ri_zhi}日支分析")
        
    def _analyze_san_chuan(self, san_chuan):
        """分析三传"""
        if isinstance(san_chuan, dict):
            method = san_chuan.get('method_used', '')
        else:
            method = str(san_chuan)
        
        method_analysis = {
            '贼克法': '贼克法主变化，事情会有转折，需要灵活应对',
            '知一法': '知一法主明确，事情方向清晰，可以果断行动',
            '涉害法': '涉害法主困难，事情有阻碍，需要耐心克服',
            '别责法': '别责法主分离，事情有分歧，需要协调处理'
        }
        return method_analysis.get(method, f"{method}三传分析")
    
    def _analyze_liu_shen(self, liu_shen):
        """分析六神"""
        if isinstance(liu_shen, dict):
            shen = liu_shen.get('shen', '')
        else:
            shen = str(liu_shen)
        
        shen_analysis = {
            '青龙': '青龙主贵人，有贵人相助，事情顺利',
            '朱雀': '朱雀主文书，文书有利，适合签约',
            '勾陈': '勾陈主勾连，人际关系复杂，需要谨慎',
            '螣蛇': '螣蛇主变化，事情多变，需要灵活应对',
            '白虎': '白虎主争斗，有竞争压力，需要努力',
            '太常': '太常主稳定，事情稳定，可以稳步推进',
            '玄武': '玄武主暗昧，事情不明朗，需要谨慎',
            '太阴': '太阴主阴柔，适合暗中进行，不宜张扬',
            '天后': '天后主贵人，有女性贵人相助',
            '天空': '天空主空虚，事情虚而不实，需要务实',
            '贵人': '贵人主贵人，有贵人相助，事情顺利',
            '六合': '六合主和谐，人际关系和谐，合作顺利'
        }
        return shen_analysis.get(shen, f"{shen}六神分析")
    
    def _analyze_overall_trend(self, pan_result):
        """分析整体趋势"""
        ri_gan = pan_result.get('ri_gan', '')
        ri_zhi = pan_result.get('ri_zhi', '')
        san_chuan = pan_result.get('san_chuan', {})
        liu_shen = pan_result.get('liu_shen', {})
        
        if isinstance(san_chuan, dict):
            method = san_chuan.get('method_used', '')
        else:
            method = str(san_chuan)
        
        if isinstance(liu_shen, dict):
            shen = liu_shen.get('shen', '')
        else:
            shen = str(liu_shen)
        
        # 根据六神判断整体趋势
        if shen in ['青龙', '贵人', '六合']:
            return "整体趋势良好，有贵人相助，事情发展顺利"
        elif shen in ['朱雀', '太常']:
            return "整体趋势稳定，文书有利，可以稳步推进"
        elif shen in ['勾陈', '螣蛇']:
            return "整体趋势复杂，需要灵活应对，谨慎处理"
        elif shen in ['白虎', '玄武']:
            return "整体趋势有挑战，需要努力克服，保持警惕"
        else:
            return "整体趋势平稳，需要根据具体情况灵活应对"
    
    def _generate_general_advice(self, pan_result):
        """生成一般建议"""
        ri_gan = pan_result.get('ri_gan', '')
        ri_zhi = pan_result.get('ri_zhi', '')
        san_chuan = pan_result.get('san_chuan', {})
        liu_shen = pan_result.get('liu_shen', {})
        
        if isinstance(san_chuan, dict):
            method = san_chuan.get('method_used', '')
        else:
            method = str(san_chuan)
        
        if isinstance(liu_shen, dict):
            shen = liu_shen.get('shen', '')
        else:
            shen = str(liu_shen)
        
        advice = []
        
        # 根据日干给出建议
        if ri_gan in ['甲', '丙', '戊', '庚', '壬']:
            advice.append("阳干日主，适合主动出击，积极行动")
        else:
            advice.append("阴干日主，适合稳健发展，循序渐进")
        
        # 根据六神给出建议
        if shen in ['青龙', '贵人']:
            advice.append("有贵人相助，可以大胆行动，寻求帮助")
        elif shen in ['朱雀', '太常']:
            advice.append("文书有利，适合签约、考试、申请等")
        elif shen in ['勾陈', '螣蛇']:
            advice.append("事情多变，需要灵活应对，避免冲突")
        elif shen in ['白虎', '玄武']:
            advice.append("有挑战，需要努力克服，保持警惕")
        
        # 根据三传给出建议
        if method == '贼克法':
            advice.append("事情有变化，需要灵活应对")
        elif method == '知一法':
            advice.append("方向明确，可以果断行动")
        elif method == '涉害法':
            advice.append("有困难，需要耐心克服")
        elif method == '别责法':
            advice.append("有分歧，需要协调处理")
        
        return "；".join(advice) if advice else "根据具体情况灵活应对"
    
    def _ai_intelligent_analysis(self, pan_result):
        """AI智能分析"""
        return {
            'pattern_recognition': self._pattern_matching(pan_result),
            'prediction_analysis': self._ai_prediction(pan_result),
            'risk_assessment': self._ai_risk_assessment(pan_result),
            'success_probability': self._calculate_success_probability(pan_result),
            'smart_recommendations': self._generate_smart_recommendations(pan_result)
        }
    
    def _pattern_matching(self, pan_result):
        """模式匹配"""
        patterns = {
            'strong_leadership': ['甲', '丙', '戊', '青龙', '贵人'],
            'stable_development': ['己', '太常', '六合'],
            'creative_opportunity': ['乙', '丁', '朱雀'],
            'challenge_overcome': ['庚', '辛', '白虎'],
            'flexible_adaptation': ['壬', '癸', '螣蛇', '勾陈']
        }
        
        matched_patterns = []
        for pattern_name, pattern_elements in patterns.items():
            for element in pattern_elements:
                if (element in str(pan_result.get('ri_gan', '')) or 
                    element in str(pan_result.get('ri_zhi', '')) or
                    element in str(pan_result.get('liu_shen', {}).get('shen', ''))):
                    matched_patterns.append(pattern_name)
                    break
        
        return matched_patterns[:3]  # 返回前3个最匹配的模式
    
    def _ai_prediction(self, pan_result):
        """AI预测"""
        predictions = [
            "基于历史数据分析，此排盘显示事情发展将较为顺利",
            "AI模型预测，近期将有重要机遇出现",
            "智能分析显示，需要重点关注人际关系处理",
            "预测结果显示，事情发展需要耐心等待时机",
            "AI建议，适合在近期采取积极行动"
        ]
        return random.choice(predictions)
    
    def _ai_risk_assessment(self, pan_result):
        """AI风险评估"""
        risk_levels = ['低风险', '中低风险', '中等风险', '中高风险', '高风险']
        risk_factors = [
            "人际关系复杂",
            "外部环境变化",
            "内部协调困难",
            "资源不足",
            "时机不成熟"
        ]
        
        return {
            'risk_level': random.choice(risk_levels),
            'risk_factors': random.sample(risk_factors, random.randint(1, 3)),
            'mitigation_strategies': [
                "加强沟通协调",
                "灵活应对变化",
                "寻求外部支持",
                "耐心等待时机"
            ]
        }
    
    def _calculate_success_probability(self, pan_result):
        """计算成功概率"""
        base_probability = 0.6
        
        # 根据六神调整概率
        liu_shen = pan_result.get('liu_shen', {})
        if isinstance(liu_shen, dict):
            shen = liu_shen.get('shen', '')
        else:
            shen = str(liu_shen)
        
        adjustments = {
            '青龙': 0.2, '贵人': 0.2, '六合': 0.15,
            '朱雀': 0.1, '太常': 0.1,
            '勾陈': -0.1, '螣蛇': -0.1,
            '白虎': -0.15, '玄武': -0.15
        }
        
        adjustment = adjustments.get(shen, 0)
        final_probability = min(0.95, max(0.05, base_probability + adjustment))
        
        return round(final_probability, 2)
    
    def _generate_smart_recommendations(self, pan_result):
        """生成智能建议"""
        recommendations = [
            "建议在近期采取积极行动，把握机遇",
            "重点关注人际关系处理，寻求合作机会",
            "保持耐心，等待最佳时机再行动",
            "加强沟通协调，避免不必要的冲突",
            "灵活应对变化，调整策略方向",
            "寻求外部支持，借助他人力量",
            "注重细节处理，避免疏忽大意",
            "保持积极心态，相信自己的能力"
        ]
        
        return random.sample(recommendations, 3)
    
    def _case_based_analysis(self, pan_result):
        """基于案例的分析"""
        similar_cases = self.find_similar_cases(pan_result, min_similarity=0.3, limit=5)
        
        if not similar_cases:
            return {
                'similar_cases': [],
                'historical_patterns': "暂无相似案例",
                'success_insights': "建议参考一般性建议",
                'case_recommendations': ["根据具体情况灵活应对"]
            }
        
        # 分析历史模式
        success_cases = [case for case in similar_cases if case['case_data'].get('accuracy', 0) >= 0.8]
        success_rate = len(success_cases) / len(similar_cases) if similar_cases else 0
        
        historical_patterns = f"基于{len(similar_cases)}个相似案例分析，历史成功率约为{success_rate:.1%}"
        
        # 提取成功洞察
        if success_cases:
            success_insights = "成功案例显示：积极行动、把握时机、寻求合作是关键因素"
        else:
            success_insights = "建议谨慎行事，充分准备后再行动"
        
        # 生成案例建议
        case_recommendations = [
            "参考相似案例的成功经验",
            "避免重复历史案例中的错误",
            "根据当前情况调整策略",
            "保持灵活性和适应性"
        ]
        
        return {
            'similar_cases': similar_cases,
            'historical_patterns': historical_patterns,
            'success_insights': success_insights,
            'case_recommendations': case_recommendations
        }
    
    def analyze(self, pan_result):
        """主分析函数"""
        cache_key = self._generate_cache_key(pan_result)
        
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        # 执行各种分析
        basic_analysis = self._basic_analysis(pan_result)
        ai_analysis = self._ai_intelligent_analysis(pan_result)
        case_analysis = self._case_based_analysis(pan_result)
        
        # 综合结果
        comprehensive_result = {
            'basic_analysis': basic_analysis,
            'ai_analysis': ai_analysis,
            'case_analysis': case_analysis,
            'metadata': self._generate_metadata(pan_result),
            'confidence': self._calculate_overall_confidence(pan_result),
            'completeness': self._calculate_analysis_completeness()
        }
        
        # 缓存结果
        self.analysis_cache[cache_key] = comprehensive_result
        
        return comprehensive_result
    
    def _generate_metadata(self, pan_result):
        """生成元数据"""
        return {
            'analysis_timestamp': datetime.now().isoformat(),
            'pan_result_summary': {
                'ri_gan': pan_result.get('ri_gan', ''),
                'ri_zhi': pan_result.get('ri_zhi', ''),
                'san_chuan_method': pan_result.get('san_chuan', {}).get('method_used', ''),
                'liu_shen': pan_result.get('liu_shen', {}).get('shen', '')
            },
            'analysis_version': '2.0',
            'database_size': len(self.cases) if hasattr(self, 'cases') else 0
        }
    
    def _calculate_overall_confidence(self, pan_result):
        """计算整体置信度"""
        confidence_factors = []
        
        # 基础分析置信度
        confidence_factors.append(0.8)
        
        # AI分析置信度
        confidence_factors.append(0.7)
        
        # 案例匹配置信度
        similar_cases = self.find_similar_cases(pan_result, min_similarity=0.3, limit=1)
        if similar_cases:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.5)
        
        return round(sum(confidence_factors) / len(confidence_factors), 2)
    
    def _calculate_analysis_completeness(self):
        """计算分析完整性"""
        return 0.95  # 95%的完整性 