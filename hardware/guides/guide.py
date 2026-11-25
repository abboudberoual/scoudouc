"""Assembly-guide engine: a guide spec (steps + geometry) -> illustrated, printable PDF.

Every buildable part or vehicle gets one (CLAUDE.md, "Every build has a printable guide").
A guide spec is a Python module in this folder that defines GUIDE (see stand_v3_guide.py, the reference):

    GUIDE = dict(id="G-001", title=..., rev="A", parts={name: Part}, steps=[Step(...), ...], ...)

Each Step lists the part names it ADDS; the engine draws every step with the new parts in the accent
colour, the parts already fitted in light grey, numbered callouts on the new parts, then lays the
pages out as HTML with print CSS and prints the PDF with headless Chrome (Letter, 0.5 in margins).

Run:  python3 hardware/guides/build.py stand_v3      -> hardware/guides/out/stand_v3/...pdf
"""
import os, html, subprocess, shutil, datetime
from dataclasses import dataclass, field
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d

ACCENT = "#E4572E"      # new in this step
DONE = "#C9CDD3"        # already fitted
PRINTED = "#E8821A"
PURCHASED = "#1F3A5F"
INK = "#1D2430"


@dataclass
class Step:
    title: str
    adds: list                      # part names added in this step (drawn in the accent colour)
    do: list                        # numbered instructions (strings, may contain <b>, <code>)
    parts: list = field(default_factory=list)   # (qty, item) rows for "You need"
    tools: list = field(default_factory=list)
    time: str = ""
    check: list = field(default_factory=list)   # pass/fail checks at the end of the step
    warn: list = field(default_factory=list)    # safety or "don't" notes
    tip: str = ""
    view: tuple = (24, -52)         # elev, azim
    show: list = None               # names to draw (default: everything fitted so far)
    zoom: list = None               # names to frame on (default: all drawn)
    zoom_scale: float = 1.04        # >1 zooms out around the framed parts
    callouts: list = None           # (label, part name) to number; default = adds, numbered 1..n
    image: str = None               # use a pre-made image instead of a render (relative to out dir)
    extra_html: str = ""            # tables, templates etc. placed after the instructions


def _mesh(shape, tol=0.5):
    s = shape.val() if hasattr(shape, "val") else shape
    verts, tris = s.tessellate(tol, 0.3)
    return np.array([[p.x, p.y, p.z] for p in verts], float), np.array(tris, int)


def render_step(parts, fitted, adds, path, view=(24, -52), zoom=None, callouts=None, size=(7.5, 5.4), dpi=170, zoom_scale=1.04):
    """parts: {name: Part}; fitted: names already in place; adds: names new in this step."""
    fig = plt.figure(figsize=size, dpi=dpi)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")
    tris_all, cols_all, frame_v, centres = [], [], [], {}
    light = np.array([0.35, -0.55, 0.75]); light /= np.linalg.norm(light)
    for name in list(fitted) + list(adds):
        p = parts[name]
        v, f = _mesh(p.shape)
        if len(f) == 0:
            continue
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
        sh = 0.62 + 0.38 * np.clip(np.abs(n @ light), 0, 1)
        if p.kind == "ground":
            base = matplotlib.colors.to_rgb("#EEF0F2")
        elif name in adds:
            base = matplotlib.colors.to_rgb(ACCENT if p.kind != "printed" else PRINTED)
        else:
            base = matplotlib.colors.to_rgb(DONE if p.kind not in ("ground",) else "#EEF0F2")
        c = np.clip(np.array(base)[None, :] * sh[:, None], 0, 1)
        a = p.alpha if name not in adds else 1.0
        tris_all.append(tri); cols_all.append(np.hstack([c, np.full((len(c), 1), a)]))
        if p.frame and (zoom is None or name in zoom):
            frame_v.append(v)
        centres[name] = (v.min(0) + v.max(0)) / 2
        if getattr(p, "anchor", None) is not None:
            centres[name] = np.array(p.anchor, float)
    T = np.vstack(tris_all); C = np.vstack(cols_all)
    pc = Poly3DCollection(T, facecolors=C, edgecolors="none")
    ax.add_collection3d(pc)
    V = np.vstack(frame_v)
    lo, hi = V.min(0), V.max(0)
    c, r = (lo + hi) / 2, (hi - lo).max() / 2 * zoom_scale
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=view[0], azim=view[1]); ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    fig.canvas.draw()
    if callouts is None:
        callouts = [(str(i + 1), n) for i, n in enumerate(adds)]
    M = ax.get_proj()
    pts = []
    for label, name in callouts:
        x, y, z = centres[name]
        x2, y2, _ = proj3d.proj_transform(x, y, z, M)
        pts.append((label, x2, y2))
    if pts:
        cx = np.mean([p[1] for p in pts]); cy = np.mean([p[2] for p in pts])
        corners = [proj3d.proj_transform(x, y, z, M)[:2] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
        cx_, cy_ = zip(*corners)
        span = max(max(cx_) - min(cx_), max(cy_) - min(cy_))
        used = []
        for label, x2, y2 in pts:
            d = np.array([x2 - cx, y2 - cy]); d = d / (np.linalg.norm(d) + 1e-9) if np.linalg.norm(d) > 1e-6 else np.array([0.7, 0.7])
            tx, ty = x2 + d[0] * span * 0.16, y2 + d[1] * span * 0.16
            for (ux, uy) in used:                          # nudge labels apart
                if abs(tx - ux) < span * 0.06 and abs(ty - uy) < span * 0.05:
                    ty += span * 0.065
            used.append((tx, ty))
            ax.annotate(label, xy=(x2, y2), xytext=(tx, ty), textcoords="data", fontsize=10, fontweight="bold",
                        color="white", ha="center", va="center", family="DejaVu Sans",
                        bbox=dict(boxstyle="circle,pad=0.28", fc=INK, ec=INK),
                        arrowprops=dict(arrowstyle="-", color=INK, lw=0.9, shrinkA=7, shrinkB=1))
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    _autocrop(path)
    return path


def _autocrop(path, pad=24):
    from PIL import Image, ImageChops
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bb = ImageChops.difference(im, bg).getbbox()
    if bb:
        x0, y0, x1, y1 = bb
        im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad))).save(path)


