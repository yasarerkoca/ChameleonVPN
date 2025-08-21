# Chameleon Backend (FastAPI)

## Çalıştırma (Docker)
docker compose up -d --build
# Swagger: http://localhost:8000/docs

## Lokal Geliştirme
cp .env.example .env
# `.env` içindeki değişkenleri ihtiyaca göre düzenleyin
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
- `OAUTH_GOOGLE_CLIENT_ID`=...
