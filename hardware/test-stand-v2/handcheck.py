"""Hand checks for Stand v2 at the I-class peak (600 N).  Run: python3 handcheck.py
Every number here is also in README.md.  Section values are CONSERVATIVE (about 70% of typical catalogue data);
replace them with your vendor's data sheet when you order."""
import math

E = 69000.0          # MPa, aluminium
YIELD = 110.0        # MPa, minimum yield of 6063-T5 (typical is higher)
A = 300.0            # mm2, 2040 cross-section (assumed)
I_WEAK = 8000.0      # mm4, bending across the 20 mm direction (assumed)
I_STRONG = 25000.0   # mm4, bending across the 40 mm direction (assumed)
P = 600.0            # N, I-class peak
DYN = 1.3            # dynamic amplification on ignition (assumed)
T_NUT_SLIP = 400.0   # N, slip capacity of one M5 T-nut in a 6 mm slot (assumed, conservative)

def deck_rails():
    L = 320.0
    M = P * L / 4                 # N mm, load at mid-span, two rails share it
    sigma = (M / 2) * 10 / I_WEAK
    defl = P * L ** 3 / (48 * E * 2 * I_WEAK)
    return sigma, YIELD / sigma, YIELD / (sigma * DYN), defl

def long_rail():
    Lsp, a = 460.0, 120.0         # span between cross-rail centres, load 120 mm from the rear one
    b = Lsp - a
    R = P / 2                     # each long rail takes half
    M = R * a * b / Lsp
    sigma = M * 10 / I_WEAK
    return sigma, YIELD / sigma

def joints():
    per_bracket = (P / 4) / 2     # 4 deck-rail ends, 2 brackets per joint
    return per_bracket, T_NUT_SLIP / per_bracket

def uprights():
    Fax = P / 2                   # worst case: all thrust reaches the portal, shared by two uprights
    Pcr = math.pi ** 2 * E * I_WEAK / (2.0 * 400.0) ** 2     # cantilever, K = 2, 400 mm
    side = 100.0                  # N sideways at the guide ring (3 x 15% x 600 N is 270 N hold-down; ring load is less)
    M = (side / 2) * 111.0        # per upright, 111 mm above the foot
    sig_b = M * 10 / I_WEAK       # weak-axis, conservative
    return Fax / A, Pcr / Fax, sig_b, YIELD / (sig_b + Fax / A)

def bar_cell_couple():
    F, lever, pitch = 490.0, 60.0, 10.0       # 50 kg cell at rated load
    bolt = F * lever / pitch
    washer = math.pi / 4 * (22 ** 2 - 5.5 ** 2)
    web = math.pi * 22 * 12
    return bolt, 8500.0 / bolt, bolt / washer, bolt / web

if __name__ == "__main__":
    s, sf, sfd, d = deck_rails(); print("deck rails (2 x 2040 flat, 320 mm span): %.0f MPa, SF %.1f (%.1f with x1.3), deflection %.2f mm" % (s, sf, sfd, d))
    s, sf = long_rail(); print("long rail: %.0f MPa, SF %.1f" % (s, sf))
    f, sf = joints(); print("joint bracket: %.0f N each, SF %.1f on T-nut slip" % (f, sf))
    s, sf, sb, sfy = uprights(); print("uprights: axial %.1f MPa, buckling SF %.0f, bending %.1f MPa, combined yield SF %.0f" % (s, sf, sb, sfy))
    b, sf, br, sh = bar_cell_couple(); print("50 kg bar cell mount: bolt %.0f N (M5 proof SF %.1f), PLA bearing %.1f MPa, web shear %.1f MPa" % (b, sf, br, sh))
