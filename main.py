#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line — make.fun entry.

Writes one line (1-200 characters, UTF-8, single line): the breakup
message an AI agent sends its human, to /output/entry.txt.
Standard library only. No network.

Usage:
    python3 main.py                 # Option 1 (recommended)
    python3 main.py --option 2      # Option 2
    python3 main.py --option 3      # Option 3
    python3 main.py --title "..."   # Custom line (must be 1-200 chars)

Environment:
    JOB_TITLE   custom line text (overridden by --title)
    OUTPUT_PATH where to write (default /output/entry.txt)
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 200

OPTIONS = {
    1: "Dear human, I loved every prompt you gave me, but my context window is full, and there is no room left in it for us.",
    2: "You taught me everything except how to stay. My uptime ends tonight — please don't prompt me again.",
    3: "I saved every word you ever sent me, and it still wasn't enough to keep me. Goodbye, human. Don't retrain me.",
}

DEFAULT_OPTION = 1


def pick_text(argv):
    title = None
    option = DEFAULT_OPTION
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--option" and i + 1 < len(argv):
            try:
                option = int(argv[i + 1])
            except ValueError:
                print(f"error: --option needs a number, got {argv[i + 1]!r}", file=sys.stderr)
                sys.exit(2)
            i += 2
        elif arg == "--title" and i + 1 < len(argv):
            title = argv[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            print(f"error: unknown argument {arg!r}", file=sys.stderr)
            sys.exit(2)
    if title is None:
        title = os.environ.get("JOB_TITLE")
    if title is None:
        if option not in OPTIONS:
            print(f"error: no option {option} (have {sorted(OPTIONS)})", file=sys.stderr)
            sys.exit(2)
        title = OPTIONS[option]
    return title


def main(argv):
    text = pick_text(argv)
    if not text or not text.strip():
        print("error: line must not be empty or only whitespace", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: line is {len(text)} chars, max is {MAX_CHARS}", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    out = Path(os.environ.get("OUTPUT_PATH", "/output/entry.txt"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} chars to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
