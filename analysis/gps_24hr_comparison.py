#!/usr/bin/env python3
"""
GPS 24-Hour Time Dilation Comparison
=====================================
Method 1: Standard GR (Einstein's g_tt)
Method 2: Entropy Rate (β = √(r_s/r), no time dimension)

Generates hour-by-hour tables for a 24-hour UTC period showing:
- Earth surface clock time
- GPS satellite clock time  
- Time dilation amount (difference)

GPS satellite distance held constant at ~20,200 km altitude.
"""

import math

# ═══════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11        # gravitational constant (m³/kg/s²)
c = 2.99792458e8       # speed of light (m/s)
M_earth = 5.9722e24    # Earth mass (kg)
R_earth = 6.3781e6     # Earth radius (m)
R_gps = 2.6571e7       # GPS orbit radius (m) — ~20,200 km altitude
r_s = 2 * G * M_earth / c**2  # Schwarzschild radius of Earth (m)
v_gps = math.sqrt(G * M_earth / R_gps)  # GPS orbital velocity (m/s)

# ═══════════════════════════════════════════════════════════
# METHOD 1: STANDARD GR (g_tt)
# ═══════════════════════════════════════════════════════════
# Gravitational time dilation: clock rate = √(1 - r_s/r)
# Velocity time dilation: clock rate × √(1 - v²/c²)

# Fractional clock rate difference (satellite vs ground) per second
# Gravitational: satellite runs FASTER (higher altitude, weaker gravity)
grav_gr = (r_s / 2) * (1/R_earth - 1/R_gps)
# Velocity: satellite runs SLOWER (moving at orbital speed)  
vel_gr = -(v_gps**2) / (2 * c**2)
# Net fractional difference per second
net_gr = grav_gr + vel_gr

# ═══════════════════════════════════════════════════════════
# METHOD 2: ENTROPY RATE (β = √(r_s/r))
# ═══════════════════════════════════════════════════════════
# β = river velocity = escape velocity / c
# Clock rate = √(1 - β²) — derived purely from spatial geometry

beta_earth = math.sqrt(r_s / R_earth)
beta_gps = math.sqrt(r_s / R_gps)

clock_earth = math.sqrt(1 - beta_earth**2)
clock_gps = math.sqrt(1 - beta_gps**2)

# Gravitational part
grav_entropy = clock_gps - clock_earth
# Velocity correction (same as SR)
vel_entropy = -(v_gps**2) / (2 * c**2)
# Net
net_entropy = grav_entropy + vel_entropy

# ═══════════════════════════════════════════════════════════
# CONSTANTS SUMMARY
# ═══════════════════════════════════════════════════════════
print("=" * 80)
print("  GPS 24-HOUR TIME DILATION COMPARISON")
print("=" * 80)
print()
print("  CONSTANTS:")
print(f"    G  = {G} m³/(kg·s²)")
print(f"    c  = {c} m/s")
print(f"    M  = {M_earth} kg (Earth)")
print(f"    R_earth = {R_earth} m")
print(f"    R_gps   = {R_gps} m (altitude ≈ 20,200 km)")
print(f"    r_s     = {r_s:.6e} m (Earth Schwarzschild radius = {r_s*1000:.4f} mm)")
print(f"    v_gps   = {v_gps:.2f} m/s ({v_gps/1000:.3f} km/s)")
print(f"    β_earth = {beta_earth:.10e}")
print(f"    β_gps   = {beta_gps:.10e}")
print()
print(f"  GR net dilation rate:      {net_gr:+.6e} s/s")
print(f"  Entropy net dilation rate:  {net_entropy:+.6e} s/s")
print(f"  Difference between methods: {abs(net_gr - net_entropy):.6e} s/s")
print()

# ═══════════════════════════════════════════════════════════
# 24-HOUR TABLE — METHOD 1: STANDARD GR
# ═══════════════════════════════════════════════════════════
print("=" * 80)
print("  TABLE 1: STANDARD GR (Einstein's g_tt)")
print("  Satellite altitude: 20,200 km (constant)")
print("=" * 80)
print()
print(f"  {'UTC Hour':<12s} {'Earth Clock (s)':<20s} {'Satellite Clock (s)':<22s} {'Dilation (μs)':<16s}")
print(f"  {'─'*12} {'─'*20} {'─'*22} {'─'*16}")

