from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from slugify import slugify

app = FastAPI(title="AGenNext Content API", version="0.1.0-alpha")

ARTICLES: dict[str, dict[str, Any]] = {}
VERSIONS: dict[str, list[dict[str, Any]]] = {}
PUBLICATIONS: dict[str, dict[str, Any]] = {}
WORKFLOWS: dict[str, dict[str, Any]] = {}
EVENTS: list[dict[str, Any]] = []


class ArticleStatus(str, Enum):
    draft = "draft"
    validated = "validated"
    ai_ready = "ai_ready"
    review = "review"
    approved = "approved"
    publishing = "publishing"
    published = "published"
    failed = "failed"
    archived = "archived"


class ArticleCreate(BaseModel):
    title: str = Field(min_length=3)
    slug: str | None = None
    author: str = "Chinmay Panda"
    body: str = Field(min_length=1)
    excerpt: str | None = None
    cover_image: str | None = None
    tags: list[str] = []
    categories: list[str] = []
    channels: list[str] = ["wordpress"]


class ArticleUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    excerpt: str | None = None
    cover_image: str | None = None
    tags: list[str] | None = None
    categories: list[str] | None = None
    channels: list[str] | None = None
    status: ArticleStatus | None = None


class PublishRequest(BaseModel):
    article_id: str
    channels: list[str] = ["rss"]
    dry_run: bool = True


class EnhanceRequest(BaseModel):
    article_id: str
    apply: bool = True


class WorkflowRequest(BaseModel):
    article_id: str
    workflow: str = "content-publishing"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(event_type: str, subject_id: str, payload: dict[str, Any] | None = None) -> None:
    EVENTS.append({"type": event_type, "subject_id": subject_id, "payload": payload or {}, "created_at": now()})


def get_article(article_id: str) -> dict[str, Any]:
    article = ARTICLES.get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    return article


def snapshot(article: dict[str, Any]) -> None:
    VERSIONS.setdefault(article["id"], []).append({**article, "snapshot_at": now()})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}


@app.get("/metrics")
def metrics() -> Response:
    body = "\n".join([
        f"agennext_articles_total {len(ARTICLES)}",
        f"agennext_publications_total {len(PUBLICATIONS)}",
        f"agennext_events_total {len(EVENTS)}",
    ]) + "\n"
    return Response(body, media_type="text/plain")


@app.post("/articles")
def create_article(payload: ArticleCreate) -> dict[str, Any]:
    article_id = f"article_{uuid4().hex[:12]}"
    created = now()
    article = payload.model_dump()
    article.update({"id": article_id, "slug": payload.slug or slugify(payload.title), "status": ArticleStatus.draft, "version": 1, "created_at": created, "updated_at": created})
    ARTICLES[article_id] = article
    snapshot(article)
    emit("content.created", article_id)
    return article


@app.get("/articles")
def list_articles(q: str | None = None, status: ArticleStatus | None = None) -> list[dict[str, Any]]:
    items = list(ARTICLES.values())
    if q:
        query = q.lower()
        items = [a for a in items if query in a["title"].lower() or query in a["body"].lower()]
    if status:
        items = [a for a in items if a["status"] == status]
    return sorted(items, key=lambda a: a["updated_at"], reverse=True)


@app.get("/articles/{article_id}")
def read_article(article_id: str) -> dict[str, Any]:
    return get_article(article_id)


