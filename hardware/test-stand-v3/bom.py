"""Stand v3 bill of materials, 2020 EXTRUSION version (CAD, before ~15% Quebec tax).
ALL PRICES ARE ESTIMATES: confirm at order time.  Used by drawing.py, test_stand_v3.py and costing.md.
Run: python3 bom.py"""
P, B = "PURCHASED", "PRINTED"
# (no, name, kind, qty, unit CAD, source, group)
ITEMS = [
    (1, "VEVOR 2020 T-slot extrusion, black, 10 x 1000 mm pack (4 used here; 6 kept for swing rig and gimbal fixture)", P, 1, 67.99, "Amazon.ca B0F47L334H, seen 19 Nov 2026, in stock", "frame"),
    (2, "Inside-corner bracket kit, steel, 2020 (bracket + 2 M5 screws + 2 T-nuts each)", P, 24, 1.30, "Amazon.ca / AliExpress CA", "frame"),
    (3, "M5 drop-in T-nuts, pack of 20 (16 used: plate 8, guys 8)", P, 1, 4.00, "Amazon.ca", "frame"),
    (4, "M5 x 10 button-head screws, pack of 20 (16 used)", P, 1, 3.00, "Amazon.ca / Princess Auto", "frame"),
    (5, "Aluminium plate 3.2 mm (1/8 in) 6061-T6, 160 x 160 blank, owner cuts the corners", P, 1, 18.00, "Metal Supermarkets / Princess Auto", "frame"),
    (6, "Stainless pad eye (eye plate), 2 holes, M5 screws (guy anchor)", P, 4, 2.50, "Canadian Tire / marine store", "holddown"),
    (7, "M3 x 10 screws + M3 drop-in T-nuts (4 each) for the ring", P, 1, 4.00, "Amazon.ca", "frame"),
    (8, "S-type load cell 100 kg, M12 thread", P, 1, 38.00, "Amazon.ca (CZL301 type)", "cell"),
    (9, "M12 hardware: SHCS 30 mm, hex bolt 25 mm, 2 fender washers", P, 1, 8.00, "Princess Auto / Home Depot", "cell"),
    (10, "Aluminium disc 2 mm (cut from flashing or a baking tray)", P, 1, 3.00, "Home Depot / Dollarama", "cell"),
    (11, "Guy rope, 4 mm polyester, 12 m", P, 1, 7.00, "Canadian Tire", "holddown"),
    (12, "Rope tensioner (tent type)", P, 4, 1.00, "Canadian Tire / MEC", "holddown"),
    (13, "Ground stake 300 mm, steel", P, 4, 2.50, "Canadian Tire / RONA", "holddown"),
    (14, "ADS1220 24-bit ADC breakout", P, 1, 35.00, "ProtoCentral / Amazon.ca", "daq"),
    (15, "microSD module + 32 GB card", P, 1, 16.00, "Amazon.ca / RobotShop CA", "daq"),
    (16, "Cell extension: 3 m shielded 4-core cable + GX12 4-pin pair", P, 1, 10.00, "Amazon.ca / DigiKey CA", "daq"),
    (17, "Button, LED, resistors, perfboard, wire, capacitors, box", P, 1, 8.00, "RobotShop CA / DigiKey CA", "daq"),
    (18, "ESP32-S3 board (already owned)", P, 1, 0.00, "owned", "daq"),
    # printed: filament only at CAD 25 per kg of PLA, grams from collar.py
    (19, "Collar 18 mm (collar.py)", B, 1, 0.30, "own filament, LIBRARY", "printed"),
    (20, "Collar 24 mm", B, 1, 0.50, "own filament, LIBRARY", "printed"),
    (21, "Collar 29 mm", B, 1, 0.70, "own filament, LIBRARY", "printed"),
    (22, "Collar 38 mm", B, 1, 1.10, "own filament, LIBRARY", "printed"),
    (23, "Guide ring (ring.stl)", B, 1, 0.95, "own filament, LIBRARY", "printed"),
    (24, "Spare collars (one more each of 29 and 38)", B, 1, 1.80, "own filament, LIBRARY / LAB", "printed"),
]
STRUCTURE = (1, 2, 3, 4, 5, 6, 7)       # item numbers that are the extrusion structure (for the plywood comparison)
PLYWOOD_STRUCTURE = 48.00               # old plywood tower: panel 32 + screws 7 + 8 braces 9 (v3 plywood version)
PLYWOOD_TOTAL = 192.35                  # old whole-stand total, plywood version
PLYWOOD_REDUCED = 117.35                # old reduced total (needed free plywood and a spare card)
PLYWOOD_SURE_ONLY = 159.35

# Printed-bracket alternative (bracket.py): filament only, M5 hardware bought in 100-packs instead of kit hardware
PLA_CAD_PER_KG = 25.0
BRACKET_G = 5.2                         # grams per bracket, solid (bracket.py prints the real value)
PRINTED_ALT = {"brackets": 24 * BRACKET_G / 1000 * PLA_CAD_PER_KG,   # about 3.1
               "tnut_pack100": 13.00, "screw_pack100": 9.00}


def total(items=ITEMS):
    return sum(q * u for (_, _, _, q, u, _, _) in items)

def by_group(items=ITEMS):
    g = {}
    for (_, _, _, q, u, _, grp) in items:
        g[grp] = g.get(grp, 0) + q * u
    return g

def structure_cost(items=ITEMS):
    return sum(q * u for (n, _, _, q, u, _, _) in items if n in STRUCTURE)

def printed_bracket_saving():
    """Steel kits (item 2) and the small packs (items 3, 4) are replaced by 24 printed brackets + two 100-packs."""
    steel = 24 * 1.30 + 4.00 + 3.00
    printed = PRINTED_ALT["brackets"] + PRINTED_ALT["tnut_pack100"] + PRINTED_ALT["screw_pack100"]
    return steel - printed

# Reductions taken in costing.md: (driver item no., what, saving CAD, sure?)  sure=False depends on the owner
REDUCTIONS = [
    (8, "Cell from a direct-import seller (38 to 20)", 18.0, True),
    (1, "2020 from a direct-import seller or a salvage bin (16 to 9 per metre)", 28.0, True),
    (2, "Printed PLA brackets (bracket.py, LAB, one plate) + 100-pack T-nuts and screws", None, True),
    (16, "Cable: alarm cable + soldered inline JST instead of GX12 pair", 4.0, True),
    (13, "Landscape spikes 10 in (1.50) instead of 300 mm stakes (2.50)", 4.0, True),
    (12, "Taut-line hitch instead of tent tensioners", 4.0, True),
    (17, "Take button, LED, wire, box from the owner's bin", 3.0, True),
    (15, "Use a spare microSD card the owner already has", 10.0, False),
    (5, "Plate from a makerspace offcut of 3 mm 6061 (check the alloy)", 18.0, False),
]

def _saving(s):
    return printed_bracket_saving() if s is None else s

def reduced(sure_only=False, items=ITEMS):
    return total(items) - sum(_saving(s) for (_, _, s, ok) in REDUCTIONS if (ok or not sure_only))


if __name__ == "__main__":
    for it in ITEMS:
        print("%2d %-80s %-9s %2d x %6.2f = %7.2f" % (it[0], it[1], it[2], it[3], it[4], it[3] * it[4]))
    print("TOTAL %.2f   structure %.2f   printed-bracket saving %.2f" % (total(), structure_cost(), printed_bracket_saving()))
    print({k: round(v, 2) for k, v in by_group().items()})
    print("reduced %.2f   sure-only %.2f" % (reduced(), reduced(sure_only=True)))
