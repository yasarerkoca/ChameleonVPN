import 'dart:async';
import 'package:flutter/services.dart';

class FlutterWireguardPlugin {
  static const MethodChannel _channel = MethodChannel('flutter_wireguard_plugin');
  static const EventChannel _statusChannel = EventChannel('flutter_wireguard_plugin/status');
  static Stream<String>? _statusStream;

  static Future<bool> connect(String config) async {
    final result = await _channel.invokeMethod<bool>('connect', {'config': config});
    return result ?? false;
  }

  static Future<bool> disconnect() async {
    final result = await _channel.invokeMethod<bool>('disconnect');
    return result ?? false;
  }

  static Stream<String> get statusStream {
    _statusStream ??= _statusChannel.receiveBroadcastStream().cast<String>();
    return _statusStream!;
  }
}
