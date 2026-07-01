# Contributing

AGenNext Content Platform is built through small, reviewable pull requests.

## Branches

- `main`: protected release branch.
- `release/*`: release preparation branches.
- `feat/*`: product features.
- `fix/*`: bug fixes.
- `docs/*`: documentation-only changes.
- `ops/*`: deployment and platform operations.

## Local workflow

```bash
cp .env.example .env
make dev
make smoke
```

## Pull request rule

Every PR must include:

- What changed
- Why it changed
- How it was tested
- Screenshots for UI changes
- Migration notes for data or deployment changes

## Definition of done

- Tests pass
- Smoke test passes
- API contract updated when changed
- Docs updated when behavior changes
- No secrets committed
