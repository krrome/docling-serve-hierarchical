"""Smoke test for docling-serve-hierarchical.

Usage: python tests/smoke.py <base_url> <pdf_path>
  base_url  e.g. http://localhost:5001
  pdf_path  path to a PDF with headings, e.g. tests/sample.pdf

Exits 0 if all tests pass, non-zero on first failure.
"""

import base64
import json
import sys
import urllib.request
from pathlib import Path

OPTS = {"to_formats": ["md"], "ocr": False}
EXPECTED_MD = (Path(__file__).parent / "sample.md").read_text()


def _check(label: str, body: dict) -> None:
    assert body["status"] == "success", (
        f"[{label}] status={body['status']} errors={body.get('errors')}"
    )
    md = (body.get("document") or {}).get("md_content") or ""
    import pdb
    pdb.set_trace()
    assert md.strip() == EXPECTED_MD.strip(), (
        f"[{label}] markdown output does not match tests/sample.md"
    )
    print(f"[{label}] PASS  (processing_time={body['processing_time']:.1f}s)")


def _post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def test_file_upload(base_url: str, pdf_path: Path) -> None:
    boundary = "----SmokeBoundary"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files"; filename="{pdf_path.name}"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode() + pdf_path.read_bytes() + (
        f"\r\n--{boundary}--\r\n"
    ).encode()

    req = urllib.request.Request(
        f"{base_url}/v1/convert/file",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    _check("file_upload", result)


def test_http_source(base_url: str, raw_url: str) -> None:
    payload = {
        "sources": [{"kind": "http", "url": raw_url}],
        "options": OPTS,
    }
    result = _post_json(f"{base_url}/v1/convert/source", payload)
    _check("http_source", result)


def test_base64_source(base_url: str, pdf_path: Path) -> None:
    b64 = base64.b64encode(pdf_path.read_bytes()).decode()
    payload = {
        "sources": [{"kind": "file", "base64_string": b64, "filename": pdf_path.name}],
        "options": OPTS,
    }
    result = _post_json(f"{base_url}/v1/convert/source", payload)
    _check("base64_source", result)


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <base_url> <pdf_path>", file=sys.stderr)
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    pdf_path = Path(sys.argv[2])

    raw_url = (
        "https://raw.githubusercontent.com/krrome/docling-serve-hierarchical"
        "/main/tests/sample.pdf"
    )

    test_file_upload(base_url, pdf_path)
    test_http_source(base_url, raw_url)
    test_base64_source(base_url, pdf_path)

    print("All smoke tests passed.")


if __name__ == "__main__":
    main()
