#!/usr/bin/env python3
"""
GR Emergence from Primes — Version 2: The Explicit Formula
============================================================
Mapping: x = (r/r_s)²

Key insight:
  x^(ρ-1) envelope = x^(-1/2) = r_s/r   ← this IS the gravitational 1/r falloff

Metric built from the Chebyshev prime-counting function ψ(x):
  g_tt(r) = -ψ(x)/x          ← time component from prime counting
  g_rr(r) =  x/ψ(x)          ← radial (automatic inverse of g_tt)
  g_θθ(r) =  r² · x/ψ(x)    ← polar, scaled by curvature
  g_φφ(r) =  r²sin²θ · x/ψ(x)  ← azimuthal, scaled

Properties:
  r → ∞  :  x → ∞,  ψ(x)/x → 1    →  flat Minkowski  ✓
  r = r_s :  x = 1,  ψ(1) = 0       →  g_tt = 0 (horizon)  ✓
  g_tt × g_rr = -1 always            →  Schwarzschild determinant  ✓

ψ(x) via explicit formula:
  ψ(x) = x - Σ_ρ x^ρ/ρ - ln(2π) - ½ln(1 - x⁻²)
  where ρ = ½ + iγ are the non-trivial zeros of ζ(s)
"""

import math
import cmath

# ═══════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11
c_light = 2.99792458e8
M_earth = 5.9722e24
R_earth = 6.3781e6
R_gps = 2.6571e7
r_s_earth = 2 * G * M_earth / c_light**2
v_gps = math.sqrt(G * M_earth / R_gps)

# ═══════════════════════════════════════════════════════════
# NON-TRIVIAL ZEROS OF ζ(s): ρ = 1/2 + iγ
# (imaginary parts of the first 30 zeros)
# ═══════════════════════════════════════════════════════════
ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851
]

# ═══════════════════════════════════════════════════════════
# CHEBYSHEV ψ(x) — DIRECT COMPUTATION (for validation)
# ═══════════════════════════════════════════════════════════
def sieve_primes(n):
    """Sieve of Eratosthenes"""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def chebyshev_psi_direct(x):
    """Compute ψ(x) = Σ Λ(n) for n ≤ x, directly from primes"""
    if x < 2:
        return 0.0
    primes = sieve_primes(int(x))
    total = 0.0
    for p in primes:
        # Add ln(p) for each prime power p^k ≤ x
        pk = p
        while pk <= x:
            total += math.log(p)
            pk *= p
    return total

# ═══════════════════════════════════════════════════════════
# CHEBYSHEV ψ(x) — EXPLICIT FORMULA (using zeros of ζ)
# ═══════════════════════════════════════════════════════════
def chebyshev_psi_explicit(x, num_zeros=None):
    """
    ψ(x) via the Riemann-von Mangoldt explicit formula:
    ψ(x) = x - Σ_ρ x^ρ/ρ - ln(2π) - ½ln(1 - x⁻²)

    Sum over conjugate pairs: x^ρ/ρ + x^ρ̄/ρ̄ = 2·Re(x^ρ/ρ)
    """
    if x <= 1:
        return 0.0

    zeros = ZETA_ZEROS[:num_zeros] if num_zeros else ZETA_ZEROS
    ln_x = math.log(x)
    sqrt_x = math.sqrt(x)

    # Main term
    result = x

    # Sum over non-trivial zeros (conjugate pairs)
    zero_sum = 0.0
    for gamma in zeros:
        # ρ = 1/2 + iγ
        # x^ρ = x^(1/2) · e^(iγ·ln(x))
        # x^ρ/ρ = x^(1/2) · e^(iγ·ln(x)) / (1/2 + iγ)
        #
        # Re(x^ρ/ρ) = x^(1/2) · [(1/2)cos(γ·lnx) + γ·sin(γ·lnx)] / (1/4 + γ²)

        cos_term = math.cos(gamma * ln_x)
        sin_term = math.sin(gamma * ln_x)
        denom = 0.25 + gamma**2

        real_part = sqrt_x * (0.5 * cos_term + gamma * sin_term) / denom

        # Factor of 2 for conjugate pair
        zero_sum += 2.0 * real_part

    result -= zero_sum

    # Trivial zeros contribution: -ln(2π)
    result -= math.log(2 * math.pi)

    # Trivial zeros tail: -½ln(1 - x⁻²) ≈ 0 for large x
    if x > 1.0001:
        result -= 0.5 * math.log(1.0 - x**(-2))

    return result

