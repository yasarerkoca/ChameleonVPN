import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  void _login() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Login success')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(key: const Key('emailField'), controller: _emailController),
            TextField(
              key: const Key('passwordField'),
              controller: _passwordController,
              obscureText: true,
            ),
            ElevatedButton(
              key: const Key('loginButton'),
              onPressed: _login,
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
