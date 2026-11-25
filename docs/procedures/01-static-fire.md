# 01 - Static fire on the nozzle-up stand (rung R1)

**Purpose (rung R1 of the test ladder):** measure, for the motors we will fly, (1) the real thrust curve, (2) the **ignition delay** (time from pressing FIRE to thrust onset) and its spread, and (3) the impulse spread between motors of the same lot. R1 feeds decision 009 (landing ignition timing, T-027). The rocket does not fly; the motor stands nozzle-UP on a load cell in stand v3 (`hardware/test-stand-v3/`, decisions 005 and 007).

Read `00-safety-checklist.md` first. Start with a C6 (stand calibration) and work upward one class at a time (C6, then the E-class landing motors, then F and G), up to **G only** (300 m clear; the low-power limit in `00-safety-checklist.md`). H and above need their own ticket only if the previous class went cleanly. This procedure contains **no igniter code**: a commercial launch controller with a removable safety key fires the motor.

## What changed from the earlier version (and why)
- Nozzle-up stand v3 replaces the generic stand: the ejection charge of a delay motor now fires **down** into the collar floor (decision 005).
- The fire command is timestamped on the same clock as the thrust data, so ignition delay can be measured.
- Each motor is weighed before and after, to correct for the propellant weight lost during the burn (it matters only when the motor stands on the cell).
- Landing motors are fired in matched sets from one lot, with lot numbers recorded, so spread is measured, not guessed.
- Logging runs continuously from before arming; the threshold-triggered recording in `hardware/test-stand-v3/electronics.md` would miss the fire command.

## Required items
- Stand v3: tower, 50 kg S-type load cell on the plate (as bought, 490 N ceiling: fine to G; the README's 100 kg cell is for I-class, T-007), printed collar for the motor diameter with its **1 mm kraft-card liner** (PLA heat barrier) and the **2 mm aluminium disc** on the collar floor, guide ring set to the motor's mid-height (README section 2 ring-height rule), four guy ropes and stakes (or the sandbag option, G-class and below only).
- DAQ box (ESP32-S3 + ADC + SD) with the 3 m cell cable, powered from its own USB power bank, **never** from the launch controller battery.
- **Fire-command timestamp:** a read-only fire-command input on the DAQ, as specified by T-022 (firmware) and T-017 (pin map). It only listens; it must not sit in, power, or alter the controller's firing path. It must be **electrically isolated** (optocoupler, or a light sensor on the controller's lamp), must pass T-022/T-017 review and the pyro safety review before it sees a live igniter, and its pin must not be ESP32-S3 GPIO 0, 3, 35, 36, 37, 45 or 46. Until that input exists, use the fallback in "Ignition delay without the input" below.
- Commercial launch controller with a removable safety key, continuity light or beep, and at least 5 m of lead wire (longer is better: it puts people farther away).
- Certified motors, igniters from the same maker, motor-matched closures. **Prefer plugged (-P) motors.** Booster (-0) motors may pass flame forward through the bottom of the motor (T-016 open): until that is answered, treat a -0 like a delay motor whose charge fires at once. Delay motors are allowed with the precautions below.
- Kitchen scale reading to **0.1 g** (motor mass before and after).
- Calibration masses 0.5 to 2 kg and one larger (5 to 10 kg), weighed on a known scale.
- Spring scale or 30 kg weight for the stake pull test.
- Phone or camera that films at 60 frames/s or more (fallback timing and a record of every fire).
- ABC fire extinguisher, bucket or hose of water, safety glasses, first-aid kit, phone, laptop in a car or shelter, tape measure.
- Second adult.

## Site and distances (unchanged)
- Outdoors, flat, cleared of dry grass, on gravel/dirt/wet ground. No overhead wires or branches.
- Clear area (CAR minimums, CHECK): C 120 m, D 150 m, E and F 300 m. This is the strict reading; C/D motors need at least a 30 m radius with nobody in it, but use the larger field if possible. Backyards do not qualify for E or F. E/F need written landowner permission or a club (CQF) launch day.
- Everyone (including operator) at least 30 m from the stand during ignition; for E/F stand at 30 m and prefer a vehicle or barrier. Operator watches from behind a barrier or from 30 m with wire fully extended.
- Wind under 15 km/h. Nothing combustible within 3 m of the stand.
- **Approach the stand at 90 degrees to the vent-notch line** (the notches point front and back; the leads run out the front), never along the lead wire.
- DAQ box on the ground **2 m or more** from the stand and **out of line with the two vent notches** at the collar foot (front and back of the frame).