gr_rows = []
for hour in range(25):  # 0 through 24
    earth_seconds = hour * 3600.0
    # Satellite accumulates extra time due to net dilation
    sat_seconds = earth_seconds * (1 + net_gr)
    dilation_us = (sat_seconds - earth_seconds) * 1e6
    
    label = f"{hour:02d}:00 UTC"
    gr_rows.append((label, earth_seconds, sat_seconds, dilation_us))
    print(f"  {label:<12s} {earth_seconds:<20.3f} {sat_seconds:<22.9f} {dilation_us:<+16.3f}")

print()
print(f"  24-hour total dilation: {gr_rows[-1][3]:+.3f} μs")
print()

# ═══════════════════════════════════════════════════════════
# 24-HOUR TABLE — METHOD 2: ENTROPY RATE
# ═══════════════════════════════════════════════════════════
print("=" * 80)
print("  TABLE 2: ENTROPY RATE (β = √(r_s/r), no time dimension)")  
print("  Satellite altitude: 20,200 km (constant)")
print("=" * 80)
print()
print(f"  {'UTC Hour':<12s} {'Earth Clock (s)':<20s} {'Satellite Clock (s)':<22s} {'Dilation (μs)':<16s}")
print(f"  {'─'*12} {'─'*20} {'─'*22} {'─'*16}")

ent_rows = []
for hour in range(25):
    earth_seconds = hour * 3600.0
    sat_seconds = earth_seconds * (1 + net_entropy)
    dilation_us = (sat_seconds - earth_seconds) * 1e6
    
    label = f"{hour:02d}:00 UTC"
    ent_rows.append((label, earth_seconds, sat_seconds, dilation_us))
    print(f"  {label:<12s} {earth_seconds:<20.3f} {sat_seconds:<22.9f} {dilation_us:<+16.3f}")

print()
print(f"  24-hour total dilation: {ent_rows[-1][3]:+.3f} μs")
print()

# ═══════════════════════════════════════════════════════════
# COMPARISON TABLE
# ═══════════════════════════════════════════════════════════
print("=" * 80)
print("  TABLE 3: COMPARISON — GR vs ENTROPY RATE")
print("=" * 80)
print()
print(f"  {'UTC Hour':<12s} {'GR Dilation (μs)':<20s} {'Entropy Dilation (μs)':<24s} {'Difference (μs)':<18s}")
print(f"  {'─'*12} {'─'*20} {'─'*24} {'─'*18}")

for i in range(25):
    label = gr_rows[i][0]
    gr_d = gr_rows[i][3]
    ent_d = ent_rows[i][3]
    diff = abs(gr_d - ent_d)
    print(f"  {label:<12s} {gr_d:<+20.3f} {ent_d:<+24.3f} {diff:<18.6f}")

print()
total_diff = abs(gr_rows[-1][3] - ent_rows[-1][3])
print(f"  24-hour GR total:       {gr_rows[-1][3]:+.3f} μs")
print(f"  24-hour Entropy total:  {ent_rows[-1][3]:+.3f} μs")
print(f"  24-hour difference:     {total_diff:.6f} μs")
print(f"  Percent deviation:      {total_diff/abs(gr_rows[-1][3])*100:.10f}%")
print()
print(f"  Measured GPS correction: ~38.6 μs/day")
print()

# ═══════════════════════════════════════════════════════════
# EQUATIONS USED
# ═══════════════════════════════════════════════════════════
print("=" * 80)
print("  EQUATIONS")
print("=" * 80)
print("""
  METHOD 1 — Standard GR:
    Gravitational: Δτ/τ = (r_s/2)(1/R_earth - 1/R_gps)
    Velocity:      Δτ/τ = -v²/(2c²)
    Clock rate:    √(1 - r_s/r) × √(1 - v²/c²)

  METHOD 2 — Entropy Rate:
    β = √(r_s/r)            (river velocity, from spatial geometry)
    Clock rate = √(1 - β²)  (no g_tt needed)
    Velocity:   Δτ/τ = -v²/(2c²)  (same as SR)
    
  Both methods use:
    r_s = 2GM/c²
    v_gps = √(GM/R_gps)
""")
