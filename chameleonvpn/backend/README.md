# ChameleonVPN Backend (FastAPI)

- JWT oturum desteği
- SQLAlchemy SQLite örneği
- /auth, /vpn, /admin endpointleri
- Docker ile çalıştırılır

## Başlatmak için:
docker build -t chameleonvpn-backend .
docker run -p 8000:8000 chameleonvpn-backend
