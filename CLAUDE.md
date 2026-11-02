# Working rules for agents in this repo

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