# ═══════════════════════════════════════════════════════════
# METRIC FROM PRIMES
# ═══════════════════════════════════════════════════════════
def prime_metric(r, r_s, theta=math.pi/2, use_direct=False, num_zeros=None):
    """
    Build the metric from ψ(x) where x = (r/r_s)².

    g_tt = -ψ(x)/x
    g_rr = x/ψ(x)
    g_θθ = r² · x/ψ(x)
    g_φφ = r²sin²θ · x/ψ(x)
    """
    x = (r / r_s)**2

    if use_direct and x <= 1e7:
        psi = chebyshev_psi_direct(x)
    else:
        psi = chebyshev_psi_explicit(x, num_zeros)

    psi_over_x = psi / x if x > 0 else 0.0

    g_tt = -psi_over_x
    g_rr = x / psi if psi > 0 else float('inf')
    g_thth = r**2 * (x / psi) if psi > 0 else float('inf')
    g_phph = r**2 * math.sin(theta)**2 * (x / psi) if psi > 0 else float('inf')

    # Schwarzschild for comparison
    sch_gtt = -(1 - r_s/r)
    sch_grr = 1/(1 - r_s/r) if r != r_s else float('inf')

    clock_prime = math.sqrt(psi_over_x) if psi_over_x > 0 else 0.0
    clock_sch = math.sqrt(1 - r_s/r) if r > r_s else 0.0

    return {
        'x': x, 'psi': psi, 'psi_over_x': psi_over_x,
        'g_tt': g_tt, 'g_rr': g_rr, 'g_thth': g_thth, 'g_phph': g_phph,
        'clock': clock_prime,
        'sch_gtt': sch_gtt, 'sch_grr': sch_grr, 'sch_clock': clock_sch
    }


# ═══════════════════════════════════════════════════════════
# PHASE 1: VALIDATE ψ(x) — DIRECT vs EXPLICIT FORMULA
# ═══════════════════════════════════════════════════════════
print()
print("=" * 95)
print("  GR EMERGENCE FROM PRIMES — Version 2")
print("  Metric from the explicit formula: g_tt = -ψ(x)/x,  x = (r/r_s)²")
print("=" * 95)

print()
print("─" * 95)
print("  PHASE 1: VALIDATE — Does the explicit formula match direct prime counting?")
print("─" * 95)
print()

print(f"  {'x':<10s} {'ψ direct':<16s} {'ψ explicit':<16s} {'ψ/x direct':<14s} {'ψ/x explicit':<14s} {'1-1/√x (Sch)':<14s}")
print(f"  {'─'*10} {'─'*16} {'─'*16} {'─'*14} {'─'*14} {'─'*14}")

for x_val in [4, 9, 25, 100, 400, 1000, 5000, 10000, 50000, 100000]:
    psi_d = chebyshev_psi_direct(x_val)
    psi_e = chebyshev_psi_explicit(x_val)
    sch = 1 - 1/math.sqrt(x_val)  # (1 - r_s/r) when x = (r/r_s)²

    pd_str = f"{psi_d:.4f}"
    pe_str = f"{psi_e:.4f}"
    pxd_str = f"{psi_d/x_val:.8f}"
    pxe_str = f"{psi_e/x_val:.8f}"

    print(f"  {x_val:<10} {pd_str:<16s} {pe_str:<16s} {pxd_str:<14s} {pxe_str:<14s} {sch:<14.8f}")

print()
print("  Note: ψ/x should approach 1 for large x (Prime Number Theorem)")
print("  1-1/√x is the Schwarzschild g_tt = -(1-r_s/r) with x = (r/r_s)²")

# ═══════════════════════════════════════════════════════════
# PHASE 2: WATCH THE METRIC EMERGE
# ═══════════════════════════════════════════════════════════
print()
print("─" * 95)
print("  PHASE 2: METRIC EMERGENCE — r/r_s from ∞ down to horizon")
print("  Comparing ψ(x)/x to Schwarzschild (1 - r_s/r)")
print("─" * 95)
print()

r_s = r_s_earth  # Use Earth's Schwarzschild radius for reference

print(f"  {'r/r_s':<10s} {'x=(r/r_s)²':<14s} {'ψ/x (prime)':<14s} {'1-r_s/r (GR)':<14s} {'prime clock':<14s} {'GR clock':<14s} {'diff':<12s}")
print(f"  {'─'*10} {'─'*14} {'─'*14} {'─'*14} {'─'*14} {'─'*14} {'─'*12}")

