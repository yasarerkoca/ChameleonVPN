COMPOSE ?= docker compose

.PHONY: help backend-up backend-down backend-migrate mobile-build

help:
	@echo "Targets: backend-up | backend-down | backend-migrate | mobile-build"

backend-up:
	$(COMPOSE) up -d

backend-down:
	$(COMPOSE) down

backend-migrate:
	cd backend && alembic upgrade head

mobile-build:
	cd chameleon_vpn_client && flutter clean && flutter pub get && flutter build apk
