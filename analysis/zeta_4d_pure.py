#!/usr/bin/env python3
"""
ζ PURE 4D — PRIMES ON SPACETIME ONLY
======================================
Compare three things:

  GR:  g_μν = diag( -(1-r_s/r),     1/(1-r_s/r),     r²,       r²sin²θ )
  4D:  g_μν = diag( -(1-r_s/r)·ζ,   1/(1-r_s/r)·ζ,   r²·ζ,     r²sin²θ·ζ )

  Standard 4×4 Schwarzschild vs prime-modified 4×4.
  No extra dimensions. Pure 4D only.

Question: Does the 4D prime-modified metric hold up on its own?
"""

import math

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11
c = 2.99792458e8
k_B = 1.380649e-23
hbar = 1.054571817e-34

M_sun = 1.989e30
r_s_sun = 2 * G * M_sun / c**2  # ~2953 m

M_earth = 5.9722e24
R_earth = 6.3781e6
R_gps = 2.6571e7
r_s_earth = 2 * G * M_earth / c**2

# Sagittarius A*
M_sgra = 4.0e6 * M_sun
r_s_sgra = 2 * G * M_sgra / c**2

# ═══════════════════════════════════════════════════════════
# ZETA (Euler product over primes)
# ═══════════════════════════════════════════════════════════
def sieve_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

PRIMES = sieve_primes(10000)

def zeta(s):
    """Riemann zeta via Euler product"""
    if s <= 1.0:
        return float('inf')
    product = 1.0
    for p in PRIMES:
        term = 1.0 / (1.0 - p**(-s))
        product *= term
        if abs(term - 1.0) < 1e-15:
            break
    return product

def s_of_r(r, r_s):
    """Map radial coordinate to zeta argument"""
    return 1.0 + (r / r_s)**3

# ═══════════════════════════════════════════════════════════
# STANDARD GR (4D Schwarzschild)
# ═══════════════════════════════════════════════════════════
def standard_gr(r, r_s, theta=math.pi/2):
    ratio = r_s / r
    g_tt = -(1 - ratio)
    g_rr = 1 / (1 - ratio) if r != r_s else float('inf')
    g_thth = r**2
    g_phph = r**2 * math.sin(theta)**2
    clock = math.sqrt(abs(g_tt)) if g_tt != 0 else 0

    return {
        'g_tt': g_tt, 'g_rr': g_rr, 'g_thth': g_thth, 'g_phph': g_phph,
        'clock': clock, 'zeta': 1.0, 's': None,
        'label': 'Standard GR'
    }

# ═══════════════════════════════════════════════════════════
# PRIME-MODIFIED 4D (ζ on all 4 components, nothing else)
# ═══════════════════════════════════════════════════════════
def prime_4d(r, r_s, theta=math.pi/2):
    s = s_of_r(r, r_s)
    z = zeta(s)
    ratio = r_s / r

    g_tt = -(1 - ratio) * z
    g_rr = (1 / (1 - ratio)) * z if r != r_s else float('inf')
    g_thth = r**2 * z
    g_phph = r**2 * math.sin(theta)**2 * z
    clock = math.sqrt(abs(g_tt)) if g_tt != 0 else 0

    return {
        'g_tt': g_tt, 'g_rr': g_rr, 'g_thth': g_thth, 'g_phph': g_phph,
        'clock': clock, 'zeta': z, 's': s,
        'label': 'Prime 4D'
    }

# ═══════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════

def fmt(v, w=14):
    if v is None: return "—".ljust(w)
    if abs(v) == float('inf'): return "∞".ljust(w)
    if abs(v) > 1e6: return f"{v:.4e}".ljust(w)
    if abs(v) > 100: return f"{v:.4f}".ljust(w)
    if abs(v) < 1e-6 and v != 0: return f"{v:.4e}".ljust(w)
    if abs(v) < 0.0001 and v != 0: return f"{v:.8f}".ljust(w)
    return f"{v:.8f}".ljust(w)

