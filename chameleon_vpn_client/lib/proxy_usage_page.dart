import 'package:flutter/material.dart';
class ProxyUsagePage extends StatelessWidget {
  final String accessToken;
  const ProxyUsagePage({super.key, required this.accessToken});
  @override Widget build(BuildContext c)=>const Scaffold(body: Center(child: Text("Proxy Usage")));
}
