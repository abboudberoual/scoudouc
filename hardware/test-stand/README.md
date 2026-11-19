# Scoudouc 0 thrust test stand (nozzle UP)

> **Note (2026-11-19):** this v1 stand (single PLA cup, HX711, plywood base) remains the **quick-start**. **v2** (`hardware/test-stand-v2/`, aluminium T-slot frame, swappable load-cell cartridges, ADS1220 recorder, C6 to I-class) is the long-lived stand. v2 is proposed in `docs/decisions/006-test-stand-v2.md`. v1 is not deleted.

**What it does:** stands a small solid motor upright, nozzle up, and measures how hard it pushes (thrust) 80 times a second. It saves the result as a CSV you can plot. Motors: C6 up to F15, thrust 5 to 30 N, burns up to about 1.5 s.

**What it does NOT do:** fire the motor. A commercial launch controller (with its own battery and safety key) does that. The stand's computer has no connection to the igniter at all. This is deliberate: the measuring part can be wrong or crash and it still cannot cause a firing.

*This replaces the old nozzle-down layout (guide rods, blast deflector). `holder.scad` is kept only for reference.*

## How it works (one paragraph)
A load cell is a metal bar with strain gauges glued on. Push on it and its electrical resistance changes a tiny bit. The HX711 board amplifies that tiny signal and turns it into a number. The ESP32-S3 reads the number, converts it to newtons using a calibration factor you measure with known weights, and records it. The motor stands nozzle-up in a printed cup. The exhaust goes up into open air, so the thrust pushes the motor DOWN into the cup floor, the floor presses on the load cell, and the cell rests on a plywood base on the ground. The test pushes the whole stand into the ground, not off it.

```
          exhaust (up, into open air, nothing overhead)
                 ^  ^  ^
              .--|--|--|--.
              |  nozzle   |
      cage    |   MOTOR   |    cage
      ring ===[===========]=== ring   (3 mm gap each side, never touches)
      (post)  | PLA cup +  |  (post)
        |     | card liner |     |
        |     |[cup floor, |     |
        |     | 8 mm thick]|     |
        |  ---+--flange----+---  |
        |     | platform   |     |   thrust pushes DOWN  (v v v)
        |     [ LOAD CELL  ]     |
        |     | free end   |     |
   -----+-----+--riser-----+-----+------
   | PLYWOOD BASE  (400 x 400 x 18 mm)  |  <- bricks / sandbags on the edges
   | o stake hole                 o stake hole |   (two tent stakes, opposite corners)
   ======= bare ground / gravel / paver, nothing flammable ======
   igniter leads: down the cup's inside groove, out the side notch at
   the base, along the plywood to the launch controller 10 m away.
```
The cup can be pushed freely down by a few hundredths of a millimetre (the cell bends that much). Nothing else may touch it.

### Why the cage has a gap (plain words)
The load cell can only measure force that goes through it. If the cage ring rubbed on the cup, part of the thrust would go into the cage, down its posts and into the plywood, and never pass through the cell. The reading would come out too low, and by an amount you cannot predict. So the ring sits 3 mm away from the cup on every side. In a normal burn the cup never moves sideways far enough to touch it. If the thrust is a few degrees off-axis and the cup starts to tilt, it hits the ring before it falls over. That touch is a rare event, and it also tells you the test was off-axis. After a firing, check the cup for scuff marks on the ring side. Also the cage must be fixed to the plywood only, never to the cup or the cell.

