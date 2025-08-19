import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

import 'flutter_wireguard_plugin_platform_interface.dart';

/// An implementation of [FlutterWireguardPluginPlatform] that uses method channels.
class MethodChannelFlutterWireguardPlugin extends FlutterWireguardPluginPlatform {
  /// The method channel used to interact with the native platform.
  @visibleForTesting
  final methodChannel = const MethodChannel('flutter_wireguard_plugin');

  @override
  Future<String?> getPlatformVersion() async {
    final version = await methodChannel.invokeMethod<String>('getPlatformVersion');
    return version;
  }

  @override
  Future<bool> connect({required String config}) async {
    final result = await methodChannel.invokeMethod<bool>('connect', {'config': config});
    return result ?? false;
  }

  @override
  Future<bool> disconnect() async {
    final result = await methodChannel.invokeMethod<bool>('disconnect');
    return result ?? false;
  }
}
