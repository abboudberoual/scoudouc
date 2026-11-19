"""Tests for stand v3 (2020 extrusion version).  Run from this folder:  python3 -m pytest -q test_stand_v3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trimesh
import bom, collar, handcheck, bracket

STL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
NAMES = ["collar_18", "collar_24", "collar_29", "collar_38", "ring"]


def test_stls_watertight_fit_and_under_6h():
    res = collar.build_all()
    for n in NAMES:
        m = trimesh.load(os.path.join(STL, n + ".stl"))
        assert m.is_watertight, n
        v, hrs, g = res[n]
        assert hrs < 6.0, n
        assert all(e <= b for e, b in zip(sorted(m.extents), sorted(collar.MK3_BED))), n


def test_bracket_watertight_and_under_1h():
    v, hrs, g = bracket.build()
    m = trimesh.load(os.path.join(STL, "bracket.stl"))
    assert m.is_watertight and m.volume > 0
    assert hrs < 1.0
    assert g <= bom.BRACKET_G                                  # the BOM weight is not understated


def test_ring_passes_the_biggest_collar_and_sits_between_bars():
    big = collar.make_collar(38)
    assert max(big.extents[:2]) < collar.RING_ID           # ring slides over the 38 mm collar
    assert collar.RING_OD < 72                              # fits between 2020 bars set 72 mm clear apart (92 c-c)


def test_motor_sticks_out_15mm_for_shortest_motor():
    shortest = {18: 70, 24: 70, 29: 98, 38: 130}
    for d, L in shortest.items():
        assert L - collar.DEPTH[d] >= 15


def test_cut_list_and_stock_packing():
    o = handcheck.out
    assert abs(o["cut_total_m"] - 3.612) < 1e-6
    assert o["longest_piece_mm"] == 483
    # four 1 m stock lengths with a 3 mm saw kerf: 2 uprights each, six 160s, six 120s
    kerf = 3.0
    assert 2 * 483 + kerf <= 1000 and 6 * 160 + 5 * kerf <= 1000 and 6 * 120 + 5 * kerf <= 1000
    assert o["top_clearance_mm"] >= 20                       # a 360 mm 38 mm motor sits fully inside the top frame
    assert o["m5_screws"] == 64 and o["m5_tnuts"] == 64


def test_handcheck_margins():
    o = handcheck.out
    assert o["plate_two_edge_SF"] >= 1.5                     # 3.2 mm 6061 plate, worst case two-edge support
    assert o["ply6_two_edge_SF"] < 1.0                       # the 6 mm plywood insert would NOT pass the same case
    assert o["rail_SF"] >= 3 and o["rail_deflection_mm"] < 0.5
    assert o["guy_tnut_SF"] >= 3 and o["guy_padeye_SF"] >= 3
    assert o["ring_screw_SF"] >= 5 and o["bar_SF"] >= 10 and o["upright_SF"] >= 5
    assert o["bracket_tnut_SF"] >= 3
    assert o["cell_100_peak_frac_with_overshoot"] < 0.85      # 100 kg survives 600 N x 1.3
    assert o["cell_50_peak_frac_with_overshoot"] > 1.0        # 50 kg does not
    assert o["frame_mass_kg"] < 3.5 and o["total_mass_kg"] < 6


def test_cost_numbers():
    assert abs(bom.total() - 278.55) < 0.01
    assert abs(bom.reduced() - 176.47) < 0.01
    assert abs(bom.reduced(sure_only=True) - 204.47) < 0.01
    assert bom.reduced() > 120                                # honest: extrusion does not meet the CAD 120 line
    assert 80 < bom.total() - bom.PLYWOOD_TOTAL < 90          # the premium over plywood, about CAD 86
    assert 10 < bom.printed_bracket_saving() < 16
