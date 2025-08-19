import 'package:flutter/material.dart';
class UserDevicePage extends StatelessWidget {
  final String accessToken;
  const UserDevicePage({super.key, required this.accessToken});
  @override Widget build(BuildContext c)=>const Scaffold(body: Center(child: Text("Devices")));
}
