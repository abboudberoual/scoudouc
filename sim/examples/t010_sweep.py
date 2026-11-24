"""T-010 sweep: landing-burn success at 660 g and 750 g, E12 boost, C6/D12/E12 landing,
old stopping-distance trigger vs new integrating trigger, each motor +/-15 % thrust.

Run from the repo root:  python sim/examples/t010_sweep.py [--n 200]
Writes data/sim/t010_landing_sweep.csv (one row per case), t010_landing_flights.csv
(one row per flight) and t010_*.png. Thrust curves: built-in approximations until the
thrustcurve.org files land in data/library (T-011); then pass --eng-dir.
"""
import argparse, csv, math, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from scoudouc_sim import (VehicleParams, Vehicle, MissionConfig, builtin_motor, load_eng,
                          suggest_gains, HoverslamTrigger, IntegratingTrigger)
from scoudouc_sim.plots import monte_carlo
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "data", "sim")
MASSES_G = (660, 750)
DOWN = ("C6", "D12", "E12")
DELAY_S = 0.1


def motor(name, eng_dir):
    if eng_dir:
        return load_eng(os.path.join(eng_dir, f"Estes_{name}.eng"))
    return builtin_motor(name)


def cases(eng_dir):
    up = motor("E12", eng_dir)
    for mass_g in MASSES_G:
        veh = VehicleParams(launch_mass_kg=mass_g / 1000, length_m=0.60, radius_m=0.033,
                            cg_to_nozzle_m=0.22)
        gains = suggest_gains(Vehicle(veh).inertia(veh.launch_mass_kg - 0.5 * up.propellant_kg),
                              veh.cg_to_nozzle_m, up.average_thrust, natural_freq_rad_s=12.0,
                              damping=0.7)
        cda = veh.drag_cd * math.pi * veh.radius_m ** 2
        for down_name in DOWN:
            down = motor(down_name, eng_dir)
            trig = {
                "stopping_distance": HoverslamTrigger.from_motor(down, thrust_trust=0.9,
                                                                 ignition_delay_s=DELAY_S),
                "integrating": IntegratingTrigger(down, ignition_delay_s=DELAY_S, drag_cda_m2=cda),
            }
            for tname, tr in trig.items():
                def make(sa, sb, tilt0, veh=veh, down=down, tr=tr, gains=gains):
                    return MissionConfig(vehicle=veh, motor_a=up.scaled(sa), motor_b=down.scaled(sb),
                                         gains=gains, trigger=tr, initial_tilt_deg=tilt0)
                yield dict(vehicle="S2", mass_g=mass_g, motor=f"E12/{down_name}", trigger=tname), make


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--eng-dir", default=None)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    rows, flights = [], []
    for meta, make in cases(a.eng_dir):
        res = monte_carlo(make, n=a.n, seed=10)
        td = [c["touchdown_speed_mps"] for c in res["cases"]]
        q = statistics.quantiles(td, n=10)
        row = dict(meta, n=a.n, success_rate=round(res["success_rate"], 3),
                   touchdown_mps_p50=round(statistics.median(td), 2),
                   touchdown_mps_p10=round(q[0], 2), touchdown_mps_p90=round(q[-1], 2),
                   curves="eng" if a.eng_dir else "builtin_approx")
        rows.append(row)
        print(row)
        for c in res["cases"]:
            flights.append(dict(meta, scale_a=round(c["scale_a"], 4), scale_b=round(c["scale_b"], 4),
                                tilt0_deg=round(c["tilt0_deg"], 2), apogee_m=round(c["apogee_m"], 2),
                                t_landing_ignite_s=round(c["t_landing_ignite_s"], 3),
                                touchdown_speed_mps=round(c["touchdown_speed_mps"], 3),
                                touchdown_tilt_deg=round(c["touchdown_tilt_deg"], 2),
                                success=int(c["success"])))
    for name, data in (("t010_landing_sweep.csv", rows), ("t010_landing_flights.csv", flights)):
        with open(os.path.join(OUT, name), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader(); w.writerows(data)
    plot(flights)


def plot(flights):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for k, mass in enumerate(MASSES_G):
        for tname, color in (("stopping_distance", "#8a97a8"), ("integrating", "#e86f2c")):
            pts = [f for f in flights if f["mass_g"] == mass and f["motor"] == "E12/E12"
                   and f["trigger"] == tname]
            ax[k].scatter([f["scale_b"] for f in pts], [f["touchdown_speed_mps"] for f in pts],
                          s=10, color=color, label=tname.replace("_", " "))
        ax[k].axhline(2.0, color="#141c2b", ls="--", lw=0.8)
        ax[k].text(0.851, 2.3, "success < 2 m/s", fontsize=8)
        ax[k].set_title(f"S2 {mass} g, E12 up / E12 down")
        ax[k].set_xlabel("landing motor thrust (x nominal)")
        ax[k].grid(alpha=0.3)
    ax[0].set_ylabel("touchdown speed (m/s)")
    ax[0].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "t010_touchdown_vs_thrust.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
