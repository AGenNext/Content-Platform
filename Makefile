SHELL := /usr/bin/env bash

.PHONY: dev up down smoke test helm-template release-check

dev: up
	@echo "API: http://localhost:8080/docs"
	@echo "Dashboard: http://localhost:3000"

up:
	docker compose up -d --build

down:
	docker compose down

smoke:
	bash scripts/smoke.sh

test:
	cd apps/api && PYTHONPATH=. pytest -q

helm-template:
	helm template agennext-content-platform deploy/helm

release-check: test smoke helm-template
