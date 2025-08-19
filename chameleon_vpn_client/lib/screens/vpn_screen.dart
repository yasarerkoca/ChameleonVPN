import 'dart:async';
import 'dart:io' show Platform;
import 'package:flutter/material.dart';
import 'package:openvpn_flutter/openvpn_flutter.dart';
import 'package:flutter_wireguard_plugin/flutter_wireguard_plugin.dart';
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
  OpenVPN? _vpn;
  VpnStatus? _status;
  String _wgStatus = 'Bağlı değil';
  bool _connecting = false;
  late final bool _useWireGuard;
  StreamSubscription<String>? _wgSub;

  @override
  void initState() {
    super.initState();
    _useWireGuard = !(Platform.isAndroid || Platform.isIOS);
    if (_useWireGuard) {
      _wgSub = FlutterWireguardPlugin.statusStream.listen((status) {
        setState(() => _wgStatus = status);
      });
    } else {
      _vpn = OpenVPN(
        onVpnStatusChanged: (status) {
          setState(() => _status = status);
        },
        onVpnStageChanged: (_) {},
      );
    }
  }

  Future<void> _connect() async {
    setState(() => _connecting = true);
    final config = await rootBundle.loadString('assets/vpn_config.ovpn');
    await widget.api.startVpnSession(widget.token);
    if (_useWireGuard) {
      await FlutterWireguardPlugin.connect(config);
    } else {
      await _vpn!.connect(config, 'chameleon');
    }
    if (mounted) setState(() => _connecting = false);
  }

  Future<void> _disconnect() async {
    if (_useWireGuard) {
      await FlutterWireguardPlugin.disconnect();
    } else {
      await _vpn!.disconnect();
    }
  }

  @override
  void dispose() {
    _wgSub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final connected = _useWireGuard ? _wgStatus == 'connected' : _status?.connected == true;
    final statusText = _useWireGuard ? _wgStatus : (_status?.status ?? 'Bağlı değil');
    return Scaffold(
      appBar: AppBar(title: const Text('VPN')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Durum: $statusText'),
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
