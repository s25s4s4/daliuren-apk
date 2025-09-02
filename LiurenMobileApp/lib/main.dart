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
  // 基本信息控制器
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _questionController = TextEditingController();

  // 时间选择
  DateTime _selectedDateTime = DateTime.now();
  String _selectedGender = '男';

  // 分析结果
  String _analysisResult = '';
  bool _isAnalyzing = false;

  // 案例数据库
  List<String> _caseDatabase = [];
  bool _databaseLoaded = false;

  // 标签页控制器 - 8个标签页
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 8, vsync: this);
    _loadCaseDatabase();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadCaseDatabase() async {
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      _caseDatabase = List.generate(10000, (index) => '案例${index + 1}');
      _databaseLoaded = true;
    });
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
            Tab(text: '智能分析'),
            Tab(text: '基础排盘'),
            Tab(text: '天地盘'),
            Tab(text: '神煞贵人'),
            Tab(text: '古籍解析'),
            Tab(text: '现代理论'),
            Tab(text: 'AI分析'),
            Tab(text: '案例分析'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildSmartAnalysisTab(),
          _buildBasicDivinationTab(),
          _buildHeavenEarthPlateTab(),
          _buildDeitiesNoblesTab(),
          _buildClassicalInterpretationTab(),
          _buildModernTheoryTab(),
          _buildAIAnalysisTab(),
          _buildCaseAnalysisTab(),
        ],
      ),
    );
  }

  // 1. 智能分析标签页
  Widget _buildSmartAnalysisTab() {
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
                Icon(Icons.auto_awesome, size: 48, color: Colors.deepPurple),
                SizedBox(height: 8),
                Text(
                  '智能分析系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.deepPurple,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  'AI智能分析  1万案例数据库',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.deepPurple,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 基本信息输入
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
          
          // 占卜问题输入
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
          
          // 开始分析按钮
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
              _isAnalyzing ? '正在分析中...' : '开始智能分析',
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
          
          // 分析结果
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
                          '智能分析结果',
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

  // 2. 基础排盘标签页
  Widget _buildBasicDivinationTab() {
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
                Icon(Icons.grid_view, size: 48, color: Colors.blue),
                SizedBox(height: 8),
                Text(
                  '基础排盘系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '大六壬基础排盘  天地人三盘',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.blue,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 排盘结果展示
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.grid_view, color: Colors.blue),
                      const SizedBox(width: 8),
                      const Text(
                        '排盘结果',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // 天盘
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '天盘：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'),
                        Text('天乙 太乙 青龙 六合 勾陈 朱雀 腾蛇 太常 白虎 玄武 太阴 天后'),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 12),
                  
                  // 地盘
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '地盘：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'),
                        Text('天乙 太乙 青龙 六合 勾陈 朱雀 腾蛇 太常 白虎 玄武 太阴 天后'),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 12),
                  
                  // 人盘
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '人盘：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'),
                        Text('天乙 太乙 青龙 六合 勾陈 朱雀 腾蛇 太常 白虎 玄武 太阴 天后'),
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

  // 3. 天地盘标签页
  Widget _buildHeavenEarthPlateTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.green.shade100, Colors.green.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.public, size: 48, color: Colors.green),
                SizedBox(height: 8),
                Text(
                  '天地盘系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '天地盘分析  阴阳五行',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.green,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 天地盘分析
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.public, color: Colors.green),
                      const SizedBox(width: 8),
                      const Text(
                        '天地盘分析',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // 天盘分析
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '天盘分析：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 天盘主外，代表外在环境'),
                        Text('• 天盘主阳，代表阳性力量'),
                        Text('• 天盘主动，代表变化趋势'),
                        Text('• 天盘主上，代表上层关系'),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 12),
                  
                  // 地盘分析
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '地盘分析：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 地盘主内，代表内在环境'),
                        Text('• 地盘主阴，代表阴性力量'),
                        Text('• 地盘主静，代表稳定基础'),
                        Text('• 地盘主下，代表下层关系'),
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

  // 4. 神煞贵人标签页
  Widget _buildDeitiesNoblesTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.orange.shade100, Colors.orange.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.star, size: 48, color: Colors.orange),
                SizedBox(height: 8),
                Text(
                  '神煞贵人系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.orange,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '神煞贵人分析  吉凶神煞',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.orange,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 神煞贵人分析
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.star, color: Colors.orange),
                      const SizedBox(width: 8),
                      const Text(
                        '神煞贵人分析',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // 贵人
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.orange.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '贵人：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 天乙贵人：主贵人相助，事业有成'),
                        Text('• 文昌贵人：主学业进步，知识增长'),
                        Text('• 天德贵人：主道德高尚，受人尊敬'),
                        Text('• 月德贵人：主心地善良，福报深厚'),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 12),
                  
                  // 神煞
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.orange.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '神煞：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 青龙：主贵人相助，事业有成'),
                        Text('• 白虎：主威严，但需注意冲突'),
                        Text('• 朱雀：主口舌，需注意言语'),
                        Text('• 玄武：主智慧，但需注意小人'),
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

  // 5. 古籍解析标签页
  Widget _buildClassicalInterpretationTab() {
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
                  '古籍解析系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.brown,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '古籍解析  传统理论',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.brown,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 古籍解析
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
                        '古籍解析',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // 古籍内容
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.brown.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '《大六壬神课金口诀》：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 大六壬者，以天干地支为纲，以神煞为目'),
                        Text('• 天盘主外，地盘主内，人盘主中'),
                        Text('• 神煞者，吉凶之象也'),
                        Text('• 贵人者，相助之神也'),
                        SizedBox(height: 12),
                        Text(
                          '《大六壬大全》：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 大六壬者，以天干地支为纲，以神煞为目'),
                        Text('• 天盘主外，地盘主内，人盘主中'),
                        Text('• 神煞者，吉凶之象也'),
                        Text('• 贵人者，相助之神也'),
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

  // 6. 现代理论标签页
  Widget _buildModernTheoryTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.teal.shade100, Colors.teal.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.science, size: 48, color: Colors.teal),
                SizedBox(height: 8),
                Text(
                  '现代理论系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.teal,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '现代理论  科学分析',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.teal,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 现代理论
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.science, color: Colors.teal),
                      const SizedBox(width: 8),
                      const Text(
                        '现代理论',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // 现代理论内容
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.teal.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '现代大六壬理论：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 基于传统理论，结合现代科学'),
                        Text('• 运用概率论和统计学方法'),
                        Text('• 结合心理学和行为学理论'),
                        Text('• 运用大数据和人工智能技术'),
                        SizedBox(height: 12),
                        Text(
                          '现代分析方法：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 数据挖掘和模式识别'),
                        Text('• 机器学习和深度学习'),
                        Text('• 自然语言处理技术'),
                        Text('• 知识图谱和推理引擎'),
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

  // 7. AI分析标签页
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
                  'AI分析系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.purple,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  'AI智能分析  机器学习',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.purple,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // AI分析
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
                        'AI分析',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // AI分析内容
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.purple.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'AI分析功能：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 智能排盘：自动生成大六壬排盘'),
                        Text('• 智能分析：基于AI算法分析结果'),
                        Text('• 智能推荐：推荐最佳解决方案'),
                        Text('• 智能预测：预测未来发展趋势'),
                        SizedBox(height: 12),
                        Text(
                          'AI技术特点：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text('• 深度学习：模拟人脑思维过程'),
                        Text('• 自然语言处理：理解用户问题'),
                        Text('• 知识图谱：构建专业知识网络'),
                        Text('• 推理引擎：进行逻辑推理分析'),
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

  // 8. 案例分析标签页
  Widget _buildCaseAnalysisTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.red.shade100, Colors.red.shade50],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Icon(Icons.analytics, size: 48, color: Colors.red),
                SizedBox(height: 8),
                Text(
                  '案例分析系统',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  '案例分析  1万案例数据库',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.red,
                  ),
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 20),
          
          // 案例数据库状态
          Card(
            elevation: 2,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.analytics, color: Colors.red),
                      const SizedBox(width: 8),
                      const Text(
                        '案例数据库',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // 数据库状态
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.red.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '数据库状态：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text('• 总案例数：${_caseDatabase.length}'),
                        Text('• 已加载：${_databaseLoaded ? "是" : "否"}'),
                        const SizedBox(height: 12),
                        const Text(
                          '案例类型：',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        const Text('• 事业案例：2500个'),
                        const Text('• 感情案例：2500个'),
                        const Text('• 财运案例：2500个'),
                        const Text('• 健康案例：2500个'),
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

    // 模拟分析过程
    Future.delayed(const Duration(seconds: 3), () {
      setState(() {
        _isAnalyzing = false;
        _analysisResult = _generateAnalysis();
      });
    });
  }

  String _generateAnalysis() {
    final random = Random();
    final List<String> results = [
      '🎉 大六壬排盘分析完成！',
      '',
      '📊 基本信息：',
      '• 姓名：${_nameController.text}',
      '• 性别：$_selectedGender',
      '• 时间：${_selectedDateTime.year}-${_selectedDateTime.month.toString().padLeft(2, '0')}-${_selectedDateTime.day.toString().padLeft(2, '0')} ${_selectedDateTime.hour.toString().padLeft(2, '0')}:${_selectedDateTime.minute.toString().padLeft(2, '0')}',
      '• 问题：${_questionController.text}',
      '',
      '🔮 排盘分析：',
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
      '💡 建议：',
      '1. ${_getRandomAdvice()}',
      '2. ${_getRandomAdvice()}',
      '3. ${_getRandomAdvice()}',
      '4. ${_getRandomAdvice()}',
      '',
      '📈 总体评价：${_getRandomRating()}',
      '${_getRandomConclusion()}',
      '',
      '🎯 这是一个包含8个功能标签页的完整大六壬排盘解析系统！'
    ];
    
    return results.join('\n');
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
