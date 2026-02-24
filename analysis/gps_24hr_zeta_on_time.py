#!/usr/bin/env python3
"""
GPS 24-Hour Time Dilation: What if ζ modifies g_tt too?
========================================================
Experiment: Add the Euler product ζ(s) to the time component
and compare against standard GR.

Three methods:
  1. Standard GR:  g_tt = -(1 - r_s/r)
  2. β only:       clock = √(1 - β²)  [Paper 5 — identical to GR]
  3. ζ on time:    g_tt = -(1 - r_s/r) · ζ(s),  s = 1 + (r/r_s)³

Question: Does adding ζ to time break the GPS match?
"""

import math

# ═══════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11        # gravitational constant (m³/kg/s²)
c = 2.99792458e8       # speed of light (m/s)
M_earth = 5.9722e24    # Earth mass (kg)
R_earth = 6.3781e6     # Earth radius (m)
R_gps = 2.6571e7       # GPS orbit radius (m)
r_s = 2 * G * M_earth / c**2  # Schwarzschild radius of Earth
v_gps = math.sqrt(G * M_earth / R_gps)

# ═══════════════════════════════════════════════════════════
# ZETA FUNCTION (Euler product, truncated)
# ═══════════════════════════════════════════════════════════
def sieve_primes(n):
    """Simple sieve of Eratosthenes"""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

PRIMES = sieve_primes(10000)  # First ~1200 primes

def zeta_euler(s):
    """Compute ζ(s) via Euler product over primes"""
    if s <= 1.0:
        return float('inf')
    product = 1.0
    for p in PRIMES:
        term = 1.0 / (1.0 - p**(-s))
        product *= term
        # Convergence check
        if abs(term - 1.0) < 1e-15:
            break
    return product

def zeta_sum(s):
    """Compute ζ(s) via direct sum for verification"""
    if s <= 1.0:
        return float('inf')
    total = 0.0
    for n in range(1, 100001):
        total += n**(-s)
    return total

# ═══════════════════════════════════════════════════════════
# s(r) mapping
# ═══════════════════════════════════════════════════════════
def s_of_r(r):
    """s = 1 + (r/r_s)³ — cubic mapping (empirically constrained)"""
    return 1.0 + (r / r_s)**3

# ═══════════════════════════════════════════════════════════
# COMPUTE ζ VALUES AT KEY LOCATIONS
# ═══════════════════════════════════════════════════════════
s_earth = s_of_r(R_earth)
s_gps = s_of_r(R_gps)

zeta_earth = zeta_euler(s_earth)
zeta_gps = zeta_euler(s_gps)

# Also compute via sum for verification
zeta_earth_sum = zeta_sum(s_earth)
zeta_gps_sum = zeta_sum(s_gps)

# ═══════════════════════════════════════════════════════════
# METHOD 1: Standard GR
# ═══════════════════════════════════════════════════════════
grav_gr = (r_s / 2) * (1/R_earth - 1/R_gps)
vel_gr = -(v_gps**2) / (2 * c**2)
net_gr = grav_gr + vel_gr

# ═══════════════════════════════════════════════════════════
# METHOD 2: β (Paper 5 — no ζ)
# ═══════════════════════════════════════════════════════════
beta_earth = math.sqrt(r_s / R_earth)
beta_gps = math.sqrt(r_s / R_gps)
clock_earth_beta = math.sqrt(1 - beta_earth**2)
clock_gps_beta = math.sqrt(1 - beta_gps**2)
grav_beta = clock_gps_beta - clock_earth_beta
net_beta = grav_beta + vel_gr

# ═══════════════════════════════════════════════════════════
# METHOD 3: ζ on g_tt
# ═══════════════════════════════════════════════════════════
# g_tt = -(1 - r_s/r) · ζ(s)
# clock rate = √|g_tt| = √((1 - r_s/r) · ζ(s))
clock_earth_zeta = math.sqrt((1 - r_s/R_earth) * zeta_earth)
clock_gps_zeta = math.sqrt((1 - r_s/R_gps) * zeta_gps)
grav_zeta = clock_gps_zeta - clock_earth_zeta
net_zeta = grav_zeta + vel_gr

