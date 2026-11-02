"""Scoudouc 1 'Hop': one D12, 350 g, 40 cm, chute at apogee.

Run from the sim/ folder:  python examples/hop_s1.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scoudouc_sim import (VehicleParams, Vehicle, MissionConfig, builtin_motor,
                          run_mission, suggest_gains)
from scoudouc_sim.plots import plot_flight, monte_carlo, plot_monte_carlo

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

D12 = builtin_motor("D12")
VEH = VehicleParams(launch_mass_kg=0.350, length_m=0.40, radius_m=0.033, cg_to_nozzle_m=0.15)
mid_mass = VEH.launch_mass_kg - D12.propellant_kg / 2
GAINS = suggest_gains(Vehicle(VEH).inertia(mid_mass), VEH.cg_to_nozzle_m,
                      D12.average_thrust, natural_freq_rad_s=12.0, damping=0.7)
CHUTE_CDA = 0.25  # Cd*A of a ~65 cm round chute: about 4.7 m/s descent at 350 g


def make_config(scale_a=1.0, scale_b=1.0, tilt0=0.0):
    return MissionConfig(vehicle=VEH, motor_a=D12.scaled(scale_a), gains=GAINS,
                         initial_tilt_deg=tilt0, chute_cda_m2=CHUTE_CDA)


if __name__ == "__main__":
    print(f"gains: kp={GAINS.kp:.2f} kd={GAINS.kd:.3f}")
    summary, log = run_mission(make_config(tilt0=4.0), os.path.join(OUT, "hop_s1_flight.csv"))
    print("S1 nominal (4 deg initial tilt):", {k: round(v, 2) if isinstance(v, float) else v
                                               for k, v in summary.as_dict().items()})
    plot_flight(log, os.path.join(OUT, "hop_s1_flight.png"), "S1 Hop, D12, 4 deg start tilt")
    # S1 goal: stay within 10 degrees of vertical while the motor burns.
    ok = lambda s: s.touched_down and s.max_tilt_powered_deg < 10.0
    res = monte_carlo(make_config, n=100, success_fn=ok)
    print(f"S1 Monte Carlo (max tilt under power < 10 deg): {res['successes']}/{res['n']}")
    plot_monte_carlo(res, os.path.join(OUT, "hop_s1_montecarlo.png"), "S1 tilt < 10 deg")
