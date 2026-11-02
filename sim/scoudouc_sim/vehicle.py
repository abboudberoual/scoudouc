"""2D rigid-body rocket: position (x, z), tilt angle, gimballed thrust at the base.

Conventions
-----------
* x is horizontal, z is up. Tilt theta is the angle of the body axis from vertical,
  positive toward +x. omega = d(theta)/dt.
* Gimbal angle delta deflects the thrust line relative to the body axis. The thrust
  force acts at the nozzle, a distance `cg_to_nozzle_m` behind the centre of gravity,
  so it makes a torque:   torque = -r * T * sin(delta).
  Positive delta therefore pushes tilt back toward negative; a stabilising
  controller uses delta = +Kp*tilt + ... (see control.py).
* Thrust direction in the world frame is (sin(theta+delta), cos(theta+delta)).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

G = 9.80665
RHO_AIR = 1.225  # kg/m^3, sea level


@dataclass
class VehicleParams:
    launch_mass_kg: float          # everything, including ALL propellant, at ignition
    length_m: float
    radius_m: float = 0.033        # 66 mm body
    cg_to_nozzle_m: float = 0.15   # lever arm of the gimbal torque (held constant)
    drag_cd: float = 0.6           # crude body drag coefficient on frontal area
    gimbal_limit_deg: float = 6.0
    servo_tau_s: float = 0.045     # first-order lag time constant
    servo_rate_dps: float = 400.0  # servo slew-rate limit


@dataclass
class State:
    x: float = 0.0
    z: float = 0.0
    vx: float = 0.0
    vz: float = 0.0
    theta: float = 0.0   # rad
    omega: float = 0.0   # rad/s
    delta: float = 0.0   # actual gimbal angle, rad


class Vehicle:
    def __init__(self, params: VehicleParams):
        self.p = params
        self.area = math.pi * params.radius_m ** 2
        self.limit = math.radians(params.gimbal_limit_deg)
        self.rate_max = math.radians(params.servo_rate_dps)

    def inertia(self, mass_kg: float) -> float:
        """Slender solid cylinder about a transverse axis: m(3r^2+L^2)/12."""
        p = self.p
        return mass_kg * (3 * p.radius_m ** 2 + p.length_m ** 2) / 12.0

    def servo_step(self, delta: float, cmd: float, dt: float) -> float:
        """Clamp the command, apply first-order lag, rate limit, then clamp the result."""
        cmd = max(-self.limit, min(self.limit, cmd))
        rate = (cmd - delta) / self.p.servo_tau_s
        rate = max(-self.rate_max, min(self.rate_max, rate))
        delta += rate * dt
        return max(-self.limit, min(self.limit, delta))

    def step(self, s: State, thrust_n: float, delta_cmd: float, mass_kg: float,
             dt: float, extra_cda: float = 0.0, airborne: bool = True) -> None:
        """Advance state by dt (semi-implicit Euler). Mutates s."""
        p = self.p
        s.delta = self.servo_step(s.delta, delta_cmd, dt)
        ang = s.theta + s.delta
        speed = math.hypot(s.vx, s.vz)
        cda = p.drag_cd * self.area + extra_cda
        k = 0.5 * RHO_AIR * cda * speed
        fx = thrust_n * math.sin(ang) - k * s.vx
        fz = thrust_n * math.cos(ang) - k * s.vz - mass_kg * G
        if not airborne and fz <= 0.0:
            # Sitting on the pad: the ground holds everything still.
            s.vx = s.vz = s.omega = 0.0
            s.z = 0.0
            return
        torque = -p.cg_to_nozzle_m * thrust_n * math.sin(s.delta)
        s.vx += fx / mass_kg * dt
        s.vz += fz / mass_kg * dt
        s.omega += torque / self.inertia(mass_kg) * dt
        s.x += s.vx * dt
        s.z += s.vz * dt
        s.theta += s.omega * dt
