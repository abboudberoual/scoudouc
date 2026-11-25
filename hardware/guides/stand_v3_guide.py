"""G-001: Thrust stand v3 assembly guide (the reference guide for the engine in guide.py).

Design of record: hardware/test-stand-v3/README.md (decision 007). This guide builds it with the parts
the owner actually has: VEVOR 2020 extrusion (10 x 1000 mm), a 0-50 kg S-type cell, NAU7802 ADC.
Geometry here is for illustration (plain 20 x 20 bars, block cell); dimensions in the text are the real ones.
Coordinates: z = 0 on the ground, origin on the stand's axis, +Y = rear (cell cable side), -Y = front (igniter side).
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cad"))
import cadquery as cq
from render import Part
from guide import Step

E, W = 20.0, 160.0
HALF, IN = W / 2, W / 2 - E          # 80, 60
H_UP = 483.0
PLATE_T = 3.2
PLATE_TOP = E + PLATE_T              # 23.2 above ground
CELL_H, CELL_W, CELL_T = 76.0, 51.0, 13.0
COLLAR_D, COLLAR_H, COLLAR_FLOOR = 32.0, 73.0, 18.0
MOTOR_D, MOTOR_L = 24.0, 70.0        # E12
BAR_TOP_H = 101 + MOTOR_L / 2        # ring rule from the README, above the plate top: 136 for an E12
BAR_TOP_Z = PLATE_TOP + BAR_TOP_H


def box(x0, y0, z0, x1, y1, z1):
    lo = (min(x0, x1), min(y0, y1), min(z0, z1)); hi = (max(x0, x1), max(y0, y1), max(z0, z1))
    return cq.Workplane("XY").box(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]).translate(
        ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))


def screw_head(x, y, z, axis):
    """M5 button head, 9.5 mm across, 2.8 mm tall, pointing along axis (+x,-x,+y,-y,+z,-z)."""
    d = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}[axis]
    return cq.Workplane(cq.Plane(origin=(x, y, z), xDir=(d[1], d[2], d[0]) if d[0] == 0 else (0, 1, 0), normal=d)).circle(4.75).extrude(2.8)


def bracket(face_axis, face_pos, run_axis, run_dir, along_axis, along_c, z_face, z_dir):
    """Inside-corner bracket in the corner between an upright face and a rail face.
    face_axis/face_pos: the upright face (x or y) and its coordinate; run_dir: direction along the rail away from the upright.
    z_face: rail face height the bracket sits on; z_dir: +1 bracket goes up from z_face, -1 down."""
    t, L, w = 3.0, 20.0, 18.0
    a0, a1 = along_c - w / 2, along_c + w / 2
    z0, z1 = z_face, z_face + z_dir * L
    f0, f1 = face_pos, face_pos + run_dir * L
    if face_axis == "x":
        vert = box(f0, a0, z0, f0 + run_dir * t, a1, z1)
        horz = box(f0, a0, z_face, f1, a1, z_face + z_dir * t)
        s1 = screw_head(f0 + run_dir * t, along_c, z_face + z_dir * 11, "+x" if run_dir > 0 else "-x")
        s2 = screw_head(f0 + run_dir * 11, along_c, z_face + z_dir * t, "+z" if z_dir > 0 else "-z")
    else:
        vert = box(a0, f0, z0, a1, f0 + run_dir * t, z1)
        horz = box(a0, f0, z_face, a1, f1, z_face + z_dir * t)
        s1 = screw_head(along_c, f0 + run_dir * t, z_face + z_dir * 11, "+y" if run_dir > 0 else "-y")
        s2 = screw_head(along_c, f0 + run_dir * 11, z_face + z_dir * t, "+z" if z_dir > 0 else "-z")
    return vert.union(horz).union(s1).union(s2)


P = {}
def add(name, shape, kind="purchased", **kw):
    P[name] = Part(name, shape, kind, **kw)

# --- extrusion -----------------------------------------------------------------------------------
for sx, side in ((-1, "left"), (1, "right")):
    x0 = sx * HALF; x1 = sx * IN
    add(f"Long rail, bottom {side}", box(x0, -HALF, 0, x1, HALF, E))
    add(f"Long rail, top {side}", box(x0, -HALF, E + H_UP, x1, HALF, 2 * E + H_UP))
for sy, side in ((-1, "front"), (1, "rear")):
    y0 = sy * HALF; y1 = sy * IN
    add(f"Short rail, bottom {side}", box(-IN, y0, 0, IN, y1, E))
    add(f"Short rail, top {side}", box(-IN, y0, E + H_UP, IN, y1, 2 * E + H_UP))
CORNERS = [(-1, -1, "front-left"), (1, -1, "front-right"), (1, 1, "rear-right"), (-1, 1, "rear-left")]
for sx, sy, c in CORNERS:
    add(f"Upright {c}", box(sx * HALF, sy * HALF, E, sx * IN, sy * IN, E + H_UP))
    xc, yc = sx * (HALF - E / 2), sy * (HALF - E / 2)
    # bottom: bracket on the long rail (against the upright's inner Y face) and on the short rail (inner X face)
    add(f"Bracket {c} bottom, long rail", bracket("y", sy * IN, "y", -sy, "x", xc, E, 1))
    add(f"Bracket {c} bottom, short rail", bracket("x", sx * IN, "x", -sx, "y", yc, E, 1))
    add(f"Bracket {c} top, long rail", bracket("y", sy * IN, "y", -sy, "x", xc, E + H_UP, -1))
    add(f"Bracket {c} top, short rail", bracket("x", sx * IN, "x", -sx, "y", yc, E + H_UP, -1))

# --- plate: 160 x 160 blank with an L notch at each corner, centre hole for the cell bolt, 8 x M5 ----
pl = cq.Workplane("XY").box(W, W, PLATE_T).translate((0, 0, E + PLATE_T / 2))
for sx, sy, _ in CORNERS:
    pl = pl.cut(box(sx * HALF, sy * HALF, E - 1, sx * IN, sy * (IN - E), E + 5))
    pl = pl.cut(box(sx * HALF, sy * HALF, E - 1, sx * (IN - E), sy * IN, E + 5))
HOLES = [(70, 25), (70, -25), (-70, 25), (-70, -25), (25, 70), (-25, 70), (25, -70), (-25, -70)]
for hx, hy in HOLES:
    pl = pl.cut(cq.Workplane("XY").circle(2.75).extrude(10).translate((hx, hy, E - 2)))
pl = pl.cut(cq.Workplane("XY").circle(6.5).extrude(10).translate((0, 0, E - 2)))
add("Plate (3.2 mm aluminium)", pl)

# --- cell, bolt, collar, disc, motor dummy ---------------------------------------------------------
cell = box(-CELL_T / 2, -CELL_W / 2, PLATE_TOP, CELL_T / 2, CELL_W / 2, PLATE_TOP + CELL_H)
cell = cell.cut(box(-CELL_T, -CELL_W / 2 + 10, PLATE_TOP + 12, CELL_T, CELL_W / 2 - 10, PLATE_TOP + 30))
cell = cell.cut(box(-CELL_T, -CELL_W / 2 + 10, PLATE_TOP + CELL_H - 30, CELL_T, CELL_W / 2 - 10, PLATE_TOP + CELL_H - 12))
add("S-type load cell, 50 kg", cell)
add("Hex bolt + fender washer (from below)", cq.Workplane("XY").polygon(6, 19).extrude(8).translate((0, 0, E - 8))
    .union(cq.Workplane("XY").circle(12).extrude(1.5).translate((0, 0, E - 1.5))))
cz = PLATE_TOP + CELL_H
collar = (cq.Workplane("XY").circle(COLLAR_D / 2).extrude(COLLAR_H).translate((0, 0, cz))
          .cut(cq.Workplane("XY").circle(26.4 / 2).extrude(COLLAR_H).translate((0, 0, cz + COLLAR_FLOOR)))
          .cut(box(-3, -COLLAR_D, cz + COLLAR_FLOOR, 3, -COLLAR_D / 2 + 2, cz + COLLAR_FLOOR + 10)))
add("Collar 24 mm (printed)", collar, "printed")
add("Aluminium disc 2 mm", cq.Workplane("XY").circle(12.5).extrude(2).translate((0, 0, cz + COLLAR_FLOOR)))
mz = cz + COLLAR_FLOOR + 2
add("Dummy motor 24 x 70 mm (dowel or spent casing)", cq.Workplane("XY").circle(MOTOR_D / 2).extrude(MOTOR_L).translate((0, 0, mz)), "motor")

# --- ring ladder, ring bars, guide ring --------------------------------------------------------------
rz1 = BAR_TOP_Z - E                      # ladder rail top = bar bottom
for sx, side in ((-1, "left"), (1, "right")):
    add(f"Ladder rail {side}", box(sx * HALF, -IN, rz1 - E, sx * IN, IN, rz1))
    for sy in (-1, 1):
        add(f"Bracket ladder {side} {'front' if sy < 0 else 'rear'}",
            bracket("y", sy * IN, "y", -sy, "x", sx * (HALF - E / 2), rz1 - E, -1))
for sy, side in ((-1, "front"), (1, "rear")):
    yc = sy * 46
    add(f"Ring bar {side}", box(-HALF, yc - E / 2, rz1, HALF, yc + E / 2, rz1 + E))
    for sx in (-1, 1):
        # bracket on the bar's inner side face, other leg in the ladder rail's top slot
        add(f"Bracket bar {side} {'left' if sx < 0 else 'right'}",
            bracket("y", yc - sy * E / 2, "y", -sy, "x", sx * (HALF - E / 2), rz1, 1))
ring = (cq.Workplane("XY").box(66, 116, 5).translate((0, 0, BAR_TOP_Z + 2.5))
        .union(cq.Workplane("XY").circle(33).extrude(20).translate((0, 0, BAR_TOP_Z - 15)))
        .cut(cq.Workplane("XY").circle(25).extrude(40).translate((0, 0, BAR_TOP_Z - 20))))
add("Guide ring (printed)", ring, "printed")

# --- pad eyes, ropes, stakes, ground -----------------------------------------------------------------
for sx, sy, c in CORNERS:
    x = sx * 45; y = sy * HALF
    eye = box(x - 16, y, 3, x + 16, y + sy * 2.5, 17).union(
        cq.Workplane("XZ").circle(6).circle(3.5).extrude(4).translate((x, y + sy * 6, 10)))
    add(f"Pad eye {c}", eye)
STAKE = 330
for sx, sy, c in CORNERS:
    p0 = cq.Vector(sx * 45, sy * (HALF + 6), 10)
    p1 = cq.Vector(sx * STAKE, sy * STAKE, 0)
    d = p1 - p0
    rope = cq.Workplane("XY").circle(2).extrude(d.Length)
    ax = cq.Vector(0, 0, 1); n = d.normalized()
    ang = math.degrees(math.acos(max(-1, min(1, n.dot(ax))))); ra = ax.cross(n)
    rope = rope.rotate((0, 0, 0), (ra.x, ra.y, ra.z), ang).translate((p0.x, p0.y, p0.z))
    add(f"Guy rope {c}", rope, "other")
    add(f"Stake {c}", cq.Workplane("XY").circle(4).extrude(140).rotate((0, 0, 0), (sy, -sx, 0), 30)
        .translate((sx * STAKE, sy * STAKE, -110)), "other")
add("Ground", cq.Workplane("XY").rect(820, 820).extrude(-2), "ground", alpha=0.35, frame=False)

# ------------------------------------------------------------------------------------------------------
names = lambda pred: [n for n in P if pred(n)]
corner = lambda c: [f"Upright {c}", f"Bracket {c} bottom, long rail", f"Bracket {c} bottom, short rail"]
BOTTOM_FRAME = ["Long rail, bottom left", "Long rail, bottom right", "Short rail, bottom front", "Short rail, bottom rear"]
TOP_FRAME = ["Long rail, top left", "Long rail, top right", "Short rail, top front", "Short rail, top rear"]
TOP_BR = names(lambda n: n.startswith("Bracket") and " top," in n)
LADDER = names(lambda n: n.startswith("Ladder rail") or n.startswith("Bracket ladder"))
BARS = names(lambda n: n.startswith("Ring bar") or n.startswith("Bracket bar"))
EYES = names(lambda n: n.startswith("Pad eye"))
FIELD = names(lambda n: n.startswith("Guy rope") or n.startswith("Stake")) + ["Ground"]
CENTRE = ["Plate (3.2 mm aluminium)", "S-type load cell, 50 kg", "Hex bolt + fender washer (from below)",
          "Collar 24 mm (printed)", "Aluminium disc 2 mm", "Guide ring (printed)", "Dummy motor 24 x 70 mm (dowel or spent casing)"]

M5 = "M5 x 10 button-head screw + M5 drop-in T-nut"
STEPS = [
    Step("Measure your load cell", ["S-type load cell, 50 kg"], show=["S-type load cell, 50 kg"], view=(15, -60), time="10 min",
         callouts=[("1", "S-type load cell, 50 kg")],
         do=["Read the label: write the <b>rated load</b> (50 kg = 490 N), the <b>sensitivity</b> (mV/V) and the <b>wire colours</b> in the table below.",
             "Measure the <b>height</b> end to end with calipers. The guide assumes 76 mm; every height above the cell moves by the difference.",
             "Find the <b>thread</b> in the two end holes: try an M12 bolt by hand first, then M10, then M8. Do not force it. This sets the two cell bolts you buy.",
             "Measure the <b>width of the flat end face</b> around the hole (the collar sits on it; assumed 30 mm).",
             "Send the four numbers to the project chat: the collar and the bolt list are regenerated from them."],
         parts=[(1, "S-type load cell (you have it)")], tools=["Calipers or ruler", "An M12 and an M10 bolt to test-fit"],
         check=["Table filled in", "Cell is marked <b>MAX 490 N, NO MOTOR ABOVE G</b> on the box and on the cell with tape"],
         warn=["Never load the cell sideways or drop it: a bent element reads wrong forever.",
               "A 50 kg cell takes up to G-class motors (1.5 &times; peak inside 490 N). The program only needs E and F."],
         extra_html="""<table><tr><th>Measured</th><th>Assumed in this guide</th><th>Yours</th></tr>
