import 'package:flutter/material.dart';
import 'package:openvpn_flutter/openvpn_flutter.dart';
import '../api_service.dart';
import 'package:flutter/services.dart' show rootBundle;

/// Simple VPN connection screen using the openvpn_flutter plugin.
class VpnScreen extends StatefulWidget {
  const VpnScreen({super.key, required this.token, required this.api});

  final String token;
  final ApiService api;

  @override
  State<VpnScreen> createState() => _VpnScreenState();
}

class _VpnScreenState extends State<VpnScreen> {
  late OpenVPN _vpn;
  VpnStatus? _status;
  bool _connecting = false;

  @override
  void initState() {
    super.initState();
    _vpn = OpenVPN(
      onVpnStatusChanged: (status) {
        setState(() => _status = status);
      },
      onVpnStageChanged: (_) {},
    );
  }

  Future<void> _connect() async {
    setState(() => _connecting = true);
    final config = await rootBundle.loadString('assets/vpn_config.ovpn');
    await widget.api.startVpnSession(widget.token);
    await _vpn.connect(config, 'chameleon');
    if (mounted) setState(() => _connecting = false);
  }

  Future<void> _disconnect() async {
    await _vpn.disconnect();
  }

  @override
  Widget build(BuildContext context) {
    final connected = _status?.connected == true;
    return Scaffold(
      appBar: AppBar(title: const Text('VPN')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Durum: ${_status?.status ?? 'Bağlı değil'}'),
            const SizedBox(height: 20),
            if (_connecting)
              const CircularProgressIndicator()
            else if (connected)
              ElevatedButton(
                onPressed: _disconnect,
                child: const Text('Bağlantıyı Kes'),
              )
            else
              ElevatedButton(
                onPressed: _connect,
                child: const Text('Bağlan'),
              ),
          ],
        ),
      ),
    );
  }
}