## Setup (before any motor is near the stand)
- [ ] Stand assembled per `hardware/test-stand-v3/README.md`. Guy ropes tied; **every stake pull-tested to 300 N with less than 10 mm movement** at this site (README section 12). No stakes possible: sandbags, and nothing above G.
- [ ] Collar matches the motor diameter; liner in; disc on the floor; collar not soft, warped or shiny (it is a consumable: bin it if so).
- [ ] Ring at the motor's mid-height; ring top at least 15 mm below the nozzle plane.
- [ ] Logger on, continuous logging (not threshold-triggered), at **320 samples/s or more** (about 3 ms between samples; the NAU7802 maximum; the ADS1220 does 1000).
- [ ] Calibrate the cell with at least 3 known masses including one over 5 kg; record the readings; check the zero returns. Calibrate with the cable you will use.
- [ ] Fire-command input check (if fitted): with the controller **key OUT and no igniter connected**, confirm on the logger that the input reads idle. Do not test it with the key in.
- [ ] Controller key REMOVED and in the operator's pocket. Leads shorted (twisted) at the pad end. Controller battery checked.
- [ ] Extinguisher and water within 3 m but not in the line of the vent notches.

## Motor preparation (at the prep table, away from the stand)
- [ ] Write down: motor type, **lot number** (printed on the motor or the packet), delay, date code, ambient temperature.
- [ ] Weigh the motor **with its closure, without the igniter**: `mass_before_g` to 0.1 g.
- [ ] Landing motors (the type that will fire for the landing burn): fire them as a **matched set of at least 3 from one lot** on the same day, same igniter type, same controller battery. Do not mix lots inside a set.