<tr><td>Rated load / sensitivity</td><td>50 kg (490 N) / about 2 mV/V</td><td></td></tr>
<tr><td>Height, end to end</td><td>76 mm</td><td></td></tr><tr><td>Thread in the end holes</td><td>M12</td><td></td></tr>
<tr><td>Flat end-face width</td><td>30 mm</td><td></td></tr><tr><td>Wire colours (E+, E&minus;, S+, S&minus;)</td><td>red, black, green, white (typical)</td><td></td></tr></table>"""),
    Step("Cut the extrusion", [], image="cutplan.png", time="60–90 min",
         do=["Pick four of your ten 1000 mm bars. Mark the cuts from <b>one end</b> with a square, measuring each piece from the last cut face, not from the first end (errors add up otherwise).",
             "Bars 1 and 2: two <b>483 mm uprights</b> each. Bar 3: six <b>160 mm</b> pieces (4 long rails + 2 ring bars). Bar 4: six <b>120 mm</b> pieces (4 short rails + 2 ladder rails).",
             "Cut square in a mitre box with a fine hacksaw (24 TPI or finer) or a chop saw with a non-ferrous blade. Clamp the bar; let the saw do the work.",
             "Deburr every cut with a file. File a <b>1 mm chamfer</b> on the ends that meet a bracket.",
             "Measure every piece and write the length on it with a marker. Uprights within &plusmn;0.5 mm of each other matter most: unequal uprights rack the frame."],
         parts=[(4, "2020 bars, 1000 mm (you have 10)")], tools=["Hacksaw + mitre box (or chop saw, non-ferrous blade)", "Square, tape, marker", "Flat file", "Clamp", "Safety glasses, gloves"],
         check=["4 &times; 483, 6 &times; 160, 6 &times; 120 mm, labelled", "The four uprights within 0.5 mm of each other", "No burrs: run a glove over every end"],
         warn=["Cut aluminium edges are sharp: gloves on until every end is filed."],
         tip="Keep the six spare bars: the swing rig (rung R2) and the gimbal fixture use them."),
    Step("Make the plate", ["Plate (3.2 mm aluminium)"], show=["Plate (3.2 mm aluminium)"], view=(55, -60), time="45 min",
         do=["Print <b>Appendix A</b> (the drilling template) at 100 % and check the 50 mm square with a ruler before you trust it.",
             "Tape the template to a 160 &times; 160 mm blank of 3.2 mm <b>6061-T6</b> (not hardware-store 3003: it bends). Centre-punch the 9 hole centres and scribe the four corner notches.",
             "Cut the four L-shaped corner notches (each 20 &times; 40 plus 40 &times; 20 mm) with a hacksaw or jigsaw. File the cuts and round the outside corners.",
             "Drill the eight <b>5.5 mm</b> holes. Drill the centre hole to <b>13 mm</b> for an M12 cell (11 mm for M10) with a step drill, or pilot 5 mm then open up.",
             "Deburr both faces of every hole."],
         parts=[(1, "Aluminium plate 3.2 mm 6061-T6, 160 &times; 160 (to buy)")], tools=["Centre punch, scribe", "Drill, 5 mm + 5.5 mm bits, 13 mm step drill", "Hacksaw or jigsaw, file"],
         check=["Plate lies on the bottom frame later with no corner touching an upright (checked in step 6)", "Holes deburred on both faces"],
         warn=["Clamp the plate to the drill table: a grabbing step drill spins thin plate."]),
    Step("Bolt the cell to the plate", ["S-type load cell, 50 kg", "Hex bolt + fender washer (from below)"],
         show=["Plate (3.2 mm aluminium)", "S-type load cell, 50 kg", "Hex bolt + fender washer (from below)"], view=(18, -60), time="10 min",
         callouts=[("1", "S-type load cell, 50 kg"), ("2", "Hex bolt + fender washer (from below)")],
         do=["Set the plate on two blocks so its underside is free.",
             "Stand the cell on the centre hole, <b>cable toward the rear</b> (+Y, the side with no notch in the collar later).",
             "From below: fender washer, then the <b>hex bolt</b> up through the plate into the cell's lower thread. Engage at least 1.5 &times; the bolt diameter (18 mm for M12) but do not bottom out.",
             "Snug it, about 10 N&middot;m (a firm one-hand pull on a short wrench). Hold the cell body, not the cable."],
         parts=[(1, "Hex bolt in your cell's thread, 25 mm (to buy)"), (1, "Fender washer (to buy)")], tools=["Wrench for the bolt head (19 mm for M12)"],
         check=["Cell stands square to the plate (check with a square on two sides)", "Bolt head stays under the plate's bottom face by less than 20 mm (the rails are 20 mm tall)"],
         warn=["Never clamp the cell's middle (the thin element) in a vise or with pliers."]),
    Step("Lay the bottom frame and screw the plate down", BOTTOM_FRAME, show=BOTTOM_FRAME + ["Plate (3.2 mm aluminium)", "S-type load cell, 50 kg"],
         view=(35, -55), time="20 min",
         do=["Slide <b>T-nuts into the top slots first</b>: 2 in each bottom rail for the plate. Into each <b>short</b> rail's <b>outer</b> slot add 2 more per end for the pad eyes (8 in all). Drop-in nuts can also go in later; roll-in nuts cannot.",
             "Lay the two <b>160 mm long rails</b> left and right, running front to back, and the two <b>120 mm short rails</b> between their ends.",
             "Lower the plate and cell onto the four rails. Line the eight plate holes up over the rail slots and slide the T-nuts under them.",
             "Screw the plate down with 8 &times; M5 &times; 10. Tighten in a cross pattern to about <b>4 N&middot;m</b> (firm with a short hex key, no more: the slot lips are 1.8 mm).",
             "The plate now holds the bottom frame square."],
         parts=[(2, "Long rails 160 mm"), (2, "Short rails 120 mm"), (8, M5), (8, "Extra M5 T-nuts for the pad eyes (step 13)")], tools=["3 mm hex key (button heads)", "Square"],
         check=["Diagonals of the bottom frame equal within 1 mm", "Plate flat on all four rails, no rocking"]),
    Step("First corner: upright and two brackets", corner("front-left"),
         show=BOTTOM_FRAME + ["Plate (3.2 mm aluminium)"] + corner("front-left"), zoom=["Bracket front-left bottom, long rail", "Bracket front-left bottom, short rail"], zoom_scale=3.2,
         view=(26, -40), time="10 min",
         callouts=[("1", "Upright front-left"), ("2", "Bracket front-left bottom, long rail"), ("3", "Bracket front-left bottom, short rail")],
         do=["Stand a <b>483 mm upright</b> on the end of the long rail, in the corner. Its outside faces are flush with the rail's end and outer side: every outside face of the stand is flat.",
             "Bracket <b>2</b> sits on the <b>long rail's top face</b> against the upright's inner face. One leg's T-nut goes in the upright's slot, the other in the rail's top slot.",
             "Bracket <b>3</b> sits on the <b>short rail's top face</b> against the upright's other inner face, the same way.",
             "Hold the upright square with a square on two faces and tighten the four screws to 4 N&middot;m."],
         parts=[(1, "Upright 483 mm"), (2, "Inside-corner bracket kits (bracket + 2 screws + 2 T-nuts)")], tools=["3 mm or 4 mm hex key (check your kit)", "Square"],
         check=["Upright square to the frame in both directions", "No gap under the upright"],
         tip="Turn each T-nut a quarter turn into the slot before tightening: with drop-in nuts you can feel it click square."),
    Step("The other three corners", corner("front-right") + corner("rear-right") + corner("rear-left"),
         show=BOTTOM_FRAME + ["Plate (3.2 mm aluminium)", "S-type load cell, 50 kg"] + names(lambda n: n.startswith("Upright") or (n.startswith("Bracket") and "bottom" in n)),
         view=(24, -52), time="20 min",
         callouts=[("1", "Upright front-right"), ("2", "Upright rear-right"), ("3", "Upright rear-left")],
         do=["Repeat step 6 at the other three corners: upright on the long rail's end, one bracket on the long rail, one on the short rail.",
             "Tighten every bracket only once all four uprights stand, then check square again."],
         parts=[(3, "Uprights 483 mm"), (6, "Bracket kits")], tools=["Hex key", "Square"],
         check=["All four uprights the same height (lay a straightedge across the tops)", "8 bottom brackets fitted"]),
    Step("Fit the ring ladder", LADDER, show=None, view=(22, -50), time="15 min",
         callouts=[("1", "Ladder rail left"), ("2", "Ladder rail right")],
         do=[f"The two <b>120 mm ladder rails</b> go between the front and rear uprights, left and right. Their <b>top</b> sits <b>{BAR_TOP_H - E:.0f} mm above the plate</b> for an E12 (the ring bars then sit on them with their top at {BAR_TOP_H:.0f} mm).",
             "One bracket under each rail end: one leg in the rail's bottom slot, one in the upright's inner slot (4 brackets).",
             "Set both rails at the same height with a spacer block cut to length, then tighten. All four screws sit in slots, so the whole ladder slides later for other motors."],
         parts=[(2, "Ladder rails 120 mm"), (4, "Bracket kits")], tools=["Hex key", "Spacer block or ruler"],
         check=["Both ladder rails level and at the same height (&plusmn;1 mm)"],
         extra_html=f"""<div class="box tip"><h4>Ring height rule (other motors)</h4>Ring bar top above the plate = 101 + motor length / 2 (mm), never below 125, and the ring's top at least 15 mm below the nozzle.
