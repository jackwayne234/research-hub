#!/usr/bin/env python3
"""
GR Emergence from Primes — Version 3: The Inverse Relationship
================================================================
Framework:
  ζ(s) × 1/ζ(s) = 1    (perfect symmetry = flat spacetime)
  Mass breaks the symmetry by changing s.

Equation:
  PRIME SIDE          =  GEOMETRY SIDE
  ∏(1 - p⁻ˢ)⁻¹      =  g_rr = 1/(1-r_s/r)
  ∏(1 - p⁻ˢ)         =  -g_tt = (1-r_s/r)

Equivalently:
  r_s/r = 1 - ∏(1 - p⁻ˢ)     ← gravitational potential from primes

Test:
  Invert ζ to find s(r). If s(r) is natural (not tuned), primes are
  doing real physics. Napkin math predicts s ≈ log₂(r/r_s).
"""

import math

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11
c = 2.99792458e8
M_earth = 5.9722e24
R_earth = 6.3781e6
R_gps = 2.6571e7
r_s_earth = 2 * G * M_earth / c**2
v_gps = math.sqrt(G * M_earth / R_gps)

M_sun = 1.989e30
r_s_sun = 2 * G * M_sun / c**2

# ═══════════════════════════════════════════════════════════
# PRIMES & ZETA
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
    """ζ(s) via Euler product"""
    if s <= 1.0:
        return float('inf')
    product = 1.0
    for p in PRIMES:
        term = 1.0 / (1.0 - p**(-s))
        product *= term
        if abs(term - 1.0) < 1e-15:
            break
    return product

def inv_zeta(s):
    """1/ζ(s) = ∏(1 - p⁻ˢ)"""
    if s <= 1.0:
        return 0.0
    product = 1.0
    for p in PRIMES:
        term = 1.0 - p**(-s)
        product *= term
        if abs(term - 1.0) < 1e-15:
            break
    return product

def invert_zeta(target, tol=1e-12, max_iter=200):
    """
    Find s such that ζ(s) = target.
    Uses bisection since ζ is monotonically decreasing for s > 1.
    """
    if target <= 1.0:
        return float('inf')
    if target == float('inf'):
        return 1.0

    # Bisection: ζ(s_low) > target > ζ(s_high)
    s_low = 1.0001
    s_high = 100.0

    # Make sure bracket is wide enough
    while zeta(s_high) > target:
        s_high *= 2
    while zeta(s_low) < target and s_low > 1.00001:
        s_low = 1.0 + (s_low - 1.0) / 2

    for _ in range(max_iter):
        s_mid = (s_low + s_high) / 2
        z_mid = zeta(s_mid)

        if abs(z_mid - target) / target < tol:
            return s_mid

        if z_mid > target:
            s_low = s_mid   # need larger s to decrease ζ
        else:
            s_high = s_mid  # need smaller s to increase ζ

    return (s_low + s_high) / 2


# ═══════════════════════════════════════════════════════════
# THE EQUATION
# ═══════════════════════════════════════════════════════════
def symmetry_at(r, r_s):
    """
    Given a radius r and Schwarzschild radius r_s, compute:
    - The GR metric components
    - The required ζ value
    - The s value (by inverting ζ)
    - The symmetry breaking: ζ - 1/ζ
    - The log₂ prediction for s
    """
    ratio = r_s / r

    # GR side
    g_tt = -(1 - ratio)
    g_rr = 1 / (1 - ratio) if r > r_s else float('inf')
    clock_gr = math.sqrt(1 - ratio) if r > r_s else 0.0

    # Prime side: ζ(s) must equal g_rr
    target_zeta = g_rr
    s = invert_zeta(target_zeta) if target_zeta < 1e15 else 1.0001

    # Verify
    z = zeta(s)
    iz = inv_zeta(s)

    # Symmetry measures
    asymmetry = z - iz           # = 0 when flat, grows with curvature
    product = z * iz             # should always = 1 (by definition)

    # Prediction: s ≈ log₂(r/r_s)
    s_predicted = math.log2(r / r_s) if r > r_s else 0.0

    return {
        'r_over_rs': r / r_s,
        'g_tt': g_tt, 'g_rr': g_rr, 'clock_gr': clock_gr,
        'zeta': z, 'inv_zeta': iz,
        's': s, 's_predicted': s_predicted,
        'asymmetry': asymmetry, 'product': product,
        'ratio': ratio
    }


