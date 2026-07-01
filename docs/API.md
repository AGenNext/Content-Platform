# API Contract

Base URL: `http://localhost:8080`

## Health

- `GET /health`
- `GET /metrics`

## Articles

- `POST /articles`
- `GET /articles`
- `GET /articles/{article_id}`
- `PATCH /articles/{article_id}`
- `POST /articles/{article_id}/validate`
- `POST /articles/{article_id}/approve`
- `POST /articles/{article_id}/archive`
- `GET /articles/{article_id}/versions`

## AI

- `POST /ai/enhance`

## Workflow

- `POST /workflows/start`
- `POST /workflows/{workflow_id}/complete`

## Publishing

- `POST /publish`
- `GET /publications`

## Events

- `GET /events`

## Connectors

- `GET /connectors/health`
