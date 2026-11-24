# ops/ — the agents' home (canonical)

- `agent-operating-model.md` — governance: builders, brain, volunteers, tiers, autonomy matrix, roster.
- `prompts/` — scheduled-task prompts. Builders are created at claude.ai/code/routines bound to this repo and the `Scoudouc` environment; the orchestrator runs inside the claude.ai Project. `builder-common.md` is read by every builder first.
- `playbook-library.md`, `playbook-sim-regression.md` — what runs without asking.
- `metrics.md` — pre-registered measurement definitions (v1). `metrics/compute.py` computes `metrics/weekly` from `metrics/events.csv`.
- `schemas/` — ticket, job and result schemas: the whole interface between tiers.
- `local/` — the volunteer tier: `run_job.py` (one job), `daemon.py` (loop over `jobs/`, results to `results/<ticket>` branches), `mcp_server.py` (sync channel for builders; register in `.mcp.json`).
- `runs/` — fallback run records when the dashboard is unreachable.

Mission Control: https://claude.ai/artifact/VjUxjh3WCvrnCw8MNwbxfD

## Local setup (owner's machine, Windows, 16 GB, no dGPU)
```
winget install Ollama.Ollama
ollama pull qwen3:8b
ollama pull gemma4:e4b
pip install mcp
python ops/local/daemon.py --once      # run one queued job
python ops/local/daemon.py             # loop (leave running overnight; power: lid-close = nothing, no sleep)
```
Energy accounting uses `SCOUDOUC_WATTS` (default 40); measure once with a plug meter.
