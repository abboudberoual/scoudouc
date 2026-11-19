# 007 — Thrust stand v3: plywood tower, one S-type cell, copied from working stands

**Date:** 2026-11-19  **Status:** PROPOSED  (replaces 006)

## What we decided
Build **Stand v3** for motors from Estes C6 to I-class (about 600 N peak): an 18 mm plywood tower (base board, two side panels, two ring bars; one 2 x 4 ft panel), **ONE 100 kg S-type load cell** standing on the base board with the motor nozzle-UP above it in a printed collar (18, 24, 29, 38 mm, one M12 screw into the cell's own thread), a **printed guide ring** at mid-height on the two bars, and **four guy ropes from the base corners to stakes** as the hold-down. ESP32-S3 + ADS1220 records to SD; HX711 is the CAD 7 fallback. Firing stays on a commercial launch controller. Nozzle-up (005) unchanged. Files: `hardware/test-stand-v3/`.

## Where it is copied from
Three working stands share one core (frame, one cell on the floor, motor on the cell): **Aero Propulsions** (plywood frame with an S-type cell and printed cage; and a 2020 box with a printed ring on two mid-height cross-bars) and **BPS.space** (tall narrow 2020 tower with four guy wires to stakes). Departures, each justified in `README.md` section 0: plywood instead of extrusion (cheaper: structure about CAD 48 vs 73); guys at the base corners rather than the top (a top pull on thin plywood needs about 75 N-m in the panel foot); ring kept (the S-type takes side moments badly); DAQ on the ground 2 m away (005 wants 1 m from the vents).

## Why
- v2 was rejected as over-engineered: 36 parts and CAD 562, for a job the working stands do with one cell and a frame.
- Recommended build CAD 192, **reduced CAD 117** (with free plywood and a spare microSD card; CAD 159 without), against the CAD 120 line. See `costing.md`.
- Hand check at 600 N (780 N with ignition overshoot): the base board is the only loaded member, safety factor 4.1; ring screws in shear 11; weakest links are the stakes (assumed 300 N, pull-tested on site) and rope (2.2).
- 100 kg is the smallest S-type that survives an I (80% of rating at 780 N). One cell works for C6 to I because accuracy is a percentage of full scale; on a C6 that is about 0.3 N, 2% of its peak, 6% of its plateau.

## What we gave up compared with v2
- **No "breakdown-flat" packing**: v2 broke down into flat 500 mm pieces. v3 is a 4 kg glued-and-screwed plywood tower, 260 x 220 x 300 mm that does not fold. It fits a car boot.
- **One cell, one resolution compromise**: C6 error about 2 to 6% instead of v2's 5 kg cartridge (about 0.2%). Fixable later by a hand swap to a 5 kg S-type on the same two bolts (never above about 30 N), not a cartridge system.
- Plywood scorches and is consumable; no reuse for K-class and above (v2's HPR module is gone).
- Less stiff; a tall-rocket K-class module would need a new stand.
- Several numbers are assumptions: plywood strength, stake holding force, rope strength, the real cell's dimensions and noise, all prices.

## Lesson (record for every hardware design)
**Copy working designs first.** Before designing, find a stand, airframe or mechanism that someone has actually built and fired (BPS.space, JRD, university teams, forum builds with photos), copy its layout and materials, justify every departure in one line, and keep parts count and cost at or below the example's. Deriving from requirements is the last resort. v2 did the opposite and cost 3x. (Also now in CLAUDE.md.)

## Learn more
`hardware/test-stand-v3/explainer.md` (to be moved to `docs/learning/`), `docs/learning/load-cells-and-sampling.md`.
