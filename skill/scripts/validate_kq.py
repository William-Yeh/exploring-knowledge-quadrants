#!/usr/bin/env python3
"""Structural validator for knowledge-quadrant (KQ) output files.

Usage:
    python3 validate_kq.py <file.md> [--level basic|full]

basic  — title, metadata line, four quadrant headers, >=3 bullets each.
full   — basic plus mode-specific checks: probe tags (shallow), personas
         line and bullet attribution (deep), Migration Log (refresh).

Exit code 0 when every check passes, 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Base emoji codepoints (without the U+FE0F variation selector) so matching
# works whether or not the file's emoji carry the selector.
QUADRANTS = [
    ("\U0001F441", "Known Knowns — Conscious Knowledge"),
    ("\U0001F50D", "Known Unknowns — Identified Gaps"),
    ("\U0001F32B", "Unknown Knowns — Tacit Knowledge"),
    ("\U0001F311", "Unknown Unknowns — Hidden Risks & Blind Spots"),
]
UU_TITLE = QUADRANTS[3][1]
META_RE = re.compile(
    r"^_\d{4}-\d{2}-\d{2} · depth: (shallow|deep) · web: (on|off)(.*)_$"
)
PROBE_TAG_RE = re.compile(r"\(probe: ([^)]+)\)")
ATTRIBUTION_RE = re.compile(r"\([^()]+\)\s*$")


def find_sections(lines: list[str]) -> dict[str, list[str]]:
    """Map each H2 header line to the lines that follow it (until next H2)."""
    sections: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line.strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the structure of a KQ output file."
    )
    parser.add_argument("file", type=Path)
    parser.add_argument("--level", choices=["basic", "full"], default="basic")
    args = parser.parse_args(argv)

    failures: list[str] = []

    def check(name: str, ok: bool, reason: str = "") -> None:
        if ok:
            print(f"PASS: {name}")
        else:
            print(f"FAIL: {name}" + (f" — {reason}" if reason else ""))
            failures.append(name)

    text = args.file.read_text(encoding="utf-8")
    lines = text.splitlines()

    check(
        "H1 title",
        bool(lines) and lines[0].startswith("# Knowledge Quadrants:"),
        "first line must start with '# Knowledge Quadrants:'",
    )

    meta = None
    for line in lines[:5]:
        m = META_RE.match(line.strip())
        if m:
            meta = m
            break
    check(
        "metadata line",
        meta is not None,
        "expected '_YYYY-MM-DD · depth: shallow|deep · web: on|off…_' "
        "within the first 5 lines",
    )

    sections = find_sections(lines)
    quadrant_bodies: dict[str, list[str]] = {}
    for emoji, title in QUADRANTS:
        matches = [h for h in sections if emoji in h and title in h]
        check(
            f"quadrant header: {title}",
            len(matches) == 1,
            f"found {len(matches)} matching H2 headers, expected exactly 1",
        )
        if len(matches) == 1:
            quadrant_bodies[title] = sections[matches[0]]

    for title, body in quadrant_bodies.items():
        bullets = [l for l in body if l.startswith("- ")]
        check(f">=3 bullets: {title}", len(bullets) >= 3, f"found {len(bullets)}")

    if args.level == "full" and meta is not None:
        depth = meta.group(1)
        uu = quadrant_bodies.get(UU_TITLE, [])
        uu_bullets = [l for l in uu if l.startswith("- ")]
        if depth == "shallow":
            tags = {
                m.group(1).strip()
                for l in uu
                for m in PROBE_TAG_RE.finditer(l)
            }
            check(
                "shallow: >=3 distinct probe tags in UU",
                len(tags) >= 3,
                f"found {len(tags)}: {sorted(tags)}",
            )
        else:
            check(
                "deep: personas line in UU",
                any(l.strip().startswith("_Personas consulted:") for l in uu),
                "expected a line starting with '_Personas consulted:'",
            )
            attributed = [l for l in uu_bullets if ATTRIBUTION_RE.search(l)]
            check(
                "deep: >=3 attributed UU bullets",
                len(attributed) >= 3,
                f"found {len(attributed)}",
            )
        if "refreshed from" in (meta.group(3) or ""):
            check(
                "refresh: migration log section",
                any("\U0001F501" in h and "Migration Log" in h for h in sections),
                "expected a '## 🔁 Migration Log' section",
            )

    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nAll checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
