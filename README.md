# AGenNext Content Platform

Enterprise AI-native content operations platform for authoring, reviewing, approving, and publishing content across WordPress, GitHub Pages, RSS, Medium, Substack, and future channels.

## Status

`v0.1.0-alpha` release-ready foundation.

This alpha intentionally freezes platform boundaries before adding more connectors.

## Platform Stack

| Layer | Tool |
|---|---|
| Business workflow | Camunda 8 |
| AI pipelines | Langflow |
| Integrations/workers | n8n |
| Application backend | Appwrite-ready |
| Canonical content data | SurrealDB-ready |
| Event bus | NATS |
| Dashboard | Next.js |
| API | FastAPI |
| Deployment | Docker Compose + Helm |

## Service Boundaries

- **Content API** owns articles, versions, publications, workflow summaries, connector config, and events.
- **Camunda** owns BPMN process state, human tasks, timers, and approvals.
- **Langflow** owns AI research, writing, review, SEO, and structured content generation.
- **n8n** owns external integrations and repeatable worker automations.
- **Connector Runtime** owns publishing adapters such as WordPress, GitHub Pages, and RSS.
- **NATS** distributes immutable platform events.

## Local Run

```bash
cp .env.example .env
make dev
make smoke
```

Services:

| Service | URL |
|---|---|
| Dashboard | http://localhost:3000 |
| API | http://localhost:8080/docs |
| n8n | http://localhost:5678 |
| Langflow | http://localhost:7860 |
| NATS monitor | http://localhost:8222 |
| SurrealDB | http://localhost:8000 |

## Release Scope

v0.1.0-alpha includes:

- FastAPI Content API lifecycle scaffold
- Article create, validate, AI enhance, approve, workflow start, publish dry-run, archive
- Prometheus `/metrics`
- Next.js dashboard starter
- Connector SDK contract
- WordPress connector contract path
- RSS generation path
- GitHub Pages connector path
- Camunda BPMN and DMN seed artifacts
- Langflow seed flow
- n8n publish worker seed
- Docker Compose
- Helm skeleton
- GitHub Actions CI
- Security, release, contributing, roadmap, and ADR docs

## Release Checklist

```bash
make smoke
helm template agennext-content-platform deploy/helm
pytest -q apps/api/tests
```

## Repository Workflow

- `main` is the protected release branch.
- `release/v0.1.0-alpha` is the current alpha release branch.
- Feature work should use `feat/*` branches and merge via PR.

## License

Apache-2.0 unless changed by maintainers.
