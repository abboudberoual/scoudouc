"""Shared renderer for CadQuery assemblies: shaded isometric PNG (matplotlib, no GPU) + GLB (trimesh) + STEP.

Usage from a part script:
    from render import Part, render
    parts = [Part("Upright", solid, "purchased"), Part("Collar", solid, "printed")]
    render(parts, out_dir, "stand_v3", views=(("iso", 28, -52), ("front", 0, -90)))

Colours follow the repo convention: PRINTED orange, PURCHASED navy, other grey (motor, ground, ropes).
Every CAD deliverable ships with a render (CLAUDE.md).
"""
import os, math
import numpy as np
import cadquery as cq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

COLORS = {"printed": "#E8821A", "purchased": "#1F3A5F", "other": "#9AA0A6", "motor": "#6B6E73", "ground": "#C9CED4", "highlight": "#E4572E"}


class Part:
    def __init__(self, name, shape, kind="purchased", alpha=1.0, frame=True):
        self.name, self.shape, self.kind, self.alpha, self.frame = name, shape, kind, alpha, frame

    def mesh(self, tol=0.6):
        s = self.shape.val() if hasattr(self.shape, "val") else self.shape
        verts, tris = s.tessellate(tol, 0.3)
        v = np.array([[p.x, p.y, p.z] for p in verts], dtype=float)
        f = np.array(tris, dtype=int)
        return v, f


def _shade(normals, light=(0.4, -0.6, 0.7)):
    l = np.array(light) / np.linalg.norm(light)
    return 0.55 + 0.45 * np.clip(normals @ l, 0, 1)


def render_png(parts, path, elev=28, azim=-52, title=None, dpi=160, figsize=(9, 9)):
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, projection="3d")
    allv = []
    for p in parts:
        v, f = p.mesh()
        if len(f) == 0:
            continue
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
        base = np.array(matplotlib.colors.to_rgb(COLORS.get(p.kind, COLORS["other"])))
        sh = _shade(n)
        cols = np.clip(base[None, :] * sh[:, None], 0, 1)
        pc = Poly3DCollection(tri, facecolors=cols, edgecolors="none", alpha=p.alpha)
        ax.add_collection3d(pc)
        if p.frame:
            allv.append(v)
    V = np.vstack(allv)
    lo, hi = V.min(0), V.max(0)
    c, r = (lo + hi) / 2, (hi - lo).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    if title:
        fig.text(0.02, 0.97, title, fontsize=12, va="top", family="DejaVu Sans")
    fig.text(0.02, 0.03, "orange = PRINTED   navy = PURCHASED   grey = not part of the kit", fontsize=9, color="#444")
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def export_glb(parts, path):
    try:
        import trimesh
    except ImportError:
        return None
    meshes = []
    for p in parts:
        v, f = p.mesh(0.4)
        if len(f) == 0:
            continue
        m = trimesh.Trimesh(vertices=v, faces=f, process=False)
        rgb = [int(255 * x) for x in matplotlib.colors.to_rgb(COLORS.get(p.kind, COLORS["other"]))]
        m.visual.face_colors = rgb + [int(255 * p.alpha)]
        m.metadata["name"] = p.name
        meshes.append(m)
    scene = trimesh.Scene(meshes)
    scene.export(path)
    return path


def export_step(parts, path):
    asm = cq.Assembly()
    for i, p in enumerate(parts):
        asm.add(p.shape, name=f"{i:02d} {p.name}")
    asm.save(path)
    return path


def render(parts, out_dir, stem, views=(("iso", 28, -52),), title=None, step=True, glb=True):
    os.makedirs(out_dir, exist_ok=True)
    out = {}
    for name, elev, azim in views:
        out[name] = render_png(parts, os.path.join(out_dir, f"{stem}-{name}.png"), elev, azim, title)
    if glb:
        out["glb"] = export_glb(parts, os.path.join(out_dir, f"{stem}.glb"))
    if step:
        out["step"] = export_step(parts, os.path.join(out_dir, f"{stem}.step"))
    return out
