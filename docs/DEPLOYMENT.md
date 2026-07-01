# Deployment Guide

## Local Docker Compose

```bash
cp .env.example .env
docker compose up -d --build
make smoke
```

Services:

- Dashboard: http://localhost:3000
- API: http://localhost:8080/docs
- n8n: http://localhost:5678
- Langflow: http://localhost:7860
- NATS monitor: http://localhost:8222

## k3s / Kubernetes

```bash
bash scripts/deploy-k3s.sh
```

Equivalent manual commands:

```bash
kubectl create namespace content-platform --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install content-platform ./deploy/helm -n content-platform
kubectl rollout status deployment/agennext-content-api -n content-platform
kubectl rollout status deployment/agennext-content-dashboard -n content-platform
kubectl get pods -n content-platform
```

## Smoke validation

For local API:

```bash
make smoke
```

For a port-forwarded Kubernetes API:

```bash
kubectl port-forward svc/agennext-content-api 8080:8080 -n content-platform
BASE=http://localhost:8080 make smoke
```

## Current alpha limitations

- Helm chart deploys API and dashboard only.
- Docker Compose runs the wider local tool stack.
- Live WordPress publishing still requires real connector credentials and the next connector-hardening milestone.
