# 007 — Thrust stand v3: 2020 extrusion tower, one S-type cell, copied from working stands

**Date:** 2026-11-19  **Status:** ACCEPTED — option A (extrusion tower), approved by the owner on Mission Control 2026-11-24 01:10 UTC (T-007). Replaces 006.

**As bought (2026-11-21/23):** VEVOR 10 x 1000 mm 2020 anodised extrusion (CAD 78.17, arriving 26–27 Nov) and a **0–50 kg** S-type load cell (CAD 40.24, delivered 23 Nov), not the 100 kg cell below. The 50 kg cell's 490 N ceiling covers C to G with margin and most H; revisit (buy the 100 kg cell) before any I-class fire. Still to buy: 6061 plate, brackets, guy ropes, stakes; still to print: collars and guide ring.

**Update 2026-11-19: extrusion chosen for durability and presentation (it does not scorch; T-slots mount electronics; it will feature in videos and a portfolio); +CAD 86 recommended, +CAD 59 reduced against the plywood version.** The earlier estimate of about +CAD 25 was for a 300 mm box with printed brackets and a plywood plate; the tall tower needs 4 m of extrusion, steel brackets and an aluminium plate (`hardware/test-stand-v3/costing.md`). This is a proposal until the owner marks it Approved in Notion; the CAD 120 line is no longer reachable with extrusion (reduced 176.47).

## What we decided
Build **Stand v3** for motors from Estes C6 to I-class (about 600 N peak): a 160 x 160 x 523 mm **2020 aluminium extrusion tower** (four 483 mm uprights, small square top and bottom frames, a mid-height ring ladder with two ring bars; 3.61 m in four 1 m lengths, 24 steel inside-corner brackets, a 3.2 mm 6061 aluminium cell plate resting on the bottom rails), **ONE 100 kg S-type load cell** standing on the plate with the motor nozzle-UP above it in a printed collar (18, 24, 29, 38 mm, one M12 screw into the cell's own thread), a **printed guide ring** at the motor's mid-height on the two ring bars (M3 into the T-slots), and **four guy ropes from pad eyes at the bottom corners to stakes** as the hold-down. ESP32-S3 + ADS1220 records to SD; HX711 is the CAD 7 fallback. Firing stays on a commercial launch controller. Nozzle-up (005) unchanged. Files: `hardware/test-stand-v3/`.

## Where it is copied from
Three working stands share one core (frame, one cell on the floor, motor on the cell): **Aero Propulsions** (plywood frame with an S-type cell and printed cage; and a 2020 box with a printed ring on two mid-height cross-bars) and **BPS.space** (tall narrow 2020 tower with four guy wires to stakes; its proportions are the model). Departures, each justified in `README.md` section 0: guys at the bottom corners rather than the top (owner's call; the pull goes straight into the bottom rails); a mid-height ring ladder kept (the S-type takes side moments badly); steel brackets instead of printed ones (printed would save CAD 13, but they carry the guy pull and sit under the plume); DAQ on the ground 2 m away (005 wants 1 m from the vents).

## Why
- v2 was rejected as over-engineered: 36 parts and CAD 562, for a job the working stands do with one cell and a frame.
- Recommended build **CAD 278.55**, **reduced CAD 176.47** (CAD 204.47 without the owner-dependent items: spare card, plate offcut), against the CAD 120 line. Plywood version for comparison: 192.35 / 117.35. See `costing.md`.
- Hand check at 600 N (780 N with ignition overshoot): the loaded members are the 3.2 mm aluminium plate (worst case SF 1.9; the 6 mm plywood insert would be 0.55, so it was rejected) and the two bottom rails under it (SF 4.5, 0.07 mm); guy attachment SF 5.2 (T-nut) and 3.7 (pad eye); weakest links remain the stakes (assumed 300 N, pull-tested on site) and rope (2.2).
- 100 kg is the smallest S-type that survives an I (80% of rating at 780 N). One cell works for C6 to I because accuracy is a percentage of full scale; on a C6 that is about 0.3 N, 2% of its peak, 6% of its plateau.

## What we gave up compared with v2
- **No "breakdown-flat" packing by default**: v3 is 160 x 160 x 523 mm assembled (longest piece 483 mm, 2.8 kg frame, about 4.3 kg whole), but the bracket joints can be undone. It fits a car boot.
- **One cell, one resolution compromise**: C6 error about 2 to 6% instead of v2's 5 kg cartridge (about 0.2%). Fixable later by a hand swap to a 5 kg S-type on the same two bolts (never above about 30 N), not a cartridge system.
- The extrusion does not scorch, so the frame is reusable; K-class and above still needs more (v2's HPR module is gone).
- Frame has no diagonals and flexes if pushed; a tall-rocket K-class module would need a new stand.
- Several numbers are assumptions: T-nut and pad-eye strength, extrusion section properties, stake holding force, rope strength, the real cell's dimensions and noise, all prices.

## Lesson (record for every hardware design)
**Copy working designs first.** Before designing, find a stand, airframe or mechanism that someone has actually built and fired (BPS.space, JRD, university teams, forum builds with photos), copy its layout and materials, justify every departure in one line, and keep parts count and cost at or below the example's. Deriving from requirements is the last resort. v2 did the opposite and cost 3x. (Also now in CLAUDE.md.)

## Learn more
`hardware/test-stand-v3/explainer.md` (to be moved to `docs/learning/`; the existing `docs/learning/thrust-stand-v3.md` still describes the plywood version), `docs/learning/load-cells-and-sampling.md`.