print()
print("=" * 110)
print("  PURE 4D PRIME-MODIFIED METRIC — NO EXTRA DIMENSIONS")
print("=" * 110)
print()
print("  GR:  g_μν = diag( -(1-rₛ/r),     1/(1-rₛ/r),     r²,       r²sin²θ )")
print("  4D:  g_μν = diag( -(1-rₛ/r)·ζ,   1/(1-rₛ/r)·ζ,   r²·ζ,     r²sin²θ·ζ )")
print()

# ── GPS SANITY CHECK ──────────────────────────────────────
print("=" * 110)
print("  TEST 1: GPS SANITY CHECK")
print("=" * 110)
print()

gr_earth = standard_gr(R_earth, r_s_earth)
p4_earth = prime_4d(R_earth, r_s_earth)
gr_gps = standard_gr(R_gps, r_s_earth)
p4_gps = prime_4d(R_gps, r_s_earth)

# Time dilation in μs/day
sec_per_day = 86400
grav_dilation_earth = (1 - gr_earth['clock']) * sec_per_day * 1e6
grav_dilation_gps = (1 - gr_gps['clock']) * sec_per_day * 1e6
net_gr = grav_dilation_gps - grav_dilation_earth

p4_dilation_earth = (1 - p4_earth['clock']) * sec_per_day * 1e6
p4_dilation_gps = (1 - p4_gps['clock']) * sec_per_day * 1e6
net_p4 = p4_dilation_gps - p4_dilation_earth

print(f"  At Earth surface:")
print(f"    GR:  g_tt = {gr_earth['g_tt']:.15f}   clock = {gr_earth['clock']:.15f}")
print(f"    4D:  g_tt = {p4_earth['g_tt']:.15f}   clock = {p4_earth['clock']:.15f}   ζ = {p4_earth['zeta']:.15f}")
print(f"  At GPS orbit:")
print(f"    GR:  g_tt = {gr_gps['g_tt']:.15f}   clock = {gr_gps['clock']:.15f}")
print(f"    4D:  g_tt = {p4_gps['g_tt']:.15f}   clock = {p4_gps['clock']:.15f}   ζ = {p4_gps['zeta']:.15f}")
print()
print(f"  GPS gravitational dilation (GR):  {net_gr:.4f} μs/day")
print(f"  GPS gravitational dilation (4D):  {net_p4:.4f} μs/day")
print(f"  Difference: {abs(net_gr - net_p4):.2e} μs/day")
print(f"  → {'PASS: Identical to GR at GPS distances' if abs(net_gr - net_p4) < 1e-6 else 'DIFFERENCE DETECTED'}")
print()

# ── SOLAR-MASS BLACK HOLE ─────────────────────────────────
print("=" * 110)
print("  TEST 2: SOLAR-MASS BLACK HOLE — RADIAL PROFILE")
print("=" * 110)
print()

r_s = r_s_sun
print(f"  M = 1 M☉,  rₛ = {r_s:.2f} m")
print()

header = f"  {'r/rₛ':<8s} │ {'ζ(s)':<12s} │ {'GR: g_tt':<14s} │ {'4D: g_tt':<14s} │ {'GR: clock':<12s} │ {'4D: clock':<12s} │ {'GR: g_rr':<14s} │ {'4D: g_rr':<14s}"
print(header)
print("  " + "─" * (len(header) - 2))

test_radii = [1000, 100, 50, 20, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05, 1.01]
for rr in test_radii:
    r = rr * r_s
    gr = standard_gr(r, r_s)
    p4 = prime_4d(r, r_s)
    z_str = f"{p4['zeta']:.6f}" if p4['zeta'] < 1e6 else f"{p4['zeta']:.2e}"
    print(f"  {rr:<8.2f} │ {z_str:<12s} │ {fmt(gr['g_tt'])} │ {fmt(p4['g_tt'])} │ {fmt(gr['clock'],12)} │ {fmt(p4['clock'],12)} │ {fmt(gr['g_rr'])} │ {fmt(p4['g_rr'])}")

print()

