"""Patch docling_serve/rq_job_wrapper.py to add hierarchical PDF post-processing.

Usage: python patch_rq_job_wrapper.py <path-to-rq_job_wrapper.py>

A single anchor (the convert_documents tracing block) is replaced with an
extended version that prepends inline imports and a deepcopy, and appends
inline post-processing. Fails loudly if the anchor is not found exactly once
or if the result has a syntax error.
"""

import sys

ANCHOR = (
    "            # Document conversion with detailed tracing\n"
    '            with tracer.start_as_current_span("convert_documents") as conv_span:\n'
    "                conv_span.set_attribute(\"num_sources\", len(convert_sources))\n"
    "                conv_span.set_attribute(\"has_headers\", headers is not None)\n"
    "\n"
    "                conv_results = conversion_manager.convert_documents(\n"
    "                    sources=convert_sources,\n"
    "                    options=task.convert_options,\n"
    "                    headers=headers,\n"
    "                )\n"
)

REPLACEMENT = (
    "            import copy; from hierarchical.postprocessor import ResultPostprocessor\n"
    "            postprocessor_sources = copy.deepcopy(convert_sources)\n"
    "            # Document conversion with detailed tracing\n"
    '            with tracer.start_as_current_span("convert_documents") as conv_span:\n'
    "                conv_span.set_attribute(\"num_sources\", len(convert_sources))\n"
    "                conv_span.set_attribute(\"has_headers\", headers is not None)\n"
    "\n"
    "                conv_results = conversion_manager.convert_documents(\n"
    "                    sources=convert_sources,\n"
    "                    options=task.convert_options,\n"
    "                    headers=headers,\n"
    "                )\n"
    "            conv_results = (\n"
    "                r for r, s in zip(conv_results, postprocessor_sources)\n"
    "                for _ in [ResultPostprocessor(r, source=s).process()]\n"
    "            )\n"
)


def patch(filepath: str) -> None:
    with open(filepath) as f:
        content = f.read()

    count = content.count(ANCHOR)
    if count != 1:
        print(
            f"ERROR: anchor expected exactly once, found {count} times — "
            "upstream rq_job_wrapper.py may have changed; update ANCHOR in this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    content = content.replace(ANCHOR, REPLACEMENT, 1)

    try:
        compile(content, filepath, "exec")
    except SyntaxError as exc:
        print(f"ERROR: patched file has a syntax error: {exc}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Patched {filepath} successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-rq_job_wrapper.py>", file=sys.stderr)
        sys.exit(1)
    patch(sys.argv[1])
