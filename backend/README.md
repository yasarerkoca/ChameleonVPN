# Chameleon Backend (FastAPI)

## Çalıştırma (Docker)
docker compose up -d --build
# Swagger: http://localhost:8000/docs

## Lokal Geliştirme
cp .env.example .env
# `.env` içindeki değişkenleri ihtiyaca göre düzenleyin ve güçlü bir POSTGRES_PASSWORD ayarlayın
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

### Debug Modu
Varsayılan olarak `DEBUG` kapalıdır. Geliştirme için `.env` dosyanıza:

```
DEBUG=true
```

ya da komut satırından:

```
DEBUG=true uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Alembic
alembic upgrade head
alembic revision --autogenerate -m "change"
alembic downgrade -1

## Veritabanı Seed
```bash
python -m app.db.seed
```
Bu komut, varsayılan roller ve yönetici hesabını ekler.
Varsayılan yönetici bilgileri `ADMIN_EMAIL` ve `ADMIN_PASSWORD` ortam değişkenlerinden alınır.

## Test
pytest -q

## Sağlık/Koruma
- /healthz, /metrics aktif
- Rate limit: Redis
- Port kilitlenirse: `fuser -k 8000/tcp`

## ENV (özet)
- DB_URL=postgresql+psycopg2://vpnadmin:PASS@db:5432/chameleonvpn
- REDIS_URL=redis://redis:6379/0
- SECRET_KEY=change-me
- JWT_ALGO=HS256
- OAUTH_GOOGLE_CLIENT_ID=...
- `DATABASE_URL`=postgresql+psycopg2://vpnadmin:PASS@db:5432/chameleonvpn
- `REDIS_URL`=redis://redis:6379/0
- `SECRET_KEY`=change-me (JWT için zorunlu)
- `SESSION_SECRET_KEY`=change-me-too (SessionMiddleware için zorunlu)
- `JWT_ALGO`=HS256
- `GOOGLE_CLIENT_ID`=... (Google OAuth için zorunlu)
- `GOOGLE_CLIENT_SECRET`=... (Google OAuth için zorunlu)
- `GOOGLE_REDIRECT_URI`=https://yourdomain.com/auth/google/callback (Google OAuth için zorunlu)
- `PASSWORD_RESET_URL`=https://example.com/auth/password/reset (şifre sıfırlama linki temeli)
- `EMAIL_VERIFY_URL`=https://example.com/auth/verify-email (e-posta doğrulama linki temeli)
- `ALLOWED_ORIGINS`=https://app.example.com,https://admin.example.com (CORS için izinli originler)
- `STRIPE_API_KEY`=... (Stripe secret API anahtarı)
- `STRIPE_SUCCESS_URL`=https://yourdomain.com/success (Stripe başarı dönüş URL'i)
- `STRIPE_CANCEL_URL`=https://yourdomain.com/cancel (Stripe iptal dönüş URL'i)
- `IYZICO_CALLBACK_URL`=https://yourdomain.com/iyzico/callback (iyzico callback URL'i)
- `ADMIN_EMAIL`=admin@example.com (varsayılan yönetici e-posta adresi)
- `ADMIN_PASSWORD`=super-secure (varsayılan yönetici parolası, uygulama tarafından hashlenir)
