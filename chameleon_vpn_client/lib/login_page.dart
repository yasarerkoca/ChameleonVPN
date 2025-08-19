import 'package:flutter/material.dart';
class LoginPage extends StatelessWidget {
  final void Function(String jwt) onLogin;
  const LoginPage({super.key, required this.onLogin});
  @override Widget build(BuildContext c)=>Scaffold(appBar: AppBar(title: const Text("Login")),
    body: Center(child: ElevatedButton(onPressed:()=>onLogin("DUMMY_JWT"), child: const Text("Dev Login"))));
}
