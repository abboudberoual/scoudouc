"""Stand v3 hand check at 600 N, 2020 extrusion version (plain arithmetic, all assumptions listed).  Run: python3 handcheck.py"""
import math

G = 9.81
PEAK = 600.0            # I-class peak thrust, N
OVERSHOOT = 1.3         # ignition spike over the data-sheet peak
P = PEAK * OVERSHOOT    # 780 N design vertical load
SIDE = 0.15 * PEAK      # sideways load, 15% of peak (an 8.5 degree misalignment: generous)
SIDE3 = 3 * SIDE        # hold-down design load, 270 N

# --- assumptions (2020 extrusion frame, 3.2 mm aluminium plate; vendor data sheets may be better) ---
E_AL = 69000.0                         # MPa, aluminium
I_2020, Z_2020 = 6000.0, 600.0         # mm4 and mm3 for a 2020 profile (conservative; data sheets say about 6000 to 7000 mm4)
Y_2020 = 110.0                         # MPa, 6063-T5 minimum yield
T_PL, Y_PL = 3.2, 240.0                # plate thickness (1/8 in) and 6061-T6 minimum yield, MPa
SPAN_PLATE = 140.0                     # mm, centre to centre of the two rails the plate rests on
SHEAR_M3_LIP = 3 * 1.8                 # mm2, M3 shank bearing on a T-slot lip (3 mm x 1.8 mm)
TNUT_PULLOUT = 1000.0                  # N, assumed pull-out of an M5 drop-in T-nut (aluminium lips), derated
PADEYE_BREAK = 1000.0                  # N, assumed break load of a small stainless pad eye in plane
PADEYE_H, PADEYE_SPACING = 15.0, 30.0  # mm eye height above the face, screw spacing

out = {}

# --- geometry of the frame (mm): outer 160 x 160, rails 20 x 20, plate top 23 above the ground ---
UPRIGHT, LONG, SHORT, LADDER, BAR = 483.0, 160.0, 120.0, 120.0, 160.0
CUT = {"upright": (UPRIGHT, 4), "long rail (bottom 2, top 2)": (LONG, 4), "short rail (bottom 2, top 2)": (SHORT, 4),
       "ring ladder rail": (LADDER, 2), "ring bar": (BAR, 2)}
out["cut_total_m"] = sum(l * q for l, q in CUT.values()) / 1000.0
out["longest_piece_mm"] = max(l for l, q in CUT.values())
out["height_mm"] = 20 + UPRIGHT + 20
out["motor_tip_H_mm"] = 96 + 360                      # nozzle height above the plate top for a 360 mm motor (foot at 96)
out["top_clearance_mm"] = (out["height_mm"] - 20 - 23) - out["motor_tip_H_mm"]   # underside of the top rails above the motor tip
out["m5_screws"] = 24 * 2 + 8 + 8
out["m5_tnuts"] = 24 * 2 + 8 + 8

# 1) PLATE in bending (it is on the thrust path with the cell): 780 N at the centre.
#    Worst case = only two opposite rails touch it (two-edge, simply supported, effective width = span - 14 mm hole).
b_eff = SPAN_PLATE - 14.0
M = P * SPAN_PLATE / 4
S = b_eff * T_PL ** 2 / 6
out["plate_stress_MPa"] = M / S
out["plate_two_edge_SF"] = Y_PL / (M / S)
out["plate_two_edge_deflection_mm"] = P * SPAN_PLATE ** 3 / (48 * E_AL * (b_eff * T_PL ** 3 / 12))
# four rails touching (the normal case): thin-plate sag of a simply supported square, textbook coefficient 0.1267
out["plate_four_edge_deflection_mm"] = 0.1267 * P * SPAN_PLATE ** 2 / (E_AL * T_PL ** 3)
# the plywood alternative (6 mm, 20 MPa along the grain) in the same two-edge case
out["ply6_two_edge_SF"] = 20.0 / (M / (b_eff * 6.0 ** 2 / 6))

