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
RUN SITE_PACKAGES=$(/opt/app-root/bin/python -c "import site; print(site.getsitepackages()[0])") && \
    /opt/app-root/bin/python /tmp/patch_rq_job_wrapper.py \
        "$SITE_PACKAGES/docling_serve/rq_job_wrapper.py"

USER 1001
