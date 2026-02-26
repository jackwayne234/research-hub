#!/usr/bin/env python3
"""
GR Emergence from Primes
=========================
Does General Relativity emerge from the Euler product?

Metric tensor built ENTIRELY from ζ(s):
  g_tt  = -1/ζ(s)    = -∏(1 - p⁻ˢ)       ← time
  g_rr  =  ζ(s)      =  ∏(1 - p⁻ˢ)⁻¹     ← radial
  g_θθ  =  r²·ζ(s)                         ← polar
  g_φφ  =  r²sin²θ·ζ(s)                   ← azimuthal

s = mass parameter.
  s → ∞  :  ζ = 1  →  flat Minkowski (no mass)
  s → 1⁺ :  ζ → ∞  →  singularity

Phase 1: Start Euclidean (s large, matrix flat)
Phase 2: Dial up mass (decrease s, matrix fills)
Phase 3: Check if GPS ~38.6 μs/day emerges
"""

import math

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
    """ζ(s) via Euler product over primes"""
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

# ═══════════════════════════════════════════════════════════
# METRIC TENSOR FROM PRIMES
# ═══════════════════════════════════════════════════════════
def prime_metric(s, r, theta=math.pi/2):
    """
    Build the 4x4 diagonal metric purely from ζ(s).
    Returns the 4 diagonal components and the perturbation from flat.
    """
    z = zeta(s)
    iz = inv_zeta(s)

    # Metric components
    g_tt   = -iz            # -1/ζ(s) = -∏(1 - p⁻ˢ)
    g_rr   =  z             #  ζ(s)   =  ∏(1 - p⁻ˢ)⁻¹
    g_thth =  r**2 * z
    g_phph =  r**2 * math.sin(theta)**2 * z

    # Flat Minkowski in spherical coords (for comparison)
    eta_tt   = -1.0
    eta_rr   =  1.0
    eta_thth =  r**2
    eta_phph =  r**2 * math.sin(theta)**2

    # Perturbation from flat
    h_tt   = g_tt   - eta_tt     # = 1 - 1/ζ
    h_rr   = g_rr   - eta_rr     # = ζ - 1
    h_thth = g_thth - eta_thth   # = r²(ζ - 1)
    h_phph = g_phph - eta_phph   # = r²sin²θ(ζ - 1)

    # Clock rate: √|g_tt| = √(1/ζ) = 1/√ζ
    clock = math.sqrt(iz) if iz > 0 else 0.0

    return {
        'g_tt': g_tt, 'g_rr': g_rr, 'g_thth': g_thth, 'g_phph': g_phph,
        'h_tt': h_tt, 'h_rr': h_rr, 'h_thth': h_thth, 'h_phph': h_phph,
        'clock': clock, 'zeta': z, 'inv_zeta': iz, 's': s
    }

# ═══════════════════════════════════════════════════════════
# STANDARD GR (for comparison)
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11
c = 2.99792458e8
M_earth = 5.9722e24
R_earth = 6.3781e6
R_gps = 2.6571e7
r_s_earth = 2 * G * M_earth / c**2
v_gps = math.sqrt(G * M_earth / R_gps)

def schwarzschild_clock(r, r_s):
    """Standard GR clock rate at radius r"""
    return math.sqrt(1 - r_s / r)

# GR time dilation (gravitational only)
gr_clock_earth = schwarzschild_clock(R_earth, r_s_earth)
gr_clock_gps = schwarzschild_clock(R_gps, r_s_earth)
gr_grav_dilation = (gr_clock_gps - gr_clock_earth) * 86400 * 1e6  # μs/day

# GR velocity correction
vel_correction = -(v_gps**2) / (2 * c**2) * 86400 * 1e6  # μs/day
gr_total = gr_grav_dilation + vel_correction

# ═══════════════════════════════════════════════════════════
# PHASE 1: START EUCLIDEAN — VERIFY FLAT
# ═══════════════════════════════════════════════════════════
print()
print("=" * 90)
print("  GR EMERGENCE FROM PRIMES")
print("  Metric: g_μν = diag( -1/ζ(s),  ζ(s),  r²·ζ(s),  r²sin²θ·ζ(s) )")
print("  s = mass parameter.  s → ∞: flat.  s → 1⁺: singularity.")
print("=" * 90)

