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


class IntegratingTrigger:
    """Landing-burn trigger that integrates the motor's actual thrust curve.

    The stopping-distance rule above treats the motor as a constant average thrust.
    Real curves spike early and tail off, so that rule lights at the wrong height.
    This trigger instead asks, at every control tick: "if I commanded ignition now,
    how fast would I touch down?" It answers by integrating, in 1D, the ignition
    delay (free fall), then the whole thrust curve with propellant burn-off, gravity
    and drag. If the motor would stop the rocket above the ground, the answer is the
    speed after falling from wherever the burn ended. It fires at the tick where
    waiting one more tick would make the predicted touchdown worse, i.e. at the
    minimum of predicted touchdown speed along the fall. For a motor that can stop
    the fall, that is the moment the burn's velocity reaches zero at the ground.

    It predicts with the curve times `thrust_trust` (1.0 = trust the nominal curve).
    It cannot know whether this particular motor is hot or cold, which is the point
    of the +/-15 % sweep. Speed: the predictions are pre-computed once per mass as
    a table over falling speed (numpy, all speeds at once), then looked up.
    """

    def __init__(self, motor: ThrustCurve, ignition_delay_s: float = 0.1,
                 thrust_trust: float = 1.0, drag_cda_m2: float = 0.0,
                 rho: float = 1.225, lookahead_s: float = 0.005,
                 v_max: float = 60.0, dv: float = 0.1, dt: float = 0.002,
                 flat_tol_mps: float = 0.02):
        self.motor = motor
        self.flat_tol_mps = flat_tol_mps
        self.ignition_delay_s = ignition_delay_s
        self.thrust_trust = thrust_trust
        self.k_drag = 0.5 * rho * drag_cda_m2   # drag force = k_drag * v^2
        self.lookahead_s = lookahead_s
        self.v_max, self.dv, self.dt = v_max, dv, dt
        self._tables = {}

    # --- prediction table ---------------------------------------------------
    def _table(self, mass_kg: float):
        key = round(mass_kg, 4)
        if key in self._tables:
            return self._tables[key]
        import numpy as np
        v0 = np.arange(0.0, self.v_max + self.dv / 2, self.dv)   # falling speed at command
        vz = -v0.copy()                                          # up is positive
        z = np.zeros_like(v0)
        runmin = [z.copy()]
        vz_hist = [vz.copy()]
        dt = self.dt
        t_end = self.ignition_delay_s + self.motor.burn_time
        n = int(math.ceil(t_end / dt))
        for i in range(n):
            t = i * dt
            tb = t - self.ignition_delay_s
            f = self.motor.thrust(tb) * self.thrust_trust if tb > 0 else 0.0
            m = mass_kg - (self.motor.mass_burned(tb) if tb > 0 else 0.0)
            a = f / m - G - self.k_drag * vz * np.abs(vz) / m
            vz = vz + a * dt
            z = z + vz * dt
            runmin.append(np.minimum(runmin[-1], z))
            vz_hist.append(vz.copy())
        tab = dict(v0=v0, runmin=np.array(runmin), vz=np.array(vz_hist),
                   z_end=z, vz_end=vz)
        self._tables[key] = tab
        return tab

    def _outcome_row(self, tab, j: int, h: float) -> float:
        import numpy as np
        col = tab["runmin"][:, j]            # non-increasing with time
        hit = np.nonzero(col <= -h)[0]
        if hit.size:                          # touches down during delay or burn
            return float(abs(tab["vz"][hit[0], j]))
        z_end, v_end = tab["z_end"][j], tab["vz_end"][j]
        drop = max(0.0, h + z_end)            # height left at burnout
        return math.sqrt(v_end ** 2 + 2.0 * G * drop)

    def predicted_touchdown(self, height_m: float, v_down: float, mass_kg: float) -> float:
        """Touchdown speed (m/s) if ignition were commanded now."""
        tab = self._table(mass_kg)
        x = min(max(v_down, 0.0), self.v_max) / self.dv
        j0 = min(int(x), len(tab["v0"]) - 2)
        w = x - j0
        o0 = self._outcome_row(tab, j0, height_m)
        o1 = self._outcome_row(tab, j0 + 1, height_m)
        return (1 - w) * o0 + w * o1

    def should_fire(self, height_m: float, vz: float, mass_kg: float) -> bool:
        if vz >= 0.0:
            return False
        v = -vz
        L = self.lookahead_s
        now = self.predicted_touchdown(height_m, v, mass_kg)
        a = G - self.k_drag * v * v / mass_kg     # free-fall acceleration (down +)
        v_next = v + a * L
        h_next = height_m - v * L - 0.5 * a * L * L
        nxt = self.predicted_touchdown(h_next, v_next, mass_kg)
        # Fire unless waiting clearly helps. The tolerance stops the trigger from
        # waiting forever where the outcome is flat, e.g. so close to the ground that
        # the motor cannot light in time, where table interpolation alone can make
        # "later" look a hair better.
        return nxt >= now - self.flat_tol_mps
