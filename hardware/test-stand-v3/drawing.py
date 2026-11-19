"""Draws assembly-callouts.png (2020 extrusion version): elevation (cut at the motor axis, front half removed) + plan + legend.
ORANGE = PRINTED, NAVY = PURCHASED.  Grey = not part of the kit (motor, ground).  Numbers match bom.py.
Callout bubbles are placed in columns by code and checked so none overlap.   Run: python3 drawing.py"""
import os, sys, math, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from bom import ITEMS, total, reduced

HERE = os.path.dirname(os.path.abspath(__file__))
OR, NV, GR, INK = "#E8821A", "#1F3A5F", "#C9CED4", "#222222"
fig = plt.figure(figsize=(26, 16), dpi=100)
ax = fig.add_axes([0.005, 0.30, 0.64, 0.69]); pl = fig.add_axes([0.005, 0.01, 0.64, 0.28]); lg = fig.add_axes([0.655, 0.01, 0.34, 0.98])
for a in (ax, pl):
    a.set_aspect("equal"); a.axis("off")
ax.set_xlim(-330, 600); ax.set_ylim(-40, 570)
pl.set_xlim(-330, 600); pl.set_ylim(-140, 150)
BUBBLES = {id(ax): [], id(pl): []}

def R(a, x0, y0, x1, y1, c, al=1.0, ec="black", lw=0.6, hatch=None, z=2):
    a.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec=ec, lw=lw, alpha=al, hatch=hatch, zorder=z))

def bub(a, n, px, py, bx, by):
    a.plot([px, bx], [py, by], color=INK, lw=0.7, zorder=8)
    a.plot([px], [py], "o", color=INK, ms=2.5, zorder=9)
    a.add_patch(Circle((bx, by), 12, fc="white", ec=INK, lw=1.0, zorder=10))
    a.text(bx, by, str(n), ha="center", va="center", fontsize=8, weight="bold", zorder=11, color=INK)
    BUBBLES[id(a)].append((n, bx, by))

def T(a, x, y, s, fs=9, **k):
    k.setdefault("color", INK); a.text(x, y, s, fontsize=fs, zorder=12, **k)

def column(a, x, items):
    """items = [(number, point_x, point_y, bubble_y)] ; bubbles stacked at x."""
    for (n, px, py, by) in items:
        bub(a, n, px, py, x, by)

# ---------------- ELEVATION: cut at Y=0, front half removed; looking along +Y ----------------
T(ax, -325, 552, "ELEVATION  (cut through the motor axis, front half removed: you see the back uprights, the back bar and the back short rails)", 11, weight="bold")
ax.plot([-330, 600], [0, 0], color="#555", lw=1.4, zorder=1)
T(ax, -325, 6, "ground (grass / gravel)", 8, color="#555")
ZP = 23.2                      # plate top above ground
CX = 0.0
# bottom frame: long rails cut (squares), back short rail beyond, plate cut, uprights
R(ax, -80, 0, -60, 20, NV); R(ax, 60, 0, 80, 20, NV)                          # long rails in section (1)
R(ax, -60, 0, 60, 20, NV, 0.35)                                                 # back short rail (1)
for xs in (-80, 60):
    R(ax, xs, 20, xs + 20, 503, NV, 0.45)                                       # back uprights (1)
R(ax, -80, 20, 80, ZP, NV, z=4)                                                 # plate (5), cut at the axis
# top frame
R(ax, -80, 503, -60, 523, NV); R(ax, 60, 503, 80, 523, NV)                    # top long rails in section (1)
R(ax, -60, 503, 60, 523, NV, 0.35)                                              # top back short rail (1)
# ring ladder: bar top at 281 above the plate top (I-class mid-height), bar bottom 261, ladder rail 241 to 261 above plate
BT_ = ZP + 281; BB_ = BT_ - 20; LB_ = BB_ - 20
R(ax, -80, LB_, -60, BB_, NV); R(ax, 60, LB_, 80, BB_, NV)                    # ladder rails in section (1)
R(ax, -80, BB_, 80, BT_, NV, 0.45, z=3)                                         # back ring bar (1)
# brackets (2): triangles seen in profile at the back corners, bottom (on top of the rails), top and mid (under the rails)
def tri(a, pts, z=6):
    a.add_patch(Polygon(pts, fc=NV, ec="black", lw=0.5, zorder=z))
