# Scoudouc Stand v3 (thrust stand, C6 to I-class, about 600 N peak)

**Status: PROPOSED** (decision 007, replaces v2). Recommended build **CAD 192**, reduced build **CAD 117** (see `costing.md`). About **4 kg** with the cell, one 2 x 4 ft plywood panel (half of it used), one cell, nine plywood-and-printed parts, and no cartridges.

**What it is:** a small plywood tower. One S-type load cell stands on the base board with the motor standing on top of it, nozzle UP, in a printed collar. Thrust pushes the motor straight down through the cell into the base and the ground. Four guy ropes from the base corners to stakes hold it down. A printed ring at mid-height catches the motor if it tips. It does **not** fire the motor: a separate commercial launch controller does (see `electronics.md`).

Drawing, every part numbered, PRINTED (orange) vs PURCHASED (navy): `assembly-callouts.png` (regenerate: `python3 drawing.py`).

## 0. What we copied, from whom (and where we departed)

Three stands that have actually been fired share one core: **a box or tower of uprights, ONE load cell on the floor, the motor standing on the cell**. v3 copies that core and nothing more.

| Photo | Channel | What we took from it |
|---|---|---|
| Painted plywood frame, one S-type cell on a shelf, printed cage, a few steel angle brackets, gravel | **Aero Propulsions** (video still) | Plywood is enough; one S-type cell; printed collar and cage around the motor foot; steel angle brackets; igniter leads out the side |
| Black 2020 extrusion box, cell on a plate in the bottom frame, printed ring held mid-height on two cross-bars | **Aero Propulsions** (video still) | Mid-height guide ring on two cross-bars; cell on the floor, not on a shelf |
| Tall narrow 2020 tower, cell on a plate at the floor, boards along one upright, four guy wires to stakes, grass | **BPS.space** (video still) | Guy wires to ground stakes as the hold-down (cheap, light, lets the frame be narrow); one cell at the floor |

(Attribution as given by the project lead. Photos are not in the repo; I did not look up the videos.)

| Departure | Why, in one line |
|---|---|
| Plywood instead of 2020 | Cheaper in Canada: structure about CAD 48 in plywood vs about CAD 73 in extrusion (section 11). Material is a cost call. |
| Two side panels instead of four uprights | Fewer parts to cut and join in plywood; the frame carries no thrust anyway. |
| Guys go to the **base corners**, not the top corners as on BPS | A top pull on a thin plywood panel puts about 75 N-m into its foot joint at 270 N, which screws and brackets cannot take; at the base it goes straight into the base board. (With rigid extrusion corners, top guys work as on BPS.) |
| **Ring kept** (Aero box) | Chosen: an S-type cell takes side moments badly and a 300 mm motor on a 46 mm collar is a long lever; the ring is one CAD 1 printed part, and it never carries thrust. |
| S-type cell, not the pancake or column cell in the photos | Cheap (about CAD 38), one thread on both ends, takes a straight push through its middle. |
| DAQ box on the ground 2 m away, not clipped to the frame (BPS) | Decision 005 says electronics at least 1 m from the vent notches; the frame is 0.3 m. |
| No blast plate, no portal, no cartridges, no extrusion | None of the three working stands has them. |

## 1. Layout (not to scale; mm)

```
ELEVATION (front view, cut through the motor axis)

              |   |        motor, nozzle UP (not in kit; sticks out of the top)
              |   |
   panel  +---+---+---+  panel        frame top = 280
     |    |  collar   |    |
     |  ==|==[ ring ]=|====|==      <- ring on 2 bars (bar tops 145 above base)
     |    |   disc    |    |
     |    |  [ CELL ] |    |         S-type cell, 76 tall (measure yours)
  ---+----+-----+-----+----+---      base board 260 x 220 x 18, on the ground
  guy ~~~~~~ (corner hole)  (corner hole) ~~~~~~ guy
  stake                                        stake       DAQ box 2 m+ away, 3 m cable

PLAN (looking down; base 260 x 220, panels inset 30)

   guy .                                        . guy
        +--+-----------------------------+--+
        |P |   ring bar  (40 x 164)      |P |
        |A |        ( collar + motor )   |A |     P = side panel;
        |N |   ring bar                  |N |     8 braces, one each side
        |E |                             |E |     of each panel foot
        +--+-----------------------------+--+
   guy .                                        . guy
```

