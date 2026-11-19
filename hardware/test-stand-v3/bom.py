"""Stand v3 bill of materials (CAD, before ~15% Quebec tax).  ALL PRICES ARE ESTIMATES: confirm at order time.
Used by drawing.py, test_stand_v3.py and costing.md.  Run: python3 bom.py"""
P, B = "PURCHASED", "PRINTED"
# (no, name, kind, qty, unit CAD, source, group)
ITEMS = [
    (1, "Plywood 18 mm (3/4 in), 2 x 4 ft panel (half is used)", P, 1, 32.00, "Home Depot / RONA / Canadian Tire (fir; birch about 45)", "plywood"),
    (2, "Wood screws #8 and #6, assorted box (about 100)", P, 1, 7.00, "Canadian Tire / Home Depot", "plywood"),
    (3, "Steel corner brace 2 in, pack of 4 (8 used)", P, 2, 4.50, "Home Depot / Canadian Tire", "plywood"),
    (4, "S-type load cell 100 kg, M12 thread", P, 1, 38.00, "Amazon.ca (CZL301 type)", "cell"),
    (5, "M12 hardware: SHCS 30 mm, hex bolt 45 mm, 2 fender washers", P, 1, 8.00, "Princess Auto / Home Depot", "cell"),
    (6, "Aluminium disc 2 mm (cut from flashing or a baking tray)", P, 1, 3.00, "Home Depot / Dollarama", "cell"),
    (7, "Guy rope, 4 mm polyester, 12 m", P, 1, 7.00, "Canadian Tire", "holddown"),
    (8, "Rope tensioner (tent type)", P, 4, 1.00, "Canadian Tire / MEC", "holddown"),
    (9, "Ground stake 300 mm, steel", P, 4, 2.50, "Canadian Tire / RONA", "holddown"),
    (10, "ADS1220 24-bit ADC breakout", P, 1, 35.00, "ProtoCentral / Amazon.ca", "daq"),
    (11, "microSD module + 32 GB card", P, 1, 16.00, "Amazon.ca / RobotShop CA", "daq"),
    (12, "Cell extension: 3 m shielded 4-core cable + GX12 4-pin pair", P, 1, 10.00, "Amazon.ca / DigiKey CA", "daq"),
    (13, "Button, LED, resistors, perfboard, wire, capacitors, box", P, 1, 8.00, "RobotShop CA / DigiKey CA", "daq"),
    (14, "ESP32-S3 board (already owned)", P, 1, 0.00, "owned", "daq"),
    # printed: filament only at CAD 25 per kg of PLA, grams from collar.py
    (15, "Collar 18 mm (collar.py)", B, 1, 0.30, "own filament, LIBRARY", "printed"),
    (16, "Collar 24 mm", B, 1, 0.50, "own filament, LIBRARY", "printed"),
    (17, "Collar 29 mm", B, 1, 0.70, "own filament, LIBRARY", "printed"),
    (18, "Collar 38 mm", B, 1, 1.10, "own filament, LIBRARY", "printed"),
    (19, "Guide ring (ring.stl)", B, 1, 0.95, "own filament, LIBRARY", "printed"),
    (20, "Spare collars (one more each of 29 and 38)", B, 1, 1.80, "own filament, LIBRARY / LAB", "printed"),
]
# plywood parts are listed under item 1 (cut list in README)

def total(items=ITEMS):
    return sum(q * u for (_, _, _, q, u, _, _) in items)

def by_group(items=ITEMS):
    g = {}
    for (_, _, _, q, u, _, grp) in items:
        g[grp] = g.get(grp, 0) + q * u
    return g

if __name__ == "__main__":
    for it in ITEMS:
        print("%2d %-62s %-9s %2d x %6.2f = %6.2f" % (it[0], it[1], it[2], it[3], it[4], it[3] * it[4]))
    print("TOTAL %.2f" % total())
    print({k: round(v, 2) for k, v in by_group().items()})


# Reductions taken in costing.md: (driver item no., what, saving CAD, sure?)  sure=False depends on the owner
REDUCTIONS = [
    (4, "Cell from a direct-import seller (38 to 20)", 18.0, True),
    (1, "Plywood from a wood-shop offcut bin or store remnant (free)", 32.0, False),
    (11, "Use a spare microSD card the owner already has", 10.0, False),
    (12, "Cable: alarm cable + soldered inline JST instead of GX12 pair", 4.0, True),
    (9, "Landscape spikes 10 in (1.50) instead of 300 mm stakes (2.50)", 4.0, True),
    (8, "Taut-line hitch instead of tent tensioners", 4.0, True),
    (13, "Take button, LED, wire, box from the owner's bin", 3.0, True),
]

def reduced(sure_only=False, items=ITEMS):
    return total(items) - sum(s for (_, _, s, ok) in [(a, b, c, d) for (a, b, c, d) in REDUCTIONS] if (ok or not sure_only))