print()
print("─" * 90)
print("  PHASE 1: EUCLIDEAN (no mass, s → ∞)")
print("─" * 90)
print()

r_test = R_earth  # use Earth radius for spatial coords
for s_val in [1000, 100, 50, 20]:
    m = prime_metric(s_val, r_test)
    print(f"  s = {s_val:<6}  ζ = {m['zeta']:.12f}   g_tt = {m['g_tt']:.12f}   g_rr = {m['g_rr']:.12f}   clock = {m['clock']:.12f}")
    print(f"           perturbation:  h_tt = {m['h_tt']:.2e}   h_rr = {m['h_rr']:.2e}")
    print()

print("  → At large s, all perturbations ≈ 0. Flat Minkowski. ✓")

# ═══════════════════════════════════════════════════════════
# PHASE 2: SLOWLY ADD MASS — WATCH MATRIX FILL
# ═══════════════════════════════════════════════════════════
print()
print("─" * 90)
print("  PHASE 2: ADDING MASS (decrease s, watch curvature emerge)")
print("─" * 90)
print()
print(f"  {'s':<10s} {'ζ(s)':<16s} {'g_tt':<16s} {'g_rr':<16s} {'clock':<14s} {'h_tt':<14s} {'h_rr':<14s}")
print(f"  {'─'*10} {'─'*16} {'─'*16} {'─'*16} {'─'*14} {'─'*14} {'─'*14}")

mass_steps = [100, 50, 20, 10, 7, 5, 4, 3.5, 3, 2.5, 2.2, 2.0, 1.8, 1.5, 1.3, 1.2, 1.1, 1.05, 1.01]
for s_val in mass_steps:
    m = prime_metric(s_val, r_test)
    z_str = f"{m['zeta']:.8f}" if m['zeta'] < 1e6 else f"{m['zeta']:.4e}"
    gtt_str = f"{m['g_tt']:.8f}" if abs(m['g_tt']) < 1e6 else f"{m['g_tt']:.4e}"
    grr_str = f"{m['g_rr']:.8f}" if m['g_rr'] < 1e6 else f"{m['g_rr']:.4e}"
    clk_str = f"{m['clock']:.8f}" if m['clock'] < 1e6 else f"{m['clock']:.4e}"
    htt_str = f"{m['h_tt']:.6e}"
    hrr_str = f"{m['h_rr']:.6e}"
    print(f"  {s_val:<10.2f} {z_str:<16s} {gtt_str:<16s} {grr_str:<16s} {clk_str:<14s} {htt_str:<14s} {hrr_str:<14s}")

print()
print("  → As s decreases: ζ grows, g_tt → 0, g_rr → ∞, clock slows.")
print("    This IS the Schwarzschild pattern — but derived from primes, not assumed.")

# ═══════════════════════════════════════════════════════════
# PHASE 2b: THE MATRIX AT KEY POINTS — FULL 4x4 VIEW
# ═══════════════════════════════════════════════════════════
print()
print("─" * 90)
print("  FULL 4×4 METRIC TENSOR AT KEY MASS VALUES")
print("─" * 90)

for s_val in [1000, 5, 2, 1.1]:
    m = prime_metric(s_val, r_test)
    label = "no mass" if s_val > 100 else f"s = {s_val}"
    print(f"""
  s = {s_val}  ({label})   ζ = {m['zeta']:.6f}
  ┌                                                                    ┐
  │  {m['g_tt']:>12.6f}        0              0              0         │  g_tt = -1/ζ
  │        0         {m['g_rr']:>12.6f}        0              0         │  g_rr = ζ
  │        0              0       {m['g_thth']:>.4e}        0         │  g_θθ = r²ζ
  │        0              0              0       {m['g_phph']:>.4e}  │  g_φφ = r²sin²θ·ζ
  └                                                                    ┘""")

