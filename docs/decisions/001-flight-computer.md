# 001 — Flight computer platform

**Date:** 2026-11-02  **Status:** proposed

## What we decided
Not decided yet. The ESP32-S3 in the early plan was a placeholder because two are already owned. The comparison (Notion Research Log, "Flight computer comparison") recommends a Teensy 4.1 for the flight loop and the ESP32-S3 for the test stand, logging and pad telemetry.

## Options
- **Teensy 4.1** (~CAD 45–55): fastest, no radio jitter, SD slot, most TVC precedent. Buy one.
- **ESP32-S3** (owned): workable if radios are off in flight and servos/igniters avoid boot pins. Zero cost, Wi-Fi for pad checks.
- **Pico 2** (~CAD 10): cheap spare with floating-point hardware.

## What we gave up (if Teensy)
About CAD 50 and the Wi-Fi convenience; the ESP32 still does telemetry on the ground.

## Learn more
https://www.pcbway.com/project/shareproject/Tortuga_A_TVC_Avionics_Board_7ad2a5ee.html
