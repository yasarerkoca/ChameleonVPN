import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:chameleon_vpn_client/pages/servers.dart';
import 'package:chameleon_vpn_client/state.dart';

void main() {
  testWidgets('Server list loads and connects', (tester) async {
    final servers = [const Server(id: '1', name: 'Server A')];
    final app = AppNotifier();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          serverListProvider.overrideWith((ref) => Future.value(servers)),
          appProvider.overrideWith(() => app),
        ],
        child: const MaterialApp(home: ServersPage()),
      ),
    );
    await tester.pump();
    expect(find.text('Server A'), findsOneWidget);
    expect(find.text('Connect'), findsOneWidget);
    await tester.tap(find.text('Connect'));
    await tester.pump();
    expect(find.text('Disconnect'), findsOneWidget);
  });
}