## Steps (go / no-go in brackets)
1. Brief the second adult: who counts, who watches, who handles a misfire, who films. [Go: both agree and can state the plan.]
2. Weather and area check. [Go: wind under 15 km/h, area clear, no people or animals within 30 m.]
3. Start the logger (continuous) and the camera. Frame the controller (or its light) and the nozzle in one shot if using the video fallback. [Go: baseline noise steady near zero, file growing.]
4. **Nozzle up means the nozzle line is straight up: no face or hand ever goes over the nozzle (00 rule). Work from the side.** Stand the motor in the collar, nozzle UP, on the disc (motor still not wired). Check it is seated and centred in the ring without touching it. [Go: motor cannot fall out; ring gap all round.]
5. Zero: do **not** press tare now. The zero is the mean of the last 1 s of data before the fire command (it includes the motor's weight and any pull from the leads), so nobody touches the DAQ box after the igniter goes in. [Go: reading steady, within 0.1 N over 5 s.]
6. Insert the igniter fully **from the side**, secure it with the closure. Leads run out the collar's -Y notch and the open front. Leads still shorted. [Go: igniter tip touches the propellant.]
7. Everyone but the operator walks back to 30 m. With the **key in the operator's pocket**, the operator unshorts the igniter leads and clips on the lead wire at the stand (clips not touching each other or metal), then walks out to the controller at 30 m or more and connects the lead wire there.
8. Operator at the controller. Check the continuity light. [Go: continuity on. No-go: no continuity, go to Abort.]
9. Announce "Range is clear, arming". Insert the key.
10. Count down 5 to 1 aloud. Press and HOLD the launch button. (The fire-command input or the video marks this moment.)
11. Release the button when the motor lights, or after 3 seconds if nothing happens. **Remove the key at once** in both cases.
12. **Delay or -0 motor:** expect a second bang into the collar floor after the delay; it may pop the empty casing up out of the collar. Do not approach until **delay time + 60 s** after the burn ends. **No second bang from a delay motor: wait 5 more minutes**, then treat the casing as live: do not weigh or pocket it until the charge has fired or the motor has been soaked in water.
13. Misfire: key out, unclip the lead wire at the controller and twist its ends together, wait a full 60 s, do not approach in that time. Then approach from the side, unclip the igniter and twist the igniter leads. One retry only, with a new igniter and the launch officer's agreement. Log the misfire (it is data for the igniter spread too).
14. After a burn: wait until the casing is cool and no smoke. Put out any fire with water first, extinguisher second.
15. Stop the logger only after the wait in step 12. Save the file before touching the stand.

## Data capture (per fire)
- Thrust file: `data/static-fires/YYYY-MM-DD_<motor>_<n>.csv`, header row with units, as in `TEMPLATE.csv`: `time_s,thrust_n,fire_cmd` (`fire_cmd` = 1 while the button is held, 0 otherwise; leave the column out if the input is not fitted).
- Weigh the **spent** motor (casing, closure, any burnt igniter stub removed): `mass_after_g`.
- One row per fire in `data/static-fires/fires.csv` (header already there; units in the column names).
- Video: keep the file; name it like the thrust file.

## Reduction (after the day; the numbers that matter for R1)
- **Thrust onset:** the first sample of 3 in a row above 5 % of that fire's peak thrust. **Burn end:** the last sample above 5 % of peak. Burn time = end − onset.
- **Ignition delay** = onset − fire command (the rising edge of `fire_cmd`, or the video frame where the button is pressed / the controller light changes). Report to the nearest sample; with video, to the nearest frame (17 ms at 60 frames/s, so video is a coarse fallback).
- **Mass-loss correction** (the motor stands on the cell, and the cell was tared with the full motor on it, so as propellant burns away the cell reads its lost weight as less thrust): `lost_g = mass_before_g − mass_after_g`; `I(t)` = impulse so far (after subtracting the pre-command zero); corrected thrust `F_true(t) = F_meas(t) + g × (lost_g / 1000) × I(t) / I_total`, with g = 9.81 m/s². It assumes mass leaves in step with impulse (good enough: the correction is about 0.4 N on an E12 near burnout, roughly 36 g of propellant). For a delay or -0 motor, `lost_g` also includes the delay grain and ejection charge, which leave after the burn: use the maker's propellant mass instead when it is smaller. Report both raw and corrected total impulse.
- `tools/plot_thrust.py` uses 10 % of peak for its burn window; for R1 numbers use the 5 % rule above (until the tool gets a flag).
- **Delay-charge pulse:** a delay motor shows an extra spike (either sign) after the burn; it is not thrust; cut it from the impulse.
- **Spread, per matched set:** mean and range (and the standard deviation once a set has 5 or more) of ignition delay, total impulse and burn time. Compare impulse to the maker's data and to thrustcurve.org.

## Post-fire inspection
- [ ] Wait until everything is cool to touch (at least 5 minutes).
- [ ] Collar: soft, warped, shiny, cracked? Bin it and use a spare. Liner charred through? Replace.
- [ ] Disc: dented or burnt through by the delay charge? Replace before the next delay motor.
- [ ] Stand, ring, cell, guy ropes, stakes and wires: no cracks, melting, loosened screws or stakes that moved.
- [ ] Load cell zero re-check with the motor removed: did it drift or get damaged?
- [ ] Spent casing kept, labelled with the fire number; any unburned parts reported.
- [ ] Find the spent casing (a delay charge can throw it out of the collar). Check for sparks or hot spots in grass for 15 minutes before leaving.

## Abort conditions
- Wind over 15 km/h, someone enters the area, animal or vehicle approaches, fire hazard (dry grass), thunder heard.
- No continuity, a stand that moves, a stake that moved in its pull test, loose parts, logger not recording.
- Any smell, smoke or fire before ignition: key out, short leads only if safe, wait.
- After an abort: key out, 60 s wait (delay time + 60 s if a motor lit), then safe the stand. Never "just check" quickly.

## Ignition delay without the input
If the fire-command input is not yet built (T-022), film the controller and the motor in one frame at 60 frames/s or more and read the delay from the video. Do not wire anything new into the launch controller to get a timestamp: that is a pyro-circuit change and needs its own approved ticket and review.

## Learn more
`docs/learning/ignition-delay-and-mass-loss.md`, `docs/learning/thrust-stand-nozzle-up.md`, `docs/learning/thrust-curves.md`.