E12 (70 mm): bar top <b>{BAR_TOP_H:.0f}</b>, ladder rail top {BAR_TOP_H - E:.0f}. Re-check this rule once your cell height and collar are measured: it assumes a 76 mm cell.</div>"""),
    Step("Fit the ring bars", BARS, view=(30, -50), time="15 min",
         zoom=BARS + LADDER + ["Collar 24 mm (printed)"] + ["Upright front-left", "Upright rear-right"],
         callouts=[("1", "Ring bar front"), ("2", "Ring bar rear")],
         do=["Put <b>two M3 drop-in T-nuts in each bar's top slot</b> now (for the guide ring, step 12).",
             "Lay the two <b>160 mm ring bars</b> across the ladder rails, front and rear, <b>92 mm apart centre to centre</b> (72 mm clear between them), outer ends flush with the rails' outer faces.",
             "One bracket at each bar end on the bar's <b>inner</b> side face, the other leg in the ladder rail's top slot (4 brackets). Inner side keeps them clear of the ring flange."],
         parts=[(2, "Ring bars 160 mm"), (4, "Bracket kits"), (4, "M3 drop-in T-nuts")], tools=["Hex key", "Ruler"],
         check=["72 mm clear between the bars along their whole length", "Bars square to the ladder rails"]),
    Step("Fit the top frame", TOP_FRAME + TOP_BR, view=(28, -55), time="25 min",
         callouts=[("1", "Long rail, top left"), ("2", "Long rail, top right"), ("3", "Short rail, top front"), ("4", "Short rail, top rear")],
         do=["The two <b>160 mm long rails</b> sit on top of the uprights, left and right; the two <b>120 mm short rails</b> fit between them.",
             "Brackets go <b>under</b> the rails, against the uprights' inner faces: one on each long rail and one on each short rail at every corner (8 brackets).",
             "Tighten with the frame standing on a flat floor, so it settles square."],
         parts=[(2, "Long rails 160 mm"), (2, "Short rails 120 mm"), (8, "Bracket kits")], tools=["Hex key", "Square"],
         check=["Top-frame diagonals equal within 1 mm", "Push the top sideways: it springs back, no clicking joints (no diagonals in this frame, so some flex is expected)"]),
    Step("Fit the collar and the disc", ["Collar 24 mm (printed)", "Aluminium disc 2 mm"],
         show=["Plate (3.2 mm aluminium)", "S-type load cell, 50 kg", "Collar 24 mm (printed)", "Aluminium disc 2 mm"] + BOTTOM_FRAME,
         zoom=["S-type load cell, 50 kg", "Collar 24 mm (printed)", "Plate (3.2 mm aluminium)"], view=(20, -62), time="15 min",
         callouts=[("1", "Collar 24 mm (printed)"), ("2", "Aluminium disc 2 mm")],
         do=["Print <b>collar_24</b> for E12 (or <b>collar_29</b> for E16) from <code>hardware/test-stand-v3/stl/</code>: LIBRARY MK3, PLA, floor down, no supports, 0.2 mm layers, 4 perimeters, 40 % infill (about 1.6 h).",
             "Line the bore with a 1 mm kraft-card tube: that is the PLA heat barrier.",
             "Set the collar on the cell's top face, <b>notch toward the front</b> (&minus;Y). Drop the socket-head screw down the bore into the cell's top thread and tighten with a long hex key, <b>snug, about 5 N&middot;m</b> (a 5.5 mm PLA ledge carries it).",
             "Lay the 2 mm aluminium disc on the collar floor. The motor will stand on it."],
         parts=[(1, "Collar (printed)"), (1, "Socket-head screw in your cell's thread, 30 mm (to buy)"), (1, "Aluminium disc 2 mm, 25 mm across"), (1, "1 mm kraft card liner")],
         tools=["Long hex key (10 mm for M12)", "Scissors, glue stick for the liner"],
         check=["Collar does not rock on the cell", "Notch faces the open front"],
         warn=["The collar is a consumable: bin it if it is soft, warped or shiny after a burn."]),
    Step("Fit the guide ring", ["Guide ring (printed)"], zoom=["Guide ring (printed)"] + BARS, view=(38, -50), time="10 min",
         callouts=[("1", "Guide ring (printed)")],
         do=["Print <b>ring.stl</b>: LIBRARY MK3, PLA, flange down, 20 % infill (about 3.1 h).",
             "Set the flange on the two ring bars, tube hanging between them.",
             "Four M3 &times; 10 screws through the flange into the T-nuts you put in the bar slots in step 9. Snug only."],
         parts=[(1, "Guide ring (printed)"), (4, "M3 &times; 10 screws")], tools=["2.5 mm hex key"],
         check=["Ring centred over the collar: slide a card all the way round, 2 mm gap or more"]),
    Step("Fit the pad eyes", EYES, view=(18, -48), time="10 min",
         zoom=EYES + BOTTOM_FRAME,
         callouts=[("1", "Pad eye front-left"), ("2", "Pad eye front-right"), ("3", "Pad eye rear-right"), ("4", "Pad eye rear-left")],
         do=["One pad eye on the <b>outer face</b> of each short bottom rail, near each corner end (about 45 mm from the centre line).",
             "Two M5 &times; 10 each into the T-nuts you put in the outer slots in step 5, 4 N&middot;m."],
         parts=[(4, "Stainless pad eyes, 2-hole (to buy)"), (8, M5)], tools=["3 mm hex key"],
         check=["Eyes point outward and down; rope can run at 45&deg; to the corner"]),
    Step("Dry run with a dummy motor", ["Dummy motor 24 x 70 mm (dowel or spent casing)"], view=(22, -52), time="10 min",
         zoom=CENTRE + ["Upright front-left", "Upright rear-right"],
         callouts=[("1", "Dummy motor 24 x 70 mm (dowel or spent casing)")],
         do=["Stand a 24 mm dowel or a spent E12 casing (70 mm) on the disc, nozzle end up.",
             "Check the ring clears it all round and its top is at least 15 mm below the nozzle end.",
             "Lead routing rehearsal: igniter leads out of the collar notch, taped (not clamped) to the plate, out the <b>front</b>; cell cable out the <b>rear</b>. A 100 mm slack loop on each.",
             "With the DAQ connected (after the NAU7802 arrives, procedure 05): lift each lead; the zero must not move."],
         parts=[(1, "24 mm dowel or spent casing, 70 mm")], tools=["Card for the gap check", "Masking tape"],
         check=["Ring clears the dummy by 2 mm or more", "Ring top 15 mm or more below the nozzle end", "Leads exit front, cable exits rear, both with slack"]),
    Step("At the test site: guys, stakes, pull test", FIELD, view=(28, -50), time="20 min",
         callouts=[("1", "Guy rope front-left"), ("2", "Stake front-left")],
         do=["Drive a stake about <b>330 mm out on each diagonal</b>, leaning 45&deg; away from the stand.",
             "Tie a rope from each pad eye (bowline or figure-eight) to its stake (taut-line hitch or tent tensioner). Ropes nearly flat; snug, not banjo-tight.",
             "<b>Pull-test every stake</b> to 300 N (30 kg on a spring scale or a hanging bag). It must move less than 10 mm. If not, drive deeper or add a second stake in line.",
             "On ground that will not take stakes: two 10 kg sandbags on the bottom rails' outer ends (never on the plate). Good to G-class only.",
             "Then follow <code>docs/procedures/01-static-fire.md</code>. Nothing is fired until that procedure says so."],
         parts=[(4, "Guy ropes, 4 mm polyester, about 3 m each"), (4, "Stakes 300 mm"), (4, "Tensioners (optional)")], tools=["Mallet", "Spring scale or a 30 kg bag"],
         check=["Every stake pull-tested to 300 N", "Everyone 30 m back with the launch controller key out"],
         warn=["Static fires follow procedure 01 only: key out until clear, 5 s count, 60 s wait after a misfire, delay + 60 s after an ejection charge."]),
]

SHOP = [
    ("have", "2020 T-slot extrusion, 10 &times; 1000 mm (VEVOR)", "4 bars used", "78.17 paid"),
    ("have", "S-type load cell 0–50 kg", "1", "40.24 paid"),
    ("have", "NAU7802 24-bit ADC module (wiring: procedure 05, ticket T-022)", "1", "20.47 paid, arrives 1–7 Dec"),
    ("need", "Inside-corner bracket kit for 2020 / 6 mm slot, steel, each with 2 &times; M5 screws + 2 T-nuts", "24", "~31"),
    ("need", "M5 drop-in T-nuts for 2020 / 6 mm slot", "16 (pack of 20)", "~4"),
    ("need", "M5 &times; 10 button-head screws", "16 (pack of 20)", "~3"),
    ("need", "Aluminium plate 3.2 mm (1/8 in) <b>6061-T6</b>, 160 &times; 160 mm (offcut is fine)", "1", "~18"),
    ("need", "Stainless pad eyes, 2-hole, M5", "4", "~10"),
    ("need", "M3 &times; 10 screws + M3 drop-in T-nuts", "4 + 4", "~4"),
    ("need", "Cell bolts in <b>your cell's thread</b> (step 1): socket-head 30 mm + hex bolt 25 mm + 2 fender washers", "1 set", "~8"),
    ("need", "Aluminium disc 2 mm, about 25 mm across (flashing or a baking tray)", "1", "~3"),
    ("need", "Guy rope 4 mm polyester 12 m, 4 stakes 300 mm, 4 tensioners", "1 set", "~21"),
    ("print", "collar_24 (E12) and/or collar_29 (E16), guide ring: LIBRARY MK3, PLA", "2–3 jobs", "~2 filament"),
]
shop_rows = "".join(f'<tr><td class="{k if k != "print" else "have"}">{k.upper()}</td><td>{a}</td><td>{b}</td><td class="num">{c}</td></tr>' for k, a, b, c in SHOP)

COVER_LEFT = f"""<h3>What you are building</h3>
<p>The thrust stand for rung <b>R1</b> (static fires) and <b>R1b</b> (throttle test): a 160 &times; 160 &times; 523 mm aluminium tower copied from the BPS.space stand. The motor stands nozzle-up on a printed collar on one load cell; thrust goes straight down through the cell, the plate and the bottom rails into the ground.</p>
<p><b>15 steps, about 6 hours</b> of work plus printing. Steps 1–14 at home; step 15 at the test site.</p>"""
COVER_RIGHT = """<h3>How to read this guide</h3>
<p>Each step shows the stand so far: <span style="color:#E4572E"><b>red</b></span> is new in this step, <span style="color:#E8821A"><b>orange</b></span> is new and printed, grey is already fitted. Numbers in the picture match the list under it.</p>
<p>Do the <b>check box</b> at the end of every step before you go on. Torque everything M5 to about 4 N&middot;m: the slot lips are only 1.8 mm thick.</p>
<p>Design of record: <code>hardware/test-stand-v3/README.md</code> (decision 007).</p>"""

FRONT = [
    ("Before you start: what you have, what to buy, tools", f"""
