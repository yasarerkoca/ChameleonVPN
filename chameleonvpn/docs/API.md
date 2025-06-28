# ChameleonVPN API
## Auth
- POST /auth/login
- POST /auth/register
## User
- GET /user/profile
- POST /vpn/connect
- POST /vpn/disconnect

### Örnek Kullanım
```bash
curl -X POST https://api.chameleonvpn.com/auth/login -d '{"email":"user@demo.com","password":"****"}'
```
