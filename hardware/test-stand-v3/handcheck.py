"""Stand v3 hand check at 600 N (plain arithmetic, all assumptions listed).  Run: python3 handcheck.py"""
import math

G = 9.81
PEAK = 600.0            # I-class peak thrust, N
OVERSHOOT = 1.3         # ignition spike over the data-sheet peak
P = PEAK * OVERSHOOT    # 780 N design vertical load
SIDE = 0.15 * PEAK      # sideways load, 15% of peak (an 8.5 degree misalignment: generous)
SIDE3 = 3 * SIDE        # hold-down design load, 270 N

# --- assumptions (18 mm plywood, vendor data sheets may be better) ---
T = 18.0
MOR_ACROSS, MOR_ALONG = 10.0, 20.0     # MPa, assumed rupture stress (across / along face grain), conservative
E_ALONG = 6000.0                       # MPa, assumed
SHEAR_SCREW = 250.0                    # N per #6/#8 screw in single shear in 18 mm ply, assumed (derated)
WD_FACE, WD_EDGE = 300.0, 80.0         # N withdrawal per #8 screw: into ply face / into ply edge, assumed (derated)

out = {}

# 1) BASE BOARD in bending: the ONLY member on the thrust path. Worst case: ground touches only two edges,
#    board simply supported over its long side, load at mid-span, grain along the span.
L, b = 260.0, 220.0
hole = 28.0                                   # counterbore under the cell (net width)
S = (b - hole) * T ** 2 / 6
M = P * L / 4
sig = M / S
out["base_stress_MPa"] = sig
out["base_SF_along_grain"] = MOR_ALONG / sig
out["base_SF_across_grain"] = MOR_ACROSS / sig            # if the sheet is cut the wrong way round
I = b * T ** 3 / 12
out["base_deflection_mm"] = P * L ** 3 / (48 * E_ALONG * I)
out["base_bearing_MPa"] = P / (30 * 50 - math.pi / 4 * 14 ** 2)   # cell foot 30 x 50 mm assumed

# 2) Ring-to-bar screws in SHEAR: motor hits the ring with the whole 15% sideways load, 4 screws
out["ring_screw_N_each"] = SIDE / 4
out["ring_screw_SF"] = SHEAR_SCREW / (SIDE / 4)

# 3) Ring catch load in Y: two bars, each a 40 x 18 plywood strip on edge, 224 mm span, bent the weak way
Sb = 40 * T ** 2 / 6
BAR_SPAN = 164.0                                         # clear between the two panels
Mb = (SIDE / 2) * BAR_SPAN / 4
out["bar_stress_MPa"] = Mb / Sb
out["bar_SF"] = MOR_ACROSS / (Mb / Sb)

# 4) Ring catch load in X: each panel gets half of it at the ring height (145 mm); the foot joint takes the moment
Z_RING = 145.0
# the two bars share the push, so each panel sees half of it at the ring height
Tension = (SIDE / 2 * Z_RING) / (T + 25.0)               # couple over 43 mm (panel thickness + half a bracket leg)
cap = 2 * WD_FACE + 3 * WD_EDGE                          # outer bracket 2 screws + 3 screws up through the base
out["panel_foot_T_N"] = Tension
out["panel_foot_SF"] = cap / Tension

# 5) Buckling of a side panel (cantilever K=2, 280 mm) with 100 N down from guy/ring effects: trivial
Ip = 220 * T ** 3 / 12
out["panel_buckling_N"] = math.pi ** 2 * E_ALONG * Ip / (2 * 280) ** 2

# 6) Cell bolts in shear, M12 8.8 (shear strength about 0.6 x 800 MPa x 84 mm2) vs 270 N
out["M12_shear_SF"] = (0.6 * 800 * 84.3) / SIDE3

# 7) Guys: worst case one guy carries the full 270 N (push along a diagonal)
ROPE_BREAK, KNOT = 1000.0, 0.6                           # N, assumed 4 mm polyester; knot keeps 60%
out["guy_SF_with_knot"] = ROPE_BREAK * KNOT / SIDE3
STAKE = 300.0                                            # N, assumed for a 300 mm stake in firm soil, PROVE by pull test
out["stake_SF"] = STAKE / SIDE3
out["stake_pull_test_N"] = 300.0

# 7b) Base-corner guy hole: 6 mm hole 15 mm from the edges, pull toward the corner, plywood shear 2 MPa assumed
out["guy_hole_SF"] = (2 * (15 - 3) * T * 2.0) / SIDE3

# 8) Mass
area = 0.260 * 0.220 + 2 * 0.220 * 0.280 + 2 * 0.040 * 0.164
out["ply_mass_kg"] = area * 0.018 * 650
out["total_mass_kg"] = out["ply_mass_kg"] + 0.45 + 0.1 + 0.15 + 0.1 + 0.8   # cell, collar+ring, brackets, screws, rope+stakes

# 9) Cell choice and C6 resolution (ESP32 3.3 V excitation, ADS1220 gain 128, 2 mV/V cell, ASSUMED noise)
for kg in (50, 100):
    rated = kg * G
    out["cell_%d_rated_N" % kg] = rated
    out["cell_%d_peak_frac_with_overshoot" % kg] = P / rated
FS_N = 100 * G
fs_mV = 2.0 * 3.3
lsb_nV = 2 * (3.3 / 128) / 2 ** 24 * 1e9
out["counts_full_scale"] = fs_mV * 1e-3 / (lsb_nV * 1e-9)
out["N_per_count_mN"] = FS_N / out["counts_full_scale"] * 1e3
NOISE_UV = 0.6                                           # uV rms at 1000 SPS gain 128 (assumed; read the data sheet)
out["noise_N_rms"] = NOISE_UV * 1e-6 / (fs_mV * 1e-3) * FS_N
out["noise_N_rms_avg10"] = out["noise_N_rms"] / math.sqrt(10)
out["cell_error_N"] = 0.0003 * FS_N                      # 0.03% FS combined error, typical, ASSUMED
C6_PEAK, C6_PLATEAU = 14.0, 5.0
out["C6_peak_pct_err"] = 100 * out["cell_error_N"] / C6_PEAK
out["C6_plateau_pct_err"] = 100 * out["cell_error_N"] / C6_PLATEAU
out["C6_noise_pct_of_plateau_avg10"] = 100 * out["noise_N_rms_avg10"] / C6_PLATEAU
out["C6_cell_pct_of_range"] = 100 * C6_PEAK / FS_N

if __name__ == "__main__":
    for k, v in out.items():
        print("%-34s %10.3f" % (k, v))
