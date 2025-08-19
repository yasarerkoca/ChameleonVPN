import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:http/http.dart' as http;
import 'package:openvpn_flutter/openvpn_flutter.dart';
import 'screens/login_screen.dart';

import 'constants.dart';
import 'login_page.dart';
import 'proxy_usage_page.dart';
import 'twofa_page.dart';
import 'user_device_page.dart';
import 'inapp_purchase_page.dart';
import 'log_error_page.dart';
import 'login_google.dart'; // signInWithGoogle()

void main() {
  runApp(const MyApp());
}

/// Root widget of the application.
class ChameleonVpnApp extends StatelessWidget {
  const ChameleonVpnApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chameleon VPN',
      theme: ThemeData(useMaterial3: true),
      home: const LoginScreen(),
    );
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});
  @override
  State<MyApp> createState() => _MyAppState();
}

// Şimdilik WireGuard bağlanmayı stub'la (plugin MethodChannel entegre edilince değiştirilecek)
Future<void> connectWireGuard(String config) async {
  try {
    // final result = await FlutterWireguardPlugin.connect(config: config);
    final result = await Future.value("stub_connected");
    debugPrint('WireGuard bağlantısı başarılı: $result');
  } catch (e) {
    debugPrint('WireGuard bağlantı hatası: $e');
  }
}

class _MyAppState extends State<MyApp> {
  String? jwt; // backend’den gelecek gerçek JWT
  String? ovpnConfig;
  final List<String> vpnLogs = [];
  late OpenVPN openVPN;

  @override
  void initState() {
    super.initState();
    openVPN = OpenVPN(
      onVpnStatusChanged: (status) {
        setState(() => vpnLogs.add(status.toString()));
      },
      onVpnStageChanged: (stage, text) {
        setState(() => vpnLogs.add('Stage: $stage | $text'));
      },
    );
    _loadOvpnConfig();
  }

  Future<void> _loadOvpnConfig() async {
    try {
      final config = await rootBundle.loadString('assets/vpn_config.ovpn');
      if (!mounted) return;
      setState(() => ovpnConfig = config);
    } catch (e) {
      if (!mounted) return;
      setState(() => ovpnConfig = null);
      debugPrint('OpenVPN yapılandırması yüklenemedi: $e');
    }
  }

  void handleLogin(String tokenFromClassicLogin) {
    setState(() => jwt = tokenFromClassicLogin);
    debugPrint('Gelen JWT (klasik): $tokenFromClassicLogin');
  }

  Future<void> _sendLog(String type) async {
    if (jwt == null) return;
    final url = Uri.parse('$baseUrl/logs/$type');
    final headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $jwt',
    };
    final body = type == 'start'
        ? json.encode({"ip_address": "1.2.3.4", "location": "TestLokasyon"})
        : '{}';
    try {
      final res = await http.post(url, headers: headers, body: body);
      if (!mounted) return;
      if (res.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$type logu başarıyla gönderildi!')),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Hata: ${res.statusCode}\n${res.body}')),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Bağlantı hatası: $e')),
      );
    }
  }

  Future<void> _startVpn() async {
    if (ovpnConfig == null) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('OpenVPN yapılandırması yüklenemedi!')),
      );
      return;
    }
    try {
      await openVPN.connect(
        'ChameleonVPN',
        ovpnConfig!,
        username: 'KULLANICI_ADI',
        password: 'SIFRE',
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('VPN bağlantısı başlatıldı!')),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('VPN başlatılamadı: $e')),
      );
    }
  }

  Future<void> _stopVpn() async {
    try {
      openVPN.disconnect();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('VPN bağlantısı kesildi!')),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('VPN bağlantısı sonlandırılamadı: $e')),
      );
    }
  }

  // GOOGLE → BACKEND TOKEN EXCHANGE
  Future<void> _loginWithGoogle() async {
    final googleAccessToken = await signInWithGoogle();
    if (googleAccessToken == null) return;

    try {
      final res = await http.post(
        Uri.parse('$baseUrl/auth/google/callback'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'access_token': googleAccessToken}),
      );

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body) as Map<String, dynamic>;
        setState(() => jwt = data['access_token'] as String?);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Google ile giriş başarılı')),
        );
      } else {
        debugPrint('Google callback hata: ${res.statusCode} - ${res.body}');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Giriş hatası: ${res.statusCode}')),
        );
      }
    } catch (e) {
      debugPrint('Google callback exception: $e');
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Bağlantı hatası: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final loggedIn = jwt != null;

    return MaterialApp(
      title: 'ChameleonVPN',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: loggedIn
          ? Scaffold(
              appBar: AppBar(title: const Text('VPN Anasayfa')),
              body: Center(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('Giriş başarılı, ana sayfa!'),
                      const SizedBox(height: 24),

                      // OpenVPN
                      ElevatedButton(
                        onPressed: () async {
                          await _sendLog('start');
                          await _startVpn();
                        },
                        child: const Text('Bağlan (OpenVPN başlat)'),
                      ),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () async {
                          await _sendLog('end');
                          await _stopVpn();
                        },
                        child: const Text('Bağlantıyı Kes (OpenVPN durdur)'),
                      ),

                      const SizedBox(height: 12),

                      // WireGuard (test stub)
                      ElevatedButton(
                        onPressed: () async {
                          const wgConfig = '''
[Interface]
PrivateKey = (senin client private key)
Address = 10.8.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = aa6UMt797WxM4yUqdOMcZu4joDK030fHS0uIoMZPHXw=
Endpoint = 34.107.33.22:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
''';
                          await connectWireGuard(wgConfig);
                        },
                        child: const Text('WireGuard ile Bağlan (Test)'),
                      ),

                      const SizedBox(height: 12),

                      // Diğer sayfalar
                      ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  ProxyUsagePage(accessToken: jwt!),
                            ),
                          );
                        },
                        child: const Text('Proxy Kullanımını Göster'),
                      ),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => TwoFaPage(accessToken: jwt!),
                            ),
                          );
                        },
                        child: const Text('2FA Doğrula'),
                      ),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  UserDevicePage(accessToken: jwt!),
                            ),
                          );
                        },
                        child: const Text('Ek Kullanıcı/Cihaz Yönetimi'),
                      ),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  InAppPurchasePage(accessToken: jwt!),
                            ),
                          );
                        },
                        child: const Text('Satın Alma'),
                      ),
                      const SizedBox(height: 20),

                      const Text(
                        'VPN Logları:',
                        style: TextStyle(fontWeight: FontWeight.w600),
                      ),
                      const SizedBox(height: 8),
                      SizedBox(
                        height: 140,
                        child: ListView.builder(
                          itemCount: vpnLogs.length,
                          itemBuilder: (_, i) => Text(vpnLogs[i]),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            )
          : Scaffold(
              appBar: AppBar(title: const Text('Giriş Yap')),
              body: Center(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      LoginPage(onLogin: handleLogin),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: _loginWithGoogle,
                        child: const Text('Google ile Giriş'),
                      ),
                    ],
                  ),
                ),
              ),
            ),
    );
  }
}
