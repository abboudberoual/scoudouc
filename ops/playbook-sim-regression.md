# Playbook — simulation regression

The landing-burn simulator (`sim/`) is the program's plan-as-simulation. Its regression is the number the brief's "biggest unknown" tile shows.

## Cases (fixed set; adding one is a PR)
| id | vehicle | mass_g | ascent motor | landing motor | trigger | n |
|---|---|---|---|---|---|---|
| S2-660-E12-naive | S2 | 660 | E12 | E12 | naive stopping-distance | 100 |
| S2-660-E12-integ | S2 | 660 | E12 | E12 | integrating (T-010) | 100 |
| S2-750-E12-integ | S2 | 750 | E12 | E12 | integrating | 100 |
| S1-380-C6-hop | S1 | 380 | C6 | — | hop, chute | 100 |

Thrust spread ±15 % (uniform) until measured; wind 0 until the 3-DOF update.

## Rules
- Rerun whenever `data/library/motors.json`, `docs/mass-budget.csv` or `sim/` changes on `main`.
- Output: `data/sim/regression-<date>.csv` and `metrics/sim` on Mission Control with success rate, p50 touchdown speed, n, and `delta_vs_last`.
- A success-rate move over 5 points must be explained in the run summary (what changed and why) or the change is reverted.
- Trigger logic changes get an Opus review recorded in the PR body before the PR opens.
- Under 70 % success on S2-660-E12-integ after T-010: a decision ticket (lighter vehicle, two landing motors, or thrust cutoff), never a silent redesign.
