# Mass and thrust-to-weight

**What it is.** Thrust-to-weight (T/W) is how hard the motor pushes divided by how hard gravity pulls the whole rocket down. Weight is mass x 9.81. A 660 g rocket weighs 6.5 N; an E12 pushes about 11 N on average, so T/W is 11 / 6.5 = 1.7.

**Why we care.** Below 1 the rocket never leaves the pad. Just above 1 it crawls up and wobbles, and a gimbal needs speed and push to steer. Our rule is above 1.3 at liftoff. For the landing burn the rocket is already falling, so T/W above 1 is the floor: it must be strong enough to stop the fall.

**Why mass is everything.** Every gram comes off the margin. The roadmap's 900 g for Scoudouc 2 gives 1.25 on an E12, which fails. Our parts list adds up to about 660 g, which passes at 1.7. Weigh the real parts and update docs/mass-budget.csv as you go.

**Watch out.**
- "Average thrust" hides a short spike at ignition and a weak tail. Cold weather lowers thrust.
- A solid motor cannot throttle. More thrust in the landing burn is not automatically better, because a rocket that stops early climbs again.
- Mass drops as propellant burns, so T/W rises during the burn.

**Read next.** thrustcurve.org: pick a motor and look at the curve, not only the average.
