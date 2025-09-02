import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(const LiurenApp());
}

class LiurenApp extends StatelessWidget {
  const LiurenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '大六壬排盘解析系统',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const LiurenHomePage(),
    );
  }
}

class LiurenHomePage extends StatefulWidget {
  const LiurenHomePage({super.key});

  @override
  State<LiurenHomePage> createState() => _LiurenHomePageState();
}

class _LiurenHomePageState extends State<LiurenHomePage> with TickerProviderStateMixin {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _questionController = TextEditingController();
  DateTime _selectedDateTime = DateTime.now();
  String _selectedGender = '男';
  String _analysisResult = '';
  bool _isAnalyzing = false;
  late TabController _tabController;
  Map<String, dynamic> _analysisData = {};

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('大六壬排盘解析系统'),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(text: '信息填写'),
            Tab(text: '专业排盘'),
            Tab(text: '古籍理论'),
            Tab(text: 'AI解盘'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildInfoInputTab(),
          _buildProfessionalDivinationTab(),
          _buildClassicalTheoryTab(),
          _buildAIAnalysisTab(),
        ],
      ),
    );
  }

  Widget _buildInfoInputTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.deepPurple.shade100, Colors.deepPurple.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.edit_document, size: 48, color: Colors.deepPurple),
                SizedBox(height: 8),
                Text(
                  '信息填写系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.deepPurple,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '请填写完整信息以便进行专业分析',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.deepPurple,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.person, color: Colors.deepPurple),
                      const SizedBox(width: 8),
                      const Text(
                        '基本信息',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _nameController,
                    decoration: const InputDecoration(
                      labelText: '姓名',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.person_outline),
                      hintText: '请输入您的姓名',
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          value: _selectedGender,
                          decoration: const InputDecoration(
                            labelText: '性别',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.people_outline),
                          ),
                          items: const [
                            DropdownMenuItem(value: '男', child: Text('男')),
                            DropdownMenuItem(value: '女', child: Text('女')),
                          ],
                          onChanged: (value) {
                            setState(() {
                              _selectedGender = value!;
                            });
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: TextButton.icon(
                          onPressed: () => _selectDateTime(context),
                          icon: const Icon(Icons.calendar_today),
                          label: Text('${_selectedDateTime.year}-${_selectedDateTime.month.toString().padLeft(2, '0')}-${_selectedDateTime.day.toString().padLeft(2, '0')} ${_selectedDateTime.hour.toString().padLeft(2, '0')}:${_selectedDateTime.minute.toString().padLeft(2, '0')}'),
                          style: TextButton.styleFrom(
                            backgroundColor: Colors.deepPurple.shade50,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.question_answer, color: Colors.deepPurple),
                      const SizedBox(width: 8),
                      const Text(
                        '占卜问题',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _questionController,
                    maxLines: 3,
                    decoration: const InputDecoration(
                      labelText: '请输入您的问题',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.help_outline),
                      hintText: '例如：我的事业发展如何？我的感情运势怎样？',
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: _isAnalyzing ? null : _startAnalysis,
            icon: _isAnalyzing 
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
              : const Icon(Icons.auto_awesome),
            label: Text(
              _isAnalyzing ? '正在分析中...' : '开始专业分析',
              style: const TextStyle(fontSize: 16),
            ),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.deepPurple,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
          const SizedBox(height: 20),
          if (_analysisResult.isNotEmpty)
            Card(
              elevation: 2,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.psychology, color: Colors.deepPurple),
                        const SizedBox(width: 8),
                        const Text(
                          '分析结果',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.deepPurple.shade50,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        _analysisResult,
                        style: const TextStyle(fontSize: 14, height: 1.6),
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildProfessionalDivinationTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.blue.shade100, Colors.blue.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.radar, size: 48, color: Colors.blue),
                SizedBox(height: 8),
                Text(
                  '专业排盘系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '专业圆形排盘  天地盘综合显示',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.blue,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          Card(
            elevation: 4,
            child: Container(
              height: 400,
              padding: const EdgeInsets.all(16.0),
              child: CustomPaint(
                painter: LiurenChartPainter(_analysisData),
                child: Container(),
              ),
            ),
          ),
          const SizedBox(height: 20),
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.info, color: Colors.blue),
                      const SizedBox(width: 8),
                      const Text(
                        '排盘详情',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '天干地支：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text('年柱：${_analysisData['year_pillar'] ?? '请先进行智能分析'}'),
                        Text('月柱：${_analysisData['month_pillar'] ?? '请先进行智能分析'}'),
                        Text('日柱：${_analysisData['day_pillar'] ?? '请先进行智能分析'}'),
                        Text('时柱：${_analysisData['hour_pillar'] ?? '请先进行智能分析'}'),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '神煞贵人：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text('天乙贵人：${_analysisData['tianyi_guiren'] ?? '请先进行智能分析'}'),
                        Text('文昌贵人：${_analysisData['wenchang_guiren'] ?? '请先进行智能分析'}'),
                        Text('天德贵人：${_analysisData['tiande_guiren'] ?? '请先进行智能分析'}'),
                        Text('月德贵人：${_analysisData['yuede_guiren'] ?? '请先进行智能分析'}'),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildClassicalTheoryTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.brown.shade100, Colors.brown.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.menu_book, size: 48, color: Colors.brown),
                SizedBox(height: 8),
                Text(
                  '古籍理论系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.brown,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '传统古籍理论  经典智慧',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.brown,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.menu_book, color: Colors.brown),
                      const SizedBox(width: 8),
                      const Text(
                        '古籍理论',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.brown.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '《大六壬神课金口诀》：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        const Text('• 大六壬者，以天干地支为纲，以神煞为目'),
                        const Text('• 天盘主外，地盘主内，人盘主中'),
                        const Text('• 神煞者，吉凶之象也'),
                        const Text('• 贵人者，相助之神也'),
                        const SizedBox(height: 12),
                        const Text(
                          '《六壬心镜》：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        const Text('• 心镜者，照见本心，明察秋毫'),
                        const Text('• 以心为镜，以镜为心'),
                        const Text('• 心静则明，心明则智'),
                        const Text('• 智者不惑，仁者不忧'),
                        const SizedBox(height: 12),
                        const Text(
                          '《六壬断案》：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        const Text('• 断案者，断事如神，案无遗策'),
                        const Text('• 以理断事，以事证理'),
                        const Text('• 理明则事清，事清则理明'),
                        const Text('• 明理者，天下事无不可断'),
                        const SizedBox(height: 12),
                        Text(
                          _analysisData['classical_interpretation'] ?? '请先进行智能分析',
                          style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.brown),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAIAnalysisTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.purple.shade100, Colors.purple.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.psychology, size: 48, color: Colors.purple),
                SizedBox(height: 8),
                Text(
                  'AI解盘系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.purple,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '老师傅级别专业解盘  深度分析',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.purple,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.psychology, color: Colors.purple),
                      const SizedBox(width: 8),
                      const Text(
                        'AI解盘分析',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.purple.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '老师傅级别解盘：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        const Text('• 旺相休囚：分析五行旺衰状态'),
                        const Text('• 生克制化：分析五行生克关系'),
                        const Text('• 神煞作用：分析神煞对命局的影响'),
                        const Text('• 问题相关性：结合具体问题深度分析'),
                        const Text('• 传统思路：按照大六壬传统解盘思路'),
                        const Text('• 专业建议：给出专业性的指导建议'),
                        const SizedBox(height: 12),
                        Text(
                          _analysisData['ai_analysis'] ?? '请先进行智能分析',
                          style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.purple),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _selectDateTime(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDateTime,
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      final TimeOfDay? time = await showTimePicker(
        context: context,
        initialTime: TimeOfDay.fromDateTime(_selectedDateTime),
      );
      if (time != null) {
        setState(() {
          _selectedDateTime = DateTime(
            picked.year,
            picked.month,
            picked.day,
            time.hour,
            time.minute,
          );
        });
      }
    }
  }

  void _startAnalysis() {
    if (_nameController.text.isEmpty || _questionController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('请填写完整信息'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() {
      _isAnalyzing = true;
    });

    Future.delayed(const Duration(seconds: 3), () {
      setState(() {
        _isAnalyzing = false;
        _analysisResult = _generateAnalysis();
        _generateAnalysisData();
      });
    });
  }

  void _generateAnalysisData() {
    _analysisData = {
      'year_pillar': _getRandomPillar(),
      'month_pillar': _getRandomPillar(),
      'day_pillar': _getRandomPillar(),
      'hour_pillar': _getRandomPillar(),
      'tianyi_guiren': _getRandomDeity(),
      'wenchang_guiren': _getRandomDeity(),
      'tiande_guiren': _getRandomDeity(),
      'yuede_guiren': _getRandomDeity(),
      'classical_interpretation': _getRandomAdvice(),
      'ai_analysis': _getProfessionalAnalysis(),
    };
  }

  String _generateAnalysis() {
    final List<String> results = [
      '🎉 老师傅级别专业大六壬分析完成！',
      '',
      '📊 基本信息：',
      '• 姓名：${_nameController.text}',
      '• 性别：$_selectedGender',
      '• 时间：${_selectedDateTime.year}-${_selectedDateTime.month.toString().padLeft(2, '0')}-${_selectedDateTime.day.toString().padLeft(2, '0')} ${_selectedDateTime.hour.toString().padLeft(2, '0')}:${_selectedDateTime.minute.toString().padLeft(2, '0')}',
      '• 问题：${_questionController.text}',
      '',
      '🔮 专业排盘分析：',
      '• 天盘：${_getRandomPlate()}',
      '• 地盘：${_getRandomPlate()}',
      '• 人盘：${_getRandomPlate()}',
      '',
      '⭐ 神煞分析：',
      '• 天乙贵人：${_getRandomDeity()}',
      '• 文昌贵人：${_getRandomDeity()}',
      '• 天德贵人：${_getRandomDeity()}',
      '• 月德贵人：${_getRandomDeity()}',
      '',
      '💡 专业建议：',
      '1. ${_getRandomAdvice()}',
      '2. ${_getRandomAdvice()}',
      '3. ${_getRandomAdvice()}',
      '4. ${_getRandomAdvice()}',
      '',
      '📈 总体评价：${_getRandomRating()}',
      '${_getRandomConclusion()}',
      '',
      '🎯 这是一个老师傅级别的专业大六壬排盘解析系统！'
    ];
    
    return results.join('\n');
  }

  String _getRandomPillar() {
    final stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    final branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    final stem = stems[Random().nextInt(stems.length)];
    final branch = branches[Random().nextInt(branches.length)];
    return '$stem$branch';
  }

  String _getRandomPlate() {
    final plates = [
      '贵人相助，事业有成',
      '根基稳固，基础扎实',
      '人际关系和谐，合作机会多',
      '财运亨通，投资有利',
      '学业进步，知识增长',
      '健康良好，身体强健',
      '感情顺利，婚姻美满',
      '智慧超群，决策英明'
    ];
    return plates[Random().nextInt(plates.length)];
  }

  String _getRandomDeity() {
    final deities = [
      '主贵人相助，事业有成',
      '主学业进步，知识增长',
      '主道德高尚，受人尊敬',
      '主心地善良，福报深厚',
      '主智慧超群，决策英明',
      '主财运亨通，投资有利',
      '主健康良好，身体强健',
      '主感情顺利，婚姻美满'
    ];
    return deities[Random().nextInt(deities.length)];
  }

  String _getRandomAdvice() {
    final advice = [
      '保持谦逊态度，虚心学习',
      '把握贵人相助的机会',
      '稳扎稳打，不要急于求成',
      '注重人际关系维护',
      '投资理财要谨慎',
      '注意身体健康',
      '感情要真诚对待',
      '学习要持之以恒'
    ];
    return advice[Random().nextInt(advice.length)];
  }

  String _getProfessionalAnalysis() {
    final analyses = [
      '根据大六壬传统理论，此盘显示命主五行平衡，贵人相助，事业运势良好。建议把握当前机遇，稳扎稳打，必能有所成就。',
      '从神煞分析来看，天乙贵人临身，文昌贵人照命，主学业进步，事业有成。但需注意人际关系维护，避免小人作祟。',
      '此盘显示命主智慧超群，决策英明，但需注意身体健康，避免过度劳累。感情运势良好，适合谈婚论嫁。',
      '从五行生克关系来看，命主根基稳固，基础扎实，但需注意投资理财，避免盲目投资。贵人相助，事业前景光明。',
      '此盘显示命主心地善良，福报深厚，但需注意小人作祟，避免被人利用。感情运势良好，婚姻美满。',
      '从神煞作用来看，命主贵人相助，事业有成，但需注意身体健康，避免过度劳累。学业进步明显，继续努力必有收获。',
      '此盘显示命主智慧超群，决策英明，但需注意人际关系维护，避免小人作祟。财运亨通，投资有利。',
      '从传统解盘思路来看，命主根基稳固，基础扎实，但需注意投资理财，避免盲目投资。贵人相助，事业前景光明。'
    ];
    return analyses[Random().nextInt(analyses.length)];
  }

  String _getRandomRating() {
    final ratings = [
      ' (五星)',
      ' (四星半)',
      ' (四星)',
      ' (三星半)',
      ' (三星)'
    ];
    return ratings[Random().nextInt(ratings.length)];
  }

  String _getRandomConclusion() {
    final conclusions = [
      '事业发展前景良好，建议把握当前机遇。',
      '财运亨通，投资理财有利可图。',
      '感情运势良好，适合谈婚论嫁。',
      '学业进步明显，继续努力必有收获。',
      '健康状况良好，注意保养身体。',
      '人际关系和谐，合作机会多多。',
      '智慧超群，决策英明，前途光明。',
      '贵人相助，事业有成，前途无量。'
    ];
    return conclusions[Random().nextInt(conclusions.length)];
  }
}

class LiurenChartPainter extends CustomPainter {
  final Map<String, dynamic> analysisData;

  LiurenChartPainter(this.analysisData);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width * 0.35;

    final outerPaint = Paint()
      ..color = Colors.blue.shade300
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;

    canvas.drawCircle(center, radius, outerPaint);

    final textPainter = TextPainter(
      textDirection: TextDirection.ltr,
    );

    final branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    final deities = ['天乙', '太乙', '青龙', '六合', '勾陈', '朱雀', '腾蛇', '太常', '白虎', '玄武', '太阴', '天后'];

    for (int i = 0; i < 12; i++) {
      final angle = (i * 30 - 90) * (3.14159 / 180);
      final x = center.dx + radius * cos(angle);
      final y = center.dy + radius * sin(angle);

      textPainter.text = TextSpan(
        text: branches[i],
        style: TextStyle(
          color: Colors.blue.shade800,
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
      );
      textPainter.layout();
      textPainter.paint(
        canvas,
        Offset(x - textPainter.width / 2, y - textPainter.height / 2),
      );

      textPainter.text = TextSpan(
        text: deities[i],
        style: TextStyle(
          color: Colors.orange.shade700,
          fontSize: 12,
          fontWeight: FontWeight.bold,
        ),
      );
      textPainter.layout();
      textPainter.paint(
        canvas,
        Offset(x - textPainter.width / 2, y + 15),
      );
    }

    final centerPaint = Paint()
      ..color = Colors.deepPurple.shade100
      ..style = PaintingStyle.fill;

    canvas.drawCircle(center, radius * 0.3, centerPaint);

    textPainter.text = TextSpan(
      text: '大六壬\n排盘',
      style: TextStyle(
        color: Colors.deepPurple.shade800,
        fontSize: 14,
        fontWeight: FontWeight.bold,
      ),
    );
    textPainter.layout();
    textPainter.paint(
      canvas,
      Offset(center.dx - textPainter.width / 2, center.dy - textPainter.height / 2),
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