for sx in (-1, 1):
    tri(ax, [(sx * 60, 20), (sx * 40, 20), (sx * 60, 40)])                      # bottom bracket 2
    tri(ax, [(sx * 60, 503), (sx * 40, 503), (sx * 60, 483)])                   # top bracket 2
    tri(ax, [(sx * 60, LB_), (sx * 40, LB_), (sx * 60, LB_ - 20)])              # ladder bracket
    ax.plot([sx * 54], [34], "s", color="white", ms=2.2, mec="black", mew=0.5, zorder=7)   # screw head
# cell, bolt below the plate, collar
R(ax, CX - 15, ZP, CX + 15, ZP + 76, NV)                                        # cell (8)
R(ax, CX - 9, 11, CX + 9, 20, "#6b7a90", z=5); R(ax, CX - 6, 20, CX + 6, ZP + 12, "#6b7a90", z=5)   # M12 hex bolt (9)
CZ = ZP + 76
ax.add_patch(Polygon([(CX - 23.2, CZ), (CX - 23.2, CZ + 103), (CX + 23.2, CZ + 103), (CX + 23.2, CZ)], fc=OR, ec="black", lw=0.6, zorder=3))
R(ax, CX - 20.2, CZ + 18, CX + 20.2, CZ + 103, "#f4efe4", z=4)                # bore
R(ax, CX - 9.75, CZ + 5.5, CX + 9.75, CZ + 18, "#f4efe4", z=4)                # head pocket
R(ax, CX - 9, CZ + 5.5, CX + 9, CZ + 17.5, "#6b7a90", z=5)                    # M12 SHCS (9)
R(ax, CX - 19, CZ + 18, CX + 19, CZ + 20, NV, z=6)                            # aluminium disc (10)
R(ax, CX - 19, CZ + 20, CX + 19, CZ + 20 + 360, GR, z=5, ec="#888")           # motor, 360 mm, not in kit
T(ax, CX - 4, 392, "38 mm I-class motor, 360 mm\n(not in kit)", 7, color="#555", rotation=90, va="center", ha="center")
# ring section
RZ = BT_ - 15
for x0, x1 in ((CX - 33, CX - 25), (CX + 25, CX + 33)):
    R(ax, x0, RZ, x1, RZ + 20, OR, hatch="///", z=6)
R(ax, CX - 33, RZ + 15, CX + 33, RZ + 20, OR, z=6)
# dimensions
ax.annotate("", xy=(98, 523), xytext=(98, 0), arrowprops=dict(arrowstyle="<->", lw=0.8, color="#555")); T(ax, 103, 262, "523", 8, color="#555")
T(ax, 103, 493, "24 mm over\nthe motor tip", 6.5, color="#555")
# guys: through pad eyes on the bottom short rails, to stakes (drawn shortened)
SL, SR = -250, 290
ax.plot([-55, SL], [10, 4], color=NV, lw=1.4, zorder=3); ax.plot([55, SR], [10, 4], color=NV, lw=1.4, zorder=3)
for sx in (SL, SR):
    ax.plot([sx, sx + (-14 if sx < 0 else 14)], [4, -26], color=NV, lw=3, zorder=3, solid_capstyle="round")
