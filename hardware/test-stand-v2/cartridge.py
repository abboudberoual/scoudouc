"""Scoudouc Stand v2: LOAD-CELL CARTRIDGES (base plates + top platforms).

Run:  python3 cartridge.py     (writes stl/ files and prints a summary)

Standard (every cartridge):
  BOTTOM  SCP pattern: four M5 holes on a 20 x 60 mm rectangle, which lines up with the two inner T-slots of the
          two side-by-side 2040 "deck" rails.  Screw heads sit ON TOP of the plate (5 mm tall; the cell clears them).
  TOP     SCF flange: 56 x 56 mm platform, four M4 on a 40 x 40 mm square (same as the cups).
  PLUG    one GX12 4-pin panel socket (12.2 mm hole) in a wall on the +X edge.  Pin 1 E+ red, 2 E- black,
          3 S+ white, 4 S- green.
Origin (0,0) = the cup axis.  X across the deck, Y along the deck rails.

Parts:  plate_bar (5 kg and 50 kg bar cells), platform_bar, plate_s (200 kg S-type), platform_s.
!! Bar-cell hole pitch and body height are PARAMETERS (BAR_*): measure the cell you receive, edit, re-run.
!! The S-type cell height and M12 thread are parameters too (S_*).
PLA, LIBRARY printer (Prusa MK3), flat on the bed (underside down), no supports, 0.2 mm, 4 perimeters, 40% infill
.  Nothing here is within 15 mm of a motor
case (the cup and its card liner sit between), so no extra heat barrier is needed on the cartridge itself.
"""
import os
import trimesh
from trimesh import creation, boolean

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stl")
H_PER_CM3 = 0.062

PLATE_T = 8.0
PLATE_W = 60.0                 # across the deck (X)
SCP = [(-10, -30), (10, -30), (-10, 30), (10, 30)]      # four M5 on 20 x 60
SCF = [(-20, -20), (20, -20), (-20, 20), (20, 20)]      # four M4 on 40 x 40
PLAT = 56.0

# --- bar cell parameters (TAL220-style straight bar; CHECK against your cell) ---
BAR_W = 12.7
BAR_H = 12.7
BAR_HOLE_PITCH = 10.0        # distance between the two M5 holes at one end
BAR_FIXED_Y = 60.0           # fixed-end hole pair centre, measured from the free-end pair centre (at Y=0)
RISER_H = 8.0                # lifts the fixed end so the free end has 8 mm of air below it (clears screw heads)
STOP_GAP = 0.8               # overload stop pillar gap under the platform (mm)
PLAT_BAR_T = 10.0
# --- S-type parameters ---
S_H = 60.0                   # S-type body height between its two end faces (CHECK)
PLAT_S_T = 12.0


def box(x0, x1, y0, y1, z0, z1):
    m = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return m


def cyl(x, y, z0, z1, d, sections=48):
    m = creation.cylinder(radius=d / 2, height=z1 - z0, sections=sections)
    m.apply_translation([x, y, (z0 + z1) / 2])
    return m


def hexpocket(x, y, z0, z1, af):
    # hexagonal prism, across flats = af
    m = creation.cylinder(radius=af / 3 ** 0.5, height=z1 - z0, sections=6)
    m.apply_translation([x, y, (z0 + z1) / 2])
    return m


def gx12_wall(y_end):
    """Wall at the -Y end of the plate (outside the platform footprint), hole axis along Y."""
    wall = box(-11, 11, y_end, y_end + 5, PLATE_T, PLATE_T + 28)
    hole = creation.cylinder(radius=6.1, height=12, sections=48)
    hole.apply_transform(trimesh.transformations.rotation_matrix(1.5707963, [1, 0, 0]))
    hole.apply_translation([0, y_end + 2.5, PLATE_T + 14])
    return wall, hole


