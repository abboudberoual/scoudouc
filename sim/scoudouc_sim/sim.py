"""Fixed-step mission simulator: boost on motor A, coast, optional landing burn on B."""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass, asdict, field
from typing import Optional

from .thrust import ThrustCurve
from .vehicle import Vehicle, VehicleParams, State
from typing import Union
from .control import PID, PIDGains, HoverslamTrigger, IntegratingTrigger


@dataclass
class MissionConfig:
    vehicle: VehicleParams
    motor_a: ThrustCurve
    gains: PIDGains
    motor_b: Optional[ThrustCurve] = None
    trigger: Optional[Union[HoverslamTrigger, IntegratingTrigger]] = None
    initial_tilt_deg: float = 0.0
    chute_cda_m2: float = 0.0       # drag area (Cd*A) of a parachute opened at apogee
    dt: float = 0.001               # physics step, 1 ms
    control_dt: float = 0.005       # controller runs at 200 Hz (zero-order hold)
    log_every: int = 10             # log every N physics steps (10 ms)
    t_max: float = 120.0


@dataclass
class Summary:
    apogee_m: float
    t_apogee_s: float
    max_tilt_deg: float
    max_tilt_powered_deg: float
    touchdown_speed_mps: float
    touchdown_tilt_deg: float
    horizontal_drift_m: float
    touched_down: bool
    landing_burn_fired: bool
    t_landing_ignite_s: float
    flight_time_s: float

    def as_dict(self):
        return asdict(self)


LOG_COLUMNS = ["t_s", "x_m", "z_m", "vx_mps", "vz_mps", "speed_mps", "tilt_deg",
               "omega_dps", "gimbal_deg", "gimbal_cmd_deg", "thrust_n", "mass_kg"]


def run_mission(cfg: MissionConfig, log_path: Optional[str] = None):
    """Run one flight. Returns (Summary, log) where log is a dict of lists keyed by
    LOG_COLUMNS. If log_path is given the log is also written as CSV."""
    veh = Vehicle(cfg.vehicle)
    s = State(theta=math.radians(cfg.initial_tilt_deg))
    pid = PID(cfg.gains)
    a, b = cfg.motor_a, cfg.motor_b
    dt = cfg.dt
    ctrl_every = max(1, round(cfg.control_dt / dt))
    ctrl_dt = ctrl_every * dt

    log = {k: [] for k in LOG_COLUMNS}
    t = 0.0
    n = 0
    cmd = 0.0
    airborne = False
    apogee, t_apogee = 0.0, 0.0
    max_tilt = max_tilt_pow = abs(s.theta)
    fire_t: Optional[float] = None   # when the trigger fired
    b_start: Optional[float] = None  # when motor B actually lights
    chute_open = False
    touched = False

    while t < cfg.t_max:
        ta = t
        tb = (t - b_start) if b_start is not None else -1.0
        thrust = a.thrust(ta) + (b.thrust(tb) if b and tb > 0 else 0.0)
        burned = a.mass_burned(ta) + (b.mass_burned(tb) if b and tb > 0 else 0.0)
        m = cfg.vehicle.launch_mass_kg - burned

        if n % ctrl_every == 0:
            if (b is not None and cfg.trigger is not None and fire_t is None
                    and airborne and t > a.burn_time
                    and cfg.trigger.should_fire(s.z, s.vz, m)):
                fire_t = t
                b_start = t + cfg.trigger.ignition_delay_s
            cmd = pid.update(s.theta, s.omega, ctrl_dt, active=thrust > 0.0)

        if (cfg.chute_cda_m2 > 0 and not chute_open and airborne
                and t > a.burn_time and s.vz < 0):
            chute_open = True

        veh.step(s, thrust, cmd, m, dt,
                 extra_cda=cfg.chute_cda_m2 if chute_open else 0.0, airborne=airborne)
        t += dt
        n += 1
        if not airborne and s.z > 0.0:
            airborne = True

        if s.z > apogee:
            apogee, t_apogee = s.z, t
        tilt = abs(s.theta)
        max_tilt = max(max_tilt, tilt)
        if thrust > 0.0:
            max_tilt_pow = max(max_tilt_pow, tilt)

        if n % cfg.log_every == 0:
            row = (t, s.x, s.z, s.vx, s.vz, math.hypot(s.vx, s.vz),
                   math.degrees(s.theta), math.degrees(s.omega), math.degrees(s.delta),
                   math.degrees(max(-veh.limit, min(veh.limit, cmd))), thrust, m)
            for k, v in zip(LOG_COLUMNS, row):
                log[k].append(v)

        if airborne and s.z <= 0.0:
            touched = True
            break

    speed = math.hypot(s.vx, s.vz)
    summary = Summary(
        apogee_m=apogee, t_apogee_s=t_apogee,
        max_tilt_deg=math.degrees(max_tilt), max_tilt_powered_deg=math.degrees(max_tilt_pow),
        touchdown_speed_mps=speed if touched else float("nan"),
        touchdown_tilt_deg=abs(math.degrees(s.theta)) if touched else float("nan"),
        horizontal_drift_m=abs(s.x) if touched else float("nan"),
        touched_down=touched, landing_burn_fired=fire_t is not None,
        t_landing_ignite_s=b_start if b_start is not None else float("nan"),
        flight_time_s=t)

    if log_path:
        with open(log_path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(LOG_COLUMNS)
            w.writerows(zip(*[log[k] for k in LOG_COLUMNS]))
    return summary, log
