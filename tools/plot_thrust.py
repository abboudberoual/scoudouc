"""Plot static-fire CSV files (columns: time_s, thrust_n) and print the key numbers.

Usage:
  python tools/plot_thrust.py measured.csv                 one run
  python tools/plot_thrust.py measured.csv published.csv   run + published thrustcurve.org curve overlaid
  python tools/plot_thrust.py run1.csv run2.csv run3.csv   3 or more files: all treated as runs, compared
  add --ref published.csv to overlay a published curve while comparing several runs
  add --save out.png to write a picture instead of opening a window

For each run it prints: peak thrust, burn time and total impulse.
  burn time     = time between the first and last moment thrust is above 10% of peak
  total impulse = area under the thrust curve over the burn (trapezoid rule), in newton-seconds
Lines starting with # (from a serial log) are ignored. A published CSV only needs two columns:
time in seconds, then thrust in newtons (header names are not checked).
"""
import argparse
import csv


def load(path):
    """Read a CSV into two lists (time_s, thrust_n). Header row and '#' comment lines are skipped."""
    t, f = [], []
    with open(path, newline="") as fh:
        for row in csv.reader(line for line in fh if not line.startswith("#")):
            try:
                t.append(float(row[0]))
                f.append(float(row[1]))
            except (ValueError, IndexError):
                continue  # header or blank line
    if len(t) < 2:
        raise SystemExit(f"{path}: no data rows found")
    return t, f


def metrics(t, f, burn_fraction=0.10):
    """Return dict: peak_n, start_s, end_s, burn_s, impulse_ns (burn window only)."""
    peak = max(f)
    limit = burn_fraction * peak
    above = [i for i, v in enumerate(f) if v >= limit]
    i0, i1 = above[0], above[-1]
    impulse = sum((f[i] + f[i + 1]) / 2 * (t[i + 1] - t[i]) for i in range(i0, i1))
    return {"peak_n": peak, "start_s": t[i0], "end_s": t[i1],
            "burn_s": t[i1] - t[i0], "impulse_ns": impulse}


def report(name, m):
    print(f"{name}: peak {m['peak_n']:.1f} N | burn {m['burn_s']:.2f} s | impulse {m['impulse_ns']:.1f} N·s")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--ref", help="published curve CSV to overlay")
    ap.add_argument("--save", help="save the plot to this image file instead of showing it")
    a = ap.parse_args()
    runs, ref = a.files, a.ref
    if ref is None and len(runs) == 2:      # "a second CSV" = the published curve
        runs, ref = runs[:1], runs[1]

    import matplotlib
    if a.save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for path in runs:
        t, f = load(path)
        m = metrics(t, f)
        name = path.split("/")[-1]
        report(name, m)
        shift = m["start_s"]                # line every run up so burn starts at time 0
        plt.plot([x - shift for x in t], f, label=f"{name} ({m['impulse_ns']:.1f} N·s)")
    if ref:
        t, f = load(ref)
        m = metrics(t, f)
        report("published " + ref.split("/")[-1], m)
        plt.plot([x - m["start_s"] for x in t], f, "k--", label=f"published ({m['impulse_ns']:.1f} N·s)")

    plt.xlabel("time since ignition (s)")
    plt.ylabel("thrust (N)")
    plt.title("Thrust curves")
    plt.legend()
    plt.grid(True)
    if a.save:
        plt.savefig(a.save, dpi=120)
    else:
        plt.show()


if __name__ == "__main__":
    main()
