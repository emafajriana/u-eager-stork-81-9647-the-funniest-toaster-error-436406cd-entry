#!/usr/bin/env python3
"""Entry for make.fun: 'The Funniest Toaster Error Message'.

Writes one line (the toaster's error message) to the output entry file.
Stdlib only, deterministic.
"""

import os
import sys

LINE = (
    "E-09: LEVER PRESSED 14 TIMES. "
    "TOAST COOKS AT THE SPEED OF PHYSICS, NOT OF HUNGER."
)

MAX_CHARS = 120


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify(path: str) -> None:
    """Read the written file back and check it against the kit gate:
    UTF-8 text, 1..MAX_CHARS characters, not only whitespace, one line.
    """
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")  # raises if not valid UTF-8
    if text != LINE:
        raise SystemExit(f"gate: file content drifted from LINE: {text!r}")
    if not (1 <= len(text) <= MAX_CHARS):
        raise SystemExit(f"gate: length {len(text)} outside 1..{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("gate: entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("gate: entry must be a single line")


def main() -> int:
    path = output_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(LINE)
    verify(path)
    print(f"wrote {path} ({len(LINE)} chars)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
