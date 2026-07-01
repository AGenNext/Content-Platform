# Architecture

AGenNext Content Platform is split by responsibility, not by tool preference.

```text
Users -> Dashboard -> Content API -> SurrealDB-ready state
                         |
                         +-> Camunda process state
                         +-> Langflow AI enrichment
                         +-> n8n integration workers
                         +-> Connector Runtime
                         +-> NATS events
```

## Principles

1. Content API is the only canonical writer for article state.
2. Camunda owns business workflow state.
3. Langflow returns structured AI output only.
4. n8n executes integration workers, not business process state.
5. Connectors implement a stable contract.
6. Events are immutable integration signals.
