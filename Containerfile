ARG BASE_IMAGE=ghcr.io/docling-project/docling-serve:latest

FROM ${BASE_IMAGE}

USER 0

# Fail the build if the upstream rq_job_wrapper.py has changed since the patch was written.
# To update: copy the new upstream file to rq_job_wrapper.py.orig and re-apply the patch.
COPY rq_job_wrapper.py.orig /tmp/rq_job_wrapper.py.orig
RUN SITE_PACKAGES=$(/opt/app-root/bin/python -c "import site; print(site.getsitepackages()[0])") && \
    UPSTREAM="$SITE_PACKAGES/docling_serve/rq_job_wrapper.py" && \
    if ! cmp -s /tmp/rq_job_wrapper.py.orig "$UPSTREAM"; then \
        echo "ERROR: upstream rq_job_wrapper.py has changed — update rq_job_wrapper.py.orig and re-apply the patch." >&2; \
        diff /tmp/rq_job_wrapper.py.orig "$UPSTREAM" >&2 || true; \
        exit 1; \
    fi

# Install docling-hierarchical-pdf into the existing uv environment
RUN /opt/app-root/bin/pip install --quiet \
    git+https://github.com/krrome/docling-hierarchical-pdf.git

# Overwrite with patched rq_job_wrapper.py
COPY rq_job_wrapper.py /tmp/rq_job_wrapper.py
RUN SITE_PACKAGES=$(/opt/app-root/bin/python -c "import site; print(site.getsitepackages()[0])") && \
    cp /tmp/rq_job_wrapper.py "$SITE_PACKAGES/docling_serve/rq_job_wrapper.py"

USER 1001
