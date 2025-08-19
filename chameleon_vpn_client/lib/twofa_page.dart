import 'package:flutter/material.dart';
class TwoFaPage extends StatelessWidget {
  final String accessToken;
  const TwoFaPage({super.key, required this.accessToken});
  @override Widget build(BuildContext c)=>const Scaffold(body: Center(child: Text("2FA")));
}
