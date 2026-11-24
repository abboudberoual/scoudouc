#!/usr/bin/env python3
"""Run one local job (tier 0 or tier 1) and write its result.

Usage: python ops/local/run_job.py jobs/T-011-1.json [--model qwen3:8b] [--ollama http://localhost:11434]

Tier 0 ("code"): runs the job's acceptance command as the work itself (sweeps, parsers).
Tier 1 ("local"): asks the local model for JSON constrained to output_schema, writes it to
output_path, runs the acceptance command, retries up to budget.attempts, then escalates
mechanically. The model never decides to escalate.

Memory discipline: inputs are chunked to context_limit_tokens (approx 4 chars/token); no file is
read whole into the prompt beyond that. One request at a time.
"""
import argparse, json, os, subprocess, sys, time, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAPTOP_WATTS = float(os.environ.get("SCOUDOUC_WATTS", "40"))


def now():
    return datetime.now(timezone.utc).isoformat()


def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def read_inputs(paths, limit_tokens):
    budget = limit_tokens * 4
    parts = []
    for rel in paths:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            parts.append(f"[missing input: {rel}]")
            continue
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        take = text[: max(0, budget - sum(len(x) for x in parts))]
        if len(take) < len(text):
            take += f"\n[truncated {rel} at context limit; chunk the input in a follow-up job]"
        parts.append(f"=== {rel} ===\n{take}")
        if sum(len(x) for x in parts) >= budget:
            break
    return "\n\n".join(parts)


def ollama_generate(base, model, prompt, schema):
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": schema,  # constrained decoding to the JSON schema
        "options": {"temperature": 0.1, "num_ctx": 8192},
        "keep_alive": "30m",
    }
    req = urllib.request.Request(f"{base}/api/generate", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        out = json.loads(r.read().decode())
    return out


def run_acceptance(cmd, log_path):
    with open(log_path, "w", encoding="utf-8") as log:
        proc = subprocess.run(cmd, shell=True, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    return proc.returncode == 0


def append_event(row):
    path = os.path.join(ROOT, "metrics", "events.csv")
    header = "ts,ticket,vehicle,tier,task_type,size,actor,event,tokens_in,tokens_out,cache_read,model_cost_usd,wall_seconds,energy_wh,pass,notes\n"
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write(header)
        f.write(",".join("" if v is None else str(v).replace(",", ";") for v in row) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job")
    ap.add_argument("--model", default=None)
    ap.add_argument("--ollama", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
    a = ap.parse_args()

    job = load_json(a.job)
    jid = job["id"]
    out_dir = os.path.join(ROOT, "results", jid)
    os.makedirs(out_dir, exist_ok=True)
    out_path = job.get("output_path") or f"results/{jid}/output.json"
    acc_log = os.path.join(out_dir, "acceptance.log")
    model = a.model or job.get("model_hint") or "qwen3:8b"
    attempts_allowed = int(job.get("budget", {}).get("attempts", 2))
    started = time.time()
    result = {"job": jid, "status": "fail", "output_path": out_path, "summary": "", "evidence": [], "attempts": 0,
              "acceptance_output_path": f"results/{jid}/acceptance.log", "cost": {"model": model, "prompt_tokens": 0, "completion_tokens": 0},
              "started_at": now()}

    missing = [rel for rel in job.get("inputs", []) if not os.path.exists(os.path.join(ROOT, rel))]
    if missing and job["tier"] != "code":
        # Never call a model without its inputs: a model asked to extract from nothing invents values
        # (observed 2026-11-23: T-011-1 produced a fabricated C6 that passed a shape-only check).
        result["status"] = "escalate"; result["escalation_reason"] = "missing_input: " + ", ".join(missing)
        result["summary"] = f"Not run: input(s) missing ({', '.join(missing)}). The builder must fetch them first."
        result["cost"]["model"] = "none"
    elif job["tier"] == "code":
        result["attempts"] = 1
        ok = run_acceptance(job["acceptance"], acc_log)
        result["status"] = "pass" if ok else "escalate"
        result["escalation_reason"] = None if ok else "acceptance_failed_tier0"
        result["summary"] = f"Tier-0 job ran `{job['acceptance']}`: {'pass' if ok else 'fail'}. See acceptance.log."
        result["cost"]["model"] = "code"
    else:
        inputs = read_inputs(job.get("inputs", []), int(job.get("context_limit_tokens", 8000)))
        schema = job["output_schema"]
        prompt = (f"You are a careful extraction worker for a model-rocket engineering program.\nGOAL: {job['goal']}\n"
                  f"Return ONLY JSON matching the given schema. Use null for anything not present in the inputs; never invent values. "
                  f"Include source_url fields where the schema has them.\n\nINPUTS:\n{inputs}\n")
        feedback = ""
        for attempt in range(1, attempts_allowed + 1):
            result["attempts"] = attempt
            try:
                out = ollama_generate(a.ollama, model, prompt + feedback, schema)
            except Exception as e:  # model server down
                result["status"] = "escalate"; result["escalation_reason"] = f"ollama_error: {e}"; break
            result["cost"]["prompt_tokens"] += int(out.get("prompt_eval_count", 0) or 0)
            result["cost"]["completion_tokens"] += int(out.get("eval_count", 0) or 0)
            try:
                data = json.loads(out.get("response", ""))
            except Exception:
                feedback = "\n\nPrevious attempt was not valid JSON. Return valid JSON only."
                if attempt == attempts_allowed:
                    result["status"] = "escalate"; result["escalation_reason"] = "schema_invalid"
                continue
            with open(os.path.join(ROOT, out_path), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if run_acceptance(job["acceptance"], acc_log):
                result["status"] = "pass"; break
            with open(acc_log, "r", encoding="utf-8", errors="replace") as f:
                tail = f.read()[-1500:]
            feedback = f"\n\nThe acceptance check failed with:\n{tail}\nFix the output."
            if attempt == attempts_allowed:
                result["status"] = "escalate"; result["escalation_reason"] = "acceptance_fails_twice"
        result["summary"] = (f"{job['type']} for {job['ticket']} on {model}: {result['status']} after {result['attempts']} attempt(s); "
                             f"{result['cost']['prompt_tokens']} prompt + {result['cost']['completion_tokens']} completion tokens. "
                             f"Output at {out_path}; acceptance log at results/{jid}/acceptance.log.")
        if result["status"] == "pass":
            try:
                with open(os.path.join(ROOT, out_path), "r", encoding="utf-8") as f:
                    d = json.load(f)
                n = len(d) if isinstance(d, (list, dict)) else 1
                result["summary"] += f" {n} top-level item(s)."
            except Exception:
                pass

    wall = time.time() - started
    result["cost"]["wall_seconds"] = round(wall, 1)
    result["cost"]["energy_wh"] = round(LAPTOP_WATTS * wall / 3600, 3)
    result["finished_at"] = now()
    with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    append_event([now(), job["ticket"], "", job["tier"], job["type"], "", result["cost"]["model"], "result",
                  result["cost"]["prompt_tokens"], result["cost"]["completion_tokens"], "", "", result["cost"]["wall_seconds"],
                  result["cost"]["energy_wh"], 1 if result["status"] == "pass" else 0, result.get("escalation_reason") or ""])
    print(json.dumps({"job": jid, "status": result["status"], "attempts": result["attempts"]}))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
