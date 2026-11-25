# Assembly guides (printable, illustrated, repeatable)

Every part or vehicle that gets built ships with a printable PDF guide made here (CLAUDE.md rule).
Reference guide: **G-001 thrust stand v3** (`stand_v3_guide.py`, `stand_v3_figures.py`).

Build: `python3 hardware/guides/build.py stand_v3` → `out/stand_v3/G-001-…-revA.pdf` (needs CadQuery, matplotlib, Pillow, Chrome).

## How a guide is written
1. `<name>_guide.py` defines the parts (CadQuery solids wrapped in `Part`, one per physical piece, unique names) and `GUIDE = dict(id, title, rev, steps, front, back, ...)`.
2. Each `Step` lists the parts it **adds**; the engine draws them red (orange if printed) over the grey parts already fitted, with numbered callouts. `show`, `zoom`, `zoom_scale`, `view` pick the picture; `image` uses a 2D figure instead.
3. Every step has: numbered actions, "You need" with quantities, tools, time, a check box list that must pass before the next step, and warnings where a mistake damages a part or a person.
4. Front matter: what you have vs what to buy (with prices marked as estimates), tools, safety. Back matter: 1:1 templates (verify the 50 mm square), fastener/torque table, build record, revision log.
5. 1:1 templates are PNGs drawn on axes spanning exactly their width in mm and placed with `width: <W>mm`; check scale after every build.
6. Geometry is illustrative; the real dimensions live in the text and in the design of record. Bump `rev` and add a revision-log row on every change.