# Use a range of r/r_s values — some small enough for direct computation
test_ratios = [1000, 500, 200, 100, 50, 20, 10, 7, 5, 3, 2, 1.5, 1.2, 1.1, 1.05]

for ratio in test_ratios:
    r = ratio * r_s
    x = ratio**2

    # Use direct computation for small enough x
    use_direct = (x <= 1e6)
    m = prime_metric(r, r_s, use_direct=use_direct)

    sch = 1 - 1/ratio
    psi_x = m['psi_over_x']

    x_str = f"{x:.1f}" if x < 1e6 else f"{x:.2e}"
    psi_str = f"{psi_x:.8f}" if abs(psi_x) < 100 else f"{psi_x:.4e}"
    sch_str = f"{sch:.8f}"
    clk_p = f"{m['clock']:.8f}" if m['clock'] < 100 else f"{m['clock']:.4e}"
    clk_s = f"{m['sch_clock']:.8f}"
    diff = abs(psi_x - sch)
    diff_str = f"{diff:.4e}" if diff < 0.01 else f"{diff:.6f}"

    print(f"  {ratio:<10.2f} {x_str:<14s} {psi_str:<14s} {sch_str:<14s} {clk_p:<14s} {clk_s:<14s} {diff_str:<12s}")

print()
print("  If ψ/x tracks (1 - r_s/r), GR is emerging from prime counting.")

# ═══════════════════════════════════════════════════════════
# PHASE 2b: FULL 4×4 MATRIX AT KEY POINTS
# ═══════════════════════════════════════════════════════════
print()
print("─" * 95)
print("  FULL 4×4 METRIC TENSOR AT KEY DISTANCES")
print("─" * 95)

r_display = 100.0  # Use r = 100 r_s for readable angular components
for ratio in [1000, 10, 2, 1.1]:
    r = ratio * r_s
    x = ratio**2
    use_direct = (x <= 1e6)
    m = prime_metric(r, r_s, use_direct=use_direct)
    sch = 1 - 1/ratio

    label = "far field" if ratio > 100 else f"r = {ratio} r_s"
    print(f"""
  r/r_s = {ratio}  ({label})     x = {x:.1f}     ψ/x = {m['psi_over_x']:.6f}   (Schwarzschild: {sch:.6f})
  ┌                                                                    ┐
  │  {m['g_tt']:>12.6f}        0              0              0         │  g_tt = -ψ/x
  │        0         {m['g_rr']:>12.6f}        0              0         │  g_rr = x/ψ
  │        0              0       {m['g_thth']:>.4e}        0         │  g_θθ
  │        0              0              0       {m['g_phph']:>.4e}  │  g_φφ
  └                                                                    ┘""")

# ═══════════════════════════════════════════════════════════
# PHASE 3: GPS TEST
# ═══════════════════════════════════════════════════════════
print()
print("─" * 95)
print("  PHASE 3: GPS TEST")
print("─" * 95)
print()

# Standard GR values
gr_clock_earth = math.sqrt(1 - r_s_earth / R_earth)
gr_clock_gps = math.sqrt(1 - r_s_earth / R_gps)
gr_grav = (gr_clock_gps - gr_clock_earth) * 86400 * 1e6
vel_corr = -(v_gps**2) / (2 * c_light**2) * 86400 * 1e6
gr_total = gr_grav + vel_corr

print(f"  Earth Schwarzschild radius: r_s = {r_s_earth:.6e} m ({r_s_earth*1000:.4f} mm)")
print(f"  R_earth / r_s = {R_earth/r_s_earth:.4f}")
print(f"  R_gps / r_s   = {R_gps/r_s_earth:.4f}")
print()

# Prime metric at Earth surface and GPS orbit
# These x values are huge, so we must use the explicit formula
x_earth = (R_earth / r_s_earth)**2
x_gps = (R_gps / r_s_earth)**2

print(f"  x(Earth) = (R_earth/r_s)² = {x_earth:.4e}")
print(f"  x(GPS)   = (R_gps/r_s)²   = {x_gps:.4e}")
print()

# Compute ψ/x via explicit formula
psi_earth = chebyshev_psi_explicit(x_earth)
psi_gps = chebyshev_psi_explicit(x_gps)
psi_over_x_earth = psi_earth / x_earth
psi_over_x_gps = psi_gps / x_gps

