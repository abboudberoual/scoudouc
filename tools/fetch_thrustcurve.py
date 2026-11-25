#!/usr/bin/env python3
"""Fetch motors from thrustcurve.org and convert them to data/library/motors.json entries (tier 0: code, no model).

Usage:
  python tools/fetch_thrustcurve.py --names C6 E12 E16 F15 G8 --out results/T-011-2

Writes into --out:
  search-<name>.json   the raw thrustcurve.org search reply (provenance)
  <Mfr>_<name>_<simfileId>.eng   each RASP file as downloaded
  output.json          {"entries": [...]} in the motors.json schema, tier "single-source"
Exit 1 if nothing at all was found (network blocked, API changed). A name with no match is
reported in output.json "missing" but is not an error: the builder decides.

Stdlib only so it runs on the owner's laptop daemon without installs.
API: https://www.thrustcurve.org/info/api.html (search.json, download.json).
"""
import argparse, base64, json, os, sys, urllib.request
from datetime import date

API = "https://www.thrustcurve.org/api/v1"
UA = "scoudouc-library/1.0"


def post(path, body):
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def parse_rasp(text):
    """RASP .eng -> header dict + [[t, N]] curve (starts at [0, 0] if the file does not)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith(";")]
    if not lines:
        raise ValueError("empty .eng")
    h = lines[0].split()
    if len(h) < 7:
        raise ValueError(f"bad .eng header: {lines[0]!r}")
    header = {"name": h[0], "diameter_mm": float(h[1]), "length_mm": float(h[2]), "delays": h[3],
              "propellant_kg": float(h[4]), "total_kg": float(h[5]), "manufacturer": " ".join(h[6:])}
    curve = []
    for ln in lines[1:]:
        p = ln.split()
        if len(p) < 2:
            continue
        curve.append([float(p[0]), float(p[1])])
    if curve and curve[0][0] > 0:
        curve.insert(0, [0.0, 0.0])
    return header, curve


def impulse(curve):
    return sum((curve[j][0] - curve[j - 1][0]) * (curve[j][1] + curve[j - 1][1]) / 2 for j in range(1, len(curve)))


def entry_from(meta, header, curve, eng_url, today):
    """Prefer thrustcurve metadata for summary numbers; fall back to the curve itself."""
    I = meta.get("totImpulseNs") or round(impulse(curve), 2)
    burn = meta.get("burnTimeS") or (curve[-1][0] if curve else None)
    delays = meta.get("delays") or header["delays"]
    return {
        "designation": f"{meta.get('manufacturerAbbrev') or header['manufacturer']} {meta.get('commonName') or header['name']}",
        "manufacturer": meta.get("manufacturer") or header["manufacturer"],
        "diameter_mm": meta.get("diameter") or header["diameter_mm"],
        "length_mm": meta.get("length") or header["length_mm"],
        "total_impulse_Ns": I,
        "avg_thrust_N": meta.get("avgThrustN") or (round(I / burn, 2) if burn else None),
        "max_thrust_N": meta.get("maxThrustN") or max(n for _, n in curve),
        "burn_s": burn,
        "propellant_g": meta.get("propWeightG") or round(header["propellant_kg"] * 1000, 1),
        "total_g": meta.get("totalWeightG") or round(header["total_kg"] * 1000, 1),
        "delay_options": [d for d in str(delays).replace("-", ",").split(",") if d and d != "P"],
        "curve": curve,
        "cert_body": meta.get("certOrg"),
        "thrustcurve_motor_id": meta.get("motorId"),
        "sources": [{"url": eng_url, "date": today, "what": "thrustcurve.org RASP curve + summary metadata"}],
        "tier": "single-source",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", nargs="+", required=True, help="common names, e.g. C6 E12")
    ap.add_argument("--manufacturer", default=None, help="restrict search (e.g. Estes)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    today = date.today().isoformat()
    entries, missing, errors = [], [], []
    for name in a.names:
        q = {"commonName": name, "availability": "all", "maxResults": 20}
        if a.manufacturer:
            q["manufacturer"] = a.manufacturer
        try:
            res = post("search.json", q)
        except Exception as e:
            errors.append(f"{name}: search failed: {e}")
            continue
        with open(os.path.join(a.out, f"search-{name}.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)
        motors = res.get("results") or []
        if not motors:
            missing.append(name)
            continue
        for m in motors:
            try:
                dl = post("download.json", {"motorIds": [m["motorId"]], "format": "RASP", "data": "file"})
            except Exception as e:
                errors.append(f"{name}/{m.get('motorId')}: download failed: {e}")
                continue
            files = dl.get("results") or []
            if not files:
                errors.append(f"{name}/{m.get('motorId')}: no RASP file")
                continue
            fdat = files[0]  # first file = thrustcurve's preferred (usually the certification curve)
            text = base64.b64decode(fdat["data"]).decode("utf-8", errors="replace")
            mfr = (m.get("manufacturerAbbrev") or "X").replace(" ", "")
            fn = f"{mfr}_{name}_{fdat.get('simfileId', m['motorId'])}.eng"
            with open(os.path.join(a.out, fn), "w", encoding="utf-8") as f:
                f.write(text)
            header, curve = parse_rasp(text)
            url = f"https://www.thrustcurve.org/simfiles/{fdat['simfileId']}/" if fdat.get("simfileId") else \
                  f"https://www.thrustcurve.org/motors/{m.get('manufacturerAbbrev', '')}/{m.get('commonName', name)}/"
            e = entry_from(m, header, curve, url, today)
            e["raw_file"] = fn
            entries.append(e)
    with open(os.path.join(a.out, "output.json"), "w", encoding="utf-8") as f:
        json.dump({"entries": entries, "missing": missing, "errors": errors, "fetched_at": today}, f, indent=1)
    print(json.dumps({"entries": len(entries), "missing": missing, "errors": len(errors)}))
    return 0 if entries else 1


if __name__ == "__main__":
    sys.exit(main())
