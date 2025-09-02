from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
from core.liu_ren import LiuRenPan
from core.analysis import LiuRenAnalysis
from core.event_analyzer import EventAnalyzer
from data.classics import ClassicsDatabase
from data.modern import ModernTheory

app = Flask(__name__)

# 初始化数据库和分析器
classics_db = ClassicsDatabase()
modern_theory = ModernTheory()
event_analyzer = EventAnalyzer()

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """计算大六壬排盘"""
    try:
        data = request.get_json()
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
        hour = int(data['hour'])
        minute = int(data['minute'])
        
        # 获取用户询问的事件
        user_question = data.get('question', '').strip()
        
        # 获取求测人信息
        user_info = data.get('user_info', {})
        birth_year = user_info.get('birth_year', year)
        birth_month = user_info.get('birth_month', month)
        birth_day = user_info.get('birth_day', day)
        birth_hour = user_info.get('birth_hour', hour)
        
        # 验证日期范围
        if year < 1900 or year > 2100:
            return jsonify({
                'success': False,
                'error': '年份必须在1900-2100之间'
            })
        if month < 1 or month > 12:
            return jsonify({
                'success': False,
                'error': '月份必须在1-12之间'
            })
        if day < 1 or day > 31:
            return jsonify({
                'success': False,
                'error': '日期必须在1-31之间'
            })
        if hour < 0 or hour > 23:
            return jsonify({
                'success': False,
                'error': '小时必须在0-23之间'
            })
        if minute < 0 or minute > 59:
            return jsonify({
                'success': False,
                'error': '分钟必须在0-59之间'
            })
        
        # 创建排盘对象并计算
        pan = LiuRenPan(year, month, day, hour, minute)
        result = pan.calculate()
        
        # 计算年命和行年
        result['user_info'] = {
            'birth_year': birth_year,
            'birth_month': birth_month,
            'birth_day': birth_day,
            'birth_hour': birth_hour,
            'nian_ming': calculate_nian_ming(birth_year, birth_month, birth_day, birth_hour),
            'xing_nian': calculate_xing_nian(birth_year, year)
        }
        
        # 分析用户询问的事件
        event_analysis = event_analyzer.analyze_event(user_question)
        
        # 进行解析
        analysis = LiuRenAnalysis()
        full_analysis = analysis.analyze(result)
        
        # 根据事件类型过滤和个性化分析结果
        filtered_analysis = event_analyzer.get_analysis_filter(
            event_analysis, result, full_analysis
        )
        
        # 获取事件相关的古籍分析
        event_type = event_analysis.get('analysis_config', {}).get('category', 'general')
        classics_analysis = classics_db.get_event_specific_classics(event_type, result)
        
        return jsonify({
            'success': True,
            'pan': result,
            'analysis': full_analysis,
            'event_analysis': event_analysis,
            'targeted_analysis': filtered_analysis,
            'classics_analysis': classics_analysis
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'日期格式错误: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'计算失败: {str(e)}'
        })

@app.route('/classics')
def classics():
    """古籍查询页面"""
    return render_template('classics.html')

@app.route('/theory')
def theory():
    """现代理论页面"""
    return jsonify(modern_theory.get_all_theories())

@app.route('/api/classics/<category>')
def get_classics(category):
    """获取古籍内容API"""
    try:
        content = classics_db.get_all_content(category)
        return jsonify(content)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/classics/all')
def get_all_classics():
    """获取所有古籍内容API"""
    try:
        content = classics_db.get_all_theories()
        return jsonify(content)
    except Exception as e:
        return jsonify({'error': str(e)})

def calculate_nian_ming(birth_year, birth_month, birth_day, birth_hour):
    """计算年命"""
    # 简化计算，实际应该根据农历计算
    gan_zhi = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
               '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
               '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
               '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
               '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
               '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']
    
    # 计算年干支
    year_index = (birth_year - 4) % 60
    year_gz = gan_zhi[year_index]
    
    # 计算月干支（简化）
    month_gz = gan_zhi[(year_index * 12 + birth_month - 1) % 60]
    
    # 计算日干支（简化）
    day_gz = gan_zhi[(year_index * 365 + birth_month * 30 + birth_day - 1) % 60]
    
    # 计算时干支
    hour_gz = gan_zhi[(year_index * 24 + birth_hour // 2) % 60]
    
    return {
        'year_gz': year_gz,
        'month_gz': month_gz,
        'day_gz': day_gz,
        'hour_gz': hour_gz,
        'description': f'年命：{year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时'
    }

def calculate_xing_nian(birth_year, current_year):
    """计算行年"""
    age = current_year - birth_year
    if age < 0:
        age = 0
    
    # 行年计算（简化）
    xing_nian = age + 1
    
    return {
        'age': age,
        'xing_nian': xing_nian,
        'description': f'行年：{xing_nian}岁（虚岁）'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
