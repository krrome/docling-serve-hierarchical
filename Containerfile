ARG BASE_IMAGE=ghcr.io/docling-project/docling-serve:latest

FROM ${BASE_IMAGE}

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
