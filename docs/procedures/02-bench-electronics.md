# 02 - Bench electronics

**Purpose:** Prove the flight computer, sensors, servos and igniter circuit work and are safe on a table, with NO motor and NO igniter in the room (milestone M4).

Read 00-safety-checklist.md first. Indoors, desk, safety glasses on.

## Required items
- Flight computer (ESP32-S3 for now; pin map in `electronics/flight-computer/` once written), USB cable, laptop.
- IMU (orientation sensor), barometer, two servos with the gimbal frame (no rocket yet), servo battery.
- Pyro circuit: its own battery, a physical arm switch, a dummy load (LED plus series resistor, sized so LED current is within spec), multimeter.
- A bench power supply or a charged battery, a fire bag for LiPos.
- NO igniter. NO motor. Confirm they are in another room, in their boxes.

## Setup
- [ ] Check the pin map: pyro and servo pins are NOT 0, 3, 35, 36, 37, 45, 46. Flag any that are.
- [ ] Pyro battery is separate from the logic battery. Arm switch is OFF and in series with the pyro supply.
- [ ] Radios (Wi-Fi/Bluetooth) set as planned for flight (off in the control loop).

## Steps

### A. First power-up
1. Disconnect servos and pyro board. Power the computer from USB only. [Go: it boots, prints a version line, no hot parts or smoke.]
2. Measure the 3.3 V and 5 V rails. [Go: within 5 percent. No-go: anything else, power off.]
3. Add the logic battery (USB unplugged). [Go: same behavior, current draw sensible.]

### B. IMU axes
4. Print raw accelerometer and gyro. Hold the board flat, still. [Go: Z reads about 1 g, X and Y near 0, gyro near 0.]
5. Tilt nose up, nose down, roll left, roll right, one at a time. Write down which axis moves and which sign. [Go: the axes match the diagram in the docs and the table you record. No-go: mismatched, fix the axis map in firmware, retest.]
6. Leave it still for 60 s. [Go: gyro drift small and estimated tilt stays within 1 degree.]

### C. Servo centering and travel
7. Power the servos from their own battery with the horn off the shaft. Command center. Fit the horn so the gimbal is centered by eye and with a level.
8. Step slowly towards each limit in small increments. Record the point where the gimbal first binds. Set software limits at least 2 degrees inside that. [Go: no buzzing, no hitting the stops.]
9. Command small moves from IMU tilt (hand tilts, servos oppose). [Go: servos move the right way for each axis. Wrong way means flip sign now.]

### D. Barometer
10. Read pressure and temperature for 2 minutes. [Go: steady, noise within about 1 m equivalent altitude.]
11. Raise the board about 1 m, then lower it. [Go: altitude change follows in the right direction by roughly the right amount.]
12. Cover with a hand briefly. [Go: little change in altitude; if big, add foam or shielding.]

### E. Logging
13. Run the control loop for 5 minutes with logging at the planned rate. [Go: 200 Hz or better, no dropped rows, file opens with header and units.]
14. Pull power mid-write. [Go: the file is still readable up to the last flush.]
15. Copy the file to `data/` (as CSV: `time_s,ax_g,...`).

### F. Battery brownout test under servo load
16. With servos on the gimbal, move them back and forth hard (full-travel sweeps) for 60 s while logging battery voltage and watching for resets. [Go: no reset, logged voltage never below the computer's minimum; add a bulk capacitor or separate regulator if it dips.]
17. Stall one servo by hand briefly (peak current). [Go: no reset. No-go: any reset, fix the power before continuing.]

### G. Pyro channel with dummy load (never a real igniter)
18. Confirm the igniter terminals have the dummy load (LED plus resistor) only. Look at it, hold it up, say it aloud.
19. Arm switch OFF. Command "fire" in software. [Go: LED stays dark. Any light means stop and find the fault.]
20. Continuity check with arm OFF if the design has a small sense current. [Go: sense current is well below the igniter's no-fire current from its datasheet. CHECK this value with the safety review.]
21. Arm switch ON, software NOT armed. Command fire. [Go: LED stays dark.]
22. Arm switch ON, software armed, command fire. [Go: LED lights only for the programmed time.]
23. Arm switch ON, power-cycle or reset the computer. [Go: the pyro channel does not light at boot or during reset.]
24. Arm switch OFF again, disconnect the pyro battery, store it separately.

## What to record
- IMU axis table (axis, positive direction), servo center and limits, baro noise, loop rate, brownout minimum voltage, pyro test results line by line, firmware commit/version, date.

## Abort conditions
- Smoke, heat, burning smell, swollen battery: power off, move battery to fire bag outside.
- Any pyro LED lights when it should not: stop, no flight work until the circuit is reviewed.
- A real igniter or motor in the room.
- Reset during brownout test not fixed.
