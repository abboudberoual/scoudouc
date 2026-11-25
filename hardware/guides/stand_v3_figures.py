"""2D figures for G-001: the extrusion cut plan and the 1:1 plate drilling template."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

INK, ACC, GREY = "#1D2430", "#E4572E", "#C9CDD3"
KERF = 3


def cut_plan(path):
    bars = [("Bar 1", [("Upright", 483), ("Upright", 483)]),
            ("Bar 2", [("Upright", 483), ("Upright", 483)]),
            ("Bar 3", [("Long rail", 160)] * 4 + [("Ring bar", 160)] * 2),
            ("Bar 4", [("Short rail", 120)] * 4 + [("Ladder rail", 120)] * 2)]
    col = {"Upright": "#1F3A5F", "Long rail": "#3E6A99", "Ring bar": ACC, "Short rail": "#6C93BC", "Ladder rail": "#E8821A"}
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=200)
    for i, (bn, cuts) in enumerate(bars):
        y = 3 - i
        ax.add_patch(Rectangle((0, y - 0.3), 1000, 0.6, fc="#F3F5F8", ec=GREY, lw=0.8))
        x = 0
        for nm, L in cuts:
            ax.add_patch(Rectangle((x, y - 0.3), L, 0.6, fc=col[nm], ec="white", lw=0.8))
            ax.text(x + L / 2, y, f"{nm}\n{L}", ha="center", va="center", color="white", fontsize=6.5, fontweight="bold")
            x += L + KERF
        ax.text(-12, y, bn, ha="right", va="center", fontsize=8, color=INK, fontweight="bold")
        ax.text(1012, y, f"{1000 - x + KERF:.0f} left", ha="left", va="center", fontsize=7, color="#5A6472")
    for t in range(0, 1001, 100):
        ax.plot([t, t], [-0.55, -0.45], color="#5A6472", lw=0.6)
        ax.text(t, -0.72, str(t), ha="center", va="top", fontsize=6, color="#5A6472")
    ax.text(500, 3.62, "Cut plan: four 1000 mm bars, 3 mm saw kerf allowed between pieces (mm)", ha="center", fontsize=8.5, color=INK)
    ax.set_xlim(-90, 1110); ax.set_ylim(-1.0, 3.8); ax.axis("off")
    fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)


def plate_template(path):
    """1:1 when the PNG is shown 180 mm wide. Axes span exactly 180 x 200 mm."""
    Wmm, Hmm = 180.0, 200.0
    fig = plt.figure(figsize=(Wmm / 25.4, Hmm / 25.4), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-90, 90); ax.set_ylim(-110, 90); ax.set_aspect("equal"); ax.axis("off")
    s, n1, n2 = 80, 60, 40          # half size, notch inner edges
    pts = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        pts += [(sx * n2, sy * s), (sx * n2, sy * n1), (sx * n1, sy * n1), (sx * n1, sy * n2), (sx * s, sy * n2)] if (sx, sy) == (1, 1) else []
    # walk the outline counter-clockwise: each corner has an L notch (20 x 40 + 40 x 20)
    outline = [(40, 80), (-40, 80), (-40, 60), (-60, 60), (-60, 40), (-80, 40), (-80, -40), (-60, -40), (-60, -60), (-40, -60),
               (-40, -80), (40, -80), (40, -60), (60, -60), (60, -40), (80, -40), (80, 40), (60, 40), (60, 60), (40, 60)]
    ax.add_patch(Rectangle((-80, -80), 160, 160, fill=False, ec=GREY, lw=0.6, ls="--"))
    ax.add_patch(Polygon(outline, closed=True, fill=False, ec=INK, lw=1.0))
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        ax.text(sx * 70, sy * 70, "cut\naway", ha="center", va="center", fontsize=5.5, color="#8A93A0")
    holes = [(70, 25), (70, -25), (-70, 25), (-70, -25), (25, 70), (-25, 70), (25, -70), (-25, -70)]
    for hx, hy in holes:
        ax.add_patch(Circle((hx, hy), 2.75, fill=False, ec=ACC, lw=0.8))
        ax.plot([hx - 4, hx + 4], [hy, hy], color=INK, lw=0.4); ax.plot([hx, hx], [hy - 4, hy + 4], color=INK, lw=0.4)
    ax.add_patch(Circle((0, 0), 6.5, fill=False, ec=ACC, lw=0.9))
    ax.plot([-9, 9], [0, 0], color=INK, lw=0.4); ax.plot([0, 0], [-9, 9], color=INK, lw=0.4)
    ax.text(0, -12, "Ø13 (M12 cell)\nØ11 for M10", ha="center", va="top", fontsize=6, color=INK)
    ax.text(0, 50, "8 holes Ø5.5 (M5) on the rail centre lines,\n70 mm from centre, 25 mm either side", ha="center", va="center", fontsize=6.2, color=INK)
    ax.text(0, 30, "FRONT (−Y) is the bottom edge", ha="center", fontsize=6, color="#5A6472")
    ax.text(-80, 84, "160 mm", fontsize=6, color="#5A6472")
    # scale check square
    ax.add_patch(Rectangle((-80, -105), 50, 18, fill=False, ec=INK, lw=0.8))
    ax.text(-55, -96, "50 mm check: must measure 50.0", ha="center", va="center", fontsize=5.8, color=INK)
    ax.text(20, -96, "G-001 Appendix A · plate 3.2 mm 6061-T6", ha="left", va="center", fontsize=5.8, color="#5A6472")
    fig.savefig(path, facecolor="white", dpi=300); plt.close(fig)


def make_figures(out):
    cut_plan(os.path.join(out, "cutplan.png"))
    plate_template(os.path.join(out, "plate_template.png"))
