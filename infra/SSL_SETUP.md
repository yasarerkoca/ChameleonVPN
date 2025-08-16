# Domain + SSL (son aşama)

## Nginx reverse-proxy (örnek)
# 80 -> 443 yönlendirme, 443 -> backend:8000
# Let's Encrypt için certbot örnekleri eklenir.

## Adımlar
1) DNS A kaydı -> sunucu IP
2) Nginx host dosyası -> backend upstream
3) certbot --nginx -d domain.com -d www.domain.com
4) Otomatik yenileme: systemd timer/cron
