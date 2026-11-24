#!/usr/bin/env python3
"""Validate data/library/*.json: every entry has sources with URLs; numeric fields are numbers; motors have curves.

Usage: python data/library/validate.py [--file path.json]   (exit 1 on any problem)
"""
import argparse, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIRED = {
    "motors": ["designation", "diameter_mm", "total_impulse_Ns", "avg_thrust_N", "burn_s", "curve", "sources"],
    "materials": ["name", "sources"],
    "vendors": ["part", "vendor", "url", "price_cad", "checked_at"],
    "rules": ["id", "authority", "section", "text", "sources"],
}


def problems_for(kind, entries):
    out = []
    for i, e in enumerate(entries):
        for k in REQUIRED.get(kind, []):
            if k not in e or e[k] in (None, "", []):
                out.append(f"{kind}[{i}] missing {k}")
        for s in e.get("sources", []) or []:
            if not str(s.get("url", "")).startswith("http"):
                out.append(f"{kind}[{i}] source without http url")
        if kind == "motors":
            c = e.get("curve") or []
            if len(c) < 3 or any(len(p) != 2 for p in c):
                out.append(f"{kind}[{i}] curve needs >=3 [t,N] points")
            for k in ("diameter_mm", "total_impulse_Ns", "avg_thrust_N", "burn_s"):
                if not isinstance(e.get(k), (int, float)):
                    out.append(f"{kind}[{i}] {k} not numeric")
            if e.get("tier") not in (None, "seed", "single-source", "dual-source", "measured"):
                out.append(f"{kind}[{i}] bad tier {e.get('tier')}")
        if kind == "rules" and e.get("review") not in (None, "opus", "owner"):
            out.append(f"{kind}[{i}] bad review {e.get('review')}")
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--file", default=None); a = ap.parse_args()
    files = [a.file] if a.file else sorted(glob.glob(os.path.join(HERE, "*.json")))
    probs = []
    for f in files:
        kind = os.path.splitext(os.path.basename(f))[0]
        kind = {"motors": "motors", "materials": "materials", "vendors": "vendors", "rules": "rules"}.get(kind, kind)
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            probs.append(f"{f}: not valid JSON ({e})"); continue
        entries = data if isinstance(data, list) else data.get("entries", [])
        if kind in REQUIRED:
            probs += problems_for(kind, entries)
    for p in probs:
        print("PROBLEM:", p)
    print(f"checked {len(files)} file(s), {len(probs)} problem(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
