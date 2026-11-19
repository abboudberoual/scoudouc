"""Tests for stand v3.  Run from this folder:  python3 -m pytest -q test_stand_v3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trimesh
import bom, collar, handcheck

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


def test_ring_passes_the_biggest_collar_and_sits_between_bars():
    big = collar.make_collar(38)
    assert max(big.extents[:2]) < collar.RING_ID           # 46.4 < 50: ring slides over the 38 mm collar
    assert collar.RING_OD < 72                              # fits between bars set 72 mm apart


def test_motor_sticks_out_15mm_for_shortest_motor():
    shortest = {18: 70, 24: 70, 29: 98, 38: 130}            # C6, D12, shortest 29 mm, shortest 38 mm (v2 rule)
    for d, L in shortest.items():
        assert L - collar.DEPTH[d] >= 15


def test_handcheck_margins():
    o = handcheck.out
    assert o["base_SF_along_grain"] >= 3.5 and o["base_SF_across_grain"] >= 1.8
    assert o["ring_screw_SF"] >= 5 and o["panel_foot_SF"] >= 2.5
    assert o["cell_100_peak_frac_with_overshoot"] < 0.85      # 100 kg survives 600 N x 1.3
    assert o["cell_50_peak_frac_with_overshoot"] > 1.0        # 50 kg does not
    assert o["total_mass_kg"] < 6


def test_cost_numbers():
    assert abs(bom.total() - 192.35) < 0.01
    assert abs(bom.reduced() - 117.35) < 0.01
    assert bom.reduced() <= 120
    assert bom.reduced(sure_only=True) > 120                  # honest: only with the two owner-dependent items
