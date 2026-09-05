#!/usr/bin/env python3
"""Dependency-free project validator. Pair with official Agent Skills validation in CI."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
errors=[]

if not SKILL.exists():
    errors.append("SKILL.md is missing")
else:
    text=SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    parts=text.split("---",2)
    if len(parts)<3:
        errors.append("SKILL.md frontmatter is not closed")
    else:
        fm=parts[1]
        name=re.search(r"(?m)^name:\s*(.+)$",fm)
        desc=re.search(r"(?m)^description:\s*(.+)$",fm)
        if not name:
            errors.append("frontmatter name is required")
        else:
            n=name.group(1).strip()
            if len(n)>64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",n):
                errors.append("name must be <=64 chars and lowercase hyphenated")
            if ROOT.name != n:
                errors.append(f"skill name '{n}' must match parent directory '{ROOT.name}'")
        if not desc or not desc.group(1).strip():
            errors.append("frontmatter description is required")
        elif len(desc.group(1).strip())>1024:
            errors.append("description must be <=1024 chars")
    if len(text.splitlines())>500:
        errors.append("SKILL.md exceeds recommended 500 lines")

required=[
 "references/process.md","references/discovery.md","references/data-systems.md",
 "references/reliability.md","references/architecture-fitness.md","references/ai-systems.md",
 "references/security.md","references/review-matrix.md","references/sources.md",
 "templates/ADR.md","templates/DESIGN.md","templates/ARCHITECTURE_REVIEW.md",
 "templates/THREAT_MODEL.md","templates/FITNESS_CHECKS.md","evals/evals.json",
 "LICENSE","SECURITY.md","CHANGELOG.md"
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f"missing required repository file: {rel}")

try:
    ev=json.loads((ROOT/'evals/evals.json').read_text())
    if ev.get('skill_name')!='system-design-architect': errors.append('eval skill_name mismatch')
    if len(ev.get('evals',[]))<4: errors.append('expected at least 4 eval scenarios')
except Exception as e:
    errors.append(f"invalid evals/evals.json: {e}")

lic=(ROOT/'LICENSE').read_text(errors='ignore') if (ROOT/'LICENSE').exists() else ''
for marker in ['1. Definitions.','2. Grant of Copyright License.','9. Accepting Warranty or Additional Liability.','END OF TERMS AND CONDITIONS']:
    if marker not in lic: errors.append(f"LICENSE appears incomplete: missing {marker}")

if errors:
    for e in errors: print(f"ERROR: {e}")
    sys.exit(1)
print("Project validation passed.")
