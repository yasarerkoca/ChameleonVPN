import 'package:flutter/material.dart';
import '../api_service.dart';
import 'vpn_screen.dart';

/// Displays the subscription info and allows starting the VPN.
class SubscriptionScreen extends StatefulWidget {
  const SubscriptionScreen({super.key, required this.token, required this.api});

  final String token;
  final ApiService api;

  @override
  State<SubscriptionScreen> createState() => _SubscriptionScreenState();
}

class _SubscriptionScreenState extends State<SubscriptionScreen> {
  Map<String, dynamic>? _subscription;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final sub = await widget.api.fetchSubscription(widget.token);
    if (mounted) {
      setState(() => _subscription = sub);
    }
  }

  void _startVpn() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => VpnScreen(token: widget.token, api: widget.api),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Abonelik')),
      body: Center(
        child: _subscription == null
            ? const CircularProgressIndicator()
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Durum: ${_subscription!['status']}'),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: _startVpn,
                    child: const Text('VPN\'e Bağlan'),
                  ),
                ],
              ),
      ),
    );
  }
}
