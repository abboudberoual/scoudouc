"""T-010 follow-up: landing success vs landing-motor thrust spread (integrating trigger,
E12 up / E12 down). Answers: how repeatable must the motor be for timing alone to work?
Run from the repo root:  python sim/examples/t010_spread.py [--n 150]
Writes data/sim/t010_success_vs_spread.csv and .png.
"""
import argparse, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from t010_sweep import cases, OUT  # noqa: E402
from scoudouc_sim.plots import monte_carlo  # noqa: E402
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SPREADS_PCT = (0, 1, 2, 3, 5, 10, 15)

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=150)
a = ap.parse_args()
rows = []
for meta, make in cases(None):
    if meta["motor"] != "E12/E12" or meta["trigger"] != "integrating":
        continue
    for s in SPREADS_PCT:
        r = monte_carlo(make, n=a.n, seed=11, scale_range=(1 - s / 100, 1 + s / 100))
        rows.append(dict(meta, landing_spread_pct=s, boost_spread_pct=s, n=a.n,
                         success_rate=round(r["success_rate"], 3)))
        print(rows[-1])
with open(os.path.join(OUT, "t010_success_vs_spread.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
fig, ax = plt.subplots(figsize=(6, 4))
for mass, color in ((660, "#e86f2c"), (750, "#141c2b")):
    pts = [r for r in rows if r["mass_g"] == mass]
    ax.plot([r["landing_spread_pct"] for r in pts], [100 * r["success_rate"] for r in pts],
            "o-", color=color, label=f"{mass} g")
ax.axhline(70, color="#8a97a8", ls="--", lw=0.8); ax.text(9, 72, "70 % line (T-010)", fontsize=8)
ax.set_xlabel("motor-to-motor thrust spread, +/- %"); ax.set_ylabel("landing success (%)")
ax.set_title("Timing-only landing vs motor repeatability (E12/E12)")
ax.grid(alpha=0.3); ax.legend(); fig.tight_layout()
fig.savefig(os.path.join(OUT, "t010_success_vs_spread.png"), dpi=120)
