#!/usr/bin/env python3
"""Dependency-free project validator. Pair with official Agent Skills validation in CI."""
from pathlib import Path
import json
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
        version = re.search(r'(?m)^\s*version:\s*"?([^"\n]+)"?$', fm)
        if not name:
            errors.append("frontmatter name is required")
        else:
            n = name.group(1).strip().strip('"')
            if len(n) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n):
                errors.append("name must be <=64 chars and lowercase hyphenated")
            if ROOT.name != n:
                errors.append(f"skill name '{n}' must match parent directory '{ROOT.name}'")
        if not desc or not desc.group(1).strip():
            errors.append("frontmatter description is required")
        elif len(desc.group(1).strip()) > 1200:
            errors.append("description appears excessively long")
        if not version:
            errors.append("metadata version is required")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds recommended 500 lines")

required = [
    "references/daily-use.md",
    "references/visual-first.md",
    "references/canonical-model.md",
    "references/build-layer.md",
    "references/process.md",
    "references/domain-neutral-systems.md",
    "references/diagramming.md",
    "references/teaching-mode.md",
    "references/adaptive-systems.md",
    "references/discovery.md",
    "references/data-systems.md",
    "references/reliability.md",
    "references/architecture-fitness.md",
    "references/ai-systems.md",
    "references/security.md",
    "references/review-matrix.md",
    "references/sources.md",
    "model/system.schema.json",
    "model/system.example.json",
    "scripts/render_system.py",
    "scripts/validate_model.py",
    "templates/SYSTEM_VIEW_PACK.md",
    "templates/ADR.md",
    "templates/DESIGN.md",
    "templates/ARCHITECTURE_REVIEW.md",
    "templates/SYSTEM_HEALTH.md",
    "templates/ADAPTIVE_OPERATING_LOOP.md",
    "templates/THREAT_MODEL.md",
    "templates/FITNESS_CHECKS.md",
    "evals/evals.json",
    "evals/visual-daily-evals.json",
    "LICENSE",
    "SECURITY.md",
    "CHANGELOG.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing required repository file: {rel}")


def validate_eval_file(path: Path, minimum: int) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("skill_name") != "system-design-architect":
            errors.append(f"{path.name}: skill_name mismatch")
        scenarios = data.get("evals", [])
        if len(scenarios) < minimum:
            errors.append(f"{path.name}: expected at least {minimum} eval scenarios")
        ids = [item.get("id") for item in scenarios]
        if len(ids) != len(set(ids)):
            errors.append(f"{path.name}: eval scenario IDs must be unique")
        for item in scenarios:
            if not item.get("prompt") or not item.get("expected_output"):
                errors.append(f"{path.name}: eval {item.get('id')} missing prompt or expected_output")
            if len(item.get("assertions", [])) < 2:
                errors.append(f"{path.name}: eval {item.get('id')} should have at least 2 assertions")
    except Exception as exc:
        errors.append(f"invalid {path}: {exc}")


validate_eval_file(ROOT / "evals/evals.json", 10)
validate_eval_file(ROOT / "evals/visual-daily-evals.json", 4)

for json_path in [ROOT / "model/system.schema.json", ROOT / "model/system.example.json"]:
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if json_path.name == "system.example.json" and len(data.get("process_steps", [])) < 5:
            errors.append("system.example.json should demonstrate at least 5 granular process steps")
    except Exception as exc:
        errors.append(f"invalid JSON {json_path}: {exc}")

lic = (ROOT / "LICENSE").read_text(errors="ignore") if (ROOT / "LICENSE").exists() else ""
for marker in ["1. Definitions.", "2. Grant of Copyright License.", "9. Accepting Warranty or Additional Liability.", "END OF TERMS AND CONDITIONS"]:
    if marker not in lic:
        errors.append(f"LICENSE appears incomplete: missing {marker}")

if SKILL.exists():
    body = SKILL.read_text(encoding="utf-8")
    for phrase in [
        "domain-neutral",
        "Visual first",
        "End to end",
        "buildable granularity",
        "Granular build-step contract",
        "BUILD READY",
        "process_steps",
        "AS-IS",
        "TARGET",
        "Verification",
        "Validation",
        "self-healing",
        "adaptation envelope",
        "Mode D",
        "references/build-layer.md",
    ]:
        if phrase.lower() not in body.lower():
            errors.append(f"SKILL.md missing core concept: {phrase}")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)
print("Project validation passed.")
