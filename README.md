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

## 📚 Dokümantasyon ve Katkı

Ek belgeler için `chameleonvpn/docs/` dizinine göz atın. Katkıda bulunmak
isteyenler `CONTRIBUTING.md` dosyasını inceleyebilir.

## 🛡️ Lisans

Bütün hakları Yaşar Erkoca'a aittir.  
