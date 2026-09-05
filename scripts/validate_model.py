#!/usr/bin/env python3
"""Dependency-free structural validator for canonical System Design Architect models."""
from pathlib import Path
import argparse
import json

VIEW_STAGES = {"as_is", "transition", "target"}
ELEMENT_STAGES = VIEW_STAGES | {"shared"}
EVIDENCE = {"observed", "assumed", "proposed", "unknown"}
FLOW_TYPES = {"work", "information", "authority", "state", "money", "material", "resource", "feedback", "dependency"}
LEVELS = {"L0", "L1", "L2", "L3"}


def validate(model: dict) -> list[str]:
    errors = []
    for key in ("schema_version", "system", "elements", "flows"):
        if key not in model:
            errors.append(f"missing required top-level key: {key}")

    system = model.get("system", {})
    for key in ("id", "name", "purpose", "stage"):
        if not system.get(key):
            errors.append(f"system.{key} is required")
    if system.get("stage") not in VIEW_STAGES | {"mixed"}:
        errors.append(f"invalid system.stage: {system.get('stage')}")

    elements = model.get("elements", [])
    ids = []
    element_by_id = {}
    for i, e in enumerate(elements):
        eid = e.get("id")
        if not eid:
            errors.append(f"elements[{i}].id is required")
            continue
        ids.append(eid)
        element_by_id[eid] = e
        if e.get("stage") not in ELEMENT_STAGES:
            errors.append(f"element {eid}: invalid stage {e.get('stage')}")
        if e.get("evidence") not in EVIDENCE:
            errors.append(f"element {eid}: invalid evidence {e.get('evidence')}")
        if not e.get("name") or not e.get("kind"):
            errors.append(f"element {eid}: name and kind are required")
    if len(ids) != len(set(ids)):
        errors.append("element IDs must be unique")
    idset = set(ids)

    flow_ids = []
    for i, f in enumerate(model.get("flows", [])):
        fid = f.get("id") or f"flows[{i}]"
        flow_ids.append(fid)
        if f.get("from") not in idset:
            errors.append(f"flow {fid}: unknown from element {f.get('from')}")
        if f.get("to") not in idset:
            errors.append(f"flow {fid}: unknown to element {f.get('to')}")
        if f.get("stage") not in ELEMENT_STAGES:
            errors.append(f"flow {fid}: invalid stage {f.get('stage')}")
        if f.get("evidence") not in EVIDENCE:
            errors.append(f"flow {fid}: invalid evidence {f.get('evidence')}")
        if f.get("type") not in FLOW_TYPES:
            errors.append(f"flow {fid}: invalid type {f.get('type')}")

        src = element_by_id.get(f.get("from"))
        dst = element_by_id.get(f.get("to"))
        # A flow can reference shared elements, but a stage-specific flow should not silently connect
        # two elements that both belong exclusively to a different stage.
        if src and dst and src.get("stage") == dst.get("stage") and src.get("stage") in VIEW_STAGES:
            if f.get("stage") != src.get("stage"):
                errors.append(f"flow {fid}: stage differs from both endpoint stages")
    if len(flow_ids) != len(set(flow_ids)):
        errors.append("flow IDs must be unique")

    for r in model.get("risks", []):
        rid = r.get("id", "<risk>")
        if r.get("stage") not in ELEMENT_STAGES:
            errors.append(f"risk {rid}: invalid stage")
        for target in r.get("affects", []):
            if target not in idset:
                errors.append(f"risk {rid}: affects unknown element {target}")

    for s in model.get("health_signals", []):
        if not s.get("id") or not s.get("name") or not s.get("desired_state"):
            errors.append("health signal requires id, name, and desired_state")

    for r in model.get("recovery_actions", []):
        rid = r.get("id", "<recovery>")
        if r.get("level") not in LEVELS:
            errors.append(f"recovery {rid}: invalid autonomy level {r.get('level')}")
        for key in ("trigger", "action", "authority"):
            if not r.get(key):
                errors.append(f"recovery {rid}: {key} is required")
        if r.get("level") in {"L2", "L3"} and "reversible" not in r:
            errors.append(f"recovery {rid}: automated/adaptive action must state reversibility")

    adaptation = model.get("adaptation", {})
    if adaptation:
        if adaptation.get("level") not in LEVELS:
            errors.append(f"adaptation.level invalid: {adaptation.get('level')}")
        if adaptation.get("level") in {"L2", "L3"} and not adaptation.get("max_blast_radius"):
            errors.append("L2/L3 adaptation must define max_blast_radius")

    for t in model.get("transitions", []):
        tid = t.get("id", "<transition>")
        if t.get("from") not in VIEW_STAGES or t.get("to") not in VIEW_STAGES:
            errors.append(f"transition {tid}: invalid from/to stage")
        if not t.get("change"):
            errors.append(f"transition {tid}: change is required")

    return errors


def main() -> None:
    p = argparse.ArgumentParser(description="Validate a canonical System Design Architect model")
    p.add_argument("model", help="Path to system.json")
    args = p.parse_args()
    path = Path(args.model)
    try:
        model = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: invalid JSON: {exc}")
        raise SystemExit(1)
    errors = validate(model)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("Canonical system model validation passed.")


if __name__ == "__main__":
    main()
