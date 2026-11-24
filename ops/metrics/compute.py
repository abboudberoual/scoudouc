#!/usr/bin/env python3
"""Compute the six weekly metrics from metrics/events.csv (definitions: ops/metrics.md v1).

Usage: python ops/metrics/compute.py [--week 2026-W48] [--json out.json]
Prints the metrics/weekly document. The orchestrator writes it to Mission Control; this script never
talks to the dashboard itself. Pure stdlib. Never backfills: a week is computed from the rows it has.
"""
import argparse, csv, json, os, statistics, sys
from collections import defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVENTS = os.path.join(ROOT, "metrics", "events.csv")
B0_TOKENS_PER_RUN = 1_220_000 / 12
SIZE_W = {"S": 1, "M": 3, "L": 8}
CLOCK_START = datetime(2026, 11, 7, tzinfo=timezone.utc)


def week_of(ts):
    d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def load():
    if not os.path.exists(EVENTS):
        return []
    with open(EVENTS, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def compute(rows, week):
    wk = [r for r in rows if r.get("ts") and week_of(r["ts"]) == week]
    by_ticket = defaultdict(list)
    for r in rows:
        by_ticket[r.get("ticket", "")].append(r)

    frontier = lambda r: str(r.get("actor", "")).startswith("claude")
    merged = {r["ticket"] for r in wk if r.get("event") == "merged"}
    closed = merged | {r["ticket"] for r in wk if r.get("event") in ("rejected",) }

    # 1. frontier tokens per merged PR
    ftoks = sum(num(r["tokens_in"]) + num(r["tokens_out"]) for t in merged for r in by_ticket[t] if frontier(r))
    m1 = ftoks / len(merged) if merged else None

    # 2. cost per closed ticket (USD model cost + energy)
    cost = sum(num(r["model_cost_usd"]) for t in closed for r in by_ticket[t]) + sum(num(r["energy_wh"]) for t in closed for r in by_ticket[t]) / 1000 * 0.08
    m2 = cost / len(closed) if closed else None
    local_toks = sum(num(r["tokens_in"]) + num(r["tokens_out"]) for r in wk if r.get("tier") == "local" and r.get("event") == "result")
    grade_toks = sum(num(r["tokens_in"]) + num(r["tokens_out"]) for r in wk if r.get("event") == "graded")
    b2_saved = max(0.0, local_toks - grade_toks)

    # 3. cycle time approved -> done, by size
    cycles = defaultdict(list)
    for t in merged:
        ev = {r["event"]: r["ts"] for r in by_ticket[t]}
        if "approved" in ev and "merged" in ev:
            a = datetime.fromisoformat(ev["approved"].replace("Z", "+00:00")); m = datetime.fromisoformat(ev["merged"].replace("Z", "+00:00"))
            size = next((r.get("size") for r in by_ticket[t] if r.get("size")), "M")
            cycles[size].append((m - a).total_seconds() / 86400)
    m3 = {s: {"median_days": round(statistics.median(v), 2), "p90_days": round(sorted(v)[int(0.9 * (len(v) - 1))], 2), "n": len(v)} for s, v in cycles.items()} or None

    # 4. velocity size-weighted
    m4 = sum(SIZE_W.get(next((r.get("size") for r in by_ticket[t] if r.get("size")), "M"), 3) for t in merged)

    # 5. first-pass yield per tier x task_type
    fpy = defaultdict(lambda: [0, 0])
    for r in wk:
        if r.get("event") == "result":
            k = f"{r.get('tier')}/{r.get('task_type')}"
            fpy[k][1] += 1; fpy[k][0] += 1 if r.get("pass") in ("1", "True", "true") else 0
    m5 = {k: round(v[0] / v[1], 3) for k, v in fpy.items() if v[1]} or None
    started = sum(1 for r in wk if r.get("event") == "started"); esc = sum(1 for r in wk if r.get("event") == "escalated")
    m5_esc = round(esc / started, 3) if started else None

    # 6. program clock
    hours = sum(num(r["wall_seconds"]) for r in rows if r.get("event") == "owner_minutes") / 3600
    dollars = sum(num(r["model_cost_usd"]) for r in rows if r.get("actor") == "owner" and r.get("event") == "spend")
    weeks = (datetime.now(timezone.utc) - CLOCK_START).days / 7

    return {
        "week": week, "computed_at": datetime.now(timezone.utc).isoformat(), "definitions": "ops/metrics.md v1",
        "metrics": [
            {"name": "Frontier tokens / merged PR", "value": None if m1 is None else round(m1), "baseline": round(B0_TOKENS_PER_RUN), "baseline_kind": "B0 session 1 per run", "delta": None if m1 is None else f"{(m1 / B0_TOKENS_PER_RUN - 1) * 100:+.0f}%"},
            {"name": "Cost / closed ticket (USD)", "value": None if m2 is None else round(m2, 3), "baseline": None, "baseline_kind": "B2 counterfactual", "delta": f"saved ~{round(b2_saved)} frontier tokens (B2)"},
            {"name": "Cycle time approved→merged", "value": m3, "baseline": None, "baseline_kind": "first month", "delta": None},
            {"name": "Velocity (size-weighted)", "value": m4, "baseline": None, "baseline_kind": "first month", "delta": None},
            {"name": "First-pass yield (tier/task)", "value": m5, "baseline": None, "baseline_kind": "B1 shadow", "delta": None if m5_esc is None else f"escalation rate {m5_esc}"},
            {"name": "Program clock", "value": f"{hours:.1f} h · ${dollars:.0f} · week {int(weeks) + 1}", "baseline": "floor 4 wk; reference 7 yr / 3 yr", "baseline_kind": "B3", "delta": None},
        ],
        "rows_in_week": len(wk),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    rows = load()
    week = a.week or week_of(datetime.now(timezone.utc).isoformat())
    out = compute(rows, week)
    s = json.dumps(out, indent=2)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            f.write(s)
    print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