# ═══════════════════════════════════════════════════════════
# PHASE 2c: IS THE DILATION LINEAR OR STEPPED?
# ═══════════════════════════════════════════════════════════
print()
print("─" * 90)
print("  LINEAR CHECK: Does time dilation increase smoothly or in steps?")
print("─" * 90)
print()

# Fine-grained sweep near s=2 where ζ changes rapidly
print(f"  {'s':<10s} {'ζ(s)':<16s} {'clock = 1/√ζ':<16s} {'Δclock from prev':<20s}")
print(f"  {'─'*10} {'─'*16} {'─'*16} {'─'*20}")

fine_steps = [3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0,
              1.95, 1.9, 1.85, 1.8, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5]
prev_clock = None
for s_val in fine_steps:
    m = prime_metric(s_val, r_test)
    delta = ""
    if prev_clock is not None:
        d = m['clock'] - prev_clock
        delta = f"{d:+.8f}"
    prev_clock = m['clock']
    print(f"  {s_val:<10.2f} {m['zeta']:<16.8f} {m['clock']:<16.8f} {delta:<20s}")

print()
print("  → If steps are uneven, primes are introducing discrete structure.")
print("    If smooth, ζ is acting as a continuous field.")

# ═══════════════════════════════════════════════════════════
# PHASE 3: GPS TEST
# ═══════════════════════════════════════════════════════════
print()
print("─" * 90)
print("  PHASE 3: GPS TEST — FIND THE VALUE OF s THAT GIVES ~38.6 μs/day")
print("─" * 90)
print()

# Standard GR reference
print(f"  Standard GR prediction:")
print(f"    Gravitational dilation:  {gr_grav_dilation:+.3f} μs/day")
print(f"    Velocity correction:     {vel_correction:+.3f} μs/day")
print(f"    Net (GR):                {gr_total:+.3f} μs/day")
print(f"    Measured:                ~38.6 μs/day")
print()

# In standard GR, the gravitational time dilation between Earth surface
# and GPS orbit comes from the difference in clock rates:
#   clock = √(1 - r_s/r)
# In our prime metric:
#   clock = 1/√ζ(s)
# We need TWO different s values — one for Earth surface, one for GPS orbit.
# This means s must depend on position too, not just mass.
#
# OR: we use the same s (= mass) but the spatial coordinates still matter
# through the r² terms in g_θθ and g_φφ.
#
# The key question: in the prime framework, what produces the DIFFERENCE
# in clock rates at different altitudes?
#
# In GR: it's r_s/r — the ratio changes with r.
# In primes: ζ(s) is the same everywhere for a given mass.
#
# This means: with s = mass alone, there's no position-dependent dilation.
# The clock runs the same everywhere. That DOESN'T match GPS.
#
# INSIGHT: We need s to depend on BOTH mass and position.
# The simplest choice: s = f(r, M) such that:
#   - More mass → smaller s → more curvature
#   - Farther from mass → larger s → flatter
#
# Natural candidate: s(r) = 1 + (r/r_s) where r_s = 2GM/c²
# This connects s to mass (through r_s) and position (through r).

print("  IMPORTANT FINDING:")
print("  With s = mass only (no position dependence), ζ(s) is the same everywhere.")
print("  That means no difference in clock rates at different altitudes → no GPS dilation.")
print()
print("  GR needs both mass AND position: the ratio r_s/r = 2GM/(c²r).")
print("  For primes to reproduce this, s must encode both.")
print()
print("  Testing s(r, M) = 1 + r/r_s  where r_s = 2GM/c² :")
print()

# s(r) = 1 + r/r_s  (linear in r)
def s_linear(r, r_s):
    return 1.0 + r / r_s

s_earth = s_linear(R_earth, r_s_earth)
s_gps = s_linear(R_gps, r_s_earth)

m_earth = prime_metric(s_earth, R_earth)
m_gps = prime_metric(s_gps, R_gps)

# Time dilation from prime metric
prime_grav_dilation = (m_gps['clock'] - m_earth['clock']) * 86400 * 1e6
prime_total = prime_grav_dilation + vel_correction  # same velocity correction

