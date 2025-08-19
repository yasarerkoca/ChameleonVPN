import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:chameleon_vpn_client/pages/home.dart';

void main() {
  testWidgets('Home page shows welcome text', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: HomePage()));
    expect(find.byKey(const Key('homeText')), findsOneWidget);
  });
}
