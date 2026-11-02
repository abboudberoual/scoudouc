# 002 — Airframe: body diameter and construction (Scoudouc 1 and 2)

**Date:** 2026-11-02  **Status:** proposed

## What we decided
Proposed: build Scoudouc 1 and 2 with a **74 mm (3 in) 3D-printed body in short sections**, not the 66 mm Estes BT-80 tube the roadmap lists. This changes the roadmap (S1 and S2 move from 66 mm to 74 mm; S3 and S4 were already 74 mm, so one body size from S1 onward). Needs the owner's OK.

## Options compared
| | A. 66 mm BT-80 cardboard | B. 74 mm printed (recommended) | C. 76 mm thin-wall PETG |
|---|---|---|---|
| Fits free Garrett-R16 gimbal (made for 74 mm) | No: gimbal must be shrunk and the servo linkage redrawn | Yes, as designed | Loose; needs shims. If "74 mm" in that design means inside diameter, C is just B |
| Body mass, S1 (40 cm) / S2 (60 cm) | ~47 g / ~70 g | ~107 g / ~160 g | ~85 g / ~130 g |
| Cost per body (CAD, estimates) | ~10-15 plus a nose cone | ~3-5 of filament | ~3-4 of filament |
| After a crash | Tube creases or splits; buy a new one | Reprint the broken section (hours); PETG survives better than PLA | Same as B, but the thinner wall cracks sooner |
| Canada availability | In stock at bigboyswithcooltoys.ca (from our cost research) | Filament anywhere; needs a printer or print service (3dprintingcanada.com was in our research) | Same as B |
| Other | Light, stiff, easy to cut and glue | Sections can hold bulkheads and leg mounts in the print | Saves ~30 g over B but 2 mm of slop around the gimbal |

## Why
1. **The gimbal is the hard part and it is free, but only at 74 mm.** Shrinking it to 66 mm means redesigning pivot, servo arms and linkage: weeks of work on the exact system the owner most needs to understand.
2. **The mass penalty is affordable.** B costs about 90 g more than A on S2. Our S2 estimate is ~660 g (see docs/mass-budget.md), which still gives thrust-to-weight 1.7 on an E12. A 66 mm body would give ~2.0, which we do not need.
3. **Crashes are certain, and printed sections are cheaper and faster to replace** than tubes. One diameter from S1 to S4 also means one set of jigs, bulkheads and chute sizes.

## What we gave up
- About 90 g on S2 (60 g on S1) and a stiffer, cheaper-to-buy tube.
- Cardboard is more forgiving of heat near the nozzle. Printed plastic must stay clear of the motor casing; check this in the static fire (PETG softens near 80 C, PLA near 55 C, so use PETG).
- Printing time: roughly 12-16 h for an S2 body.

## Open items to check before printing
- Open the Garrett-R16 files and confirm whether 74 mm is the tube **inside** or **outside** diameter. A 3 in tube is often 76 mm inside.
- Weigh one printed ring and one printed section; replace the estimates in docs/mass-budget.csv.
- That gimbal takes a **29 mm** motor. D12 and E12 are 24 mm, so a printed adapter sleeve is needed (F15 is 29 mm and fits directly).
- Assumes the owner can print. If not, cost A looks better and the gimbal redesign becomes the price.

## Learn more
https://github.com/Garrett-R16/TVC_Mount
