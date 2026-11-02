# The Spirit of Scoudouc

A small solid-fuel model rocket, called **Scoudouc**, that launches and lands upright under its own thrust, built as fast and cheaply as possible with most of the work done by AI agents.

Project hub (tasks, milestones, costs, risks, learning): see the Notion page "The Spirit of Scoudouc — Project Hub".

## The name

Scoudouc is a rural area in New Brunswick with nothing remarkable about it, except that this project's owner grew up there on a farm. The Spirit of St. Louis was built in about two months on a small budget by a small company for an unknown pilot, after the famous names turned the job down. It won by being simple and fast. That is the spirit here.

## Milestones

| # | Milestone | Done when |
|---|---|---|
| M0 | Infrastructure live | Notion hub, repo, agents, first research in |
| M1 | Concept decided | Decision files for airframe, motors, flight computer, sensors, altitude, site; mass budget under 1,500 g with backup chute |
| M2 | Design package complete | Schematic + pin map, OpenRocket model, CAD, Python simulator (loop tuned, landing timing tested), written test procedures, top-model safety review. Nothing bought beyond test-stand parts before this |
| M3 | Test stand measures real thrust | 3+ motors logged, variation known |
| M4 | Flight computer reads orientation on the bench | 200+ Hz, logs, arms and fires a test igniter safely |
| M5 | Gimbal holds the rocket upright on a swing rig | Returns to vertical after a push |
| M6 | First finless TVC flight | Straight ascent, parachute recovery, full log |
| M7 | Landing burn timed in sim and on a drop test | Near-zero speed at ground across measured thrust spread |
| M8 | First propulsive landing attempt | Lands on legs, or data says why not |
| M9 | Public demo and write-up | Video, cost, token usage, lessons |

## Plan in one paragraph

Decide the concept and finish the design on paper and in simulation first. Then build a test stand and measure real motor thrust. Get the ESP32-S3 reading tilt and firing an igniter safely on the bench. Print a gimbal that steers the motor, tune the control loop in a simulator, prove it on a swing rig, then fly without fins under a parachute. Only then add the landing burn and legs.

## Folder layout

| Folder | What lives here |
|---|---|
| `docs/learning/` | Plain-language explainers for each subsystem, written as it gets built |
| `docs/decisions/` | One short file per decision (motor class, airframe size, sensors...) and why |
| `docs/research/` | Research agent reports, mirrored from the Notion Research Log |
| `hardware/gimbal/` | Gimbal mount CAD and print files |
| `hardware/legs/` | Landing leg design |
| `hardware/test-stand/` | Load-cell thrust stand |
| `electronics/flight-computer/` | Wiring, pin map, schematics |
| `electronics/pyro/` | Igniter circuit (safety-reviewed before use) |
| `firmware/` | ESP32-S3 flight code (PlatformIO) |
| `sim/` | Python flight and landing-burn simulator |
| `data/static-fires/` | Measured thrust curves |
| `data/flights/` | Flight logs |
| `tools/` | Scripts: plot thrust curves, parse logs, sync Notion |
| `.claude/agents/` | Agent definitions with fixed model choices |

## Safety rules (non-negotiable)

- Igniters get their own battery, a physical arm switch, and are armed only on the pad.
- No pyro channel on an ESP32 boot/strapping pin.
- Every flight follows the club's launch officer and the CAR safety code.
- Nothing flies before it has passed the bench and swing-rig tests.
