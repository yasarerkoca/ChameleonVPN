import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'state.dart';

class LoginPage extends ConsumerWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Center(
        child: ElevatedButton(
          key: const Key('devLogin'),
          onPressed: () {
            ref.read(appProvider.notifier).login(
                const User(name: 'Demo User', subscription: 'Pro', token: 'TOKEN'));
            Navigator.pushReplacementNamed(context, '/servers');
          },
          child: const Text('Dev Login'),
        ),
      ),
    );
  }
}