@app.patch("/articles/{article_id}")
def update_article(article_id: str, payload: ArticleUpdate) -> dict[str, Any]:
    article = get_article(article_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            article[key] = value
    article["version"] += 1
    article["updated_at"] = now()
    snapshot(article)
    emit("content.updated", article_id)
    return article


@app.get("/articles/{article_id}/versions")
def article_versions(article_id: str) -> list[dict[str, Any]]:
    get_article(article_id)
    return VERSIONS.get(article_id, [])


@app.post("/articles/{article_id}/validate")
def validate_article(article_id: str) -> dict[str, Any]:
    article = get_article(article_id)
    if len(article["body"].split()) < 30:
        raise HTTPException(status_code=422, detail="article body must contain at least 30 words")
    article["status"] = ArticleStatus.validated
    article["updated_at"] = now()
    emit("content.validated", article_id)
    return article


@app.post("/ai/enhance")
def enhance(payload: EnhanceRequest) -> dict[str, Any]:
    article = get_article(payload.article_id)
    generated = {"seo_title": article["title"][:60], "meta_description": (article.get("excerpt") or article["body"][:150]).strip(), "tags": sorted(set(article.get("tags", []) + ["AI", "Content Operations"])), "summary": article["body"][:240]}
    if payload.apply:
        article["tags"] = generated["tags"]
        article["status"] = ArticleStatus.ai_ready
        article["updated_at"] = now()
        emit("ai.completed", payload.article_id, generated)
    return generated


@app.post("/articles/{article_id}/approve")
def approve(article_id: str) -> dict[str, Any]:
    article = get_article(article_id)
    article["status"] = ArticleStatus.approved
    article["updated_at"] = now()
    emit("approval.approved", article_id)
    return article


@app.post("/articles/{article_id}/archive")
def archive(article_id: str) -> dict[str, Any]:
    article = get_article(article_id)
    article["status"] = ArticleStatus.archived
    article["updated_at"] = now()
    emit("content.archived", article_id)
    return article


@app.post("/workflows/start")
def start_workflow(payload: WorkflowRequest) -> dict[str, Any]:
    get_article(payload.article_id)
    workflow_id = f"workflow_{uuid4().hex[:12]}"
    workflow = {"id": workflow_id, "article_id": payload.article_id, "workflow": payload.workflow, "status": "started", "created_at": now()}
    WORKFLOWS[workflow_id] = workflow
    emit("workflow.started", payload.article_id, workflow)
    return workflow


@app.post("/workflows/{workflow_id}/complete")
def complete_workflow(workflow_id: str) -> dict[str, Any]:
    workflow = WORKFLOWS.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="workflow not found")
    workflow["status"] = "completed"
    workflow["completed_at"] = now()
    emit("workflow.completed", workflow["article_id"], workflow)
    return workflow


@app.post("/publish")
def publish(payload: PublishRequest) -> dict[str, Any]:
    article = get_article(payload.article_id)
    if article["status"] not in [ArticleStatus.approved, ArticleStatus.published]:
        raise HTTPException(status_code=409, detail="article must be approved before publishing")
    results = []
    original_status = article["status"]
    if not payload.dry_run:
        article["status"] = ArticleStatus.publishing
    emit("publication.started", payload.article_id, {"channels": payload.channels, "dry_run": payload.dry_run})
    for channel in payload.channels:
        publication_id = f"publication_{uuid4().hex[:12]}"
        result = {"id": publication_id, "article_id": payload.article_id, "channel": channel, "status": "dry_run" if payload.dry_run else "published", "url": f"https://example.com/{channel}/{article['slug']}", "created_at": now()}
        PUBLICATIONS[publication_id] = result
        results.append(result)
    article["status"] = original_status if payload.dry_run else ArticleStatus.published
    article["updated_at"] = now()
    emit("publication.completed", payload.article_id, {"results": results, "dry_run": payload.dry_run})
    return {"article_id": payload.article_id, "results": results, "dry_run": payload.dry_run, "article_status": article["status"]}


@app.get("/publications")
def publications(article_id: str | None = None) -> list[dict[str, Any]]:
    items = list(PUBLICATIONS.values())
    if article_id:
        items = [p for p in items if p["article_id"] == article_id]
    return items


@app.get("/events")
def events(subject_id: str | None = None) -> list[dict[str, Any]]:
    if subject_id:
        return [e for e in EVENTS if e["subject_id"] == subject_id]
    return EVENTS[-100:]


@app.get("/connectors/health")
def connector_health() -> dict[str, Any]:
    return {"wordpress": {"status": "configured_required_for_live_publish"}, "rss": {"status": "ready"}, "github_pages": {"status": "configured_required_for_live_publish"}}