## Parts list
| Qty | Part | Notes |
|---|---|---|
| 1 | Load cell, 5 kg, bar type (or a button type) | Comes with 4 wires (red, black, white, green). 5 kg is about 49 N, so the max motor (30 N) uses about 60% of the range. |
| 1 | HX711 amplifier board | Check the **RATE** pin: many boards tie it low = only 10 samples/s. Cut the trace/jumper and connect RATE to 3.3 V for 80 samples/s. |
| 1 | ESP32-S3 N16R8 dev board | You have two. Use one for the stand, keep the other as a spare. |
| 1 | microSD module (SPI) + card (FAT32, 32 GB or less) | Use a 3.3 V logic module. |
| 1 | Momentary push button | Arm button (to GND). |
| 1 | LED + 330 ohm resistor | Armed light. |
| 1 | Battery pack (USB power bank) + USB cable | Lets the stand run away from the laptop. |
| 1 | Printed motor cup | `cup.scad`, STL `cup_29mm_85mm.stl` / `cup_24mm_75mm.stl` / `cup_18mm_75mm.stl`. **PLA**, LIBRARY printer. A **consumable**: print 3 or more spares (LAB printer for a batch). |
| 1 | Printed cage | `cage.scad`, `cage.stl` (fits the 29 mm cup; `cage_24mm_75mm.stl`, `cage_18mm_75mm.stl` for the others). PLA, LIBRARY printer. |
| 1 | Cardboard liner tube per firing | About 1 mm thick, rolled kraft paper or a spare casing wrap, cut a bit shorter than the cup bore. Fresh one every burn. |
| 1 | Plywood base plate, about 400 x 400 x 18 mm (exterior grade) | Flat and stiff. Drill two 10 mm stake holes in opposite corners, 30 mm in from each edge. |
| 1 | Riser block (hardwood or aluminium, about 20 x 20 mm cross-section) | Lifts the cell's fixed end so the free end has at least 3 mm of air below it. |
| 1 | Stiff platform plate (about 60 x 60 x 5 mm, aluminium or 6 mm plywood) | Bolts to the cell's free end and carries the cup's 40 mm bolt square. Only needed with a bar cell. |
| 4 | M4 x 16 bolts, nuts, washers | Cup flange to the platform (40 mm square, set by `bolt_sq`). |
| 2 | M3 or M4 bolts for the load cell fixed end | Check your cell's hole size. |
| 3 | No. 8 / M4 wood screws, 20 mm | Cage feet to the plywood. |
| 2 | Tent stakes (about 200 mm) | Through the plywood corner holes into the ground. |
| 10 kg | Mass for the base: 4 clay bricks (about 2.5 kg each) or 2 sandbags of 5 kg | See "Securing" below. |
| 1 | Commercial launch controller with safety key + 5 m or more of lead wire | Owned or borrowed. Fires the igniter. Not part of this build. |
| 2 | Alligator clips | Controller lead to igniter. |
| 1 | Set of known weights (for example 100 g, 200 g, 500 g, 1 kg) | Must fit inside the cup bore. Coins work (a Canadian toonie is 6.92 g and fits the 29 mm bore); so does a bag of sand weighed on a kitchen scale. |
| 1 | Fire extinguisher or bucket of water, safety glasses | Always present. |
| - | Hookup wire, heat-shrink, zip ties | Keep the 4 load-cell wires short and twisted together. |

### Printed parts (estimates for a Prusa MK3 at 0.2 mm layers, ~50 mm/s, PLA, LIBRARY printer; confirm in the slicer)
| Part | Orientation | Infill | Est. time | Printer |
|---|---|---|---|---|
| `cup_29mm_85mm.stl` | upright, flange on the bed, no supports | 40%, 4 perimeters | ~3.2 h | LIBRARY |
| `cup_24mm_75mm.stl` | same | 40%, 4 perimeters | ~2.8 h | LIBRARY |
| `cup_18mm_75mm.stl` | same | 40%, 4 perimeters | ~2.5 h | LIBRARY |
| `cage.stl` (29 mm cup) | already ring-down, posts up, no supports | 30%, 4 perimeters | ~4.0 h | LIBRARY |
| `cage_24mm_75mm.stl`, `cage_18mm_75mm.stl` | same | 30%, 4 perimeters | ~3.7 h | LIBRARY |
Spare cups for a whole test day can go in a batch on a LAB (Creality) printer. The cage fits a 128 x 111 mm footprint, 113 mm tall, so it also fits the Creality plate. The cage ring is sized to its cup, so use the cage that matches the cup.

No guide rods, linear bearings, steel deflector or tall frame are needed any more.

## Wiring (ESP32-S3 N16R8)
None of these pins are 0, 3, 35, 36, 37, 45, 46. We also avoid GPIO 26 to 32 (flash) and 19/20 (USB) and 43/44 (serial). N16R8 boards use 35, 36, 37 for the octal PSRAM, which is why they are off limits.

| From | To | ESP32-S3 pin |
|---|---|---|
| HX711 VCC | 3.3 V | 3V3 |
| HX711 GND | Ground | GND |
| HX711 DT (data) | GPIO 4 | **GPIO 4** |
| HX711 SCK (clock) | GPIO 5 | **GPIO 5** |
| HX711 RATE | 3.3 V (for 80 Hz) | 3V3 |
| HX711 E+ / E- | Load cell red / black | (on HX711) |
| HX711 A+ / A- | Load cell white / green | (on HX711) |
| SD module VCC | 3.3 V (or 5 V only if the module has its own regulator) | 3V3 |
| SD module GND | Ground | GND |
| SD CS | GPIO 10 | **GPIO 10** |
| SD MOSI | GPIO 11 | **GPIO 11** |
| SD SCK | GPIO 12 | **GPIO 12** |
| SD MISO | GPIO 13 | **GPIO 13** |
| Arm button | other side to GND | **GPIO 6** |
| Armed LED (via 330 ohm) | other side to GND | **GPIO 7** |

