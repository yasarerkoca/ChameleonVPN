import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'login_page.dart';
import 'server_selection_page.dart';
import 'connection_status_page.dart';
import 'profile_page.dart';

void main() {
  runApp(const ProviderScope(child: ChameleonVpnApp()));
}

class ChameleonVpnApp extends StatelessWidget {
  const ChameleonVpnApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chameleon VPN',
      initialRoute: '/',
      routes: {
        '/': (_) => const LoginPage(),
        '/servers': (_) => const ServerSelectionPage(),
        '/status': (_) => const ConnectionStatusPage(),
        '/profile': (_) => const ProfilePage(),
      },
    );
  }
}
