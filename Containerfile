ARG BASE_IMAGE=ghcr.io/docling-project/docling-serve:latest

FROM ${BASE_IMAGE}

ARG BAKE_MODELS=0

USER 0

# Install docling-hierarchical-pdf into the existing uv environment
RUN /opt/app-root/bin/pip install --quiet \
    git+https://github.com/krrome/docling-hierarchical-pdf.git

# Patch manager.py to add hierarchical post-processing.
# The script searches for unique anchor strings; it fails loudly if any anchor
# is missing (e.g. after an upstream restructure) and validates syntax before writing.
COPY patch_manager.py /tmp/patch_manager.py
RUN DOCLING_JOBKIT_CONVERT_PATH=$(/opt/app-root/bin/python -c "import docling_jobkit.convert; print(docling_jobkit.convert.__path__[0])") && \
    /opt/app-root/bin/python /tmp/patch_manager.py \
        "$DOCLING_JOBKIT_CONVERT_PATH/manager.py"

USER 1001

# Pre-download docling's default models so the image is ready to use immediately.
# Skipped in the base variant (BAKE_MODELS=0).
RUN if [ "${BAKE_MODELS}" = "1" ]; then \
    /opt/app-root/bin/python -c \
      "from docling.document_converter import DocumentConverter; DocumentConverter()"; \
fi
