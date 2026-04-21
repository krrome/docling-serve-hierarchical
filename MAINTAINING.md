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
