# ChameleonVPN Dokümantasyonu

Bu belge API uç noktalarını, mimari kararları ve kurulum/dağıtım adımlarını özetler.

## API Uçları

### Genel
- `GET /` – API çalışıyor mu kontrol eder
- `GET /healthz` – servis sağlık kontrolü
- `GET /download/apk` – resmi mağaza dışı APK istekleri için 410 döner
- `GET /test-limit` – örnek hız limiti uç noktası

### Kimlik Doğrulama
- `POST /auth/register` – yeni kullanıcı kaydı
- `POST /auth/login` – JWT tabanlı giriş
- `GET /auth/verify-email` – e‑posta doğrulama
- `GET /auth/profile/me` – mevcut kullanıcı bilgisi
- `PUT /auth/profile/me` – profil güncelleme
- `POST /auth/profile/change-password` – şifre değiştirme
- `DELETE /auth/profile/me` – hesabı devre dışı bırakma
- `GET /auth/google/login` – Google OAuth girişini başlatır
- `GET /auth/google/callback` – Google OAuth dönüşü
- `POST /auth/google/token` – mobil token doğrulama

### Yönetim (Admin)
- `/admin/api-keys/*` – API anahtarı oluşturma, listeleme, pasifleştirme
- `/admin/corporate-groups/*` – grup yönetimi ve kullanıcı atamaları
- `/admin/session/*` – aktif oturumları listeleme ve sonlandırma
- `/admin/proxy/*` – proxy IP ve kota yönetimi
- `/admin/quota/*` – kullanıcı ve grup kotaları
- Diğer başlıklar: IP engelleme, güvenlik kontrolleri, AI log incelemeleri

### Diğer Modüller
- `payment`, `billing`, `provider`, `webhook` – ödeme servisleri
- `membership` – plan ve abonelik işlemleri
- `vpn` – sunucu, bağlantı ve trafik kayıtları
- `corporate` – kurumsal uç noktalar
- `monitor` – sistem ve DNS sızıntı kontrolleri
- `proxy` – son kullanıcı proxy hizmetleri

## Kurulum ve Dağıtım

### Geliştirme Ortamı
1. `cd backend`
2. `cp .env.example .env` ve gereken değişkenleri düzenleyin
3. `python -m venv venv && source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Docker ile Çalıştırma
1. `POSTGRES_PASSWORD` ortam değişkenini belirleyin
2. `docker-compose up --build` komutu ile servisleri başlatın
3. API `http://localhost:8000` adresinden ulaşılabilir

### Üretim (production.yml)
- Nginx ve Certbot içeren gelişmiş yapılandırma
- `docker compose -f production.yml up -d` ile çalıştırılabilir

## Mimari
Ayrıntılı karar kayıtları için `docs/adr/0001-record-architecture.md` dosyasına bakın.
