"""Build the nozzle-UP thrust-stand cup and cage as STL files, without OpenSCAD.

Same geometry and parameter names as cup.scad and cage.scad. Usage:
    python hardware/test-stand/make_holder_stl.py            # makes all four default STLs
    python hardware/test-stand/make_holder_stl.py --motor-d 24 --holder-len 75   # one cup + matching cage
Needs: pip install trimesh manifold3d

(The old nozzle-down holder is superseded; holder.scad and the holder_*.stl files are kept for reference only.)
"""
import argparse
import os
import numpy as np
import trimesh
from trimesh.creation import cylinder, box

HERE = os.path.dirname(os.path.abspath(__file__))


def cup_dims(motor_d=29, clearance=0.4, liner_t=1.0, wall=3):
    bore = motor_d + 2 * liner_t + clearance
    return bore, bore + 2 * wall


def _cyl(d, h, z0, segs=96):
    c = cylinder(radius=d / 2, height=h, sections=segs)
    c.apply_translation([0, 0, z0 + h / 2])
    return c


def _cube(sx, sy, sz, x0, y0, z0):
    b = box(extents=[sx, sy, sz])
    b.apply_translation([x0 + sx / 2, y0 + sy / 2, z0 + sz / 2])
    return b


def build_cup(motor_d=29, holder_len=85, clearance=0.4, liner_t=1.0, wall=3, plate_t=8,
              bolt_sq=40, bolt_d=4.4, flange_w=56, lead_slot=7, lead_h=4, groove_w=4,
              groove_d=1.2, bolt_holes=True, vent_notch=True, sections=96):
    """Cup: bolt flange at the bottom (z=0), thick floor, open top, lead notch at the base (+X side)."""
    assert motor_d in (18, 24, 29), "motor_d must be 18, 24 or 29"
    assert 70 <= holder_len <= 100, "holder_len must be 70 to 100 mm"
    bore, outer = cup_dims(motor_d, clearance, liner_t, wall)
    top = plate_t + holder_len

    tube = _cyl(outer, top, 0, sections)
    flange = _cube(flange_w, flange_w, plate_t, -flange_w / 2, -flange_w / 2, 0)
    body = trimesh.boolean.union([tube, flange], engine="manifold")

    cuts = [
        _cyl(bore, holder_len + 1, plate_t, sections),                      # bore, floor stays 8 mm thick
        # vertical groove behind the liner for the igniter leads (+X side), top to base
        _cube(groove_d + 1, groove_w, holder_len + 1, bore / 2 - groove_d, -groove_w / 2, plate_t),
        # side notch through the wall at the base: leads leave here (+X)
        _cube(outer / 2 + 2 - (bore / 2 - groove_d), lead_slot, lead_h,
              bore / 2 - groove_d, -lead_slot / 2, plate_t),
    ]
    if vent_notch:  # opposite side: lets any gas escape sideways (see README, ejection charge)
        cuts.append(_cube(outer / 2 + 2 - (bore / 2 - groove_d), lead_slot, lead_h,
                          -(outer / 2 + 2), -lead_slot / 2, plate_t))
    if bolt_holes:
        for x in (-1, 1):
            for y in (-1, 1):
                h = _cyl(bolt_d, plate_t + 2, -1, 24)
                h.apply_translation([x * bolt_sq / 2, y * bolt_sq / 2, 0])
                cuts.append(h)
    return trimesh.boolean.difference([body] + cuts, engine="manifold")


