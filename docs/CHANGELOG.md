# Changelog

One entry per merged PR, appended by the code builder on reconciliation (`docs: changelog for #N (T-NNN)`). PRs never edit this file; the entry comes from the PR body's `## Changelog entry`. Library data changes live in `data/library/CHANGELOG.md`.

- 2026-11-25 — #7 (T-010): sim: integrating landing-burn trigger + `.eng` loader; T-010 sweep shows timing-only landing ≤ 2.5 % at ±15 % thrust spread (≈40 % even at ±1 %), routing S2 landing to decision 009.
- 2026-11-25 — #8 (T-011): tools/fetch_thrustcurve.py + job T-011-2: thrustcurve.org fetch/convert moved to tier 0 on the laptop (source: https://www.thrustcurve.org/info/api.html).
- 2026-11-25 — #9 (T-018): static-fire procedure rewritten for the nozzle-up stand v3 and rung R1 (ignition-delay timing, mass-loss correction, matched sets, delay-charge precautions; Opus-reviewed). New `data/static-fires/fires.csv` log and ignition-delay explainer.
- 2026-11-25 — #10 (T-002): decision 002 accepted (S1–S2 airframe = 3-inch kraft tube + printed internals); open items split into T-035..T-038.
- 2026-11-25 — #11 (T-007): decision 007 accepted (stand v3 = 2020 extrusion tower); built with the 50 kg cell actually bought (490 N, C–G).
- 2026-11-25 — #12 (ops): procurement data and no-op run metrics have a defined commit path; procurement's 25 Nov purchase log rescued from a session branch.
- 2026-11-25 — #13 (no ticket): hardware/guides printable assembly-guide engine + G-001 thrust stand v3 guide (15 steps, have/buy list, 1:1 template, torque table); CLAUDE.md rule "every build has a printable guide". (PR body had no changelog entry; written from its summary.)
