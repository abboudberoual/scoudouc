# ops/ — the agents' home (canonical)

- `agent-operating-model.md` — governance: builders, brain, volunteers, tiers, autonomy matrix, roster.
- `prompts/` — scheduled-task prompts. Builders are created at claude.ai/code/routines bound to this repo and the `Scoudouc` environment; the orchestrator runs inside the claude.ai Project. `builder-common.md` is read by every builder first.
- `playbook-library.md`, `playbook-sim-regression.md` — what runs without asking.
- `metrics.md` — pre-registered measurement definitions (v1). `metrics/compute.py` computes `metrics/weekly` from `metrics/events.csv`.
- `schemas/` — ticket, job and result schemas: the whole interface between tiers.
- `local/` — the volunteer tier: `run_job.py` (one job), `daemon.py` (loop over `jobs/`, results to `results/<ticket>` branches), `mcp_server.py` (sync channel for builders; register in `.mcp.json`).
- `runs/` — fallback run records when the dashboard is unreachable.

Mission Control: https://claude.ai/artifact/VjUxjh3WCvrnCw8MNwbxfD

## Cloud environment `Scoudouc` (created 23 Nov)
Setup script installs `numpy matplotlib pytest trimesh manifold3d scipy networkx 'mcp<2' platformio` and runs the sim tests. `mcp<2` because `ops/local/mcp_server.py` uses `FastMCP` (renamed in mcp 2.x). Network: package registries + PlatformIO registry + github.com/objects + dl.espressif.com. `MPLBACKEND=Agg`, PlatformIO telemetry off. The `scoudouc-local` MCP server fails to connect in the cloud by design (it needs the owner's Ollama); builders treat that as "machine off".

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

## Scoudouc cloud environment and scheduled tasks
Environment `Scoudouc`: `env_01Dju6okZfThB68J4rHMsGE8`. Tasks (America/Toronto): sim-builder `trig_015nRGDgXzbojNaB4KTGVvWs` 02:37 · library-builder `trig_01JTZr9pZf8h9R92V1RYrYT8` 03:17 · code-builder `trig_013YTKt4DfKbjvPrEAPeUU8m` 04:17 · procurement `trig_01BxCwD16GChSPWwmpHTRnM4` 05:07 · retry `trig_01X7gyu7SHptL5U7aZMiMt8A` 05:37 · orchestrator `trig_01K44urE9G6gSrdQHh6J4GLo` Thu 03:37. Each task's prompt is its file in `ops/prompts/`; change the file by PR, then update the task's prompt to match.
