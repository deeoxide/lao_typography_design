#!/usr/bin/env python3
"""Claude Code PostToolUse hook: check Lao text right after Claude writes or edits a file.

Runs after Write, Edit and MultiEdit. If the file is a text format and contains Lao, it runs
skills/lao-typography-design/scripts/lao_check.py and, only when there are High findings
(Thai letters inside Lao words, detached vowel signs or tone marks, prefixed vowels typed in
reading order, doubled marks, damaged characters), hands them back to Claude as context so it
can fix them in the same turn.

It never blocks and never fails the tool call: any error, a missing file, or a file without Lao
exits quietly. Standard library only.
"""
import json
import os
import sys

TEXT_EXT = {".txt", ".md", ".markdown", ".html", ".htm", ".css", ".svg", ".xml", ".json", ".csv", ".tsv",
            ".srt", ".vtt", ".yml", ".yaml"}
MAX_BYTES = 2_000_000
MAX_LINES = 8


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not path:
        return 0
    if not os.path.isabs(path):
        path = os.path.join(data.get("cwd") or os.getcwd(), path)
    if os.path.splitext(path)[1].lower() not in TEXT_EXT or not os.path.isfile(path):
        return 0
    if os.path.getsize(path) > MAX_BYTES:
        return 0
    with open(path, "rb") as f:
        raw = f.read()
    # UTF-8 Lao (U+0E80-U+0EFF) always starts with E0 BA or E0 BB: skip files without it, fast
    if b"\xe0\xba" not in raw and b"\xe0\xbb" not in raw:
        return 0

    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "..", "skills", "lao-typography-design", "scripts"))
    import lao_check  # noqa: E402

    rep = lao_check.run(path, None)
    if rep is None:
        return 0
    high = [f for f in rep.findings if f["severity"] == "High"]
    if not high:
        return 0

    lines = []
    for f in high[:MAX_LINES]:
        ctx = (" [%s]" % f["context"]) if f.get("context") else ""
        lines.append("- %s %s: %s%s" % (f["code"], f["where"], f["message"], ctx))
    if len(high) > MAX_LINES:
        lines.append("- ... and %d more" % (len(high) - MAX_LINES))
    msg = ("Lao check found %d High problem(s) in %s:\n%s\n"
           "Fix them in the file, or tell the user why they are intended (for example a vowel chart or a quoted "
           "Thai word). Run lao_check.py from the lao-typography-design skill for the full report."
           % (len(high), os.path.basename(path), "\n".join(lines)))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
