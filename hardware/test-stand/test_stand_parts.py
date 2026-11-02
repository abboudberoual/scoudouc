"""Checks for the nozzle-up cup and cage. Run: python -m pytest hardware/test-stand -q"""
import os, sys
import numpy as np
import pytest
import trimesh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_holder_stl as m

CASES = [(29, 85), (24, 75), (18, 75)]


def solid_at(mesh, p):
    """True if the point is inside solid material (probe cube test; avoids needing rtree)."""
    probe = trimesh.creation.box(extents=[0.5] * 3)
    probe.apply_translation(p)
    hit = trimesh.boolean.intersection([mesh, probe], engine="manifold")
    return len(hit.faces) > 0 and hit.volume > 0.1


def assembled(d, n, stand_h=25):
    cup = m.build_cup(d, n)
    cup.apply_translation([0, 0, stand_h])
    cage = m.build_cage(d, n, stand_h=stand_h, print_orientation=False)
    return cup, cage


@pytest.mark.parametrize("d,n", CASES)
def test_watertight_and_fits_printers(d, n):
    for mesh in (m.build_cup(d, n), m.build_cage(d, n)):
        assert mesh.is_watertight and mesh.volume > 0
        assert mesh.extents[0] <= 250 and mesh.extents[1] <= 210 and mesh.extents[2] <= 210  # MK3 bed
        assert m.print_time_h(mesh) < 6


@pytest.mark.parametrize("d,n", CASES)
def test_cage_never_touches_cup(d, n):
    cup, cage = assembled(d, n)
    overlap = trimesh.boolean.intersection([cup, cage], engine="manifold")
    assert overlap.volume < 1e-6 if len(overlap.faces) else True
    # smallest gap: sample cup surface, compare with cage vertices densely refined
    pts = cup.sample(20000)
    cp = cage.sample(40000)
    from scipy.spatial import cKDTree
    gap = cKDTree(cp).query(pts)[0].min()
    assert gap >= 2.0, f"gap {gap:.2f} mm too small (design is 3 mm; sampling error allowed)"


def test_bore_and_floor():
    cup = m.build_cup(29, 85)
    bore, _ = m.cup_dims(29)
    # floor is solid from z=0 to 8 mm along the axis; bore is open above it
    assert solid_at(cup, [0, 0, 4])
    assert not solid_at(cup, [0, 0, 9])
    assert not solid_at(cup, [0, 0, 90])
    assert bore == pytest.approx(31.4)


def test_flat_bottom_variant_has_no_bolt_holes():
    holes = m.build_cup(29, 85, bolt_holes=True)
    flat = m.build_cup(29, 85, bolt_holes=False)
    assert flat.volume > holes.volume
    assert not solid_at(holes, [20, 20, 4]) and solid_at(flat, [20, 20, 4])
