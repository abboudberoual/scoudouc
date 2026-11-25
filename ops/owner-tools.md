# Owner's tools and workshop access (design constraint)

Every design, procedure and guide is checked against this list before it reaches the owner
(CLAUDE.md, "Design for the tools on hand"). Update it the day a tool is bought or a workshop opens up.

Last updated: 2026-11-25 (owner, in chat)

| Tool | Have? |
|---|---|
| Metric hex key set | yes |
| Calipers | yes |
| Multimeter | yes |
| Square + tape measure | yes |
| Kitchen / luggage scale | yes |
| Cordless drill | no |
| Soldering iron | no |
| Rotary tool (Dremel) | no |
| Jigsaw / circular saw | no |
| Hacksaw, files | no |
| Torque wrench / torque screwdriver | no |
| Workshop access (Concordia makerspace, machine shop, garage) | none for now |
| 3D printers | Concordia library (Prusa MK3) and lab (Creality), see CLAUDE.md |

## Rules
1. Prefer designs that need only the tools above, printed parts, and hardware that is pre-made or pre-drilled (T-slot brackets, T-nuts, bracket kits, screw terminals, Wago connectors).
2. If a new tool is unavoidable, it goes on ONE ranked buy list: ranked by the work it unblocks (critical-path steps first), then by price. Never ask for a tool one step at a time.
3. Every guide's tool list says, per tool, HAVE or BUY; a BUY tool names the cheapest alternative that avoids it (e.g. print it, buy it pre-cut, have the supplier drill it).
4. Torque: no torque wrench; write torques as "about N N·m" with a hand-feel description.

## Ranked tool buy list (estimates, CAD; procurement builder confirms prices on T-036)
| Rank | Tool | Unblocks | Est. CAD | Avoid it by |
|---|---|---|---|---|
| 1 | Fine hacksaw (24–32 TPI) + mitre box | Extrusion cuts (stand, swing rig, gimbal fixture), kraft airframe tube | ~30 | Buying 2020 pre-cut to length (bars already bought) |
| 2 | Soldering iron kit (temperature-controlled) + solder | NAU7802 headers, load-cell wiring, flight computer, pyro board (December) | ~35–60 | Pre-soldered modules + screw terminals (not always available) |
| 3 | Sandpaper assortment (80–240 grit) | Deburring cut aluminium | ~6 | (replaces files) |
| 4 | Cordless drill + metal bits | Holes in aluminium, airframe holes | ~80–130 | Printed parts with built-in holes, pre-drilled brackets; defer until a critical-path step truly needs it |
| — | Torque wrench | nothing on the critical path | — | hand-feel torque notes |
