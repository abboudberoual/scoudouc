# Scoudouc 0 thrust test stand

**What it does:** holds a small solid motor, measures how hard it pushes (thrust) 80 times a second, and saves the result as a CSV you can plot. Motors: C6 up to F15, thrust 5 to 30 N, burns up to about 1.5 s.

**What it does NOT do:** fire the motor. A commercial launch controller (with its own battery and safety key) does that. The stand's computer has no connection to the igniter at all. This is deliberate: the measuring part can be wrong or crash and it still cannot cause a firing.

## How it works (one paragraph)
A load cell is a metal bar with strain gauges glued on. Push on it and its electrical resistance changes a tiny bit. The HX711 board amplifies that tiny signal and turns it into a number. The ESP32-S3 reads the number, converts it to newtons using a calibration factor you measure with known weights, and records it. The motor hangs nozzle-down (like in the rocket), so its thrust pushes the motor UP into the top plate, which presses on the load cell. That upward push is the "compression" the cell sees.

```
   rigid top beam (bolted to frame)
   ┌──────────────────────┐
   │   [ load cell ]      │  <- thrust pushes UP into the cell
   ├──────────────────────┤
   │ holder top flange    │
   │ ┌──────────────────┐ │
   │ │  motor (nozzle   │ │
   │ │  pointing down)  │ │
   │ └────────┬─────────┘ │
   │ lip + igniter notch  │
   └──────────┴───────────┘
          exhaust ↓
   ==== blast deflector (angled steel plate) ====
   ==== concrete paver / bare dirt, nothing flammable ====
```
The holder slides freely up and down on two smooth guide rods so that only vertical force reaches the cell. Without guides, the holder swings and you measure noise.

## Parts list
| Qty | Part | Notes |
|---|---|---|
| 1 | Load cell, 5 kg, with a flat pressing surface (bar type or button type) | Comes with 4 wires (red, black, white, green). 5 kg is about 49 N, so the max motor (30 N) uses about 60% of the range. |
| 1 | HX711 amplifier board | Check the **RATE** pin: many boards tie it low = only 10 samples/s. Cut the trace/jumper and connect RATE to 3.3 V for 80 samples/s. |
| 1 | ESP32-S3 N16R8 dev board | You have two. Use one for the stand, keep the other as a spare. |
| 1 | microSD module (SPI) + card (FAT32, 32 GB or less) | Use a 3.3 V logic module. |
| 1 | Momentary push button | Arm button (to GND). |
| 1 | LED + 330 ohm resistor | Armed light. |
| 1 | Battery pack (USB power bank) + USB cable | Lets the stand run away from the laptop. |
| 1 | Printed motor holder | `holder.scad`. Print in PETG or ASA. Print one for 24 mm and one for 29 mm. |
| 4 | M4 x 16 bolts, nuts, washers | Holder flange to load cell platform (spacing set in `holder.scad`, default 40 mm square). |
| 2 | M3 or M4 bolts for the load cell fixed end | Check your cell's hole size. |
| 2 | Smooth guide rods (6 mm, about 250 mm) + 4 linear bearings or printed sleeves | Keeps the holder moving straight up/down. |
| 1 | Rigid frame (aluminium extrusion or 2x4 lumber, 600 mm tall) | Must not flex. Weigh it down or stake it. |
| 1 | Steel plate about 200 x 200 mm, bent or propped at an angle | Blast deflector. Not aluminium, not plastic. |
| 1 | Flame-proof base (concrete paver or bare ground) | Nothing that burns under or near the nozzle. |
| 1 | Commercial launch controller with safety key + 5 m or more of lead wire | Owned or borrowed. Fires the igniter. Not part of this build. |
| 2 | Alligator clips | Controller lead to igniter. |
| 1 | Set of known weights (for example 100 g, 200 g, 500 g, 1 kg) | Coins work: a Canadian nickel is 3.95 g. A kitchen scale checks them. |
| 1 | Fire extinguisher or bucket of water, safety glasses | Always present. |
| - | Hookup wire, heat-shrink, zip ties | Keep the 4 load-cell wires short and twisted together. |

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
3. Print the holder. Test fit an **empty, spent** motor casing. It should slide in with a little play and sit on the lip.
4. Build the frame, fit the guide rods, bolt the load cell's fixed end to the top beam.
5. Bolt the holder flange to the load cell's free end (the pressing platform) with four M4 bolts. The holder must be free to slide on its rods without rubbing.
6. Fit the deflector below the nozzle opening, angled so exhaust goes sideways and away from you and the wiring.
7. Move the electronics to a small box on the frame, well out of the exhaust. Run all wires clear of the flame area.
8. Calibrate (next section) with the holder fitted and a spent casing inside.
9. Do a **dry run** with a dummy motor: arm, wait for the countdown, press down on the holder by hand to trigger recording, confirm a CSV lands on the SD card, then plot it with `tools/plot_thrust.py`.
10. Only then do a live test, following the safety section.

