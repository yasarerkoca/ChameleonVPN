import 'package:flutter/material.dart';
import '../api_service.dart';
import 'subscription_screen.dart';

/// Basic login form that authenticates the user against the API.
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final ApiService api = ApiService(baseUrl: 'https://example.com/api');
  String? _error;

  Future<void> _login() async {
    final token =
        await api.login(_emailController.text, _passwordController.text);
    if (!mounted) return;
    if (token != null) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => SubscriptionScreen(token: token, api: api),
        ),
      );
    } else {
      setState(() => _error = 'Giriş başarısız oldu');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Giriş Yap')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'E-posta'),
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Şifre'),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _login,
              child: const Text('Giriş'),
            ),
            if (_error != null) ...[
              const SizedBox(height: 20),
              Text(_error!, style: const TextStyle(color: Colors.red)),
            ]
          ],
        ),
      ),
    );
  }
}
