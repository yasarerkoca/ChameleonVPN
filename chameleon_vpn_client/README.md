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
flutter run --dart-define=BASE_URL=http://10.0.2.2:8000

## Test
flutter test --dart-define=BASE_URL=http://10.0.2.2:8000
flutter test integration_test --dart-define=BASE_URL=http://10.0.2.2:8000

## Build (Android)
flutter build apk --release --dart-define=BASE_URL=https://api.example.com

# Çıktı: build/app/outputs/flutter-apk/app-release.apk

## Google ile Giriş

Uygulama Google hesaplarıyla oturum açmayı destekler. Bu özelliği
etkinleştirmek için Google Cloud Console üzerinden bir OAuth istemcisi
oluşturun ve mobil uygulamaya uygun `client_id` değerini ayarlayın.

```dart
final token = await signInWithGoogle();
```

`signInWithGoogle` fonksiyonu kullanıcıyı Google hesabıyla
kimlik doğrular ve elde edilen ID token'ını backend API'sine göndererek
uygulama için bir erişim jetonu oluşturur.