## Calibrating with known weights
The load cell reports raw counts. Calibration tells the firmware how many counts equal one newton.
1. Calibrate on the bench BEFORE mounting the cell upside down in the frame. Stand the load cell on the table with its pressing surface facing up and the holder (with a spent casing inside) resting on it. Gravity then presses on the cell the same way thrust will.
2. Power the stand, open the serial monitor, type `tare` (zero with just the holder on it). Wait for "Zeroed".
3. Gently set a known weight on the holder (centred, directly over the cell). Wait for it to settle.
4. Type `cal 500` if the weight is 500 g (use its true mass). The firmware prints counts per newton and saves it to memory.
5. Check: remove the weight, type `tare` again, add a different weight (say 200 g) and type `raw`. It should read mass x 0.00981 N per gram: 200 g is 1.96 N. If it is off by more than 2%, redo step 4 with a heavier weight.
6. Repeat the check with 3 or 4 weights. If the error grows with weight, the cell or mount is binding.
Heavier calibration weights give a more accurate factor: use about 1 kg (9.8 N) if you can; 5 kg is the limit and must never be exceeded.
Recalibrate whenever you change the holder, the cell, or the wiring.

## Safety setup
- **Distance:** everyone at least **10 m** away from the stand during a live test (5 m is a bare minimum; check your local club or national rules for the motor class and follow whichever is stricter). Spectators behind you, not beside the stand.
- **Remote firing:** the launch controller leads are at least 5 m long, ideally 10 m or more, so you fire from a safe distance. Use the controller's safety key. The key stays **out** of the controller until everyone is clear.
- **Order of operations:** frame secured, motor loaded, igniter inserted and held with a plug, controller leads **shorted or not connected** while you work, clip on igniter, retreat, check continuity light, press `arm` (10 s countdown), key in, count down aloud, fire.
- **Misfire wait:** if the motor does not fire, remove the controller key first, disconnect the battery side, then wait **60 seconds** (a slow motor can still start). Only then approach. Also type `disarm` (or press the button) on the stand.
- **Never** stand over the stand, never put your face over the motor, and never fire with the stand in a closed room or on a flammable surface.
- Wear safety glasses. Keep the extinguisher or water bucket within reach, upwind of the stand.
- Only use motors from a legitimate supplier, in the sizes the stand is designed for. Follow the motor's own instructions.
- The ESP32 stays powered from a power bank, never from the launch controller battery. Keep the igniter leads away from the load-cell wires so they do not pick up noise.
- A real firing is allowed only after steps 1 to 9 of the build sequence are complete.

## Output
Each run is saved to the SD card as `thrust_001.csv`, `thrust_002.csv`, ... with columns `time_s, thrust_n`. Time 0 is the first sample over the trigger threshold (negative times are the last 0.2 s before ignition). The same lines are printed to the serial monitor, so you can also copy them from there. Copy files to `data/static-fires/` and run `python tools/plot_thrust.py data/static-fires/thrust_001.csv`.

Next: read `docs/learning/thrust-curves.md`.