# ═══════════════════════════════════════════════════════════
# PHASE 1: THE SYMMETRY — ζ × 1/ζ = 1
# ═══════════════════════════════════════════════════════════
print()
print("=" * 100)
print("  GR EMERGENCE FROM PRIMES — Version 3: The Inverse Relationship")
print("  ∏(1-p⁻ˢ)⁻¹ = g_rr     ∏(1-p⁻ˢ) = -g_tt     ζ × 1/ζ = 1 (symmetry)")
print("=" * 100)

print()
print("─" * 100)
print("  PHASE 1: SYMMETRY — ζ(s) × 1/ζ(s) = 1 at all s")
print("─" * 100)
print()
print(f"  {'s':<8s} {'ζ(s)':<16s} {'1/ζ(s)':<16s} {'ζ × 1/ζ':<12s} {'ζ - 1/ζ':<14s} {'state':<20s}")
print(f"  {'─'*8} {'─'*16} {'─'*16} {'─'*12} {'─'*14} {'─'*20}")

test_s = [100, 50, 20, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05, 1.01]
for s_val in test_s:
    z = zeta(s_val)
    iz = inv_zeta(s_val)
    prod = z * iz
    asym = z - iz

    z_str = f"{z:.8f}" if z < 1e5 else f"{z:.4e}"
    iz_str = f"{iz:.8f}" if iz > 1e-8 else f"{iz:.4e}"

    if asym < 0.001:
        state = "≈ flat"
    elif asym < 1:
        state = "mild curvature"
    elif asym < 10:
        state = "strong curvature"
    else:
        state = "near singularity"

    print(f"  {s_val:<8.2f} {z_str:<16s} {iz_str:<16s} {prod:<12.8f} {asym:<14.6f} {state}")

print()
print("  → ζ × 1/ζ = 1 always. Perfect symmetry when ζ = 1/ζ = 1 (flat).")
print("    Asymmetry (ζ - 1/ζ) grows as s → 1 — symmetry breaking IS gravity.")

# ═══════════════════════════════════════════════════════════
# PHASE 2: INVERT ζ — FIND s(r) FOR EARTH
# ═══════════════════════════════════════════════════════════
print()
print("─" * 100)
print("  PHASE 2: WHAT IS s(r)? — Inverting ζ to find the prime coordinate")
print("  Testing against prediction: s ≈ log₂(r/r_s)")
print("─" * 100)
print()

r_s = r_s_earth
print(f"  Earth: r_s = {r_s:.6e} m ({r_s*1000:.4f} mm)")
print()

print(f"  {'r/r_s':<12s} {'g_rr (GR)':<16s} {'s (inverted)':<14s} {'log₂(r/r_s)':<14s} {'s - log₂':<12s} {'asymmetry':<14s}")
print(f"  {'─'*12} {'─'*16} {'─'*14} {'─'*14} {'─'*12} {'─'*14}")

test_ratios = [1e9, 1e8, 1e7, 1e6, 1e5, 1e4, 1e3, 100, 50, 20, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05]
for ratio in test_ratios:
    r = ratio * r_s
    result = symmetry_at(r, r_s)

    grr_str = f"{result['g_rr']:.10f}" if result['g_rr'] < 100 else f"{result['g_rr']:.6f}"
    s_str = f"{result['s']:.6f}"
    sp_str = f"{result['s_predicted']:.6f}"
    diff = result['s'] - result['s_predicted']
    diff_str = f"{diff:+.6f}"
    asym_str = f"{result['asymmetry']:.6e}" if result['asymmetry'] < 0.01 else f"{result['asymmetry']:.6f}"

    print(f"  {ratio:<12.0e} {grr_str:<16s} {s_str:<14s} {sp_str:<14s} {diff_str:<12s} {asym_str:<14s}")

