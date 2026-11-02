"""Plots and the Monte Carlo helper."""
from __future__ import annotations

import math
import random
from dataclasses import replace
from typing import Callable, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .sim import MissionConfig, run_mission


def plot_flight(log: dict, path: str, title: str = "Flight") -> None:
    """Tilt, altitude and speed against time (with thrust shaded lightly)."""
    fig, ax = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    t = log["t_s"]
    ax[0].plot(t, log["tilt_deg"], label="tilt", color="#1f77b4")
    ax[0].plot(t, log["gimbal_deg"], label="gimbal angle", color="#d62728", lw=1)
    ax[0].axhline(0, color="gray", lw=0.5)
    ax[0].set_ylabel("degrees")
    ax[0].legend(loc="upper right")
    ax[1].plot(t, log["z_m"], color="#2ca02c")
    ax[1].set_ylabel("altitude (m)")
    ax[2].plot(t, log["speed_mps"], color="#9467bd", label="speed")
    ax[2].plot(t, log["vz_mps"], color="#7f7f7f", lw=1, label="vertical velocity")
    ax[2].set_ylabel("m/s")
    ax[2].set_xlabel("time (s)")
    ax[2].legend(loc="upper right")
    for a in ax:
        a.grid(alpha=0.3)
        a2 = a.twinx()
        a2.fill_between(t, log["thrust_n"], color="orange", alpha=0.12)
        a2.set_yticks([])
    ax[0].set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def landing_success(summary) -> bool:
    """Landing success: touchdown speed < 2 m/s and tilt < 10 degrees."""
    return (summary.touched_down and summary.touchdown_speed_mps < 2.0
            and summary.touchdown_tilt_deg < 10.0)


def monte_carlo(make_config: Callable[[float, float, float], MissionConfig], n: int = 100,
                seed: int = 1, scale_range=(0.85, 1.15), tilt_range_deg=(-5.0, 5.0),
                success_fn: Callable = landing_success) -> Dict:
    """Run n flights. make_config(scale_a, scale_b, initial_tilt_deg) builds each case.
    Each motor gets its own thrust scale. Returns per-case lists and the success rate."""
    rng = random.Random(seed)
    cases: List[dict] = []
    ok = 0
    for _ in range(n):
        sa, sb = rng.uniform(*scale_range), rng.uniform(*scale_range)
        tilt0 = rng.uniform(*tilt_range_deg)
        summary, _ = run_mission(make_config(sa, sb, tilt0))
        good = bool(success_fn(summary))
        ok += good
        cases.append(dict(scale_a=sa, scale_b=sb, tilt0_deg=tilt0, success=good,
                          **summary.as_dict()))
    return dict(n=n, successes=ok, success_rate=ok / n, cases=cases)


def plot_monte_carlo(result: dict, path: str, title: str = "Monte Carlo") -> None:
    cases = result["cases"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for good, color, lab in ((True, "#2ca02c", "success"), (False, "#d62728", "fail")):
        pts = [c for c in cases if c["success"] == good]
        ax[0].scatter([c["scale_b"] for c in pts], [c["touchdown_speed_mps"] for c in pts],
                      s=14, color=color, label=lab)
        ax[1].scatter([c["scale_a"] for c in pts], [c["apogee_m"] for c in pts],
                      s=14, color=color, label=lab)
    ax[0].axhline(2.0, color="gray", ls="--", lw=0.8)
    ax[0].set_xlabel("landing motor thrust scale")
    ax[0].set_ylabel("touchdown speed (m/s)")
    ax[1].set_xlabel("boost motor thrust scale")
    ax[1].set_ylabel("apogee (m)")
    ax[0].legend()
    fig.suptitle(f"{title}: {result['successes']}/{result['n']} success "
                 f"({100 * result['success_rate']:.0f}%)")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
