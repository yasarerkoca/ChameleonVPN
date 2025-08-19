import 'package:plugin_platform_interface/plugin_platform_interface.dart';

import 'flutter_wireguard_plugin_method_channel.dart';

abstract class FlutterWireguardPluginPlatform extends PlatformInterface {
  /// Constructs a FlutterWireguardPluginPlatform.
  FlutterWireguardPluginPlatform() : super(token: _token);

  static final Object _token = Object();

  static FlutterWireguardPluginPlatform _instance = MethodChannelFlutterWireguardPlugin();

  /// The default instance of [FlutterWireguardPluginPlatform] to use.
  ///
  /// Defaults to [MethodChannelFlutterWireguardPlugin].
  static FlutterWireguardPluginPlatform get instance => _instance;

  /// Platform-specific implementations should set this with their own
  /// platform-specific class that extends [FlutterWireguardPluginPlatform] when
  /// they register themselves.
  static set instance(FlutterWireguardPluginPlatform instance) {
    PlatformInterface.verifyToken(instance, _token);
    _instance = instance;
  }

  Future<String?> getPlatformVersion() {
    throw UnimplementedError('getPlatformVersion() has not been implemented.');
  }

  Future<bool> connect({required String config}) {
    throw UnimplementedError('connect() has not been implemented.');
  }

  Future<bool> disconnect() {
    throw UnimplementedError('disconnect() has not been implemented.');
  }
}
