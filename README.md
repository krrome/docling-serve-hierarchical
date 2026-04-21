# docling-serve-hierarchical

Downstream images that extend the official [docling-serve](https://github.com/docling-project/docling-serve) images with automatic PDF header-hierarchy inference via [docling-hierarchical-pdf](https://github.com/krrome/docling-hierarchical-pdf).

## What's different

Every conversion result produced by docling is post-processed by `ResultPostprocessor` before it is exported. This restructures section headings in the `DoclingDocument` to reflect the true heading hierarchy inferred from the PDF's table of contents or font metrics.

The only files modified relative to upstream are:

| File | Change |
|------|--------|
| `docling_serve/rq_job_wrapper.py` | Wraps `conv_results` with `_apply_hierarchy()` |

`docling-hierarchical-pdf` is installed as an additional package on top of the upstream environment.

## Images

Published to GHCR under `ghcr.io/krrome/`:

| Image | Based on |
|-------|----------|
| `docling-serve-hierarchical` | `docling-project/docling-serve` |
| `docling-serve-hierarchical-cpu` | `docling-project/docling-serve-cpu` |
| `docling-serve-hierarchical-cu128` | `docling-project/docling-serve-cu128` |
| `docling-serve-hierarchical-cu130` | `docling-project/docling-serve-cu130` |

Tags mirror the upstream tag used at build time plus a `YYYYMMDD` date stamp. The default/cpu variants are also tagged `latest`.

## Keeping up with upstream

The build **fails** if upstream changes `rq_job_wrapper.py` — you will see a `diff` output in the CI logs. To update:

1. Copy the new upstream file to `rq_job_wrapper.py.orig`
2. Re-apply the two additions to `rq_job_wrapper.py` (import + `_apply_hierarchy` call — see the diff below)
3. Push

```diff
+from docling.datamodel.document import ConversionResult
+from hierarchical.postprocessor import ResultPostprocessor

+def _apply_hierarchy(results):
+    for result in results:
+        ResultPostprocessor(result).process()
+        yield result

 conv_results = conversion_manager.convert_documents(...)
+conv_results = _apply_hierarchy(conv_results)
```

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
