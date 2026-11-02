# PID control: keeping the rocket upright

**What it is.** A PID controller looks at how far the rocket is leaning (the error) and decides how far to swing the motor (the gimbal angle) to push it back. "PID" is three ideas added together:

- **P (proportional):** lean more, push harder. `Kp x tilt`. Too low and the rocket is lazy; too high and it overshoots and wobbles.
- **D (derivative):** how fast it is tipping. `Kd x tilt rate`. This is the brake: it stops the P term from overshooting. In the simulator it uses the gyro's tilt rate directly.
- **I (integral):** a slow memory of leftover lean, `Ki x (tilt added up over time)`. It fixes a steady push to one side (for example an off-centre motor). We start with Ki = 0 and clamp it so it cannot "wind up" while the motor is off.

`gimbal angle = Kp*tilt + Ki*(sum of tilt*dt) + Kd*tilt_rate`

**Why the sign works.** The motor sits below the centre of gravity. Swing the nozzle one way and the thrust pushes the tail that way, which tips the nose the other way. If the rocket leans right, swing the nozzle so the nose comes back left; the simulator's positive gains do exactly that.

**Picking starting gains.** The tilt behaves like `tilt acceleration = (r x T / I) x gimbal angle`, where `r` is the distance from centre of gravity to nozzle, `T` the thrust and `I` the moment of inertia (how hard the body is to spin). Choose how fast you want it to respond (`wn`; about 12 rad/s corrects a lean in roughly a tenth of a second) and a damping of about 0.7, then `Kp = wn^2 * I / (r T)` and `Kd = 2 * 0.7 * wn * I / (r T)`. That is `suggest_gains()` in `control.py`.

**What can go wrong.**
- Thrust changes a lot during a burn (a D12 spikes to about 3x its average), so fixed gains are too gentle late in the burn and too strong at the start. We do not schedule gains yet.
- The servo is slow (about 45 ms lag) and limited to +/-6 degrees. Too much gain plus that lag makes it oscillate.
- With no thrust (coasting) the gimbal does nothing: tilt just drifts at whatever rate it had at burnout. A finless rocket cannot be steered while coasting.

**Try it.** Change `natural_freq_rad_s` in `sim/examples/hop_s1.py` to 6, 12 and 30 and watch the tilt and gimbal curves in the plot.

**Read next.** Brian Douglas's "PID Control" video series on YouTube.
