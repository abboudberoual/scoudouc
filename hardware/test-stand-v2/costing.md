# Stand v2 costing (CAD, before about 15% Quebec tax; all prices are estimates)

Follows the repo cost loop. Line items, PRINTED vs PURCHASED and sources are in `README.md` section 12 and `bom.py`; numbered drawing: `assembly-callouts.png`.

## (a) Recommended C-I build: **CAD 562**
(Minimum C-G 498; Future with HPR module 882.) Printed parts are filament only (about CAD 40 including a spool); launch controller, safety kit, ESP32 and power bank are owned and excluded.

## (b) Top five cost drivers (groups of line items)
| Rank | Driver | CAD | % of 562 |
|---|---|---|---|
| 1 | 2040 extrusion, 9 pieces, 3.08 m | 119.5 | 21% |
| 2 | Load cells (5 kg, 50 kg, 200 kg) | 99.0 | 18% |
| 3 | DAQ electronics (ADS1220, SD, box, cable, switches) | 95.0 | 17% |
| 4 | Cut aluminium sheet (guide arm, blast plate, shield, stake tabs) | 77.0 | 14% |
| 5 | Hold-down and safety (stakes, bags, Nomex) | 57.0 | 10% |
| | Top five | 447.5 | 80% |
Next: frame hardware 42 (7%), printed parts 40 (7%), cartridge hardware 32 (6%).

## (c) Reductions: saving, and what it costs us
| Driver | Option | Saving | Cost to us | Taken? |
|---|---|---|---|---|
| 1 Extrusion | 2020 instead of 2040 for uprights and cross-bar (0.64 m at about 14/m less) | 9 | Slightly less stiff portal; it only carries the guide ring (checked: SF 14 weak-axis, unaffected). Low risk | **Yes** |
| 1 | Salvaged 2040 from the university lab or a makerspace for uprights, bar and cross rails | up to 60 | Time hunting, odd lengths, unknown profile; deck rails stay new | No (upside, not counted) |
| 2 Cells | Buy the 50 kg and 200 kg cells from direct-import sellers (30 to 20, 55 to 40) | 25 | 3 to 4 weeks lead time, unknown brand; we calibrate with masses anyway | **Yes** |
| 2 | Used or surplus cells | 15 to 30 | Unknown overload history, which is exactly what kills cells | No |
| 2 | Buy CART-200 later (when an I motor is in hand) | 69 | No I-class until then; changes scope, see (e) | No (scope) |
| 3 DAQ | NAU7802 instead of ADS1220 (about 35 to 30, estimate) | 5 | Only 320 samples/s, 3x slower; near the 250 minimum. Not worth it | No |
| 3 | Reuse the v1 SD module, key switch and LED | 33 | Only if v1 electronics are already bought; v1 and v2 cannot run at once | **Yes** (if v1 parts exist) |
| 4 Sheet | Cut the four stake tabs from the guide-arm offcut | 8 | Ask the shop; none | **Yes** |
| 4 | Vent shield from a baking tray instead of flashing | 10 | Looks scruffy; same job | **Yes** |
| 4 | Blast plate 1.2 mm instead of 2 mm | 8 | Warps sooner; it is a safety part | No |
| 5 Hold-down | Contractor bags instead of canvas ballast bags | 12 | Wear out, double-bag | **Yes** |
| 5 | Fibreglass welding blanket instead of Nomex | 15 | Research said Nomex; fibreglass is probably fine but untested. Owner's call | No |

## (d) Reduced total (same C-I scope): **CAD 465**
562 - 9 - 25 - 33 - 8 - 10 - 12 = 465 (97 saved, 17%).

## (e) Still over about CAD 250: earlier decisions that would bring it down
I have not changed any of these; they are the owner's calls in the Notion Decisions table.
| Decision | Change | Saving | Running total |
|---|---|---|---|
| 006 ceiling I to **G** | drop CART-200 set and 38 mm cup (54), one deck rail (11.5; one 2040 still has two slots for the SCP holes, and G passes at SF over 8), 2020 for long and cross rails (23) | 88.5 | **377** |
| 006 ceiling G to **F15 / E (CART-5 only)** | also drop CART-50 set (32), the portal (2020 uprights and bar 23, guide arm 30, less a printed ring 2.5) and its brackets and T-nuts (9) | 91.5 | **285** |
| Salvaged extrusion (see c) on top of the F15 ceiling | rails from the lab (about 47 of 285) | up to 47 | about 238 |
| Research choice ADS1220 over HX711 | not recommended: saves about 29, but 80 samples/s | 29 | not taken |
So **under CAD 250 is only reachable at an F15 ceiling with salvaged extrusion** (essentially v1 on a metal frame). The F15 ceiling matches the motors the project actually plans to buy (E12, F15: see `docs/research/2026-11-02-costs-cad.md`), and the cartridge standard still lets you add CART-50 and CART-200 later.

**Totals: Recommended 562, Reduced 465, Earlier-decision alternative (F15 ceiling) 285 (G ceiling 377).**
