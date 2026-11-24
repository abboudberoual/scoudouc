# 002 — Airframe: body diameter and construction (Scoudouc 1 and 2)

**Date:** 2026-11-02, revised 2026-11-23  **Status:** proposed (owner asked for a decision matrix; recommendation changed from B to D)

## What is being decided
The body tube for Scoudouc 1 (40 cm) and 2 (60 cm): diameter and what it is made of. The free Garrett-R16 TVC mount is drawn for a "74 mm" tube (inside or outside diameter still unconfirmed: open item 1).

## Options
- **A. 66 mm Estes BT-80 cardboard tube.** Standard model-rocket tube; the gimbal must be shrunk and its linkage redrawn.
- **B. 74 mm 3D-printed sections (PLA/PETG).** The 2 Nov recommendation. Fits the gimbal as drawn; bulkheads and leg mounts print into the sections.
- **C. 76 mm thin-wall printed PETG.** Lighter print, slop around the gimbal.
- **D. 3-inch kraft/cardboard tube (~76 mm ID, LOC/Madcow class, or a 3" mailing tube) with printed rings, bulkheads and a gimbal adapter ring.** The tube is bought; everything that needs a shape is printed. This is how most flown TVC rockets are built: tube plus printed internals.

## Decision matrix
Weights sum to 100 and come from the program goals (fast, cheap, learn each system, land). Scores 1–5 (5 best). Estimates are marked ~ and must be replaced by measurements before the build (open items).

| Criterion | Weight | A. 66 mm cardboard | B. 74 mm printed | C. 76 mm thin printed | D. 3" tube + printed internals |
|---|---|---|---|---|---|
| Body mass, S2 60 cm (~g) | 20 | 5 (~70) | 2 (~160–175) | 3 (~130) | 4 (~120) |
| Heat tolerance near the motor | 15 | 5 (paper chars, does not soften) | 2 (PLA 55 °C, PETG 80 °C; needs a liner) | 2 | 5 |
| Crash repair (cost, hours) | 15 | 3 (buy a tube, wait for shipping) | 4 (reprint a section, hours) | 3 | 4 (tube is cheap and stocked; reprint rings) |
| Fit with the free gimbal | 15 | 1 (redesign pivot, arms, linkage) | 5 (as drawn) | 3 (shims) | 4 (one printed adapter ring; depends on open item 1) |
| Time to first body | 10 | 4 (cut, glue, dry) | 2 (12–16 h of printing in <6 h library jobs = 3–4 jobs) | 2 | 4 |
| Cost per body (CAD) | 5 | 4 (~10–15) | 5 (~3–5 filament) | 5 | 4 (~15–25) |
| Stiffness / strength on landing | 10 | 4 | 3 (layer lines crack) | 2 | 4 |
| Mounting legs, bulkheads, avionics | 10 | 3 (printed rings anyway) | 5 (in the print) | 4 | 4 (printed rings, glued) |
| **Weighted total (max 500)** | | **365** | **330** | **285** | **415** |

**Result: D first, A second, B third.** The 2 Nov recommendation (B) rested almost entirely on gimbal fit; once heat and mass carry their weight, a bought tube with printed internals wins and keeps the gimbal fit through one adapter ring.

**Sensitivity (what would change the answer):** B overtakes D only if "fit with the free gimbal" is weighted above ~45 and time-to-first-body is ignored, or if the tube cannot be sourced in Canada. A overtakes D only if the gimbal is redesigned anyway for another reason (then A's 1 becomes a 4 and A wins on mass). C never wins.

## Recommended
**D: 3-inch kraft tube with printed rings, bulkheads and a gimbal adapter ring**, pending open items 1–3. Keep B as the fallback if no 3" tube is available in Canada within a week.

## What we give up with D
- ~50 g over cardboard A on S2 (still thrust-to-weight ~1.9 on an E12 at ~640 g total).
- Printed features are glued, not integral: joints are the weak point on a hard landing; design rings with generous glue area.
- One more interface to get right (tube ID vs gimbal OD).

## Open items before the build
1. Open the Garrett-R16 files: is "74 mm" the tube inside or outside diameter? Decides the adapter ring.
2. Source a 3" tube in Canada (LOC Precision / Madcow via Canadian dealers, or a 3" kraft mailing tube) and weigh a 60 cm length; replace the ~120 g estimate in docs/mass-budget.csv.
3. Copy before you engineer: check what BPS.space Scout F and JRD Propulsion actually used for the airframe and record it here with a link.
4. Print one adapter ring and one bulkhead; weigh them.

## Learn more
https://github.com/Garrett-R16/TVC_Mount
