# 004 — Sensors: IMU, barometer, servos

**Date:** 2026-11-02  **Status:** proposed

## What we decided
Start cheap and upgrade on evidence. Prices are rough CAD estimates; check before buying.
- **S0 bench:** MPU-6050 + BMP280 + SG90 servos (about CAD 15 for all).
- **S1:** keep them unless the triggers below fire; flight is the first real vibration test.
- **S2:** ICM-42688 or BMI088 (SPI) + BMP390 + 9 g metal-gear servos (MG90S).
- **20 kg servos:** not before S3, and only if bench data asks for them.

## IMU (measures turning rate and acceleration)
| | MPU-6050 | BMI088 | ICM-42688 |
|---|---|---|---|
| Price (est.) | ~CAD 4 | ~CAD 25 (Newark Canada listed) | ~CAD 15-20 |
| Bus | I2C | SPI | SPI |
| Gyro / accel range | 2000 deg/s / 16 g | 2000 deg/s / 24 g | 2000 deg/s / 16 g |
| Noise and vibration | Noisier; many fake chips | Built for vibration | Very low noise |
| Verdict | Learn on it | Best vibration design | Best value |

Both newer parts match the SPI preference in decision 001. Accel range matters: the motor gives 5-6 g, but a hard landing can pass 16 g; the log will clip, which is fine for bench learning.
**Upgrade when:** a static fire shows gyro noise that disturbs the control loop, or before S2. Do not use the I2C MPU-6050 for the landing run.

## Barometer (measures height from air pressure)
| | BMP280 | BMP390 |
|---|---|---|
| Price (est.) | ~CAD 4 | ~CAD 12-15 |
| Noise | Roughly 1 m of height jitter | Noticeably lower, faster readout |
| Verdict | Fine for hops | Better for a height-triggered landing burn |

Both need a vent hole and a foam cover (light and wind upset them).
**Upgrade when:** bench logs show height jitter bigger than the margin in the landing-ignition altitude, or before S2.

## Servos (move the gimbal)
| | SG90 | 9 g metal gear (MG90S) | 20 kg (e.g. DS3218) |
|---|---|---|---|
| Price (est.) | ~CAD 3-4 | ~CAD 5-8 | ~CAD 20-30 |
| Mass each | 9 g | 13.4 g | ~60 g |
| Torque | ~1.6 kg·cm | ~2.2 kg·cm | ~20 kg·cm |
| Weak point | Plastic gears strip, slop | Better gears, still some slop | Heavy, needs 6-7 V and amps |

The gimbal only swings ±6° and the thrust line passes near the pivot, so the real load is small; measure it on S0. Two 20 kg servos add ~93 g to S2 and cut thrust-to-weight from 1.70 to about 1.49.
**Upgrade when:** servos stall, strip gears, or visibly lag on the S0 hanging test.

## What we gave up
A less noisy IMU and barometer on S0 and S1, in exchange for about CAD 40 saved and a real reason to learn why the better parts exist.

## Learn more
https://github.com/hyphenspace/opentvc
