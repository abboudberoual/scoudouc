# Measurement definitions (v1, 2026-11-23) — pre-registered, append-only

Changing a definition here is a new version with a new name (`v2`), never a rewrite. Numbers computed under v1 stay v1.

## Event log: `metrics/events.csv`
Append-only. One row per event. Header:

```
ts,ticket,vehicle,tier,task_type,size,actor,event,tokens_in,tokens_out,cache_read,model_cost_usd,wall_seconds,energy_wh,pass,notes
```

- `ts` ISO-8601 UTC. `actor`: model name (`claude-sonnet-5-5`, `qwen3:8b`), `owner`, or `code`.
- `event`: opened | approved | started | result | graded | escalated | pr_opened | ci_green | merged | rejected | needs_info | surprise | owner_minutes | shadow_result.
- `tokens_*` from the platform's usage report or Ollama's counters; never estimated. Empty if unavailable, with `notes=usage_unavailable`.
- `energy_wh` = laptop wattage (measured once with a plug meter; default 40 W until measured) × wall_seconds / 3600, local tier only.
- `pass` 1/0 for result, graded, ci_green events.
- `owner_minutes` rows carry the minutes in `wall_seconds` (×60) and `actor=owner`.

## Owner values (set once, change = new version)
`OWNER_HOURLY_CAD = [to set]`, `MAX_PICKUP_KM = [to set]`, `MIN_SAVINGS_PCT = [to set]`, `LAPTOP_WATTS = 40`, `ELECTRICITY_CAD_PER_KWH = 0.08`.

## The six metrics
| # | Metric | Definition | Baseline |
|---|---|---|---|
| 1 | Frontier tokens per merged PR | Σ(tokens_in + tokens_out) of events with actor starting `claude-` over all tickets whose PR merged that week ÷ merged PRs. Also per closed ticket. | B0: session 1 = 1,220,000 tokens / 12 runs ≈ 101,700 per run. B1: shadow runs. |
| 2 | Cost per ticket (CAD) | frontier model_cost_usd × FX + energy_wh/1000 × ELECTRICITY, per closed ticket | B2 counterfactual: local tokens consumed − grading tokens, priced at the Sonnet rate |
| 3 | Cycle time | approved → done, median and p90, by size | first month = own baseline; Alchemy tickets when available |
| 4 | Velocity | merged PRs/week and closed tickets/week, size-weighted S=1 M=3 L=8 | first month |
| 5 | First-pass yield | result events with pass=1 ÷ result events, per tier × task_type; escalation rate = escalated ÷ started | B1 shadow (same tickets on Sonnet) |
| 6 | Program clock | Σ owner hours, Σ dollars, weeks since 2026-11-07 vs floor 4 wk vs reference class 7 yr / 3 yr | B3 reference class |

## Baselines
- **B0 historical:** session 1 of Scoudouc (1.22M tokens, 12 runs); Alchemy nightly run costs when exported.
- **B1 shadow runs:** every ticket whose id number ends in 0 (≈10 %) is also executed single-tier on Sonnet in a sandbox branch `shadow/T-NNN`, never merged; its events carry `event=shadow_result`. Weekly budget cap: 150k tokens.
- **B2 counterfactual:** for each local-tier result, saved tokens ≈ prompt + completion tokens of the local run minus the grading tokens; the per-task-type factor is calibrated monthly from B1 pairs.
- **B3 reference class:** 7 yr (BPS.space, 2015–2022), 3 yr (JRD Propulsion, 2021–2024); floor ≈ 4 weeks for a fully known design.

## Goodhart guards
`size` is set at ticket creation by the manager (Sonnet) with a one-line rationale and sampled weekly; velocity is size-weighted; a ticket split after creation keeps its original size on the parent.

## Output: `metrics/weekly` on Mission Control
`{week: "2026-W48", computed_at, metrics: [{name, value, baseline, baseline_kind, delta}], notes}` written only by `ops/metrics/compute.py`.
