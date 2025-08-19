# Flutter WireGuard Plugin
Basit WireGuard VPN bağlantıları için Flutter eklentisi.

## Gerekli Araçlar
Eklenti çalışmadan önce hedef platformda aşağıdaki komut satırı araçları
kurulu olmalıdır:

- `wg-quick` (wireguard-tools paketinde bulunur)
- `openvpn`

## Örnek Kullanım
```dart
import 'package:flutter_wireguard_plugin/flutter_wireguard_plugin.dart';

await FlutterWireguardPlugin.connect(configString);
await FlutterWireguardPlugin.disconnect();
FlutterWireguardPlugin.statusStream.listen(print);
```