R(ax, -170, 4, -156, 12, NV, z=4); R(ax, 170, 4, 184, 12, NV, z=4)             # tensioners
ax.plot([-60, -50], [10, 10], "s", color=NV, ms=5, zorder=5); ax.plot([50, 60], [10, 10], "s", color=NV, ms=5, zorder=5)   # pad eyes (6)
T(ax, -325, -36, "guys and stakes drawn shortened: stakes sit about 330 mm out on the diagonals", 8, color="#555")
# cell cable to the DAQ box (2 m or more away, decision 005)
ax.plot([10, 40, 100, 300, 460, 560], [40, 26, 26, 26, 26, 40], color=NV, lw=1.2, ls="--", zorder=3)
T(ax, 598, 52, "to DAQ box, 2 m or more away (3 m cable)", 7.5, color="#555", ha="right")
# DAQ inset top right
R(ax, 340, 440, 590, 540, "white", ec=NV, lw=1.6)
T(ax, 342, 545, "DAQ box (on the ground, not on the frame)", 7.5, color="#555")
R(ax, 352, 455, 400, 520, NV, z=4); R(ax, 412, 490, 470, 520, NV, z=4); R(ax, 412, 455, 470, 480, NV, z=4); R(ax, 482, 455, 530, 520, NV, z=4); R(ax, 540, 455, 580, 490, NV, z=4)
for (n, px, bx) in ((14, 376, 360), (15, 441, 405), (17, 441, 450), (18, 506, 495), (16, 560, 540)):
    bub(ax, n, px, 462, bx, 410)

# left column (x=-190)
column(ax, -190, [(1, -70, 513, 525), (1, -70, 430, 430), (1, -75, BT_ - 10, 310), (2, -50, LB_ - 10, 255),
                  (2, -52, 38, 190), (4, -54, 34, 154), (3, -46, 25, 118), (5, -78, 21.6, 82), (1, -70, 10, 46)])
# right column (x=150)
column(ax, 150, [(7, 28, BT_ + 3, 364), (23, 31, RZ + 8, 330), (22, 23, CZ + 60, 296), (10, 19, CZ + 19, 262),
                 (9, 9, CZ + 10, 228), (8, 15, ZP + 40, 194), (9, 6, 15, 160)])
# ground items right: rope (11), tensioner (12), stake (13)
column(ax, 215, [(11, 110, 7, 80)]); column(ax, 265, [(12, 177, 12, 80)]); column(ax, 315, [(13, SR, -10, 80)])

# ---------------- PLAN ----------------
T(pl, -325, 140, "PLAN  (looking down; frame 160 x 160 mm; top frame, uprights and bottom frame all project onto the same square)", 11, weight="bold")
R(pl, -80, -80, 80, 80, NV, 0.12)                                                # footprint
# plate (dashed outline, under the top rails): cross with the corner L-notches
plate = [(-80, -40), (-60, -40), (-60, -60), (-40, -60), (-40, -80), (40, -80), (40, -60), (60, -60), (60, -40), (80, -40),
         (80, 40), (60, 40), (60, 60), (40, 60), (40, 80), (-40, 80), (-40, 60), (-60, 60), (-60, 40), (-80, 40)]
pl.add_patch(Polygon(plate, fc="#9fb0c8", ec=NV, lw=1.0, ls="--", alpha=0.55, zorder=2))
for (x0, y0, x1, y1) in ((-80, -80, -60, 80), (60, -80, 80, 80), (-60, -80, 60, -60), (-60, 60, 60, 80)):
    R(pl, x0, y0, x1, y1, NV, 0.55, z=3)                                          # top rails
for yb in (-46, 46):
    R(pl, -80, yb - 10, 80, yb + 10, NV, 0.8, z=4)                                # ring bars
R(pl, -33, -58, 33, 58, OR, 0.9, z=5)                                              # ring flange
pl.add_patch(Circle((0, 0), 25, fc="white", ec="black", lw=0.6, zorder=6))
pl.add_patch(Circle((0, 0), 23.2, fc=OR, ec="black", lw=0.8, zorder=7)); pl.add_patch(Circle((0, 0), 20.2, fc="#f4efe4", ec="black", lw=0.5, zorder=8))
pl.add_patch(Circle((0, 0), 19, fc=GR, ec="#888", lw=0.5, zorder=9))
for xx in (-12, 12):
    for yy in (-45, 45):
        pl.plot([xx], [yy], "o", color="white", ms=3, mec=OR, zorder=10)           # ring M3 screws (7)
