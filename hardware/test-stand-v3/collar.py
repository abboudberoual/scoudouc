"""Stand v3: printed MOTOR COLLAR family (18 / 24 / 29 / 38 mm) and the guide RING.

Run:  python3 collar.py     (writes stl/collar_18.stl ... collar_38.stl and stl/ring.stl, prints a summary)

COLLAR: sits on the top boss of the S-type load cell and is held down by ONE M12 socket-head screw that
screws into the cell's own thread.  The screw head sits in a pocket in the floor.  A 2 mm aluminium disc
(decision 005's ejection-charge disc) lies on the floor and the motor stands on the disc.
  - 1 mm kraft-card liner tube in the bore is the PLA heat barrier (same as v1/v2); the collar is a CONSUMABLE.
  - Two notches at the foot (+Y and -Y) vent the ejection puff sideways.  The igniter leads leave through the -Y notch,
    down a groove in the bore wall.
  - Print: floor DOWN on the bed, no supports, 0.2 mm, 4 perimeters, 5 top/bottom layers, 40% infill, LIBRARY (Prusa MK3).

RING: a short tube with a flange.  The flange rests on two 2020 extrusion bars (72 mm clear between them) and is held by
four M3 x 10 screws into M3 T-nuts in the bars' top slots; the tube (66 mm across) hangs between the bars.  ID 50 mm lets the 46 mm 38-mm collar pass through, so the ring
guides the collar (2 mm gap) or the bare motor (6 to 16 mm gap).  It never carries thrust.
  - Print: flange DOWN on the bed (tube points up), no supports, 0.2 mm, 4 perimeters, 20% infill, LIBRARY.

Print time is estimated from volume with the v2 calibration (0.062 h per cm3 of solid on an MK3).
ALL cell dimensions are parameters: measure the cell you receive and re-run.
"""
import os
import numpy as np
import trimesh
from trimesh import creation, boolean

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stl")
H_PER_CM3 = 0.062          # h per cm3 of solid, MK3 (calibrated on the v1 cups, reused in v2)
MK3_BED = (250.0, 210.0, 210.0)
LIMIT_H = 6.0

LINER_T, CLEAR, WALL = 1.0, 0.4, 3.0
FLOOR = 18.0               # floor thickness: holds the screw-head pocket and spreads the load
POCKET_D, POCKET_DIA = 12.5, 19.5     # M12 socket head: 18 mm across, 12 mm tall
HOLE_DIA = 13.5            # M12 clearance (an M6 bolt with an 18 mm washer also fits: 5 kg cell swap)
NOTCH_W, NOTCH_H = 8.0, 6.0
GROOVE_W, GROOVE_D = 4.0, 1.2
CLEAR_18 = 1.4              # 18 mm bore is looser so the screw-head pocket (19.5) leaves a ledge of 0.95 mm, not a 0.45 mm sliver
DEPTH = {18: 50.0, 24: 55.0, 29: 65.0, 38: 85.0}   # bore depth above the floor; nozzle sticks out >= 15 mm (v2 rule)

RING_ID, RING_OD, RING_TUBE_H, RING_FL_T = 50.0, 66.0, 15.0, 5.0
RING_FL_Y, RING_FL_X = 116.0, 66.0
RING_SCREW_Y, RING_SCREW_X, RING_SCREW_D = 45.0, 12.0, 3.5


def cyl(r, h, z0=0.0, sections=96):
    m = creation.cylinder(radius=r, height=h, sections=sections)
    m.apply_translation([0, 0, z0 + h / 2])
    return m


def box(x0, x1, y0, y1, z0, z1):
    m = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return m


def make_collar(motor_d):
    depth = DEPTH[motor_d]
    bore_r = (motor_d + 2 * LINER_T + (CLEAR_18 if motor_d == 18 else CLEAR)) / 2
    r = bore_r + WALL
    top = FLOOR + depth
    body = cyl(r, top)
    cuts = [cyl(bore_r, depth + 1, FLOOR),                       # bore
            cyl(POCKET_DIA / 2, POCKET_D + 0.01, FLOOR - POCKET_D),   # screw-head pocket (under the bore)
            cyl(HOLE_DIA / 2, FLOOR + 2, -1)]                    # M12 clearance hole
    cuts.append(box(-NOTCH_W / 2, NOTCH_W / 2, -(r + 2), -(bore_r - 0.5), FLOOR, FLOOR + NOTCH_H))   # -Y notch (leads + vent)
    cuts.append(box(-NOTCH_W / 2, NOTCH_W / 2, bore_r - 0.5, r + 2, FLOOR, FLOOR + NOTCH_H))         # +Y notch (vent)
    cuts.append(box(-GROOVE_W / 2, GROOVE_W / 2, -(bore_r + GROOVE_D), -(bore_r - 0.5), FLOOR, top + 1))    # lead groove up the wall
    return boolean.difference([body] + cuts, engine="manifold")


def make_ring():
    tube = cyl(RING_OD / 2, RING_TUBE_H + RING_FL_T)
    flange = box(-RING_FL_X / 2, RING_FL_X / 2, -RING_FL_Y / 2, RING_FL_Y / 2, 0, RING_FL_T)
    ring = boolean.union([tube, flange], engine="manifold")
    cuts = [cyl(RING_ID / 2, RING_TUBE_H + RING_FL_T + 2, -1)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = cyl(RING_SCREW_D / 2, RING_FL_T + 2, -1, 24)
            h.apply_translation([sx * RING_SCREW_X, sy * RING_SCREW_Y, 0])
            cuts.append(h)
    return boolean.difference([ring] + cuts, engine="manifold")   # built flange-down, tube up = print orientation


def report(name, m):
    v = m.volume / 1000.0
    hrs = v * H_PER_CM3
    grams = v * 1.24 * 0.6
    ok_fit = all(e <= b for e, b in zip(sorted(m.extents), sorted(MK3_BED)))
    assert m.is_watertight and m.volume > 0, name + " not watertight"
    assert hrs < LIMIT_H, name + " over the 6 h library limit"
    assert ok_fit, name + " does not fit the MK3 bed"
    print("%-12s %7.1f cm3  %-18s watertight=%s  %.1f h  %3.0f g  LIBRARY" % (
        name, v, "x".join("%.0f" % e for e in m.extents), m.is_watertight, hrs, grams))
    return v, hrs, grams


def build_all():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for d in (18, 24, 29, 38):
        m = make_collar(d)
        m.export(os.path.join(OUT, "collar_%d.stl" % d))
        res["collar_%d" % d] = report("collar_%d" % d, m)
    m = make_ring()
    m.export(os.path.join(OUT, "ring.stl"))
    res["ring"] = report("ring", m)
    return res


if __name__ == "__main__":
    build_all()
