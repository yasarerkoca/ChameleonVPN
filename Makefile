COMPOSE ?= docker compose

.PHONY: help backend-up backend-down backend-migrate mobile-build mobile-test deps

help:
	@echo "Targets: backend-up | backend-down | backend-migrate | mobile-build | mobile-test"
backend-up:
	$(COMPOSE) up -d

backend-down:
	$(COMPOSE) down

backend-migrate:
	$(COMPOSE) exec backend alembic upgrade head
	cd backend && alembic upgrade head

deps:
	sudo apt-get update && sudo apt-get install -y openvpn wireguard-tools

mobile-build: deps

	cd chameleon_vpn_client && flutter clean && flutter pub get && flutter build apk
mobile-test:
	cd chameleon_vpn_client && flutter test && flutter test integration_test
firebase-deploy:
	cd infra/firebase && npx firebase deploy --config firebase.json
