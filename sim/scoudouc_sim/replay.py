"""Replay a simulator log as an animation or a filmstrip.

The simulator writes a CSV per flight (t_s, x_m, z_m, tilt_deg, gimbal_deg, thrust_n, mass_kg ...).
This module draws the rocket at each moment: a body tilted by tilt_deg, a motor plume whose length
follows thrust_n and whose direction follows the gimbal, plus side panels for height, speed and tilt.

Usage:
    python -m scoudouc_sim.replay LOG.csv --mp4 out.mp4            # video, real time
    python -m scoudouc_sim.replay LOG.csv --gif out.gif --speed 0.5  # half-speed GIF
    python -m scoudouc_sim.replay LOG.csv --strip out.png --frames 8 # filmstrip of 8 moments
Nothing here fires anything; it only draws numbers the simulator already produced.
"""
import argparse
import csv
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Polygon, Rectangle, Circle

NAVY, ORANGE, BLUE, GREY, PAPER = "#141c2b", "#e86f2c", "#5b8db8", "#8a97a8", "#f4f1ea"


def load(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    cols = {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}
    return cols


def rocket_outline(x, z, tilt_deg, length_m, width_m):
    """Body polygon (nose at top) rotated by tilt about its base. Tilt is from vertical, +ve leans +x."""
    a = math.radians(tilt_deg)
    hw, L = width_m / 2, length_m
    pts = np.array([[-hw, 0], [hw, 0], [hw, 0.78 * L], [0, L], [-hw, 0.78 * L]])
    rot = np.array([[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]])  # lean toward +x
    return pts @ rot.T + [x, z]


def plume(x, z, tilt_deg, gimbal_deg, thrust_n, thrust_max, length_m):
    """Plume leaves the base in the gimbal direction. Length scales with thrust."""
    if thrust_n <= 0.05:
        return None
    a = math.radians(tilt_deg + gimbal_deg)
    plen = 0.35 * length_m * (0.3 + 0.7 * thrust_n / max(thrust_max, 1e-6))
    pw = 0.09 * length_m
    pts = np.array([[-pw, 0], [pw, 0], [0, -plen]])
    rot = np.array([[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]])
    return pts @ rot.T + [x, z]


def draw_scale(d, length_m):
    """Rocket drawn large enough to see: about 1/8 of the frame height, never smaller than life."""
    zmax = max(d["z_m"].max() * 1.15, 3 * length_m)
    return max(1.0, (zmax / 8) / length_m)


def make_figure(d, length_m=0.6, width_m=0.074, title=""):
    k = draw_scale(d, length_m); length_m, width_m = length_m * k, width_m * k
    t, x, z = d["t_s"], d["x_m"], d["z_m"]
    zmax = max(z.max() * 1.15, 3 * length_m)
    xr = max(abs(x).max() * 1.3, zmax * 0.45, 2 * length_m)

    fig = plt.figure(figsize=(12, 7), dpi=100, facecolor=PAPER)
    gs = fig.add_gridspec(3, 2, width_ratios=[1.15, 1], hspace=0.45, wspace=0.25,
                          left=0.06, right=0.98, top=0.9, bottom=0.08)
    ax = fig.add_subplot(gs[:, 0])
    ax.set_facecolor(PAPER)
    ax.set_xlim(-xr, xr); ax.set_ylim(-0.4 * length_m, zmax); ax.set_aspect("equal")
    ax.axhline(0, color=BLUE, lw=2)
    ax.plot(x, z, color=GREY, lw=1, ls="--", alpha=0.6)   # full path, faint
    ax.set_xlabel("sideways (m)"); ax.set_ylabel("height (m)")
    for s in ("top", "right"): ax.spines[s].set_visible(False)

    body = Polygon(rocket_outline(x[0], z[0], d["tilt_deg"][0], length_m, width_m), closed=True,
                   fc=NAVY, ec=NAVY)
    fl = Polygon(np.zeros((3, 2)), closed=True, fc=ORANGE, ec="none", alpha=0.9)
    ax.add_patch(fl); ax.add_patch(body)
    readout = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", ha="left",
                      fontsize=11, family="monospace", color=NAVY)

    panels, cursors = [], []
    for i, (key, label, col) in enumerate([("z_m", "height (m)", NAVY),
                                           ("speed_mps", "speed (m/s)", BLUE),
                                           ("tilt_deg", "tilt from vertical (°)", ORANGE)]):
        p = fig.add_subplot(gs[i, 1]); p.set_facecolor(PAPER)
        p.plot(t, d[key], color=col, lw=1.8)
        if key == "tilt_deg":
            p.axhspan(-10, 10, color=BLUE, alpha=0.08)
        p.set_ylabel(label, fontsize=9); p.tick_params(labelsize=8)
        for s in ("top", "right"): p.spines[s].set_visible(False)
        c = p.axvline(t[0], color=GREY, lw=1); cursors.append(c); panels.append(p)
    panels[-1].set_xlabel("time (s)", fontsize=9)
    # shade where a motor is burning
    burning = d["thrust_n"] > 0.5
    for p in panels:
        p.fill_between(t, p.get_ylim()[0], p.get_ylim()[1], where=burning, color=ORANGE, alpha=0.08, lw=0)
    fig.suptitle(title, fontsize=13, color=NAVY, x=0.06, ha="left")
    if k > 1.01:
        ax.text(0.98, 0.02, f"rocket drawn {k:.0f}x life size; path and numbers are true", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=8, color=GREY)
    return fig, ax, body, fl, readout, cursors


