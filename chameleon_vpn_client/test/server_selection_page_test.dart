import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:chameleon_vpn_client/server_selection_page.dart';
import 'package:chameleon_vpn_client/state.dart';

void main() {
  testWidgets('Server list loads', (tester) async {
    final servers = [
      const Server(id: '1', name: 'Server A'),
      const Server(id: '2', name: 'Server B'),
    ];
    await tester.pumpWidget(
      ProviderScope(
        overrides: [serverListProvider.overrideWith((ref) => Future.value(servers))],
        child: const MaterialApp(home: ServerSelectionPage()),
      ),
    );
    await tester.pump();
    expect(find.text('Server A'), findsOneWidget);
  });
}
