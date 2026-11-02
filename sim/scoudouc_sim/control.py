"""Attitude PID and the landing-burn (hoverslam) trigger."""
from __future__ import annotations

import math
from dataclasses import dataclass

from .vehicle import G
from .thrust import ThrustCurve


@dataclass
class PIDGains:
    kp: float = 1.0      # rad of gimbal per rad of tilt
    ki: float = 0.0
    kd: float = 0.1      # rad of gimbal per rad/s of tilt rate
    i_limit: float = 0.05  # anti-windup clamp on the integral term (rad of gimbal)


class PID:
    """tilt -> gimbal angle. Gains are fixed (no gain scheduling).

    delta = Kp*e + Ki*integral(e) + Kd*omega, with e = tilt - setpoint.
    The derivative term uses the measured tilt rate directly (no noisy differencing).
    """

    def __init__(self, gains: PIDGains, setpoint_rad: float = 0.0):
        self.g = gains
        self.setpoint = setpoint_rad
        self.integral = 0.0

    def reset(self) -> None:
        self.integral = 0.0

    def update(self, tilt: float, omega: float, dt: float, active: bool = True) -> float:
        e = tilt - self.setpoint
        if active:  # only wind up the integrator while the motor can actually steer
            self.integral += self.g.ki * e * dt
            self.integral = max(-self.g.i_limit, min(self.g.i_limit, self.integral))
        return self.g.kp * e + self.integral + self.g.kd * omega


def suggest_gains(inertia: float, lever_arm_m: float, thrust_ref_n: float,
                  natural_freq_rad_s: float = 15.0, damping: float = 0.7) -> PIDGains:
    """Textbook starting gains. Plant: theta'' = -(r*T/I) * delta, so
    Kp = wn^2 * I/(r*T)  and  Kd = 2*zeta*wn * I/(r*T)."""
    b = lever_arm_m * thrust_ref_n / inertia
    return PIDGains(kp=natural_freq_rad_s ** 2 / b, ki=0.0,
                    kd=2 * damping * natural_freq_rad_s / b)


class HoverslamTrigger:
    """Fire the landing motor when the stopping distance reaches the height above ground.

        d_stop = v^2 / (2 * (T/m - g))   (+ v * ignition delay, times a safety margin)

    T is an *estimate* of landing-motor thrust (a motor can be 15% off), m the current
    mass. If T/m <= g the motor can never stop the fall, so d_stop is infinite and the
    trigger fires as soon as the rocket starts descending.
    """

    def __init__(self, thrust_est_n: float, margin: float = 1.0,
                 ignition_delay_s: float = 0.1):
        self.thrust_est_n = thrust_est_n
        self.margin = margin
        self.ignition_delay_s = ignition_delay_s

    @classmethod
    def from_motor(cls, motor: ThrustCurve, thrust_trust: float = 0.9, **kw):
        """Estimate thrust as the motor's average thrust times a derating factor."""
        return cls(motor.average_thrust * thrust_trust, **kw)

    def stopping_distance(self, v_down: float, mass_kg: float) -> float:
        if v_down <= 0.0:
            return 0.0
        net = self.thrust_est_n / mass_kg - G
        if net <= 0.0:
            return math.inf
        d = v_down ** 2 / (2.0 * net) + v_down * self.ignition_delay_s
        return d * self.margin

    def should_fire(self, height_m: float, vz: float, mass_kg: float) -> bool:
        """vz is vertical velocity (negative = falling)."""
        if vz >= 0.0:
            return False
        return self.stopping_distance(-vz, mass_kg) >= height_m
