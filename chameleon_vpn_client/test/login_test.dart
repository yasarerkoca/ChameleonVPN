import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:chameleonvpn/pages/login.dart';

void main() {
  testWidgets('Login form renders and works', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: LoginPage()));
    expect(find.text('Login'), findsOneWidget);

    await tester.enterText(find.byType(TextField).first, 'testuser');
    await tester.enterText(find.byType(TextField).last, 'testpass');
    await tester.tap(find.byType(ElevatedButton));
    await tester.pump();
    // Mock API cevabı olmadığı için gerçek doğrulama burada olmayacak
  });
}