# ═══════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════
print("=" * 90)
print("  EXPERIMENT: WHAT IF ζ MODIFIES TIME TOO?")
print("=" * 90)
print()
print("  SETUP:")
print(f"    Earth Schwarzschild radius:  r_s = {r_s:.6e} m ({r_s*1000:.4f} mm)")
print(f"    Earth surface radius:        R   = {R_earth:.4e} m")
print(f"    GPS orbit radius:            R   = {R_gps:.4e} m")
print()
print(f"    s(Earth surface) = 1 + (R_earth/r_s)³ = {s_earth:.6e}")
print(f"    s(GPS orbit)     = 1 + (R_gps/r_s)³   = {s_gps:.6e}")
print()
print(f"    ζ(s) at Earth surface (Euler product): {zeta_earth:.15f}")
print(f"    ζ(s) at Earth surface (direct sum):    {zeta_earth_sum:.15f}")
print(f"    ζ(s) at GPS orbit (Euler product):     {zeta_gps:.15f}")
print(f"    ζ(s) at GPS orbit (direct sum):        {zeta_gps_sum:.15f}")
print()
print(f"    ζ deviation from 1.0 (Earth): {abs(zeta_earth - 1.0):.6e}")
print(f"    ζ deviation from 1.0 (GPS):   {abs(zeta_gps - 1.0):.6e}")
print()

print("=" * 90)
print("  24-HOUR COMPARISON: THREE METHODS")
print("=" * 90)
print()
print(f"  {'UTC Hour':<10s} {'Std GR (μs)':<16s} {'β only (μs)':<16s} {'ζ on time (μs)':<18s} {'GR vs ζ diff (μs)':<20s}")
print(f"  {'─'*10} {'─'*16} {'─'*16} {'─'*18} {'─'*20}")

for hour in range(25):
    t = hour * 3600.0
    d_gr = t * net_gr * 1e6
    d_beta = t * net_beta * 1e6
    d_zeta = t * net_zeta * 1e6
    diff = abs(d_gr - d_zeta)
    label = f"{hour:02d}:00"
    print(f"  {label:<10s} {d_gr:<+16.3f} {d_beta:<+16.3f} {d_zeta:<+18.3f} {diff:<20.9f}")

print()

# Final summary
total_gr = 86400.0 * net_gr * 1e6
total_beta = 86400.0 * net_beta * 1e6
total_zeta = 86400.0 * net_zeta * 1e6

print("=" * 90)
print("  SUMMARY")
print("=" * 90)
print()
print(f"  24-hour totals:")
print(f"    Standard GR:      {total_gr:+.6f} μs")
print(f"    β only (Paper 5): {total_beta:+.6f} μs")
print(f"    ζ on time:        {total_zeta:+.6f} μs")
print()
print(f"  Differences:")
print(f"    GR vs β:          {abs(total_gr - total_beta):.9f} μs  ({abs(total_gr - total_beta)/abs(total_gr)*100:.12f}%)")
print(f"    GR vs ζ-on-time:  {abs(total_gr - total_zeta):.9f} μs  ({abs(total_gr - total_zeta)/abs(total_gr)*100:.12f}%)")
print()
print(f"  Measured GPS correction: ~38.6 μs/day")
print()

# ═══════════════════════════════════════════════════════════
# EXTREME REGIME COMPARISON
# ═══════════════════════════════════════════════════════════
print("=" * 90)
print("  EXTREME REGIME: ζ ON TIME vs STANDARD GR")
print("  (What happens closer to a black hole?)")
print("=" * 90)
print()
print(f"  {'r/r_s':<12s} {'s(r)':<14s} {'ζ(s)':<16s} {'GR clock':<14s} {'ζ clock':<14s} {'Difference':<14s}")
print(f"  {'─'*12} {'─'*14} {'─'*16} {'─'*14} {'─'*14} {'─'*14}")

test_radii = [1000, 100, 10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05, 1.01]
for r_ratio in test_radii:
    r = r_ratio * r_s
    s = s_of_r(r)
    z = zeta_euler(s) if s > 1 else float('inf')
    
    gr_clock = math.sqrt(1 - r_s/r) if r > r_s else 0
    
    if s > 1 and r > r_s:
        zeta_clock = math.sqrt((1 - r_s/r) * z)
    else:
        zeta_clock = float('inf')
    
    diff_pct = abs(zeta_clock - gr_clock) / gr_clock * 100 if gr_clock > 0 else float('inf')
    
    z_str = f"{z:.6f}" if z < 1e6 else f"{z:.2e}"
    zc_str = f"{zeta_clock:.8f}" if zeta_clock < 1e6 else "∞"
    
    print(f"  {r_ratio:<12.2f} {s:<14.4f} {z_str:<16s} {gr_clock:<14.8f} {zc_str:<14s} {diff_pct:.6f}%")

print()
print("  KEY INSIGHT: At GPS distances, s is enormous → ζ ≈ 1 → no difference.")
print("  Near a black hole, s approaches 1 → ζ grows → time runs DIFFERENTLY than GR predicts.")
print("  The question: is that physical, or a sign ζ shouldn't touch time?")
print()