def frame_updater(d, body, fl, readout, cursors, length_m, width_m):
    tmax = d["thrust_n"].max()

    def update(i):
        x, z, tilt, g, th = d["x_m"][i], d["z_m"][i], d["tilt_deg"][i], d["gimbal_deg"][i], d["thrust_n"][i]
        body.set_xy(rocket_outline(x, z, tilt, length_m, width_m))
        pp = plume(x, z, tilt, g, th, tmax, length_m)
        fl.set_xy(pp if pp is not None else np.zeros((3, 2)))
        fl.set_visible(pp is not None)
        readout.set_text(f"t      {d['t_s'][i]:6.2f} s\nheight {z:6.1f} m\nspeed  {d['speed_mps'][i]:6.1f} m/s\n"
                         f"tilt   {tilt:6.1f} °\ngimbal {g:6.1f} °\nthrust {th:6.1f} N")
        for c in cursors:
            c.set_xdata([d["t_s"][i], d["t_s"][i]])
        return [body, fl, readout, *cursors]
    return update


def animate(d, out, fps=30, speed=1.0, length_m=0.6, width_m=0.074, title=""):
    t = d["t_s"]
    dt = np.median(np.diff(t))
    step = max(1, int(round(speed / (fps * dt))))
    idx = list(range(0, len(t), step))
    fig, ax, body, fl, readout, cursors = make_figure(d, length_m, width_m, title)
    k = draw_scale(d, length_m)
    upd = frame_updater(d, body, fl, readout, cursors, length_m * k, width_m * k)
    anim = animation.FuncAnimation(fig, upd, frames=idx, blit=False, interval=1000 / fps)
    if out.lower().endswith(".gif"):
        anim.save(out, writer=animation.PillowWriter(fps=fps))
    else:
        anim.save(out, writer=animation.FFMpegWriter(fps=fps, bitrate=2400))
    plt.close(fig)
    return len(idx)


def filmstrip(d, out, frames=8, length_m=0.6, width_m=0.074, title=""):
    """One row of snapshots at evenly spaced times, plus key events (ignitions, apogee, touchdown)."""
    t, z, th = d["t_s"], d["z_m"], d["thrust_n"]
    picks = set(np.linspace(0, len(t) - 1, frames).astype(int).tolist())
    picks.add(int(np.argmax(z)))
    on = np.where((th[1:] > 0.5) & (th[:-1] <= 0.5))[0] + 1
    picks.update(on.tolist())
    picks = sorted(picks)
    n = len(picks)
    k = draw_scale(d, length_m); length_m, width_m = length_m * k, width_m * k
    zmax = max(z.max() * 1.15, 3 * length_m)
    xr = max(abs(d["x_m"]).max() * 1.3, zmax * 0.3, 1.5 * length_m)
    fig, axes = plt.subplots(1, n, figsize=(1.9 * n, 6), dpi=110, facecolor=PAPER, sharey=True)
    tmax = th.max()
    for ax, i in zip(np.atleast_1d(axes), picks):
        ax.set_facecolor(PAPER); ax.set_xlim(-xr, xr); ax.set_ylim(-0.4 * length_m, zmax); ax.set_aspect("equal")
        ax.axhline(0, color=BLUE, lw=1.5)
        pp = plume(d["x_m"][i], z[i], d["tilt_deg"][i], d["gimbal_deg"][i], th[i], tmax, length_m)
        if pp is not None: ax.add_patch(Polygon(pp, fc=ORANGE, ec="none"))
        ax.add_patch(Polygon(rocket_outline(d["x_m"][i], z[i], d["tilt_deg"][i], length_m, width_m), fc=NAVY))
        tag = ""
        if i == int(np.argmax(z)): tag = "apogee"
        if i in on.tolist(): tag = "ignition"
        ax.set_title(f"{t[i]:.2f} s\n{z[i]:.1f} m · {d['speed_mps'][i]:.1f} m/s\n{tag}", fontsize=8.5, color=NAVY)
        ax.set_xticks([]);
        for s in ("top", "right", "bottom"): ax.spines[s].set_visible(False)
    np.atleast_1d(axes)[0].set_ylabel("height (m)")
    fig.suptitle(title, fontsize=12, color=NAVY)
    if k > 1.01:
        fig.text(0.99, 0.01, f"rocket drawn {k:.0f}x life size; heights, speeds and tilt are true", ha="right", fontsize=8, color=GREY)
    fig.savefig(out, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--mp4"); ap.add_argument("--gif"); ap.add_argument("--strip")
    ap.add_argument("--speed", type=float, default=1.0, help="1 = real time, 0.5 = half speed")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--frames", type=int, default=8)
    ap.add_argument("--length", type=float, default=0.6, help="rocket length drawn, m")
    ap.add_argument("--width", type=float, default=0.074)
    ap.add_argument("--title", default="")
    a = ap.parse_args()
    d = load(a.log)
    if a.mp4: print("frames:", animate(d, a.mp4, a.fps, a.speed, a.length, a.width, a.title))
    if a.gif: print("frames:", animate(d, a.gif, a.fps, a.speed, a.length, a.width, a.title))
    if a.strip: filmstrip(d, a.strip, a.frames, a.length, a.width, a.title)
