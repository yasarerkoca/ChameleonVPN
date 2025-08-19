# 0001 - ChameleonVPN Mimari Kararları

## Durum
Kabul edildi

## Bağlam
ChameleonVPN; FastAPI tabanlı bir API, PostgreSQL veri tabanı, Redis önbelleği ve çok sayıda domain‑odaklı router içeren çok katmanlı bir VPN platformudur. Sistem Docker ile konteynerize edilmiştir.

## Karar
- Backend için **FastAPI** tercih edildi; asenkron performans ve tip güvenliği sağlar.
- Domain ayrımı için `routers` yapısı kullanıldı (auth, admin, vpn, payment vb.).
- **PostgreSQL** kalıcı veri deposu, **Redis** ise hem hız hem de hız limiti için kullanılır.
- Güvenlik ve gözlenebilirlik için çok sayıda middleware uygulanır (MFA, IP bloklama, oturum takibi, loglama).
- Dağıtım ve geliştirme sürecini sadeleştirmek adına **Docker Compose** ile çoklu servis kurulumu yapılır.

## Sonuçlar
- Servisler ayrı konteynerlerde çalıştığından bağımsız ölçeklenebilir.
- Middleware katmanı sayesinde saldırı ve anomali tespiti erken aşamada yapılabilir.
- Docker temelli yapı, yerel geliştirme ile üretim ortamı arasında tutarlılık sağlar.
