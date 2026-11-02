# 04 - First flight, Scoudouc 1 "Hop"

**Purpose:** A 10 to 20 m hop of the finless Scoudouc 1 (about 350 g, 66 mm, 1x D12) steered by the gimbal, landing under a parachute (milestone M6). Requires 02 and 03 passed.

Read 00-safety-checklist.md first. Fly at a club launch or on permitted private land with the launch officer's approval.

## Required items
- Scoudouc 1 with backup parachute packed and checked, flight computer, gimbal, logging.
- One D12 motor, one igniter, motor retention.
- Launch pad with a rigid vertical rod or stand, blast deflector, commercial launch controller with key and 5 m or more of lead (use 30 m of lead if the site allows).
- Pyro battery, physical arm switch (accessible from outside the rocket), logic battery.
- Extinguisher, water, safety glasses, first-aid kit, phone, tape measure, laptop.
- Checklists printed, pen. Second adult.

## Go / no-go weather
- Wind under 15 km/h (check at ground and with a streamer).
- No cloud below 300 m and clear sky above.
- No rain, fog, or thunder. Temperature within the motor's range.
- Site clear: 150 m for D motor (CHECK), with a clear direction away from people, roads and trees.

## Pad setup (arm switch OFF throughout)
- [ ] Both batteries fully charged and measured. Pyro battery disconnected.
- [ ] Parachute packed and wadding in place; shock cord, ejection path checked. Recovery has a tested ejection (not tested with a real charge indoors).
- [ ] Mass and balance recorded; CG where planned.
- [ ] Gimbal moves free; servos center; last firmware flashed and commit noted.
- [ ] Rocket carried to the pad with the motor NOT yet installed.
- [ ] On the pad: install motor, then igniter, secure, leads shorted.
- [ ] Rocket vertical (level check, within 1 degree). IMU initialized with the rocket still.
- [ ] Logging started. Data check: tilt reads ~0, baro altitude steady.

## Arming and countdown
1. Everyone except the operator moves back 30 m or more (the launch officer's distance if larger).
2. With key out and leads shorted, switch the physical arm switch ON ONLY on the pad. [Go: status indicator shows armed, pyro continuity good.]
3. Unshort leads and clip to the controller. [Go: continuity light on.]
4. Announce "Range clear, arming"; insert key; the launch officer says go.
5. Countdown 5 to 1 aloud. Hold the button.
6. Watch the flight. Stay clear of the pad while it is landing.
7. If no ignition: release the button, remove the key, wait 60 s. Switch the arm switch OFF only after the 60 s wait. Then proceed under 01 misfire rules.

## Recovery
- Do not run to the rocket until it has landed and the range officer says so. Watch for the parachute drifting toward people or trees.
- Approach the rocket with the arm switch assumed OFF; switch it OFF first. Check the motor is not hot, treat any unburned igniter carefully.
- Do not retrieve from power lines or trees.
- Photograph the rocket and the landing place before moving it.

## Log download
- Power down, then connect to the laptop. Copy the log to `data/flights/YYYY-MM-DD_S1_flight1.csv` with header row and units.
- Back up before opening. Note the weather, motor batch, and times.

## Post-flight inspection
- Airframe, fins (none), gimbal, servo horns, wiring, parachute, motor mount: no cracks, burns, loose parts.
- Battery temperature and charge; return LiPos to a fire bag.

## The one question to answer after the flight
**Did the rocket stay within 10 degrees of vertical during the burn?** (Check the tilt trace in the log.) Write down yes/no plus the peak tilt angle, and one sentence on why.

## Abort conditions
- Wind or cloud outside the limits, people in the area, any smell or smoke, any pyro anomaly, any mismatch in the checklist.
- Parachute not packed, battery below threshold, log not recording.
- No continuity. Arm switch OFF, key out, 60 s wait.
