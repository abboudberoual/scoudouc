# TVC designs, flight computers and landing timing (2026-11-02, haiku, ~82k tokens)

Full report lives in the Notion Research Log. Summary:

- Only BPS.space has landed a hobby solid rocket (2022, after ~7 years). Landing ignition is triggered by barometer altitude; four rubber-band-released carbon legs.
- Free gimbal mount: Garrett-R16/TVC_Mount (MIT), 29 mm motor, 74 mm body, ±6°.
- ESP32 firmware start: intensite/morgan-firmware (BMP280 + MPU-6050, 4 servos, 4 pyro). Unproven in flight, no licence.
- Clean control-loop code: hyphenspace/opentvc (MIT).
- Motors used: Estes F15, Apogee F10, Aerotech G8/G11. 9 g servos common.
- Gaps: no public landing-controller code, no published rocket mass or full landing log.

Sources: bps.space/products/thrust-vector-control, github.com/Garrett-R16/TVC_Mount, github.com/intensite/morgan-firmware, github.com/hyphenspace/opentvc, makezine.com (thrust-vectored rockets article), hackaday.com/tag/joe-barnard
