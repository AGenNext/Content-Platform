# Release Process

Versioning follows `vMAJOR.MINOR.PATCH` with prerelease labels during alpha.

## Current release

`v0.1.0-alpha`

## Release checks

```bash
make test
make smoke
helm template agennext-content-platform deploy/helm
```

## Tagging

```bash
git tag v0.1.0-alpha
git push origin v0.1.0-alpha
```

## Release notes template

- Summary
- Added
- Changed
- Fixed
- Known gaps
- Upgrade notes
