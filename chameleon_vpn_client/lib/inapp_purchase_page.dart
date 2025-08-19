import 'package:flutter/material.dart';
class InAppPurchasePage extends StatelessWidget {
  final String accessToken;
  const InAppPurchasePage({super.key, required this.accessToken});
  @override Widget build(BuildContext c)=>const Scaffold(body: Center(child: Text("IAP")));
}
