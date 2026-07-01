from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
BODY = " ".join(["authorization"] * 70)


def test_content_lifecycle_dry_run_publish():
    created = client.post("/articles", json={"title": "Apache Casbin Platform", "body": BODY, "tags": ["casbin"], "channels": ["rss"]}).json()
    article_id = created["id"]
    assert created["status"] == "draft"

    validated = client.post(f"/articles/{article_id}/validate").json()
    assert validated["status"] == "validated"

    ai = client.post("/ai/enhance", json={"article_id": article_id, "apply": True}).json()
    assert "Content Operations" in ai["tags"]

    approved = client.post(f"/articles/{article_id}/approve").json()
    assert approved["status"] == "approved"

    workflow = client.post("/workflows/start", json={"article_id": article_id}).json()
    assert workflow["status"] == "started"

    results = client.post("/publish", json={"article_id": article_id, "channels": ["rss"], "dry_run": True}).json()
    assert results["results"][0]["status"] == "dry_run"
    assert results["article_status"] == "approved"

    article = client.get(f"/articles/{article_id}").json()
    assert article["status"] == "approved"

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "agennext_articles_total" in metrics.text
