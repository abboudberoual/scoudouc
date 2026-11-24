# Working rules for agents in this repo (The Spirit of Scoudouc)

## Goal
Launch and land a small solid-fuel rocket under thrust, as fast and cheaply as possible, while the owner learns each system. Keep token use low.

## Model selection (pick the cheapest that can do the job) — tiers, see ops/agent-operating-model.md
- **code (tier 0)**: sims, parsers, BOM math, tests, metrics. If a program can do it, no model touches it.
- **local (tier 1)**: extraction, conversion, drafts, small boilerplate against tests — written as a job to `jobs/` (schema `ops/schemas/job.schema.json`), run by the owner's machine, never trusted without the job's acceptance check. A local model never decides to escalate; escalation is mechanical.
- **haiku**: grading local results (clean context: diff + ticket only), web research, summaries, link checks, log parsing, plotting; on the owner's laptop also the volunteer for code.
- **sonnet**: tickets and acceptance tests, firmware, simulator code, test procedures, CAD scripts, docs/learning explainers.
- **opus / fable**: control-loop design, landing-burn timing, pyro circuit safety review, regulatory text, any decision that is expensive to redo. Use sparingly.
- Report the tokens the platform shows (never an estimate) in every run record and append the events to `metrics/events.csv` (`ops/metrics.md`).

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
Read, in this order, before doing anything else: `ops/agent-operating-model.md`; Mission Control (https://claude.ai/artifact/VjUxjh3WCvrnCw8MNwbxfD): `program/brief`, then the `tickets` collection ("Needs your call" = decision tickets `open` and `needs_info`). A decision ticket `approved` / `rejected` is the owner's ruling: update the matching docs/decisions file status, unblock or re-plan the dependent tickets (`depends_on`), and never re-ask it in chat. Decisions are made on Mission Control or in chat ("approve T-003"); the session records them on the ticket. The Notion hub is read-only history since 2026-11-23.

## Session end ("wrap up")
Commit and push (never to `main` except `library:` / `repair:` / `docs: changelog` commits); update ticket statuses and `program/brief` on Mission Control; write the run record (`runs/<date>-<agent>`) with the tokens the platform reports; append events to `metrics/events.csv`; rewrite the Project handoff doc (`claude/project-map.md`) so the next chat starts cold without losing anything.

## Governance
`ops/` is canonical: operating model, prompts, playbooks, schemas, measurement definitions, local tooling. Approved tickets become PRs on `ticket/T-NNN-slug`; the owner merges. Never: spend, buy, launch, fire, contact regulators/suppliers/landowners/sellers, change safety procedures or pyro code outside an approved ticket, create or change scheduled tasks, delete tickets or events.

## Cost loop (every hardware deliverable)
Every design that will be bought or built ships with a `costing.md` beside it, and the loop runs in this order:
1. **Cost it**: full BOM in CAD, Canadian sources, estimates marked. Split PRINTED vs PURCHASED.
2. **Rank the drivers**: top five line items with % of total.
3. **Reduce**: for each driver, concrete alternatives with the saving and what it costs us (capability, time, risk). Take the ones that keep the requirement. Give the reduced total.
4. **Escalate**: if still over the budget line for that item, list which earlier decisions (by number) would bring it down and by how much. Do not change them; the owner does, in the Notion Decisions table.
Every assembly drawing numbers each part and says PRINTED or PURCHASED with its cost. Costs go to the Notion Cost Scenarios database when the owner approves the build.

## Copy before you engineer (every hardware design)
Before designing anything, find a working example built by someone who has flown or fired it (BPS.space, JRD Propulsion, university teams with results, forum builds with photos). Copy its layout and materials. Justify every departure in one line, and keep the parts count and cost at or below the example's. Requirements-driven design from scratch is the last resort, not the first step, and it has to say why no working example applied. The stand v2 (hardware/test-stand-v2) is the cautionary case: 36 parts and CAD 562 for a job BPS.space does with plywood and one load cell.
