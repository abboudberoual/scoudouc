# Thrust stand v3 in plain language (move to docs/learning/ when you review)

**What it does.** A rocket motor pushes hard for a second or two. To see how hard, you stand the motor on a **load cell** (a small metal block that measures push by how much it squeezes) and record the number many times a second. The result is the **thrust curve**, the thing every flight calculation depends on.

**Why nozzle up.** The flame goes up into open air and the thrust pushes the motor *down* onto the cell, and the cell onto the ground. The test presses the stand into the ground instead of trying to throw it.

**Why copy.** Three stands that have really been fired look alike: a frame, one cell on the floor, the motor on top. v2 ignored that and ended up with 36 parts and CAD 562. v3 copies the core, and each difference is justified in one line in `README.md`.

**The parts.** A *plywood base board* sits on the ground and carries the cell. The *cell* carries a *printed collar* that holds the motor foot. Two *plywood side panels* and two *cross-bars* hold a *printed ring* around the motor in case it tips (it should never touch). Four *ropes* from the base corners to *stakes* stop the stand sliding if the thrust is slightly sideways. A small *DAQ box* (an ESP32 with an ADS1220 chip) sits 2 m away and writes the numbers to an SD card. Firing the motor is done by the separate launch controller, never by this box.

**One cell for every motor.** A load cell's error is a fixed percentage of its *full* rating. The 100 kg cell is wrong by about 0.3 N whatever you put on it. For a big motor (hundreds of N) that is nothing; for a C6 (about 14 N peak) it is about 2% at the peak and 6% on the flat part. That is good enough to see the curve and the burn time. If you want better on small motors, a 5 kg cell fits the same two bolts.

**What can go wrong.** A lead wire pulling on the collar looks like thrust (leave slack). A loose stake lets the stand shift (pull-test it). A PLA collar can soften (use the card liner, bin it if it looks shiny). Too much motor for the cell breaks the cell (check 1.5 x peak against its rating).

**Read next.** `README.md` for sizes and the hand check, `electronics.md` for wiring and calibration, `costing.md` for money, `docs/learning/load-cells-and-sampling.md` for why sample rate matters.
