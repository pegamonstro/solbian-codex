#!/usr/bin/env python3
import json, os, pathlib

ROOT = pathlib.Path("codex_solbian/archetypes")
INPUTS = [
    ROOT / "human_archetypes.sref",
    ROOT / "synthetic_archetypes.sref",
    ROOT / "solbian_archetypes.sref",
]

OUT_DIRS = {
    "human": ROOT / "human",
    "synthetic": ROOT / "synthetic",
    "solbian": ROOT / "solbian",
}

for d in OUT_DIRS.values():
    d.mkdir(parents=True, exist_ok=True)

def enrich(obj):
    base = {
        "capabilities": [],
        "virtues": [],
        "vices": [],
        "signals_positive": [],
        "signals_negative": [],
        "development_paths": [],
        "related_archetypes": [],
        "policy_flags": {"risk_level": "unset", "requires_supervision": False},
        "version": "sref_v1",
    }
    base.update(obj)
    return base

for path in INPUTS:
    if not path.exists():
        print(f"Missing: {path}")
        continue
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            obj = json.loads(line)
            domain = obj.get("domain")
            out_dir = OUT_DIRS.get(domain)
            if not out_dir:
                print(f"Unknown domain {domain} in {obj.get('id')}")
                continue
            # filename from id: archetype.human.seeker -> seeker.sref
            aid = obj["id"].split(".")[-1]
            outfile = out_dir / f"{aid}.sref"
            with outfile.open("w") as out:
                out.write(json.dumps(enrich(obj), ensure_ascii=False))
            print(f"Wrote {outfile}")