There is **no pyro pin** and no output that goes near the igniter. The igniter leads go only to the launch controller.

## Build sequence
1. **Bench the electronics first.** Wire HX711, SD, button, LED on a breadboard. Upload `firmware/test-stand` (`pio run -t upload`). Open the monitor (`pio device monitor`). Type `raw`: you should see a steady number that changes when you press the load cell with a finger.
2. Check the rate: with RATE tied high, readings should arrive about 80 per second. If it feels slow, the RATE pin is still low.
3. Print the cup and the cage (PLA, settings are in the `.scad` headers). Test fit an **empty, spent** motor casing in the cup with a cardboard liner. It should slide in with a little play and sit flat on the floor, standing straight.
4. Drill the plywood (two 10 mm stake holes). Bolt the load cell's fixed end onto the riser, and the riser onto the plywood in the middle. The free end must overhang with at least 3 mm of air below it.
5. Bolt the platform plate to the free end of the cell. Bolt the cup flange to the platform with four M4 bolts. (**Button cell instead:** print the cup with `bolt_holes = false`, set it flat on the button with a dab of Blu-Tack to keep it centred. The cage will stop it wandering.) Mind the arrow on a bar cell: it points in the direction of load, which is down.
6. Measure the height from the plywood to the underside of the cup flange (`stand_h` in `cage.scad`, default 25 mm). If yours differs by more than 3 mm, re-run `python hardware/test-stand/make_holder_stl.py --motor-d 29 --holder-len 85 --stand-h <your number>` and reprint the cage.
7. Place the cage around the cup, turn it so no post lands on the cell bar or its riser, and mark the foot holes. Screw the three feet to the plywood. **Check the ring: the gap to the cup should look even all around, and you should be able to slide a card between ring and cup everywhere.** Press the cup by hand: it must move freely, with nothing rubbing.
8. Move the electronics to a small box on the plywood or ground, at least 1 m to the side, out of the exhaust path. Run all wires low and away from the igniter leads.
9. Calibrate (next section) with the cup, liner and a spent casing fitted.
10. Do a **dry run** with a dummy motor: arm, wait for the countdown, press down on the casing top by hand to trigger recording, confirm a CSV lands on the SD card, then plot it with `tools/plot_thrust.py`.
11. Only then do a live test, following the securing and safety sections.

## Calibrating with known weights
The load cell reports raw counts. Calibration tells the firmware how many counts equal one newton. **With this layout it is simple: the weights go straight into the cup, pressing down exactly the way thrust will.** There is no cell to turn over and no frame to take apart.
1. Fit the cup (with a fresh liner) and the cage, with the stand on its plywood base in place. The bricks are not needed yet.
2. Power the stand, open the serial monitor, type `tare` (zero with just the cup and liner on it). Wait for "Zeroed".
3. Gently lower a known weight into the cup bore so it rests on the floor (stack coins, or lower a weighed bag of sand). Keep it centred and wait for it to settle.
4. Type `cal 500` if the weight is 500 g (use its true mass). The firmware prints counts per newton and saves it to memory.
5. Check: remove the weight, type `tare` again, add a different weight (say 200 g) and type `raw`. It should read mass x 0.00981 N per gram: 200 g is 1.96 N. If it is off by more than 2%, redo step 4 with a heavier weight. If the reading goes negative when you add weight, swap the white and green load-cell wires (A+ and A-) on the HX711.
6. Repeat the check with 3 or 4 weights. If the error grows with weight, the cell or mount is binding.
7. Cage check: with a weight in the cup, note the reading, then lift the cage off (unscrew a foot) and look at the reading again. It must not change. If it does, the ring was touching the cup.
Heavier calibration weights give a more accurate factor: use about 1 kg (9.8 N) if you can; 5 kg is the limit and must never be exceeded.
Recalibrate whenever you change the cup design, the cell, or the wiring.
A loaded motor weighs about 40 to 60 g more than a spent casing and loses roughly 25 g of propellant during the burn, so the reading drifts up by a quarter of a newton at the end. Do `tare` with a motor of the same mass sitting in the cup (before the igniter goes in) if you want to remove that.