<p>This guide uses the parts you already bought (extrusion, 50 kg cell, NAU7802), which differ from the README in two places: the cell is 50 kg instead of 100 kg (fine: the program fires E/F motors, the cell takes up to G), and the ADC is a NAU7802 instead of an ADS1220 (firmware port is T-022). Prices are estimates in CAD before tax; agents never buy, you do.</p>
<table><tr><th></th><th>Part</th><th>Qty</th><th class="num">CAD</th></tr>{shop_rows}
<tr><td></td><td><b>Still to buy for the mechanical build</b></td><td></td><td class="num"><b>~102</b></td></tr></table>
<h3>Tools</h3>
<p>Hacksaw and mitre box (or a chop saw with a non-ferrous blade) &middot; flat file &middot; square and tape &middot; calipers &middot; drill with 5 mm and 5.5 mm bits and a 13 mm step drill &middot; centre punch &middot; hex keys 2.5, 3, 4 and 10 mm &middot; wrench for the cell bolt (19 mm for M12) &middot; clamps &middot; safety glasses and gloves &middot; marker and masking tape.</p>
<h3>Safety while building</h3>
<p>Cut aluminium is sharp until filed. Clamp thin plate when drilling. No motor goes near the stand until step 15 and procedure 01.</p>"""),
]

BACK = [
    ("Appendix A — Plate drilling template (print at 100 %)", """<p>Print this page at <b>100 % / actual size</b> (no "fit to page"). Check the 50 mm square with a ruler first. Tape to the 160 &times; 160 blank, punch the 9 centres, scribe the notches.</p>
