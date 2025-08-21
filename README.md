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

`deployment/` dizininden Docker ile sistemi başlatabilirsiniz. Öncelikle örnek
ortam dosyasını kopyalayın:

```bash
cp backend/.env.example backend/.env
POSTGRES_PASSWORD=<parola> docker-compose up --build
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

Örnek değişkenler `backend/.env.example` dosyasında yer alır. Docker ile
çalıştırmadan önce bu dosyayı `backend/.env` olarak kopyalayıp düzenleyin ve
aşağıdaki ortam değişkenini tanımlayın:

- `POSTGRES_PASSWORD` – PostgreSQL veritabanı parolası.

İsteğe bağlı değişkenler:

- `UVICORN_WORKERS` – Uvicorn işçi sayısı (varsayılan `2`).

## 🔐 GitHub Actions Secrets

Projeyi GitHub Actions ile dağıtırken şu gizli değişkenleri **Settings ➜ Secrets and variables ➜ Actions** altında tanımlayın:

- `PROD_HOST`, `PROD_USER`, `PROD_SSH_KEY` – üretim sunucusuna SSH ile bağlanmak için.
- `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_PASSWORD`, `ANDROID_KEY_ALIAS` – Android imzalama anahtarları.
- `IOS_CERT_BASE64`, `IOS_PROVISION_PROFILE_BASE64`, `IOS_CERT_PASSWORD` – iOS imzalama sertifikaları.


## 📚 Dokümantasyon ve Katkı

Ek belgeler için `chameleonvpn/docs/` dizinine göz atın. Katkıda bulunmak
isteyenler `CONTRIBUTING.md` dosyasını inceleyebilir.

## 📄 Policies

- [Privacy Policy](docs/privacy.md)
- [Terms of Service](docs/terms.md)


## 🛡️ Lisans

Bütün hakları Yaşar Erkoca'a aittir.
Ayrıntılar için `chameleon_vpn_client/plugins/flutter_wireguard_plugin/LICENSE` dosyasına bakın.
