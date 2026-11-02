# Thrust stand, nozzle-up: what and why

**The idea:** stand the motor on its tail with the nozzle pointing at the sky. The exhaust goes up and away. The thrust pushes the motor down onto a load cell sitting on a plywood board on the ground. The test squeezes the stand into the earth instead of trying to lift it.

**Why this beats hanging it nozzle-down:** no frame, no guide rods and no steel blast plate. The old layout needed the motor to slide on rods without friction, and any rubbing stole thrust. Now the cup sits straight on the cell.

**What the load cell does:** it bends a hair under load and the strain gauges turn that into a tiny electrical change. It can only feel force that passes through it. That is why the cage ring around the cup keeps a 3 mm gap: if it touched, some thrust would leak into the cage and the reading would be low.

**Securing:** thrust presses the stand down, so the 10 kg of bricks and two tent stakes are for the unusual things: sideways kicks, tugged wires, wind. 10 kg is about 98 N, roughly 3 times the 30 N peak.

**Watch out for:**
- The ejection charge in delay motors (E12-4) fires from the FRONT of the motor. Nozzle-up, that is the bottom, so the bang and smoke come out of the base notches a few seconds after the burn, and push down on the cell once more. Prefer plugged or zero-delay motors for stand tests.
- PLA softens near a hot casing. The cardboard liner and the cup wall are a heat barrier; the cup is a consumable.
- A motor's weight changes during the burn (about 25 g of propellant), which shows up as roughly a quarter of a newton at the end.

**Calibration is easy:** put known weights into the cup and type `cal`. Gravity pushes down just like thrust.

Read next: `docs/learning/thrust-curves.md`.
