# 003 — Motors: tuning (C6/D12) vs landing (E12/F15)

**Date:** 2026-11-02  **Status:** proposed

## What we decided
Proposed: tune and hop on **C6 and D12** at a 150 m field; use **E12** (not F15) for both climb and landing on Scoudouc 2 until F-class is reliably available in Canada. F15 stays an upgrade for S3 and S4. Also: reconsider the S1 motor (see "Contradiction" below).

## Motor numbers
From memory of published Estes data. **Verify each at thrustcurve.org before relying on it.** "Average" is the number the rocketry rules use; the real curve spikes early.

| Motor | Size | Loaded mass | Total impulse | Average / peak thrust | Burn |
|---|---|---|---|---|---|
| C6 | 18 mm | ~23 g | ~10 N·s | ~5 / ~14 N | ~1.9 s |
| D12 | 24 mm | ~44 g | ~20 N·s | ~10.5 / ~29 N | ~1.7 s |
| E12 | 24 mm | ~56 g | ~28 N·s | ~11 / ~33 N | ~2.5 s |
| F15 | 29 mm | ~95 g | ~50 N·s | ~15 / ~25 N | ~3.3 s |

## Thrust-to-weight checks
Thrust-to-weight = thrust divided by weight (mass x 9.81). Rule: **above 1.3 at liftoff, above 1 in the landing burn.** Masses are our bottom-up estimates (docs/mass-budget.md).

| Case | Mass | Thrust | Thrust-to-weight | Result |
|---|---|---|---|---|
| S1 on D12 | 376 g | 10.5 N | 2.85 | Pass |
| S1 on C6 | 355 g | 5 N | 1.44 | Pass, thin margin |
| S2 liftoff, E12 climb (landing E12 on board) | 659 g | 11 N | 1.70 | Pass |
| S2 landing burn, E12 (climb propellant gone) | 631 g | 11 N | 1.78 | Pass |
| S2 with F15 landing motor: liftoff | 698 g | 11 N | 1.61 | Pass |
| S2 with F15 landing motor: landing burn | 670 g | 15 N | 2.28 | Pass |
| **S2 at the roadmap's 900 g, E12 climb** | 900 g | 11 N | **1.25** | **Fail** |
| S2 at 900 g, E12 landing burn | 872 g | 11 N | 1.29 | Pass (just) |

Mass needed on S2 with an E12 climb: **at most 862 g** for 1.3, and **at most ~750 g** for a comfortable 1.5. Our estimate (~660 g, ~725 g with a 10% growth allowance) fits. The average thrust hides cold-day and curve variation, so do not build to the limit.

More landing thrust is not better. A solid motor cannot throttle, so with T/W of 2.3 the rocket stops sooner and then climbs again unless the ignition altitude is exactly right. E12 (~1.8) is the gentler choice; burn timing is a control-design task for a stronger model, later.

## Contradictions with the roadmap
1. **S1 "10-20 m hop on one D12" will not happen.** A simple no-drag estimate for a 376 g vehicle on a D12 is ~80 m; with drag maybe 55-65 m. A C6 (355 g) gives about 12 m, which matches the goal. Either fly S1 on a C6 (watch the 1.44 margin and the 18 mm to 29 mm adapter) or accept a ~60 m flight and the 150 m field. Check in OpenRocket before choosing. Estimates, not simulation.
2. **S2 at 900 g cannot lift off an E12** (above). The bottom-up mass is ~660 g, so the 900 g figure looks like a placeholder; replace it.
3. **Two motors, one gimbal.** Roadmap says E12 up, E12/F15 down. The mass budget assumes a stacked pair in one gimbal mount with the spent climb motor ejected (the JRD design in our research). That layout is not designed yet, and a motor with an ejection charge would fire it at burnout; the landing motor needs no ejection charge. Resolve in a later decision before S2 CAD.

## Canadian availability
- **E12:** found at bigboyswithcooltoys.ca (our cost research).
- **F-class:** Estes ships E/F motors only inside the US, and no Canadian F-class stock was found. BPS Signal R2 does not ship to Canada. Do not plan S2 around F15. Options: ask Canadian dealers directly; ask CQF members at the 3-4 launches a year; use E12 for both burns.
- **Purchase limit:** a person 12+ may buy up to 80 N·s and keep 6 motors at home. That is **two E12 (57 N·s)**, not 15 at once, so the "15 x E12" cost scenario must be bought in batches. Explosives amendment SOR/2026-206 (Oct 2026) changes storage rules; check before ordering.
- Site size: D motors need 150 m, E to G need 300 m, per the launch-site research.

## What we gave up
F15's longer burn and higher thrust (more landing margin for a heavier S2), and a one-trip motor purchase.

## Learn more
https://www.thrustcurve.org
