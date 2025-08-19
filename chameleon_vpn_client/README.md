# Chameleon VPN Client (Flutter)

## Kurulum
flutter --version
flutter pub get

### Yerel Bağımlılıklar
Uygulamanın VPN tünellerini başlatabilmesi için hedef platformda
`wg-quick` ve `openvpn` araçlarının kurulu olması gerekir.

- **Linux**: `sudo apt install wireguard-tools openvpn`
- **macOS**: `brew install wireguard-tools openvpn`
- **Windows**: resmi sitelerinden WireGuard ve OpenVPN indirilmelidir.

## Geliştirme
flutter run

## Test
flutter test
flutter test integration_test

## Build (Android)
flutter build apk --release
# Çıktı: build/app/outputs/flutter-apk/app-release.apk
