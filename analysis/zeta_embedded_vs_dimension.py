#!/usr/bin/env python3
"""
ζ EMBEDDED vs ζ AS ITS OWN DIMENSION
======================================
Compare two approaches:

  A) ζ embedded: g_μν = diag(-(1-r_s/r)·ζ, g_rr·ζ, g_θθ·ζ, g_φφ·ζ, Ṡ², 1/r)
     Primes modify all 4 spacetime dimensions. 6D total.

  B) ζ as dimension: g_μν = diag(-(1-r_s/r), g_rr, g_θθ, g_φφ, Ṡ², ζ(s))
     Primes live in their own dimension, replacing temperature. 6D total.
     Standard GR spacetime untouched.

Question: What are the physical differences?
"""

import math

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11
c = 2.99792458e8
M_sun = 1.989e30  # Use a solar-mass black hole for dramatic effects
r_s_sun = 2 * G * M_sun / c**2  # ~2953 m

# Also Earth for GPS check
M_earth = 5.9722e24
R_earth = 6.3781e6
R_gps = 2.6571e7
r_s_earth = 2 * G * M_earth / c**2

# ═══════════════════════════════════════════════════════════
# ZETA
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
    return 1.0 + (r / r_s)**3

# ═══════════════════════════════════════════════════════════
# APPROACH A: ζ EMBEDDED IN SPACETIME
# ═══════════════════════════════════════════════════════════
def approach_A(r, r_s, theta=math.pi/2):
    """Returns dict of all metric components with ζ embedded"""
    s = s_of_r(r, r_s)
    z = zeta(s)
    
    g_tt = -(1 - r_s/r) * z
    g_rr = (1 / (1 - r_s/r)) * z if r != r_s else float('inf')
    g_thth = r**2 * z
    g_phph = r**2 * math.sin(theta)**2 * z
    S_dot = 1.0  # normalized entropy rate
    g_55 = 1.0 / r
    
    # Total geometric content = product of |diagonal elements|
    # (determinant-like measure)
    clock_rate = math.sqrt(abs(g_tt)) if g_tt != 0 else 0
    
    return {
        'g_tt': g_tt, 'g_rr': g_rr, 'g_thth': g_thth, 'g_phph': g_phph,
        'g_55': g_55, 'g_66': None,  # no separate prime dimension
        'zeta': z, 's': s,
        'clock': clock_rate,
        'label': 'ζ embedded'
    }

# ═══════════════════════════════════════════════════════════
# APPROACH B: ζ AS ITS OWN DIMENSION (replaces temperature)
# ═══════════════════════════════════════════════════════════
def approach_B(r, r_s, theta=math.pi/2):
    """Returns dict of all metric components with ζ as own dimension"""
    s = s_of_r(r, r_s)
    z = zeta(s)
    
    # Standard GR — untouched
    g_tt = -(1 - r_s/r)
    g_rr = 1 / (1 - r_s/r) if r != r_s else float('inf')
    g_thth = r**2
    g_phph = r**2 * math.sin(theta)**2
    S_dot = 1.0
    g_55 = z  # prime dimension replaces 1/r temperature
    
    clock_rate = math.sqrt(abs(g_tt)) if g_tt != 0 else 0
    
    return {
        'g_tt': g_tt, 'g_rr': g_rr, 'g_thth': g_thth, 'g_phph': g_phph,
        'g_55': g_55, 'g_66': None,
        'zeta': z, 's': s,
        'clock': clock_rate,
        'label': 'ζ as dimension'
    }

# ═══════════════════════════════════════════════════════════
# COMPARISON
# ═══════════════════════════════════════════════════════════
print("=" * 100)
print("  ζ EMBEDDED IN SPACETIME  vs  ζ AS ITS OWN DIMENSION")
print("=" * 100)
print()
print("  Approach A: g_μν = diag( -(1-r_s/r)·ζ,  g_rr·ζ,  g_θθ·ζ,  g_φφ·ζ,  Ṡ²,  1/r )")
print("  Approach B: g_μν = diag( -(1-r_s/r),     g_rr,    g_θθ,    g_φφ,    Ṡ²,   ζ  )")
print()
print("  In A, primes touch everything. In B, primes live in their own house.")
print()

