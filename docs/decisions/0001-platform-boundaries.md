# ADR 0001: Platform Boundaries

## Status

Accepted.

## Decision

AGenNext Content Platform separates core responsibilities:

- Content API owns business data.
- Camunda owns process state.
- Langflow owns AI generation.
- n8n owns integration workers.
- Connector Runtime owns destination publishing.
- NATS owns platform events.

## Consequences

This prevents orchestration overlap and keeps every tool replaceable behind clear contracts.
