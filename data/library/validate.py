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
            # Physics consistency: a fabricated entry usually breaks these (observed 2026-11-23).
            if len(c) >= 3 and all(len(pt) == 2 for pt in c) and all(isinstance(e.get(k), (int, float)) for k in ("total_impulse_Ns", "avg_thrust_N", "burn_s")):
                area = sum((c[j][0] - c[j-1][0]) * (c[j][1] + c[j-1][1]) / 2 for j in range(1, len(c)))
                I, avg, burn = e["total_impulse_Ns"], e["avg_thrust_N"], e["burn_s"]
                if I <= 0 or abs(area - I) > 0.15 * I:
                    out.append(f"{kind}[{i}] curve area {area:.2f} N·s disagrees with total_impulse {I} by >15%")
                if burn > 0 and abs(I / burn - avg) > 0.15 * avg:
                    out.append(f"{kind}[{i}] avg_thrust {avg} disagrees with impulse/burn {I / burn:.2f} by >15%")
                mx = e.get("max_thrust_N")
                if isinstance(mx, (int, float)) and mx < avg:
                    out.append(f"{kind}[{i}] max_thrust below avg_thrust")
                cls = str(e.get("designation", "")).split()[-1][:1].upper()
                ranges = {"A": (1.26, 2.5), "B": (2.51, 5), "C": (5.01, 10), "D": (10.01, 20), "E": (20.01, 40), "F": (40.01, 80), "G": (80.01, 160)}
                if cls in ranges and not (ranges[cls][0] * 0.9 <= I <= ranges[cls][1] * 1.0):
                    out.append(f"{kind}[{i}] total_impulse {I} outside class {cls} range {ranges[cls]}")
            pg, tg = e.get("propellant_g"), e.get("total_g")
            if isinstance(pg, (int, float)) and isinstance(tg, (int, float)) and pg >= tg:
                out.append(f"{kind}[{i}] propellant_g must be less than total_g")
            if e.get("tier") not in (None, "seed", "single-source", "dual-source", "measured"):
                out.append(f"{kind}[{i}] bad tier {e.get('tier')}")
        if kind == "rules" and e.get("review") not in (None, "opus", "owner"):
            out.append(f"{kind}[{i}] bad review {e.get('review')}")
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--file", default=None)
    ap.add_argument("--kind", default=None, choices=sorted(REQUIRED), help="schema to check --file against (required when the file name is not one of them)")
    a = ap.parse_args()
    files = [a.file] if a.file else sorted(glob.glob(os.path.join(HERE, "*.json")))
    probs = []
    for f in files:
        kind = os.path.splitext(os.path.basename(f))[0]
        if a.kind:
            kind = a.kind
        if a.file and kind not in REQUIRED:
            probs.append(f"{f}: unknown kind '{kind}' — pass --kind (fail closed: an unchecked file never passes)")
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            probs.append(f"{f}: not valid JSON ({e})"); continue
        entries = data if isinstance(data, list) else data.get("entries", [])
        if kind in REQUIRED:
            if a.file and not entries:
                probs.append(f"{f}: no entries")
            probs += problems_for(kind, entries)
    for p in probs:
        print("PROBLEM:", p)
    print(f"checked {len(files)} file(s), {len(probs)} problem(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
