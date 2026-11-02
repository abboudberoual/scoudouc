"""Thrust curves: load from CSV or use built-in approximations of Estes motors.

A ThrustCurve is thrust (N) versus time (s) since ignition, zero outside the
burn. It also knows how much propellant has burned so far, so the vehicle can
get lighter during the burn (propellant burned is assumed proportional to the
impulse delivered so far).
"""
from __future__ import annotations

import csv
from bisect import bisect_right
from dataclasses import dataclass
from typing import List, Optional, Sequence


class ThrustCurve:
    def __init__(self, time_s: Sequence[float], thrust_n: Sequence[float],
                 name: str = "custom", propellant_kg: float = 0.0):
        t = [float(v) for v in time_s]
        f = [float(v) for v in thrust_n]
        if len(t) != len(f) or len(t) < 2:
            raise ValueError("need at least two (time, thrust) points")
        if any(t2 <= t1 for t1, t2 in zip(t, t[1:])):
            raise ValueError("time_s must be strictly increasing")
        if any(v < 0 for v in f):
            raise ValueError("thrust must be >= 0")
        # Force the curve to start and end at zero thrust, starting at t=0.
        if t[0] > 0:
            t.insert(0, 0.0); f.insert(0, 0.0)
        if f[-1] != 0.0:
            t.append(t[-1] + 1e-3); f.append(0.0)
        self.t: List[float] = t
        self.f: List[float] = f
        self.name = name
        self.propellant_kg = float(propellant_kg)
        # Cumulative impulse at each point (trapezoids), used for propellant burn-off.
        cum = [0.0]
        for i in range(1, len(t)):
            cum.append(cum[-1] + 0.5 * (f[i] + f[i - 1]) * (t[i] - t[i - 1]))
        self._cum = cum

    # --- basic properties -------------------------------------------------
    @property
    def burn_time(self) -> float:
        return self.t[-1]

    @property
    def total_impulse(self) -> float:
        """Total impulse in newton-seconds (area under the curve)."""
        return self._cum[-1]

    @property
    def average_thrust(self) -> float:
        return self.total_impulse / self.burn_time

    @property
    def peak_thrust(self) -> float:
        return max(self.f)

    # --- evaluation -------------------------------------------------------
    def thrust(self, t: float) -> float:
        """Thrust (N) at time t since ignition; 0 before ignition / after burnout."""
        if t <= 0.0 or t >= self.t[-1]:
            return 0.0
        i = bisect_right(self.t, t)
        t0, t1 = self.t[i - 1], self.t[i]
        f0, f1 = self.f[i - 1], self.f[i]
        return f0 + (f1 - f0) * (t - t0) / (t1 - t0)

    def impulse_until(self, t: float) -> float:
        if t <= 0.0:
            return 0.0
        if t >= self.t[-1]:
            return self._cum[-1]
        i = bisect_right(self.t, t)
        t0 = self.t[i - 1]
        f_t = self.thrust(t)
        return self._cum[i - 1] + 0.5 * (self.f[i - 1] + f_t) * (t - t0)

    def mass_burned(self, t: float) -> float:
        """Propellant mass (kg) burned t seconds after ignition."""
        if self.propellant_kg <= 0.0 or self.total_impulse <= 0.0:
            return 0.0
        return self.propellant_kg * self.impulse_until(t) / self.total_impulse

    def scaled(self, factor: float) -> "ThrustCurve":
        """Same burn time, thrust multiplied by factor (motor-to-motor variation).

        Propellant mass is unchanged: a "hot" motor delivers more impulse from the
        same propellant, which is how real batch variation looks.
        """
        return ThrustCurve(self.t, [v * factor for v in self.f],
                           name=f"{self.name}x{factor:.3f}",
                           propellant_kg=self.propellant_kg)


def load_csv(path: str, name: Optional[str] = None, propellant_kg: float = 0.0) -> ThrustCurve:
    """Load a measured curve from a CSV with header columns time_s, thrust_n."""
    ts, fs = [], []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            ts.append(float(row["time_s"]))
            fs.append(float(row["thrust_n"]))
    return ThrustCurve(ts, fs, name=name or str(path), propellant_kg=propellant_kg)


# --- built-in approximations ----------------------------------------------------
# APPROXIMATIONS ONLY. Headline numbers (total impulse, burn time, propellant mass)
# are rounded from memory of thrustcurve.org / Estes data sheets; the SHAPE is a
# hand-drawn piecewise-linear sketch (fast spike, then a plateau, then a taper).
# Each shape is rescaled so its area equals the stated total impulse exactly.
# Replace with measured bench data (Scoudouc 0) as soon as we have it.
@dataclass(frozen=True)
class _Spec:
    total_impulse_ns: float
    propellant_kg: float
    shape: tuple  # (time_s, relative thrust) points, ends at zero thrust


BUILTIN_MOTORS = {
    # C6: ~8.8 N*s, ~1.85 s, ~4.7 N average, ~12 g propellant
    "C6": _Spec(8.8, 0.0123, ((0, 0), (0.05, 5), (0.15, 14), (0.3, 11), (0.5, 6.5),
                              (1.0, 5), (1.5, 4.5), (1.8, 4), (1.85, 0))),
    # D12: ~16.8 N*s, ~1.65 s, ~10 N average, ~30 N peak, ~21 g propellant
    "D12": _Spec(16.8, 0.0211, ((0, 0), (0.04, 12), (0.1, 29), (0.2, 22), (0.4, 11),
                                (0.8, 9), (1.2, 8.5), (1.55, 8), (1.65, 0))),
    # E12: ~28.5 N*s, ~2.3 s, ~12.4 N average, ~30 N peak, ~35 g propellant
    "E12": _Spec(28.5, 0.035, ((0, 0), (0.05, 16), (0.12, 32), (0.3, 18), (0.6, 11),
                               (1.4, 10), (2.1, 9.5), (2.3, 0))),
    # F15: ~49.6 N*s, ~3.3 s, ~15 N average, ~25 N peak, ~60 g propellant
    "F15": _Spec(49.6, 0.060, ((0, 0), (0.05, 14), (0.15, 25), (0.4, 19), (1.0, 15),
                               (2.0, 14), (3.0, 13), (3.3, 0))),
}


def builtin_motor(name: str) -> ThrustCurve:
    """Approximate Estes C6, D12, E12 or F15 curve (see the note above)."""
    key = name.upper()
    if key not in BUILTIN_MOTORS:
        raise KeyError(f"unknown motor {name!r}; choose from {sorted(BUILTIN_MOTORS)}")
    spec = BUILTIN_MOTORS[key]
    t = [p[0] for p in spec.shape]
    f = [p[1] for p in spec.shape]
    area = sum(0.5 * (f[i] + f[i - 1]) * (t[i] - t[i - 1]) for i in range(1, len(t)))
    k = spec.total_impulse_ns / area
    return ThrustCurve(t, [v * k for v in f], name=key, propellant_kg=spec.propellant_kg)
