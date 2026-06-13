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

| Image | Based on | Models pre-installed |
|-------|----------|----------------------|
| `docling-serve-hierarchical` | `docling-project/docling-serve` | No |
| `docling-serve-hierarchical-cpu` | `docling-project/docling-serve-cpu` | No |
| `docling-serve-hierarchical-cu128` | `docling-project/docling-serve-cu128` | No |
| `docling-serve-hierarchical-cu130` | `docling-project/docling-serve-cu130` | No |
| `docling-serve-hierarchical-models` | `docling-project/docling-serve` | Yes |
| `docling-serve-hierarchical-cpu-models` | `docling-project/docling-serve-cpu` | Yes |
| `docling-serve-hierarchical-cu128-models` | `docling-project/docling-serve-cu128` | Yes |
| `docling-serve-hierarchical-cu130-models` | `docling-project/docling-serve-cu130` | Yes |

Tags mirror the upstream commit SHA (`sha-<hash>`) used at build time. The default/cpu variants are also tagged `latest`.

## Licenses

The software in these images is MIT-licensed ([docling-serve](https://github.com/docling-project/docling-serve/blob/main/LICENSE), [docling](https://github.com/docling-project/docling/blob/main/LICENSE)) and Apache 2.0-licensed (EasyOCR). The base layer is Red Hat UBI, which [explicitly permits redistribution](https://www.redhat.com/licenses/EULA_Red_Hat_Universal_Base_Image_English_20190422.pdf).

The `-models` images additionally contain model weights from [`ds4sd/docling-models`](https://huggingface.co/ds4sd/docling-models) (layout analysis and TableFormer), which are released under [CDLA Permissive 2.0](https://cdla.dev/permissive-2-0/) and [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Both licenses permit redistribution; if you redistribute a `-models` image you must pass these license terms on to your recipients.
