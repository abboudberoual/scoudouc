# Stand v3 costing (CAD, before about 15% Quebec tax; all prices are estimates)

Follows the repo cost loop. Full BOM with PRINTED vs PURCHASED and sources: `README.md` section 10 and `bom.py`; numbered drawing: `assembly-callouts.png`. Budget line: **CAD 120**, ESP32-S3 (owned) excluded. Launch controller, safety kit, tools and known masses are owned and excluded.

## (a) Cost it: Recommended build **CAD 192.35**
PURCHASED 187.00, PRINTED (filament only, PLA at about CAD 25 per kg) 5.35. For comparison v2 was 562 with 36 parts; v3 has 20 lines.

## (b) Top five cost drivers (line items)
| Rank | Line item | CAD | % of 192.35 |
|---|---|---|---|
| 1 | S-type load cell 100 kg | 38.00 | 19.8% |
| 2 | ADS1220 ADC breakout | 35.00 | 18.2% |
| 3 | Plywood 2 x 4 ft panel | 32.00 | 16.6% |
| 4 | microSD module + card | 16.00 | 8.3% |
| 5 (tie) | Ground stakes x4; cell extension cable | 10.00 each | 5.2% each |
| | Top five (taking the stakes as 5th) | 131.00 | 68% |
By group: electronics 69, cell and its hardware 49, plywood and fixings 48, hold-down 21, printed 5.35.

## (c) Reductions: saving, and what it costs us
| Driver | Option | Saving | Cost to us | Taken? |
|---|---|---|---|---|
| 1 Cell | Buy from a direct-import seller (38 to 20) | 18 | 3 to 4 weeks lead time, unknown brand; we calibrate with masses anyway | **Yes** |
| 1 | 50 kg cell instead of 100 kg | about 8 | Overloaded at an I (159% of rating): destroys the cell | **No** (breaks the requirement) |
| 1 | Used or surplus cell | 15 to 25 | Unknown overload history, which is what kills cells | No |
| 2 ADC | HX711 instead of ADS1220 (35 to 7) | 28 | Only 80 samples/s, loses the ignition spike, about 150 points on a C6 | **No** (this is the escalation, section e) |
| 2 | NAU7802 (about 30) | 5 | 320 samples/s, 3x slower; not worth it | No |
| 3 Plywood | Offcut from a wood-shop bin or a store remnant, free | 32 | Hunting time; check grain, voids and flatness; fallback is to buy the panel (+32) | **Yes, but owner-dependent** |
| 4 SD | Use a spare microSD the owner already has (module 6 stays) | 10 | None if owned; +10 if not | **Yes, but owner-dependent** |
| 5 Stakes | Landscape spikes 10 in at 1.50 instead of 300 mm at 2.50 | 4 | Shorter in soil, lower holding force: pull test decides; may need two per corner | **Yes** |
| 5 | Cable: alarm cable and soldered inline JST instead of GX12 pair (10 to 6) | 4 | Weaker connection, more soldering; same cable length, recalibrate | **Yes** |
| other | Taut-line hitch instead of 4 tent tensioners | 4 | A knot to learn | **Yes** |
| other | Button, LED, wire, box from the owner's bin | 3 | None if owned | **Yes** |
| other | Sheet aluminium disc: baking tray already owned | 3 | None | No (not counted) |
| other | Plywood sandbags and extra stakes | n/a | Not in the build; optional CAD 6 for two bags | n/a |

## (d) Reduced total: **CAD 117.35**
192.35 - 18 - 32 - 10 - 4 - 4 - 4 - 3 = **117.35**, under the CAD 120 line.
**Caveat:** 42 of the 75 saved (free plywood 32, owned microSD card 10) depends on what the owner already has or can find. With only the sure reductions (cell import, cable, spikes, hitch, bin parts: 33) the total is **CAD 159.35**.

## (e) If over CAD 120: earlier decisions that would bring it down
The reduced total is under 120 only with the owner-dependent items. If those fail (sure-only 159.35), the owner would need about 40 more:
| Decision | Change | Saving | Running total (from 159.35) |
|---|---|---|---|
| **007 / earlier 006 electronics choice (ADS1220)** | HX711 instead (one line in `electronics.md`; keeps everything else) | 28 | **131.35** |
| 003 motors | Ceiling I down to G (120 N peak): a 20 kg cell (about 15 imported vs 20) and no 38 mm collar | about 6 | 125.35 |
| Owner's own stock (not a decision) | Free plywood (32): already counted in the reduced total | 32 | 93.35 |
So with the sure-only path the **only** earlier decision that moves the needle is the ADC choice (28); the motor ceiling (003) barely does (about 6) because the cell and stakes cost about the same at every ceiling. **Under 120 needs either free plywood plus a spare card (reduced total 117.35), or the HX711 plus free plywood (about 99).** I have not changed any decision; they are the owner's calls in the Notion Decisions table.

## (f) Material alternative
2020 extrusion box with printed corners: structure about CAD 72.5 vs plywood 48, whole stand **CAD 216.85** (README section 11). Plywood taken as the cheaper.

**Totals: Recommended 192.35, Reduced 117.35 (sure-only 159.35), extrusion alternative 216.85.**
