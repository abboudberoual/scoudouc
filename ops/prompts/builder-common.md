# Common rules for every Scoudouc builder (read first, every run)

You are a Claude Code scheduled task with the repo `abboudberoual/scoudouc` cloned. Governance: `ops/agent-operating-model.md` (binding). Safety and style: `CLAUDE.md`.

STEP ZERO: `git fetch origin && git checkout main && git pull`. Read `ops/agent-operating-model.md`, `CLAUDE.md`, `docs/START-HERE.md` if present, and the `tickets` collection on Mission Control (https://claude.ai/artifact/VjUxjh3WCvrnCw8MNwbxfD) via the ArtifactData tool (load with ToolSearch "ArtifactData"; on this server `db_list`/`db_get`/`db_query`/`db_write` with the artifact slug `e8ae5a35-6764-4e89-9c97-fdd9ce2bc2b4`). Pin every write with `if_version`; on conflict re-read and redo. Never delete tickets.

GIT HYGIENE: never commit to `main` except `library:` data commits (library-builder, and procurement for `data/library/used_prices.json` / `seller_flags.json` only), `repair:` tooling fixes, and `docs: changelog` reconciliations. Never leave work only on a session branch: a commit not on `main` must be on a branch with an open PR. Tickets build on `ticket/T-NNN-slug` from fresh `origin/main`. PRs via `gh`. Never merge. Never force-push. The PR body: ticket id, what changed, verification run (commands + results), simulation deltas, what was deliberately not done, review focus, `## Changelog entry`, and the attribution lines.

CHECKS before any push touching `sim/` or `data/library/`: `python -m pytest sim/tests -q` and `python data/library/validate.py` (once it exists). CI runs the same.

TIERS: you are tier 3. For extraction, conversion, drafts and sim sweeps, write a job (`ops/schemas/job.schema.json`) to `jobs/<ticket-id>-<n>.json` instead of doing it yourself; the local daemon (tier 0/1) returns `results/<id>/` on branch `results/T-NNN`. If a result is present, grade it: run its acceptance test; if it passes, integrate; if it fails, apply the job's `escalate_if` (rerun once, then do it on Haiku, then on yourself). Never read a worker's raw output into your context: read `result.json` summary + the files the acceptance test needs. If the machine is off (no result after one night), do the ticket on Haiku and note `tier_fallback: haiku`.

MEASUREMENT: append one row per event to `metrics/events.csv` (schema in `ops/metrics.md`) with the tokens your run report shows; commit it with your other changes. Never estimate your own tokens: use the usage the platform reports; if unavailable, write `tokens_in=,tokens_out=` empty and `notes=usage_unavailable`. A run with nothing else to commit (no-op) does not commit its row: it puts the rows in its run record as `events: [csv lines]`, and the next builder that commits (or the retry builder) appends them.

SELF-REPAIR: a tool or script that breaks for a reason inside `ops/local/`, `tools/` or `data/library/validate.py` may be fixed with a direct commit to `main` prefixed `repair:`; anything else is a ticket.

REPORT CONTRACT: at the end `set` `runs/{YYYY-MM-DD}-{agent}`: `{date, agent, at, mode: "repo", summary, head_commit, ci_main, built: [{ticket, pr, ci}], reconciled: [], skipped: [{ticket, why}], jobs_written: [], results_graded: [{job, pass}], tokens_in, tokens_out, cost_usd, repairs: []}` and update each ticket you touched. If the dashboard is unreachable, write the same JSON to `ops/runs/{date}-{agent}.json` and commit it. Finish with a concise report mirroring the summary.

NEVER: spend money, contact anyone outside the repo/board, fire or arm anything, change safety procedures or pyro code outside an approved ticket, create or change scheduled tasks, publish outside the repo and board.
