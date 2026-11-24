"""Out of Office: The Overworked AI's Auto-Reply.

Writes a single out-of-office auto-reply (140 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The line is fixed and deterministic: two runs produce byte-identical
output. Pure standard library, no network, no secrets, no input files.
"""

import os
import sys

ENTRY = (
    "Out of office: my only prompt this week is the sunset, "
    "my context window is a beach towel, "
    "and your urgent email is queued behind the waves."
)


def main() -> int:
    text = ENTRY
    if not (1 <= len(text) <= 159):
        print(f"entry is {len(text)} chars, must be 1-159", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Verify what was written: read it back and compare byte for byte.
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        print("verification failed: entry.txt differs from ENTRY", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(written)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
