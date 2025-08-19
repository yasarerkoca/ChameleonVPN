# ChameleonVPN

ChameleonVPN çok katmanlı bir VPN platformudur. Backend API, web tabanlı yönetim
ve kullanıcı panelleri, mobil uygulama ve daha fazlasını içerir.

[![Mobile Build](https://github.com/yasarerkoca/ChameleonVPN/actions/workflows/release.yml/badge.svg)](https://github.com/yasarerkoca/ChameleonVPN/actions/workflows/release.yml)


## 📁 Dizin Yapısı

```
backend/      # Python API
frontend/web-admin/    # Admin paneli (React)
frontend/web-user/     # Kullanıcı paneli (React)
mobile/       # Flutter mobil uygulama
chameleonvpn/
├── backend/      # API ve VPN sunucusu
├── frontend/web-admin/    # Yönetici paneli
├── frontend/web-user/     # Kullanıcı paneli
├── mobile/       # Mobil uygulama
├── desktop/      # Masaüstü uygulama
├── docs/         # Dökümantasyon
├── assets/       # Görseller
├── i18n/         # Dil dosyaları
├── tests/        # Testler
├── deployment/   # Docker ve yapılandırmalar
```

## 🚀 Kısa Kurulum

`deployment/` dizininden Docker ile sistemi başlatabilirsiniz:

```bash
cd chameleonvpn/deployment
docker-compose up --build
```

Her modül kendi klasöründe ayrıntılı bir `README.md` dosyası barındırır.

## Kullanıcı Doğrulama

Yeni kayıt olan kullanıcılar e-postalarına gönderilen bağlantı ile hesaplarını doğrulamalıdır.
Doğrulanmamış hesaplar giriş yapmaya çalıştığında API `403 Forbidden` döner ve hesap "pending verification" durumunda kalır.

## ⚙️ Gereksinimler

## 🔌 Kullanım Örneği

Aşağıdaki örnek, WireGuard eklentisi ile bir tünelin nasıl başlatılıp durdurulacağını gösterir:

```dart
const config = '''
[Interface]
PrivateKey = <private-key>
Address = 10.0.0.2/32

[Peer]
PublicKey = <peer-public-key>
AllowedIPs = 0.0.0.0/0
Endpoint = vpn.example.com:51820
''';

final channel = const MethodChannel('flutter_wireguard_plugin');

Future<void> connect() async {
  await channel.invokeMethod('connect', {'config': config});
}

Future<void> disconnect() async {
  await channel.invokeMethod('disconnect');
}
```


## ⚙️ Ortam Değişkenleri

Uygulamayı Docker ile çalıştırmadan önce aşağıdaki ortam değişkeninin tanımlanması gerekir:

- `POSTGRES_PASSWORD` – PostgreSQL veritabanı parolası.

İsteğe bağlı değişkenler:

- `UVICORN_WORKERS` – Uvicorn işçi sayısı (varsayılan `2`).


## 📚 Dokümantasyon ve Katkı

Ek belgeler için `chameleonvpn/docs/` dizinine göz atın. Katkıda bulunmak
isteyenler `CONTRIBUTING.md` dosyasını inceleyebilir.

## 🛡️ Lisans

Bütün hakları Yaşar Erkoca'a aittir.
Ayrıntılar için `chameleon_vpn_client/plugins/flutter_wireguard_plugin/LICENSE` dosyasına bakın.
