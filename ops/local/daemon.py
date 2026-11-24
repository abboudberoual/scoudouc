#!/usr/bin/env python3
"""The volunteer daemon: loops over jobs/, runs each with run_job.py, commits results to a branch.

Usage: python ops/local/daemon.py [--once] [--model qwen3:8b] [--interval 60]

Priority: jobs whose ticket is marked critical first (the builder writes "critical": true into the
job), then oldest. Jobs flagged needs_browser are skipped here (a scheduled task with Claude in
Chrome handles them). One job at a time: one model resident, memory stays bounded.

Results go to branch results/<ticket> and are pushed; the nightly builder grades and integrates.
Never touches main.
"""
import argparse, glob, json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def sh(cmd, check=True):
    return subprocess.run(cmd, shell=True, cwd=ROOT, check=check, capture_output=True, text=True)


def queued_jobs():
    jobs = []
    for p in glob.glob(os.path.join(ROOT, "jobs", "*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                j = json.load(f)
        except Exception:
            continue
        if j.get("status", "queued") != "queued" or j.get("needs_browser"):
            continue
        jobs.append((0 if j.get("critical") else 1, j.get("created_at", ""), p, j))
    jobs.sort()
    return [(p, j) for _, _, p, j in jobs]


def set_status(path, job, status):
    job["status"] = status
    with open(path, "w", encoding="utf-8") as f:
        json.dump(job, f, indent=2)


def run_one(path, job, model):
    ticket = job["ticket"]
    branch = f"results/{ticket}"
    sh("git fetch origin main", check=False)
    sh(f"git checkout -B {branch} origin/main", check=False)
    set_status(path, job, "running")
    cmd = f"{sys.executable} ops/local/run_job.py \"{path}\"" + (f" --model {model}" if model else "")
    proc = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
    ok = proc.returncode == 0
    set_status(path, job, "done" if ok else "failed")
    sh(f"git add results/{job['id']} jobs/{os.path.basename(path)} metrics/events.csv", check=False)
    sh(f"git commit -m \"results: {job['id']} ({'pass' if ok else job.get('status')})\"", check=False)
    sh(f"git -c push.negotiate=true push -u origin {branch}", check=False)
    print(proc.stdout.strip() or proc.stderr.strip()[-400:])
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--model", default=None)
    ap.add_argument("--interval", type=int, default=60)
    a = ap.parse_args()
    while True:
        sh("git fetch origin main && git checkout main && git pull --ff-only origin main", check=False)
        jobs = queued_jobs()
        if not jobs:
            if a.once:
                print("no queued jobs"); return 0
            time.sleep(a.interval); continue
        path, job = jobs[0]
        print(f"running {job['id']} ({job['type']}, tier {job['tier']})")
        run_one(path, job, a.model)
        if a.once:
            return 0


if __name__ == "__main__":
    sys.exit(main())
