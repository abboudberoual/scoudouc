# VTOL Rocket

A small solid-fuel model rocket that launches and lands upright under its own thrust, built as fast and cheaply as possible with most of the work done by AI agents.

Project hub (tasks, milestones, costs, risks, learning): see the Notion page "VTOL Rocket — Project Hub".

## Plan in one paragraph

Build a test stand first and measure real motor thrust. Get the ESP32-S3 reading tilt and firing an igniter safely on the bench. Print a gimbal that steers the motor, tune the control loop in a simulator, prove it on a swing rig, then fly without fins under a parachute. Only then add the landing burn and legs.

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