CSS = """
@page { size: Letter; margin: 0.55in 0.55in 0.6in 0.55in; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; color: #1D2430; font-size: 10.2pt; line-height: 1.38; margin: 0; }
h1 { font-size: 22pt; margin: 0 0 4pt; letter-spacing: -0.3pt; }
h2 { font-size: 14pt; margin: 14pt 0 6pt; border-bottom: 2px solid #1D2430; padding-bottom: 3pt; }
h3 { font-size: 11pt; margin: 10pt 0 4pt; }
.meta { color: #5A6472; font-size: 9pt; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.step { page-break-before: always; }
.stephead { display: flex; align-items: baseline; gap: 10pt; border-bottom: 2px solid #1D2430; padding-bottom: 4pt; margin-bottom: 6pt; }
.stepno { font-size: 26pt; font-weight: 700; color: #E4572E; min-width: 34pt; }
.steptitle { font-size: 15pt; font-weight: 700; flex: 1; }
.steptime { color: #5A6472; font-size: 9pt; white-space: nowrap; }
.grid { display: grid; grid-template-columns: 1fr 2.05in; gap: 10pt; }
.side { font-size: 9pt; }
.box { border: 1px solid #C9CDD3; border-radius: 4pt; padding: 5pt 7pt; margin-bottom: 7pt; break-inside: avoid; }
.box h4 { margin: 0 0 3pt; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.6pt; color: #5A6472; }
.box ul { margin: 0; padding-left: 12pt; }
.fig { width: 100%; max-height: 3.35in; object-fit: contain; border: 1px solid #E3E6EA; border-radius: 4pt; }
.legend { font-size: 8pt; color: #5A6472; margin-top: 2pt; }
.sw { display: inline-block; width: 9pt; height: 9pt; border-radius: 2pt; vertical-align: -1pt; margin: 0 2pt 0 6pt; }
ol.do { padding-left: 16pt; margin: 6pt 0; }
ol.do li { margin-bottom: 4pt; }
.check { background: #EEF6EE; border-color: #9CC59C; }
.warn { background: #FFF2EC; border-color: #E4572E; }
.tip { background: #F3F5F8; }
.cb { display: inline-block; width: 9pt; height: 9pt; border: 1.2px solid #1D2430; border-radius: 2pt; margin-right: 5pt; vertical-align: -1pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 4pt 0 8pt; }
th, td { border: 1px solid #C9CDD3; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #F3F5F8; }
td.num, th.num { text-align: right; white-space: nowrap; }
.have { color: #2E7D32; font-weight: 700; } .need { color: #C62828; font-weight: 700; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt; background: #F3F5F8; padding: 0 2pt; border-radius: 2pt; }
.cover-img { width: 100%; max-height: 5.4in; object-fit: contain; }
.foot { position: fixed; bottom: -0.38in; left: 0; right: 0; font-size: 7.5pt; color: #8A93A0; display: flex; justify-content: space-between; }
.full { width: 100%; }
"""