def _box_pts(x0, x1, y0, y1, z0, z1):
    return [[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def build_cage(motor_d=29, holder_len=85, clearance=0.4, liner_t=1.0, wall=3, plate_t=8,
               stand_h=25, cage_gap=3, ring_h=10, ring_w=5, ring_drop=5, post_R=52,
               post_r=10, post_t=16, arm_w=10, foot_ext=12, tab_t=5, screw_d=4.5,
               post_angle0=90, print_orientation=True, sections=96):
    """Ring + 3 posts + foot tabs. Built in USE orientation (z=0 is the plywood), then flipped
    ring-down for printing if print_orientation is True."""
    _, outer = cup_dims(motor_d, clearance, liner_t, wall)
    cup_top = stand_h + plate_t + holder_len
    ring_top = cup_top - ring_drop
    ring_z = ring_top - ring_h
    ring_id = outer + 2 * cage_gap
    ring_od = ring_id + 2 * ring_w
    parts = []

    ring = trimesh.boolean.difference(
        [_cyl(ring_od, ring_h, ring_z, sections), _cyl(ring_id, ring_h + 2, ring_z - 1, sections)],
        engine="manifold")
    parts.append(ring)

    for k in range(3):
        a = post_angle0 + 120 * k
        px0, px1 = post_R - post_r / 2, post_R + post_r / 2
        pieces = []
        pieces.append(_cube(post_r, post_t, ring_top, px0, -post_t / 2, 0))                 # post
        pieces.append(_cube(px0 - (ring_od / 2 - 1), arm_w, ring_h,
                            ring_od / 2 - 1, -arm_w / 2, ring_z))                          # arm to ring
        tab = _cube(post_r + foot_ext, post_t, tab_t, px0, -post_t / 2, 0)                  # foot tab
        pieces.append(tab)
        # two 45 degree ribs so the tab prints upside-down without support
        for s in (-1, 1):
            yc = s * (post_t / 2 - 1.5)
            pts = (_box_pts(px0, px1 + foot_ext, yc - 1.5, yc + 1.5, 0, tab_t)
                   + _box_pts(px0, px1, yc - 1.5, yc + 1.5, tab_t + foot_ext - 0.01, tab_t + foot_ext))
            pieces.append(trimesh.convex.convex_hull(np.array(pts)))
        solid = trimesh.boolean.union(pieces, engine="manifold")
        hole = _cyl(screw_d, tab_t + foot_ext + 2, -1, 24)
        hole.apply_translation([px1 + foot_ext / 2, 0, 0])
        solid = trimesh.boolean.difference([solid, hole], engine="manifold")
        solid.apply_transform(trimesh.transformations.rotation_matrix(np.radians(a), [0, 0, 1]))
        parts.append(solid)
    cage = trimesh.boolean.union(parts, engine="manifold")
    if print_orientation:
        cage.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
        cage.apply_translation([0, 0, -cage.bounds[0][2]])
    return cage


build = build_cup  # old name kept so older notes still work


def print_time_h(mesh, infill=0.4, perimeters=4):
    """Rough MK3 estimate at 0.2 mm layers, ~50 mm/s: about 3.5 mm3/s of plastic including travel and
    slow layers, plus a small per-layer overhead. Shell volume ~ perimeters x 0.45 mm x surface area."""
    shell = min(mesh.volume, mesh.area * perimeters * 0.45 / 2 * 0.9)
    plastic = shell + (mesh.volume - shell) * infill
    layers = (mesh.bounds[1][2] - mesh.bounds[0][2]) / 0.2
    return (plastic / 3.5 + layers * 4) / 3600


def report(path, m):
    print(f"{os.path.relpath(path)}: {len(m.faces)} faces, watertight={m.is_watertight}, "
          f"bounds {np.round(m.extents, 1).tolist()} mm, volume {m.volume/1000:.1f} cm3, "
          f"est. MK3 print {print_time_h(m):.1f} h")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor-d", type=int, default=None)
    ap.add_argument("--holder-len", type=int, default=None)
    ap.add_argument("--stand-h", type=float, default=25, help="height of cup underside above the plywood (mm)")
    ap.add_argument("--outdir", default=HERE)
    a = ap.parse_args()
    jobs = ([(a.motor_d, a.holder_len or 75)] if a.motor_d
            else [(29, 85), (24, 75), (18, 75)])
    for d, n in jobs:
        cup = build_cup(d, n)
        p = os.path.join(a.outdir, f"cup_{d}mm_{n}mm.stl")
        cup.export(p)
        report(p, cup)
    # the default cage.stl fits the 29 mm / 85 mm cup; others are named for their cup
    for d, n in jobs:
        cage = build_cage(d, n, stand_h=a.stand_h)
        name = "cage.stl" if (d, n) == (29, 85) else f"cage_{d}mm_{n}mm.stl"
        p = os.path.join(a.outdir, name)
        cage.export(p)
        report(p, cage)
