# Operasyon RUNBOOK

## Backup
- Git: infra/scripts/git-backup.sh
- Services: infra/scripts/backup.sh
- Postgres ve Redis dump'larını `$HOME/backups/<timestamp>` dizinine yazar.
- Varsayılan olarak 7 günlük yedek saklanır (`RETENTION_DAYS` ile değiştirilebilir).
- Çalıştırmadan önce `PGPASSWORD` değişkenini ayarlayın.
## Restore
- Postgres ve Redis verilerini geri yüklemek için `infra/scripts/restore.sh [timestamp]` kullanın.
- Timestamp verilmezse en son yedekten geri yükler.
## Monitoring
- Prometheus konfigurasyonu `infra/prometheus.yml` dosyasında. Çalıştırmak için:

  ```bash
  docker run -p 9090:9090 -v $(pwd)/infra/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
  ```

- Grafana için sağlanan provisioning `infra/grafana/` klasöründe. Başlatmak için:

  ```bash
  docker run -p 3000:3000 \
    -v $(pwd)/infra/grafana/provisioning:/etc/grafana/provisioning \
    -v $(pwd)/infra/grafana/dashboards:/etc/grafana/dashboards \
    grafana/grafana
  ```

- Dashboard, backend ve veritabanı metriklerini gösterir.
- Backend `SENTRY_DSN` ortam değişkeni tanımlandığında Sentry'ye hata raporları gönderir.
## Nginx Reload
- Konfigürasyon değişikliklerinden sonra Nginx'i yeniden yükleyin:

```bash
docker compose exec nginx nginx -s reload
```
