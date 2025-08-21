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
	@test -n "$(BASE_URL)" || (echo "BASE_URL not set. Use 'make mobile-build BASE_URL=https://api.example.com'" && exit 1)
	cd chameleon_vpn_client && flutter clean && flutter pub get && flutter build apk --dart-define=BASE_URL=$(BASE_URL)
mobile-test:
	@test -n "$(BASE_URL)" || (echo "BASE_URL not set. Use 'make mobile-test BASE_URL=https://api.example.com'" && exit 1)
	cd chameleon_vpn_client && flutter test --dart-define=BASE_URL=$(BASE_URL) && flutter test integration_test --dart-define=BASE_URL=$(BASE_URL)
firebase-deploy:
	cd infra/firebase && npx firebase deploy --config firebase.json