# 2) BOTTOM RAILS under the plate: worst case two rails take half each (390 N) at mid-length and the rail is
#    held only at its two ends (a dip in the ground), clear length 150 mm.
P_RAIL, L_RAIL = P / 2, 150.0
out["rail_stress_MPa"] = (P_RAIL * L_RAIL / 4) / Z_2020
out["rail_SF"] = Y_2020 / out["rail_stress_MPa"]
out["rail_deflection_mm"] = P_RAIL * L_RAIL ** 3 / (48 * E_AL * I_2020)

# 3) GUY ATTACHMENT: pad eye on the outer face of a bottom short rail at the corner end, two M5 screws in two T-nuts.
#    Rope at 45 degrees to the face in plan, nearly flat: 270 N splits into 191 N out of the face and 191 N along it,
#    along the slot toward the end of the rail where the T-nut stops against the long rail.
F_N = SIDE3 / math.sqrt(2)
out["guy_axial_N"] = F_N
tilt_couple = F_N * PADEYE_H / (PADEYE_SPACING / 1000.0) / 1000.0     # N: screw force from tipping the eye
out["guy_screw_peak_N"] = F_N / 2 + tilt_couple
out["guy_tnut_SF"] = TNUT_PULLOUT / out["guy_screw_peak_N"]
out["guy_padeye_SF"] = PADEYE_BREAK / SIDE3
out["guy_stop_bearing_MPa"] = F_N / 25.0                             # T-nut end on the long rail's face, about 25 mm2
out["guy_lip_bearing_MPa"] = F_N / 9.0                               # force across the slot into a bracket-2 screw: 5 mm x 1.8 mm lip

# 4) RING CATCH LOAD 90 N (failure case only; the ring never carries thrust)
out["ring_screw_N_each"] = SIDE / 4
out["ring_screw_lip_MPa"] = (SIDE / 4) / SHEAR_M3_LIP                # across the slot: bearing on the lip
out["ring_screw_SF"] = 100.0 / out["ring_screw_lip_MPa"]            # aluminium bearing about 100 MPa, derated
out["ring_x_friction_SF"] = (4 * 200.0) / SIDE                       # along the slot, friction only, 4 M3 T-nuts at about 200 N each
Mb = (SIDE / 2) * 140.0 / 4                                          # each bar, half the load, 140 mm between the ladder rails
out["bar_stress_MPa"] = Mb / Z_2020
out["bar_SF"] = Y_2020 / out["bar_stress_MPa"]
Z_RING = 304.0                                                       # mm above ground when the ring is at its highest (bar top 281 + 23)
out["upright_stress_MPa"] = (SIDE / 4 * Z_RING) / Z_2020             # worst case: the whole catch load carried by uprights as cantilevers
out["upright_SF"] = Y_2020 / out["upright_stress_MPa"]
out["bracket_screw_pull_N"] = (SIDE / 4 * Z_RING) / 24.0             # one bracket on the 2 N-m class joint, 24 mm lever
out["bracket_tnut_SF"] = TNUT_PULLOUT / out["bracket_screw_pull_N"]

# 5) Hold-down (unchanged from the plywood version)
ROPE_BREAK, KNOT = 1000.0, 0.6                           # N, assumed 4 mm polyester; knot keeps 60%
out["guy_SF_with_knot"] = ROPE_BREAK * KNOT / SIDE3
STAKE = 300.0                                            # N, assumed for a 300 mm stake in firm soil, PROVE by pull test
out["stake_SF"] = STAKE / SIDE3
out["stake_pull_test_N"] = 300.0
out["M12_shear_SF"] = (0.6 * 800 * 84.3) / SIDE3         # M12 8.8 in shear vs 270 N

# 6) Mass (kg)
out["extrusion_kg"] = out["cut_total_m"] * 0.52
out["brackets_kg"] = 24 * 0.015
out["hardware_kg"] = 64 * 0.0025 + 64 * 0.0015 + 4 * 0.03
out["plate_kg"] = 20800 * T_PL * 2.70e-6
out["frame_mass_kg"] = out["extrusion_kg"] + out["brackets_kg"] + out["hardware_kg"] + out["plate_kg"]
out["total_mass_kg"] = out["frame_mass_kg"] + 0.45 + 0.1 + 0.05 + 0.15 + 0.8   # cell, collar+ring, disc, M12 kit, rope+stakes

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
