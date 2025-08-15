COMPOSE ?= docker compose

.PHONY: help backend-up backend-down backend-migrate mobile-build

help:
	@echo "Targets: backend-up | backend-down | backend-migrate | mobile-build"

backend-up:
	$(COMPOSE) up -d

backend-down:
	$(COMPOSE) down

backend-migrate:
	$(COMPOSE) exec backend alembic upgrade head
	cd backend && alembic upgrade head

mobile-build:
	cd chameleon_vpn_client && flutter clean && flutter pub get && flutter build apk
firebase-deploy:
	cd infra/firebase && npx firebase deploy --config firebase.json
