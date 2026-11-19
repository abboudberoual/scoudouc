# Stand v2 electronics (DAQ = data acquisition: the box that measures and records)

**Recommended:** ESP32-S3 + **ADS1220** (24-bit ADC, SPI, up to 2000 samples/s). **Cheap fallback:** ESP32-S3 + **NAU7802** (24-bit, I2C, 320 samples/s). The stand does **not** fire the motor.

## Why not the HX711
HX711 runs at 80 samples/s at best (10 on many boards). An ignition spike lasts a few milliseconds and a thrust curve has fast corners, so 80 per second smears them. Proven stands record 250 samples/s or more, ideally about 1000. Source: `docs/research/` findings summarised in the task brief (HX711 80 SPS too slow; NAU7802 320 SPS; ADS1220 about 2 kSPS; ADS1256 up to 30 kSPS).

| Chip | Rate | Interface | Verdict |
|---|---|---|---|
| ADS1220 | 20 to 1000 SPS normal, 2000 turbo | SPI | **Use.** Run at 1000 SPS, gain 128 |
| NAU7802 | up to 320 SPS | I2C | Fallback. Saves only about CAD 5 (see `costing.md`) and is 3x slower |
| ADS1256 | up to 30 kSPS | SPI | Overkill for now; consider if you want 5 V excitation |

## Wiring (ESP32-S3 N16R8)
None of these use GPIO **0, 3, 35, 36, 37, 45, 46** (boot and PSRAM pins). I also avoid GPIO 33 and 34 (also used by octal PSRAM on N16R8), 26 to 32 (flash), 19 and 20 (USB), 43 and 44 (serial). **No pin touches an igniter.**

| From | To | ESP32-S3 pin |
|---|---|---|
| ADS1220 AVDD and DVDD | 3.3 V | 3V3 |
| ADS1220 AVSS and DGND | ground | GND |
| ADS1220 SCLK | clock | **GPIO 14** |
| ADS1220 DOUT (MISO) | data out | **GPIO 15** |
| ADS1220 DIN (MOSI) | data in | **GPIO 16** |
| ADS1220 CS | chip select | **GPIO 17** |
| ADS1220 DRDY | "new sample ready" interrupt | **GPIO 18** |
| ADS1220 RESET | tie to 3.3 V (reset by SPI command) | 3V3 |
| Cell E+ (red, GX12 pin 1) | AVDD and REFP0 | 3V3 |
| Cell E- (black, pin 2) | AVSS and REFN0 | GND |
| Cell S+ (white, pin 3) | AIN0 | |
| Cell S- (green, pin 4) | AIN1 | |
| SD CS / MOSI / SCK / MISO | as v1 | **GPIO 10 / 11 / 12 / 13** |
| Arm button (to GND) | | **GPIO 6** |
| Armed LED (via 330 ohm) | | **GPIO 7** |

Use the cell's own excitation as the ADC reference (REFP0/REFN0 across E+/E-): then supply wobble cancels out of the reading ("ratiometric"). Put 10 uF + 100 nF across the ADS1220 supply, as close as you can. Settings to start from (check the data sheet, section on registers, and the common-mode limits): input AIN0-AIN1, gain 128 with PGA on, external reference, 1000 SPS normal mode, continuous conversion. A 2 mV/V cell at 3.3 V gives about 6.6 mV full scale, a quarter of the range at gain 128, so the cartridge swap needs no gain change.

## Power
USB power bank into the ESP32 board. About 150 to 250 mA with SD writes; the bridge takes about 3 to 10 mA. Use a bank that does not switch off at low current (or add a 100 ohm load). **Never** power it from the launch controller battery. Optional: a separate low-noise 3.3 V regulator for the ADS1220 if the readings are noisy.

## Cable to the cell
Shielded 4-core cable (for example 22 AWG, 2 twisted pairs plus shield), **3 m, 5 m maximum**. Twist E+/E- as one pair and S+/S- as the other. Shield to ground at the DAQ end only. GX12 plug at the cartridge end (same pinout for all three cartridges). Route it away from the igniter leads (cross at 90 degrees, at least 1 m apart otherwise). Cable resistance (about 0.5 ohm in total for 3 m) changes the gain by about 0.15%; **calibrate with the cable you will use**.

## Calibration by known masses (every cartridge, every test day)
Force in newtons = mass in kg x 9.807.
1. Fit the cartridge, a cup, a fresh liner and a spent casing. Select the cartridge in the serial monitor (`cart 5`, `cart 50`, `cart 200`) so its calibration is stored separately.
2. `tare` (zero). Wait for the reading to settle.
3. Lower known masses into the cup, centred. Use at least four points up to **50 to 70% of the expected peak** for the chosen cartridge, then take them off in reverse (this shows sticking). Suggested: CART-5: 0.5, 1, 2, 3 kg. CART-50: 5, 10, 20, 30 kg (water jugs, weighed sand bags). CART-200: 10, 20, 40, 60 kg (weigh bags on a bathroom scale, or use plates).
4. The firmware fits a straight line (counts per newton and zero offset) and stores it with the cartridge ID.
5. **Pass:** every point within 1% of full scale or better than 1% of reading above 20% of range; up and down within 0.5% of full scale; reading does not change when the guide ring is lifted off. Otherwise something is binding or rubbing.
6. Never exceed the cell's rating. Bar cells have overload stops, S-types do not.

## Logging to SD at full rate
At 1000 SPS each line `time_s,raw_counts,thrust_N` is about 28 bytes, so 28 kB/s. An SD card write can stall 100 to 200 ms now and then, so:
- DRDY interrupt on GPIO 18 stamps each sample with the ESP32 microsecond clock and puts it in a **ring buffer in PSRAM** (8 MB, minutes of data); a second task writes to SD in 4 kB blocks.
- Keep a 0.5 s **pre-trigger** buffer; start at thrust above a threshold (about 3% of the cartridge rating); stop when it is below the threshold for 2 s, or 20 s maximum (so a delay-charge push is captured).
- Pre-allocate the file (about 2 MB) before arming so the SD card does not stall allocating space; flush at the end.
- Header row and units, as repo rules require: `time_s,raw_counts,thrust_N`. Time 0 = first sample over threshold. Copy to `data/static-fires/`.
- Serial live view: a decimated 20 Hz line stream over USB for a laptop plot; the SD file keeps every sample. Commands: `tare`, `cart N`, `cal <mass_kg>`, `raw`, `arm`, `disarm`.
- Firmware for v2 is **not written yet** (v1 firmware in `firmware/test-stand` is for the HX711); this document is the spec.

## Why ignition stays on a separate commercial launch controller
The measuring board is the part most likely to be wrong, crash, reboot or glitch (a SD card stall, a bad solder joint, a brown-out). If it also fired the igniter, any of those could fire a motor at the wrong time, and a stuck pin could do it with nobody ready. A commercial controller has its own battery, a physical safety key that is out until everyone is clear, a continuity light, and a momentary switch you hold, so a firing needs a deliberate human action by someone who can see the stand. The stand's board has no wire to the igniter at all, so it **cannot** cause a firing. Procedure: key out until clear, key in, 5 s countdown aloud, hold the button, release on ignition, if nothing happens key out and wait 60 s.
