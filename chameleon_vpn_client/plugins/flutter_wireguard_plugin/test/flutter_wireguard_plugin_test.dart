import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_wireguard_plugin/flutter_wireguard_plugin.dart';
import 'package:flutter_wireguard_plugin/flutter_wireguard_plugin_platform_interface.dart';
import 'package:flutter_wireguard_plugin/flutter_wireguard_plugin_method_channel.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';

class MockFlutterWireguardPluginPlatform
    with MockPlatformInterfaceMixin
    implements FlutterWireguardPluginPlatform {

  @override
  Future<String?> getPlatformVersion() => Future.value('42');
}

void main() {
  final FlutterWireguardPluginPlatform initialPlatform = FlutterWireguardPluginPlatform.instance;

  test('$MethodChannelFlutterWireguardPlugin is the default instance', () {
    expect(initialPlatform, isInstanceOf<MethodChannelFlutterWireguardPlugin>());
  });

  test('getPlatformVersion', () async {
    FlutterWireguardPlugin flutterWireguardPlugin = FlutterWireguardPlugin();
    MockFlutterWireguardPluginPlatform fakePlatform = MockFlutterWireguardPluginPlatform();
    FlutterWireguardPluginPlatform.instance = fakePlatform;

    expect(await flutterWireguardPlugin.getPlatformVersion(), '42');
  });
}