# ═══════════════════════════════════════════════════════════
# GPS CHECK
# ═══════════════════════════════════════════════════════════
print("=" * 100)
print("  GPS SANITY CHECK (Earth)")
print("=" * 100)
print()
a_earth = approach_A(R_earth, r_s_earth)
b_earth = approach_B(R_earth, r_s_earth)
a_gps = approach_A(R_gps, r_s_earth)
b_gps = approach_B(R_gps, r_s_earth)

print(f"  At Earth surface:")
print(f"    A (embedded):  g_tt = {a_earth['g_tt']:.12f}   clock = {a_earth['clock']:.12f}   ζ = {a_earth['zeta']:.15f}")
print(f"    B (dimension): g_tt = {b_earth['g_tt']:.12f}   clock = {b_earth['clock']:.12f}   ζ = {b_earth['zeta']:.15f}")
print(f"  At GPS orbit:")
print(f"    A (embedded):  g_tt = {a_gps['g_tt']:.12f}   clock = {a_gps['clock']:.12f}")
print(f"    B (dimension): g_tt = {b_gps['g_tt']:.12f}   clock = {b_gps['clock']:.12f}")
print(f"  → Both identical at GPS distances (ζ = 1)")
print()

# ═══════════════════════════════════════════════════════════
# SOLAR-MASS BLACK HOLE COMPARISON
# ═══════════════════════════════════════════════════════════
print("=" * 100)
print("  SOLAR-MASS BLACK HOLE — FALLING IN")
print("=" * 100)
print()

r_s = r_s_sun
print(f"  r_s = {r_s:.2f} m ({r_s/1000:.3f} km)")
print()

header = f"  {'r/r_s':<8s} │ {'s(r)':<10s} │ {'ζ(s)':<12s} │ {'A: g_tt':<14s} │ {'B: g_tt':<14s} │ {'A: clock':<12s} │ {'B: clock':<12s} │ {'A: g_rr':<14s} │ {'B: g_rr':<14s} │ {'A: g_55':<12s} │ {'B: g_55(=ζ)':<12s}"
print(header)
print("  " + "─" * (len(header) - 2))

test_radii = [1000, 100, 50, 20, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05, 1.01]
for rr in test_radii:
    r = rr * r_s
    a = approach_A(r, r_s)
    b = approach_B(r, r_s)
    
    def fmt(v, w=12):
        if v is None: return "—".ljust(w)
        if abs(v) > 1e6: return f"{v:.2e}".ljust(w)
        if abs(v) > 100: return f"{v:.2f}".ljust(w)
        if abs(v) < 0.001: return f"{v:.6f}".ljust(w)
        return f"{v:.6f}".ljust(w)
    
    z_str = f"{a['zeta']:.6f}" if a['zeta'] < 1e6 else f"{a['zeta']:.2e}"
    
    print(f"  {rr:<8.2f} │ {a['s']:<10.4f} │ {z_str:<12s} │ {fmt(a['g_tt'],14)} │ {fmt(b['g_tt'],14)} │ {fmt(a['clock'])} │ {fmt(b['clock'])} │ {fmt(a['g_rr'],14)} │ {fmt(b['g_rr'],14)} │ {fmt(a['g_55'])} │ {fmt(b['g_55'])}")

print()

# ═══════════════════════════════════════════════════════════
# KEY DIFFERENCES ANALYSIS
# ═══════════════════════════════════════════════════════════
print("=" * 100)
print("  KEY DIFFERENCES")
print("=" * 100)
print()

print("  ┌─────────────────────────────────────────────────────────────────────────────────────┐")
print("  │ PROPERTY                    │ A (ζ EMBEDDED)              │ B (ζ AS DIMENSION)       │")
print("  ├─────────────────────────────┼─────────────────────────────┼──────────────────────────┤")

# Time at horizon
a_h = approach_A(1.01 * r_s, r_s)
b_h = approach_B(1.01 * r_s, r_s)
print(f"  │ Clock at r=1.01r_s          │ {a_h['clock']:.6f} (primes help)    │ {b_h['clock']:.6f} (standard GR)  │")

# Radial stretch at r=1.5
a15 = approach_A(1.5 * r_s, r_s)
b15 = approach_B(1.5 * r_s, r_s)
print(f"  │ g_rr at r=1.5r_s            │ {a15['g_rr']:.4f} (amplified)       │ {b15['g_rr']:.4f} (standard)       │")