def _li(items):
    return "".join(f"<li>{x}</li>" for x in items)


def build_html(G, out_dir, step_imgs, cover_img):
    e = html.escape
    today = G.get("date", datetime.date.today().isoformat())
    foot = ""
    out = [f"<!doctype html><html><head><meta charset='utf-8'><title>{e(G['title'])}</title><style>{CSS}</style></head><body>{foot}"]
    # cover
    out.append(f"""<div class="page"><div class="meta">{e(G['id'])} · rev {e(G['rev'])} · {today}</div>
<h1>{e(G['title'])}</h1><div class="meta">{G.get('subtitle','')}</div>
<img class="cover-img" src="{cover_img}">
<div class="grid" style="grid-template-columns:1fr 1fr"><div>{G.get('cover_left','')}</div><div>{G.get('cover_right','')}</div></div></div>""")
    for sec in G.get("front", []):        # front-matter pages: (title, html)
        out.append(f'<div class="page"><h2>{e(sec[0])}</h2>{sec[1]}</div>')
    for i, (s, img) in enumerate(zip(G["steps"], step_imgs), 1):
        side = ""
        if s.parts:
            side += '<div class="box"><h4>You need</h4><table>' + "".join(
                f'<tr><td class="num">{q}</td><td>{it}</td></tr>' for q, it in s.parts) + "</table></div>"
        if s.tools:
            side += f'<div class="box"><h4>Tools</h4><ul>{_li(s.tools)}</ul></div>'
        if s.warn:
            side += f'<div class="box warn"><h4>Careful</h4><ul>{_li(s.warn)}</ul></div>'
        if s.tip:
            side += f'<div class="box tip"><h4>Tip</h4>{s.tip}</div>'
        labels = s.callouts if s.callouts is not None else [(str(k + 1), n) for k, n in enumerate(s.adds)]
        leg = " ".join(f"<b>{l}</b> {e(n)}" + ("&nbsp;&nbsp;" if True else "") for l, n in labels)
        legend = (f'<div class="legend"><span class="sw" style="background:{ACCENT}"></span>new in this step'
                  f'<span class="sw" style="background:{PRINTED}"></span>new, printed'
                  f'<span class="sw" style="background:{DONE}"></span>already fitted</div>'
                  + (f'<div class="legend">{leg}</div>' if labels else ""))
        checks = "".join(f'<div><span class="cb"></span>{c}</div>' for c in s.check)
        out.append(f"""<div class="step"><div class="stephead"><span class="stepno">{i}</span><span class="steptitle">{e(s.title)}</span><span class="steptime">{e(s.time)} · {e(G["id"])} rev {e(G["rev"])} · step {i}/{len(G["steps"])}</span></div>
<div class="grid"><div><img class="fig" src="{img}">{legend}<ol class="do">{_li(s.do)}</ol>
{('<div class="box check"><h4>Check before you go on</h4>' + checks + '</div>') if checks else ''}{s.extra_html}</div><div class="side">{side}</div></div></div>""")
    for sec in G.get("back", []):
        out.append(f'<div class="step"><h2>{e(sec[0])}</h2>{sec[1]}</div>')
    out.append("</body></html>")
    path = os.path.join(out_dir, "guide.html")
    with open(path, "w") as f:
        f.write("\n".join(out))
    return path


def print_pdf(html_path, pdf_path):
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        raise SystemExit("needs Chrome/Chromium for the PDF; the HTML is at " + html_path)
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", "file://" + os.path.abspath(html_path)],
                   check=True, capture_output=True, timeout=180)
    return pdf_path


def build(G, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    parts = G["parts"]
    fitted, imgs = [], []
    for i, s in enumerate(G["steps"], 1):
        if s.image:
            imgs.append(s.image)
        else:
            before = [n for n in fitted if (s.show is None or n in s.show) and n not in s.adds]
            adds = [n for n in s.adds if (s.show is None or n in s.show)]
            fn = f"step{i:02d}.png"
            render_step(parts, before, adds, os.path.join(out_dir, fn), s.view, s.zoom, s.callouts, zoom_scale=s.zoom_scale)
            imgs.append(fn)
        fitted += [n for n in s.adds if n not in fitted]
    cover = "cover.png"
    render_step(parts, [n for n in fitted if n not in G.get("cover_hide", [])], [], os.path.join(out_dir, cover),
                G.get("cover_view", (22, -55)), callouts=[], size=(7.5, 6.2))
    h = build_html(G, out_dir, imgs, cover)
    pdf = print_pdf(h, os.path.join(out_dir, G["pdf_name"]))
    return pdf
