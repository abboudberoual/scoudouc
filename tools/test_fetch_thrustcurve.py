"""Offline tests for fetch_thrustcurve.py (no network). Run: python -m pytest tools/ -q
The .eng below is a SYNTHETIC fixture (a triangle, 8 N·s), not real motor data."""
import base64, json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import fetch_thrustcurve as ft

ENG = """; synthetic test fixture
C6 18 70 0-3-5-7 0.0108 0.0241 Estes
0.5 8.0
1.0 8.0
2.0 0.0
"""
META = {"motorId": "abc", "manufacturer": "Estes Industries", "manufacturerAbbrev": "Estes", "commonName": "C6",
        "diameter": 18, "length": 70, "certOrg": "NAR"}  # summary numbers left out: fall back to the curve


def test_parse_and_entry():
    h, c = ft.parse_rasp(ENG)
    assert h["diameter_mm"] == 18 and c[0] == [0.0, 0.0] and len(c) == 4
    e = ft.entry_from(META, h, c, "https://www.thrustcurve.org/simfiles/x/", "2026-11-25")
    assert abs(e["total_impulse_Ns"] - 10.0) < 1e-6  # 2 + 4 + 4 N·s
    assert e["propellant_g"] == 10.8 and e["total_g"] == 24.1
    assert e["delay_options"] == ["0", "3", "5", "7"] and e["tier"] == "single-source"


def test_main_with_fake_api():
    calls = []
    def fake_post(path, body):
        calls.append(path)
        if path == "search.json":
            return {"results": [META] if body["commonName"] == "C6" else []}
        return {"results": [{"simfileId": "s1", "data": base64.b64encode(ENG.encode()).decode()}]}
    ft.post = fake_post
    with tempfile.TemporaryDirectory() as d:
        sys.argv = ["x", "--names", "C6", "Z9", "--out", d]
        assert ft.main() == 0
        out = json.load(open(os.path.join(d, "output.json")))
        assert len(out["entries"]) == 1 and out["missing"] == ["Z9"]
        assert os.path.exists(os.path.join(d, "Estes_C6_s1.eng"))
