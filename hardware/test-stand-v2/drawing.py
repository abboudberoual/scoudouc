"""Draws assembly-callouts.png: elevation, plan, cartridge and cup details, every part numbered, with a legend.
Orange = PRINTED, navy = PURCHASED structure, grey = PURCHASED small parts / electronics.  Run: python3 drawing.py
Numbers match bom.py (and the parts tables in README.md)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
from bom import ITEMS

HERE = os.path.dirname(os.path.abspath(__file__))
OR, NV, GR = "#E8821A", "#1F3A5F", "#8C97A3"
INK = "#222222"
fig = plt.figure(figsize=(27, 14), dpi=100)
ax = fig.add_axes([0.005, 0.01, 0.635, 0.98])
lg = fig.add_axes([0.645, 0.01, 0.35, 0.98])
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-90, 1590); ax.set_ylim(-110, 1130)

def R(x0, y0, x1, y1, c, a=1.0, ec="black", lw=0.6, hatch=None, z=2):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec=ec, lw=lw, alpha=a, hatch=hatch, zorder=z))

def bub(n, x, y, tx=None, ty=None, c="white"):
    if tx is not None:
        ax.plot([x, tx], [y, ty], color=INK, lw=0.7, zorder=8)
        ax.plot([x], [y], "o", color=INK, ms=2.5, zorder=9)
        x, y = tx, ty
    ax.add_patch(Circle((x, y), 14, fc=c, ec=INK, lw=1.0, zorder=10))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, weight="bold", zorder=11, color=INK)

def T(x, y, s, fs=10, **k):
    k.setdefault("color", INK)
    ax.text(x, y, s, fontsize=fs, zorder=12, **k)

# ---------------- ELEVATION (section through the centre line) ----------------
ZE = 640     # ground level of the elevation
AX = 140     # cup axis X
T(-80, ZE + 480, "ELEVATION  (side view, centre-line cut, near rail and near upright removed)", 12, weight="bold")
ax.plot([-60, 800], [ZE, ZE], color="#555", lw=1.5, zorder=1)
R(0, ZE, 500, ZE + 20, NV, 0.22)                                     # far long rail
R(0, ZE, 40, ZE + 20, NV, hatch="///"); R(460, ZE, 500, ZE + 20, NV, hatch="///")   # cross rails cut
R(100, ZE, 140, ZE + 20, NV, hatch="///"); R(140, ZE, 180, ZE + 20, NV, hatch="///")  # deck rails cut
R(0, ZE + 20, 40, ZE + 420, NV, 0.55)                               # far upright
R(0, ZE + 111, 40, ZE + 131, NV)                                    # cross-bar
R(0, ZE + 131, 110, ZE + 136, NV, 0.8); R(170, ZE + 131, 185, ZE + 136, NV, 0.8)   # arm with ring hole
R(50, ZE + 20, 108, ZE + 22, NV, 0.8); R(172, ZE + 20, 290, ZE + 22, NV, 0.8)      # blast plate
R(205, ZE + 22, 207, ZE + 150, GR)                                   # vent shield
# S cartridge
R(110, ZE + 20, 170, ZE + 28, OR); R(122, ZE + 28, 158, ZE + 36, OR)
R(124, ZE + 36, 156, ZE + 96, NV); R(112, ZE + 96, 168, ZE + 108, OR)
R(136, ZE + 14, 144, ZE + 100, GR, 0.9, z=3)                        # M12 bolt
R(120, ZE + 20, 124, ZE + 25, GR); R(156, ZE + 20, 160, ZE + 25, GR)  # M5 heads
# cup 38
ZC = ZE + 108
R(112, ZC, 168, ZC + 8, OR)
cup = [(AX - 23.2, ZC + 8), (AX - 23.2, ZC + 23 - 3.8), (AX - 27, ZC + 23), (AX - 27, ZC + 29), (AX - 23.2, ZC + 32.8),
       (AX - 23.2, ZC + 93), (AX + 23.2, ZC + 93), (AX + 23.2, ZC + 32.8), (AX + 27, ZC + 29), (AX + 27, ZC + 23), (AX + 23.2, ZC + 19.2), (AX + 23.2, ZC + 8)]
ax.add_patch(Polygon(cup, fc=OR, ec="black", lw=0.6, zorder=3))
R(AX - 20.2, ZC + 8, AX + 20.2, ZC + 93, "#f4efe4", z=4)            # bore
R(AX - 19, ZC + 8, AX + 19, ZC + 278, "#BDBDBD", z=5)               # motor (I class, 270 mm)
T(AX + 28, ZC + 200, "motor\n(not part of kit)", 8, va="center", color="#444")
ax.annotate("", xy=(AX, ZC + 345), xytext=(AX, ZC + 290), arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5))
T(AX + 8, ZC + 330, "exhaust UP", 8, color="#C0392B")
ax.annotate("", xy=(AX - 55, ZC + 150), xytext=(AX - 55, ZC + 210), arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5), zorder=12)
T(AX - 122, ZC + 175, "thrust\nload path\nDOWN", 8, color="#C0392B")
# ballast, stake, DAQ
R(300, ZE + 20, 380, ZE + 65, GR, 0.8); R(390, ZE + 20, 470, ZE + 60, GR, 0.8)
ax.plot([500, 548], [ZE + 12, ZE - 55], color=NV, lw=3, zorder=3)
R(486, ZE + 20, 514, ZE + 24, NV)                                    # stake tab
R(570, ZE, 700, ZE + 70, GR, 0.55); R(572, ZE + 2, 698, ZE + 68, "none", hatch="xx", ec="#a05", lw=0.4)  # box + Nomex
R(715, ZE, 765, ZE + 80, GR, 0.8)                                    # power bank
ax.plot([142, 142, 560], [ZE + 24, ZE + 6, ZE + 6], color="black", lw=1.2, ls="--", zorder=3)   # cell cable
T(250, ZE + 12, "cell cable 3 m", 8, ha="left")
T(40, ZE - 28, "rear cross rail", 8); T(250, ZE - 28, "front cross rail", 8)
for n, p, t in [(1, (350, ZE + 10), (350, ZE + 75)), (2, (20, ZE + 10), (-30, ZE + 60)), (3, (120, ZE + 10), (60, ZE - 45)),
                (4, (20, ZE + 300), (-35, ZE + 300)), (5, (20, ZE + 121), (-35, ZE + 150)), (9, (60, ZE + 133), (60, ZE + 185)),
                (10, (80, ZE + 21), (80, ZE + 70)), (11, (206, ZE + 120), (250, ZE + 190)), (23, (115, ZE + 24), (60, ZE + 24 + 0)),
                (18, (140, ZE + 70), (200, ZE + 70)), (24, (165, ZE + 102), (225, ZE + 102)), (28, (AX + 23, ZC + 50), (230, ZC + 30)),
                (20, (140, ZE + 40), (110, ZE + 70)), (13, (540, ZE - 40), (580, ZE - 40)), (12, (500, ZE + 22), (440, ZE + 100)),
                (14, (340, ZE + 50), (340, ZE + 110)), (15, (640, ZE + 66), (640, ZE + 120)), (33, (690, ZE + 20), (690, ZE + 160)),
                (36, (740, ZE + 70), (740, ZE + 130)), (34, (400, ZE + 6), (400, ZE + 40)), (7, (160, ZE + 8), (200, ZE - 45)),
                (6, (40, ZE + 21), (-35, ZE + 215))]:
    bub(n, p[0], p[1], t[0], t[1])
bub(19, 110, ZE + 15, 70, ZE + 130, c="white")

# ---------------- PLAN ----------------
PY = 60
T(-80, PY + 450, "PLAN  (looking down; cup axis marked +)", 12, weight="bold")
def PR(x0, y0, x1, y1, c, a=1.0, **k):
    R(x0, PY + y0, x1, PY + y1, c, a, **k)
PR(0, 0, 500, 40, NV, 0.9); PR(0, 360, 500, 400, NV, 0.9)           # long rails
PR(0, 40, 40, 360, NV, 0.9); PR(460, 40, 500, 360, NV, 0.9)         # cross rails
PR(100, 40, 140, 360, NV, 0.9); PR(140, 40, 180, 360, NV, 0.9)      # deck rails
PR(50, 50, 290, 350, GR, 0.35, ec="#555")                            # blast plate
PR(0, 60, 40, 80, "#0f2038"); PR(0, 320, 40, 340, "#0f2038")        # uprights
PR(0, 80, 40, 320, NV, 0.55, ec="white")                             # top cross-bar
PR(0, 150, 185, 250, NV, 0.5, ec="black"); ax.add_patch(Circle((AX, PY + 200), 30, fc="white", ec="black", lw=0.8, zorder=4))
PR(110, 150, 170, 250, OR, 0.95, z=5)                                # cartridge base plate
PR(AX - 28, 172, AX + 28, 228, OR, 0.95, z=6)                        # platform / cup flange
ax.add_patch(Circle((AX, PY + 200), 27, fc=OR, ec="black", lw=0.8, zorder=7))
ax.add_patch(Circle((AX, PY + 200), 20.2, fc="#f4efe4", ec="black", lw=0.6, zorder=8))
ax.plot([AX - 8, AX + 8], [PY + 200, PY + 200], color="black", lw=0.8, zorder=9); ax.plot([AX, AX], [PY + 192, PY + 208], color="black", lw=0.8, zorder=9)
PR(205, 150, 208, 250, GR, 1.0)                                     # vent shield
for (x, y) in [(10, 10), (490, 10), (10, 390), (490, 390)]:
    PR(x - 14, y - 14, x + 14, y + 14, NV, 1.0, z=6)
    sx, sy = (-1 if x < 250 else 1), (-1 if y < 200 else 1)
    ax.add_patch(Circle((x + sx * 40, PY + y + sy * 40), 7, fc=NV, ec="black", lw=0.6, zorder=6))
PR(300, 50, 380, 160, GR, 0.8); PR(300, 240, 380, 350, GR, 0.8)    # ballast
PR(570, 140, 700, 260, GR, 0.55); PR(570, 140, 700, 260, "none", hatch="xx", ec="#a05", lw=0.4)  # DAQ box + Nomex
PR(590, 180, 625, 215, "#B9C2CC", 1.0, z=5); PR(630, 180, 660, 215, "#B9C2CC", 1.0, z=5)       # ESP32 + ADS1220 boards
PR(590, 225, 625, 250, "#B9C2CC", 1.0, z=5); PR(640, 150, 690, 175, "#B9C2CC", 1.0, z=5)       # SD + key switch/LED
PR(715, 150, 800, 215, GR, 0.8)                                      # power bank
ax.plot([AX, AX, 560, 570], [PY + 150, PY + 120, PY + 120, PY + 180], color="black", lw=1.4, ls="--", zorder=7)
for n, p, t in [(1, (250, 20), (250, -35)), (2, (480, 200), (530, 200)), (3, (120, 90), (120, 20)), (4, (20, 70), (-40, 70)),
                (5, (20, 200), (-40, 200)), (9, (80, 180), (80, 120)), (10, (240, 320), (240, 385)), (11, (206, 240), (240, 280)),
                (12, (10, 390), (-45, 425)), (13, (-30, 430), (-65, 385)), (14, (340, 100), (340, 20)), (15, (580, 255), (560, 310)),
                (21, (118, 160), (90, 140)), (22, (AX + 20, 172), (190, 135)), (25, (AX + 20, 220), (190, 270)),
                (31, (645, 195), (645, 130)), (30, (607, 200), (610, 330)), (32, (607, 238), (660, 300)), (35, (665, 162), (720, 120)),
                (33, (700, 200), (720, 270)), (34, (450, 120), (450, 190)), (36, (760, 190), (760, 250))]:
    bub(n, p[0], PY + p[1], t[0], PY + t[1])
T(300, PY + 170, "ballast bags (filled on site)", 8)

# ---------------- CARTRIDGE STACKS ----------------
CY = 640
T(870, CY + 480, "THREE CARTRIDGES (same SCP bottom, same SCF top, same GX12 plug)", 12, weight="bold")
def stack(x, name, plate_t, riser, cell_h, plat_t, cell_n, plate_n, plat_n, cell_label, boss=0):
    R(x - 30, CY, x + 30, CY + plate_t, OR)
    if boss: R(x - 18, CY + plate_t, x + 18, CY + plate_t + boss, OR)
    if riser:
        R(x + 40, CY + plate_t, x + 70, CY + plate_t + riser, OR)
        R(x - 10, CY + plate_t + riser, x + 70, CY + plate_t + riser + cell_h, NV)
        top = CY + plate_t + riser + cell_h
    else:
        R(x - 16, CY + plate_t + boss, x + 16, CY + plate_t + boss + cell_h, NV)
        top = CY + plate_t + boss + cell_h
    R(x - 28, top, x + 28, top + plat_t, OR)
    R(x - 11, CY + 8, x + 11, CY + 36, GR); R(x - 45, CY + 8, x - 30, CY + 36, GR, 0.9)   # GX12 wall + plug
    T(x, CY - 30, name, 10, ha="center", weight="bold"); T(x, CY - 48, cell_label, 8, ha="center")
    bub(cell_n, x + 40 if riser else x + 16, top - cell_h / 2 if not riser else top - 6, x + 100, CY + 140)
    bub(plate_n, x - 30, CY + 4, x - 75, CY + 70)
    bub(plat_n, x + 28, top + plat_t / 2, x + 100, top + 80)
stack(950, "5 kg  (A-E)", 8, 8, 12.7, 10, 16, 21, 22, "bar cell, 80 mm")
stack(1130, "50 kg  (F-H)", 8, 8, 12.7, 10, 17, 21, 22, "bar cell, same shape")
stack(1330, "200 kg  (I)", 8, 0, 60, 12, 18, 23, 24, "S-type, M12", boss=8)
bub(19, 925, CY + 56, 880, CY + 150); bub(20, 1330, CY + 22, 1420, CY + 40)
T(870, CY + 440, "heights above the deck rail: 39 mm / 39 mm / 88 mm", 9)

# ---------------- CUP FAMILY ----------------
KY = 130
T(870, KY + 230, "CUP FAMILY (same 56 mm SCF flange, same 54 mm guide band)", 12, weight="bold")
for i, (d, h, n) in enumerate([(18, 58, 25), (24, 63, 26), (29, 73, 27), (38, 93, 28)]):
    x = 930 + i * 140
    r = (d + 2.4 + 3 * 2) / 2
    R(x - 28, KY, x + 28, KY + 8, OR)
    pts = [(x - r, KY + 8), (x - r, KY + 23 - (27 - r)), (x - 27, KY + 23), (x - 27, KY + 29), (x - r, KY + 29 + (27 - r)),
           (x - r, KY + h), (x + r, KY + h), (x + r, KY + 29 + (27 - r)), (x + 27, KY + 29), (x + 27, KY + 23), (x + r, KY + 23 - (27 - r)), (x + r, KY + 8)]
    ax.add_patch(Polygon(pts, fc=OR, ec="black", lw=0.6, zorder=3))
    R(x - (d + 2.4) / 2, KY + 8, x + (d + 2.4) / 2, KY + h, "#f4efe4", z=4)
    T(x, KY - 22, "%d mm" % d, 10, ha="center", weight="bold")
    bub(n, x + 27, KY + 26, x + 62, KY + 100)

# ---------------- LEGEND ----------------
lg.axis("off"); lg.set_xlim(0, 100); lg.set_ylim(0, 100)
lg.text(0, 99, "PARTS (Recommended C-I build; costs are CAD estimates, before tax)", fontsize=11, weight="bold", va="top")
cols = [0, 4, 52, 62, 67, 74]
heads = ["#", "Part", "Kind", "Qty", "Unit $", "Source"]
y = 96
for c, h in zip(cols, heads):
    lg.text(c, y, h, fontsize=8, weight="bold", va="center")
rowh = 94.0 / (len(ITEMS) + 1)
for it in ITEMS:
    n, name, kind, qmin, qrec, unit, src, grp, kg = it
    y -= rowh
    col = OR if kind == "PRINTED" else (NV if grp in ("Frame", "Aluminium sheet", "Load cells") else GR)
    lg.add_patch(Rectangle((-0.6, y - rowh * 0.4), 2.6, rowh * 0.8, fc=col, ec="none"))
    lg.text(0.7, y, str(n), color="white", fontsize=6.5, ha="center", va="center", weight="bold")
    lg.text(cols[1], y, name[:52], fontsize=6.6, va="center")
    lg.text(cols[2], y, kind, fontsize=6.6, va="center", color=OR if kind == "PRINTED" else NV, weight="bold")
    lg.text(cols[3], y, str(qrec), fontsize=6.6, va="center")
    lg.text(cols[4], y, "%.2f" % unit if unit < 10 else "%.0f" % unit, fontsize=6.6, va="center")
    lg.text(cols[5], y, src.replace("Amazon.ca", "Amzn.ca")[:30], fontsize=5.8, va="center", color="#444")
y -= rowh * 1.2
for i, (c, t) in enumerate([(OR, "PRINTED (PLA)"), (NV, "PURCHASED, structure"), (GR, "PURCHASED, small parts / electronics")]):
    lg.add_patch(Rectangle((i * 33, y - 0.7), 2.4, 1.6, fc=c, ec="none")); lg.text(i * 33 + 3, y, t, fontsize=7.5, va="center")
fig.savefig(os.path.join(HERE, "assembly-callouts.png"))
print("wrote assembly-callouts.png")
