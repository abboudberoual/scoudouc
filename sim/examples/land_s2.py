"""Scoudouc 2 'Land': E12 up, E12 down, 900 g, 60 cm.

Run from the sim/ folder:  python examples/land_s2.py [--down F15]
"""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scoudouc_sim import (VehicleParams, Vehicle, MissionConfig, builtin_motor,
                          run_mission, suggest_gains, HoverslamTrigger)
from scoudouc_sim.plots import plot_flight, monte_carlo, plot_monte_carlo

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

ap = argparse.ArgumentParser()
ap.add_argument("--down", default="E12", help="landing motor: E12 (default) or F15, C6, D12")
ARGS, _ = ap.parse_known_args()
E12 = builtin_motor("E12")
DOWN = builtin_motor(ARGS.down)
TAG = "" if ARGS.down.upper() == "E12" else "_" + ARGS.down.upper()
VEH = VehicleParams(launch_mass_kg=0.900, length_m=0.60, radius_m=0.033, cg_to_nozzle_m=0.22)
mid_mass = VEH.launch_mass_kg - 0.5 * E12.propellant_kg
GAINS = suggest_gains(Vehicle(VEH).inertia(mid_mass), VEH.cg_to_nozzle_m,
                      E12.average_thrust, natural_freq_rad_s=12.0, damping=0.7)
TRIGGER = HoverslamTrigger.from_motor(DOWN, thrust_trust=0.9, margin=1.0, ignition_delay_s=0.1)


def make_config(scale_a=1.0, scale_b=1.0, tilt0=0.0):
    return MissionConfig(vehicle=VEH, motor_a=E12.scaled(scale_a), motor_b=DOWN.scaled(scale_b),
                         gains=GAINS, trigger=TRIGGER, initial_tilt_deg=tilt0)


if __name__ == "__main__":
    print(f"gains: kp={GAINS.kp:.2f} kd={GAINS.kd:.3f}")
    summary, log = run_mission(make_config(tilt0=2.0), os.path.join(OUT, f"land_s2{TAG}_flight.csv"))
    print("S2 nominal (2 deg initial tilt):", {k: round(v, 2) if isinstance(v, float) else v
                                               for k, v in summary.as_dict().items()})
    plot_flight(log, os.path.join(OUT, f"land_s2{TAG}_flight.png"), f"S2 Land, E12 up / {ARGS.down} down")
    res = monte_carlo(make_config, n=100)
    print(f"S2 Monte Carlo landing success: {res['successes']}/{res['n']} "
          f"({100 * res['success_rate']:.0f}%)")
    plot_monte_carlo(res, os.path.join(OUT, f"land_s2{TAG}_montecarlo.png"), f"S2 landing ({ARGS.down} down)")
