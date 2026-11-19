"""Stand v2 bill of materials (CAD, before ~15% Quebec tax). ALL PRICES ARE ESTIMATES unless noted.
Used by drawing.py (callout legend) and run directly to print the totals.  qty_min = Minimum (C-G, 2 cartridges),
qty_rec = Recommended (C-I, 3 cartridges).  Future = Recommended + HPR module (FUTURE list below)."""
from collections import OrderedDict

P, B = "PRINTED", "PURCHASED"
# n, name, kind, qty_min, qty_rec, unit_cad, source, group, kg_each
ITEMS = [
 (1, "Long rail, 2040 x 500 mm", B, 2, 2, 18.0, "Amazon.ca / Misumi CA, cut to length", "Frame", 0.50),
 (2, "Cross rail, 2040 x 320 mm (rear, front)", B, 2, 2, 11.5, "same", "Frame", 0.32),
 (3, "Deck rail, 2040 x 320 mm (pair under cartridge)", B, 2, 2, 11.5, "same", "Frame", 0.32),
 (4, "Upright, 2040 x 400 mm", B, 2, 2, 14.5, "same", "Frame", 0.40),
 (5, "Top cross-bar, 2040 x 240 mm", B, 1, 1, 8.5, "same", "Frame", 0.24),
 (6, "Corner bracket for 2040 (L, with screws)", B, 20, 20, 0.8, "Amazon.ca, pack of 20 about 16", "Frame hardware", 0.015),
 (7, "M5 drop-in T-nut", B, 50, 60, 0.14, "Amazon.ca, pack of 100 about 14", "Frame hardware", 0.004),
 (8, "M5 screw kit (8/12/16/20 mm) + M4 nuts/bolts + washers", B, 1, 1, 18.0, "Amazon.ca / Princess Auto", "Frame hardware", 0.25),
 (9, "Guide arm, 5 mm aluminium plate 100 x 180, 60 mm hole", B, 1, 1, 30.0, "local metal shop (estimate)", "Aluminium sheet", 0.20),
 (10, "Blast plate, 2 mm aluminium 240 x 300", B, 1, 1, 25.0, "local metal shop (estimate)", "Aluminium sheet", 0.45),
 (11, "Vent shield, aluminium flashing 0.8 mm", B, 1, 1, 10.0, "Home Depot / RONA (estimate)", "Aluminium sheet", 0.10),
 (12, "Stake tab, 3 mm Al flat bar 25 x 60, 10 mm hole", B, 4, 4, 3.0, "local metal shop (estimate)", "Aluminium sheet", 0.012),
 (13, "Ground stake, 300 mm steel", B, 4, 4, 3.0, "Canadian Tire / RONA (estimate)", "Hold-down", 0.15),
 (14, "Ballast bag (empty canvas / dry bag, filled on site)", B, 2, 2, 7.5, "Amazon.ca (estimate)", "Hold-down", 0.10),
 (15, "Nomex blanket for the electronics (about 30 x 30 cm)", B, 1, 1, 30.0, "Amazon.ca (estimate)", "Hold-down", 0.10),
 (16, "Load cell, 5 kg straight bar (TAL220 type)", B, 1, 1, 14.0, "Amazon.ca / RobotShop CA (estimate)", "Load cells", 0.05),
 (17, "Load cell, 50 kg straight bar", B, 1, 1, 30.0, "Amazon.ca / AliExpress (estimate)", "Load cells", 0.10),
 (18, "Load cell, 200 kg S-type (M12)", B, 0, 1, 55.0, "Amazon.ca (estimate)", "Load cells", 0.70),
 (19, "GX12 4-pin plug + socket pair", B, 2, 3, 4.0, "Amazon.ca, pack of 5 about 15", "Cartridge hardware", 0.02),
 (20, "Cartridge fasteners (M5 x 16/20 bolts, M5 fender washers, M12 bolt)", B, 1, 1, 20.0, "Princess Auto / Amazon.ca", "Cartridge hardware", 0.20),
 (21, "Base plate, bar cell (cartridge.py plate_bar)", P, 2, 2, 1.3, "own filament", "Printed", 0.051),
 (22, "Top platform, bar cell (platform_bar)", P, 2, 2, 0.6, "own filament", "Printed", 0.022),
 (23, "Base plate, S-type (plate_s)", P, 0, 1, 1.0, "own filament", "Printed", 0.040),
 (24, "Top platform, S-type (platform_s)", P, 0, 1, 0.6, "own filament", "Printed", 0.024),
 (25, "Motor cup 18 mm (cup.py)", P, 2, 2, 1.25, "own filament", "Printed", 0.050),
 (26, "Motor cup 24 mm", P, 2, 2, 1.2, "own filament", "Printed", 0.047),
 (27, "Motor cup 29 mm", P, 2, 2, 1.15, "own filament", "Printed", 0.046),
 (28, "Motor cup 38 mm", P, 0, 2, 1.2, "own filament", "Printed", 0.048),
 (29, "PLA filament, 1 kg spool", B, 1, 1, 25.0, "spool3d.ca (estimate)", "Printed", 0.0),
 (30, "ESP32-S3 N16R8 board (already owned)", B, 1, 1, 0.0, "owned (about 22 on Amazon.ca)", "DAQ", 0.02),
 (31, "ADS1220 24-bit ADC breakout board", B, 1, 1, 35.0, "ProtoCentral / Amazon.ca (estimate)", "DAQ", 0.01),
 (32, "microSD module + 32 GB card", B, 1, 1, 18.0, "RobotShop CA / Amazon.ca (estimate)", "DAQ", 0.01),
 (33, "Enclosure, IP65 plastic box", B, 1, 1, 15.0, "Amazon.ca (estimate)", "DAQ", 0.20),
 (34, "Shielded 4-core cable, 3 m, plus mating plug", B, 1, 1, 12.0, "DigiKey CA / Amazon.ca (estimate)", "DAQ", 0.15),
 (35, "Arm key switch, button, LED, wire, perfboard", B, 1, 1, 15.0, "DigiKey CA / RobotShop CA (estimate)", "DAQ", 0.05),
 (36, "USB power bank (already owned)", B, 1, 1, 0.0, "owned", "DAQ", 0.25),
]
# Future = Recommended + HPR module (rough estimates, not designed in detail)
FUTURE = [
 ("4040 sleeper beam x 500 mm (2)", 2, 27.5), ("4040 spreader x 320 mm", 1, 18.0),
 ("4040 corner brackets (set of 8)", 1, 32.0), ("M8 T-nuts, bolts, washers (kit)", 1, 30.0),
 ("1000 kg column / pancake load cell", 1, 150.0), ("SCF-H adapter plate, 8 mm Al 120 x 120, drilled", 1, 35.0),
]

def total(col):
    return sum(i[col] * i[5] for i in ITEMS)

def group_totals():
    g = OrderedDict()
    for i in ITEMS:
        g[i[7]] = g.get(i[7], 0) + i[4] * i[5]
    return g

def mass(col):
    return sum(i[col] * i[8] for i in ITEMS)

if __name__ == "__main__":
    tmin, trec = total(3), total(4)
    tfut = trec + sum(q * p for _, q, p in FUTURE)
    print("Minimum %.0f  Recommended %.0f  Future %.0f" % (tmin, trec, tfut))
    print("mass min %.1f rec %.1f kg" % (mass(3), mass(4)))
    for k, v in group_totals().items():
        print("%-20s %6.1f  %4.1f%%" % (k, v, 100 * v / trec))