## Securing the stand
**How much mass:** put **10 kg** on the plywood (4 clay bricks, or two 5 kg sandbags), spread on the edges and corners, and push the two tent stakes through the corner holes.
The reasoning, in plain words:
- Thrust pushes the stand DOWN into the ground, so for a normal burn the test itself holds the stand in place. The peak is 30 N, which is the weight of about 3 kg.
- The mass is there for the things that are not normal: a sideways kick from an off-axis burn, a tugged wire, wind, an uneven spot of ground, or a motor that behaves badly. 10 kg weighs about 98 N, which is **about 3 times** the 30 N peak. That is a comfortable margin, and it keeps the plywood from rocking, which would show up as noise in the reading.
- The two stakes stop the plywood sliding sideways, and keep it from lifting if something pulls on it. A stake in soft ground holds a few hundred newtons.
- If you ever test a bigger motor than 30 N peak, scale up: at least 3 times the peak thrust in weight (a 60 N motor means 20 kg), and do not go past the load cell's 5 kg (49 N) rating.
Rules for the mass: bricks and bags sit **on the plywood only**, never on the cup, the cell or the cage, and not touching the cell bar. Keep them symmetric so the plywood stays flat. Put the bricks on after calibrating, then check the reading has not moved (re-tare).
Ground: bare dirt, gravel or a paver. Cut or wet any grass within 3 m of the stand. Exhaust and hot bits go straight up and come down around the stand.

## Safety setup
- **Distance:** everyone at least **10 m** away from the stand during a live test (5 m is a bare minimum; check your local club or national rules for the motor class and follow whichever is stricter). Spectators behind you, not beside the stand. Nothing overhead: no trees, wires, roofs or awnings above the nozzle, and no flammable material within 3 m.
- **Remote firing:** the launch controller leads are at least 5 m long, ideally 10 m or more, so you fire from a safe distance. Use the controller's safety key. The key stays **out** of the controller until everyone is clear.
- **Order of operations:** stand secured (bricks on, stakes in), fresh liner in the cup, motor loaded straight, igniter inserted and held with a plug, controller leads **shorted or not connected** while you work, route the igniter leads down the cup groove and out the side notch, clip on igniter, retreat, check continuity light, press `arm` (10 s countdown), key in, count down aloud, fire.
- **Ejection charge (delay motors such as E12-4):** read this one carefully. A model rocket motor's ejection charge sits at the FRONT end, the end opposite the nozzle, and it fires after the delay time, a few seconds after the burn ends. With the nozzle up, the front end is at the BOTTOM, against the cup floor. So expect a loud bang and a puff of hot gas and smoke a few seconds after the burn, coming out of the base (the two side notches), not from the top. It also gives the load cell one more short push downward. Do not walk up after the burn: wait until after the delay time has passed plus 60 s. Keep the wiring and electronics box away from the notch sides (at least 1 m) and out of the lead-notch direction. **Prefer plugged or zero-delay motors (for example E12-0, or a "P" plugged motor) for stand tests where available**, and confirm with your motor supplier what a "-0" motor does at burnout, because some pass a little flame forward. Check whether your firmware's recording window includes the delay time; if it does, the ejection push will appear as a small spike after the burn, and you should ignore it in the plots.
- **Misfire wait:** if the motor does not fire, remove the controller key first, disconnect the battery side, then wait **60 seconds** (a slow motor can still start). Only then approach, from the side, never from above. Also type `disarm` (or press the button) on the stand.
- **Never** stand over the stand, never put your face over the motor, and never fire with the stand in a closed room or on a flammable surface. Never lean over the top of the cup, even with the key out.
- **After every burn:** the casing and cup are hot. Let them cool, then check the PLA cup for softening or warping, and for scuff marks from the cage. Replace the liner every time and the cup if it is soft, warped or discoloured. The cup is a consumable.
- Wear safety glasses. Keep the extinguisher or water bucket within reach, upwind of the stand.
- Only use motors from a legitimate supplier, in the sizes the stand is designed for. Follow the motor's own instructions.
- The ESP32 stays powered from a power bank, never from the launch controller battery. Keep the igniter leads away from the load-cell wires so they do not pick up noise.
- **Heat note:** PLA softens at about 60 degrees C. The cardboard liner, the cup wall and the 3 mm air gap are the heat barrier between a hot casing and the cage ring; the ring sits below the cup rim for that reason. Do not use the stand with motors above F15 or burns longer than 1.5 s without re-checking this.
- A real firing is allowed only after steps 1 to 10 of the build sequence are complete.

## Output
Each run is saved to the SD card as `thrust_001.csv`, `thrust_002.csv`, ... with columns `time_s, thrust_n`. Time 0 is the first sample over the trigger threshold (negative times are the last 0.2 s before ignition). The same lines are printed to the serial monitor, so you can also copy them from there. Copy files to `data/static-fires/` and run `python tools/plot_thrust.py data/static-fires/thrust_001.csv`.

Next: read `docs/learning/thrust-curves.md`.
