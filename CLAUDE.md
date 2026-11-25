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
- **Every part and vehicle has a 3D render** (owner's rule, 23 Nov): a CadQuery script in `hardware/cad/` that exports STEP + GLB and shaded PNGs via `hardware/cad/render.py` (orange PRINTED, navy PURCHASED, grey not-in-kit), regenerated whenever the geometry changes, and registered on Mission Control (`parts/<id>` with the render asset) so the board shows what is being built. Concept renders are labelled CONCEPT; the numbered callout drawing stays the drawing of record.

## Design for the tools on hand (owner's rule, 25 Nov)
Designs use the owner's tools (`ops/owner-tools.md`: today only hex keys, calipers, multimeter, square, tape, scale; no drill, saw or soldering iron; no workshop), printed parts, and pre-made or pre-drilled hardware. A design that needs a missing tool says which tool, what it unblocks and the cheapest way to avoid it; unavoidable tools go on the one ranked buy list there (ordered by critical-path work unblocked, then price), never one at a time.

## Every build has a printable guide (owner's rule, 25 Nov)
Anything the owner assembles ships with an illustrated, printable PDF step-by-step guide built by `hardware/guides/` (reference: G-001, thrust stand v3): per-step renders with the new parts highlighted and numbered, parts and tools per step, a check list per step, have/buy list, 1:1 templates where something is marked out, torque table, build record. Regenerate it whenever the geometry or the parts change.

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

## Requirement before hardware (owner's rule, 23 Nov)
Every vehicle, mode or test article starts from a written test requirement, before any motor, mass or geometry is chosen: **prove what** (the one claim), **measured how** (the logged signal and the pass/fail number), **how much powered time and how many flights** that needs, and the margin. Motor, mass and airframe are then derived from it and the derivation is shown (simulator run or hand calculation, with the numbers). A decision that picks hardware without the requirement on top is not ready for the owner. Example: proving TVC needs ≥ 2 s of burn at a sustain thrust-to-weight ≥ 2 and ≥ 3 flights, which rules out the C6 and D12 on any vehicle that carries the avionics.

## Mass budget only when needed (owner's rule, 23 Nov)
No mass budget is built or maintained ahead of need. Mass is an envelope derived from the test requirement (e.g. sustain TWR ≥ 2 on the chosen motor → max mass); an itemised budget is made only when a ticket asks for one for a vehicle that is about to be built, so it is not recalculated every time a decision moves. `docs/mass-budget.*` is historical until then.

## Copy the state of the art (every hardware design and engineering decision)
We start with more than the people before us, so we start where they finished, not where they started. Before designing anything, find the most recent working example built by someone who has flown or fired it (BPS.space, JRD Propulsion, university teams with results, forum builds with photos) and copy its **final, flown** solution, not its early iterations: e.g. BPS landed Scout F with a thrust-blocking throttle after timing-only ignition proved unrepeatable, so timing-only is a step back, not a starting point. Copy its layout and materials. Justify every departure in one line, and keep the parts count and cost at or below the example's. Any option that repeats an approach the example already abandoned must say why it will work for us. Then add what is newer than the example (parts, sensors, tools) only where it removes a known failure. Requirements-driven design from scratch is the last resort and has to say why no working example applied. The stand v2 (hardware/test-stand-v2) is the cautionary case: 36 parts and CAD 562 for a job BPS.space does with an aluminium-extrusion box and one load cell.
