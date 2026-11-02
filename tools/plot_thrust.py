"""Plot one or more static-fire CSV files (columns: time_s, thrust_n).

Usage: python tools/plot_thrust.py data/static-fires/*.csv
"""
import sys
import csv
import matplotlib.pyplot as plt

for path in sys.argv[1:]:
    t, f = [], []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            t.append(float(row["time_s"]))
            f.append(float(row["thrust_n"]))
    impulse = sum((f[i] + f[i + 1]) / 2 * (t[i + 1] - t[i]) for i in range(len(t) - 1))
    plt.plot(t, f, label=f"{path.split('/')[-1]}  ({impulse:.1f} N·s)")

plt.xlabel("time (s)")
plt.ylabel("thrust (N)")
plt.title("Measured thrust curves")
plt.legend()
plt.grid(True)
plt.show()