print()
print("  → If s ≈ log₂(r/r_s) holds, the mapping is natural (base-2 because 2 is the first prime).")
print("    Deviations at small r/r_s = where HIGHER primes contribute to ζ.")

# ═══════════════════════════════════════════════════════════
# PHASE 2b: HOW MANY PRIMES MATTER AT EACH DISTANCE?
# ═══════════════════════════════════════════════════════════
print()
print("─" * 100)
print("  HOW MANY PRIMES CONTRIBUTE AT EACH DISTANCE?")
print("─" * 100)
print()

print(f"  {'r/r_s':<10s} {'s':<10s} {'p=2 term':<14s} {'p=3 term':<14s} {'p=5 term':<14s} {'p=7 term':<14s} {'# primes > 1e-10':<18s}")
print(f"  {'─'*10} {'─'*10} {'─'*14} {'─'*14} {'─'*14} {'─'*14} {'─'*18}")

for ratio in [1e9, 1e6, 1e3, 100, 10, 5, 3, 2, 1.5, 1.1]:
    r = ratio * r_s
    result = symmetry_at(r, r_s)
    s_val = result['s']

    terms = []
    for p in [2, 3, 5, 7]:
        terms.append(p**(-s_val))

    # Count significant primes
    n_sig = 0
    for p in PRIMES:
        if p**(-s_val) > 1e-10:
            n_sig += 1
        else:
            break

    t_strs = [f"{t:.4e}" if t < 0.001 else f"{t:.8f}" for t in terms]
    print(f"  {ratio:<10.0e} {s_val:<10.4f} {t_strs[0]:<14s} {t_strs[1]:<14s} {t_strs[2]:<14s} {t_strs[3]:<14s} {n_sig:<18d}")

print()
print("  → Far from mass: only p=2 matters (weak field, s large).")
print("    Near horizon: ALL primes contribute (strong field, s → 1).")

# ═══════════════════════════════════════════════════════════
# PHASE 3: GPS TEST
# ═══════════════════════════════════════════════════════════
print()
print("─" * 100)
print("  PHASE 3: GPS TEST — Does the inverse relationship reproduce ~38.6 μs/day?")
print("─" * 100)
print()

# GR reference
gr_clock_earth = math.sqrt(1 - r_s_earth / R_earth)
gr_clock_gps = math.sqrt(1 - r_s_earth / R_gps)
gr_grav = (gr_clock_gps - gr_clock_earth) * 86400 * 1e6
vel_corr = -(v_gps**2) / (2 * c**2) * 86400 * 1e6
gr_total = gr_grav + vel_corr

# Prime metric via inversion
result_earth = symmetry_at(R_earth, r_s_earth)
result_gps = symmetry_at(R_gps, r_s_earth)

# Clock rates from 1/ζ (the g_tt side): clock = √(1/ζ) = √(-g_tt)
clock_prime_earth = math.sqrt(result_earth['inv_zeta'])
clock_prime_gps = math.sqrt(result_gps['inv_zeta'])

prime_grav = (clock_prime_gps - clock_prime_earth) * 86400 * 1e6
prime_total = prime_grav + vel_corr

