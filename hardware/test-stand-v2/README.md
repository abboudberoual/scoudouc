# Scoudouc Stand v2 (long-lived thrust stand, C6 to I-class)

**Status: PROPOSED** (decision 006). v1 (`hardware/test-stand/`, one PLA cup, HX711) stays the quick-start. v2 is the stand you keep.

**What it is:** an aluminium T-slot frame (2040 extrusion) that holds a motor nozzle UP in a printed cup. Thrust pushes the cup DOWN onto a swappable **load-cell cartridge**, which sits on the frame, which sits on the ground. Three cartridges (5 kg, 50 kg, 200 kg) cover Estes C6 (18 mm, about 15 N peak) up to an I-class 38 mm motor (about 600 N peak, Level 2 range). A DAQ board (ESP32-S3 + ADS1220, about 1000 samples a second) records the curve. It does **not** fire the motor; a separate commercial launch controller does (see `electronics.md`).

**Numbers:** about 9 kg carried (8.2 kg itemised + 10% for small bits), longest piece 500 mm, packs flat into one bag, about 10 minutes to assemble with one 4 mm hex key. Recommended build about CAD 562 (estimates, before tax); see "Parts and prices" and `costing.md`.

Drawing with every part numbered, PRINTED (orange) vs PURCHASED (navy/grey): `assembly-callouts.png`. Regenerate with `python3 drawing.py`.

## 1. Layout (not to scale)

```
ELEVATION (side, centre-line cut)                      cup axis = X 140 mm
                          exhaust  ^ ^ ^   (nothing overhead)
                                   | | |
      upright (4)            +-----nozzle----+
      2040 x 400             |    MOTOR      |  <- motor stands in cup, nozzle UP
       |                     |               |
       |   top cross-bar (5) |  card liner   |
       |   +---------+  guide arm (9) with 60 mm ring, 3 mm gap to the cup's guide band
       |   |=========|======[ring]==(band)====|
       |   |         |     |   CUP (25-28)  |    thrust pushes DOWN (v v v)
       |   |         |     +---flange 56----+
       |   |         |     | PLATFORM (22/24)|
       |   |         |     | [LOAD CELL]     |   <- the cartridge (16/17/18)
       |   |         |     | BASE PLATE (21/23)
  =====+===+=========+=====+=================+==== blast plate (10), 2 mm Al
  | rear cross (2) | deck rails (3) x2 side by side | ... front cross (2) |
  ground (gravel / dirt / paver; stakes (13) angle in at the four corners)

PLAN (looking down), base 500 x 400 mm, all rails lying flat (40 mm face up)
  Y
  ^  +-long rail 1 (500)-----------------------------------------------+
  |  |R|up  top cross-bar 5 (between uprights, slides to ring height)  |F|
  |  |E|rig                       [ring + cup]  deck rails 3,3          |R|
  |  |A|hts  guide arm 9 -->      cartridge on the deck                |O|
  |  |R|                                          ballast bags 14 (x2)  |N|
  |  +-long rail 1 (500)-----------------------------------------------+T|
  +--------------------------------------------------------------------> X
  stake tabs 12 at the 4 corners; DAQ box + Nomex 2 m or more away on a 3 m cable.
```

## 2. Frame (2040 extrusion, 6063-T5, 6 mm slot, M5 drop-in T-nuts)

Order these **cut to length** (cut tolerance +/- 0.5 mm, deburred; ask for square ends):

| Piece | Length | Qty | Job |
|---|---|---|---|
| Long rail | **500 mm** | 2 | base sides, lie flat |
| Cross rail | **320 mm** | 2 | base rear and front, between the long rails |
| Deck rail | **320 mm** | 2 | the cartridge deck: two rails side by side, centred 100 to 180 mm from the rear |
| Upright | **400 mm** | 2 | portal at the rear, 40 mm side along X (strong way against the guide push) |
| Cross-bar | **240 mm** | 1 | between the uprights at ring height, 40 mm face up |
| **Total** | **3.08 m** (9 pieces) | | about 3.1 kg at 1.0 kg/m (assumed) |

