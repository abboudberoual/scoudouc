# Stand v3 electronics (DAQ = data acquisition: the box that measures and records)

**Use:** ESP32-S3 + **ADS1220** breakout (24-bit ADC, SPI, 20 to 1000 samples/s, 2000 in turbo). **Cheap fallback: HX711 (about CAD 7), with the 80 samples/s caveat below.** The stand does **not** fire the motor: a commercial launch controller with a key does. **No pin in this document touches an igniter.**

## ADS1220 or HX711
| | ADS1220 | HX711 (fallback) |
|---|---|---|
| Cost (est.) | CAD 35 | CAD 7 (saves 28) |
| Rate | 1000 samples/s used | 80 samples/s at best (10 on many boards: cut the RATE trace and tie RATE to 3.3 V) |
| C6 (about 1.85 s burn) | about 1850 points | about 150 points: **the ignition spike and sharp corners are smeared** |
| Verdict | Use | Fine for I-class shape and burn time, poor for C6 detail. Proven stands record 250 samples/s or more. |

The 100 kg cell reads the same way through either board (a 2 mV/V cell at 3.3 V gives about 6.6 mV full scale).

## Wiring, ESP32-S3 N16R8
**Avoided pins (CLAUDE.md): GPIO 0, 3, 35, 36, 37, 45, 46** (boot and PSRAM). I also avoid 33 and 34, 26 to 32 (flash), 19 and 20 (USB), 43 and 44 (serial). None of the pins below is one of those.

| From | To | ESP32-S3 pin |
|---|---|---|
| ADS1220 AVDD and DVDD | 3.3 V | 3V3 |
| ADS1220 AVSS and DGND | ground | GND |
| ADS1220 SCLK | clock | **GPIO 14** |
| ADS1220 DOUT (MISO) | data out | **GPIO 15** |
| ADS1220 DIN (MOSI) | data in | **GPIO 16** |
| ADS1220 CS | chip select | **GPIO 17** |
| ADS1220 DRDY | "new sample ready" | **GPIO 18** |
| ADS1220 RESET | to 3.3 V (reset by SPI command) | 3V3 |
| Cell E+ (red) | AVDD and REFP0 | 3V3 |
| Cell E- (black) | AVSS and REFN0 | GND |
| Cell S+ (white) | AIN0 | |
| Cell S- (green) | AIN1 | |
| microSD CS / MOSI / SCK / MISO | | **GPIO 10 / 11 / 12 / 13** |
| Button to GND (tare / start) | | **GPIO 6** |
| Status LED via 330 ohm | | **GPIO 7** |

**HX711 instead** (same SD, button and LED): VCC to 3V3, GND to GND, **DT to GPIO 4**, **SCK to GPIO 5**, RATE to 3V3, cell red/black to E+/E-, white/green to A+/A-. With 3.3 V supply the cell's 6.6 mV is about half the HX711's range at gain 128: fine.

**Ratiometric reference:** the ADS1220 uses the cell's own excitation as its reference (REFP0/REFN0 across E+/E-), so supply wobble cancels out. Put 10 uF + 100 nF across the ADS1220 supply, close to it. Starting settings (check the data sheet's register section and common-mode limits): AIN0-AIN1, gain 128 with PGA on, external reference, 1000 SPS normal mode, continuous conversion. Full scale is then about 26% of the ADC range, so there is no gain change to make for any motor. If readings are noisy, give the ADS1220 its own low-noise 3.3 V regulator.

## Power and cable
USB power bank into the ESP32 board (about 150 to 250 mA with SD writes). Use a bank that does not switch off at low current, or add a 100 ohm load. **Never** power it from the launch controller battery. Cell cable: shielded 4-core, **3 m (5 m maximum)**, E+/E- as one twisted pair and S+/S- as the other, shield to ground at the DAQ end only, GX12 4-pin plug at the cell end. Cable resistance changes the gain by about 0.15%, so **calibrate with the cable you will use**. DAQ box on the ground **2 m or more** from the stand, out of line with the vent notches (decision 005 says at least 1 m).

## Logging to SD at full rate
At 1000 samples/s a line `time_s,raw_counts,thrust_N` is about 28 bytes, so 28 kB/s. An SD write can stall 100 to 200 ms now and then, so: sample into a ring buffer in PSRAM (the N16R8's 8 MB holds minutes), start recording when the reading crosses 0.5 N, keep a **0.2 s pre-trigger**, write to the card in 4 kB blocks from a second task, and flush when the reading has been under 0.5 N for 5 s. One file per run: `thrust_001.csv`, header row, units in the header (`time_s`, `thrust_N`). Copy to `data/static-fires/`. Firmware for this board is **not** part of this deliverable (v1's `firmware/test-stand` is HX711-based).

## Calibration with known masses (before every test day, with the cable and collar you will use)
Force in newtons = mass in kg x 9.807. Fit a collar, a fresh liner and a spent motor casing, and set the ring in place.
1. `tare` (zero), wait for the reading to settle.
2. Stand a rigid rod or the spent casing in the collar and lower masses onto it, centred, steadied by the ring (never touching it). **Small points first, because that is the C6 range:** 0.2, 0.5, 1, 2 kg (2 to 20 N). Then for bigger motors: 5, 10, 20, 40, 60 kg (weigh sandbags or water jugs on a bathroom scale; 60 kg is 590 N, 60% of range). Take the masses off in reverse order (this shows sticking).
3. The firmware fits a straight line (counts per newton and a zero offset) and stores it.
4. **Pass:** below 20 N every point within **0.5 N**; above that within **1% of reading**; up and down within 0.3 N; the reading does not change when the ring is lifted off or an igniter lead is lifted. Otherwise something is binding or rubbing.
5. The 50 g point (0.49 N) is the noise check: if it wobbles by more than about 0.3 N, look at the shield, the supply, or the cable routing.
6. Never exceed 981 N on the 100 kg cell, and never exceed about 30 N on a 5 kg cell (if you fit one).
