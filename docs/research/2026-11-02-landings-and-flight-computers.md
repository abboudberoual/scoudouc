# Recent landings + flight computer comparison (2026-11-02, haiku, ~180k tokens for both runs)

## Landings since 2023
- GSP Colibri (Oct 2024): throttleable liquid engine, ~100 kg. Lessons: a gimbal alone cannot control roll (they added side thrusters); leg behaviour; tethered hop testing. Hardware does not transfer.
- JRD Propulsion / Aryan Kapoor (2024): two solid motors (climb, then land), barometer-triggered switch, spent stack ejected, syringe shock-absorber legs. Landed upright. Closest match to our build. No code.
- Sparrow TVC Hopper (2024–25): two D motors, RP2040 board, IMU+barometer fusion, public simulation code, not flown yet.
- Project Horizon (YouTube): publishes nothing; landing unconfirmed. Owner to send link if different channel.

## Flight computer
Teensy 4.1 recommended for flight; owned ESP32-S3 for test stand/logging/telemetry. No commercial TVC computer ships to Canada. No mature open TVC firmware; madflight (MIT) is a possible base layer. Prefer SPI IMU (BMI088 / ICM-42688). Details in docs/decisions/001-flight-computer.md.
