# ChameleonVPN

ChameleonVPN çok katmanlı bir VPN platformudur: **FastAPI Backend**, **web tabanlı paneller** ve **Flutter mobil/masaüstü istemcisi** içerir.

[![Mobile Build](https://github.com/yasarerkoca/ChameleonVPN/actions/workflows/release.yml/badge.svg)](https://github.com/yasarerkoca/ChameleonVPN/actions/workflows/release.yml)

## 📁 Dizin Yapısı (Monorepo)

```
backend/                   # FastAPI API (PostgreSQL, Redis)
frontend/
  ├─ web-admin/            # Admin panel (React)
  └─ web-user/             # Kullanıcı paneli (React)
chameleon_vpn_client/      # Flutter istemci (Android/iOS/Windows/macOS/Linux)
desktop/                   # Masaüstü uygulama (varsa)
docs/                      # Dokümantasyon
infra/                     # Docker/CI/Scriptler (örn. infra/scripts)
archive/                   # Eski/deneme içerikler (build’e dahil edilmez)
docker-compose.yml         # Geliştirme orkestrasyonu
```

> Not: Eski README’de geçen `mobile/` klasörü artık **`chameleon_vpn_client/`**.

---

## 🚀 Hızlı Başlangıç (Docker)

Önkoşullar: **Docker** ve **Docker Compose**

1) Ortam dosyalarını oluştur:
```bash
cp backend/.env.example backend/.env
# backend/.env ve .env içindeki kritik değişkenleri doldur:
# - POSTGRES_PASSWORD=...
# - ALLOWED_ORIGINS=...
# - EMAIL_VERIFY_URL=...
# (Diğerleri: backend/.env.example içinde)
```

2) Veritabanı ve Redis’i başlat:
```bash
docker-compose up -d --build db redis
```

3) Alembic migration (tek seferlik):
```bash
# Migrate servisi varsa:
docker-compose run --rm migrate
# Yoksa backend konteyneri içinden:
docker-compose run --rm backend bash -lc "cd /srv && alembic -c alembic.ini upgrade head"
```

4) Backend’i ve Web’i başlat:
```bash
docker-compose up -d backend web
```
> WireGuard peers are configured inside the container. The `backend` service now requires
> `NET_ADMIN` capability and access to the host's `/etc/wireguard` directory. Ensure the host
> exposes `/etc/wireguard` and supports these permissions when starting the stack.

5) Sağlık kontrolü:
```bash
curl -sS http://127.0.0.1/api/healthz
```

> Sorun olursa port çakışmalarını temizleyin: `fuser -k 8000/tcp`

---

## 🧑‍💻 Yerel Geliştirme (Docker’sız)

```bash
cd backend
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# .env içindeki değerleri doldur
alembic -c alembic.ini upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔐 Kimlik Doğrulama Akışı

- Yeni kayıt olan kullanıcı, e-postasına gelen doğrulama linki ile hesabını **aktif** eder.
- Doğrulanmamış hesaplara API **403 Forbidden** döner (pending verification).
- JWT tabanlı oturum, refresh mekanizması ve opsiyonel 2FA (TOTP) desteği bulunur.

---

## ⚙️ Ortam Değişkenleri

 Tüm örnekler `backend/.env.example` ve `.env` dosyalarında yer alır. Başlıca değişkenler:
- **Veritabanı:** `POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- **Uygulama:** `ALLOWED_ORIGINS`, `EMAIL_VERIFY_URL`, `UVICORN_WORKERS`
- **Admin:** `ADMIN_EMAIL`, `ADMIN_PASSWORD` (ilk kurulumda varsayılan yönetici)
- **Cache/Queue (varsa):** `REDIS_URL`
- **Güvenlik (varsa):** `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES` vb.

> Üretimde gizlileri **repo dışında** yönetin (Actions Secrets / Vault). `.env` dosyasını **commit etmeyin**.

---

## 🧩 Migration ve Veritabanı

- Tüm modeller Alembic ile versiyonlanır.
- Yükseltme:
  ```bash
  alembic -c alembic.ini upgrade head
  ```
- Versiyon görüntüleme:
  ```bash
  alembic -c alembic.ini current -v
  ```

---

## 🖥️ Frontend (Admin & User)

Geliştirme:
```bash
cd frontend/web-admin
npm install
npm run dev

cd ../web-user
npm install
npm run dev
```

API tabanı ve CORS izinleri `backend/.env` üzerinden yönetilir.

---

## 📱 Flutter İstemci (chameleon_vpn_client)

Kurulum ve derleme:
```bash
cd chameleon_vpn_client
flutter pub get
flutter run            # geliştirme
flutter build apk      # Android release
# iOS için Xcode/sertifika gereklidir.
```

OpenVPN/WireGuard eklentileri için platform izinlerini `AndroidManifest.xml` ve iOS projelerinde tanımlayın.

---

## 🧪 Test & Kalite

- Backend: `pytest` (uygunsa)
- Lint/Format: `ruff`, `black`, `isort` (projede varsa)
- CI: GitHub Actions badge yukarıdadır. Gerekli secret’lar aşağıda.

---

## 🔐 GitHub Actions Secrets

**Settings → Secrets and variables → Actions** bölümünde:

- Deploy: `PROD_HOST`, `PROD_USER`, `PROD_SSH_KEY`
- Android imzalama: `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_PASSWORD`, `ANDROID_KEY_ALIAS`
- iOS imzalama: `IOS_CERT_BASE64`, `IOS_PROVISION_PROFILE_BASE64`, `IOS_CERT_PASSWORD`

---

## 🆘 Sorun Giderme

- **Backend unhealthy / web açılmıyor:** Migration’ları uygulayın, DB/Redis ayakta mı kontrol edin.
- **Port kullanılıyor:** `fuser -k 8000/tcp`
- **Docker build yavaş/karmaşık:** `archive/`, `node_modules`, `.venv`, `build/` klasörlerini `.dockerignore` ile hariç tutun.
- **`.env` sızıntısı:** `.gitignore`’a ekleyin, anahtarları **rotation** yapın.

---

## 📚 Dokümantasyon ve Katkı

Ek belgeler için `docs/` dizinine göz atın. Katkıda bulunmak için `CONTRIBUTING.md` (varsa) rehberini izleyin.

---

## 📄 Policies

- [Privacy Policy](docs/privacy.md)
- [Terms of Service](docs/terms.md)

---

## 🛡️ Lisans

Tüm hakları **Yaşar Erkoca**’ya aittir. Ayrıntılar için ilgili lisans dosyalarına bakın (örn. `chameleon_vpn_client/plugins/flutter_wireguard_plugin/LICENSE`).
