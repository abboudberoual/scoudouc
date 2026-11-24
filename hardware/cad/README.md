# hardware/cad — parametric models and renders

Every part and vehicle has a render (CLAUDE.md). Scripts are CadQuery; `render.py` exports shaded PNGs (matplotlib, no GPU), a GLB (trimesh) and a STEP assembly.

| Script | What | Status |
|---|---|---|
| `stand_v3_assembly.py` | Thrust stand v3, 2020 tower (decision 007) | layout model; drawing of record is `../test-stand-v3/assembly-callouts.png` |
| `s1_hopper_concept.py` | Scoudouc 1 "Hop" concept (decisions 002 D, 003) | CONCEPT: gimbal is a placeholder until the Garrett-R16 files are checked |

Run: `pip install cadquery trimesh` then `python3 hardware/cad/<script>.py` → `renders/<stem>-{iso,front}.png`, `.glb`, `.step`.
Register on Mission Control: upload the PNG as an asset and write `parts/<id>` `{name, vehicle, status, decision, render, cad, note, concept?}`.
Colours: orange PRINTED, navy PURCHASED, grey motor/ground/ropes. Keep models simple (bars, cylinders, blocks) until a part is being drawn for print; then its own script with print notes.
