ARG BASE_IMAGE=ghcr.io/docling-project/docling-serve:latest

FROM ${BASE_IMAGE}

USER 0

# Install docling-hierarchical-pdf into the existing uv environment
RUN /opt/app-root/bin/pip install --quiet \
    git+https://github.com/krrome/docling-hierarchical-pdf.git

# Patch rq_job_wrapper.py to add hierarchical post-processing.
# The script searches for unique anchor strings; it fails loudly if any anchor
# is missing (e.g. after an upstream restructure) and validates syntax before writing.
COPY patch_rq_job_wrapper.py /tmp/patch_rq_job_wrapper.py
RUN DOCLING_SERVE_PATH=$(/opt/app-root/bin/python -c "import docling_serve; print(docling_serve.__path__[0])") && \
    /opt/app-root/bin/python /tmp/patch_rq_job_wrapper.py \
        "$DOCLING_SERVE_PATH/rq_job_wrapper.py"

USER 1001
