# Simulator

Python 3 with numpy + matplotlib only. A 2D rocket model (horizontal x, height z, tilt) that takes thrust curves, mass, gimbal limits and servo lag, and lets us (1) tune the attitude loop and (2) test landing-burn ignition rules across motor-to-motor variation. Move to RocketPy only if we need 3D.

## Run

```
cd sim
pip install numpy matplotlib pytest
python -m pytest tests            # 13 tests
python examples/hop_s1.py         # S1: D12, 350 g, 40 cm
python examples/land_s2.py        # S2: E12 up, E12 down, 900 g, 60 cm
python examples/land_s2.py --down F15
```

Outputs (PNG plots and CSV logs with units in the column names) go to `examples/output/`.

## Files

| File | What it does |
|---|---|
| `scoudouc_sim/thrust.py` | `ThrustCurve` (thrust vs time, impulse, propellant burn-off, `.scaled(k)`), `load_csv()` for `time_s,thrust_n` files, `builtin_motor("C6"/"D12"/"E12"/"F15")` |
| `scoudouc_sim/vehicle.py` | 2D rigid body: mass, inertia, gimbal torque, servo (45 ms lag, 400 deg/s rate limit, +/-6 deg), drag, gravity |
| `scoudouc_sim/control.py` | `PID` (tilt to gimbal, fixed gains), `suggest_gains()`, `HoverslamTrigger` (stopping distance rule) |
| `scoudouc_sim/sim.py` | `run_mission()`: 1 ms fixed steps, controller at 200 Hz, boost, coast, optional landing burn, CSV log, `Summary` |
| `scoudouc_sim/plots.py` | `plot_flight()`, `monte_carlo()` (thrust scale 0.85-1.15 per motor, initial tilt +/-5 deg), `plot_monte_carlo()` |
| `examples/` | S1 and S2 scripts and `output/` |
| `tests/` | pytest: impulse, gimbal limit, servo, trigger fires before ground contact |

Landing success = touchdown speed < 2 m/s and tilt < 10 deg. See `docs/learning/pid-control.md` and `docs/learning/landing-burn-timing.md`.

## What is simplified

- 2D only: no roll, no yaw, no out-of-plane motion.
- No wind and no gusts.
- Thrust curves are approximations: published total impulse, burn time and propellant mass (rounded from memory, not re-checked), with a hand-drawn shape. Replace with measured bench CSVs when available.
- Perfect sensing: the controller reads true tilt and tilt rate (no gyro noise, bias or delay), and the trigger knows true height and speed.
- Centre of gravity and lever arm are constant as propellant burns; inertia is a simple cylinder formula scaled with mass.
- Drag is one coefficient on frontal area (Cd 0.6); no lift, no aerodynamic stability (finless), no ejection charge or motor delay.
- Parachute is an instant drag area at apogee (S1 only).
- Pad contact is a hard clamp; touchdown ends the run (no legs, no bounce, no tip-over).
- Landing motor lights after a fixed igniter delay; the trigger uses a derated average thrust.
- Simulation only: nothing here fires anything. Real ignition needs the arm step and physical arm switch per CLAUDE.md.

## Replaying a flight as a picture or video
`python -m scoudouc_sim.replay LOG.csv --strip out.png` makes a filmstrip (snapshots at even times plus apogee and each ignition). `--mp4 out.mp4 --speed 0.5` makes a half-speed video with a live readout and height/speed/tilt traces; `--gif` works the same way. The rocket is drawn a few times life size so it is visible against tens of metres of flight; the caption says by how much, and every number is true to the log.
