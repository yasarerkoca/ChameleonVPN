import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'login_page.dart';
import 'pages/servers.dart';
import 'connection_status_page.dart';
import 'profile_page.dart';
import 'services/vpn_status.dart';

void main() {
  runApp(const ProviderScope(child: ChameleonVpnApp()));
}

class ChameleonVpnApp extends ConsumerWidget {
  const ChameleonVpnApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Ensure the VPN status service is initialized.
    ref.watch(vpnStatusProvider);
    return MaterialApp(
      title: 'Chameleon VPN',
      initialRoute: '/',
      routes: {
        '/': (_) => const LoginPage(),
        '/servers': (_) => const ServersPage(),
        '/status': (_) => const ConnectionStatusPage(),
        '/profile': (_) => const ProfilePage(),
      },
    );
  }
}
