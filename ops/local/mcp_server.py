#!/usr/bin/env python3
"""Local MCP server: lets a Claude Code builder hand a job to the volunteer tier synchronously.

Tools: run(job_json) -> result summary; status(job_id) -> result.json if present; batch(jobs) -> summaries.
Transport: stdio (register in .mcp.json). Requires the `mcp` package: pip install mcp

Everything returned to the orchestrator is the result's summary + paths, never raw output.
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # keep the file importable for tests without the package
    FastMCP = None


def _run(job: dict) -> dict:
    path = os.path.join(ROOT, "jobs", f"{job['id']}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(job, f, indent=2)
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "local", "run_job.py"), path], cwd=ROOT, capture_output=True, text=True)
    return _status(job["id"]) or {"job": job["id"], "status": "fail", "summary": proc.stderr[-800:]}


def _status(job_id: str):
    p = os.path.join(ROOT, "results", job_id, "result.json")
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        r = json.load(f)
    return {k: r.get(k) for k in ("job", "status", "summary", "output_path", "acceptance_output_path", "attempts", "cost", "escalation_reason")}


if FastMCP:
    mcp = FastMCP("scoudouc-local")

    @mcp.tool()
    def run(job_json: str) -> str:
        """Run one job (JSON per ops/schemas/job.schema.json) on the local tier and return its summary."""
        return json.dumps(_run(json.loads(job_json)))

    @mcp.tool()
    def status(job_id: str) -> str:
        """Return the result summary for a job id, or 'pending'."""
        s = _status(job_id)
        return json.dumps(s) if s else "pending"

    @mcp.tool()
    def batch(jobs_json: str) -> str:
        """Run several jobs in sequence (one model resident) and return their summaries."""
        return json.dumps([_run(j) for j in json.loads(jobs_json)])

    if __name__ == "__main__":
        mcp.run()
else:
    if __name__ == "__main__":
        print("pip install mcp to run the server", file=sys.stderr)
        sys.exit(1)
