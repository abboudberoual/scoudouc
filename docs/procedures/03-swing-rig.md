# 03 - Swing rig

**Purpose:** Show that the gimbal and control loop hold Scoudouc 0 upright under thrust, and that it returns to vertical after a push (milestone M5). Requires 02 passed.

Read 00-safety-checklist.md first.

## Required items
- Scoudouc 0 article (about 300 g, 66 mm body): flight computer, IMU, gimbal, servos, ballast in place of everything not yet built.
- Rig: two cords of equal length from a rigid frame, strong enough for 3x the weight; stop cords so it cannot swing wildly.
- Option A (first): ducted fan or similar thrust source in place of the motor, with a speed controller. 
- Option B: a real C6 fired outdoors, same site and distance rules as 01.
- Laptop to download logs, camera at 240 fps if possible (phone slow-motion), tape measure.
- Extinguisher and water for Option B. Safety glasses.

## Setup
- [ ] Rig is fixed and does not wobble when pushed.
- [ ] Cords tied with double knots, equal length, pivot sits near the planned center of gravity (CHECK with the weight and balance).
- [ ] Pyro disconnected for Option A. For Option B, follow 01 for arming, plus 04's arm-on-pad rule.
- [ ] Firmware: control loop running, gimbal limits set from 02, logging on.
- [ ] Photograph the rig and record cord length and mass.

## Steps
1. Hang the article, thrust off. Rotate manually; [Go: it hangs still, the gimbal centers, IMU reads sensible tilt.]
2. Option A: spin the fan to a low setting with the loop disabled. [Go: it does not lurch; no vibration that saturates the IMU.]
3. Enable the loop at low thrust. [Go: article holds near vertical.]
4. Push test: nudge the nose about 10 degrees off vertical by hand (or a soft rod from behind a barrier), release. [Go: returns to vertical in under 1 s, no oscillation (peak overshoot under about 20 percent, no more than one small overshoot).]
5. Repeat the push test 10 times each direction (pitch and yaw). [Go: 10 of 10 pass.]
6. Raise thrust in steps to flight level; repeat 5 pushes at each. [Go: still passes.]
7. Large push of about 20 degrees. [Go: recovers, servos do not hit limits for long.]
8. Option B: fire a real C6 under the same site, distance and misfire rules as 01 (30 m for people, 60 s wait, extinguisher at hand). Do one push test during burn only if the rig is safe; otherwise rely on logs of the burn. [Go: holds vertical through burn.]
9. Disarm, power off, unplug battery, store.

## What a pass looks like
- Returns to within 2 degrees of vertical in under 1 second after a push, without oscillating.
- Servos stay inside limits, no saturation for more than a short time.
- Logs complete, loop rate steady (no dropped samples).

## What to record
- Gains/settings used, thrust level, push size and direction, settling time, overshoot, servo peak angles, loop rate, log file in `data/` as CSV with header and units, video file name, notes.

## Abort conditions
- Rig or cord shows damage, article swings out of control, loose part, or a servo overheating.
- Oscillation grows: cut thrust immediately (kill switch in the operator's hand).
- Option B: any 01 abort condition.
- If it fails, do not fly. Change gains in the simulator first, retest.
