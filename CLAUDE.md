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

## Session start (every chat)
Read, in this order, before doing anything else: the Notion hub header ("The Spirit of Scoudouc — Project Hub"), the "Needs me now" list, and the Decisions database. A decision whose Verdict is Approved / Rejected / Changed is the owner's ruling: update the matching docs/decisions file status, unblock or re-plan the dependent tasks, and never re-ask it in chat. Decisions are made in Notion, not in chat.

## Session end ("wrap up")
Commit and push; update Notion task statuses and the hub header (status line, red flag, this week's list); log every agent run's model and tokens in the Research Log; rewrite the project handoff doc so the next chat starts cold without losing anything.

## Cost loop (every hardware deliverable)
Every design that will be bought or built ships with a `costing.md` beside it, and the loop runs in this order:
1. **Cost it**: full BOM in CAD, Canadian sources, estimates marked. Split PRINTED vs PURCHASED.
2. **Rank the drivers**: top five line items with % of total.
3. **Reduce**: for each driver, concrete alternatives with the saving and what it costs us (capability, time, risk). Take the ones that keep the requirement. Give the reduced total.
4. **Escalate**: if still over the budget line for that item, list which earlier decisions (by number) would bring it down and by how much. Do not change them; the owner does, in the Notion Decisions table.
Every assembly drawing numbers each part and says PRINTED or PURCHASED with its cost. Costs go to the Notion Cost Scenarios database when the owner approves the build.

## Copy before you engineer (every hardware design)
Before designing anything, find a working example built by someone who has flown or fired it (BPS.space, JRD Propulsion, university teams with results, forum builds with photos). Copy its layout and materials. Justify every departure in one line, and keep the parts count and cost at or below the example's. Requirements-driven design from scratch is the last resort, not the first step, and it has to say why no working example applied. The stand v2 (hardware/test-stand-v2) is the cautionary case: 36 parts and CAD 562 for a job BPS.space does with plywood and one load cell.
