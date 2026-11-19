"""Stand v3: printed PLA inside-corner bracket for 2020 extrusion (the PRICED ALTERNATIVE to the steel kit).

Run: python3 bracket.py   (writes stl/bracket.stl, prints a summary)

Two legs at 90 degrees, 20 mm wide (the width of the profile), 22 mm long, 4.5 mm thick, one 5.4 mm hole per leg
for an M5 screw into a T-nut in the profile's slot, and a 3 mm triangular rib on each side edge (the middle stays open
so a hex key reaches the screw head).  Print: one leg FLAT on the bed, the other leg standing, no supports, 0.2 mm layers,
4 perimeters, 100% infill is not needed but the part is tiny so it is printed solid.  LAB: all 24 on one plate (about 3 h).
CARRIES NO THRUST: thrust goes cell -> plate -> rails -> ground.  It does carry the guy pull at the four bottom corners
(about 190 N) and, in a failure, the ring catch load, so read README section 5 before choosing it.
"""
import os
import numpy as np
import trimesh
from trimesh import creation, boolean

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stl")
H_PER_CM3 = 0.062          # h per cm3 of solid on an MK3 (same calibration as collar.py)
MK3_BED = (250.0, 210.0, 210.0)

W, L, T, RIB_T, RIB = 20.0, 22.0, 4.5, 3.0, 14.0
HOLE_D, HOLE_AT = 5.4, 13.0          # M5 clearance, hole centre 13 mm from the outer back of the bracket


def box(x0, x1, y0, y1, z0, z1):
    m = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return m


def rib(y0):
    """Triangular rib in the x-z plane between the two legs, RIB_T thick along y (convex hull of its six corners)."""
    pts = [(x, y, z) for (x, z) in ((T - 0.5, T - 0.5), (T + RIB, T - 0.5), (T - 0.5, T + RIB)) for y in (y0, y0 + RIB_T)]
    return trimesh.convex.convex_hull(np.array(pts))


def make_bracket():
    base = box(0, L, 0, W, 0, T)               # leg lying on the bed
    wall = box(0, T, 0, W, 0, L)               # leg standing up
    body = boolean.union([base, wall, rib(0.0), rib(W - RIB_T)], engine="manifold")
    h1 = creation.cylinder(radius=HOLE_D / 2, height=T + 2, sections=32)            # through the base leg (axis z)
    h1.apply_translation([HOLE_AT, W / 2, T / 2])
    h2 = creation.cylinder(radius=HOLE_D / 2, height=T + 2, sections=32)            # through the standing leg (axis x)
    h2.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    h2.apply_translation([T / 2, W / 2, HOLE_AT])
    return boolean.difference([body, h1, h2], engine="manifold")


def report(m):
    v = m.volume / 1000.0
    hrs = v * H_PER_CM3
    grams = v * 1.24
    assert m.is_watertight and m.volume > 0, "bracket not watertight"
    assert hrs < 1.0, "bracket over 1 h"
    assert all(e <= b for e, b in zip(sorted(m.extents), sorted(MK3_BED)))
    print("bracket      %5.2f cm3  %-14s watertight=%s  %.2f h  %.1f g solid  LAB (24 on one plate) or LIBRARY (one per job)" % (
        v, "x".join("%.0f" % e for e in m.extents), m.is_watertight, hrs, grams))
    return v, hrs, grams


def build():
    os.makedirs(OUT, exist_ok=True)
    m = make_bracket()
    m.export(os.path.join(OUT, "bracket.stl"))
    return report(m)


if __name__ == "__main__":
    build()