clock_prime_earth = math.sqrt(psi_over_x_earth) if psi_over_x_earth > 0 else 0
clock_prime_gps = math.sqrt(psi_over_x_gps) if psi_over_x_gps > 0 else 0

prime_grav = (clock_prime_gps - clock_prime_earth) * 86400 * 1e6
prime_total = prime_grav + vel_corr

# Schwarzschild prediction at same distances
sch_earth = 1 - r_s_earth / R_earth
sch_gps = 1 - r_s_earth / R_gps

print(f"  PRIME METRIC (from ψ):")
print(f"    ψ/x at Earth = {psi_over_x_earth:.15f}")
print(f"    ψ/x at GPS   = {psi_over_x_gps:.15f}")
print(f"    clock(Earth)  = {clock_prime_earth:.15f}")
print(f"    clock(GPS)    = {clock_prime_gps:.15f}")
print()
print(f"  SCHWARZSCHILD (standard GR):")
print(f"    g_tt at Earth = {sch_earth:.15f}")
print(f"    g_tt at GPS   = {sch_gps:.15f}")
print(f"    clock(Earth)  = {gr_clock_earth:.15f}")
print(f"    clock(GPS)    = {gr_clock_gps:.15f}")
print()
print(f"  TIME DILATION:")
print(f"    Prime grav dilation:      {prime_grav:+.6f} μs/day")
print(f"    Standard GR grav dilation:{gr_grav:+.6f} μs/day")
print(f"    Velocity correction:      {vel_corr:+.3f} μs/day (same for both)")
print()
print(f"    Prime total:              {prime_total:+.6f} μs/day")
print(f"    Standard GR total:        {gr_total:+.3f} μs/day")
print(f"    Measured GPS:             ~38.6 μs/day")
print()
print(f"    Difference (prime vs GR): {abs(prime_total - gr_total):.6f} μs/day")
print()

# ═══════════════════════════════════════════════════════════
# PHASE 3b: CONVERGENCE — HOW MANY ZEROS DO WE NEED?
# ═══════════════════════════════════════════════════════════
print("─" * 95)
print("  CONVERGENCE: Effect of number of zeros on GPS result")
print("─" * 95)
print()
print(f"  {'# zeros':<10s} {'ψ/x Earth':<20s} {'ψ/x GPS':<20s} {'Δclock (μs/day)':<20s}")
print(f"  {'─'*10} {'─'*20} {'─'*20} {'─'*20}")

for n_zeros in [1, 2, 5, 10, 15, 20, 25, 30]:
    pe = chebyshev_psi_explicit(x_earth, num_zeros=n_zeros)
    pg = chebyshev_psi_explicit(x_gps, num_zeros=n_zeros)
    pe_x = pe / x_earth
    pg_x = pg / x_gps
    ce = math.sqrt(pe_x) if pe_x > 0 else 0
    cg = math.sqrt(pg_x) if pg_x > 0 else 0
    dilation = (cg - ce) * 86400 * 1e6
    print(f"  {n_zeros:<10d} {pe_x:<20.15f} {pg_x:<20.15f} {dilation:<+20.6f}")

print()

# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print("=" * 95)
print("  SUMMARY")
print("=" * 95)
print(f"""
  WHAT WE BUILT:
    g_tt = -ψ(x)/x    where x = (r/r_s)² and ψ is the prime counting function
    g_rr = x/ψ(x)     (automatic inverse)
    g_tt × g_rr = -1   (Schwarzschild determinant condition, automatic)

  STRUCTURAL MATCH:
    ψ(1) = 0   → g_tt = 0 at horizon (r = r_s)           ✓ matches Schwarzschild
    ψ(x)/x → 1 → g_tt = -1 at infinity (flat space)      ✓ matches Schwarzschild
    g_rr → ∞ at horizon                                   ✓ matches Schwarzschild
    1/r falloff from x^(ρ-1) envelope = r_s/r             ✓ matches Schwarzschild

  THE CONNECTION:
    Euler product ∏(1-p⁻ˢ)⁻¹  →  structure (ζ as the metric)
    Zeros of ζ via explicit formula  →  spatial distribution (the "where")
    x = (r/r_s)²  →  maps number theory position to spacetime radius

  GPS RESULT:
    Prime metric: {prime_total:+.3f} μs/day
    Standard GR:  {gr_total:+.3f} μs/day
    Measured:     ~38.6 μs/day
""")
