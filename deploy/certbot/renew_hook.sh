#chmod +x deploy/certbot/renew_hook.sh
#!/bin/sh
echo "🔄 Reloading nginx in web container..."
docker exec $(docker ps -qf "name=chameleonvpn-web-1") nginx -s reload
