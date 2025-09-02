import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppProvider extends ChangeNotifier {
  bool _isDarkMode = false;
  bool _isFirstLaunch = true;
  String _selectedLanguage = 'zh';
  Map<String, dynamic> _userInfo = {};
  List<Map<String, dynamic>> _historyRecords = [];

  bool get isDarkMode => _isDarkMode;
  bool get isFirstLaunch => _isFirstLaunch;
  String get selectedLanguage => _selectedLanguage;
  Map<String, dynamic> get userInfo => _userInfo;
  List<Map<String, dynamic>> get historyRecords => _historyRecords;

  AppProvider() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    _isDarkMode = prefs.getBool('isDarkMode') ?? false;
    _isFirstLaunch = prefs.getBool('isFirstLaunch') ?? true;
    _selectedLanguage = prefs.getString('selectedLanguage') ?? 'zh';
    notifyListeners();
  }

  Future<void> toggleDarkMode() async {
    _isDarkMode = !_isDarkMode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isDarkMode', _isDarkMode);
    notifyListeners();
  }

  Future<void> setLanguage(String language) async {
    _selectedLanguage = language;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('selectedLanguage', language);
    notifyListeners();
  }

  Future<void> setUserInfo(Map<String, dynamic> info) async {
    _userInfo = info;
    notifyListeners();
  }

  Future<void> addHistoryRecord(Map<String, dynamic> record) async {
    _historyRecords.insert(0, record);
    if (_historyRecords.length > 50) {
      _historyRecords = _historyRecords.take(50).toList();
    }
    notifyListeners();
  }

  Future<void> clearHistory() async {
    _historyRecords.clear();
    notifyListeners();
  }
} 