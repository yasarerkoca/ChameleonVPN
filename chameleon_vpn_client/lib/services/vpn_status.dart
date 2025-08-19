import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../state.dart';
import 'package:flutter_wireguard_plugin/flutter_wireguard_plugin.dart';

/// Service that listens to native VPN status updates and keeps a log of events.
///
/// The service exposes a broadcast [Stream] of status changes and notifies
/// listeners when the latest status or log list changes. Recent logs are
/// persisted so they can be viewed in the log UI even after app restarts.
class VpnStatusService extends ChangeNotifier {
  static const _prefsKey = 'vpn_logs';

  final AppNotifier _appNotifier;

  final StreamController<String> _statusController =
      StreamController<String>.broadcast();
  StreamSubscription<String>? _statusSub;

  String _currentStatus = 'disconnected';
  List<String> _logs = <String>[];
  SharedPreferences? _prefs;

  /// Public stream of status updates.
  Stream<String> get statusStream => _statusController.stream;

  /// Last reported VPN status.
  String get currentStatus => _currentStatus;

  /// Recent log entries. Unmodifiable list.
  List<String> get logs => List.unmodifiable(_logs);

  VpnStatusService(this._appNotifier);

  /// Starts listening to the native status stream and loads persisted logs.
  Future<void> init() async {
    await _loadLogs();
    try {
      _statusSub = FlutterWireguardPlugin.statusStream.listen(
        _onStatus,
        onError: _onError,
      );
    } on PlatformException catch (e) {
      _addLog('Status stream error: ${e.message}');
    } on MissingPluginException catch (e) {
      _addLog('Status stream missing: ${e.message}');
    }
  }

  Future<void> _loadLogs() async {
    try {
      _prefs = await SharedPreferences.getInstance();
      _logs = _prefs?.getStringList(_prefsKey) ?? <String>[];
    } catch (e) {
      // Shared preferences might be unavailable in tests or unsupported
      _logs = <String>[];
    }
    _appNotifier.setLogs(_logs);
  }

  void _onStatus(String status) {
    _currentStatus = status;
    _statusController.add(status);
    _handleStatus(status);
    notifyListeners();
  }

  void _handleStatus(String status) {
    _addLog('Status: $status');
    if (status.toLowerCase() == 'connected') {
      _appNotifier.connect();
    } else if (status.toLowerCase() == 'disconnected') {
      _appNotifier.disconnect();
    }
  }

  void _onError(Object error) {
    _addLog('Error: $error');
  }

  void _addLog(String log) {
    _logs.add(log);
    if (_logs.length > 100) {
      _logs.removeAt(0);
    }
    _appNotifier.addLog(log);
    _prefs?.setStringList(_prefsKey, _logs);
    notifyListeners();
  }

  @override
  void dispose() {
    _statusSub?.cancel();
    _statusController.close();
    super.dispose();
  }
}

/// Riverpod provider to create and expose [VpnStatusService].
final vpnStatusProvider = ChangeNotifierProvider<VpnStatusService>((ref) {
  final service = VpnStatusService(ref.read(appProvider.notifier));
  unawaited(service.init());
  ref.onDispose(service.dispose);
  return service;
});