for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
    ex, ey = sx * 55, sy * 85
    R(pl, ex - 12, ey - 3 if sy > 0 else ey - 3, ex + 12, ey + 3, NV, z=4)         # pad eye on the short rail's outer face (6)
    tx, ty = sx * 112, sy * 120
    pl.plot([ex, tx], [ey, ty], color=NV, lw=1.2, zorder=3)
    R(pl, tx - 4, ty - 4, tx + 4, ty + 4, NV, z=4)
T(pl, 600, -135, "guys shortened in the drawing; all four bottom brackets sit under the rails", 8, color="#555", ha="right")
column(pl, -190, [(1, -70, 40, 90), (6, -67, 85, 50), (5, -50, 0, 10)])
column(pl, 200, [(1, 72, 46, 90), (23, 31, 52, 54), (7, 12, 45, 18), (22, 20, 0, -18)])

# ---------------- LEGEND ----------------
lg.axis("off"); lg.set_xlim(0, 1); lg.set_ylim(0, 1)
lg.text(0.01, 0.985, "Stand v3 parts, extrusion (CAD, before tax, estimates)", fontsize=12, weight="bold", va="top")
lg.add_patch(Rectangle((0.01, 0.952), 0.03, 0.012, fc=OR, ec="black")); lg.text(0.05, 0.958, "PRINTED (filament only)", fontsize=9, va="center")
lg.add_patch(Rectangle((0.5, 0.952), 0.03, 0.012, fc=NV, ec="black")); lg.text(0.54, 0.958, "PURCHASED", fontsize=9, va="center")
y = 0.935
lg.text(0.01, y, "No", fontsize=8, weight="bold"); lg.text(0.06, y, "Part", fontsize=8, weight="bold"); lg.text(0.62, y, "Qty", fontsize=8, weight="bold")
lg.text(0.68, y, "CAD", fontsize=8, weight="bold"); lg.text(0.76, y, "Source", fontsize=8, weight="bold")
y -= 0.014
for (n, name, kind, q, u, src, grp) in ITEMS:
    col = OR if kind == "PRINTED" else NV
    lines = textwrap.wrap(name, 40)
    srcl = textwrap.wrap(src.split("(")[0].strip(), 20)
    h = max(len(lines), len(srcl)) * 0.0128 + 0.0045
    lg.add_patch(Rectangle((0.01, y - 0.011), 0.035, 0.012, fc=col, ec="black"))
    lg.text(0.027, y - 0.005, str(n), fontsize=7, color="white", weight="bold", ha="center", va="center")
    lg.text(0.06, y, "\n".join(lines), fontsize=7, va="top", linespacing=1.15)
    lg.text(0.62, y, str(q), fontsize=7, va="top"); lg.text(0.68, y, "%.2f" % (q * u), fontsize=7, va="top")
    lg.text(0.76, y, "\n".join(srcl), fontsize=6.4, va="top", linespacing=1.15)
    y -= h
y -= 0.008
lg.plot([0.01, 0.99], [y + 0.004, y + 0.004], color="black", lw=0.8)
lg.text(0.01, y - 0.008, "Recommended total  CAD %.2f" % total(), fontsize=9.5, weight="bold", va="top")
lg.text(0.01, y - 0.028, "Reduced (see costing.md)  CAD %.2f" % reduced(), fontsize=9.5, weight="bold", va="top")
lg.text(0.01, y - 0.050, "Plywood alternative: 192.35 recommended, 117.35 reduced.\nCut list: 4 x 483, 6 x 160, 6 x 120 mm (3.61 m).  Printed bracket\nalternative (bracket.py) is not in the total.  Only the cell (8),\nplate (5) and rails (1) are on the thrust path.", fontsize=7, va="top", color="#444")

# no two bubbles may overlap
for key, lst in BUBBLES.items():
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            d = math.hypot(lst[i][1] - lst[j][1], lst[i][2] - lst[j][2])
            assert d >= 26, "callouts %s and %s overlap (%.1f)" % (lst[i][0], lst[j][0], d)
fig.savefig(os.path.join(HERE, "assembly-callouts.png"), dpi=100)
print("wrote assembly-callouts.png")
