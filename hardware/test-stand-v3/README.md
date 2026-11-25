# Scoudouc Stand v3, 2020 extrusion version (thrust stand, C6 to I-class, about 600 N peak)

**Status: ACCEPTED 2026-11-24** (decision 007, T-007; built with the **50 kg** cell actually bought, 490 N ceiling, C to G: buy the 100 kg cell before I-class; replaces v2; **extrusion chosen by the owner** for durability and presentation). Recommended build **CAD 278.55**, reduced build **CAD 176.47** (see `costing.md`); the plywood version of the same stand was 192.35 / 117.35. Frame **2.8 kg**, whole stand about **4.3 kg** with cell, collar, rope and stakes. **Tower 160 x 160 x 523 mm, longest piece 483 mm**, 3.61 m of 2020 in four 1 m lengths.

**What it is:** a tall narrow aluminium tower, four uprights, a small square frame at the bottom and at the top and a ring ladder at mid-height. One S-type load cell stands on a 3.2 mm aluminium plate in the bottom frame with the motor standing on top of it, nozzle UP, in a printed collar. Thrust goes straight down: motor, collar, cell, **plate, bottom rails**, ground. Four guy ropes from the bottom corners to stakes hold it down. A printed ring on two bars at the motor's mid-height catches the motor if it tips. It does **not** fire the motor (a commercial launch controller does, see `electronics.md`). The DAQ box sits 2 m away on the ground (decision 005).

Drawing, every part numbered, PRINTED (orange) vs PURCHASED (navy): `assembly-callouts.png` (regenerate: `python3 drawing.py`). Frame proportions and layout follow the BPS.space stand (photo: still from a **BPS.space** video, supplied by the project lead; credit BPS.space).

## 0. What we copied, from whom (and where we departed)

| Photo | Channel | What we took from it |
|---|---|---|
| Tall narrow 2020 tower: four uprights, small square top and bottom frames, cell on a plate at the floor, boards along one upright, four guy wires to stakes, grass | **BPS.space** (video still, credited here) | **The whole shape**: tall and narrow, square top and bottom frames, cell at the floor on a plate, guy wires to ground stakes, T-slot mounting for everything else |
| Black 2020 extrusion box, cell on a plate in the bottom frame, printed ring held mid-height on two cross-bars | **Aero Propulsions** (video still) | Mid-height guide ring on two cross-bars; cell on the floor |
| Painted plywood frame, one S-type cell, printed cage, gravel | **Aero Propulsions** (video still) | One S-type cell; printed collar and cage; igniter leads out the side. (Plywood was the first v3; now the alternative, section 14.) |

| Departure | Why, in one line |
|---|---|
| Guys go to the **bottom corners**, not the top corners as on BPS | Owner's call, kept: a base pull goes straight into the bottom rails and never crosses the corner joints or the uprights |
| Mid-height **ring ladder** (two rails and two bars) | The BPS photo has no ring; the S-type cell takes side moments badly and a 360 mm motor on a 46 mm collar is a long lever; two bars and four bolts, and it never carries thrust |
| Steel corner brackets, not the printed ones in the Aero photo | Section 3: they carry the guy pull and the heat of the top frame, and 24 printed parts is 24 library jobs |
| 3.2 mm aluminium plate (cross shape) | Section 5: the 6 mm plywood insert fails the worst-case check |
| DAQ box on the ground 2 m away, not clipped to the frame (BPS) | Decision 005: electronics at least 1 m from the vent notches |
| S-type cell, not the pancake or column cell in the photos | Cheap (about CAD 38), one thread on both ends, takes a straight push through its middle |

## 1. Layout (mm, not to scale). Heights H are measured above the PLATE TOP (23.2 above the ground)

