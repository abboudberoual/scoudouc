# Playbook — the library (`data/library/`)

The library is the program's moat and the product's Layer 1: structured, sourced, machine-readable knowledge of motors, materials, print constraints, vendors and rules. Every value needs a source; numeric values need two or a `single-source` flag.

## Files
- `motors.json` — one entry per motor: `{designation, manufacturer, diameter_mm, length_mm, total_impulse_Ns, avg_thrust_N, max_thrust_N, burn_s, propellant_g, total_g, delay_options, ejection_direction, curve: [[t_s, N]], cert_body, sources: [{url, date, what}], tier}`. Primary source: thrustcurve.org (.eng/.rse). Secondary: manufacturer certification sheet.
- `materials.json` — PLA and friends: `{name, density, Tg_C, print_speed_mms_mk3, heat_barrier_required_within_mm, sources}`.
- `vendors.json` — Canadian stock: `{part, vendor, url, price_cad, stock, lead_days, checked_at}`; refreshed weekly.
- `rules.json` — rules-as-code: `{id, authority, section, text, machine: {...}, sources, review}`. Anything touching impulse limits, storage or site distances carries `review: opus` before merge.
- `used_prices.json`, `seller_flags.json` — from the procurement loop.
- `validate.py` — schema + sources + unit checks; CI runs it.
- `CHANGELOG.md` — append-only, one line per change with sources.

## Tiers of confidence
`seed` (unverified) → `single-source` → `dual-source` → `measured` (our own static fire) . A sim rerun uses only `dual-source` or `measured` curves.

## Process
1. Extraction is a local job (`type: extract`, output schema = the entry schema, acceptance = `python data/library/validate.py --file <out>`).
2. The builder grades, adds the second source itself (web), sets the tier, commits `library:`.
3. Any entry our static fires contradict by > 10 % on total impulse → `measured` wins, surprise logged, sim rerun.
4. Dead source URL → replace for this run, playbook fix via PR.
