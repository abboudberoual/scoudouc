# Scoudouc — Agent Operating Model (v0.1, 2026-11-23)

*Who does what, what runs without asking, and what always waits for the owner. Adapted from Alchemy's operating model v0.8 (`abboudberoual/alchemy`, `ops/agent-operating-model.md`). "Mission Control" (https://claude.ai/artifact/VjUxjh3WCvrnCw8MNwbxfD) is the shared register: tickets, runs, metrics, surprises, program brief, agents. Its database is what the agents read and write. The Notion hub is read-only from 2026-11-23.*

## Architecture — builders, a brain, and volunteers

| Side | Runs as | Has | Does | Never needs |
|---|---|---|---|---|
| **Builders** | Claude Code scheduled tasks bound to this repo (claude.ai/code/routines → repository `abboudberoual/scoudouc`, environment `Scoudouc`) | The repo cloned + GitHub credentials, web, the dashboard tool, the local MCP server when the owner's machine is on | Library commits to `main`; approved tickets → PRs; CI; dispatch local-tier work to `jobs/`; report every run to Mission Control | Project docs |
| **Brain** | Thursday scheduled task + chats inside the claude.ai Project "VTOL Rocket build" | Project docs, web, the dashboard tool | Weekly audit of the builders from their reports, ticket grooming, program brief (clock, unknowns, next test), weekly metrics write-back, escalations | GitHub |
| **Volunteers** | The owner's machine: a daemon over `jobs/` running local models (Ollama) and tier-0 code; later a lab GPU via Slurm | The repo, the library, the simulator | Extraction, conversion, drafts, sim sweeps, small code against tests; results to `results/<id>/` on a branch | Decisions; anything without a mechanical check |

**The contract is Mission Control.** Builders write run records, metrics and ticket updates; the brain writes tickets and the brief; the owner approves on the board or in chat. **The ticket is the whole interface** between tiers (`ops/schemas/ticket.schema.json`): goal, inputs, output schema, acceptance test, budget, mechanical `escalate_if`. Each side degrades alone: a builder without the dashboard leaves its record in `ops/runs/`; a brain outage never stops the build; a daemon that is off leaves `jobs/` waiting and the builder does the ticket on Haiku instead.

## Tiers (the cheapest token is the one not spent)

| Tier | Who | Does | Never |
|---|---|---|---|
| 0 | code | sims, parsers, BOM math, tests, metrics | — |
| 1 | local models (`qwen3:8b`, `gemma4:e4b` on the Summit E16; bigger on a lab GPU) | extraction, conversion, drafts, small boilerplate against tests | decide to escalate; touch safety/regulatory text unreviewed; write to `main` |
| 2 | Haiku | grade tier-1 results against the ticket (clean context: diff + ticket only); on the laptop, also the volunteer for code | plan |
| 3 | Sonnet | decompose, write tickets + acceptance tests, build, integrate | judge ambiguous physics |
| 4 | Opus | decisions, landing-burn logic review, pyro safety review, regulatory text, disagreements between tiers | bulk anything |

Escalation is mechanical: test fails twice, schema invalid, budget exhausted, or the ticket's `escalate_if`. A local model never decides to escalate. Writes are single-threaded: one code builder, ≤3 PRs per night, each on its own branch.

## Where things live

| What | Where | Who writes |
|---|---|---|
| Simulator, firmware, CAD scripts, tests | repo `sim/`, `firmware/`, `hardware/` | Agents via PR only; owner directly |
| The library (motors, materials, vendors, rules-as-code) | repo `data/library/` | Library builder commits to `main` (`library:` prefix); two sources per value |
| Decisions | repo `docs/decisions/NNN-*.md` + Mission Control decision ticket T-NNN | Agents draft; owner decides |
| Playbooks, this model, prompts, schemas, local tooling | repo `ops/` (**canonical**; the Project holds pointers) | Owner directly; builders only via an approved-ticket PR |
| Tickets, runs, metrics, surprises, brief | Mission Control database | Agents + owner (buttons) |
| Local job queue | repo `jobs/` (in), `results/` (out, on a branch) | Builders write jobs; the daemon writes results |
| Event log for measurement | `metrics/events.csv` (append-only) + Mission Control `metrics/weekly` | Builders and daemon append; `ops/metrics/compute.py` computes |

CI runs the simulator tests and `data/library` validation on every PR and push to `main`. **The repo is canonical.** Anything that disagrees with the repo is stale.

## Operating principle — bias to action
Progress means the rocket's assets advanced: verified library data, sim success rates, printed parts, passing tests, open PRs, a truer board. `priority: build | deferred`; a `deferred` ticket is re-raised only when it concretely blocks a build step. Copy before you engineer (CLAUDE.md): every hardware design starts from a working example.

## Approval means execution
When the owner approves a ticket on Mission Control (or says so in chat: "approve T-003", "T-007: plywood"), the work starts that night.

