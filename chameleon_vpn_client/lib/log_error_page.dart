import 'package:flutter/material.dart';
class LogErrorPage extends StatelessWidget {
  final String message;
  const LogErrorPage({super.key, required this.message});
  @override Widget build(BuildContext c)=>Scaffold(body: Center(child: Text(message)));
}
