#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://localhost:8080}"
BODY=$(python - <<'PY'
print(' '.join(['authorization'] * 70))
PY
)
ARTICLE=$(curl -fsS -X POST "$BASE/articles" -H 'content-type: application/json' -d "{\"title\":\"Apache Casbin as a Platform\",\"body\":\"$BODY\",\"tags\":[\"casbin\"],\"channels\":[\"rss\"]}")
ID=$(python - <<PY
import json
print(json.loads('''$ARTICLE''')['id'])
PY
)
curl -fsS -X POST "$BASE/articles/$ID/validate" >/dev/null
curl -fsS -X POST "$BASE/ai/enhance" -H 'content-type: application/json' -d "{\"article_id\":\"$ID\",\"apply\":true}" >/dev/null
curl -fsS -X POST "$BASE/articles/$ID/approve" >/dev/null
curl -fsS -X POST "$BASE/workflows/start" -H 'content-type: application/json' -d "{\"article_id\":\"$ID\"}" >/dev/null
curl -fsS -X POST "$BASE/publish" -H 'content-type: application/json' -d "{\"article_id\":\"$ID\",\"channels\":[\"rss\"],\"dry_run\":true}" >/dev/null
curl -fsS "$BASE/health" >/dev/null
curl -fsS "$BASE/metrics" >/dev/null
echo "smoke ok: $ID"
