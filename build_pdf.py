#!/usr/bin/env python3
"""Export a PDF from this repository's public, fixed-commit TeX source.

The manuscript is first published on GitHub. This script sends only its
public raw-source URL to LaTeX.Online, using the documented compilation API.
It needs only the Python standard library and does not install a TeX runtime.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlencode
from urllib.request import urlopen

REPOSITORY = "https://github.com/JENW1N/cofinite-derivative-zeros-order-one"
RAW_BASE = "https://raw.githubusercontent.com/JENW1N/cofinite-derivative-zeros-order-one"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", help="Full 40-character public source commit")
    parser.add_argument("--output", type=Path,
                        default=Path("cofinite_derivative_zeros_order_one.pdf"))
    args = parser.parse_args()
    commit = args.source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("--source-commit must be a full 40-character hexadecimal SHA")
    source_url = f"{RAW_BASE}/{commit}/paper.tex"
    with urlopen(source_url, timeout=60) as response:
        source = response.read()
    local_source = Path(__file__).resolve().parent / "paper.tex"
    if source != local_source.read_bytes():
        raise RuntimeError("Public source differs from the local manuscript; no export made")
    endpoint = "https://latexonline.cc/compile?" + urlencode({
        "url": source_url,
        "command": "pdflatex",
        "download": args.output.name,
    })
    with urlopen(endpoint, timeout=240) as response:
        pdf = response.read()
    if not pdf.startswith(b"%PDF-"):
        raise RuntimeError("Compilation did not return a PDF")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pdf)
    record = {
        "repository": REPOSITORY,
        "source_commit": commit,
        "source_path": "paper.tex",
        "source_url": source_url,
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "pdf_name": args.output.name,
        "pdf_sha256": hashlib.sha256(pdf).hexdigest(),
        "compiler_service": "https://latexonline.cc/compile",
        "compiler_command": "pdflatex",
        "exported_at_utc": datetime.now(timezone.utc).isoformat(),
        "limitations": "Compilation and matching hashes check the artifact, not the mathematics.",
    }
    record_path = args.output.with_suffix(".build.json")
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