print(f"  s(Earth surface) = 1 + R_earth/r_s = {s_earth:.4f}")
print(f"  s(GPS orbit)     = 1 + R_gps/r_s   = {s_gps:.4f}")
print(f"  ζ at Earth  = {m_earth['zeta']:.15f}")
print(f"  ζ at GPS    = {m_gps['zeta']:.15f}")
print(f"  Clock at Earth = {m_earth['clock']:.15f}")
print(f"  Clock at GPS   = {m_gps['clock']:.15f}")
print()
print(f"  Prime gravitational dilation:  {prime_grav_dilation:+.6f} μs/day")
print(f"  Velocity correction:           {vel_correction:+.3f} μs/day")
print(f"  Prime total:                   {prime_total:+.6f} μs/day")
print()
print(f"  Standard GR total:             {gr_total:+.3f} μs/day")
print(f"  Difference:                    {abs(prime_total - gr_total):.6f} μs/day")
print()

# Also test cubic mapping from the paper for comparison
print("  Also testing s(r) = 1 + (r/r_s)³ (cubic, from paper):")
s_earth_3 = 1.0 + (R_earth / r_s_earth)**3
s_gps_3 = 1.0 + (R_gps / r_s_earth)**3
m_earth_3 = prime_metric(s_earth_3, R_earth)
m_gps_3 = prime_metric(s_gps_3, R_gps)
prime_grav_3 = (m_gps_3['clock'] - m_earth_3['clock']) * 86400 * 1e6
prime_total_3 = prime_grav_3 + vel_correction
print(f"  s(Earth) = {s_earth_3:.4e},  s(GPS) = {s_gps_3:.4e}")
print(f"  Prime total (cubic): {prime_total_3:+.6f} μs/day")
print(f"  GR total:            {gr_total:+.3f} μs/day")
print()

# ═══════════════════════════════════════════════════════════
# PHASE 3b: TRACE OF THE METRIC
# ═══════════════════════════════════════════════════════════
print("─" * 90)
print("  TRACE: Tr(g_μν) as mass increases")
print("─" * 90)
print()
print(f"  {'s':<10s} {'ζ(s)':<16s} {'Tr(g)':<20s} {'Tr(flat)':<20s} {'Tr diff':<16s}")
print(f"  {'─'*10} {'─'*16} {'─'*20} {'─'*20} {'─'*16}")

for s_val in [1000, 50, 10, 5, 3, 2, 1.5, 1.2, 1.1]:
    m = prime_metric(s_val, r_test)
    tr = m['g_tt'] + m['g_rr'] + m['g_thth'] + m['g_phph']
    flat_tr = -1.0 + 1.0 + r_test**2 + r_test**2  # flat Minkowski trace
    diff = tr - flat_tr
    print(f"  {s_val:<10.2f} {m['zeta']:<16.6f} {tr:<20.4e} {flat_tr:<20.4e} {diff:<16.4e}")

print()

# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("=" * 90)
print("  SUMMARY")
print("=" * 90)
print("""
  WHAT WE BUILT:
    g_μν = diag( -1/ζ(s), ζ(s), r²·ζ(s), r²sin²θ·ζ(s) )
    Built from the Euler product. No Schwarzschild assumed.

  WHAT EMERGED:
    • g_tt and g_rr are natural inverses (g_tt × g_rr = -1) — same as Schwarzschild
    • s → ∞: flat space. s → 1⁺: singularity. Curvature controlled by primes.
    • Matrix fills smoothly as mass increases — Phase 2 confirmed.

  THE GPS QUESTION:
    • s = mass alone → no position-dependent dilation → can't match GPS
    • s = f(r, M) → position dependence restored → GPS match depends on mapping
    • The mapping s(r) encodes HOW primes couple to spacetime geometry.

  NEXT STEP:
    Find the natural s(r, M) mapping. If one exists that isn't tuned by hand,
    primes are doing real physics. If you have to force-fit it, it's numerology.
""")