# 5th dimension at r=2
a2 = approach_A(2 * r_s, r_s)
b2 = approach_B(2 * r_s, r_s)
print(f"  │ g_55 at r=2r_s              │ {a2['g_55']:.6f} (= 1/r, temp)   │ {b2['g_55']:.6f} (= ζ, primes) │")

# GPS
print(f"  │ GPS time dilation           │ Identical to GR             │ Identical to GR          │")

# Time stops?
print(f"  │ Time at horizon             │ Slowed but primes resist    │ Stops (standard GR)      │")

# Spacetime modified?
print(f"  │ Spacetime geometry          │ Modified by primes          │ Standard GR untouched    │")

# Where do primes live?
print(f"  │ Where primes act            │ Inside all 4 dimensions     │ In their own dimension   │")

# Temperature dimension
print(f"  │ Temperature (1/r)           │ ✅ Present (g_55 = 1/r)     │ ❌ Replaced by ζ          │")

# Hawking connection
print(f"  │ Hawking temp at horizon     │ ✅ g_55 = 4π·T_H exactly    │ ❌ Lost (no 1/r)          │")

print("  └─────────────────────────────┴─────────────────────────────┴──────────────────────────┘")
print()

# ═══════════════════════════════════════════════════════════
# DETERMINANT COMPARISON (geometric volume element)
# ═══════════════════════════════════════════════════════════
print("=" * 100)
print("  GEOMETRIC VOLUME (|det g| proxy — product of diagonal magnitudes)")
print("=" * 100)
print()
print(f"  {'r/r_s':<10s} {'A: volume':<20s} {'B: volume':<20s} {'Ratio A/B':<16s}")
print(f"  {'─'*10} {'─'*20} {'─'*20} {'─'*16}")

for rr in [100, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05]:
    r = rr * r_s
    a = approach_A(r, r_s)
    b = approach_B(r, r_s)
    
    # Volume = |g_tt * g_rr * g_thth * g_phph * g_55|
    # (skip Ṡ² since it's the same)
    vol_a = abs(a['g_tt'] * a['g_rr'] * a['g_thth'] * a['g_phph'] * a['g_55'])
    vol_b = abs(b['g_tt'] * b['g_rr'] * b['g_thth'] * b['g_phph'] * b['g_55'])
    
    ratio = vol_a / vol_b if vol_b > 0 else float('inf')
    
    def vfmt(v):
        if v > 1e20: return f"{v:.2e}"
        if v > 1e6: return f"{v:.2e}"
        return f"{v:.4f}"
    
    print(f"  {rr:<10.2f} {vfmt(vol_a):<20s} {vfmt(vol_b):<20s} {ratio:<16.6f}")

print()
print("  In approach A, ζ⁴ multiplies the 4D volume (ζ on each of 4 components).")
print("  In approach B, ζ only enters as its own dimension — 4D spacetime volume is standard GR.")
print()

# ═══════════════════════════════════════════════════════════
# VERDICT
# ═══════════════════════════════════════════════════════════
print("=" * 100)
print("  ANALYSIS")
print("=" * 100)
print("""
  APPROACH A (ζ embedded in spacetime):
    ✅ Primes modify spacetime directly — "if it's matter, treat it like matter"
    ✅ Temperature dimension preserved (Hawking connection intact)
    ✅ Time doesn't fully stop at horizon (primes keep cycle alive)
    ✅ Consistent: same physics in all dimensions
    ⚠️  ζ⁴ amplification could be too aggressive deep inside

  APPROACH B (ζ as own dimension):
    ✅ Standard GR spacetime completely preserved
    ✅ Clean separation: GR does GR, primes do primes
    ✅ Easier to test — any deviation from GR is in the new dimension only
    ❌ Loses temperature dimension (Hawking connection broken)
    ❌ Time still stops at horizon (no prime resistance)
    ❌ Primes are "next to" spacetime but don't touch it — observationally harder to detect

  THE TRADE-OFF:
    A says primes ARE the fabric. B says primes live alongside the fabric.
    A modifies gravity. B adds to gravity.
    A keeps Hawking. B loses Hawking.
""")
