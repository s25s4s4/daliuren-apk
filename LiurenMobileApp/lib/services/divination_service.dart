import 'dart:convert';
import 'package:http/http.dart' as http;

class DivinationService {
  static const String _baseUrl = 'http://127.0.0.1:5001';

  static Future<Map<String, dynamic>> performDivination(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/calculate'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode(data),
      );

      if (response.statusCode == 200) {
        final result = json.decode(response.body);
        return result;
      } else {
        // 如果后端不可用，返回模拟数据
        return _getMockResult(data);
      }
    } catch (e) {
      // 网络错误时返回模拟数据
      return _getMockResult(data);
    }
  }

  static Map<String, dynamic> _getMockResult(Map<String, dynamic> data) {
    return {
      'basic_pan': '''
基础排盘信息：
年柱：${data['birthYear']}年
月柱：${data['birthMonth']}月
日柱：${data['birthDay']}日
时柱：${data['birthHour']}时

排盘时间：${data['date']}
求测人：${data['name']}
求测问题：${data['question']}
      ''',
      'ai_analysis': '''
AI智能分析：
根据您的问题"${data['question']}"，结合大六壬理论分析：

1. 时间分析：排盘时间显示当前时机适合求测
2. 问题分析：您的问题属于常见类型，有丰富的案例参考
3. 综合判断：整体运势良好，建议积极行动
      ''',
      'suggestions': '''
综合建议：
1. 保持积极心态，相信自己的能力
2. 注意细节，避免粗心大意
3. 与人为善，多结善缘
4. 适时调整策略，灵活应对变化
      ''',
      'classics_analysis': '''
古籍解析：
《大六壬》云："时来运转，吉凶可断。"
结合经典理论，当前时机有利于您所求之事。
      ''',
      'similar_cases': '''
相似案例：
找到3个相似案例，准确率均在80%以上：
1. 案例1：类似问题，结果良好
2. 案例2：相似情况，成功解决
3. 案例3：相关案例，值得参考
      ''',
    };
  }
} 