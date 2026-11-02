// Scoudouc 0 thrust stand: reads a load cell through an HX711, records a motor burn.
// This program NEVER fires anything. A separate commercial launch controller fires the motor.
//
// Plain-language flow:  type "arm" (or press the button) -> 10 s countdown -> stand zeroes itself
// -> waits for thrust to rise above TRIGGER_N -> records 3 s -> prints it and saves a CSV to SD.
#include <Arduino.h>
#include <HX711.h>
#include <SPI.h>
#include <SD.h>
#include <Preferences.h>

// ---- Pins (none of 0, 3, 35, 36, 37, 45, 46; none of 26-37 either: flash/PSRAM on N16R8) ----
const int PIN_HX_DT = 4, PIN_HX_SCK = 5;                           // HX711 data and clock
const int PIN_SD_CS = 10, PIN_SD_MOSI = 11, PIN_SD_SCK = 12, PIN_SD_MISO = 13;
const int PIN_ARM_BTN = 6;                                         // button to GND (internal pull-up)
const int PIN_LED = 7;                                             // LED + 330 ohm to GND

// ---- Settings you may tune ----
const float TRIGGER_N = 1.0f;     // ignition = thrust above this many newtons...
const int TRIGGER_COUNT = 3;      // ...for this many samples in a row (ignores single noise spikes)
const float RECORD_S = 3.0f;      // how long to record after ignition
const int PRE = 16;               // samples kept from just BEFORE ignition (about 0.2 s)
const int MAX_SAMPLES = 400;      // 3 s at 80 Hz is about 240, so this is plenty
const uint32_t COUNTDOWN_MS = 10000;
const float GRAVITY = 9.80665f;   // newtons per kilogram

HX711 hx;
Preferences prefs;                // remembers the calibration after power-off
float countsPerN = 1000.0f;       // calibration: raw HX711 counts per newton (can be negative; fine)
long baseline = 0;                // raw reading that means "zero thrust" (set by tare / arm)
bool sdOk = false;

enum State { IDLE, COUNTDOWN, ARMED, RECORDING } state = IDLE;
struct Sample { uint32_t us; float n; };
Sample ring[PRE];  int ringPos = 0, ringCount = 0;   // the "just before ignition" memory
Sample rec[MAX_SAMPLES];  int recCount = 0;          // the recording itself
uint32_t t0us = 0, countdownEnd = 0;
int aboveCount = 0;  uint32_t firstAboveUs = 0;
String cmd;

float toNewtons(long raw) { return (raw - baseline) / countsPerN; }

// Average of n raw readings (about n/80 seconds). Returns false if the HX711 is not answering.
bool readAverage(int n, long &out) {
  double sum = 0;
  for (int i = 0; i < n; i++) {
    if (!hx.wait_ready_timeout(1000)) { Serial.println("ERROR: HX711 not responding. Check wiring."); return false; }
    sum += hx.read();
  }
  out = (long)(sum / n);
  return true;
}

void tare() {
  long r;
  if (readAverage(40, r)) { baseline = r; Serial.printf("Zeroed. baseline=%ld\n", baseline); }
}

// Calibrate: put a KNOWN weight on the stand (after taring with nothing extra), then "cal 200" for 200 g.
void calibrate(float grams) {
  long r;
  if (grams <= 0 || !readAverage(80, r)) { Serial.println("Usage: cal <grams>  (weight must be on the stand)"); return; }
  countsPerN = (r - baseline) / (grams / 1000.0f * GRAVITY);
  prefs.putFloat("cpn", countsPerN);
  Serial.printf("Calibrated: %.1f counts per newton (saved). A %.0f g weight should now read %.2f N.\n",
                countsPerN, grams, grams / 1000.0f * GRAVITY);
}

void startCountdown() {
  if (state != IDLE) return;
  state = COUNTDOWN;  countdownEnd = millis() + COUNTDOWN_MS;
  Serial.println("Arming in 10 s. Leave the stand now. (This does NOT fire the motor.)");
}

void disarm() { state = IDLE; digitalWrite(PIN_LED, LOW); Serial.println("Disarmed."); }

