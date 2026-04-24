## Keeping up with upstream

The build **fails** if upstream changes `manager.py` — you will see a `diff` output in the CI logs. To update:

1. Copy the new upstream file to `manager.py.orig`
2. Re-apply the additions to `manager.py`
3. Push


## Building locally

```bash
docker build \
  --build-arg BASE_IMAGE=ghcr.io/docling-project/docling-serve:latest \
  -f Containerfile \
  -t docling-serve-hierarchical:local \
  .
```

## Automated builds

A GitHub Actions workflow (`.github/workflows/build.yml`) rebuilds all four variants every Monday at 06:00 UTC and on manual dispatch. To trigger a build against a specific upstream tag:

```
Actions → Build hierarchical docling-serve images → Run workflow → upstream_tag: 1.16.1
```
