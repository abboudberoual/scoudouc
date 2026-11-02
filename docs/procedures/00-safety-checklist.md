# 00 - Safety checklist (applies to every procedure)

**Purpose:** One page to read aloud before any test, bench session, or flight. If any line cannot be ticked, stop.

Status: DRAFT. Rules marked (CHECK) must be confirmed against the current CAR code and the club launch officer before first use.

## Always (all procedures)
- [ ] A second adult is present for anything involving a motor or igniter. Never test alone.
- [ ] Safety glasses on everyone within 30 m during any motor test.
- [ ] Follow the launch officer (or, on private land, the owner of this project acting as RSO, "range safety officer") and the CAR safety code. Their "no" is final.
- [ ] Written permission from the landowner for the site. Site size rules: A motor 30 m, B 60 m, C 120 m, D 150 m, E to G 300 m clear (CHECK, from docs/research/2026-11-02-launch-sites.md). Static tests count as launches.
- [ ] Motors are certified commercial motors, used as supplied. No modifying, drilling, or reloading. Do not use a damaged or expired motor.
- [ ] Rocket weighs under 1,500 g, total impulse under 160 N-s (low-power class). Has a parachute or similar recovery device.
- [ ] Fire extinguisher (ABC) and a bucket or hose of water at the pad. Dry grass: wet it down or do not fire.
- [ ] Phone with signal, first-aid kit, and the nearest hospital address written down.
- [ ] No flying near people, buildings, roads, power lines, trees, or aircraft. Never fly at a person.
- [ ] Never relight or approach a misfire for 60 seconds after the controller key is removed (see 01).
- [ ] Never put any part of your body over the rocket or over the nozzle line.

## CAR / NAR model rocket safety code items (CHECK wording against CAR)
- [ ] Use only lightweight, non-metal body parts (cardboard, plastic, wood, light 3D print). No metal structure in the airframe or gimbal parts that can become shrapnel.
- [ ] Launch only from a stable launch device with a rod, rail, or (for static tests) a rigid stand.
- [ ] Use an electrical launch system with a remote key and a safety interlock. The key is removed and in the operator's pocket until the countdown.
- [ ] Do not launch if winds are over 15 km/h (this project's limit, stricter than usual).
- [ ] Launch outdoors, away from overhead obstructions, with the rocket pointed within 30 degrees of vertical (a TVC rocket must also be on the pad vertical).
- [ ] Do not launch in clouds or low cloud. Project rule: no cloud base below 300 m, clear visibility.
- [ ] Recover safely: do not retrieve from power lines or trees, do not run towards a rocket still under thrust.
- [ ] Count down aloud and confirm "the range is clear" before every ignition.

## Storage and transport (NRCan rule)
- [ ] NEVER store a rocket with a motor installed. Motors live in their own box, away from the rocket, igniters, batteries and heat.
- [ ] Keep motors in original packaging, cool, dry, locked, away from children and sparks. Do not leave them in a hot car.
- [ ] Check current NRCan consumer-quantity limits and the Oct 2026 amendment SOR/2026-206 before buying or stockpiling (CHECK).
- [ ] Igniters are stored shorted (leads twisted together) and separate from the flight computer and battery.
- [ ] LiPo batteries: stored in a fire bag, never charged unattended, never used if puffed.

## Pyro rules (from CLAUDE.md, non-negotiable)
- [ ] The igniter has its own battery, a physical arm switch in series, and is armed only on the pad.
- [ ] No igniter is ever connected to the circuit indoors or on the bench. Bench uses an LED/resistor dummy load only.
- [ ] No pyro output on ESP32-S3 pins 0, 3, 35, 36, 37, 45, 46 (boot and PSRAM pins; also keep servos and critical sensors off them).
- [ ] Software alone can never fire an igniter: arm switch OFF means no current can flow whatever the code does.
- [ ] Nothing flies before it has passed 02 (bench) and 03 (swing rig).

## Weather quick check
Wind under 15 km/h, no rain, no lightning within 15 km (stop at first thunder), cloud base above 300 m, temperature in the motor maker's range.

## Abort rule
Any doubt, any surprise, any person or animal entering the area: stop, safe the system (arm switch OFF, key out), wait, and talk it through before continuing.
