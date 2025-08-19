import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:chameleon_vpn_client/connection_status_page.dart';
import 'package:chameleon_vpn_client/state.dart';

void main() {
  testWidgets('Connect button toggles state', (tester) async {
    final notifier = AppNotifier()
      ..login(const User(name: 'Bob', subscription: 'Basic', token: 't'))
      ..selectServer(const Server(id: '1', name: 'Server'));
    await tester.pumpWidget(
      ProviderScope(
        overrides: [appProvider.overrideWith(() => notifier)],
        child: const MaterialApp(home: ConnectionStatusPage()),
      ),
    );
    expect(find.text('Connect'), findsOneWidget);
    await tester.tap(find.byKey(const Key('connectButton')));
    await tester.pump();
    expect(find.text('Disconnect'), findsOneWidget);
  });
}