def plate_bar():
    y0, y1 = -40.0, 85.0
    parts = [box(-PLATE_W / 2, PLATE_W / 2, y0, y1, 0, PLATE_T)]
    pad = box(-14, 14, BAR_FIXED_Y - 15, BAR_FIXED_Y + 15, PLATE_T, PLATE_T + RISER_H)
    pillar_top = PLATE_T + RISER_H + BAR_H - STOP_GAP
    pillars = [box(sx * 24 - 3, sx * 24 + 3, -7, 7, PLATE_T, pillar_top) for sx in (-1, 1)]
    wall, whole = gx12_wall(y0)
    solid = boolean.union(parts + [pad] + pillars + [wall], engine="manifold")
    cuts = [whole]
    for x, y in SCP:   # M5 clearance holes
        cuts += [cyl(x, y, -1, PLATE_T + 1, 5.5)]
    for s in (-1, 1):  # cell fixed-end bolts from BELOW: 5.5 hole, 22 mm counterbore 4 deep for a fender washer
        y = BAR_FIXED_Y + s * BAR_HOLE_PITCH / 2
        cuts += [cyl(0, y, -1, PLATE_T + RISER_H + 1, 5.5), cyl(0, y, -1, 4, 22)]
    return boolean.difference([solid] + cuts, engine="manifold")


def platform_bar():
    solid = box(-PLAT / 2, PLAT / 2, -PLAT / 2, PLAT / 2, 0, PLAT_BAR_T)
    cuts = []
    for x, y in SCF:   # M4 with nut pocket (7.2 AF, 3.6 deep) in the underside
        cuts += [cyl(x, y, -1, PLAT_BAR_T + 1, 4.4), hexpocket(x, y, -1, 3.6, 7.2)]
    for s in (-1, 1):  # M5 into the cell free end, head recessed 10 x 6 from the top
        y = s * BAR_HOLE_PITCH / 2
        cuts += [cyl(0, y, -1, PLAT_BAR_T + 1, 5.5), cyl(0, y, PLAT_BAR_T - 6, PLAT_BAR_T + 1, 10)]
    return boolean.difference([solid] + cuts, engine="manifold")


def plate_s():
    y0, y1 = -50.0, 50.0
    boss_h = 8.0
    solid = box(-PLATE_W / 2, PLATE_W / 2, y0, y1, 0, PLATE_T)
    boss = cyl(0, 0, PLATE_T, PLATE_T + boss_h, 36.0)           # S-cell sits on this, M12 head pocket needs the depth
    wall, whole = gx12_wall(y0)
    solid = boolean.union([solid, boss, wall], engine="manifold")
    cuts = [whole, cyl(0, 0, -1, PLATE_T + boss_h + 1, 13.0), cyl(0, 0, -1, 9, 22.0)]   # M12 bolt, head pocket from below
    for x, y in SCP:
        cuts += [cyl(x, y, -1, PLATE_T + 1, 5.5)]
    return boolean.difference([solid] + cuts, engine="manifold")


def platform_s():
    solid = box(-PLAT / 2, PLAT / 2, -PLAT / 2, PLAT / 2, 0, PLAT_S_T)
    cuts = [cyl(0, 0, -1, PLAT_S_T + 1, 13.0), cyl(0, 0, PLAT_S_T - 8, PLAT_S_T + 1, 25.0)]  # M12, head recessed
    for x, y in SCF:
        cuts += [cyl(x, y, -1, PLAT_S_T + 1, 4.4), hexpocket(x, y, -1, 3.6, 7.2)]
    return boolean.difference([solid] + cuts, engine="manifold")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("%-14s %-8s %-18s %-10s %-8s %-9s" % ("part", "vol cm3", "size mm", "watertight", "print h", "filament g"))
    for name, fn in (("plate_bar", plate_bar), ("platform_bar", platform_bar),
                     ("plate_s", plate_s), ("platform_s", platform_s)):
        m = fn()
        m.export(os.path.join(OUT, name + ".stl"))
        v = m.volume / 1000.0
        hrs = v * H_PER_CM3
        assert m.is_watertight and m.volume > 0, name
        assert hrs < 6.0
        print("%-14s %-8.1f %-18s %-10s %-8.1f %-9.0f" % (name, v, "x".join("%.0f" % e for e in m.extents),
              m.is_watertight, hrs, v * 1.24 * 0.6))
    print("stack heights above the deck rail top: bar = %.1f mm, S = %.1f mm" % (
        PLATE_T + RISER_H + BAR_H + PLAT_BAR_T, PLATE_T + 8.0 + S_H + PLAT_S_T))


if __name__ == "__main__":
    main()
