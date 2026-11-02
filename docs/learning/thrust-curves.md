# Thrust curves

## What it is
A thrust curve is a graph of how hard a motor pushes (newtons, up the side) at each moment (seconds, along the bottom). A motor does not push with one steady force. It spikes quickly when the propellant lights, settles to a plateau, then tails off to zero. Makers publish an "average" curve for each motor on thrustcurve.org. Our stand measures the real curve of the exact motor we burn.

## Why motor-to-motor variation matters for a landing burn
A landing burn is a single push that must cancel the rocket's downward speed just as it reaches the ground. The burn controller has to guess when to start, based on how much push and how much time the motor will give. Two motors of the same name can differ by 10% or more in peak thrust, total impulse and burn time, and they differ with temperature and age. If the real motor gives 10% less push than the published one, the rocket is still falling when the motor runs out. If it gives 10% more or burns shorter, we stop too early or too hard. Measured curves for 3 or more motors of the same type tell us how big that spread is, and therefore how much margin the landing design needs.

## How total impulse is computed
Total impulse is the whole push added up over time, in newton-seconds (N·s). Slice the curve into thin steps. For each step, multiply the average thrust in that step by the step's duration, then add all steps (the "trapezoid rule"). It is the area under the curve. Examples: a steady 10 N for 1 s gives 10 N·s. The motor letter is a bucket of total impulse (C is 5.01 to 10 N·s, D is 10.01 to 20, E is 20.01 to 40, F is 40.01 to 80). `tools/plot_thrust.py` does this automatically and also prints peak thrust and burn time (time spent above 10% of peak).

## What to look for in the plot
- **Peak:** the ignition spike. Is it the same as published? The rocket and the stand must handle it.
- **Plateau:** is it flat or sloping? A falling plateau means thrust is changing during the burn, which a controller must expect.
- **Burn time:** the width of the curve. Compare to the published value.
- **Total impulse:** within about 10% of the published number means a healthy motor and a healthy stand. Far off? Suspect calibration first.
- **Before ignition:** the line should sit at zero. If it drifts, the load cell is warming up or something is rubbing.
- **After burn:** should return to zero. If it sits above zero, the cell shifted or soot or the motor's lost mass changed the tare (a small drop of a few grams is normal as propellant burns off).
- **Noise and wobble:** fast ripples can be real (the motor sputtering) or the stand shaking. If every run shows the same ripple at the same frequency, it is the stand.
- **Overlay:** run `python tools/plot_thrust.py mine.csv published.csv`. The dashed line is the published curve. The shapes should match even if the heights differ a little.
