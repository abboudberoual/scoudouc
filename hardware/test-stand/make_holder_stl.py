"""Build the thrust-stand motor holder as an STL without OpenSCAD.

Same geometry and parameter names as holder.scad. Usage:
    python hardware/test-stand/make_holder_stl.py --motor-d 29 --holder-len 85
Needs: pip install trimesh manifold3d
"""
import argparse
import numpy as np
import trimesh
from trimesh.creation import cylinder, box


def build(motor_d=29, holder_len=85, clearance=0.4, wall=3, plate_t=8, lip_t=2.5,
          lip_inset=3.5, bolt_sq=40, bolt_d=4.4, flange_w=56, lead_slot=7, sections=96):
    assert motor_d in (18, 24, 29), "motor_d must be 18, 24 or 29"
    assert 70 <= holder_len <= 100, "holder_len must be 70 to 100 mm"
    bore = motor_d + clearance
    outer = bore + 2 * wall

    def cyl(d, h, z0, segs=sections):
        c = cylinder(radius=d / 2, height=h, sections=segs)
        c.apply_translation([0, 0, z0 + h / 2])
        return c

    def cube(sx, sy, sz, x0, y0, z0):
        b = box(extents=[sx, sy, sz])
        b.apply_translation([x0 + sx / 2, y0 + sy / 2, z0 + sz / 2])
        return b

    tube = cyl(outer, holder_len, lip_t)
    lip = cyl(outer, lip_t + 0.01, 0)
    flange = cube(flange_w, flange_w, plate_t, -flange_w / 2, -flange_w / 2, lip_t + holder_len)
    body = trimesh.boolean.union([tube, lip, flange], engine="manifold")

    cuts = [
        cyl(bore, holder_len + 0.01, lip_t),                       # motor bore, stops at the top plate
        cyl(bore - 2 * lip_inset, lip_t + 2, -1),                   # nozzle opening through the lip
        cube(outer, lead_slot, lip_t + 1, bore / 2 - lip_inset - 1, -lead_slot / 2, -1),  # igniter lead notch
    ]
    for x in (-1, 1):
        for y in (-1, 1):
            h = cyl(bolt_d, plate_t + 2, lip_t + holder_len - 1, segs=24)
            h.apply_translation([x * bolt_sq / 2, y * bolt_sq / 2, 0])
            cuts.append(h)
    part = trimesh.boolean.difference([body] + cuts, engine="manifold")
    return part


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor-d", type=int, default=29)
    ap.add_argument("--holder-len", type=int, default=85)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    m = build(a.motor_d, a.holder_len)
    out = a.out or f"hardware/test-stand/holder_{a.motor_d}mm_{a.holder_len}mm.stl"
    m.export(out)
    print(f"{out}: {len(m.faces)} faces, watertight={m.is_watertight}, "
          f"bounds {np.round(m.bounds, 1).tolist()} mm, volume {m.volume/1000:.1f} cm3")
