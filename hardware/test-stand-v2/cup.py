"""Scoudouc Stand v2: motor CUP FAMILY (18 / 24 / 29 / 38 mm), one flange standard (SCF).

Run:  python3 cup.py            (writes stl/cup_18mm.stl ... cup_38mm.stl and prints a summary)

SCF flange standard (same as v1, so v1 cups still bolt onto v2 cartridges):
  56 x 56 mm square, 8 mm thick, four M4 holes on a 40 x 40 mm square.
Every cup also has a round GUIDE BAND (54 mm across) so ONE aluminium guide ring (60 mm hole) fits all of them.

PLA, LIBRARY printer (Prusa MK3), flange on the bed, no supports (45 degree cones), 0.2 mm layers,
4 perimeters, 40% infill.  Card liner (1 mm kraft tube) is the heat barrier; fresh one every burn.
Cups are CONSUMABLES.  Print time is estimated from volume using the v1 cups as calibration
(v1 cups: about 0.062 h per cm3 of solid volume on an MK3; see README).
"""
import os
import numpy as np
import trimesh
from trimesh import creation, boolean

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stl")
H_PER_CM3 = 0.062          # calibrated on v1 cups: 3.2 h / 51.6 cm3 etc.

FLANGE = 56.0              # SCF flange width
PLATE_T = 8.0              # floor and flange thickness
BOLT_SQ = 40.0             # M4 holes on a 40 mm square
BOLT_D = 4.4
LINER_T = 1.0
CLEAR = 0.4
WALL = 3.0
BAND_D = 54.0              # guide band diameter (standard for all cups)
BAND_H = 6.0               # straight part of the band
BAND_Z = 15.0              # band starts this far above the floor top
LEAD_SLOT, LEAD_H = 7.0, 4.0
GROOVE_W, GROOVE_D = 4.0, 1.2

# motor diameter -> bore depth above the floor.  Rule: motor nozzle sticks out of the rim by 15 mm or more
# for the SHORTEST motor of the class (C6 is 70 mm long: 70-50 = 20; D12 70-55 = 15; 29 mm 98-65 = 33; 38 mm 130-85 = 45)
DEPTH = {18: 50.0, 24: 55.0, 29: 65.0, 38: 85.0}


def cyl(r, h, z0=0.0, sections=96):
    m = creation.cylinder(radius=r, height=h, sections=sections)
    m.apply_translation([0, 0, z0 + h / 2])
    return m


def box(x0, x1, y0, y1, z0, z1):
    m = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return m


def make_cup(motor_d):
    depth = DEPTH[motor_d]
    bore_r = (motor_d + 2 * LINER_T + CLEAR) / 2
    r = bore_r + WALL
    top = PLATE_T + depth
    rb = BAND_D / 2
    z0 = PLATE_T + BAND_Z                      # band bottom
    dz = rb - r                                # 45 degree cone height
    prof = [(0, PLATE_T), (r, PLATE_T), (r, z0 - dz), (rb, z0), (rb, z0 + BAND_H),
            (r, z0 + BAND_H + dz), (r, top), (0, top)]
    body = creation.revolve(np.array(prof, dtype=float), sections=96)
    flange = box(-FLANGE / 2, FLANGE / 2, -FLANGE / 2, FLANGE / 2, 0, PLATE_T)
    cup = boolean.union([body, flange], engine="manifold")
    cuts = [cyl(bore_r, depth + 1, PLATE_T)]                                   # bore, floor stays solid
    cuts.append(box(bore_r - GROOVE_D, bore_r + 1, -GROOVE_W / 2, GROOVE_W / 2, PLATE_T, top + 1))  # lead groove (+X)
    cuts.append(box(bore_r - GROOVE_D, rb + 5, -LEAD_SLOT / 2, LEAD_SLOT / 2, PLATE_T, PLATE_T + LEAD_H))  # lead notch (+X)
    cuts.append(box(-(rb + 5), -(bore_r - GROOVE_D), -LEAD_SLOT / 2, LEAD_SLOT / 2, PLATE_T, PLATE_T + LEAD_H))  # vent notch (-X)
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = cyl(BOLT_D / 2, PLATE_T + 2, -1, 24)
            h.apply_translation([sx * BOLT_SQ / 2, sy * BOLT_SQ / 2, 0])
            cuts.append(h)
    return boolean.difference([cup] + cuts, engine="manifold")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("%-6s %-9s %-20s %-10s %-9s %-10s" % ("cup", "vol cm3", "size mm", "watertight", "print h", "filament g"))
    for d in (18, 24, 29, 38):
        m = make_cup(d)
        m.export(os.path.join(OUT, "cup_%dmm.stl" % d))
        v = m.volume / 1000.0
        hrs = v * H_PER_CM3
        grams = v * 1.24 * 0.6                 # shells + 40% infill, rough
        assert m.is_watertight and m.volume > 0
        assert hrs < 6.0, "over the 6 h library limit"
        print("%-6s %-9.1f %-20s %-10s %-9.1f %-10.0f" % (d, v, "x".join("%.0f" % e for e in m.extents),
              m.is_watertight, hrs, grams))


if __name__ == "__main__":
    main()
