"""Patch docling_jobkit/convert/manager.py to add hierarchical PDF post-processing.

Usage: python patch_manager.py <path-to-manager.py>

A single anchor (the convert_documents tracing block) is replaced with an
extended version that prepends inline imports and a deepcopy, and appends
inline post-processing. Fails loudly if the anchor is not found exactly once
or if the result has a syntax error.
"""

import sys

ANCHOR = """results: Iterator[ConversionResult] = converter.convert_all(
            sources,
            headers=headers,
            page_range=options.page_range,
            max_file_size=self.config.max_file_size,
            max_num_pages=self.config.max_num_pages,
            raises_on_error=options.abort_on_error,
        )

        return results"""

REPLACEMENT = """import copy
        from hierarchical.postprocessor import ResultPostprocessor
        sources = list(sources)  # materialise so we can zip with results
        postprocessor_sources = copy.deepcopy(sources)
        results: Iterator[ConversionResult] = converter.convert_all(
            sources,
            headers=headers,
            page_range=options.page_range,
            max_file_size=self.config.max_file_size,
            max_num_pages=self.config.max_num_pages,
            raises_on_error=options.abort_on_error,
        )
        def _postprocess() -> Iterator[ConversionResult]:
            for r, s in zip(results, postprocessor_sources):
                ResultPostprocessor(r, source=s).process()
                yield r

        return _postprocess()"""



def patch(filepath: str) -> None:
    with open(filepath) as f:
        content = f.read()

    count = content.count(ANCHOR)
    if count != 1:
        print(
            f"ERROR: anchor expected exactly once, found {count} times — "
            "upstream manager.py may have changed; update ANCHOR in this script.",
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
        print(f"Usage: {sys.argv[0]} <path-to-manager.py>", file=sys.stderr)
        sys.exit(1)
    patch(sys.argv[1])
