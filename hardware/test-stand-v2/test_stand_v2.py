"""Run: python3 -m pytest hardware/test-stand-v2 -q   (needs trimesh, manifold3d, numpy)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cup, cartridge, handcheck, bom

def test_cups_watertight_fit_and_under_6h():
    for d in (18, 24, 29, 38):
        m = cup.make_cup(d)
        assert m.is_watertight
        assert m.volume / 1000 * cup.H_PER_CM3 < 6.0
        assert m.extents[0] <= 56.01 and m.extents[1] <= 56.01          # one SCF flange for all
        bore = d + 2 * cup.LINER_T + cup.CLEAR
        assert m.extents[0] >= bore + 2 * cup.WALL                        # wall is intact

def hole_centres(mesh, z):
    """Centres of small closed loops (holes up to 12 mm across) in a slice at height z. No shapely needed."""
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    out = []
    for loop in sec.discrete:
        w = loop[:, :2].max(0) - loop[:, :2].min(0)
        if w.max() < 12:
            out.append(tuple(loop[:, :2].mean(0)))
    return out

def has_hole_near(mesh, z, pts, tol=1.0):
    c = hole_centres(mesh, z)
    return all(any(abs(x - a) < tol and abs(y - b) < tol for a, b in c) for x, y in pts)

def test_cup_bolt_pattern_is_scf():
    assert has_hole_near(cup.make_cup(29), 4.0, cartridge.SCF)

def test_motor_sticks_out_15mm_for_shortest_motor():
    shortest = {18: 70, 24: 70, 29: 98, 38: 130}                          # C6, D12, 29 mm F, 38 mm H
    for d, L in shortest.items():
        assert L - cup.DEPTH[d] >= 15

def test_cartridges_watertight_and_under_6h():
    for fn in (cartridge.plate_bar, cartridge.platform_bar, cartridge.plate_s, cartridge.platform_s):
        m = fn()
        assert m.is_watertight and m.volume / 1000 * cartridge.H_PER_CM3 < 6.0

def test_scp_holes_open_in_both_plates():
    for fn in (cartridge.plate_bar, cartridge.plate_s):
        assert has_hole_near(fn(), 4.0, cartridge.SCP)

def test_platform_scf_matches_cup_flange():
    assert sorted(cartridge.SCF) == sorted([(sx * cup.BOLT_SQ / 2, sy * cup.BOLT_SQ / 2) for sx in (-1, 1) for sy in (-1, 1)])

def test_hand_checks_have_margin():
    assert handcheck.deck_rails()[1] >= 3.0 and handcheck.deck_rails()[2] >= 2.5
    assert handcheck.long_rail()[1] >= 3.0
    assert handcheck.joints()[1] >= 4.0
    s, buck, sb, sf = handcheck.uprights()
    assert buck >= 20 and sf >= 10
    assert handcheck.bar_cell_couple()[1] >= 2.5

def test_bom_totals_and_mass():
    assert 540 < bom.total(4) < 580 and bom.total(3) < bom.total(4)
    assert bom.mass(4) * 1.1 <= 12.0                                       # solo-portable target with 10% for unlisted bits
    assert max(i[0] for i in bom.ITEMS) == len(bom.ITEMS)
