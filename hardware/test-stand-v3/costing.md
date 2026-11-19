# Stand v3 costing, 2020 extrusion version (CAD, before about 15% Quebec tax; all prices are estimates)

Follows the repo cost loop. Full BOM with PRINTED vs PURCHASED and sources: `README.md` section 13b and `bom.py`; numbered drawing: `assembly-callouts.png`. Budget line: **CAD 120**, ESP32-S3 (owned) excluded. Launch controller, safety kit, tools and known masses are owned and excluded.

## (a) Cost it: Recommended build **CAD 278.55**
PURCHASED 273.20, PRINTED (filament only, PLA at about CAD 25 per kg) 5.35. 24 lines. Structure alone is **134.20** (plywood version: 48.00). **Plywood alternative: 192.35 recommended, 117.35 reduced.** Premium for extrusion: **+86.20** (recommended) and **+59.12** (reduced against reduced). The earlier "about CAD 25" figure was for a 300 mm box with printed brackets and a plywood plate; this tower is 523 mm tall and needs an aluminium plate (README section 14).

## (b) Top five cost drivers (line items)
| Rank | Line item | CAD | % of 278.55 |
|---|---|---|---|
| 1 | 2020 extrusion, 4 x 1 m | 64.00 | 23.0% |
| 2 | S-type load cell 100 kg | 38.00 | 13.6% |
| 3 | ADS1220 ADC breakout | 35.00 | 12.6% |
| 4 | Steel corner bracket kits x 24 | 31.20 | 11.2% |
| 5 | Aluminium plate 3.2 mm | 18.00 | 6.5% |
| | Top five | 186.20 | 66.8% |
By group: frame 124.20 (extrusion, brackets, fasteners, plate, M3), electronics 69, cell and its hardware 49, hold-down 31 (rope, tensioners, stakes, pad eyes), printed 5.35.

## (c) Reductions: saving, and what it costs us
| Driver | Option | Saving | Cost to us | Taken? |
|---|---|---|---|---|
| 1 Extrusion | Direct-import or salvage 2020 (16 to 9 per metre, 4 m) | 28 | 3 to 4 weeks lead and shipping risk, unknown cut quality; free salvage from a lab is better still | **Yes** |
| 1 | Shorten uprights for a 300 mm motor (423 instead of 483) | 0 | Same four 1 m lengths, so no saving; loses the 360 mm motors | No |
| 2 Cell | Direct-import cell (38 to 20) | 18 | 3 to 4 weeks, unknown brand; we calibrate anyway | **Yes** |
| 2 | 50 kg cell | about 8 | Overloaded at an I (159%): destroys it | **No** (breaks the requirement) |
| 3 ADC | HX711 instead of ADS1220 (35 to 7) | 28 | 80 samples/s, loses the ignition spike | **No** (escalation, section e) |
| 4 Brackets | **Printed PLA brackets** (24 x `bracket.stl`, LAB, one plate about 6 h) with two 100-packs of M5 T-nuts and screws replacing the kits | **13.08** | PLA creeps under the guy pull, softens near the top frame, a lab trip; ring-catch SF stays 3.5 on steel only (README section 3) | **Yes in the reduced total**, but the recommended build stays steel |
| 4 | Buy only 16 steel kits, print the 8 ring-ladder ones | about 3 | Pack sizes eat the saving | No |
| 5 Plate | Makerspace offcut of 3 mm 6061 | 18 | Hunting; must be 6061 (soft 3003 bends) | **Yes, owner-dependent** |
| 5 | 6 mm plywood insert (about 8) | 10 | **Fails the worst-case check (SF 0.55)** and scorches | **No** (breaks the requirement) |
| other | Spare microSD card the owner already has | 10 | None if owned | **Yes, owner-dependent** |
| other | Cable: alarm cable and soldered JST instead of GX12 pair | 4 | Weaker connection, recalibrate | **Yes** |
| other | Landscape spikes 10 in (1.50) instead of 300 mm stakes (2.50) | 4 | Lower holding force: the pull test decides | **Yes** |
| other | Taut-line hitch instead of 4 tent tensioners | 4 | A knot to learn | **Yes** |
| other | Button, LED, wire, box from the owner's bin | 3 | None if owned | **Yes** |

## (d) Reduced total: **CAD 176.47**
278.55 - 28 - 18 - 13.08 - 4 - 4 - 4 - 3 - 10 - 18 = **176.47**. Still **56 over the CAD 120 line.**
**Caveat:** 28 of the 102 saved (spare microSD 10, plate offcut 18) depends on what the owner has. With only the sure reductions the total is **CAD 204.47**.

## (e) Escalate: earlier decisions that would bring it under CAD 120
I have not changed any decision; they are the owner's calls in the Notion Decisions table.
| Decision | Change | Saving | Running total (from 204.47 sure-only; 176.47 reduced) |
|---|---|---|---|
| **007 (this stand), structure material** | Back to the plywood tower | 59.12 (reduced against reduced) | 117.35 reduced; 159.35 sure-only |
| 007 / 006 electronics (ADS1220) | HX711 instead | 28 | 148.47 reduced; 176.47 sure-only |
| 003 motors | Ceiling I to G (20 kg cell, no 38 mm collar, 300 mm uprights) | about 6 | 142.47 reduced |
So **with extrusion, no combination of the earlier decisions reaches CAD 120** (extrusion plus HX711 plus G ceiling is 142.47 reduced). Under 120 needs plywood (reduced 117.35, or about 89 with the HX711). The owner chose extrusion for durability and presentation; the CAD 120 line has to move to about 180 to hold the extrusion stand.

## (f) Material alternative
Plywood tower: structure 48.00, whole stand **CAD 192.35**, reduced 117.35 (sure-only 159.35). README section 14.

**Totals: Recommended 278.55, Reduced 176.47 (sure-only 204.47), plywood alternative 192.35 / 117.35.**
