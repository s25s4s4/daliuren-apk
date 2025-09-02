import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_provider.dart';
import 'divination_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('大六壬排盘解析系统'),
        centerTitle: true,
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: const [
          DivinationHomeTab(),
          HistoryTab(),
          SettingsTab(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.psychology),
            label: '排盘',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.history),
            label: '历史',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: '设置',
          ),
        ],
      ),
    );
  }
}

class DivinationHomeTab extends StatelessWidget {
  const DivinationHomeTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            '大六壬排盘解析系统',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 20),
          const Text(
            '专业的大六壬排盘解析，提供AI智能分析和案例匹配',
            style: TextStyle(fontSize: 16),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 30),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const DivinationScreen(),
                ),
              );
            },
            icon: const Icon(Icons.psychology),
            label: const Text('开始排盘'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.all(20),
              textStyle: const TextStyle(fontSize: 18),
            ),
          ),
          const SizedBox(height: 20),
          const FeatureCard(
            icon: Icons.auto_awesome,
            title: 'AI智能分析',
            description: '基于大六壬理论的智能分析系统',
          ),
          const SizedBox(height: 16),
          const FeatureCard(
            icon: Icons.library_books,
            title: '百万案例库',
            description: '包含100万+真实案例数据库',
          ),
          const SizedBox(height: 16),
          const FeatureCard(
            icon: Icons.history,
            title: '古籍解析',
            description: '经典古籍内容深度解析',
          ),
        ],
      ),
    );
  }
}

class FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;

  const FeatureCard({
    super.key,
    required this.icon,
    required this.title,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Icon(
              icon,
              size: 40,
              color: Theme.of(context).primaryColor,
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    description,
                    style: const TextStyle(fontSize: 14),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class HistoryTab extends StatelessWidget {
  const HistoryTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AppProvider>(
      builder: (context, appProvider, child) {
        if (appProvider.historyRecords.isEmpty) {
          return const Center(
            child: Text('暂无历史记录'),
          );
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: appProvider.historyRecords.length,
          itemBuilder: (context, index) {
            final record = appProvider.historyRecords[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                title: Text(record['question'] ?? '未知问题'),
                subtitle: Text(record['date'] ?? ''),
                trailing: IconButton(
                  icon: const Icon(Icons.delete),
                  onPressed: () {
                    // 删除记录
                  },
                ),
              ),
            );
          },
        );
      },
    );
  }
}

class SettingsTab extends StatelessWidget {
  const SettingsTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AppProvider>(
      builder: (context, appProvider, child) {
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            SwitchListTile(
              title: const Text('深色模式'),
              subtitle: const Text('切换应用主题'),
              value: appProvider.isDarkMode,
              onChanged: (value) {
                appProvider.toggleDarkMode();
              },
            ),
            const Divider(),
            ListTile(
              title: const Text('清除历史记录'),
              subtitle: const Text('删除所有查询历史'),
              leading: const Icon(Icons.delete_sweep),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text('确认删除'),
                    content: const Text('确定要删除所有历史记录吗？'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('取消'),
                      ),
                      TextButton(
                        onPressed: () {
                          appProvider.clearHistory();
                          Navigator.pop(context);
                        },
                        child: const Text('删除'),
                      ),
                    ],
                  ),
                );
              },
            ),
            const Divider(),
            ListTile(
              title: const Text('关于应用'),
              subtitle: const Text('版本 1.0.0'),
              leading: const Icon(Icons.info),
              onTap: () {
                showAboutDialog(
                  context: context,
                  applicationName: '大六壬排盘解析系统',
                  applicationVersion: '1.0.0',
                  applicationIcon: const Icon(Icons.psychology),
                  children: const [
                    Text('专业的大六壬排盘解析系统'),
                    Text('提供AI智能分析和案例匹配功能'),
                  ],
                );
              },
            ),
          ],
        );
      },
    );
  }
} 