Heights above the base top: cell 0 to 76; collar 76 to 179 (38 mm; 144 for 18 mm); aluminium disc at 94; motor foot at 96; ring tube 130 to 150; frame top 280 (the motor sticks out of the top, plume goes up).

**Ring height rule:** the ring top must stay at least 15 mm below the nozzle plane of the shortest motor you fire (C6: 96 + 70 = 166 above base, so ring top at 150 or lower). Cell height is assumed 76 mm: **measure yours**; if it differs, mark the bar line on the panels as (cell height + 69) for the top of the bars (145 for a 76 mm cell), and re-check the rule.

## 2. Plywood cut list (one 2 x 4 ft panel, 18 mm / 3/4 in)

| Part | Size (mm) | Qty | Notes |
|---|---|---|---|
| Base | 260 x 220 | 1 | **Grain along the 260** (the span). 14 mm hole at the centre, with a 28 mm counterbore 13 mm deep from the **underside** for the bolt head. Four 6 mm holes, 15 mm from both edges at each corner (guy ropes). |
| Side panel | 220 x 280 | 2 | Stand 30 mm in from the base's short edges. |
| Ring bar | 40 x 164 | 2 | Between the panels, bar tops 145 above the base top, **72 mm apart** (inner faces). |
| **Total** | 0.20 m2 of 0.74 m2 | 5 pieces | Layout: strip A (220 wide x 1220 long): base, panel, panel, spare base (260+280+280+260 = 1080). Strip B (40 wide): two bars. The spare base is the sacrificial plate if one gets charred or cracked. |

Fixings: panels to base by **8 steel corner braces** (one outside and one inside each panel, two per side) plus 3 #8 x 50 mm screws up through the base into each panel's bottom edge; wood glue optional. Bars to panels by 2 #8 x 50 mm screws per end through the panel into the bar end. Ring to bars: four #6 x 16 mm screws, down through the ring flange into the bar tops. Pre-drill everything (plywood splits). Paint is optional; plywood in plume range may scorch, replace a panel if it is charred deeper than 2 mm.

## 3. Hand check at 600 N (`handcheck.py`)

**What carries the thrust:** motor, collar, cell, **base board**, ground. Nothing else. In the Aero plywood photo the cell stands on a shelf, so the shelf is the loaded member; in the floor layout the base board plays that role, and no screw sees thrust. Screws only see the ring catching a tipping motor, so those are the screws in shear.

**Assumptions (conservative):** peak 600 N; ignition overshoot 1.3 (design load **780 N**); plywood rupture stress **20 MPa along the face grain, 10 MPa across** (assumed; typical fir or birch ply is higher, check your sheet); E = 6 GPa; sideways load 15% of peak = **90 N**; hold-down design load 3 x 90 = **270 N**; #8 screw in 18 mm ply: 250 N in shear, 300 N withdrawal from a face, 80 N from an edge (all assumed, heavily derated). Worst case for the base: the ground touches only two edges (a gravel hump), load at mid-span.

| Member | Result | Margin |
|---|---|---|
| **Base board in bending** (260 mm span, 192 mm net width after the counterbore, 780 N at the middle) | 4.9 MPa, deflection 0.45 mm | **SF 4.1** along the grain (2.0 if the sheet is cut the wrong way round, so mark the grain) |
| Base bearing under the cell foot (30 x 50 mm assumed) | 0.58 MPa | far under plywood crush (several MPa) |
| **Ring screws in shear** (90 N shared by 4 screws) | 22 N each | **SF 11** |
| Ring bars (90 N across two 40 x 18 bars, 164 mm span) | 0.85 MPa | SF 12 |
| Panel foot joint when the ring pushes along the bars (45 N per panel at 145 mm: 152 N pull on the screws) | capacity 840 N (one brace, 2 screws + 3 edge screws) | **SF 5.5** |
| Side panel buckling (cantilever) | 20 kN | irrelevant |
| M12 bolt in shear at 270 N | 40 kN capacity | SF 150 |
| Guy rope, worst case one rope takes all 270 N (push along a diagonal) | 4 mm polyester, assumed 1 kN, 60% left at a knot | **SF 2.2** |
| Guy hole tear-out (6 mm hole 15 mm from the edges) | 864 N assumed | SF 3.2 |
| **Stake**, 300 mm in firm soil | assumed 300 N | **SF 1.1: prove it** (section 8) |

**Result: PASS on paper; the stake and rope are the weak links and are checked on site.** Not checked: the real plywood strength, real S-type cell dimensions and side-load rating, PLA creep, anything but vertical thrust.

