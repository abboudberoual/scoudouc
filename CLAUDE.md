# Working rules for agents in this repo (The Spirit of Scoudouc)

## Goal
Launch and land a small solid-fuel rocket under thrust, as fast and cheaply as possible, while the owner learns each system. Keep token use low.

## Model selection (pick the cheapest that can do the job)
- **haiku**: web research, summaries, filling Notion databases, link checks, log parsing, plotting.
- **sonnet**: firmware, simulator code, test procedures, CAD scripts, docs/learning explainers.
- **opus / fable**: control-loop design, landing-burn timing, pyro circuit safety review, any decision that is expensive to redo. Use sparingly.
- Say which model you used and roughly how many tokens in every report, so it can be logged in the Notion Research Log.

## Style
- Plain language. If a technical term is needed, explain it in one short clause the first time.
- Short reports. Lead with the answer. Sources at the end.
- Every task that produces something the owner should understand also produces a short explainer in `docs/learning/`.

## Safety
- Never write code that fires an igniter without an explicit arm step and a physical arm switch in the circuit.
- Flag anything touching ESP32-S3 pins 0, 3, 35, 36, 37, 45, 46 (boot and PSRAM pins).
- Do not propose flights that skip the bench and swing-rig stages.

## Where things go
- Decisions → `docs/decisions/NNN-short-name.md`
- Research → `docs/research/` and the Notion Research Log
- Measured data → `data/` as CSV with a header row and units

## Printing constraints (university printers, PLA only)
- Library: Prusa MK3 (250 x 210 x 210 mm bed, ~50 mm/s realistic), free, one part per job, under 6 hours. Estimate print times at MK3 speeds, not Bambu speeds, and design every part to fit under 6 h at 0.2 mm layers, or mark it `LAB`.
- Lab: Creality printers (assume 220 x 220 x 250 mm), longer jobs, several parts per plate; owner brings the PLA. Use for body sections, legs and spare batches.
- Bambu Lab printers exist as a fallback for a part that is too slow or too tall for the others; do not design around them.
- PLA only: anything within ~15 mm of the motor case needs a heat barrier (cardboard/phenolic liner, air gap or standoff). Say so in the part spec.
- Every CAD deliverable ships with: estimated print time, orientation, infill, and which printer (LIBRARY or LAB).
