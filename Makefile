.PHONY: help backend-up backend-down backend-migrate mobile-build

help:
	@echo "Targets: backend-up | backend-down | backend-migrate | mobile-build"

backend-up:
	docker compose up -d

backend-down:
	docker compose down

backend-migrate:
	cd backend && alembic upgrade head

mobile-build:
	cd chameleon_vpn_client && flutter clean && flutter pub get && flutter build apk
