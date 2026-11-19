"""Draws assembly-callouts.png: elevation + plan, every part numbered, legend with qty, CAD, source.
ORANGE = PRINTED, NAVY = PURCHASED.  Grey = not part of the kit (motor, ground).  Numbers match bom.py.
Run: python3 drawing.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from bom import ITEMS, total, reduced

HERE = os.path.dirname(os.path.abspath(__file__))
OR, NV, GR, INK = "#E8821A", "#1F3A5F", "#C9CED4", "#222222"
fig = plt.figure(figsize=(26, 14), dpi=100)
ax = fig.add_axes([0.005, 0.30, 0.64, 0.68]); pl = fig.add_axes([0.005, 0.01, 0.64, 0.29]); lg = fig.add_axes([0.655, 0.01, 0.34, 0.98])
for a in (ax, pl):
    a.set_aspect("equal"); a.axis("off")
ax.set_xlim(-330, 560); ax.set_ylim(-30, 440)
pl.set_xlim(-330, 560); pl.set_ylim(-110, 345)

def R(a, x0, y0, x1, y1, c, al=1.0, ec="black", lw=0.6, hatch=None, z=2):
    a.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec=ec, lw=lw, alpha=al, hatch=hatch, zorder=z))

def bub(a, n, px, py, bx, by):
    a.plot([px, bx], [py, by], color=INK, lw=0.7, zorder=8)
    a.plot([px], [py], "o", color=INK, ms=2.5, zorder=9)
    a.add_patch(Circle((bx, by), 13, fc="white", ec=INK, lw=1.0, zorder=10))
    a.text(bx, by, str(n), ha="center", va="center", fontsize=8, weight="bold", zorder=11, color=INK)

def T(a, x, y, s, fs=9, **k):
    k.setdefault("color", INK); a.text(x, y, s, fontsize=fs, zorder=12, **k)

# ---------------- ELEVATION: front view, cut through the centre line ----------------
BT = 18.0                      # base top
CX = 130.0
T(ax, -325, 428, "ELEVATION  (looking along the frame, cut through the motor axis; the rear ring bar is seen beyond the cut)", 11, weight="bold")
ax.plot([-390, 750], [0, 0], color="#555", lw=1.4, zorder=1)
T(ax, -325, 6, "ground (grass / gravel)", 8, color="#555")
R(ax, 0, 0, 260, BT, NV)                                                   # base (1)
R(ax, CX - 14, 0, CX + 14, 13, "white", z=3, hatch="///")                 # counterbore under the base
R(ax, 30, BT, 48, BT + 280, NV); R(ax, 212, BT, 230, BT + 280, NV)        # panels (1)
R(ax, 48, BT + 105, 212, BT + 145, NV, 0.28)                                # rear bar beyond the cut (1)
for x in (48, 202):
    R(ax, x, BT, x + 10, BT + 10, NV, 0.9, z=4)                             # inner braces (3)
for x in (20, 230):
    R(ax, x, BT, x + 10, BT + 10, NV, 0.9, z=4)                             # outer braces (3)
for z in (BT + 110, BT + 130):
    ax.plot([39, 39], [z, z], "o", color="white", ms=2.5, mec=NV, zorder=5); ax.plot([221, 221], [z, z], "o", color="white", ms=2.5, mec=NV, zorder=5)
# cell, bolts, collar
R(ax, CX - 15, BT, CX + 15, BT + 76, NV)                                    # cell (4)
R(ax, CX - 6, 0, CX + 6, BT + 12, "#6b7a90", z=5)                           # bottom bolt (5)
CZ = BT + 76
coll = [(CX - 23.2, CZ), (CX - 23.2, CZ + 103), (CX + 23.2, CZ + 103), (CX + 23.2, CZ)]
ax.add_patch(Polygon(coll, fc=OR, ec="black", lw=0.6, zorder=3))
R(ax, CX - 20.2, CZ + 18, CX + 20.2, CZ + 103, "#f4efe4", z=4)              # bore
R(ax, CX - 9.75, CZ + 5.5, CX + 9.75, CZ + 18, "#f4efe4", z=4)              # head pocket
R(ax, CX - 9, CZ + 5.5, CX + 9, CZ + 17.5, "#6b7a90", z=5)                  # M12 SHCS (5)
R(ax, CX - 19, CZ + 18, CX + 19, CZ + 20, NV, z=6)                          # aluminium disc (6)
R(ax, CX - 19, CZ + 20, CX + 19, CZ + 20 + 250, GR, z=5, ec="#888")         # motor (not in kit)
T(ax, CX - 17, CZ + 150, "I-class 38 mm motor\n(not in kit)", 7, color="#555", rotation=90, va="center")
# ring: section = two walls + flange, resting on the bars at BT+145
RZ = BT + 130
for x0, x1 in ((CX - 33, CX - 25), (CX + 25, CX + 33)):
    R(ax, x0, RZ, x1, RZ + 20, OR, hatch="///", z=6)
R(ax, CX - 33, RZ + 15, CX + 33, RZ + 20, OR, z=6)
T(ax, 232, BT + 296, "frame top 280 mm above base", 7, color="#555")
ax.annotate("", xy=(262, BT + 280), xytext=(262, BT), arrowprops=dict(arrowstyle="<->", lw=0.8, color="#555")); T(ax, 268, BT + 140, "280", 8, color="#555")
# guys to stakes (guy attached at base corners, drilled hole); drawn shortened
SL, SR = -230, 490
ax.plot([5, SL], [10, 4], color=NV, lw=1.4, zorder=3); ax.plot([255, SR], [10, 4], color=NV, lw=1.4, zorder=3)
for sx in (SL, SR):
    ax.plot([sx, sx + (-14 if sx < 0 else 14)], [4, -26], color=NV, lw=3, zorder=3, solid_capstyle="round")
R(ax, -110, 4, -96, 12, NV, z=4); R(ax, 346, 4, 360, 12, NV, z=4)          # tensioners
T(ax, -325, -26, "guys and stakes drawn shortened: stakes sit about 330 mm out on the diagonals", 8, color="#555")
# cell cable to the DAQ box, which sits 2 m or more away on the ground (decision 005)
ax.plot([145, 175, 230, 330, 440, 548], [40, 24, BT + 3, BT + 3, BT + 3, 40], color=NV, lw=1.2, ls="--", zorder=3)
ax.annotate("", xy=(556, 44), xytext=(540, 38), arrowprops=dict(arrowstyle="->", color=NV))
T(ax, 556, 52, "to DAQ box\n2 m or more away\n(3 m cable)", 7.5, color="#555", ha="right")
# DAQ box inset, top right
R(ax, 360, 330, 520, 420, "white", ec=NV, lw=1.6)
T(ax, 362, 424, "DAQ box (on the ground, not on the frame)", 7.5, color="#555")
R(ax, 370, 345, 415, 395, NV, z=4); R(ax, 425, 372, 465, 395, NV, z=4); R(ax, 425, 345, 465, 365, NV, z=4); R(ax, 473, 345, 510, 395, NV, z=4)
bub(ax, 10, 392, 370, 385, 312); bub(ax, 11, 445, 383, 430, 312); bub(ax, 13, 445, 355, 475, 312); bub(ax, 14, 491, 370, 520, 312)

# callouts: ordered top to bottom so leaders do not cross
bub(ax, 1, 39, BT + 235, -250, 390)       # side panel
bub(ax, 2, 39, BT + 130, -250, 330)       # screws
bub(ax, 3, 24, BT + 5, -250, 270)         # braces
bub(ax, 1, 10, 9, -250, 210)              # base
bub(ax, 7, -150, 7, -150, 70); bub(ax, 8, -103, 12, -103, 120); bub(ax, 9, SL, -8, SL, 70)
bub(ax, 7, 420, 7, 420, 70); bub(ax, 8, 353, 12, 353, 120); bub(ax, 9, SR, -8, SR, 70)
RX = 300
bub(ax, 19, CX + 33, RZ + 18, RX, 300)    # ring
bub(ax, 18, CX + 23, CZ + 60, RX, 258)    # collar 38
bub(ax, 1, 205, BT + 125, RX, 216)        # ring bar
bub(ax, 6, CX + 19, CZ + 19, RX, 174)     # disc
bub(ax, 5, CX + 9, CZ + 10, RX, 132)      # SHCS
bub(ax, 4, CX + 15, BT + 30, RX, 90)      # cell
bub(ax, 5, CX + 6, 4, RX, 48)             # bottom bolt
bub(ax, 12, 440, BT + 3, 440, 180)        # cable

# ---------------- PLAN ----------------
T(pl, -325, 330, "PLAN  (looking down; base 260 x 220 mm, grain along the 260 mm side)", 11, weight="bold")
R(pl, 0, 0, 260, 220, NV, 0.18)                                            # base (1)
R(pl, 30, 0, 48, 220, NV, 0.9); R(pl, 212, 0, 230, 220, NV, 0.9)           # panels (1)
for yb in (65, 155):
    R(pl, 48, yb - 9, 212, yb + 9, NV, 0.6)                                # ring bars (1)
R(pl, CX - 33, 52, CX + 33, 168, OR, 0.9, z=4)                              # ring flange (19)
pl.add_patch(Circle((CX, 110), 25, fc="white", ec="black", lw=0.6, zorder=5))
R(pl, CX - 15, 85, CX + 15, 135, NV, 0.25, ec="black", lw=0.6, hatch="..", z=3)   # cell footprint below (4)
pl.add_patch(Circle((CX, 110), 23.2, fc=OR, ec="black", lw=0.8, zorder=6)); pl.add_patch(Circle((CX, 110), 20.2, fc="#f4efe4", ec="black", lw=0.5, zorder=7))
pl.add_patch(Circle((CX, 110), 19, fc=GR, ec="#888", lw=0.5, zorder=8))
for xx in (CX - 12, CX + 12):
    for yy in (65, 155):
        pl.plot([xx], [yy], "o", color="white", ms=3, mec=OR, zorder=9)
for x in (18, 49, 212, 232):
    for y in (55, 165):
        R(pl, x, y - 10, x + 10, y + 10, NV, z=4)                           # braces (3), 8 in total
for (x, y, sx, sy) in ((15, 15, -1, -1), (245, 15, 1, -1), (15, 205, -1, 1), (245, 205, 1, 1)):
    ex, ey = x + sx * 110, y + sy * 110
    pl.plot([x, ex], [y, ey], color=NV, lw=1.2, zorder=3)
    pl.add_patch(Circle((x, y), 4, fc="white", ec=NV, lw=1, zorder=5))
    R(pl, ex - 4, ey - 4, ex + 4, ey + 4, NV, z=4)
T(pl, 330, -100, "guys shortened in the drawing", 8, color="#555", ha="right")
bub(pl, 1, 5, 110, -250, 220); bub(pl, 3, 22, 55, -250, 160); bub(pl, 2, 39, 20, -250, 100)
bub(pl, 19, CX + 33, 160, 330, 235); bub(pl, 18, CX + 21, 100, 330, 170); bub(pl, 4, CX + 14, 120, 330, 110)
bub(pl, 1, 120, 65, 330, 50)
bub(pl, 7, 100, 100, -120, 20) if False else None
bub(pl, 7, 245 + 55, 15 - 55, 380, -50); bub(pl, 9, 245 + 110, 15 - 110, 440, -50); bub(pl, 8, 245 + 80, 15 - 80, 410, -20) if False else None
bub(pl, 8, 245 + 130, 15 - 130, 440, -5) if False else None

# ---------------- LEGEND ----------------
lg.axis("off"); lg.set_xlim(0, 1); lg.set_ylim(0, 1)
lg.text(0.01, 0.985, "Stand v3 parts  (CAD, before tax, estimates)", fontsize=12, weight="bold", va="top")
lg.add_patch(Rectangle((0.01, 0.945), 0.03, 0.014, fc=OR, ec="black")); lg.text(0.05, 0.952, "PRINTED (filament only)", fontsize=9, va="center")
lg.add_patch(Rectangle((0.5, 0.945), 0.03, 0.014, fc=NV, ec="black")); lg.text(0.54, 0.952, "PURCHASED", fontsize=9, va="center")
y = 0.925
lg.text(0.01, y, "No", fontsize=8, weight="bold"); lg.text(0.06, y, "Part", fontsize=8, weight="bold"); lg.text(0.60, y, "Qty", fontsize=8, weight="bold")
lg.text(0.66, y, "CAD", fontsize=8, weight="bold"); lg.text(0.74, y, "Source", fontsize=8, weight="bold")
y -= 0.017
import textwrap
for (n, name, kind, q, u, src, grp) in ITEMS:
    col = OR if kind == "PRINTED" else NV
    lines = textwrap.wrap(name, 34)
    srcl = textwrap.wrap(src.split("(")[0].strip(), 22)
    h = max(len(lines), len(srcl)) * 0.0155 + 0.005
    lg.add_patch(Rectangle((0.01, y - 0.012), 0.035, 0.014, fc=col, ec="black"))
    lg.text(0.027, y - 0.005, str(n), fontsize=7.5, color="white", weight="bold", ha="center", va="center")
    lg.text(0.06, y, "\n".join(lines), fontsize=7.5, va="top", linespacing=1.15)
    lg.text(0.60, y, str(q), fontsize=7.5, va="top"); lg.text(0.66, y, "%.2f" % (q * u), fontsize=7.5, va="top")
    lg.text(0.74, y, "\n".join(srcl), fontsize=6.8, va="top", linespacing=1.15)
    y -= h
y -= 0.012
lg.plot([0.01, 0.99], [y + 0.006, y + 0.006], color="black", lw=0.8)
lg.text(0.01, y - 0.01, "Recommended total  CAD %.2f" % total(), fontsize=9.5, weight="bold", va="top")
lg.text(0.01, y - 0.034, "Reduced (see costing.md)  CAD %.2f" % reduced(), fontsize=9.5, weight="bold", va="top")
lg.text(0.01, y - 0.058, "Plywood parts, all from item 1: base 260x220, 2 panels 220x280,\n2 ring bars 40x164. Ring (19) sits on the bars, never touches the\nmotor in normal use. Only the cell (4) is on the thrust path.", fontsize=7.5, va="top", color="#444")
fig.savefig(os.path.join(HERE, "assembly-callouts.png"), dpi=100)
print("wrote assembly-callouts.png")
