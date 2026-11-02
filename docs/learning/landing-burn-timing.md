# Landing-burn timing: when to light the landing motor

**The problem.** A solid motor has no throttle. Once lit it burns for a fixed time at whatever thrust it has. So the only decision is *when* to light it. Too early: it stops the rocket in mid-air, runs out, and the rocket falls the rest of the way. Too late: it cannot slow down in time and hits the ground fast.

**The stopping-distance formula.** If the motor gives thrust `T` and the rocket weighs `m`, the motor accelerates it upward at `T/m`, but gravity pulls down at `g` (9.81 m/s^2). The net braking is

`a = T/m - g`

A rocket falling at speed `v` and braking at `a` needs this much distance to stop (from the standard rule `v^2 = 2 a d`):

`d_stop = v^2 / (2 * (T/m - g))`

The rule: **light the motor when `d_stop` is at least the height above the ground.** The simulator also adds `v x delay` for the igniter's lag, and an optional safety margin.

**A worked example.** Rocket 0.8 kg, motor 20 N, falling at 12 m/s. `T/m = 25`, so `a = 25 - 9.81 = 15.2 m/s^2`. `d_stop = 144 / (2 x 15.2) = 4.7 m`. Light it at about 4.7 m (plus the delay allowance).

**Why the formula is not enough.** It assumes thrust stays constant for as long as needed. Real motors:
- Spike early and then settle, so most of the braking comes at the start.
- Vary by about +/-15% between motors, which moves the best ignition height by metres.
- Burn out after 2 to 3 seconds. If the motor is strong enough to stop you before the ground it also pushes you back up for the rest of its burn, and then you drop.
- If `T/m` is below `g` the denominator is zero or negative: the motor can never stop the fall.

**What the first simulator runs show.** With a 900 g rocket, E12 up and E12 down, the E12 barely out-pushes gravity (about 3 m/s^2 of net braking), so it cannot cancel a fall from about 20 m: touchdown is around 14 m/s, not under 2 m/s. A stronger or lighter setup, or a parachute assist, is a design question the simulator is meant to answer before we build.

**Read next.** Search "suicide burn" or "hoverslam" for explanations of rocket powered descent.
