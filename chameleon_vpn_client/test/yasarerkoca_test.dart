import 'package:flutter_test/flutter_test.dart';
import 'package:yasarerkoca/yasarerkoca.dart';
import 'package:yasarerkoca/yasarerkoca_platform_interface.dart';
import 'package:yasarerkoca/yasarerkoca_method_channel.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';

class MockYasarerkocaPlatform
    with MockPlatformInterfaceMixin
    implements YasarerkocaPlatform {

  @override
  Future<String?> getPlatformVersion() => Future.value('42');
}

void main() {
  final YasarerkocaPlatform initialPlatform = YasarerkocaPlatform.instance;

  test('$MethodChannelYasarerkoca is the default instance', () {
    expect(initialPlatform, isInstanceOf<MethodChannelYasarerkoca>());
  });

  test('getPlatformVersion', () async {
    Yasarerkoca yasarerkocaPlugin = Yasarerkoca();
    MockYasarerkocaPlatform fakePlatform = MockYasarerkocaPlatform();
    YasarerkocaPlatform.instance = fakePlatform;

    expect(await yasarerkocaPlugin.getPlatformVersion(), '42');
  });
}
