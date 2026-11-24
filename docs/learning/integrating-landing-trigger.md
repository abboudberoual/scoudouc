# The integrating landing trigger, and why timing alone can't land us (T-010)

**Answer first.** A smarter "when to light" rule lands the rocket perfectly when the motor behaves exactly like its data sheet (touchdown about 1 m/s at 660 g and 750 g, E12 up and E12 down). With real motor-to-motor variation of ±15 % it lands **2.5 % of the time** (old rule: 0 %). Even if every motor were within ±1 %, it would land only about 40 % of the time. So no ignition-timing rule is enough: the vehicle needs a way to trim thrust after ignition. That is decision 009 (T-027), whose leading option is the thrust-blocking throttle BPS.space flew on Scout F.

**What the trigger does.** The old rule pretended the landing motor pushes with a constant average thrust. The new one, at every control tick (200 times a second), asks: *"if I lit the motor right now, how fast would I hit the ground?"* It answers by stepping through the whole thrust curve: the igniter delay (free fall), then the real curve shape (the early spike and the long tail), with the rocket getting lighter as propellant burns, plus gravity and air drag. If the motor would stop the rocket above the ground, the answer is the speed after the fall that follows burnout. It lights the motor at the moment when waiting one more tick would make that answer worse. To keep it fast, the predictions are worked out once before flight, as a table over falling speeds, and looked up during the fall.

**Why it still fails.** The trigger has to trust the published curve; it cannot know whether *this* motor is hot or cold. A motor 1 % stronger than expected stops the rocket a little above the ground with burn left over; the rocket rises again, the motor runs out, and it drops from there. A motor 1 % weaker hits the ground still moving. Near the ideal point, each 1 % of thrust error costs about 1 to 3 m/s of touchdown speed, and success needs under 2 m/s. Estes motors are commonly quoted at roughly 4 to 7 % impulse spread (one standard deviation; an estimate, not yet sourced or measured, the static fires will measure ours). The sweep draws thrust evenly across ±s, whose standard deviation is s/1.73, so a 4 to 7 % standard deviation is about ±7 to ±12 % on this table: open-loop timing sits near the bottom of it.

| Thrust spread (±) | 0 % | 1 % | 2 % | 3 % | 5 % | 10 % | 15 % |
|---|---|---|---|---|---|---|---|
| Landing success, 660 g | 100 % | 37 % | 19 % | 12 % | 7 % | 3 % | 1 % |
| Landing success, 750 g | 100 % | 40 % | 19 % | 14 % | 7 % | 3 % | 2 % |

(150 simulated flights per cell; both the climb and the landing motor get their own random spread. Plot: `data/sim/t010_success_vs_spread.png`.)

**C6 and D12 can't land this rocket at all.** Their thrust is too low for 660 to 750 g: the best timing still touches down at 11 to 22 m/s.

**What would change the answer.** Real thrustcurve.org curves (T-011) will move the numbers a little, not the conclusion: the problem is the spread, not the curve shape. Ways out are things that act *after* ignition: a mechanical throttle (pincers or a paddle in the plume), extra small trim motors, or crushable legs as the last margin. These are the options in decision 009.

**Caveats.** 2D simulator, perfect sensing (true height and speed), no wind, a fixed 0.1 s igniter delay (delay spread is another error on top), built-in approximate curves until the library has the real files.

Files: `sim/scoudouc_sim/control.py` (`IntegratingTrigger`), `sim/examples/t010_sweep.py`, `sim/examples/t010_spread.py`, results and plots in `data/sim/t010_*`.
