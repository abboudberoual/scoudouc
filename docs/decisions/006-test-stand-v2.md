# 006 — Thrust stand v2: aluminium frame, load-cell cartridges, I-class ceiling

**Date:** 2026-11-19  **Status:** replaced by 007

## What we decided
Build a long-lived second stand ("Scoudouc Stand v2") for motors from C6 up to I-class (38 mm, about 600 N peak): a 2040 T-slot aluminium frame (3.08 m of extrusion, about 9 kg carried), a standard **load-cell cartridge** (same bolt pattern and plug) in three ratings (5 kg bar, 50 kg bar, 200 kg S-type), a printed motor-cup family (18, 24, 29, 38 mm, one flange), and an **ESP32-S3 + ADS1220** recorder at about 1000 samples a second. v1 stays the quick-start. Nozzle-up (decision 005) is unchanged. Ignition stays on a separate commercial launch controller.

## Why
- One load cell cannot cover the range: accuracy is a percentage of full scale, so a 200 kg cell cannot read a C6, and a 5 kg cell breaks on an I. Swappable cartridges fix this cheaply (the three plates are one printed design).
- HX711 at 80 samples/s is too slow for ignition spikes; ADS1220 gives about 12x more for about the same price.
- An aluminium frame lasts; the hand check at 600 N passes with a safety factor of 3.7 on the weakest part (see `hardware/test-stand-v2/README.md`).

## What we gave up
- **No J-class or above (and so nothing near Level 3 sizes) without the HPR module.** The 2040 deck and PLA cups run out of margin near 1200 N; the module (4040 pedestal, bigger cell) is an extra CAD 320 or so, not designed yet.
- Cost: Recommended about CAD 562 versus v1's much smaller parts list; see `hardware/test-stand-v2/costing.md` for cheaper options (an F15 ceiling brings it to about CAD 275).
- Weight and setup time compared with v1 (about 9 kg, 10 minutes).
- Several figures are assumptions: section properties of the extrusion, T-nut slip load, bar-cell hole spacing, stake holding force, all prices.

## Learn more
docs/learning/load-cells-and-sampling.md