| Ticket kind | What the agent does | Human gate |
|---|---|---|
| Sim / code / CAD / docs / playbook with a sufficient spec | Branch `ticket/T-NNN-slug` from fresh `main` → implement → run every check → push → PR → ticket `in_review` with the PR link | **Owner merges.** Nothing merges itself. |
| Library entries with sources | `library:` commit to `main` after validation | CI; Thursday spot-check |
| Local-tier work | `jobs/<id>.json` → daemon → `results/<id>/` on branch `results/T-NNN` → Haiku grades → builder integrates | Mechanical check + grade |
| Spec insufficient or conflicting | `needs_info` + ONE precise question | Owner answers in chat or on the board |
| Spend, purchase, launch, tethered test, regulatory or landowner contact, schedule change | Leaves `open`/`in_progress`, owner `owner`, note why | Owner executes |

## Roster (ET, overnight)
| Agent | Schedule | Model | Owns |
|---|---|---|---|
| sim-builder | nightly 02:37 | Sonnet | approved sim tickets; sweeps; `metrics/sim`; mass budget check (`metrics/mass`) |
| library-builder | nightly 03:17 | Sonnet, dispatching tier 0/1 via `jobs/` | motors, materials, vendors + Canadian stock, rules-as-code; `snapshots/library` |
| code-builder | nightly 04:17 | Sonnet | approved code/CAD/firmware/docs tickets → PRs (≤3, sequenced, isolated, CI-gated); PR reconciliation |
| procurement | nightly 05:07 | Sonnet | `buy` tickets: new price + lead time, used-market scout where eligible, recommendation (never contacts sellers) |
| retry | nightly 05:37 | Sonnet | reads the night's run records, repairs tooling, continues |
| local-daemon | continuous while the machine is on | local models + code | `jobs/` queue |
| orchestrator (brain) | Thursdays 03:37 | Sonnet; Opus for verdict-grade items | audit from reports + one library spot-check; PR reconciliation; grooming; program brief; `compute.py` → `metrics/weekly`; weekly status → Project doc `claude/orchestrator-log.md` |

## Autonomy matrix
**Runs without asking:** everything a playbook prescribes (library verification with two sources, sim reruns, changelog entries, `library:` commits); implementing **approved** tickets on a ticket branch and opening the PR; addressing review comments on that branch; creating/advancing/closing `auto` tickets; Mission Control upkeep; writing `jobs/`; grading results; replacing a dead source URL for a run's own work.

**Never without the owner's approval (a `decision` ticket):** spending money or buying anything (motors: NRCan 80 N·s per order); any launch, hop, tethered or drop test; any static fire; any change to the vehicle mass cap or motor class; any regulatory, SIM, supplier or landowner correspondence; any change to a safety procedure, the pyro circuit, or igniter code; creating accounts; publishing outside the repo/board/Project; changing engine code, tests, CI, playbooks, this model or prompts outside an approved ticket's PR; merging any PR; force-pushing; creating/changing/deleting scheduled tasks; deleting data (tickets never deleted; event log append-only).

**Escalation:** open `build` decisions and `needs_info` questions lead Mission Control ("Needs your call"); open PRs lead the weekly status; `build` decisions older than 14 days are re-raised by the orchestrator; two nights without execution of an `approved` ticket, or two blocked runs in a row, is a build-priority infra ticket.

## Ticket register (Mission Control `tickets`)
`{id: T-NNN, title, type: auto|decision|buy, area: data|engine|infra|product|legal, status: open|in_progress|blocked|in_review|needs_info|approved|rejected|done, priority: build|deferred, owner: owner|sim-builder|library-builder|code-builder|procurement|orchestrator, vehicle: Program|S0..S4, tier: code|local|haiku|sonnet|opus, size: S|M|L, critical: bool, opened, note, recommended?, options?, pr?, question?, decided?: {at, via, by}, depends_on?, sequence?, repo_file?, buy?: {part, qty, spec, new_price, new_lead_days, vendor, used_eligible, max_distance_km, min_savings_pct, deadline}}`. Ids sequential; never deleted; `in_review` always carries `pr`; `needs_info` always carries `question`. `size` is set by the manager at creation, never by the worker (velocity guard). `critical: true` marks the critical path. **Every engineering `decision` ticket carries `matrix`** (schema in `ops/schemas/ticket.schema.json`): weighted criteria, 1–5 scores with the fact behind each, sensitivity, open items; the same numbers as the `docs/decisions/NNN` file. Mission Control renders it; the owner judges from it.

## Measurement (`ops/metrics.md`)
Six metrics, each with a baseline: frontier tokens per merged PR (B0 session 1 = 1.22M/12 runs; B1 shadow runs 10 %); cost per ticket (B2 counterfactual); cycle time; size-weighted velocity; first-pass yield per tier × task type; the program clock vs floor (≈4 wk) vs reference class (7 yr, 3 yr). Logged by machines, computed by `ops/metrics/compute.py`, shown on the board with baselines.

## Weekly rhythm
- **Every night** — sim 02:37 → library 03:17 → code 04:17 → procurement 05:07 → retry 05:37. Sim reruns whenever `data/library/motors.json`, the mass budget or `sim/` change.
- **Thursday 03:37** — orchestrator: audit + spot-check → PR reconciliation → decisions → grooming → brief → metrics → weekly status.
- **Owner, anytime** — open Mission Control, press Approve/Reject, answer questions, merge PRs, fly, log hours/dollars/surprises.
