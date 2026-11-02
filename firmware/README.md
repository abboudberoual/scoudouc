# Firmware (ESP32-S3, PlatformIO)

Starting point: https://github.com/intensite/morgan-firmware (ESP32, BMP280 + MPU-6050, 4 servos, 4 pyro channels). Needs porting to the S3 and a licence check before we publish.

Pin rules: avoid GPIO 0, 3, 45, 46 (boot) and 35, 36, 37 (PSRAM on N16R8 boards). Pyro channels only on pins that are low at boot.
