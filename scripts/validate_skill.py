#!/usr/bin/env python3
"""Dependency-free sanity validator for this Agent Skill repository."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
errors = []

if not SKILL.exists():
    errors.append("SKILL.md is missing")
else:
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter is not closed")
    else:
        fm = parts[1]
        name = re.search(r"(?m)^name:\s*(.+)$", fm)
        desc = re.search(r"(?m)^description:\s*(.+)$", fm)
        if not name:
            errors.append("frontmatter name is required")
        else:
            n = name.group(1).strip()
            if len(n) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n):
                errors.append("name must be <=64 chars and lowercase hyphenated")
        if not desc or not desc.group(1).strip():
            errors.append("frontmatter description is required")
        elif len(desc.group(1).strip()) > 1024:
            errors.append("description must be <=1024 chars")

required = [
    "references/process.md",
    "references/ai-systems.md",
    "references/security.md",
    "references/review-matrix.md",
    "templates/ADR.md",
    "templates/DESIGN.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing required repository file: {rel}")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)
print("Skill sanity validation passed.")