<img src="plate_template.png" style="width:180mm; display:block; margin: 4mm auto;">"""),
    ("Appendix B — Fasteners and torque", """<table><tr><th>Fastener</th><th>Where</th><th class="num">Count</th><th>Torque</th></tr>
<tr><td>M5 &times; 10 + T-nut (in bracket kits)</td><td>24 brackets</td><td class="num">48</td><td>about 4 N&middot;m</td></tr>
<tr><td>M5 &times; 10 + drop-in T-nut</td><td>plate to bottom rails</td><td class="num">8</td><td>about 4 N&middot;m</td></tr>
<tr><td>M5 &times; 10 + drop-in T-nut</td><td>pad eyes</td><td class="num">8</td><td>about 4 N&middot;m</td></tr>
<tr><td>M3 &times; 10 + drop-in T-nut</td><td>guide ring flange</td><td class="num">4</td><td>snug</td></tr>
<tr><td>Hex bolt (cell thread) + fender washer</td><td>cell to plate, from below</td><td class="num">1</td><td>about 10 N&middot;m</td></tr>
<tr><td>Socket-head screw (cell thread)</td><td>collar to cell top, through the PLA ledge</td><td class="num">1</td><td>about 5 N&middot;m, snug</td></tr></table>
<p>No torque wrench? "About 4 N&middot;m" on M5 is firm with a short hex key held at its short arm; stop when it stops turning easily.</p>
<h3>Build record</h3>
<table><tr><th>Item</th><th>Value / initials</th></tr><tr><td>Date built</td><td></td></tr><tr><td>Cell: height, thread, sensitivity</td><td></td></tr>
<tr><td>Upright lengths (4)</td><td></td></tr><tr><td>Bottom / top diagonals</td><td></td></tr><tr><td>Ladder rail top above plate</td><td></td></tr>
<tr><td>Collar printed (size, printer, date)</td><td></td></tr><tr><td>Stake pull test at site (N, movement)</td><td></td></tr>
<tr><td>Deviations from this guide</td><td></td></tr></table>
<h3>Revision log</h3><table><tr><th>Rev</th><th>Date</th><th>Change</th></tr><tr><td>A</td><td>2026-11-25</td><td>First issue, for the parts bought 21 Nov (50 kg cell, NAU7802)</td></tr></table>"""),
]

GUIDE = dict(id="G-001", title="Thrust stand v3 — assembly guide", rev="A", date="2026-11-25",
             subtitle="Scoudouc &middot; rung R1 static fires &middot; 2020 extrusion tower, 50 kg S-type cell, nozzle-up",
             parts=P, steps=STEPS, front=FRONT, back=BACK, cover_left=COVER_LEFT, cover_right=COVER_RIGHT,
             cover_hide=FIELD + ["Dummy motor 24 x 70 mm (dowel or spent casing)"], cover_view=(22, -55),
             pdf_name="G-001-thrust-stand-v3-assembly-guide-revA.pdf")
