#!/usr/bin/env python3
"""Split docs/Spartan_Strategy_Partner_Guide.md into the skill's references/ files.

Usage (from the repo root):   python scripts/split_guide.py

The guide is the single source of truth. Never edit the generated files in
skills/spartan-strategy-partner/references/ by hand (except references/api/,
which is maintained manually).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "docs" / "Spartan_Strategy_Partner_Guide.md"
OUT = ROOT / "references"

# output file -> (title, [section keys])   "overview" = the "Spartan in 60 Seconds" block
FILES = [
    ("overview.md", "Overview: the model, wallets and account types", ["overview", 1, 2, 3]),
    ("setup-and-bot-console.md", "Setup, Bot Console and bot lifecycle", [4, 11]),
    ("deposits-and-redemptions.md", "Wallets, deposits and redemptions", [5]),
    ("manual-trading.md", "For manual traders", [6]),
    ("api-and-bot-design.md", "For API traders and bot builders", [7]),
    ("profit-share-and-tiers.md", "Profit sharing, earnings and tiers", [8, 9]),
    ("risk-and-pairs.md", "Risk, pairs and execution", [10]),
    ("scenarios.md", "Worked scenarios", [12]),
    ("troubleshooting-and-faq.md", "Troubleshooting and FAQ", [13, 14]),
    ("changelog-and-glossary.md", "Change timeline, glossary and translation notes", [15, 16]),
]


def parse_sections(text):
    sections, key, buf, fence = {}, None, [], False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^## (\d+)\. ", line)
        is_60 = (not fence) and line.strip() == "## Spartan in 60 Seconds"
        if m or is_60:
            if key is not None:
                sections[key] = "\n".join(buf).strip("\n")
            key = int(m.group(1)) if m else "overview"
            buf = [line]
        elif key is not None:
            buf.append(line)
    if key is not None:
        sections[key] = "\n".join(buf).strip("\n")
    return sections


def main():
    text = GUIDE.read_text(encoding="utf-8")
    sections = parse_sections(text)
    covered = {k for _, _, keys in FILES for k in keys}
    missing = set(sections) - covered
    unknown = covered - set(sections)
    if missing or unknown:
        sys.exit(f"Section mismatch. Not mapped: {missing}. Mapped but not found: {unknown}")

    file_of = {k: name for name, _, keys in FILES for k in keys}
    OUT.mkdir(parents=True, exist_ok=True)

    for name, title, keys in FILES:
        body = []
        for k in keys:
            body.append(sections[k])
        content = "\n\n---\n\n".join(body)

        def repl(m):
            n = int(m.group(1))
            target = file_of.get(n)
            if target and target != name:
                return f"Section {n}{m.group(2)} of `{target}`"
            return m.group(0)

        content = re.sub(r"Section (\d+)((?:\.\d+)?)", repl, content)
        toc = [ln[3:].strip() for ln in content.split("\n") if ln.startswith("## ")]
        header = (
            f"# {title}\n\n"
            f"> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. "
            f"Edit the guide, not this file.\n\n"
            f"Contents: " + " | ".join(toc) + "\n\n---\n\n"
        )
        (OUT / name).write_text(header + content + "\n", encoding="utf-8")
        print(f"wrote {name}  ({len(content.splitlines())} lines)")


if __name__ == "__main__":
    main()