## 4. The cell: one 100 kg S-type, M12 (CZL301 type)

| Cell | Rated | 600 N peak (61% / 80% with the 1.3 overshoot) |
|---|---|---|
| 50 kg | 490 N | **overloaded** at the overshoot (159%). Rejected. |
| **100 kg** | 981 N | 61% at peak, **80% with the overshoot**, and 900 N (1.5 x peak) is inside 981 N. Smallest that survives an I. |
| 200 kg | 1962 N | survives, but doubles the error at the small end |

**Why one cell is enough from C6 to I:** accuracy is a percentage of full scale, so the **absolute** error is about the same for every motor (about 0.3 N), and that only matters below E. The ADC is not the limit: a 24-bit ADC at gain 128 gives about 2.1 million counts across the cell's range, so one count is **0.46 mN** (about 0.003% of a C6 peak). The limit is the cell's own error and noise.

**C6 resolution you get** (estimates; assumptions in `handcheck.py`): C6 peak about 14 N is **1.4% of the cell's range**. Noise about **0.09 N rms** per sample at 1000 samples/s (assumed 0.6 uV rms; read the ADS1220 data sheet), **0.03 N rms** if you average 10 samples. Cell error about **0.3 N** (assumed 0.03% of full scale, typical; read the data sheet), which is **2% of the C6 peak** and about **6% of its 5 N plateau**. **Acceptable** for what a first stand is for (curve shape, burn time, peak within a few %, total impulse within about 6%) but **not** for certified numbers. **Calibrate with small masses** (0.5 to 2 kg, see `electronics.md`) to remove gain error at the low end. If you need better, see the 5 kg swap below.

**Later, for better small-motor resolution (no cartridge system):** a 5 kg S-type (49 N rated, error about 0.015 N, 0.1% of a C6 peak) can go in the same place on the same two bolts. Check its thread (often M6, **check the data sheet**): the base hole (14 mm), counterbore (28 mm) and collar hole (13.5 mm) all take an M6 bolt with an 18 mm washer (ISO 7093). **A 5 kg cell must never see more than about 30 N (motors up to E-class at most); an I destroys it. Write that on the cell box.** The 5 kg cell is swapped by hand when you change motor class.

## 5. Printed collar family and guide ring (`collar.py`, run it to regenerate `stl/`)

| Part | Bore | Depth | Size | Print (MK3, estimated) | Filament |
|---|---|---|---|---|---|
| collar_18 | 21.4 | 50 | 26 x 26 x 68 | 1.0 h | 12 g |
| collar_24 | 26.4 | 55 | 32 x 32 x 73 | 1.6 h | 19 g |
| collar_29 | 31.4 | 65 | 37 x 37 x 83 | 2.2 h | 27 g |
| collar_38 | 40.4 | 85 | 46 x 46 x 103 | 3.7 h | 45 g |
| ring | ID 50, OD 66 | tube 15 + flange 5 | 66 x 116 x 20 | 3.1 h | 37 g |

All **LIBRARY** (Prusa MK3), PLA, floor/flange **down** on the bed, no supports, 0.2 mm layers, 4 perimeters, collars 40% infill (ring 20%). Times are estimated from volume at 0.062 h per cm3 (v2 calibration, solid, so conservative); confirm in the slicer. All five are watertight (tested).

**How a collar works:** it sits on the cell's top boss and is held by **one M12 socket-head screw** that threads into the cell's own M12 hole; the head sits in a pocket in the floor (a 5.5 mm PLA ledge under it: tighten **snug, about 5 N-m, no more**). A 2 mm aluminium disc (decision 005) lies on the floor and the motor stands on the disc. A 1 mm kraft-card liner tube in the bore is the **PLA heat barrier** (CLAUDE.md rule); the collar is a **consumable**, bin it if soft, warped or shiny, and do not use PLA for burns over about 3 s without trying a cheap motor first. Depth rule (from v2): the shortest motor of each class sticks out of the rim by 15 mm or more so the jet never touches PLA (C6 70 mm in 50, D12 70 in 55, a 98 mm 29 mm motor in 65, a 130 mm 38 mm motor in 85). **Measure your cell's top boss and thread** (assumed M12, 30 mm wide top face) and edit the parameters at the top of `collar.py` if they differ.

