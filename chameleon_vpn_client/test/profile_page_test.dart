import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:chameleon_vpn_client/profile_page.dart';
import 'package:chameleon_vpn_client/state.dart';

void main() {
  testWidgets('Profile displays user info', (tester) async {
    final notifier = AppNotifier()
      ..login(const User(name: 'Alice', subscription: 'Pro', token: 't'));
    await tester.pumpWidget(
      ProviderScope(
        overrides: [appProvider.overrideWith((ref) => notifier)],
        child: const MaterialApp(home: ProfilePage()),
      ),
    );
    expect(find.byKey(const Key('userName')), findsOneWidget);
    expect(find.text('Name: Alice'), findsOneWidget);
  });
}
