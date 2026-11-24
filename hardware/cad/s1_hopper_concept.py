"""Scoudouc 1 "Hop" concept, per decision 002 (option D: 3-inch kraft tube + printed internals) and 003 (C6 hop motor).

CONCEPT ONLY: dimensions from docs/program-roadmap.md and docs/mass-budget.csv; the gimbal is a placeholder
block until the Garrett-R16 files are checked (open item 1 of decision 002). No fins (TVC), parachute recovery,
no legs on S1.
Run: python3 hardware/cad/s1_hopper_concept.py → hardware/cad/renders/s1_hopper-{iso,front}.png, .glb, .step
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq
from render import Part, render

HERE = os.path.dirname(os.path.abspath(__file__))
TUBE_OD, TUBE_ID, TUBE_L = 78.0, 76.0, 400.0      # 3-inch kraft tube, S1 height 40 cm (roadmap)
NOSE_L = 110.0
GIMBAL_RING_H = 18.0                            # printed adapter ring: tube ID → gimbal mount
GIMBAL_BLOCK = (60.0, 60.0, 55.0)               # placeholder for the TVC mount
MOTOR_D, MOTOR_L = 18.0, 70.0                   # C6
SLEEVE_OD = 29.0                                # 29 mm gimbal bore → 18 mm motor sleeve (printed)
SLED_W, SLED_T, SLED_L = 60.0, 3.0, 150.0       # electronics sled (printed)
BULKHEAD_T = 4.0

parts = []
z0 = 0.0
# gimbal section hangs below the tube: motor + sleeve inside a placeholder gimbal block, ring joins it to the tube
gimbal = cq.Workplane("XY").box(*GIMBAL_BLOCK).translate((0, 0, z0 + GIMBAL_BLOCK[2] / 2))
gimbal = gimbal.cut(cq.Workplane("XY").circle(SLEEVE_OD / 2 + 0.5).extrude(GIMBAL_BLOCK[2]).translate((0, 0, z0)))
parts.append(Part("TVC mount (placeholder, Garrett-R16 class)", gimbal, "printed"))
sleeve = cq.Workplane("XY").circle(SLEEVE_OD / 2).circle(MOTOR_D / 2 + 0.3).extrude(MOTOR_L).translate((0, 0, z0 - 10))
parts.append(Part("Adapter sleeve 29→18 mm (printed)", sleeve, "printed"))
motor = cq.Workplane("XY").circle(MOTOR_D / 2).extrude(MOTOR_L).translate((0, 0, z0 - 15))
parts.append(Part("Motor C6", motor, "motor"))
ring_z = z0 + GIMBAL_BLOCK[2]
ring = cq.Workplane("XY").circle(TUBE_ID / 2 - 0.2).circle(TUBE_ID / 2 - 8).extrude(GIMBAL_RING_H).translate((0, 0, ring_z))
parts.append(Part("Gimbal adapter ring (printed)", ring, "printed"))
# body tube (purchased kraft) — cut away a quarter so the sled shows
tube_z = ring_z
tube = cq.Workplane("XY").circle(TUBE_OD / 2).circle(TUBE_ID / 2).extrude(TUBE_L).translate((0, 0, tube_z))
cutter = cq.Workplane("XY").box(TUBE_OD, TUBE_OD, TUBE_L * 0.55).translate((TUBE_OD / 2, -TUBE_OD / 2, tube_z + TUBE_L * 0.2 + TUBE_L * 0.275))
parts.append(Part("Body tube 3-inch kraft", tube, "purchased", alpha=0.35))
# bulkheads and electronics sled
for z in (tube_z + 30, tube_z + 200):
    bh = cq.Workplane("XY").circle(TUBE_ID / 2 - 0.2).extrude(BULKHEAD_T).translate((0, 0, z))
    parts.append(Part("Bulkhead (printed)", bh, "printed"))
sled = cq.Workplane("XY").box(SLED_W, SLED_T, SLED_L).translate((0, 0, tube_z + 34 + SLED_L / 2))
parts.append(Part("Electronics sled (printed)", sled, "printed"))
fc = cq.Workplane("XY").box(36, 8, 60).translate((0, SLED_T / 2 + 4, tube_z + 80))
parts.append(Part("Flight computer (placeholder)", fc, "other"))
batt = cq.Workplane("XY").box(30, 12, 50).translate((0, SLED_T / 2 + 6, tube_z + 150))
parts.append(Part("LiPo (placeholder)", batt, "other"))
# parachute bay marker + nose cone
chute = cq.Workplane("XY").circle(TUBE_ID / 2 - 6).extrude(80).translate((0, 0, tube_z + 260))
parts.append(Part("Parachute (packed)", chute, "other", alpha=0.6))
nose = (cq.Workplane("XZ").moveTo(0, 0).lineTo(TUBE_OD / 2, 0).threePointArc((TUBE_OD / 2 * 0.75, NOSE_L * 0.55), (0, NOSE_L)).close()
        .revolve(360, (0, 0, 0), (0, 1, 0))).translate((0, 0, tube_z + TUBE_L))
parts.append(Part("Nose cone (printed)", nose, "printed"))

if __name__ == "__main__":
    out = render(parts, os.path.join(HERE, "renders"), "s1_hopper",
                 views=(("iso", 18, -50), ("front", 4, -90)),
                 title="Scoudouc 1 'Hop' — concept per decisions 002 (3-inch tube + printed internals) and 003 (C6)")
    print(out)