```
ELEVATION (front, cut at the axis)                  PLAN (looking down, 160 x 160)

   +---------------+  top rails 20 x 20, top = 523 above ground           +--+-----------+--+
   |   |       |   |  underside of top rails H=480 (24 over a 360 mm tip) |UP| short rail |UP|
   |   |       |   |                                                      +--+  ring flange +--+
   |   |  motor|   |  <- motor tip H=456 (foot 96 + 360)                  |  |  bar  (Y=-46)  |
   |   |  [===]|   |                                                      |LR|  (collar)    |LR|  LR = long rail
 --|---|-ring--|---|-- ring bars (20 x 20), top H=281 = mid-height        |  |  bar  (Y=+46)  |  UP = upright
   |   |  coll |   |  collar 76..179, disc top 96                         +--+  short rail +--+
   |   |  cell |   |  cell 0..76                                                (plate under it,
 ==+===+=plate=+===+== plate 3.2 mm; bottom rails 20 x 20 under it                cross-shaped)
 stake ~~guy~~     ~~guy~~ stake   (pad eyes on the bottom short rails)
```

Joint layout: the four **uprights stand ON the ends of the two long bottom rails** and **hang UNDER the ends of the two long top rails**; the two short rails of each frame fit between the long rails. Every outside face is flat. Each of the 8 frame corners has **two inside-corner brackets**: one between the upright and the long rail, one between the upright and the short rail.

**Ring height rule:** bar top H = 101 + (motor length in mm) / 2, so the ring sits at the motor's mid-height; never below 125 (bar bottoms stay 5 mm over the vent notches) and ring top (bar top + 5) at least 15 mm below the nozzle plane (H = 96 + motor length). For a 360 mm 38 mm I motor: bar top **H 281**. For a C6 (70 mm): 136. To move the ring: loosen the eight M5 screws that hold the ladder rails' brackets, slide the ladder (all T-nuts slide in the upright slots), tighten. Cell height assumed 76 mm: **measure yours**; if it differs, shift every H above the cell by the difference.

## 2. Extrusion cut list (2020, 20 x 20 mm, T-slot, anodised black or silver)

| Part | Length (mm) | Qty | Notes |
|---|---|---|---|
| Upright | **483** | 4 | **Longest piece.** Stands from 20 to 503 above the ground |
| Long rail | 160 | 4 | 2 bottom (under the uprights), 2 top (over the uprights), run front to back |
| Short rail | 120 | 4 | 2 bottom, 2 top, between the long rails |
| Ring ladder rail | 120 | 2 | between the uprights, left and right, at ring height |
| Ring bar | 160 | 2 | lie on the ladder rails, 92 mm apart centre to centre (72 mm clear between them) |
| **Total** | **3.612 m** | 18 pieces | order **4 x 1 m**: two give 2 uprights each (969 mm with kerf), one gives 6 x 160 (975), one gives 6 x 120 (735). 0.39 m left over |

Cut square (a mitre box and hacksaw, or have the supplier cut: ask for 0.2 mm squareness); allow a 3 mm kerf; deburr every cut and **file a 1 mm chamfer on the rail ends that carry brackets**. Extrusion price is the least certain number here (16 per metre assumed).

## 3. Corner joints: printed vs steel brackets (priced both)

24 brackets: 8 bottom, 8 top, 4 ring ladder, 4 ring bars. All are standard 2020 inside-corner (angle) brackets, one M5 screw and T-nut per leg.

| | Steel kit (recommended) | Printed PLA (`bracket.py`, `stl/bracket.stl`) |
|---|---|---|
| Per bracket | 1.30 with its 2 screws and 2 T-nuts | 0.13 filament + hardware from two 100-packs |
| 24 brackets with all their hardware | 31.20 + packs 7 = **38.20** | 3.12 + packs 22 = **25.12** |
| Difference | | saves **CAD 13.08** |
| Print | none | 4.8 g, 0.24 h (14 min) each on an MK3; solid; one leg flat, no supports; **LAB**, all 24 on one plate (about 6 h), or LIBRARY, one part per job (24 jobs) |
| Strength | steel, T-nut limited | PLA, creeps under steady load, softens near heat |
| Where it matters | | 4 bottom corners carry the guy pull (about 190 N each); top-frame brackets sit 24 to 44 mm over the nozzle plane; the ring catch load puts about 285 N on one bracket screw |

