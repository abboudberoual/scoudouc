# Ignition delay and mass loss: two things the stand must measure for R1

**Ignition delay** is the time between pressing FIRE and the motor actually pushing. It has two parts: the igniter heating up until it flashes (rung R0.5 measures that alone), and the propellant catching and building pressure. For a landing burn it is the number that matters most: if the delay varies by 0.05 s, a rocket falling at 10 m/s touches down with about 6 m/s of error (decision 009, T-027). So we do not just want the average, we want the spread.

**How we measure it:** the logger records two things on one clock: the thrust, and a line that goes high while the FIRE button is held. Delay = first moment thrust rises above 5 % of its peak − the moment the button went down. One clock matters: two devices with their own clocks drift apart by more than the thing we are measuring. Until that input exists, a 60 frames/s video with the controller and the motor in shot gives the same number to within about 17 ms.

**Why matched sets:** motors from one production lot are as alike as they get. Firing 3 or more of the same lot, with the same igniter and battery, tells us the spread we will actually fly with. Mixing lots would hide which part of the spread is the lot and which is the motor.

**Mass loss:** our motor stands nozzle-up *on* the load cell. We zero the cell with the full motor on it (the average of the last second before FIRE). As the propellant burns, about 36 g of it leaves an E12, so the cell feels 0.35 N less weight by the end, and reads that as 0.35 N less thrust. The fix: weigh the motor before and after, and add the lost weight back in proportion to how much of the burn has happened. It changes total impulse by about 1 to 2 % on an E: small, but the same size as the motor-to-motor spread we are trying to see. A stand that holds the motor horizontally avoids this, which is one of the trade-offs of nozzle-up (decision 005).

**What can go wrong:** logging that starts only when thrust rises (it misses the button press); weighing with the igniter still in; reading a delay motor's ejection kick as thrust; mixing lots in a set.

**Read next:** `docs/procedures/01-static-fire.md` (the procedure), `docs/learning/landing-burn-timing.md`.
