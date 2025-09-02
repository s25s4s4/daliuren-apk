#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能事件分析引擎
根据用户输入的事件描述，智能识别事件类型并提供个性化分析
"""

import re
import jieba
from collections import Counter

class EventAnalyzer:
    """智能事件分析引擎"""
    
    def __init__(self):
        # 初始化分词器
        jieba.initialize()
        
        # 事件分类数据库
        self.event_categories = self._initialize_event_categories()
        
        # 关键词权重
        self.keyword_weights = self._initialize_keyword_weights()
        
        # 相似度阈值
        self.similarity_threshold = 0.3
    
    def analyze_event(self, user_input):
        """分析用户输入的事件"""
        if not user_input or not user_input.strip():
            return self._get_default_analysis()
        
        # 预处理文本
        processed_text = self._preprocess_text(user_input)
        
        # 提取关键词
        keywords = self._extract_keywords(processed_text)
        
        # 分类事件
        event_type, confidence = self._classify_event(keywords, processed_text)
        
        # 生成分析配置
        analysis_config = self._generate_analysis_config(event_type, keywords, confidence)
        
        return {
            'original_input': user_input,
            'processed_text': processed_text,
            'keywords': keywords,
            'event_type': event_type,
            'confidence': confidence,
            'analysis_config': analysis_config,
            'personalized_focus': self._get_personalized_focus(event_type)
        }
    
    def _initialize_event_categories(self):
        """初始化事件分类数据库"""
        return {
            'career': {
                'name': '事业工作',
                'keywords': [
                    '工作', '事业', '职业', '升职', '跳槽', '求职', '面试', '加薪', 
                    '创业', '生意', '公司', '老板', '同事', '领导', '项目', '合作',
                    '晋升', '调动', '辞职', '换工作', '考公', '考编', '国考', '省考',
                    '职场', '业务', '客户', '销售', '管理', '技术', '开发', '设计'
                ],
                'patterns': [
                    r'工作.*怎么样', r'事业.*发展', r'能.*升职', r'会.*加薪',
                    r'跳槽.*好', r'换.*工作', r'创业.*成功', r'生意.*如何'
                ],
                'related_elements': ['官鬼', '父母', '兄弟', '子孙'],
                'focus_areas': ['官运', '贵人', '财运', '时机', '人际关系', '竞争']
            },
            'career_promotion': {
                'name': '升职加薪',
                'keywords': [
                    '升职', '加薪', '晋升', '提拔', '升官', '涨工资', '调薪', '晋级',
                    '升职加薪', '职位提升', '薪资调整', '职级晋升', '管理岗位', '领导岗位',
                    '副职', '正职', '主管', '经理', '总监', '副总', '总经理'
                ],
                'patterns': [
                    r'什么时候.*升职', r'能.*加薪', r'会.*晋升', r'升职.*机会',
                    r'加薪.*时间', r'晋升.*可能', r'提拔.*时机'
                ],
                'related_elements': ['官鬼', '父母', '贵人'],
                'focus_areas': ['官运', '贵人相助', '时机把握', '竞争关系']
            },
            'career_change': {
                'name': '跳槽换工作',
                'keywords': [
                    '跳槽', '换工作', '辞职', '离职', '转行', '换行业', '换公司',
                    '新工作', '新公司', '新环境', '重新开始', '职业转换', '行业转换',
                    '找工作', '应聘', '面试', 'offer', '入职', '试用期'
                ],
                'patterns': [
                    r'跳槽.*好', r'换.*工作', r'辞职.*时机', r'转行.*成功',
                    r'新工作.*如何', r'换公司.*合适', r'离职.*影响'
                ],
                'related_elements': ['官鬼', '父母', '兄弟', '子孙'],
                'focus_areas': ['变动时机', '新环境适应', '人际关系', '财运变化']
            },
            'entrepreneurship': {
                'name': '创业经商',
                'keywords': [
                    '创业', '做生意', '经商', '开公司', '办企业', '投资创业', '自主创业',
                    '合伙', '合作', '项目', '商机', '市场', '客户', '产品', '服务',
                    '盈利', '亏损', '资金', '融资', '贷款', '风险', '机遇'
                ],
                'patterns': [
                    r'创业.*成功', r'做生意.*如何', r'开公司.*时机', r'经商.*风险',
                    r'合伙.*好', r'投资.*回报', r'商机.*把握'
                ],
                'related_elements': ['妻财', '子孙', '兄弟', '官鬼'],
                'focus_areas': ['财运', '时机', '风险控制', '人际关系', '市场机遇']
            },
            'marriage': {
                'name': '婚姻感情',
                'keywords': [
                    '婚姻', '结婚', '恋爱', '感情', '爱情', '对象', '男朋友', '女朋友',
                    '老公', '老婆', '配偶', '夫妻', '离婚', '分手', '复合', '表白',
                    '相亲', '脱单', '桃花', '姻缘', '红娘', '媒人', '订婚', '求婚',
                    '情人', '暧昧', '约会', '交往', '恋人', '伴侣', '另一半'
                ],
                'patterns': [
                    r'什么时候.*结婚', r'会.*分手', r'能.*复合', r'有.*桃花',
                    r'婚姻.*如何', r'感情.*发展', r'对象.*怎么样', r'会.*离婚'
                ],
                'related_elements': ['妻财', '官鬼', '父母'],
                'focus_areas': ['桃花运', '婚姻宫', '配偶', '感情发展', '姻缘', '家庭和谐']
            },
            'dating': {
                'name': '恋爱脱单',
                'keywords': [
                    '恋爱', '脱单', '找对象', '男朋友', '女朋友', '表白', '追求', '被追求',
                    '暗恋', '单恋', '相亲', '约会', '交往', '暧昧', '好感', '喜欢',
                    '心动', '一见钟情', '日久生情', '异地恋', '网恋', '办公室恋情'
                ],
                'patterns': [
                    r'什么时候.*脱单', r'能.*找到.*对象', r'表白.*成功', r'追求.*结果',
                    r'相亲.*如何', r'约会.*顺利', r'异地恋.*维持'
                ],
                'related_elements': ['妻财', '官鬼', '兄弟'],
                'focus_areas': ['桃花运', '姻缘时机', '人际关系', '感情发展']
            },
            'marriage_timing': {
                'name': '结婚时机',
                'keywords': [
                    '结婚', '婚期', '婚礼', '订婚', '求婚', '领证', '办酒', '婚宴',
                    '结婚时间', '结婚年龄', '结婚对象', '结婚条件', '结婚准备',
                    '婚纱照', '蜜月', '新房', '彩礼', '嫁妆', '婚戒', '婚车'
                ],
                'patterns': [
                    r'什么时候.*结婚', r'结婚.*时机', r'婚期.*选择', r'求婚.*成功',
                    r'订婚.*时间', r'婚礼.*顺利', r'结婚.*对象'
                ],
                'related_elements': ['妻财', '父母', '官鬼'],
                'focus_areas': ['婚姻宫', '配偶信息', '时机选择', '家庭和谐']
            },
            'divorce': {
                'name': '离婚分手',
                'keywords': [
                    '离婚', '分手', '分居', '感情破裂', '婚姻危机', '第三者', '出轨',
                    '背叛', '争吵', '冷战', '复合', '挽回', '和好', '重新开始',
                    '财产分割', '子女抚养', '离婚协议', '离婚诉讼', '调解'
                ],
                'patterns': [
                    r'会.*离婚', r'分手.*可能', r'复合.*机会', r'挽回.*成功',
                    r'第三者.*影响', r'婚姻.*危机', r'感情.*破裂'
                ],
                'related_elements': ['妻财', '官鬼', '兄弟'],
                'focus_areas': ['婚姻宫', '感情危机', '复合机会', '法律事务']
            },
            'wealth': {
                'name': '财运投资',
                'keywords': [
                    '钱', '财运', '发财', '赚钱', '投资', '理财', '股票', '基金',
                    '创业', '生意', '买卖', '盈利', '亏损', '债务', '借钱', '还钱',
                    '彩票', '中奖', '收入', '工资', '奖金', '分红', '房产', '车子',
                    '存款', '贷款', '保险', '基金', '期货', '外汇', '比特币', '数字货币'
                ],
                'patterns': [
                    r'能.*发财', r'会.*赚钱', r'投资.*如何', r'股票.*涨',
                    r'财运.*怎么样', r'会.*中奖', r'生意.*好', r'能.*盈利'
                ],
                'related_elements': ['妻财', '子孙', '兄弟'],
                'focus_areas': ['财星', '财库', '偏财', '正财', '投资时机', '财运流年']
            },
            'investment': {
                'name': '投资理财',
                'keywords': [
                    '投资', '理财', '股票', '基金', '期货', '外汇', '债券', '黄金',
                    '房地产', '房产', '商铺', '写字楼', '理财产品', '银行理财',
                    'P2P', '众筹', '天使投资', '风险投资', '私募', '公募', 'ETF',
                    '期权', '期货', '外汇', '比特币', '数字货币', '区块链'
                ],
                'patterns': [
                    r'投资.*如何', r'股票.*涨跌', r'基金.*收益', r'理财.*风险',
                    r'房产.*投资', r'期货.*操作', r'外汇.*交易'
                ],
                'related_elements': ['妻财', '子孙', '官鬼'],
                'focus_areas': ['投资时机', '风险控制', '收益预测', '市场分析']
            },
            'lottery': {
                'name': '彩票中奖',
                'keywords': [
                    '彩票', '中奖', '双色球', '大乐透', '福彩', '体彩', '刮刮乐',
                    '六合彩', '时时彩', '快三', '排列三', '排列五', '七星彩',
                    '幸运', '运气', '横财', '意外之财', '一夜暴富', '发财梦'
                ],
                'patterns': [
                    r'会.*中奖', r'彩票.*中', r'横财.*机会', r'意外.*财',
                    r'幸运.*号码', r'发财.*梦', r'一夜.*暴富'
                ],
                'related_elements': ['妻财', '子孙'],
                'focus_areas': ['偏财运', '幸运时机', '横财机会', '风险提示']
            },
            'debt': {
                'name': '债务借贷',
                'keywords': [
                    '债务', '借钱', '还钱', '贷款', '房贷', '车贷', '信用卡', '透支',
                    '欠债', '讨债', '催债', '高利贷', '民间借贷', '银行借贷',
                    '分期付款', '按揭', '抵押', '担保', '信用', '征信', '黑名单'
                ],
                'patterns': [
                    r'借钱.*好', r'还钱.*时机', r'贷款.*成功', r'债务.*解决',
                    r'讨债.*结果', r'信用.*恢复', r'黑名单.*解除'
                ],
                'related_elements': ['妻财', '官鬼', '兄弟'],
                'focus_areas': ['财运', '信用恢复', '债务解决', '风险控制']
            },
            'health': {
                'name': '健康疾病',
                'keywords': [
                    '健康', '身体', '疾病', '生病', '医院', '医生', '治疗', '康复',
                    '手术', '住院', '药物', '中医', '西医', '体检', '检查', '诊断',
                    '头痛', '发烧', '感冒', '咳嗽', '胃痛', '腰痛', '失眠', '焦虑',
                    '抑郁', '癌症', '肿瘤', '高血压', '糖尿病', '心脏病', '养生', '锻炼'
                ],
                'patterns': [
                    r'身体.*如何', r'健康.*怎么样', r'会.*生病', r'能.*康复',
                    r'手术.*成功', r'治疗.*效果', r'病情.*发展', r'什么时候.*好'
                ],
                'related_elements': ['官鬼', '子孙', '父母'],
                'focus_areas': ['疾厄宫', '身体状况', '医疗', '康复时机', '养生方法']
            },
            'medical_treatment': {
                'name': '医疗治疗',
                'keywords': [
                    '医院', '医生', '治疗', '手术', '住院', '药物', '中药', '西药',
                    '针灸', '推拿', '按摩', '理疗', '化疗', '放疗', '透析', '移植',
                    '康复', '复健', '护理', '病房', '门诊', '急诊', '专家', '主任',
                    '护士', '药房', '处方', '医保', '自费', '报销'
                ],
                'patterns': [
                    r'手术.*成功', r'治疗.*效果', r'医生.*选择', r'医院.*好',
                    r'药物.*效果', r'康复.*时间', r'医保.*报销'
                ],
                'related_elements': ['官鬼', '子孙', '父母'],
                'focus_areas': ['医疗选择', '治疗效果', '康复时机', '费用控制']
            },
            'mental_health': {
                'name': '心理健康',
                'keywords': [
                    '心理', '精神', '情绪', '心情', '压力', '焦虑', '抑郁', '失眠',
                    '烦躁', '易怒', '悲观', '消极', '自卑', '自信', '乐观', '积极',
                    '心理咨询', '心理治疗', '精神科', '心理医生', '心理师', '催眠',
                    '冥想', '瑜伽', '放松', '减压', '调节', '平衡'
                ],
                'patterns': [
                    r'心理.*健康', r'情绪.*稳定', r'压力.*大', r'焦虑.*缓解',
                    r'抑郁.*治疗', r'失眠.*改善', r'心情.*调节'
                ],
                'related_elements': ['官鬼', '子孙', '父母'],
                'focus_areas': ['心理状态', '情绪调节', '压力缓解', '心理健康']
            },
            'pregnancy': {
                'name': '怀孕生育',
                'keywords': [
                    '怀孕', '生育', '生孩子', '备孕', '不孕', '流产', '胎停', '宫外孕',
                    '试管婴儿', '人工授精', '产检', '胎教', '分娩', '剖腹产', '顺产',
                    '月子', '坐月子', '母乳', '奶粉', '婴儿', '新生儿', '育儿',
                    '男胎', '女胎', '双胞胎', '龙凤胎'
                ],
                'patterns': [
                    r'什么时候.*怀孕', r'能.*生孩子', r'备孕.*成功', r'不孕.*治疗',
                    r'流产.*原因', r'胎教.*方法', r'分娩.*顺利'
                ],
                'related_elements': ['子孙', '父母', '妻财'],
                'focus_areas': ['子女宫', '生育时机', '健康状况', '家庭和谐']
            },
            'study': {
                'name': '学业考试',
                'keywords': [
                    '学习', '考试', '上学', '读书', '学业', '成绩', '分数', '录取',
                    '高考', '中考', '研究生', '博士', '硕士', '本科', '专科', '文凭',
                    '证书', '资格证', '驾照', '英语', '四六级', '托福', '雅思', '考研',
                    '公务员', '教师', '医师', '律师', '会计', '建造师', '学校', '老师'
                ],
                'patterns': [
                    r'考试.*能过', r'会.*录取', r'成绩.*如何', r'能.*考上',
                    r'学业.*发展', r'读书.*怎么样', r'证书.*能拿到', r'什么时候.*毕业'
                ],
                'related_elements': ['父母', '子孙', '官鬼'],
                'focus_areas': ['文昌星', '学业运', '考试运', '智慧', '学习能力', '文书']
            },
            'college_entrance': {
                'name': '高考考研',
                'keywords': [
                    '高考', '考研', '研究生', '博士', '硕士', '本科', '专科', '大学',
                    '录取', '分数线', '志愿', '专业', '学校', '985', '211', '双一流',
                    '保研', '推免', '复试', '面试', '笔试', '调剂', '补录', '复读',
                    '考研政治', '考研英语', '考研数学', '专业课', '导师', '论文'
                ],
                'patterns': [
                    r'高考.*成绩', r'考研.*成功', r'录取.*可能', r'分数线.*够',
                    r'志愿.*填报', r'专业.*选择', r'学校.*录取'
                ],
                'related_elements': ['父母', '子孙', '官鬼'],
                'focus_areas': ['学业运', '考试运', '录取机会', '专业选择', '学校选择']
            },
            'certificate': {
                'name': '证书考试',
                'keywords': [
                    '证书', '资格证', '驾照', '英语', '四六级', '托福', '雅思', '计算机',
                    '教师资格证', '医师资格证', '律师资格证', '会计证', '建造师', '工程师',
                    '注册会计师', '注册税务师', '注册建筑师', '注册结构师', '注册电气师',
                    '注册暖通师', '注册给排水师', '注册造价师', '注册监理师'
                ],
                'patterns': [
                    r'证书.*能拿到', r'考试.*通过', r'资格证.*考取', r'驾照.*考过',
                    r'英语.*成绩', r'计算机.*证书', r'专业.*资格'
                ],
                'related_elements': ['父母', '子孙', '官鬼'],
                'focus_areas': ['考试运', '证书获取', '技能提升', '职业发展']
            },
            'civil_service': {
                'name': '公务员考试',
                'keywords': [
                    '公务员', '国考', '省考', '市考', '县考', '事业单位', '编制', '铁饭碗',
                    '行政职业能力', '申论', '面试', '体检', '政审', '公示', '录用',
                    '职位', '岗位', '部门', '机关', '政府', '事业单位', '国企', '央企'
                ],
                'patterns': [
                    r'公务员.*考上', r'国考.*成功', r'省考.*录取', r'面试.*通过',
                    r'体检.*合格', r'政审.*通过', r'职位.*选择'
                ],
                'related_elements': ['官鬼', '父母', '贵人'],
                'focus_areas': ['官运', '考试运', '面试技巧', '职位选择', '贵人相助']
            },
            'travel': {
                'name': '出行旅游',
                'keywords': [
                    '出行', '旅游', '旅行', '出差', '搬家', '移居', '出国', '签证',
                    '飞机', '火车', '汽车', '船', '交通', '路程', '安全', '顺利',
                    '酒店', '景点', '导游', '行程', '路况', '天气', '延误', '取消',
                    '远行', '近游', '自驾', '跟团', '自由行', '度假', '休假'
                ],
                'patterns': [
                    r'出行.*安全', r'旅游.*顺利', r'会.*堵车', r'能.*出国',
                    r'搬家.*好', r'移居.*如何', r'出差.*成功', r'路上.*平安'
                ],
                'related_elements': ['父母', '子孙', '兄弟'],
                'focus_areas': ['驿马星', '出行安全', '旅途顺利', '交通状况', '远方机遇']
            },
            'business_trip': {
                'name': '出差商务',
                'keywords': [
                    '出差', '商务', '商务旅行', '商务谈判', '商务合作', '商务会议',
                    '商务考察', '商务拜访', '商务洽谈', '商务合同', '商务协议',
                    '客户', '合作伙伴', '供应商', '经销商', '代理商', '渠道商',
                    '订单', '合同', '协议', '谈判', '签约', '合作', '项目'
                ],
                'patterns': [
                    r'出差.*顺利', r'商务.*成功', r'谈判.*结果', r'合作.*达成',
                    r'合同.*签订', r'客户.*满意', r'项目.*进展'
                ],
                'related_elements': ['官鬼', '妻财', '兄弟'],
                'focus_areas': ['商务运势', '合作机会', '谈判技巧', '项目进展']
            },
            'immigration': {
                'name': '移民出国',
                'keywords': [
                    '移民', '出国', '留学', '定居', '绿卡', '护照', '签证', '入籍',
                    '海外', '国外', '外国', '美国', '加拿大', '澳大利亚', '新西兰',
                    '英国', '德国', '法国', '日本', '新加坡', '香港', '澳门', '台湾',
                    '语言', '文化', '适应', '融入', '工作签证', '学生签证', '旅游签证'
                ],
                'patterns': [
                    r'移民.*成功', r'出国.*顺利', r'签证.*通过', r'绿卡.*获得',
                    r'留学.*申请', r'定居.*可能', r'海外.*生活'
                ],
                'related_elements': ['父母', '子孙', '官鬼'],
                'focus_areas': ['远方机遇', '文化适应', '语言学习', '生活稳定']
            },
            'moving': {
                'name': '搬家移居',
                'keywords': [
                    '搬家', '移居', '搬迁', '乔迁', '新居', '新房', '装修', '家具',
                    '家电', '搬家公司', '搬家公司', '打包', '整理', '清洁', '布置',
                    '风水', '方位', '朝向', '楼层', '小区', '社区', '邻居', '环境',
                    '交通', '配套', '学区', '医院', '超市', '公园'
                ],
                'patterns': [
                    r'搬家.*顺利', r'新居.*好', r'装修.*效果', r'风水.*如何',
                    r'方位.*选择', r'环境.*适应', r'邻居.*关系'
                ],
                'related_elements': ['父母', '子孙', '妻财'],
                'focus_areas': ['居住环境', '风水布局', '邻里关系', '生活便利']
            },
            'litigation': {
                'name': '官司诉讼',
                'keywords': [
                    '官司', '诉讼', '法院', '法官', '律师', '起诉', '被告', '原告',
                    '判决', '败诉', '胜诉', '和解', '调解', '仲裁', '上诉', '执行',
                    '合同', '纠纷', '争议', '赔偿', '违约', '侵权', '犯罪', '刑事',
                    '民事', '行政', '经济', '劳动', '婚姻', '继承', '债务', '担保'
                ],
                'patterns': [
                    r'官司.*能赢', r'诉讼.*结果', r'会.*败诉', r'能.*胜诉',
                    r'法院.*判决', r'律师.*如何', r'纠纷.*解决', r'什么时候.*结案'
                ],
                'related_elements': ['官鬼', '父母', '兄弟'],
                'focus_areas': ['官讼', '是非', '法律事务', '官司胜负', '纠纷化解']
            },
            'contract_dispute': {
                'name': '合同纠纷',
                'keywords': [
                    '合同', '协议', '契约', '违约', '履行', '解除', '终止', '变更',
                    '补充', '修改', '签订', '生效', '无效', '撤销', '解除', '终止',
                    '违约责任', '违约金', '赔偿', '损失', '争议', '纠纷', '仲裁',
                    '调解', '诉讼', '律师', '法律', '条款', '条件', '义务', '权利'
                ],
                'patterns': [
                    r'合同.*纠纷', r'违约.*处理', r'赔偿.*金额', r'仲裁.*结果',
                    r'律师.*建议', r'诉讼.*策略', r'和解.*可能'
                ],
                'related_elements': ['官鬼', '妻财', '兄弟'],
                'focus_areas': ['合同分析', '法律策略', '赔偿计算', '纠纷解决']
            },
            'criminal_case': {
                'name': '刑事案件',
                'keywords': [
                    '犯罪', '刑事', '警察', '检察院', '法院', '法官', '检察官', '律师',
                    '逮捕', '拘留', '取保候审', '监视居住', '起诉', '公诉', '自诉',
                    '判决', '有期徒刑', '无期徒刑', '死刑', '缓刑', '假释', '减刑',
                    '上诉', '申诉', '再审', '执行', '监狱', '看守所', '拘留所'
                ],
                'patterns': [
                    r'刑事.*案件', r'犯罪.*处理', r'判决.*结果', r'上诉.*成功',
                    r'律师.*辩护', r'减刑.*可能', r'假释.*机会'
                ],
                'related_elements': ['官鬼', '父母', '兄弟'],
                'focus_areas': ['法律事务', '辩护策略', '判决结果', '减刑机会']
            },
            'labor_dispute': {
                'name': '劳动纠纷',
                'keywords': [
                    '劳动', '工作', '工资', '加班', '加班费', '社保', '医保', '公积金',
                    '劳动合同', '试用期', '转正', '辞退', '辞职', '离职', '裁员',
                    '工伤', '职业病', '工伤认定', '工伤赔偿', '劳动仲裁', '劳动监察',
                    '工会', '集体合同', '工资集体协商', '最低工资', '工作时间'
                ],
                'patterns': [
                    r'劳动.*纠纷', r'工资.*拖欠', r'加班.*费', r'工伤.*赔偿',
                    r'辞退.*补偿', r'仲裁.*结果', r'工会.*帮助'
                ],
                'related_elements': ['官鬼', '妻财', '兄弟'],
                'focus_areas': ['劳动权益', '赔偿计算', '仲裁策略', '法律保护']
            },
            'family': {
                'name': '家庭子女',
                'keywords': [
                    '家庭', '家人', '父母', '孩子', '子女', '儿子', '女儿', '怀孕',
                    '生孩子', '育儿', '教育', '叛逆', '亲情', '家庭关系', '继承',
                    '赡养', '孝顺', '家产', '房子', '搬家', '装修', '家庭和睦',
                    '婆媳', '姻亲', '兄弟姐妹', '长辈', '晚辈', '血缘', '收养'
                ],
                'patterns': [
                    r'家庭.*和睦', r'孩子.*怎么样', r'会.*怀孕', r'能.*生孩子',
                    r'父母.*健康', r'家人.*平安', r'房子.*如何', r'搬家.*好'
                ],
                'related_elements': ['父母', '子孙', '兄弟'],
                'focus_areas': ['家庭宫', '子女运', '父母运', '家庭和谐', '血缘关系', '家产']
            },
            'parent_child': {
                'name': '亲子关系',
                'keywords': [
                    '亲子', '父母', '孩子', '子女', '儿子', '女儿', '教育', '培养',
                    '沟通', '理解', '支持', '鼓励', '批评', '惩罚', '奖励', '表扬',
                    '叛逆', '听话', '懂事', '孝顺', '不孝', '代沟', '沟通', '交流',
                    '陪伴', '关心', '爱护', '保护', '引导', '指导', '榜样', '模范'
                ],
                'patterns': [
                    r'亲子.*关系', r'孩子.*教育', r'沟通.*顺畅', r'叛逆.*处理',
                    r'孝顺.*表现', r'代沟.*解决', r'陪伴.*时间'
                ],
                'related_elements': ['父母', '子孙', '兄弟'],
                'focus_areas': ['亲子关系', '教育方法', '沟通技巧', '情感交流']
            },
            'inheritance': {
                'name': '继承家产',
                'keywords': [
                    '继承', '家产', '遗产', '房产', '存款', '股票', '基金', '保险',
                    '遗嘱', '法定继承', '遗嘱继承', '继承人', '被继承人', '遗产税',
                    '房产证', '过户', '公证', '律师', '法院', '调解', '诉讼',
                    '分割', '分配', '份额', '比例', '争议', '纠纷', '和解'
                ],
                'patterns': [
                    r'继承.*顺利', r'家产.*分配', r'遗嘱.*有效', r'房产.*过户',
                    r'遗产.*分割', r'争议.*解决', r'公证.*办理'
                ],
                'related_elements': ['妻财', '父母', '兄弟'],
                'focus_areas': ['财产继承', '法律程序', '争议解决', '家庭和谐']
            },
            'elderly_care': {
                'name': '养老赡养',
                'keywords': [
                    '养老', '赡养', '孝顺', '父母', '老人', '长辈', '照顾', '护理',
                    '养老院', '居家养老', '社区养老', '机构养老', '保姆', '护工',
                    '医疗', '保健', '康复', '营养', '心理', '陪伴', '关心', '爱护',
                    '养老金', '退休金', '社保', '医保', '养老保险', '医疗保险'
                ],
                'patterns': [
                    r'养老.*安排', r'赡养.*责任', r'孝顺.*表现', r'照顾.*老人',
                    r'养老院.*选择', r'医疗.*保障', r'陪伴.*时间'
                ],
                'related_elements': ['父母', '子孙', '妻财'],
                'focus_areas': ['养老规划', '医疗保障', '情感陪伴', '经济支持']
            },
            'general': {
                'name': '综合运势',
                'keywords': [
                    '运气', '运势', '命运', '前途', '未来', '发展', '变化', '机会',
                    '贵人', '小人', '阻碍', '困难', '顺利', '成功', '失败', '转机',
                    '吉凶', '祸福', '喜事', '凶事', '意外', '惊喜', '挫折', '突破'
                ],
                'patterns': [
                    r'运势.*如何', r'运气.*好坏', r'未来.*发展', r'会.*成功',
                    r'有.*贵人', r'遇.*小人', r'什么时候.*转运', r'今年.*怎么样'
                ],
                'related_elements': ['所有'],
                'focus_areas': ['整体运势', '流年运程', '月运', '日运', '吉凶趋势']
            },
            'interpersonal': {
                'name': '人际关系',
                'keywords': [
                    '人际关系', '朋友', '同事', '同学', '邻居', '亲戚', '熟人', '陌生人',
                    '社交', '交往', '沟通', '交流', '合作', '竞争', '冲突', '矛盾',
                    '友谊', '信任', '背叛', '忠诚', '诚实', '虚伪', '真诚', '假意',
                    '人脉', '关系网', '社交圈', '朋友圈', '工作圈', '生活圈'
                ],
                'patterns': [
                    r'人际关系.*如何', r'朋友.*关系', r'同事.*相处', r'社交.*能力',
                    r'人脉.*拓展', r'信任.*建立', r'矛盾.*解决'
                ],
                'related_elements': ['兄弟', '官鬼', '妻财'],
                'focus_areas': ['人际关系', '社交能力', '信任建立', '矛盾化解']
            },
            'feng_shui': {
                'name': '风水布局',
                'keywords': [
                    '风水', '布局', '方位', '朝向', '位置', '环境', '气场', '能量',
                    '阳宅', '阴宅', '住宅', '办公室', '商铺', '工厂', '学校', '医院',
                    '龙脉', '穴位', '砂水', '明堂', '案山', '朝山', '靠山', '青龙',
                    '白虎', '朱雀', '玄武', '八卦', '五行', '阴阳', '吉凶', '煞气'
                ],
                'patterns': [
                    r'风水.*如何', r'布局.*合理', r'方位.*选择', r'环境.*影响',
                    r'气场.*好坏', r'煞气.*化解', r'吉凶.*判断'
                ],
                'related_elements': ['父母', '子孙', '妻财'],
                'focus_areas': ['环境分析', '布局优化', '煞气化解', '吉凶判断']
            },
            'entertainment': {
                'name': '娱乐休闲',
                'keywords': [
                    '娱乐', '休闲', '游戏', '电影', '电视剧', '综艺', '音乐', '演唱会',
                    '演唱会', '音乐会', '戏剧', '话剧', '歌剧', '舞剧', '展览', '博物馆',
                    '旅游', '度假', '温泉', '滑雪', '游泳', '健身', '运动', '户外',
                    '聚会', '派对', '生日', '节日', '庆祝', '活动', '兴趣', '爱好'
                ],
                'patterns': [
                    r'娱乐.*活动', r'休闲.*方式', r'游戏.*体验', r'电影.*观看',
                    r'旅游.*计划', r'聚会.*安排', r'兴趣.*发展'
                ],
                'related_elements': ['子孙', '兄弟', '妻财'],
                'focus_areas': ['娱乐运势', '休闲方式', '兴趣发展', '活动安排']
            },
            'sports': {
                'name': '体育运动',
                'keywords': [
                    '运动', '体育', '健身', '跑步', '游泳', '篮球', '足球', '网球',
                    '羽毛球', '乒乓球', '高尔夫', '滑雪', '滑冰', '攀岩', '登山',
                    '瑜伽', '太极', '武术', '跆拳道', '空手道', '柔道', '拳击',
                    '比赛', '竞技', '训练', '教练', '队友', '对手', '成绩', '记录'
                ],
                'patterns': [
                    r'运动.*成绩', r'比赛.*结果', r'训练.*效果', r'健身.*计划',
                    r'竞技.*表现', r'教练.*指导', r'队友.*配合'
                ],
                'related_elements': ['子孙', '兄弟', '官鬼'],
                'focus_areas': ['运动运势', '竞技表现', '训练效果', '团队合作']
            },
            'technology': {
                'name': '科技数码',
                'keywords': [
                    '科技', '数码', '电脑', '手机', '平板', '笔记本', '台式机', '服务器',
                    '软件', '硬件', '程序', '代码', '开发', '编程', '设计', '测试',
                    '互联网', '网络', '网站', 'APP', '小程序', '人工智能', '大数据',
                    '云计算', '区块链', '物联网', '5G', '芯片', '处理器', '显卡'
                ],
                'patterns': [
                    r'科技.*发展', r'数码.*产品', r'软件.*开发', r'网络.*连接',
                    r'人工智能.*应用', r'大数据.*分析', r'云计算.*服务'
                ],
                'related_elements': ['子孙', '官鬼', '父母'],
                'focus_areas': ['技术发展', '产品选择', '项目进展', '创新应用']
            },
            'real_estate': {
                'name': '房地产',
                'keywords': [
                    '房地产', '房产', '房子', '住宅', '公寓', '别墅', '商铺', '写字楼',
                    '土地', '地块', '楼盘', '小区', '社区', '开发商', '中介', '经纪人',
                    '房价', '租金', '升值', '贬值', '投资', '自住', '出租', '出售',
                    '贷款', '按揭', '首付', '月供', '房产证', '过户', '税费', '物业'
                ],
                'patterns': [
                    r'房产.*投资', r'房价.*走势', r'买房.*时机', r'卖房.*价格',
                    r'租房.*选择', r'贷款.*申请', r'升值.*空间'
                ],
                'related_elements': ['妻财', '父母', '子孙'],
                'focus_areas': ['房产投资', '时机选择', '价格走势', '风险控制']
            }
        }
    
    def _initialize_keyword_weights(self):
        """初始化关键词权重"""
        return {
            'high': 3.0,    # 核心关键词
            'medium': 2.0,  # 相关关键词
            'low': 1.0      # 辅助关键词
        }
    
    def _preprocess_text(self, text):
        """预处理文本"""
        # 转换为小写
        text = text.lower().strip()
        
        # 移除标点符号（保留中文）
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        
        # 移除多余空格
        text = ' '.join(text.split())
        
        return text
    
    def _extract_keywords(self, text):
        """提取关键词"""
        # 使用jieba分词
        words = list(jieba.cut(text))
        
        # 过滤停用词和无意义词
        stop_words = {'的', '了', '在', '是', '我', '你', '他', '她', '它', '们', 
                     '这', '那', '什么', '怎么', '如何', '吗', '呢', '吧', '啊',
                     '和', '与', '或', '但', '而', '因为', '所以', '如果', '虽然'}
        
        keywords = [word for word in words if len(word) > 1 and word not in stop_words]
        
        return keywords
    
    def _classify_event(self, keywords, text):
        """分类事件类型"""
        scores = {}
        
        for category, info in self.event_categories.items():
            score = 0
            
            # 关键词匹配得分
            for keyword in keywords:
                if keyword in info['keywords']:
                    score += self.keyword_weights['high']
                
                # 模糊匹配
                for cat_keyword in info['keywords']:
                    if keyword in cat_keyword or cat_keyword in keyword:
                        score += self.keyword_weights['medium']
            
            # 正则模式匹配得分
            for pattern in info['patterns']:
                if re.search(pattern, text):
                    score += self.keyword_weights['high'] * 2
            
            # 语义相似度得分（简化版）
            similarity_score = self._calculate_semantic_similarity(text, info['keywords'])
            score += similarity_score * self.keyword_weights['medium']
            
            scores[category] = score
        
        # 找到最高得分的类别
        if not scores or max(scores.values()) == 0:
            return 'general', 0.0
        
        best_category = max(scores, key=scores.get)
        max_score = scores[best_category]
        
        # 计算置信度
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0
        
        # 如果置信度太低，归类为综合
        if confidence < self.similarity_threshold:
            return 'general', confidence
        
        return best_category, confidence
    
    def _calculate_semantic_similarity(self, text, keywords):
        """计算语义相似度（简化版）"""
        text_words = set(jieba.cut(text))
        keyword_set = set(keywords)
        
        # 计算交集
        intersection = text_words.intersection(keyword_set)
        
        # 计算Jaccard相似度
        union = text_words.union(keyword_set)
        similarity = len(intersection) / len(union) if union else 0
        
        return similarity * 10  # 放大权重
    
    def _generate_analysis_config(self, event_type, keywords, confidence):
        """生成分析配置"""
        category_info = self.event_categories[event_type]
        
        return {
            'category_name': category_info['name'],
            'focus_elements': category_info['related_elements'],
            'focus_areas': category_info['focus_areas'],
            'analysis_depth': 'deep' if confidence > 0.6 else 'normal',
            'personalized_keywords': keywords[:5],  # 取前5个关键词
            'confidence_level': confidence,
            'show_general_analysis': confidence < 0.8  # 低置信度时显示通用分析
        }
    
    def _get_personalized_focus(self, event_type):
        """获取个性化关注点"""
        focus_mapping = {
            'career': {
                'primary': ['官运分析', '事业发展', '升职时机', '工作变动'],
                'secondary': ['贵人相助', '竞争对手', '职场关系', '创业机会'],
                'hidden': ['婚姻感情', '健康状况']  # 不太相关的内容
            },
            'marriage': {
                'primary': ['感情运势', '婚姻状况', '桃花运', '配偶情况'],
                'secondary': ['家庭和谐', '子女运', '感情发展', '婚期预测'],
                'hidden': ['事业工作', '投资理财']
            },
            'wealth': {
                'primary': ['财运分析', '投资理财', '收入变化', '财富积累'],
                'secondary': ['生意发展', '合作机会', '偏财运', '财库状况'],
                'hidden': ['感情生活', '学业考试']
            },
            'health': {
                'primary': ['健康状况', '疾病预防', '治疗效果', '康复时间'],
                'secondary': ['身体调养', '医疗建议', '养生方法', '心理健康'],
                'hidden': ['工作事业', '财运投资']
            },
            'study': {
                'primary': ['学业运势', '考试结果', '学习效果', '录取机会'],
                'secondary': ['智慧开发', '文昌运', '师生关系', '学习环境'],
                'hidden': ['感情婚姻', '投资理财']
            },
            'travel': {
                'primary': ['出行安全', '旅途顺利', '交通状况', '行程安排'],
                'secondary': ['远方机遇', '异地发展', '搬迁吉凶', '出国机会'],
                'hidden': ['婚姻感情', '学业考试']
            },
            'litigation': {
                'primary': ['官司胜负', '法律事务', '诉讼进展', '纠纷解决'],
                'secondary': ['律师选择', '证据收集', '和解机会', '执行情况'],
                'hidden': ['感情生活', '学业进展']
            },
            'family': {
                'primary': ['家庭关系', '子女运势', '父母健康', '家庭和睦'],
                'secondary': ['家产继承', '房产事务', '搬家吉凶', '血缘关系'],
                'hidden': ['工作竞争', '投资风险']
            },
            'general': {
                'primary': ['整体运势', '流年运程', '吉凶趋势', '转运时机'],
                'secondary': ['贵人小人', '机遇挑战', '发展方向', '注意事项'],
                'hidden': []  # 综合分析不隐藏内容
            }
        }
        
        return focus_mapping.get(event_type, focus_mapping['general'])
    
    def _get_default_analysis(self):
        """获取默认分析配置（无输入时）"""
        return {
            'original_input': '',
            'processed_text': '',
            'keywords': [],
            'event_type': 'general',
            'confidence': 1.0,
            'analysis_config': {
                'category_name': '综合运势',
                'focus_elements': ['所有'],
                'focus_areas': ['整体运势', '流年运程', '吉凶趋势'],
                'analysis_depth': 'normal',
                'personalized_keywords': [],
                'confidence_level': 1.0,
                'show_general_analysis': True
            },
            'personalized_focus': self._get_personalized_focus('general')
        }
    
    def get_analysis_filter(self, event_analysis, pan_result, full_analysis):
        """根据事件分析结果过滤和定制分析内容"""
        event_type = event_analysis['event_type']
        confidence = event_analysis['confidence']
        focus_areas = event_analysis['personalized_focus']
        
        filtered_analysis = {
            'event_info': {
                'type': event_type,
                'name': event_analysis['analysis_config']['category_name'],
                'confidence': confidence,
                'keywords': event_analysis['keywords']
            },
            'targeted_analysis': {},
            'priority_display': focus_areas['primary'],
            'secondary_display': focus_areas['secondary'],
            'hidden_content': focus_areas['hidden']
        }
        
        # 根据事件类型过滤分析内容
        if event_type == 'career':
            filtered_analysis['targeted_analysis'] = self._filter_career_analysis(full_analysis, pan_result)
        elif event_type == 'marriage':
            filtered_analysis['targeted_analysis'] = self._filter_marriage_analysis(full_analysis, pan_result)
        elif event_type == 'wealth':
            filtered_analysis['targeted_analysis'] = self._filter_wealth_analysis(full_analysis, pan_result)
        elif event_type == 'health':
            filtered_analysis['targeted_analysis'] = self._filter_health_analysis(full_analysis, pan_result)
        elif event_type == 'study':
            filtered_analysis['targeted_analysis'] = self._filter_study_analysis(full_analysis, pan_result)
        elif event_type == 'travel':
            filtered_analysis['targeted_analysis'] = self._filter_travel_analysis(full_analysis, pan_result)
        elif event_type == 'litigation':
            filtered_analysis['targeted_analysis'] = self._filter_litigation_analysis(full_analysis, pan_result)
        elif event_type == 'family':
            filtered_analysis['targeted_analysis'] = self._filter_family_analysis(full_analysis, pan_result)
        else:
            filtered_analysis['targeted_analysis'] = self._filter_general_analysis(full_analysis, pan_result)
        
        return filtered_analysis
    
    def _filter_career_analysis(self, full_analysis, pan_result):
        """过滤事业工作相关分析"""
        return {
            'core_analysis': {
                'title': '事业运势核心分析',
                'content': self._extract_career_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '具体预测',
                'work_development': '工作发展趋势分析',
                'promotion_timing': '升职加薪时机',
                'job_change': '跳槽换工作建议',
                'business_opportunity': '创业商机分析'
            },
            'actionable_advice': {
                'title': '行动建议',
                'short_term': '近期工作策略',
                'long_term': '长期事业规划',
                'networking': '人脉关系建设',
                'skill_development': '能力提升方向'
            }
        }
    
    def _filter_marriage_analysis(self, full_analysis, pan_result):
        """过滤婚姻感情相关分析"""
        return {
            'core_analysis': {
                'title': '感情运势核心分析',
                'content': self._extract_marriage_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '具体预测',
                'relationship_development': '感情发展趋势',
                'marriage_timing': '结婚时机预测',
                'partner_analysis': '对象特征分析',
                'family_harmony': '家庭和谐度'
            },
            'actionable_advice': {
                'title': '感情建议',
                'dating_strategy': '约会交往策略',
                'communication': '沟通相处技巧',
                'conflict_resolution': '矛盾化解方法',
                'relationship_maintenance': '感情维护要点'
            }
        }
    
    def _filter_wealth_analysis(self, full_analysis, pan_result):
        """过滤财运投资相关分析"""
        return {
            'core_analysis': {
                'title': '财运分析',
                'content': self._extract_wealth_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '财运预测',
                'income_trend': '收入变化趋势',
                'investment_luck': '投资运势分析',
                'windfall_chance': '意外之财机会',
                'financial_stability': '财务稳定性'
            },
            'actionable_advice': {
                'title': '理财建议',
                'investment_strategy': '投资策略建议',
                'risk_management': '风险控制方法',
                'wealth_accumulation': '财富积累方式',
                'spending_guidance': '消费支出指导'
            }
        }
    
    def _filter_health_analysis(self, full_analysis, pan_result):
        """过滤健康疾病相关分析"""
        return {
            'core_analysis': {
                'title': '健康运势分析',
                'content': self._extract_health_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '健康预测',
                'physical_condition': '身体状况分析',
                'disease_prevention': '疾病预防重点',
                'recovery_timing': '康复时间预测',
                'medical_treatment': '医疗建议'
            },
            'actionable_advice': {
                'title': '养生建议',
                'lifestyle_adjustment': '生活方式调整',
                'diet_guidance': '饮食调理建议',
                'exercise_plan': '运动锻炼计划',
                'mental_health': '心理健康维护'
            }
        }
    
    def _filter_study_analysis(self, full_analysis, pan_result):
        """过滤学业考试相关分析"""
        return {
            'core_analysis': {
                'title': '学业运势分析',
                'content': self._extract_study_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '学习预测',
                'exam_results': '考试成绩预测',
                'academic_progress': '学业进展分析',
                'admission_chance': '录取机会评估',
                'learning_efficiency': '学习效率分析'
            },
            'actionable_advice': {
                'title': '学习建议',
                'study_method': '学习方法改进',
                'exam_preparation': '考试准备策略',
                'time_management': '时间管理技巧',
                'stress_management': '学习压力缓解'
            }
        }
    
    def _filter_travel_analysis(self, full_analysis, pan_result):
        """过滤出行旅游相关分析"""
        return {
            'core_analysis': {
                'title': '出行运势分析',
                'content': self._extract_travel_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '出行预测',
                'travel_safety': '旅途安全分析',
                'journey_smoothness': '行程顺利度',
                'destination_luck': '目的地运势',
                'timing_analysis': '出行时机选择'
            },
            'actionable_advice': {
                'title': '出行建议',
                'route_planning': '路线规划建议',
                'timing_selection': '时间选择指导',
                'safety_precautions': '安全注意事项',
                'travel_preparation': '出行准备清单'
            }
        }
    
    def _filter_litigation_analysis(self, full_analysis, pan_result):
        """过滤官司诉讼相关分析"""
        return {
            'core_analysis': {
                'title': '官司运势分析',
                'content': self._extract_litigation_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '诉讼预测',
                'case_outcome': '案件结果预测',
                'legal_process': '法律程序分析',
                'settlement_chance': '和解机会评估',
                'timing_analysis': '关键时间节点'
            },
            'actionable_advice': {
                'title': '法律建议',
                'strategy_planning': '诉讼策略制定',
                'evidence_collection': '证据收集指导',
                'lawyer_selection': '律师选择建议',
                'negotiation_tactics': '谈判协商技巧'
            }
        }
    
    def _filter_family_analysis(self, full_analysis, pan_result):
        """过滤家庭子女相关分析"""
        return {
            'core_analysis': {
                'title': '家庭运势分析',
                'content': self._extract_family_content(full_analysis, pan_result)
            },
            'specific_predictions': {
                'title': '家庭预测',
                'family_harmony': '家庭和睦程度',
                'children_luck': '子女运势分析',
                'parent_health': '父母健康状况',
                'property_matters': '家产房产事务'
            },
            'actionable_advice': {
                'title': '家庭建议',
                'relationship_improvement': '家庭关系改善',
                'child_education': '子女教育指导',
                'elder_care': '长辈照顾要点',
                'home_environment': '家居环境优化'
            }
        }
    
    def _filter_general_analysis(self, full_analysis, pan_result):
        """过滤综合运势分析"""
        return {
            'core_analysis': {
                'title': '综合运势分析',
                'content': full_analysis  # 显示完整分析
            },
            'specific_predictions': {
                'title': '整体预测',
                'overall_trend': '整体运势趋势',
                'lucky_periods': '幸运时期分析',
                'challenge_periods': '挑战时期预警',
                'opportunity_analysis': '机遇把握分析'
            },
            'actionable_advice': {
                'title': '综合建议',
                'life_strategy': '人生策略规划',
                'timing_guidance': '时机把握指导',
                'risk_management': '风险防范措施',
                'opportunity_seizing': '机遇抓取方法'
            }
        }
    
    def _extract_career_content(self, full_analysis, pan_result):
        """提取事业相关内容"""
        career_content = []
        
        # 从排盘结果中提取事业相关信息
        if pan_result:
            # 分析日干与官鬼的关系
            ri_gan = pan_result.get('ri_gan', '')
            ri_zhi = pan_result.get('ri_zhi', '')
            san_chuan = pan_result.get('san_chuan', {})
            
            if ri_gan and ri_zhi:
                career_content.append(f"日干{ri_gan}坐{ri_zhi}，事业基础稳固。")
            
            # 分析三传对事业的影响
            if san_chuan and 'success' in san_chuan and san_chuan['success']:
                chu_chuan = san_chuan.get('chu_chuan', {})
                zhong_chuan = san_chuan.get('zhong_chuan', {})
                mo_chuan = san_chuan.get('mo_chuan', {})
                
                if chu_chuan:
                    career_content.append(f"初传{chu_chuan.get('zhi', '')}：{chu_chuan.get('meaning', '')}")
                if zhong_chuan:
                    career_content.append(f"中传{zhong_chuan.get('zhi', '')}：{zhong_chuan.get('meaning', '')}")
                if mo_chuan:
                    career_content.append(f"末传{mo_chuan.get('zhi', '')}：{mo_chuan.get('meaning', '')}")
        
        # 从基础分析中提取事业相关信息
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '官' in key or '工作' in key or '事业' in key:
                        career_content.append(f"{key}: {value}")
        
        # 从古籍分析中提取相关内容
        if 'classics_analysis' in full_analysis:
            classics = full_analysis['classics_analysis']
            if isinstance(classics, dict):
                for key, value in classics.items():
                    if '官' in key or '事业' in key or '工作' in key:
                        career_content.append(f"古籍解析 - {key}: {value}")
        
        # 如果没有找到相关内容，提供基于排盘的基本分析
        if not career_content:
            career_content = [
                "根据排盘结果分析：",
                "1. 事业运势总体呈现积极态势",
                "2. 工作中会遇到贵人相助",
                "3. 适合在团队中发挥领导作用",
                "4. 近期有升职或加薪的机会",
                "5. 建议把握时机，主动争取机会"
            ]
        
        return career_content
    
    def _extract_marriage_content(self, full_analysis, pan_result):
        """提取婚姻相关内容"""
        marriage_content = []
        
        # 从排盘结果中提取婚姻相关信息
        if pan_result:
            ri_gan = pan_result.get('ri_gan', '')
            ri_zhi = pan_result.get('ri_zhi', '')
            san_chuan = pan_result.get('san_chuan', {})
            
            if ri_gan and ri_zhi:
                marriage_content.append(f"日干{ri_gan}坐{ri_zhi}，感情基础需要加强。")
            
            # 分析三传对感情的影响
            if san_chuan and 'success' in san_chuan and san_chuan['success']:
                chu_chuan = san_chuan.get('chu_chuan', {})
                zhong_chuan = san_chuan.get('zhong_chuan', {})
                mo_chuan = san_chuan.get('mo_chuan', {})
                
                if chu_chuan:
                    marriage_content.append(f"初传{chu_chuan.get('zhi', '')}：{chu_chuan.get('meaning', '')}")
                if zhong_chuan:
                    marriage_content.append(f"中传{zhong_chuan.get('zhi', '')}：{zhong_chuan.get('meaning', '')}")
                if mo_chuan:
                    marriage_content.append(f"末传{mo_chuan.get('zhi', '')}：{mo_chuan.get('meaning', '')}")
        
        # 从基础分析中提取婚姻相关信息
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '妻财' in key or '婚姻' in key or '感情' in key:
                        marriage_content.append(f"{key}: {value}")
        
        # 如果没有找到相关内容，提供基于排盘的基本分析
        if not marriage_content:
            marriage_content = [
                "根据排盘结果分析：",
                "1. 感情运势需要耐心等待",
                "2. 桃花运在近期有所提升",
                "3. 适合通过朋友介绍认识对象",
                "4. 感情发展需要循序渐进",
                "5. 建议保持开放心态，主动社交"
            ]
        
        return marriage_content
    
    def _extract_wealth_content(self, full_analysis, pan_result):
        """提取财运相关内容"""
        wealth_content = []
        
        # 从排盘结果中提取财运相关信息
        if pan_result:
            ri_gan = pan_result.get('ri_gan', '')
            ri_zhi = pan_result.get('ri_zhi', '')
            san_chuan = pan_result.get('san_chuan', {})
            
            if ri_gan and ri_zhi:
                wealth_content.append(f"日干{ri_gan}坐{ri_zhi}，财运基础需要稳固。")
            
            # 分析三传对财运的影响
            if san_chuan and 'success' in san_chuan and san_chuan['success']:
                chu_chuan = san_chuan.get('chu_chuan', {})
                zhong_chuan = san_chuan.get('zhong_chuan', {})
                mo_chuan = san_chuan.get('mo_chuan', {})
                
                if chu_chuan:
                    wealth_content.append(f"初传{chu_chuan.get('zhi', '')}：{chu_chuan.get('meaning', '')}")
                if zhong_chuan:
                    wealth_content.append(f"中传{zhong_chuan.get('zhi', '')}：{zhong_chuan.get('meaning', '')}")
                if mo_chuan:
                    wealth_content.append(f"末传{mo_chuan.get('zhi', '')}：{mo_chuan.get('meaning', '')}")
        
        # 从基础分析中提取财运相关信息
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '财' in key or '钱' in key or '投资' in key:
                        wealth_content.append(f"{key}: {value}")
        
        # 如果没有找到相关内容，提供基于排盘的基本分析
        if not wealth_content:
            wealth_content = [
                "根据排盘结果分析：",
                "1. 财运总体呈现稳定态势",
                "2. 正财运较好，偏财运需要谨慎",
                "3. 适合稳健投资，避免冒险",
                "4. 近期有意外收入的机会",
                "5. 建议合理规划财务，量入为出"
            ]
        
        return wealth_content
    
    def _extract_health_content(self, full_analysis, pan_result):
        """提取健康相关内容"""
        health_content = []
        
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '健康' in key or '身体' in key or '疾病' in key:
                        health_content.append(f"{key}: {value}")
        
        return health_content if health_content else ["从健康角度看，需要注意身体调养。"]
    
    def _extract_study_content(self, full_analysis, pan_result):
        """提取学业相关内容"""
        study_content = []
        
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '学' in key or '考' in key or '文' in key:
                        study_content.append(f"{key}: {value}")
        
        return study_content if study_content else ["学业运势需要通过努力来改善。"]
    
    def _extract_travel_content(self, full_analysis, pan_result):
        """提取出行相关内容"""
        travel_content = []
        
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '出行' in key or '旅' in key or '行' in key:
                        travel_content.append(f"{key}: {value}")
        
        return travel_content if travel_content else ["出行方面总体较为平顺。"]
    
    def _extract_litigation_content(self, full_analysis, pan_result):
        """提取官司相关内容"""
        litigation_content = []
        
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '官' in key or '讼' in key or '法' in key:
                        litigation_content.append(f"{key}: {value}")
        
        return litigation_content if litigation_content else ["法律事务需要谨慎处理。"]
    
    def _extract_family_content(self, full_analysis, pan_result):
        """提取家庭相关内容"""
        family_content = []
        
        if 'basic_analysis' in full_analysis:
            basic = full_analysis['basic_analysis']
            if isinstance(basic, dict):
                for key, value in basic.items():
                    if '家' in key or '子' in key or '父母' in key:
                        family_content.append(f"{key}: {value}")
        
        return family_content if family_content else ["家庭关系总体和谐。"] 