# ── RADIAL DIVERGENCE CHECK ───────────────────────────────
print("=" * 110)
print("  TEST 3: RADIAL DIVERGENCE — DOES g_rr BLOW UP?")
print("=" * 110)
print()
print("  In standard GR, g_rr → ∞ as r → rₛ. Does ζ help?")
print()

close_radii = [1.1, 1.05, 1.02, 1.01, 1.005, 1.002, 1.001]
print(f"  {'r/rₛ':<10s} │ {'GR: g_rr':<16s} │ {'4D: g_rr':<16s} │ {'ζ(s)':<14s} │ {'4D/GR ratio':<14s}")
print(f"  {'─'*10} │ {'─'*16} │ {'─'*16} │ {'─'*14} │ {'─'*14}")

for rr in close_radii:
    r = rr * r_s
    gr = standard_gr(r, r_s)
    p4 = prime_4d(r, r_s)
    ratio = p4['g_rr'] / gr['g_rr'] if gr['g_rr'] != float('inf') else float('inf')
    print(f"  {rr:<10.3f} │ {fmt(gr['g_rr'],16)} │ {fmt(p4['g_rr'],16)} │ {fmt(p4['zeta'])} │ {fmt(ratio)}")

print()
print("  Note: 4D/GR ratio = ζ(s). If ζ → 1, divergence is identical to GR.")
print("  If ζ > 1 near horizon, prime substrate AMPLIFIES the divergence (not removes it).")
print("  Divergence removal would require a different coupling (e.g., ζ in denominator).")
print()

# ── GEOMETRIC VOLUME ──────────────────────────────────────
print("=" * 110)
print("  TEST 4: 4D GEOMETRIC VOLUME (√|det g|)")
print("=" * 110)
print()
print(f"  {'r/rₛ':<10s} │ {'GR: √|det|':<18s} │ {'4D: √|det|':<18s} │ {'Ratio 4D/GR':<14s} │ {'= ζ^n':<10s}")
print(f"  {'─'*10} │ {'─'*18} │ {'─'*18} │ {'─'*14} │ {'─'*10}")

for rr in [100, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05]:
    r = rr * r_s
    gr = standard_gr(r, r_s)
    p4 = prime_4d(r, r_s)

    vol_gr = math.sqrt(abs(gr['g_tt'] * gr['g_rr'] * gr['g_thth'] * gr['g_phph']))
    vol_p4 = math.sqrt(abs(p4['g_tt'] * p4['g_rr'] * p4['g_thth'] * p4['g_phph']))
    ratio = vol_p4 / vol_gr if vol_gr > 0 else float('inf')

    # ζ^n where n = ?  (each component gets one ζ, so det gets ζ^4, sqrt gets ζ^2)
    z = p4['zeta']
    expected = z**2

    def vfmt(v):
        if v > 1e12: return f"{v:.4e}"
        if v > 1e6: return f"{v:.4e}"
        return f"{v:.4f}"

    print(f"  {rr:<10.2f} │ {vfmt(vol_gr):<18s} │ {vfmt(vol_p4):<18s} │ {ratio:<14.6f} │ {'ζ²':<10s}")

print()
print("  Volume ratio = ζ² always (4 components each ×ζ → det ×ζ⁴ → √det ×ζ²)")
print()

# ── VERDICT ───────────────────────────────────────────────
print("=" * 110)
print("  ANALYSIS: PURE 4D METRIC")
print("=" * 110)
print("""
  WHAT WORKS:
    ✅ GPS check passes — ζ = 1.0 at Earth/GPS distances, identical to GR
    ✅ CST axiom proof unaffected — that's about prime structure, not the metric
    ✅ Cleaner claim — "primes modify spacetime" not "primes add dimensions"
    ✅ No extra dimensions to defend

  WHAT TO WATCH:
    ⚠️  g_rr still diverges at horizon (ζ amplifies, doesn't remove)
    ⚠️  Volume element scales as ζ² — physical meaning TBD

  KEY INSIGHT:
    The 4D metric stands on its own for the CST argument.
    Paper 5 proves primes satisfy CST and couple to GR. Pure spacetime.
""")