**Recommendation: steel.** **Printed brackets carry no thrust here**: thrust goes cell, plate, bottom rails, ground, and no bracket is in that path. They do carry the guy pull and the ring-catch load, and the top frame sits just above the plume, and those are the reasons, plus 24 library jobs, not the CAD 13. If you have lab access and want the cheaper stand, printed brackets are acceptable for the **ring ladder (8)** at once, and for all 24 once you have pulled a stake test and fired a few cheap motors; the reduced total in `costing.md` takes them all.

## 4. T-nuts and M5 count

| Fastener | Count | Where |
|---|---|---|
| M5 screws | **64** | 48 in the 24 brackets, 8 holding the plate to the bottom rails, 8 in the four pad eyes |
| M5 T-nuts (drop-in or roll-in, steel) | **64** | one per screw, same places |
| M3 x 10 screws + M3 drop-in T-nuts | 4 + 4 | ring flange to the ring bars |
| M12 | 1 SHCS 30, 1 hex bolt 25, 2 fender washers | collar to cell top; cell to plate from below |

The steel kit includes 48 screws and 48 T-nuts; items 3 and 4 in the BOM (packs of 20) cover the plate and pad eyes. **Preload every T-nut before the rails are joined**: drop-in nuts can be dropped in from the top slot; roll-in nuts must be slid in from a rail end, so put them in before you fit the second rail. Torque M5 to about 4 N-m, **no more** (the lips are 1.8 mm).

## 5. The cell plate: 3.2 mm aluminium (picked) vs 6 mm plywood insert

**Picked: 3.2 mm (1/8 in) 6061-T6 aluminium, 160 x 160 blank with the four corners cut as L-shaped notches, so it is a cross.** It rests on the **top faces of the four bottom rails**; the notches leave the corner brackets and uprights clear. Eight M5 x 10 screws (two per rail, through the plate into T-nuts in the top slots) hold it; the cell stands in the middle on one M12 hex bolt from below (the head sits in the 20 mm gap under the plate, which is open to the ground).

Notch each corner: remove 20 x 40 and 40 x 20 mm rectangles that share the corner square (an L, 1200 mm2 each). Cut with a hacksaw or jigsaw, file, round the corners.

| Plate | Worst case (only two opposite rails touch it, 780 N at the centre, span 140 mm) | Four rails touching (normal) |
|---|---|---|
| **3.2 mm 6061-T6** | 127 MPa, **SF 1.9** against 240 MPa yield; sag 1.9 mm | sag about 0.9 mm |
| 6 mm plywood (20 MPa along the grain) | 36 MPa, **SF 0.55: fails** | (not relied on) |

Justification: the plywood insert fails the same case that aluminium passes, it scorches, and aluminium takes the pad-eye side loads in the screws. Cost 18 (a 160 mm square blank; a makerspace offcut is free). **Specify 6061-T6** (or 5052-H32 at about SF 1.5): the common hardware-store 3003 sheet is much softer, and at SF 1 it would take a permanent bend.

## 6. How the ring bars clamp into the T-slots

