# 01 - Static fire on the thrust stand

**Purpose:** Measure real thrust curves of C6 to F15 motors (milestone M3: 3+ motors logged, spread known). The rocket does not fly; the motor is held on a load-cell stand.

Read 00-safety-checklist.md first. Start with C6 and work upward one class at a time (C6, then D12, then E, then F15) only if the previous class went cleanly.

## Required items
- Thrust stand with load cell, amplifier (HX711 or similar), logger (ESP32-S3), rigid motor mount, blast deflector or steel plate under the nozzle line.
- Commercial launch controller with a safety key, continuity light/beep, and at least 5 m of lead wire (use longer wire so people are far away).
- Certified motors (C6, D12, E, F15 as planned), igniters from the same maker, motor-matched closures.
- Known test weights to calibrate the load cell.
- ABC fire extinguisher, bucket or hose of water, safety glasses, first-aid kit, phone, laptop in a car or shelter, tape measure.
- Second adult.

## Site and distances
- Outdoors, flat, cleared of dry grass, on gravel/dirt/wet ground. No overhead wires or branches.
- Clear area (CAR minimums, CHECK): C 120 m, D 150 m, E and F 300 m. This is the strict reading; C/D motors need at least a 30 m radius with nobody in it, but use the larger field if possible. Backyards do not qualify for E or F. E/F need written landowner permission or a club (CQF) launch day.
- Everyone (including operator) at least 30 m from the stand during ignition; for E/F stand at 30 m and prefer a vehicle or barrier. Operator watches from behind a barrier or from 30 m with wire fully extended.
- Wind under 15 km/h. Nothing combustible within 3 m of the stand.

## Setup (before motor install)
- [ ] Stand bolted or staked so it cannot tip. Nozzle points up or horizontally away from everyone and away from the logger.
- [ ] Calibrate the load cell with at least 3 known weights; record readings. Check zero.
- [ ] Logger running with test pulses (press by hand): numbers move, sample rate 500 Hz or better, file saves.
- [ ] Controller key REMOVED. Leads shorted (twisted) at the pad end. Controller battery checked.
- [ ] Extinguisher and water in place within 3 m (but not in the blast line).

## Steps (go / no-go in brackets)
1. Brief the second adult: who counts, who watches, who handles a misfire. [Go: both agree and can state the plan.]
2. Weather and area check. [Go: wind under 15 km/h, area clear, no people or animals within 30 m.]
3. Start logging. [Go: baseline noise steady near zero.]
4. Install the motor in the stand (motor still not wired). Check it is seated and retained. [Go: motor cannot slide out.]
5. Insert the igniter fully, secure it with the closure. Leads still shorted. [Go: igniter tip touches the propellant.]
6. Everyone but the operator walks back to 30 m. Wire is run out. Unshort the leads and connect to the controller clips (clips not touching each other or metal).
7. Operator at the controller. Check the continuity light. [Go: continuity on. No-go: no continuity, go to Abort.]
8. Announce "Range is clear, arming". Insert the key.
9. Count down 5 to 1 aloud. Press and HOLD the launch button.
10. Release the button when the motor lights, or after a few seconds if nothing happens.
11. Misfire wait: remove the key from the controller the moment the button is released if no ignition. Wait a full 60 seconds. Do not approach in that time.
12. After 60 s: shorten the leads (twist), disconnect at the pad end, then approach. A one-time retry only with a new igniter and the launch officer's agreement.
13. After a successful burn: wait until the motor casing is cool and no smoke. Put out any fire with water first, extinguisher second.

## Data capture
- Save the file to `data/static-fires/YYYY-MM-DD_motor_n.csv` with header row and units, e.g. `time_s,thrust_N`.
- Also write down: motor model and batch, ambient temperature, wind, load cell calibration values, mass before/after if possible, any anomaly.
- Quick numbers after each fire: peak thrust (N), burn time (s), total impulse (N-s), compare to the maker's data sheet.

## Post-fire inspection
- [ ] Wait until everything is cool to touch (at least 5 minutes).
- [ ] Stand, mount, load cell, and wires: no cracks, melting, or loosened bolts.
- [ ] Load cell zero re-check: did it drift or get damaged?
- [ ] Spent casing removed and kept; any unburned parts reported.
- [ ] Check for sparks or hot spots in grass for 15 minutes before leaving.

## Abort conditions
- Wind over 15 km/h, someone enters the area, animal or vehicle approaches, fire hazard (dry grass), thunder heard.
- No continuity, a stand that moves or loose parts, logger not recording.
- Any smell, smoke or fire before ignition: key out, short leads only if safe, wait.
- After an abort: key out, 60 s wait, then safe the stand. Never "just check" quickly.
