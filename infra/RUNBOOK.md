# Operasyon RUNBOOK

## Backup
- Git: infra/scripts/git-backup.sh
- DB dump: scripts/db_backup.sh (eklenecekse: pg_dump, günlük)

## Restore
- pg_restore / psql < dump.sql

## Monitoring
- Prometheus target: backend:8000/metrics
- Grafana dashboard: backend request/latency

## Nginx Reload
- Konfigürasyon değişikliklerinden sonra Nginx'i yeniden yükleyin:

```bash
docker compose exec nginx nginx -s reload
```
