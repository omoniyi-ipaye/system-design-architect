#!/usr/bin/env python3
"""Create a system-design dossier from the bundled template."""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "DESIGN.md"

def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "system"

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("name", help="System/product name")
    p.add_argument("--out", default=".", help="Output directory")
    args = p.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{slugify(args.name)}-design.md"
    text = TEMPLATE.read_text(encoding="utf-8").replace("<Name>", args.name)
    target.write_text(text, encoding="utf-8")
    print(target)

if __name__ == "__main__":
    main()