- The **ladder rails** (120) sit between the front and back uprights at ring height and are held by **one inside-corner bracket per end** under the rail: one leg in the rail's bottom slot, one leg in the upright's inner slot. All four screws sit in slots that slide, so the whole ladder moves up and down.
- The **ring bars** (160) lie **across the top faces of the two ladder rails** (a cross, like a ladder's rungs), outer faces flush with the rails' outer faces. Each bar end is held by **one bracket on the bar's inner side face**, whose other leg is in the rail's top slot (4 brackets in all). Brackets are on the inner side so they clear the ring flange and the rail ends.
- The ring's flange then lies on the two bars' top faces: **four M3 x 10 screws** go through the flange's 3.5 mm holes into **M3 drop-in T-nuts in the bars' top slots** (X = plus or minus 12, Y = plus or minus 45, about 1 mm off each slot's centre).
- Load directions: a sideways push **across** the slot is carried positively (the screw shank bears on the slot lip); a push **along** the bar is carried by friction of the four M3 T-nuts only (SF 8.9, section 7). The ring never carries thrust.

## 7. Hand check at 600 N (`handcheck.py`)

**What carries the thrust:** motor, collar, cell, **plate, the two bottom rails it rests on**, ground. Brackets and screws carry none of it. They carry the guy pull, the ring-catch load and the frame's own weight.

**Assumptions (conservative):** peak 600 N; ignition overshoot 1.3 (design **780 N**); 6063-T5 yield 110 MPa; 2020 section I = 6000 mm4, Z = 600 mm3 (data sheets say 6000 to 7000 mm4); E = 69 GPa; sideways load 15% of peak = **90 N**; hold-down 3 x 90 = **270 N**; M5 drop-in T-nut pull-out 1000 N (assumed, derated); pad eye break 1000 N in plane (assumed); rope 4 mm polyester 1 kN, 60% at a knot; stake 300 N (assumed).

| Member | Result | Margin |
|---|---|---|
| **Bottom frame rails under the plate** (worst case: two long rails take 390 N each at mid-length, rail held only at its ends, 150 mm clear) | 24 MPa, deflection **0.07 mm** | **SF 4.5** |
| **Plate** (section 5) | 127 MPa two-edge worst case | **SF 1.9** |
| **Guy attachment**: pad eye on the outer face of a bottom short rail at the corner end, two M5 screws in two T-nuts, rope at 45 degrees in plan, 270 N | 191 N pull out of the face + 191 N along the face. Tipping the eye (15 mm high, screws 30 mm apart) adds 95 N, so **peak 191 N per screw** | T-nut pull-out **SF 5.2**; pad eye **SF 3.7** |
| Guy along-rail part (191 N) | The T-nut stops against the long rail's inner face (7.6 MPa); the reaction goes to the long and short rails, then into the brackets across their slots (lip bearing 21 MPa) | fine; steel brackets |
| **Ring screws in shear** (90 N, 4 x M3) | 22 N each, 4.2 MPa on the lip | SF 24; **along the slot (friction only) SF 8.9** |
| Ring bars (45 N each at mid-span, 140 mm) | 2.6 MPa | SF 42 |
| Uprights if they took the whole 90 N as cantilevers (ring at its highest, 304 above ground) | 11 MPa | SF 9.6 |
| Ring catch load on one bracket screw (285 N pull) | T-nut 1000 N | **SF 3.5** (steel; PLA is the reason to stay with steel) |
| M12 bolt in shear at 270 N | 40 kN | SF 150 |
| Guy rope, worst case one rope takes all 270 N | 4 mm polyester | **SF 2.2** |
| **Stake**, 300 mm in firm soil | assumed 300 N | **SF 1.1: prove it** (section 12) |

**Result: PASS on paper; the plate (SF 1.9 in an unlikely case), the stake and the rope are the weak links.** Not checked: frame racking stiffness (not a load path for thrust; no diagonals, so expect it to flex visibly if you push the top), real extrusion section properties, real T-nut and pad-eye strengths, PLA creep, anything but vertical thrust.

**Frame mass 2.8 kg** (extrusion 1.88, brackets 0.36, plate 0.18, T-nuts, screws and pad eyes 0.38); with cell, collar, ring, disc, M12 kit, rope and stakes **about 4.3 kg**. **Longest piece 483 mm**, so it fits in a car boot assembled: 160 x 160 x 523 mm.

## 8. The cell: one 100 kg S-type, M12 (CZL301 type)

| Cell | Rated | 600 N peak (61% / 80% with the 1.3 overshoot) |
|---|---|---|
| 50 kg | 490 N | **overloaded** at the overshoot (159%). Rejected. |
| **100 kg** | 981 N | 61% at peak, **80% with the overshoot**, and 900 N (1.5 x peak) is inside 981 N. Smallest that survives an I. |
| 200 kg | 1962 N | survives, but doubles the error at the small end |

**Why one cell is enough from C6 to I:** accuracy is a percentage of full scale, so the **absolute** error is about the same for every motor (about 0.3 N), and that only matters below E. The ADC is not the limit: a 24-bit ADC at gain 128 gives about 2.1 million counts across the cell's range, so one count is **0.46 mN** (about 0.003% of a C6 peak). The limit is the cell's own error and noise.

**C6 resolution you get** (estimates; assumptions in `handcheck.py`): C6 peak about 14 N is **1.4% of the cell's range**. Noise about **0.09 N rms** per sample at 1000 samples/s (assumed 0.6 uV rms; read the ADS1220 data sheet), **0.03 N rms** if you average 10 samples. Cell error about **0.3 N** (assumed 0.03% of full scale, typical; read the data sheet), which is **2% of the C6 peak** and about **6% of its 5 N plateau**. **Acceptable** for what a first stand is for (curve shape, burn time, peak within a few %, total impulse within about 6%) but **not** for certified numbers. **Calibrate with small masses** (0.5 to 2 kg, see `electronics.md`) to remove gain error at the low end. If you need better, see the 5 kg swap below.

**Later, for better small-motor resolution (no cartridge system):** a 5 kg S-type (49 N rated, error about 0.015 N, 0.1% of a C6 peak) can go in the same place on the same two bolts. Check its thread (often M6, **check the data sheet**): the plate hole (13 to 14 mm) and collar hole (13.5 mm) take an M6 bolt with an 18 mm washer (ISO 7093). **A 5 kg cell must never see more than about 30 N (motors up to E-class at most); an I destroys it. Write that on the cell box.** The 5 kg cell is swapped by hand when you change motor class.

## 9. Printed collar family and guide ring (`collar.py`, run it to regenerate `stl/`)

| Part | Bore | Depth | Size | Print (MK3, estimated) | Filament |
|---|---|---|---|---|---|
| collar_18 | 21.4 | 50 | 26 x 26 x 68 | 1.0 h | 12 g |
| collar_24 | 26.4 | 55 | 32 x 32 x 73 | 1.6 h | 19 g |
| collar_29 | 31.4 | 65 | 37 x 37 x 83 | 2.2 h | 27 g |
| collar_38 | 40.4 | 85 | 46 x 46 x 103 | 3.7 h | 45 g |
| ring | ID 50, OD 66 | tube 15 + flange 5 | 66 x 116 x 20 | 3.1 h | 37 g |

All **LIBRARY** (Prusa MK3), PLA, floor/flange **down** on the bed, no supports, 0.2 mm layers, 4 perimeters, collars 40% infill (ring 20%). Times are estimated from volume at 0.062 h per cm3 (v2 calibration, solid, so conservative); confirm in the slicer. All five are watertight (tested).

**How a collar works:** it sits on the cell's top boss and is held by **one M12 socket-head screw** that threads into the cell's own M12 hole; the head sits in a pocket in the collar floor and is tightened with a hex key down the bore (a 5.5 mm PLA ledge under it: tighten **snug, about 5 N-m, no more**). A 2 mm aluminium disc (decision 005) lies on the floor and the motor stands on the disc. A 1 mm kraft-card liner tube in the bore is the **PLA heat barrier** (CLAUDE.md rule); the collar is a **consumable**, bin it if soft, warped or shiny, and do not use PLA for burns over about 3 s without trying a cheap motor first. Depth rule (from v2): the shortest motor of each class sticks out of the rim by 15 mm or more so the jet never touches PLA (C6 70 mm in 50, D12 70 in 55, a 98 mm 29 mm motor in 65, a 130 mm 38 mm motor in 85). **Measure your cell's top boss and thread** (assumed M12, 30 mm wide top face) and edit the parameters at the top of `collar.py` if they differ.

**The ring** rests on the two 2020 ring bars (flange on the bar tops, held by four M3 screws, tube hanging between them) and never touches anything in normal use. ID 50 mm lets the 46 mm 38-mm collar pass through (2 mm gap), the bare 38 mm motor has 6 mm each side, an 18 mm one 16 mm. After a burn look for scuff marks inside the ring: they mean the thrust was off-axis. It is within 15 mm of a case at its tightest, so the **air gap and the collar wall are its heat barrier**; it is consumable too.

## 10. Igniter leads and cable routing

- Leads leave through the collar's **-Y notch**, down its lead groove (4 mm wide) to the plate, then across the plate and straight out the **open front** of the frame (the plate's arm reaches the front rail; deburr its edge). The +Y notch is a second vent.
- Leave a **100 mm slack loop** between the collar and the first tape point on the plate. Tape (do not clamp) the leads to the plate. A tight lead pushes on the collar and reads as thrust.
- The cell cable leaves the cell toward the **rear** (+Y), with its own slack loop, taped to the plate, then 3 m to the DAQ box. Igniter leads and cell cable go out opposite sides and cross, if at all, at 90 degrees, at least 1 m from the stand.
- Nothing may touch the collar or the cell except the screw and the motor. After taping, check the zero does not change when you lift a lead.

## 11. Ejection-charge handling (decision 005)

The delay motor's ejection charge fires at the forward end, which is the **bottom** of the nozzle-up motor, into the collar floor. Mitigations: the 2 mm aluminium disc on the floor; two vent notches at the foot (+Y, -Y) that point the puff out the open front and back, and the lowest ring-bar position keeps the bar bottoms **5 mm above** the notch top (bar top at 125 or higher) so the puff passes under them; the puff hits bare aluminium uprights, not plywood; prefer **plugged or zero-delay motors** for stand tests; the DAQ box stays at least 1 m (we use 2 m) from the notches; expect one extra downward pulse in the data after the delay; wait **delay time plus 60 s** before approaching.

## 12. Hold-down: guys and stakes (sized to 3 x 15% of peak sideways)

Thrust pushes the stand into the ground; the hold-down is for the sideways part (misaligned thrust, a tugged cable, wind). 15% of 600 N = 90 N; x3 = **270 N**. Own mass (about 4.3 kg) is no help.
1. Four 4 mm polyester ropes, one from each base-corner pad eye (section 7) to a stake about 330 mm out on the diagonal, each stake driven at 45 degrees leaning **away** from the stand; ropes tied with a figure-eight or bowline at the pad eye and a taut-line hitch (or a tent tensioner) at the stake. Ropes nearly flat on the ground.
2. Worst case (push along a diagonal) one rope takes all **270 N**. Rope SF 2.2 with a knot; stake SF 1.1 **on an assumed 300 N per stake**.
3. **Pull-test every stake before the first burn at each site:** hang 30 kg (300 N) or pull with a spring scale to 300 N; it must not move more than 10 mm. If it fails, drive it deeper, add a second stake in line, or do not fire above G.
4. **Sandbag option on ground that will not take stakes:** two 10 kg bags on the bottom rails' outer ends (never on the plate) plus the stand: about 235 N of weight, friction about 94 N at mu 0.4 (assumed). That covers up to a **G** (120 N peak: 54 N design). **I-class needs stakes.**

## 13. Safety distances and procedure

Follow `docs/procedures/01-static-fire.md`: key out until clear, key in, momentary fire switch, 5 s countdown, 60 s misfire wait; **everyone at least 30 m** from the stand with the lead wire fully extended. I suggest **50 m for H and I** (my suggestion, not a source). Clear-area minimums in procedure 01: C 120 m, D 150 m, E and F 300 m, so E and above need a club (CQF) launch day or written landowner permission. I-class static tests I did not research beyond this: check club and regulatory rules first. Firing is never done from the DAQ box. **Do not skip the build order below.**

## 13b. Parts
Numbers match `assembly-callouts.png` and `bom.py` (CAD, before 15% Quebec tax; estimates, unchecked against current listings).

| # | Part | Kind | Qty | CAD | Source |
|---|---|---|---|---|---|
| 1 | 2020 T-slot aluminium extrusion, 1 m lengths (3.61 m used, cut list in README) | PURCHASED | 4 | 64.00 | Amazon.ca / Misumi CA / local (about 16 per metre: check) |
| 2 | Inside-corner bracket kit, steel, 2020 (bracket + 2 M5 screws + 2 T-nuts each) | PURCHASED | 24 | 31.20 | Amazon.ca / AliExpress CA |
| 3 | M5 drop-in T-nuts, pack of 20 (16 used: plate 8, guys 8) | PURCHASED | 1 | 4.00 | Amazon.ca |
| 4 | M5 x 10 button-head screws, pack of 20 (16 used) | PURCHASED | 1 | 3.00 | Amazon.ca / Princess Auto |
| 5 | Aluminium plate 3.2 mm (1/8 in) 6061-T6, 160 x 160 blank, owner cuts the corners | PURCHASED | 1 | 18.00 | Metal Supermarkets / Princess Auto |
| 6 | Stainless pad eye (eye plate), 2 holes, M5 screws (guy anchor) | PURCHASED | 4 | 10.00 | Canadian Tire / marine store |
| 7 | M3 x 10 screws + M3 drop-in T-nuts (4 each) for the ring | PURCHASED | 1 | 4.00 | Amazon.ca |
| 8 | S-type load cell 100 kg, M12 thread | PURCHASED | 1 | 38.00 | Amazon.ca (CZL301 type) |
| 9 | M12 hardware: SHCS 30 mm, hex bolt 25 mm, 2 fender washers | PURCHASED | 1 | 8.00 | Princess Auto / Home Depot |
| 10 | Aluminium disc 2 mm (cut from flashing or a baking tray) | PURCHASED | 1 | 3.00 | Home Depot / Dollarama |
| 11 | Guy rope, 4 mm polyester, 12 m | PURCHASED | 1 | 7.00 | Canadian Tire |
| 12 | Rope tensioner (tent type) | PURCHASED | 4 | 4.00 | Canadian Tire / MEC |
| 13 | Ground stake 300 mm, steel | PURCHASED | 4 | 10.00 | Canadian Tire / RONA |
| 14 | ADS1220 24-bit ADC breakout | PURCHASED | 1 | 35.00 | ProtoCentral / Amazon.ca |
| 15 | microSD module + 32 GB card | PURCHASED | 1 | 16.00 | Amazon.ca / RobotShop CA |
| 16 | Cell extension: 3 m shielded 4-core cable + GX12 4-pin pair | PURCHASED | 1 | 10.00 | Amazon.ca / DigiKey CA |
| 17 | Button, LED, resistors, perfboard, wire, capacitors, box | PURCHASED | 1 | 8.00 | RobotShop CA / DigiKey CA |
| 18 | ESP32-S3 board (already owned) | PURCHASED | 1 | 0.00 | owned |
| 19 | Collar 18 mm (collar.py) | PRINTED | 1 | 0.30 | own filament, LIBRARY |
| 20 | Collar 24 mm | PRINTED | 1 | 0.50 | own filament, LIBRARY |
| 21 | Collar 29 mm | PRINTED | 1 | 0.70 | own filament, LIBRARY |
| 22 | Collar 38 mm | PRINTED | 1 | 1.10 | own filament, LIBRARY |
| 23 | Guide ring (ring.stl) | PRINTED | 1 | 0.95 | own filament, LIBRARY |
| 24 | Spare collars (one more each of 29 and 38) | PRINTED | 1 | 1.80 | own filament, LIBRARY / LAB |
| | **Total** | | | **278.55** | |

Not counted (owned or borrowed): commercial launch controller with key, extinguisher and water, safety glasses, laptop, known masses, drill and screwdriver, hex keys, hacksaw and mitre box, files, a 5.5 mm drill for the plate. Printed-bracket alternative (not in the total): 24 x `bracket.stl`, about 3.12 filament (section 3).

## 14. Extrusion vs plywood (priced both; extrusion taken by the owner)

| | Extrusion tower (this design) | Plywood tower (first v3) |
|---|---|---|
| Structure | 4 x 1 m 2020 64.00 + 24 steel bracket kits 31.20 + packs 7.00 + plate 18.00 + 4 pad eyes 10.00 + M3 4.00 = **134.20** | panel 32 + screws 7 + 8 braces 9 = **48.00** |
| Whole stand | **278.55** (reduced 176.47) | **192.35** (reduced 117.35) |
| Premium | **+86.20** (reduced to reduced: +59.12) | |
| For | does not scorch; T-slots mount electronics, cameras and a rain cover; looks right in video and portfolio; ring slides to any height; reusable for bigger motors | cheaper; 4 kg; needs only a saw and drill |
| Against | CAD 86 dearer, 64 fasteners, the CAD 120 line is gone | scorches near the plume; weaker; looks like a plank |

**The earlier estimate of about CAD 25 premium was for a 300 mm box with printed brackets and a plywood plate.** This tower is 523 mm tall (4 m of extrusion, not 3), the plate has to be aluminium (section 5), and the steel brackets and pad eyes are new lines. The biggest single drivers of the extra CAD 86: extrusion +16, steel brackets and hardware +28, plate +18, pad eyes +10, M3 +4, the rest is the plywood you no longer buy.

## 15. Build order (do not skip bench and swing-rig stages)

1. Print one 29 mm collar and the ring. Bench the DAQ on a table with the cell and a collar, press with a finger, type `raw`.
2. Calibrate with known masses (`electronics.md`), then check the zero does not change when you lift a lead.
3. Assemble the frame (order below), check the ring clears the collar by 2 mm with a card, run a dummy (no motor).
4. Pull-test the stakes. First burn a C6 (nozzle up, plugged or zero-delay if possible), then work up one class at a time per procedure 01. A motor class is only fired if 1.5 x its peak is inside 981 N.
5. Swing-rig and flight stages are separate and unchanged; this stand is a static test only.

**Frame assembly order** (preload T-nuts as in section 4): (1) bench-bolt the cell to the plate (M12 hex bolt from below, fender washer, snug) with the plate on two blocks; (2) lay the two long bottom rails and the two short ones around the plate's edges, T-nuts already in the top slots, screw the plate down (8 x M5) so the bottom frame is square; (3) stand the four uprights on the long rails' ends and fit the 8 bottom brackets; (4) fit the ladder, bars and top frame, brackets last; (5) screw the collar to the cell top from inside the bore, fit the ring on the bars; (6) fit the pad eyes. To change the cell, tip the whole stand on its side: the plate's underside is then open.

## 16. What I am unsure of

Prices (all of them, extrusion per metre most of all). The real S-type cell: top boss size, thread (M12 assumed), height (76 mm assumed), side-load rating, noise and error. Motor length: sized for 360 mm (a 38 mm I-class such as the AeroTech 38/360 case); a longer 38 mm motor does not fit. Real 2020 section properties (I = 6000 mm4 assumed) and drop-in T-nut and pad-eye strength (1000 N assumed). Whether the plate alloy you can buy is 6061-T6. Frame stiffness (no diagonals). Stake holding force (300 N assumed, pull-tested on site). Rope strength (1 kN assumed). Whether a PLA collar survives long I burns (try cheap motors first). Whether the top rails, 24 mm over a 360 mm motor tip and 60 mm from its axis, tolerate the I-class plume (aluminium should; watch for discoloration, and move the top frame up 50 mm by ordering longer uprights if worried). Attribution of the photos is as the project lead stated.

## Files
`collar.py` (STL generator, `stl/`), `bracket.py` (printed bracket, `stl/bracket.stl`), `handcheck.py`, `bom.py`, `drawing.py`, `test_stand_v3.py` (`python3 -m pytest -q`), `electronics.md`, `costing.md`, `explainer.md` (plain-language explainer; belongs in `docs/learning/`), `assembly-callouts.png`. Decision: `docs/decisions/007-test-stand-v3.md`.