print(f"  PRIME SIDE:")
print(f"    s(Earth) = {result_earth['s']:.6f}    (log₂ prediction: {result_earth['s_predicted']:.6f})")
print(f"    s(GPS)   = {result_gps['s']:.6f}    (log₂ prediction: {result_gps['s_predicted']:.6f})")
print(f"    ζ(Earth) = {result_earth['zeta']:.15f}")
print(f"    ζ(GPS)   = {result_gps['zeta']:.15f}")
print(f"    1/ζ(Earth) = {result_earth['inv_zeta']:.15f}")
print(f"    1/ζ(GPS)   = {result_gps['inv_zeta']:.15f}")
print()
print(f"  GEOMETRY SIDE (Schwarzschild):")
print(f"    g_rr(Earth) = {result_earth['g_rr']:.15f}")
print(f"    g_rr(GPS)   = {result_gps['g_rr']:.15f}")
print(f"    -g_tt(Earth) = {-result_earth['g_tt']:.15f}")
print(f"    -g_tt(GPS)   = {-result_gps['g_tt']:.15f}")
print()
print(f"  SYMMETRY CHECK:")
print(f"    ζ × 1/ζ at Earth = {result_earth['product']:.15f}  (should be 1)")
print(f"    ζ × 1/ζ at GPS   = {result_gps['product']:.15f}  (should be 1)")
print(f"    Asymmetry at Earth = {result_earth['asymmetry']:.6e}")
print(f"    Asymmetry at GPS   = {result_gps['asymmetry']:.6e}")
print()
print(f"  TIME DILATION:")
print(f"    Prime gravitational:  {prime_grav:+.6f} μs/day")
print(f"    GR gravitational:     {gr_grav:+.6f} μs/day")
print(f"    Velocity correction:  {vel_corr:+.3f} μs/day")
print()
print(f"    ╔═══════════════════════════════════════════════╗")
print(f"    ║  Prime total:   {prime_total:+.3f} μs/day           ║")
print(f"    ║  GR total:      {gr_total:+.3f} μs/day            ║")
print(f"    ║  Measured GPS:  ~38.6 μs/day                 ║")
print(f"    ║  Difference:    {abs(prime_total - gr_total):.6f} μs/day            ║")
print(f"    ╚═══════════════════════════════════════════════╝")
print()

# ═══════════════════════════════════════════════════════════
# PHASE 4: THE FULL 4×4 MATRIX
# ═══════════════════════════════════════════════════════════
print("─" * 100)
print("  FULL 4×4 METRIC TENSOR — primes = geometry")
print("─" * 100)

for ratio, label in [(1e9, "deep space (flat)"), (10, "10 r_s"), (2, "2 r_s (ISCO)"), (1.1, "near horizon")]:
    r = ratio * r_s_sun
    result = symmetry_at(r, r_s_sun)
    theta = math.pi / 2

    g_tt = -result['inv_zeta']
    g_rr = result['zeta']
    g_thth = r**2 * result['zeta']
    g_phph = r**2 * math.sin(theta)**2 * result['zeta']

    sch_gtt = result['g_tt']
    sch_grr = result['g_rr']

    print(f"""
  r = {ratio:.0e} r_s  ({label})    s = {result['s']:.4f}    asymmetry = {result['asymmetry']:.6f}

  PRIME METRIC:                              SCHWARZSCHILD:
  ┌                                    ┐     ┌                                    ┐
  │ {g_tt:>10.6f}   0       0       0  │     │ {sch_gtt:>10.6f}   0       0       0  │
  │    0    {g_rr:>10.6f}   0       0  │     │    0    {sch_grr:>10.6f}   0       0  │
  │    0       0    {g_thth:>10.4e}  0  │     │    0       0    {r**2:>10.4e}  0  │
  │    0       0       0  {g_phph:>10.4e}│     │    0       0       0  {r**2*math.sin(theta)**2:>10.4e}│
  └                                    ┘     └                                    ┘""")

# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print()
print("=" * 100)
print("  SUMMARY")
print("=" * 100)
print("""
  THE EQUATION:
    ∏(1 - p⁻ˢ)⁻¹  =  (1 - r_s/r)⁻¹     primes = geometry (g_rr)
    ∏(1 - p⁻ˢ)     =  (1 - r_s/r)        inverse primes = inverse geometry (-g_tt)
    ζ × 1/ζ = 1 always                    perfect symmetry = flat spacetime

  THE MAPPING:
    s ≈ log₂(r/r_s) in weak fields (only first prime p=2 matters)
    s → 1 at horizon (all primes contribute)
    s → ∞ at infinity (no primes matter, flat)

  NOISE CANCELING:
    Primes (disorder) × Geometry (order) = 1 (symmetry)
    Mass breaks the symmetry: ζ ≠ 1/ζ → curvature
    More mass → more asymmetry → stronger gravity

  THE PRIME HIERARCHY:
    Far field:  only p=2 matters → gravity is simple
    Near horizon: all primes contribute → gravity is complex
    This is a PREDICTION: gravitational complexity increases near singularities
""")
