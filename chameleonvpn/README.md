# ChameleonVPN - Çok Katmanlı VPN Platformu

Türkiye merkezli, modern ve ölçeklenebilir VPN yönetim yazılımı.  
Backend, web admin panel, kullanıcı paneli, mobil uygulama, masaüstü, deployment, test ve çok daha fazlası!

---

## 📁 Proje Klasör Yapısı

```
chameleonvpn/
├── backend/      # Python tabanlı API & VPN sunucu
├── web-admin/    # Admin (yönetici) paneli (React)
├── web-user/     # Kullanıcı paneli (React)
├── mobile/       # Flutter mobil uygulama
├── desktop/      # Electron masaüstü uygulama
├── docs/         # Dökümantasyon ve rehberler
├── assets/       # Logolar, ikonlar ve görseller
├── i18n/         # Çoklu dil dosyaları
├── tests/        # Birim ve entegrasyon testleri
├── deployment/   # Docker, nginx, env dosyaları
```

---

## 🚀 **Kurulum (Kısa)**

1. Tüm zip dosyalarını ilgili klasörlere aç:
   ```bash
   unzip backend.zip -d backend
   unzip web-admin.zip -d web-admin
   unzip web-user.zip -d web-user
   unzip mobile.zip -d mobile
   unzip desktop.zip -d desktop
   unzip docs.zip -d docs
   unzip assets.zip -d assets
   unzip i18n.zip -d i18n
   unzip tests.zip -d tests
   unzip deployment.zip -d deployment
   ```

2. `deployment/` dizininden docker-compose ile başlatabilirsin:
   ```bash
   cd deployment
   docker-compose up --build
   ```

---

## 🖥️ **Her Modülün Kendi README.md'si ve Kurulumu Vardır.**

Örnek:
- **backend/** içinde `README.md` → Python ortamı, veritabanı vs.
- **mobile/** içinde `README.md` → Flutter kurulumu.
- **web-admin/** içinde `README.md` → npm kurulumu, local başlatma.

---

## 📚 **Ekstra Dökümantasyon**
- Kullanıcı ve yönetici kılavuzları için `docs/` dizinine bakabilirsin.
- API endpointleri için `docs/API.md` dosyasını inceleyebilirsin.

---

## 📢 **Geri Bildirim ve Katkı**
- Eksik/hatalı kısım veya önerin olursa lütfen issue oluştur ya da doğrudan bu README.md'yi düzenle!

---

## 🛡️ **Lisans**
MIT

---

**İyi kullanımlar!**