Joints: two 2040 L-brackets per joint (20 brackets, 10 joints). Uprights stand on the rear cross rail with a bracket on each side. The cross-bar bolts to the uprights with brackets that slide in the slots, so it can be set at **ring height** (bottom of the cup's guide band) for whichever cartridge is fitted. The uprights are 400 mm so the HPR module can reuse them later.

## 3. Load path (what carries the thrust)

```
motor base -> cup floor (8 mm) -> cup flange -> cartridge platform -> LOAD CELL
   -> cartridge base plate -> two deck rails (bending) -> long rails (via brackets)
   -> ground
```
Only the load cell is allowed to be in the path between the platform and the base plate. The guide ring, the blast plate and the vent shield must never touch the cup, platform or cell (the ring keeps 3 mm). The uprights carry **no** thrust; they only carry the guide ring. Thrust pushes the stand into the ground, not off it (decision 005).

## 4. Load-cell cartridge standard

A cartridge is a base plate, a load cell, a top platform and a plug. Swapping takes four M5 screws and one plug.

| Interface | Standard | Detail |
|---|---|---|
| **SCP** (bottom) | four M5 on a **20 x 60 mm** rectangle | the two inner T-slots of the two deck rails; screw heads sit on top of the plate (5 mm tall) |
| **SCF** (top) | **56 x 56 mm** flange, four M4 on a **40 x 40 mm** square | the same as the v1 cup, so v1 cups still fit |
| **Plug** | one **GX12 4-pin** socket in a wall on the plate's front edge | pin 1 E+ red, 2 E- black, 3 S+ white, 4 S- green. One cable fits all three |
| Height | 39 mm (bar) or 88 mm (S-type) above the deck | the guide arm is height-adjustable, so heights need not match |

| Cartridge | Cell (type) | Rating | Use | Why this cell |
|---|---|---|---|---|
| **CART-5** | straight **bar** (bending beam), 5 kg, 4-wire, about 80 x 12.7 x 12.7 mm | 49 N | A, B, C, D, and E motors with peak 30 N or less | Cheap, tiny, a C6 (15 N) uses 31% of the range so the curve has fine steps |
| **CART-50** | same-shape straight **bar**, 50 kg | 490 N | E motors above 30 N, F, G, H | Same plates as CART-5 (print the same files). H peaks up to about 300 N are 61% of range |
| **CART-200** | **S-type** (tension and compression), 200 kg, M12 threads | 1960 N | I-class (600 N is 31% of range) and headroom | A bar cell this big is hard to find and mount; an S-type takes a straight push through its middle, and tolerates a bit of misalignment |

**Choosing a cartridge:** rated capacity must be at least **1.5 x the motor's peak thrust** (2 x if you can), because the ignition spike can overshoot the data-sheet peak, and because an overloaded cell is damaged or wrecked (the AQUILO stand overloaded a 200 kg cell). Look up the peak on the motor's data sheet. Typical largest peaks (check each motor): C 15 N, D 30 N, E 45 N, F 70 N, G 120 N, H 300 N, I 600 N. If two cartridges could do it, take the smaller; accuracy is a percentage of full scale (see `docs/learning/load-cells-and-sampling.md`). Typical combined error is about 0.05% of full scale (estimate; read the data sheet): about 0.025 N, 0.25 N and 1 N for the three cells.

**Overload stops (bar cartridges):** two printed pillars stop the platform 0.8 mm below its rest position, so a dropped weight or a wrong motor cannot bend the bar. The gap is a guess until you measure your cell's real deflection; adjust `STOP_GAP` in `cartridge.py` or add a card shim.

**Bar-cell mount:** a bar cell is held by two M5 bolts at its fixed end, and those bolts feel a twisting push (about 2.9 kN at 490 N, see hand check). They screw up from underneath, under **M5 fender washers** (22 mm across) sitting in the plate's recesses. Do not leave the fender washers out.

**Print files:** `cartridge.py` makes `plate_bar` (4.3 h), `platform_bar` (1.8 h), `plate_s` (3.3 h), `platform_s` (2.0 h) in `stl/`, all LIBRARY (Prusa MK3), flat on the bed, underside down, no supports, 0.2 mm, 4 perimeters, 40% infill (use 100% on the plates if you can). Times are estimated from volume using the v1 cups as calibration (0.062 h per cm3 of solid on an MK3); confirm in the slicer. Bar-cell hole spacing and the S-type height are **parameters at the top of the script: measure the cell you receive and re-run**. PLA is fine here: nothing is within 15 mm of a motor case (the cup and its liner are in between).

## 5. Motor cup family (18, 24, 29, 38 mm)

`cup.py` makes `stl/cup_18mm.stl` to `cup_38mm.stl`. All share the **SCF flange** (56 mm square, 8 mm thick, M4 on 40 mm) and a round **guide band** 54 mm across so one aluminium ring fits every cup. Each has a lead groove and notch on one side and a vent notch on the other (rotate the cup so the vent notch faces sideways, not at the uprights). Bore = motor + 2 mm liner + 0.4 mm clearance.

| Cup | Bore | Depth | Height | Print (est., MK3) | Filament |
|---|---|---|---|---|---|
| 18 mm | 20.4 | 50 | 58 | 4.2 h | about 50 g |
| 24 mm | 26.4 | 55 | 63 | 3.9 h | about 47 g |
| 29 mm | 31.4 | 65 | 73 | 3.8 h | about 46 g |
| 38 mm | 40.4 | 85 | 93 | 4.0 h | about 48 g |

Printed LIBRARY, flange down, no supports (the band's cones are 45 degrees), 0.2 mm, 4 perimeters, 40% infill. Depth rule: the shortest motor of each class still sticks out of the rim by 15 mm or more (C6 70 mm in the 50 mm cup, D12 70 in 55, a 98 mm 29 mm motor in 65, a 130 mm 38 mm motor in 85) so the nozzle jet never touches PLA.

**Heat barrier (PLA):** a fresh 1 mm kraft-card liner tube every burn is the heat barrier between the case and the PLA, as in v1. The cup is a **consumable**: bin it if soft, warped or shiny. Do not use PLA cups for burns longer than about 3 s without testing on a cheap motor first; the K-class module uses a metal cup.

## 6. Cage and anti-tip (guide arm)

A 5 mm aluminium **guide arm** (100 x 180 mm) lies on top of the cross-bar and reaches forward to a 60 mm ring around the cup's guide band: a **3 mm gap all round**, as in v1, so it never carries thrust. It stops the cup toppling if a cell mount fails or the stand is bumped. It is a flat plate, so a sideways push on the ring is a push *in its own plane* and it is very stiff. Aluminium means no heat problem at the ring. After a burn, look for scuff marks on the band: they mean the thrust was off-axis.
Set the cross-bar so the arm sits on the band (bottom of band = 23 mm above the cup's underside). The arm's four bolt holes are slotted for sideways trimming.

## 7. Blast plate, deflector, electronics cover

Nozzle up means the plume goes up, but hot slag falls back around the stand and the delay motor's ejection charge puffs out of the **cup base** (as decision 005 says).
- **Blast plate** (10): 2 mm aluminium 240 x 300 lying on the rails, with a cut-out for the cartridge. It stops slag burning the frame, the cell cable and the grass.
- **Vent shield** (11): bent aluminium flashing, about 150 mm tall, bolted to the blast plate 10 mm clear of the cup on the cable side, so the ejection puff goes away from the connector and cable.
- **Nomex blanket** (15) over the DAQ box, which sits **2 m or more** from the stand on a 3 m cable, out of the line of the vent notch.
- Prefer plugged or zero-delay motors for stand tests. Wait delay time plus 60 s before approaching.

## 8. Hold-down (3 x the peak sideways load)

Thrust itself presses the stand into the ground. The hold-down is for the sideways part: a thrust vector a few degrees off-axis, a tugged cable, wind. Assumption: peak sideways load = **15% of peak thrust** (an 8.5 degree misalignment, generous). Design for **3 x that**.

| Motor class | Peak thrust | Sideways x3 | Needs |
|---|---|---|---|
| up to F (70 N) | 70 N | 32 N | frame + 10 kg ballast on pavement is fine (friction about 74 N) |
| G (120 N) | 120 N | 54 N | 20 kg ballast, pavement OK (friction about 114 N) |
| H, I (300, 600 N) | 600 N | 270 N | **stakes required**, soil or gravel only |

For I: frame about 9 kg plus **two ballast bags of 10 kg each** (filled on site with soil or gravel, so you do not carry them; empty bags weigh 0.2 kg) gives about 290 N weight, so friction at mu 0.4 is about 114 N. Four 300 mm steel stakes through the corner tabs, each assumed 250 N in firm ground (conservative, **assumption, not measured**), give 1000 N, which is **3.7 x the 270 N design load**. If you cannot drive stakes (pavement, rock) do not fire above G. Bags sit on the rails only, never on the cup, cell or guide arm; re-tare after loading the bags. The bar cells never see the bags.

## 9. Hand check at 600 N (`handcheck.py`)

**Assumptions (conservative):** 6063-T5 minimum yield 110 MPa; E = 69 GPa; 2040 area 300 mm2; bending stiffness 8,000 mm4 across the 20 mm direction (weak) and 25,000 mm4 across 40 mm (strong), roughly 70% of typical catalogue values, replace with your vendor's data sheet; I-class peak 600 N; ignition overshoot 1.3 x; one M5 T-nut slips at 400 N (assumed). Worst case, the deck rails are treated as simply supported over 320 mm with no help from the ground (the real stand sits on the ground, so this is pessimistic).

| Member | Result at 600 N | Margin |
|---|---|---|
| **Deck rails** (two 2040 flat, 320 mm span, load at mid-span) | 30 MPa, deflection 0.37 mm | **SF 3.7** on yield (2.8 with 1.3 x overshoot) |
| Long rails (300 N point load, 460 mm span) | 33 MPa | SF 3.3 |
| Deck-rail brackets (4 rail ends x 2 brackets) | 75 N each vs 400 N slip | SF 5.3 |
| **Uprights**, worst case: all 600 N somehow goes down the portal (300 N each) | axial 1.0 MPa; buckling (cantilever K = 2, 400 mm) limit 8.5 kN each | **buckling SF 28** |
| Uprights, 100 N sideways at the ring (50 N each, 111 mm lever, weak-axis) | 6.9 MPa bending | combined yield **SF 14** |
| 50 kg bar-cell fixed-end bolts at rated load (490 N x 60 mm / 10 mm pitch) | 2.9 kN per bolt | SF 2.9 on M5 8.8 proof load |
| PLA under the fender washer | 8.2 MPa bearing, 3.5 MPa web shear | OK (PLA about 50 MPa crush, about 15 MPa layer shear) |

**Result: PASS.** The weakest element is the deck rails (SF 3.7, 2.8 with overshoot). One flat 2040 would give 1.8, which is why the deck is two rails. At J-class (about 1200 N) the deck margin falls under 1.5 with overshoot, which is one reason the ceiling is I. **Not checked:** the real section properties (use your vendor's), T-nut slip load (assumed), bar-cell hole pitch (assumed 10 mm), PLA creep over weeks (store cartridges unloaded).

## 10. Teardown and transport

Flat pack, nothing longer than 500 mm, about 9 kg:
1. **Base** (4 rails + 2 deck rails, 500 x 400 x 20 mm, about 2.3 kg): left assembled.
2. **Portal** (2 uprights + cross-bar + arm, about 1.8 kg): unscrew 4 bolts from the rear cross rail, lies flat 400 x 280 x 40 mm.
3. Cartridges in foam or padded pouches, plug caps on; cups in a box; blast plate and vent shield flat in the bag.
4. DAQ box, 3 m cable coiled, power bank, Nomex.
5. Stakes, empty bags, tool bag (4 mm hex key, torque limit about 4 N-m, card gap feeler).
All fits a 550 x 450 x 150 mm tool bag. Assembly: portal on, cartridge on, plug in, ring gap check with a card, calibrate (see `electronics.md`).

## 11. How a 4040 HPR module bolts on later

For K and above (peaks of 1500 N or more) the 2040 deck and PLA cups are not enough. The module is its own stiff base:
- **Pedestal:** two 4040 sleepers (500 mm) lying on the ground and a 4040 spreader (320 mm), M8 T-nut hardware, so the thrust goes straight into the ground and not through the 2040.
- **Cell:** a 1000 kg column or pancake compression cell on the spreader, with a larger flange **SCF-H** (an 8 mm aluminium plate, four M8 on an 80 mm square) and a metal cup. Not designed yet; this is the interface only.
- **What the v2 frame gives:** the portal (uprights, cross-bar, guide arm with a bigger ring) moves from the v2 base onto the module's spreader with the same four M5 bolts; the 4040 slot pitch is 20 mm like 2040, so the foot pattern matches. The DAQ, the GX12 plug and calibration procedure are unchanged (a 2 mV/V cell reads the same way; gain stays 128).
- **Not reused:** the 2040 base, PLA cartridges and cups.
Budget: about CAD 320 (rough, Future price below).

## 12. Parts and prices (CAD, before 15% Quebec tax; estimates, many not checked against current listings)

Prices are my estimates from typical Canadian listings (Amazon.ca, Misumi CA, spool3d.ca, RobotShop CA, DigiKey CA, local metal shop). **Confirm each at order time.** Extrusion priced at about CAD 36 per metre cut to length. `bom.py` holds the same numbers.

| # | Part | Kind | Qty Min | Qty Rec | Unit CAD | Min CAD | Rec CAD | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | Long rail, 2040 x 500 mm | PURCHASED | 2 | 2 | 18.00 | 36.00 | 36.00 | Amazon.ca / Misumi CA, cut to length |
| 2 | Cross rail, 2040 x 320 mm (rear, front) | PURCHASED | 2 | 2 | 11.50 | 23.00 | 23.00 | same |
| 3 | Deck rail, 2040 x 320 mm (pair under cartridge) | PURCHASED | 2 | 2 | 11.50 | 23.00 | 23.00 | same |
| 4 | Upright, 2040 x 400 mm | PURCHASED | 2 | 2 | 14.50 | 29.00 | 29.00 | same |
| 5 | Top cross-bar, 2040 x 240 mm | PURCHASED | 1 | 1 | 8.50 | 8.50 | 8.50 | same |
| 6 | Corner bracket for 2040 (L, with screws) | PURCHASED | 20 | 20 | 0.80 | 16.00 | 16.00 | Amazon.ca, pack of 20 about 16 |
| 7 | M5 drop-in T-nut | PURCHASED | 50 | 60 | 0.14 | 7.00 | 8.40 | Amazon.ca, pack of 100 about 14 |
| 8 | M5 screw kit (8/12/16/20 mm) + M4 nuts/bolts + washers | PURCHASED | 1 | 1 | 18.00 | 18.00 | 18.00 | Amazon.ca / Princess Auto |
| 9 | Guide arm, 5 mm aluminium plate 100 x 180, 60 mm hole | PURCHASED | 1 | 1 | 30.00 | 30.00 | 30.00 | local metal shop (estimate) |
| 10 | Blast plate, 2 mm aluminium 240 x 300 | PURCHASED | 1 | 1 | 25.00 | 25.00 | 25.00 | local metal shop (estimate) |
| 11 | Vent shield, aluminium flashing 0.8 mm | PURCHASED | 1 | 1 | 10.00 | 10.00 | 10.00 | Home Depot / RONA (estimate) |
| 12 | Stake tab, 3 mm Al flat bar 25 x 60, 10 mm hole | PURCHASED | 4 | 4 | 3.00 | 12.00 | 12.00 | local metal shop (estimate) |
| 13 | Ground stake, 300 mm steel | PURCHASED | 4 | 4 | 3.00 | 12.00 | 12.00 | Canadian Tire / RONA (estimate) |
| 14 | Ballast bag (empty canvas / dry bag, filled on site) | PURCHASED | 2 | 2 | 7.50 | 15.00 | 15.00 | Amazon.ca (estimate) |
| 15 | Nomex blanket for the electronics (about 30 x 30 cm) | PURCHASED | 1 | 1 | 30.00 | 30.00 | 30.00 | Amazon.ca (estimate) |
| 16 | Load cell, 5 kg straight bar (TAL220 type) | PURCHASED | 1 | 1 | 14.00 | 14.00 | 14.00 | Amazon.ca / RobotShop CA (estimate) |
| 17 | Load cell, 50 kg straight bar | PURCHASED | 1 | 1 | 30.00 | 30.00 | 30.00 | Amazon.ca / AliExpress (estimate) |
| 18 | Load cell, 200 kg S-type (M12) | PURCHASED | 0 | 1 | 55.00 | 0.00 | 55.00 | Amazon.ca (estimate) |
| 19 | GX12 4-pin plug + socket pair | PURCHASED | 2 | 3 | 4.00 | 8.00 | 12.00 | Amazon.ca, pack of 5 about 15 |
| 20 | Cartridge fasteners (M5 x 16/20 bolts, M5 fender washers, M12 bolt) | PURCHASED | 1 | 1 | 20.00 | 20.00 | 20.00 | Princess Auto / Amazon.ca |
| 21 | Base plate, bar cell (cartridge.py plate_bar) | PRINTED | 2 | 2 | 1.30 | 2.60 | 2.60 | own filament |
| 22 | Top platform, bar cell (platform_bar) | PRINTED | 2 | 2 | 0.60 | 1.20 | 1.20 | own filament |
| 23 | Base plate, S-type (plate_s) | PRINTED | 0 | 1 | 1.00 | 0.00 | 1.00 | own filament |
| 24 | Top platform, S-type (platform_s) | PRINTED | 0 | 1 | 0.60 | 0.00 | 0.60 | own filament |
| 25 | Motor cup 18 mm (cup.py) | PRINTED | 2 | 2 | 1.25 | 2.50 | 2.50 | own filament |
| 26 | Motor cup 24 mm | PRINTED | 2 | 2 | 1.20 | 2.40 | 2.40 | own filament |
| 27 | Motor cup 29 mm | PRINTED | 2 | 2 | 1.15 | 2.30 | 2.30 | own filament |
| 28 | Motor cup 38 mm | PRINTED | 0 | 2 | 1.20 | 0.00 | 2.40 | own filament |
| 29 | PLA filament, 1 kg spool | PURCHASED | 1 | 1 | 25.00 | 25.00 | 25.00 | spool3d.ca (estimate) |
| 30 | ESP32-S3 N16R8 board (already owned) | PURCHASED | 1 | 1 | 0.00 | 0.00 | 0.00 | owned (about 22 on Amazon.ca) |
| 31 | ADS1220 24-bit ADC breakout board | PURCHASED | 1 | 1 | 35.00 | 35.00 | 35.00 | ProtoCentral / Amazon.ca (estimate) |
| 32 | microSD module + 32 GB card | PURCHASED | 1 | 1 | 18.00 | 18.00 | 18.00 | RobotShop CA / Amazon.ca (estimate) |
| 33 | Enclosure, IP65 plastic box | PURCHASED | 1 | 1 | 15.00 | 15.00 | 15.00 | Amazon.ca (estimate) |
| 34 | Shielded 4-core cable, 3 m, plus mating plug | PURCHASED | 1 | 1 | 12.00 | 12.00 | 12.00 | DigiKey CA / Amazon.ca (estimate) |
| 35 | Arm key switch, button, LED, wire, perfboard | PURCHASED | 1 | 1 | 15.00 | 15.00 | 15.00 | DigiKey CA / RobotShop CA (estimate) |
| 36 | USB power bank (already owned) | PURCHASED | 1 | 1 | 0.00 | 0.00 | 0.00 | owned |
| | **Total** | | | | | **498** | **562** | |

**Three price points**
| Price point | Scope | Total (CAD, est.) |
|---|---|---|
| **Minimum** | C to G, two cartridges (CART-5, CART-50), no 38 mm cup | **498** |
| **Recommended** | C to I, three cartridges, all four cups | **562** |
| **Future** | Recommended + 4040 HPR module (4040 pieces 55 + 18, brackets 32, M8 kit 30, 1000 kg cell 150, SCF-H plate 35 = 320; rough) | **882** |

Excluded (owned or borrowed): commercial launch controller with key (about CAD 80 to 150 for one rated for HPR igniters, estimate), extinguisher and water, safety glasses, laptop, known masses, tools. Printed parts cost filament only (university printers are free). ESP32-S3 and power bank are counted at 0 because the owner has them. See `costing.md` for how to cut the total.

## 13. Distances and procedure

Follow `docs/procedures/01-static-fire.md`: key out until clear, key in, momentary fire switch, 5 s countdown, 60 s misfire wait. Distances: Tripoli flight-table distances for static tests: H to J 100 ft (30 m), K 200 ft. Procedure 01 also says everyone 30 m from the stand for E/F. **Note:** the v1 README says 10 m, which contradicts procedure 01 (30 m); use 30 m minimum for v2 and 50 m is a sensible choice for I (my suggestion, not a source).

## 14. Build order (do not skip bench and swing-rig stages)

1. Print one 29 mm cup and the bar-cartridge parts; bench the DAQ with a cartridge on a table (type `raw`, press with a finger).
2. Calibrate each cartridge with known masses (see `electronics.md`).
3. Assemble the frame, check the 3 mm ring gap with a card, check the reading does not change with the ring removed.
4. Dummy run (no motor), then a C6 on CART-5, working up one class at a time per procedure 01.
5. A cartridge is only used for motors within its 1.5 x rule.

## Files
- `cartridge.py`, `cup.py`: STL generators (`stl/`). `bom.py`, `drawing.py`, `handcheck.py`, `test_stand_v2.py`.
- `electronics.md`, `costing.md`, `assembly-callouts.png`.
- `docs/decisions/006-test-stand-v2.md`, `docs/learning/load-cells-and-sampling.md`.
