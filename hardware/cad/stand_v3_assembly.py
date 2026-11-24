"""Stand v3 (2020 extrusion tower) as a 3D assembly, dims from hardware/test-stand-v3/README.md.

Run: python3 hardware/cad/stand_v3_assembly.py  → hardware/cad/renders/stand_v3-{iso,front}.png, .glb, .step
Not a drawing of record: the numbered callout drawing is hardware/test-stand-v3/assembly-callouts.png.
Geometry is simplified (extrusion as plain 20 mm bars, cell as a block) and good enough to see the layout.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq
from render import Part, render

HERE = os.path.dirname(os.path.abspath(__file__))
E = 20.0            # 2020 extrusion
W = 160.0           # tower footprint (outer)
H_UP = 483.0        # upright length
PLATE_T = 3.2
CELL = (76.0, 51.0, 12.7)   # S-type 50 kg, approx L x W x T (stands on its long edge)
CELL_H = 51.0
COLLAR_D, COLLAR_H = 46.0, 40.0
MOTOR_D, MOTOR_L = 24.0, 70.0   # E12 nozzle-up
RING_OD, RING_ID, RING_H = 70.0, 30.0, 12.0


def bar(x, y, z, dx, dy, dz):
    return cq.Workplane("XY").box(dx, dy, dz).translate((x + dx / 2, y + dy / 2, z + dz / 2))


parts = []
half = W / 2
# bottom frame (4 rails on the ground), uprights, top frame
for sx in (-half, half - E):
    parts.append(Part("Bottom rail", bar(sx, -half, 0, E, W, E)))
    parts.append(Part("Bottom rail", bar(-half, sx, 0, W, E, E)))
for sx in (-half, half - E):
    for sy in (-half, half - E):
        parts.append(Part("Upright", bar(sx, sy, E, E, E, H_UP)))
top_z = E + H_UP
for sx in (-half, half - E):
    parts.append(Part("Top rail", bar(sx, -half, top_z, E, W, E)))
    parts.append(Part("Top rail", bar(-half, sx, top_z, W, E, E)))
# plate (cross shape) on the bottom rails, cell on the plate, collar on the cell, motor in the collar
plate_z = E
plate = (cq.Workplane("XY").rect(W - 2 * E + 4, 60).extrude(PLATE_T)
         .union(cq.Workplane("XY").rect(60, W - 2 * E + 4).extrude(PLATE_T))).translate((0, 0, plate_z))
parts.append(Part("Plate 3.2 mm Al", plate))
cell_z = plate_z + PLATE_T
cell = cq.Workplane("XY").box(CELL[2], CELL[1], CELL_H).translate((0, 0, cell_z + CELL_H / 2))
parts.append(Part("S-type load cell", cell))
collar_z = cell_z + CELL_H
collar = cq.Workplane("XY").circle(COLLAR_D / 2).circle(MOTOR_D / 2 + 0.3).extrude(COLLAR_H).translate((0, 0, collar_z))
parts.append(Part("Collar (printed)", collar, "printed"))
motor = cq.Workplane("XY").circle(MOTOR_D / 2).extrude(MOTOR_L).translate((0, 0, collar_z + 8))
parts.append(Part("Motor E12 (nozzle up)", motor, "motor"))
# mid-height ring ladder: two rails across the tower at the motor's mid height, two bars, printed ring
ring_z = collar_z + 8 + MOTOR_L * 0.55
for sy in (-55, 35):
    parts.append(Part("Ring rail", bar(-half + E, sy, ring_z - E / 2, W - 2 * E, E, E)))
for sx in (-45, 25):
    parts.append(Part("Ring bar", bar(sx, -55, ring_z + E / 2, E, 110, E)))
ring = cq.Workplane("XY").circle(RING_OD / 2).circle(RING_ID / 2).extrude(RING_H).translate((0, 0, ring_z + E * 1.5))
parts.append(Part("Guide ring (printed)", ring, "printed"))
# guy ropes from bottom corners to stakes 600 mm out
for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
    p0 = cq.Vector(sx * (half - E / 2), sy * (half - E / 2), E / 2)
    p1 = cq.Vector(sx * 330, sy * 330, 0)
    d = p1 - p0
    rope = cq.Workplane("XY").circle(2).extrude(d.Length)
    axis = cq.Vector(0, 0, 1)
    ang = math.degrees(math.acos(max(-1, min(1, d.normalized().dot(axis)))))
    rot_axis = axis.cross(d.normalized())
    if rot_axis.Length > 1e-6:
        rope = rope.rotate((0, 0, 0), (rot_axis.x, rot_axis.y, rot_axis.z), ang)
    parts.append(Part("Guy rope", rope.translate((p0.x, p0.y, p0.z)), "other", frame=False))
    stake = cq.Workplane("XY").circle(5).extrude(120).translate((sx * 330, sy * 330, -100))
    parts.append(Part("Stake", stake, "purchased", frame=False))
ground = cq.Workplane("XY").rect(800, 800).extrude(-2)
parts.append(Part("Ground", ground, "ground", alpha=0.25, frame=False))

if __name__ == "__main__":
    out = render(parts, os.path.join(HERE, "renders"), "stand_v3",
                 views=(("iso", 22, -55), ("front", 6, -90), ("detail", 18, -40)),
                 title="Scoudouc stand v3 — 2020 tower, cell at the floor, motor nozzle-up (decision 007)")
    print(out)
