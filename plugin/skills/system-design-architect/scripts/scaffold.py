#!/usr/bin/env python3
"""Create a systems-design, review, or health dossier from bundled templates."""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "design": ROOT / "templates" / "DESIGN.md",
    "review": ROOT / "templates" / "ARCHITECTURE_REVIEW.md",
    "health": ROOT / "templates" / "SYSTEM_HEALTH.md",
    "adaptive": ROOT / "templates" / "ADAPTIVE_OPERATING_LOOP.md",
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "system"


def main() -> None:
    p = argparse.ArgumentParser(description="Scaffold a System Design Architect dossier")
    p.add_argument("name", help="System/process/product/service name")
    p.add_argument(
        "--mode",
        choices=sorted(TEMPLATES),
        default="design",
        help="Artifact to create: design, review, health, or adaptive (default: design)",
    )
    p.add_argument("--out", default=".", help="Output directory")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = {
        "design": "system-design",
        "review": "system-review",
        "health": "system-health",
        "adaptive": "adaptive-loop",
    }[args.mode]
    target = out_dir / f"{slugify(args.name)}-{suffix}.md"
    text = TEMPLATES[args.mode].read_text(encoding="utf-8")
    text = text.replace("<Name>", args.name).replace("<System>", args.name)
    target.write_text(text, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