void saveCsv() {
  if (!sdOk) { Serial.println("# No SD card. Copy the serial output above instead."); return; }
  char name[24];
  for (int i = 1; i < 1000; i++) { snprintf(name, sizeof name, "/thrust_%03d.csv", i); if (!SD.exists(name)) break; }
  File f = SD.open(name, FILE_WRITE);
  if (!f) { Serial.println("# SD write failed. Copy the serial output above instead."); return; }
  f.println("time_s,thrust_n");
  for (int i = 0; i < recCount; i++) f.printf("%.4f,%.3f\n", (int32_t)(rec[i].us - t0us) / 1e6f, rec[i].n);
  f.close();
  Serial.printf("# Saved %s (%d samples)\n", name, recCount);
}

void printSample(const Sample &s) { Serial.printf("%.4f,%.3f\n", (int32_t)(s.us - t0us) / 1e6f, s.n); }

// Called for every new load-cell reading.
void handleSample(uint32_t us, float n) {
  if (state == ARMED) {
    ring[ringPos] = {us, n};  ringPos = (ringPos + 1) % PRE;  if (ringCount < PRE) ringCount++;
    if (n > TRIGGER_N) { if (aboveCount++ == 0) firstAboveUs = us; } else aboveCount = 0;
    if (aboveCount >= TRIGGER_COUNT) {                   // ignition detected
      t0us = firstAboveUs;  state = RECORDING;  recCount = 0;
      Serial.println("# IGNITION DETECTED, recording");
      Serial.println("time_s,thrust_n");
      for (int i = 0; i < ringCount; i++) {              // copy the pre-ignition memory, oldest first
        Sample &s = ring[(ringPos - ringCount + i + PRE) % PRE];
        rec[recCount++] = s;  printSample(s);
      }
    }
  } else if (state == RECORDING) {
    rec[recCount++] = {us, n};  printSample(rec[recCount - 1]);
    if ((int32_t)(us - t0us) / 1e6f >= RECORD_S || recCount >= MAX_SAMPLES) {
      Serial.println("# END");
      saveCsv();  state = IDLE;  digitalWrite(PIN_LED, LOW);
      Serial.println("# Done. Wait for the all-clear before approaching.");
    }
  }
}

void handleCommand(String c) {
  c.trim();
  if (c == "tare") tare();
  else if (c.startsWith("cal ")) calibrate(c.substring(4).toFloat());
  else if (c == "arm") startCountdown();
  else if (c == "disarm") disarm();
  else if (c == "raw") { long r; if (readAverage(10, r)) Serial.printf("raw=%ld  thrust=%.3f N\n", r, toNewtons(r)); }
  else Serial.println("Commands: tare | cal <grams> | raw | arm | disarm");
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);  pinMode(PIN_ARM_BTN, INPUT_PULLUP);
  hx.begin(PIN_HX_DT, PIN_HX_SCK);
  prefs.begin("stand", false);  countsPerN = prefs.getFloat("cpn", countsPerN);
  SPI.begin(PIN_SD_SCK, PIN_SD_MISO, PIN_SD_MOSI, PIN_SD_CS);
  sdOk = SD.begin(PIN_SD_CS, SPI, 4000000);
  Serial.printf("# Scoudouc thrust stand ready. SD: %s. Calibration: %.1f counts/N\n", sdOk ? "ok" : "MISSING", countsPerN);
  handleCommand("help");
}

void loop() {
  while (Serial.available()) {                           // collect typed commands one line at a time
    char ch = Serial.read();
    if (ch == '\n') { handleCommand(cmd); cmd = ""; } else cmd += ch;
  }
  static bool lastBtn = HIGH;  bool btn = digitalRead(PIN_ARM_BTN);
  if (lastBtn == HIGH && btn == LOW) { if (state == IDLE) startCountdown(); else if (state != RECORDING) disarm(); }
  lastBtn = btn;

  if (state == COUNTDOWN) {
    digitalWrite(PIN_LED, (millis() / 125) % 2);         // fast blink while counting down
    if ((int32_t)(millis() - countdownEnd) >= 0) {       // time's up: zero the stand and start listening
      tare();  ringCount = ringPos = aboveCount = 0;  state = ARMED;  digitalWrite(PIN_LED, HIGH);
      Serial.println("# ARMED. Waiting for ignition from the launch controller.");
    }
  }
  if (!hx.is_ready()) return;                            // no new reading yet; check again next loop
  uint32_t us = micros();                                // timestamp the moment the reading arrived
  long raw = hx.read();
  handleSample(us, toNewtons(raw));
}