**The ring** rests on the two bars (flange on the bar tops, tube hanging between them) and never touches anything in normal use. ID 50 mm lets the 46 mm 38-mm collar pass through (2 mm gap), the bare 38 mm motor has 6 mm each side, an 18 mm one 16 mm. After a burn look for scuff marks inside the ring: they mean the thrust was off-axis. It is within 15 mm of a case at its tightest, so the **air gap and the collar wall are its heat barrier**; it is consumable too.

## 6. Igniter leads and cable routing

- Leads leave through the collar's **-Y notch**, down its lead groove (4 mm wide) to the base, then straight out the **open front** of the frame. The +Y notch is a second vent.
- Leave a **100 mm slack loop** between the collar and the first tape point on the base board. Tape (do not clamp) the leads to the base. A tight lead pushes on the collar and reads as thrust.
- The cell cable leaves the cell toward the **rear** (+Y), with its own slack loop, taped to the base, then 3 m to the DAQ box. Igniter leads and cell cable go out opposite sides and cross, if at all, at 90 degrees, at least 1 m from the stand.
- Nothing may touch the collar or the cell except the screw and the motor. After taping, check the zero does not change when you lift a lead.

## 7. Ejection-charge handling (decision 005)

The delay motor's ejection charge fires at the forward end, which is the **bottom** of the nozzle-up motor, into the collar floor. Mitigations: the 2 mm aluminium disc on the floor; two vent notches at the foot (+Y, -Y) that point the puff out the open front and back, and the ring bars sit **5 mm above** the notch top so the puff passes under them; prefer **plugged or zero-delay motors** for stand tests; the DAQ box stays at least 1 m (we use 2 m) from the notches; expect one extra downward pulse in the data after the delay; wait **delay time plus 60 s** before approaching.

## 8. Hold-down: guys and stakes (sized to 3 x 15% of peak sideways)

Thrust pushes the stand into the ground; the hold-down is for the sideways part (misaligned thrust, a tugged cable, wind). 15% of 600 N = 90 N; x3 = **270 N**. Own mass (about 4 kg) is no help.
1. Four 4 mm polyester ropes, one from each base-corner hole to a stake about 330 mm out on the diagonal, each stake driven at 45 degrees leaning **away** from the stand; ropes tied with a figure-eight or bowline at the base and a taut-line hitch (or a tent tensioner) at the stake. Ropes nearly flat on the ground.
2. Worst case (push along a diagonal) one rope takes all **270 N**. Rope SF 2.2 with a knot; stake SF 1.1 **on an assumed 300 N per stake**.
3. **Pull-test every stake before the first burn at each site:** hang 30 kg (300 N) or pull with a spring scale to 300 N; it must not move more than 10 mm. If it fails, drive it deeper, add a second stake in line, or do not fire above G.
4. **Sandbag option on ground that will not take stakes:** two 10 kg bags on the base margins (never on the cell or the span between the panels) plus the stand: about 235 N of weight, friction about 94 N at mu 0.4 (assumed). That covers up to a **G** (120 N peak: 54 N design). **I-class needs stakes.**

## 9. Safety distances and procedure

Follow `docs/procedures/01-static-fire.md`: key out until clear, key in, momentary fire switch, 5 s countdown, 60 s misfire wait; **everyone at least 30 m** from the stand with the lead wire fully extended. I suggest **50 m for H and I** (my suggestion, not a source). Clear-area minimums in procedure 01: C 120 m, D 150 m, E and F 300 m, so E and above need a club (CQF) launch day or written landowner permission. I-class static tests I did not research beyond this: check club and regulatory rules first. Firing is never done from the DAQ box. **Do not skip the build order below.**

## 10. Parts (CAD, before 15% Quebec tax; estimates, many unchecked against current listings)

Numbers match `assembly-callouts.png` and `bom.py`.

