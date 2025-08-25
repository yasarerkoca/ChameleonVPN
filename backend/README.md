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
## Authentication & 2FA

### `/auth/login` workflow
1. `POST /auth/login` with JSON `{ "email": "user@example.com", "password": "..." }`.
2. On success the API returns an `access_token` and `refresh_token`.
3. If the account requires two‑factor authentication and `is_2fa_verified` is `false`, most other endpoints will respond with `403` until a second factor is validated.
4. Submit a six‑digit code from your authenticator app to `POST /auth/2fa/login-totp` together with the `email`, or verify a one‑time code sent via e‑mail using `POST /auth/2fa/verify`.
5. Successful verification sets a `remember_device` cookie and the user gains full access.

### Enabling and verifying TOTP 2FA
1. Authenticate normally and send the `Authorization: Bearer <token>` header in subsequent requests.
2. `POST /auth/2fa/setup` (alias `/auth/2fa/generate-totp-secret`) to obtain a `secret` and `otp_auth_url` for QR generation.
3. Scan the QR code or manually enter the `secret` into a TOTP application (Google Authenticator, Authy, etc.).
4. Generate a code in the app and call `POST /auth/2fa/login-totp` with `{ "email": "user@example.com", "totp_code": "123456" }` to verify.
5. The backend marks the user as 2FA verified; future logins will require the same TOTP step unless the `remember_device` cookie is present.

### SMTP configuration & testing
E‑posta gönderimi için `.env` dosyanızda aşağıdaki değişkenleri tanımlayın:

```
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=super-secret
SMTP_FROM=noreply@example.com  # opsiyonel, SMTP_USER varsayılır
```

Geliştirmede e‑posta teslimatını test etmek için MailHog gibi yerel bir SMTP sunucusu kullanabilirsiniz:

```
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

`SMTP_HOST=localhost` ve `SMTP_PORT=1025` ayarlayın; gelen mesajları `http://localhost:8025` adresinden görüntüleyin.

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
- DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
- REDIS_URL=redis://redis:6379/0
- SECRET_KEY=change-me
- JWT_ALGO=HS256
- OAUTH_GOOGLE_CLIENT_ID=...
- `DATABASE_URL`=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
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
- `SMTP_HOST`=smtp.example.com (SMTP sunucusu)
- `SMTP_PORT`=587 (varsayılan TLS portu)
- `SMTP_USER`=user@example.com
- `SMTP_PASS`=super-secret
- `SMTP_FROM`=noreply@example.com (opsiyonel, SMTP_USER varsayılır)
