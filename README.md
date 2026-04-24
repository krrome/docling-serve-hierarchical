# docling-serve-hierarchical

Downstream images that extend the official [docling-serve](https://github.com/docling-project/docling-serve) images with automatic PDF header-hierarchy inference via [docling-hierarchical-pdf](https://github.com/krrome/docling-hierarchical-pdf).

## What's different

Every conversion result produced by docling is post-processed by `ResultPostprocessor` before it is exported. This restructures section headings in the `DoclingDocument` to reflect the true heading hierarchy inferred from the PDF's table of contents or font metrics.

The only files modified relative to upstream are:

| File | Change |
|------|--------|
| `docling_serve/convert/manager.py` | Patches the result with docling-hierarchical-pdf ResultPostprocessor |

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