| # | Part | Kind | Qty | CAD | Source |
|---|---|---|---|---|---|
| 1 | Plywood 18 mm, 2 x 4 ft panel | PURCHASED | 1 | 32.00 | Home Depot / RONA / Canadian Tire (fir; birch about 45) |
| 2 | Wood screws #8 and #6, box | PURCHASED | 1 | 7.00 | Canadian Tire / Home Depot |
| 3 | Steel corner brace 2 in, pack of 4 (8 used) | PURCHASED | 2 | 9.00 | Home Depot / Canadian Tire |
| 4 | S-type load cell 100 kg, M12 | PURCHASED | 1 | 38.00 | Amazon.ca |
| 5 | M12 SHCS 30 mm, hex bolt 45 mm, 2 fender washers | PURCHASED | 1 | 8.00 | Princess Auto / Home Depot |
| 6 | Aluminium disc 2 mm (flashing or baking tray) | PURCHASED | 1 | 3.00 | Home Depot / Dollarama |
| 7 | Guy rope 4 mm polyester, 12 m | PURCHASED | 1 | 7.00 | Canadian Tire |
| 8 | Rope tensioner (tent type) | PURCHASED | 4 | 4.00 | Canadian Tire / MEC |
| 9 | Ground stake 300 mm | PURCHASED | 4 | 10.00 | Canadian Tire / RONA |
| 10 | ADS1220 breakout | PURCHASED | 1 | 35.00 | ProtoCentral / Amazon.ca |
| 11 | microSD module + 32 GB card | PURCHASED | 1 | 16.00 | Amazon.ca / RobotShop CA |
| 12 | Cell extension, 3 m shielded 4-core + GX12 pair | PURCHASED | 1 | 10.00 | Amazon.ca / DigiKey CA |
| 13 | Button, LED, resistors, perfboard, wire, caps, box | PURCHASED | 1 | 8.00 | RobotShop CA / DigiKey CA |
| 14 | ESP32-S3 (owned) | PURCHASED | 1 | 0.00 | owned |
| 15 to 18 | Collars 18, 24, 29, 38 mm | PRINTED | 4 | 2.60 | own filament, LIBRARY |
| 19 | Guide ring | PRINTED | 1 | 0.95 | own filament, LIBRARY |
| 20 | Spare collars (29, 38) | PRINTED | 2 | 1.80 | own filament, LIBRARY / LAB |
| | **Total** | | | **192.35** | |

Not counted (owned or borrowed): commercial launch controller with key, extinguisher and water, safety glasses, laptop, known masses, drill and screwdriver, hole saw or Forstner bit for the counterbore.

## 11. Plywood vs extrusion (priced both; plywood taken)

| | Plywood tower (this design) | 2020 extrusion box (BPS/Aero style) |
|---|---|---|
| Structure | ply panel 32 + screws 7 + 8 braces 9 = **48** | 2020 x 3.0 m cut to length (4 uprights 300, 8 frame bars 180, 2 ring bars 180) at about 16/m = 48; T-nut and screw kit 14; 10 printed corner brackets about 2.5 (LAB); a 220 x 220 ply plate from a remnant 8 = **72.5** |
| Whole stand | **192.35** | **216.85** |
| For | cheaper, no printed corners, 4 kg | stiffer; top-corner guys as on BPS; reusable for bigger motors; the ring bars slide to any height |
| Against | weaker; scorches near the plume; needs a saw and drill | about CAD 25 dearer; 10 more fasteners; extrusion prices are the least certain here (I used 16/m; check Amazon.ca and Misumi CA) |

If you can get salvaged 2020 from a lab or makerspace, the extrusion box drops to near the plywood price; I did not count that.

## 12. Build order (do not skip bench and swing-rig stages)

1. Print one 29 mm collar and the ring. Bench the DAQ on a table with the cell and a collar, press with a finger, type `raw`.
2. Calibrate with known masses (`electronics.md`), then check the zero does not change when you lift a lead.
3. Assemble the frame, check the ring clears the collar by 2 mm with a card, run a dummy (no motor).
4. Pull-test the stakes. First burn a C6 (nozzle up, plugged or zero-delay if possible), then work up one class at a time per procedure 01. A motor class is only fired if 1.5 x its peak is inside 981 N.
5. Swing-rig and flight stages are separate and unchanged; this stand is a static test only.

## 13. What I am unsure of

Prices (all of them). The real S-type cell: top boss size, thread (M12 assumed), height (76 mm assumed), side-load rating, noise and error. The plywood's real strength (20/10 MPa assumed). Stake holding force (300 N assumed, pull-tested on site). Rope strength (1 kN assumed). Whether top-edge plywood scorches in an I plume. Whether a PLA collar survives long I burns (v2 had the same doubt; try cheap motors first). Whether ring bars at 5 mm above the vent notches keep the puff off them. Attribution of the three photos is as the project lead stated.

## Files
`collar.py` (STL generator, `stl/`), `handcheck.py`, `bom.py`, `drawing.py`, `test_stand_v3.py` (`python3 -m pytest -q`), `electronics.md`, `costing.md`, `explainer.md` (plain-language explainer; belongs in `docs/learning/`), `assembly-callouts.png`. Decision: `docs/decisions/007-test-stand-v3.md`.
