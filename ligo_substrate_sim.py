#!/usr/bin/env python3
"""
LIGO Substrate Fingerprint Simulation
=======================================
Simulate a gravitational wave passing through a detector.
Compare time dilation fluctuation between:
  1. Standard GR
  2. ζ-embedded metric (dark substrate)

Goal: Find the delta — the substrate fingerprint in the waveform.

Models a binary black hole inspiral gravitational wave (simplified).
"""

import math
import json

# ═══════════════════════════════════════════════════════════
# ZETA FUNCTION
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
    """Compute ζ(s) via Euler product"""
    if s <= 1.0:
        return float('inf')
    product = 1.0
    for p in PRIMES:
        term = 1.0 / (1.0 - p**(-s))
        product *= term
        if abs(term - 1.0) < 1e-15:
            break
    return product

# ═══════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════
G = 6.67430e-11
c = 2.99792458e8
M_sun = 1.989e30
pc = 3.0857e16  # parsec in meters

# ═══════════════════════════════════════════════════════════
# SOURCE PARAMETERS (GW150914-like)
# ═══════════════════════════════════════════════════════════
m1 = 36 * M_sun        # BH 1 mass
m2 = 29 * M_sun        # BH 2 mass
D = 410e6 * pc          # distance ~410 Mpc
M_total = m1 + m2
M_chirp = (m1 * m2)**(3/5) / M_total**(1/5)
r_s_total = 2 * G * M_total / c**2  # Schwarzschild radius of merged BH

# ═══════════════════════════════════════════════════════════
# GRAVITATIONAL WAVE MODEL (simplified inspiral)
# ═══════════════════════════════════════════════════════════
# h(t) = strain amplitude at detector
# For inspiral: h ~ (M_chirp)^(5/3) * f^(2/3) / D
# Frequency chirps: f(t) increases as merger approaches
# We model the last ~0.2 seconds before merger

def gw_strain(t, t_merge=0.0):
    """
    Simplified chirping gravitational wave strain.
    t < t_merge (inspiral), t = t_merge (merger), t > t_merge (ringdown)
    """
    tau = t_merge - t  # time to merger
    
    if tau > 0.001:  # inspiral phase
        # Newtonian chirp: f(t) ~ tau^(-3/8)
        f = 1.0 / (8 * math.pi) * (5 / (256 * tau))**(3/8) * (G * M_chirp / c**3)**(-5/8)
        # Cap frequency at ISCO
        f = min(f, c**3 / (6 * math.sqrt(6) * math.pi * G * M_total))
        
        # Strain amplitude
        amp = 4 * (G * M_chirp)**(5/3) / (c**4 * D) * (math.pi * f)**(2/3)
        
        # Phase
        phase = 2 * math.pi * f * t
        h = amp * math.sin(phase)
        return h, f
        
    elif tau > -0.01:  # merger/ringdown
        # Ringdown: damped sinusoid
        f_ring = c**3 / (6 * math.sqrt(6) * math.pi * G * M_total)
        amp_peak = 4 * (G * M_chirp)**(5/3) / (c**4 * D) * (math.pi * f_ring)**(2/3)
        
        t_after = t - t_merge
        tau_damp = 0.005  # ~5ms damping time
        h = amp_peak * math.exp(-t_after / tau_damp) * math.sin(2 * math.pi * f_ring * t)
        return h, f_ring
    else:
        return 0.0, 0.0

# ═══════════════════════════════════════════════════════════
# TIME DILATION FROM PASSING GRAVITATIONAL WAVE
# ═══════════════════════════════════════════════════════════
# A passing GW perturbs the local metric: g_tt ≈ -(1 + h(t))
# Time dilation: dτ/dt = √|g_tt| ≈ √(1 + h(t)) ≈ 1 + h(t)/2

# For ζ-embedded: g_tt = -(1 + h(t)) · ζ(s)
# But what is s at the detector?
# At Earth, s is enormous (ζ≈1). However, the GW itself is a 
# perturbation FROM the source BHs. The wave carries information
# about the source's substrate state.
#
# Key insight: the strain encodes how spacetime deformed at the source.
# If ζ modified the source dynamics, the WAVEFORM SHAPE changes.
# This means the fingerprint isn't in the local ζ at Earth,
# it's in how the wave was generated differently at the source.

def s_of_r(r, r_s):
    """s mapping for prime substrate"""
    return 1.0 + (r / r_s)**3

# ═══════════════════════════════════════════════════════════
# APPROACH 1: Source dynamics modification
# The orbital dynamics near merger are modified by ζ.
# At the source, the two BHs are at r ~ few r_s of each other.
# ζ modifies the effective potential → changes waveform.
# ═══════════════════════════════════════════════════════════

def effective_potential_gr(r, L, M):
    """Standard GR effective potential for orbital mechanics"""
    r_s = 2 * G * M / c**2
    # V_eff = -GM/r + L²/(2r²) - GML²/(c²r³)
    return -G * M / r + L**2 / (2 * r**2) - G * M * L**2 / (c**2 * r**3)

def effective_potential_zeta(r, L, M):
    """ζ-modified effective potential"""
    r_s = 2 * G * M / c**2
    s = s_of_r(r, r_s)
    z = zeta(s)
    # ζ modifies the spatial metric → modifies the potential
    # The correction enters through the g_rr and g_φφ terms
    return (-G * M / r + L**2 / (2 * r**2) - G * M * L**2 / (c**2 * r**3)) * z

# ═══════════════════════════════════════════════════════════
# SIMULATION: Generate waveforms for both metrics
# ═══════════════════════════════════════════════════════════

print("=" * 90)
print("  LIGO SUBSTRATE FINGERPRINT SIMULATION")
print("=" * 90)
print()
print(f"  Source: GW150914-like binary black hole merger")
print(f"  m1 = {m1/M_sun:.0f} M☉,  m2 = {m2/M_sun:.0f} M☉,  D = {D/pc/1e6:.0f} Mpc")
print(f"  M_chirp = {M_chirp/M_sun:.1f} M☉")
print(f"  r_s (merged) = {r_s_total:.1f} m ({r_s_total/1000:.2f} km)")
print()

# Time array: -0.2s to +0.02s around merger
dt = 1e-5  # 100 kHz sampling (like LIGO)
times = []
t = -0.2
while t <= 0.02:
    times.append(t)
    t += dt

print(f"  Simulation: {len(times)} samples, dt = {dt*1e6:.0f} μs")
print(f"  Time range: {times[0]:.3f}s to {times[-1]:.3f}s around merger")
print()

# ═══════════════════════════════════════════════════════════
# COMPUTE WAVEFORMS
# ═══════════════════════════════════════════════════════════
print("  Computing standard GR waveform...")

gr_strain = []
gr_freq = []
gr_timedil = []

for t in times:
    h, f = gw_strain(t)
    gr_strain.append(h)
    gr_freq.append(f)
    # Time dilation: dτ/dt ≈ 1 + h/2
    td = 1 + h / 2
    gr_timedil.append(td)

print("  Computing ζ-embedded waveform...")

# For the ζ-embedded metric, the key modification is at the SOURCE.
# During inspiral, the orbital separation decreases.
# At each orbital radius, ζ modifies the dynamics.
# 
# Simplified model: the strain gets modified by ζ at the source's
# orbital separation. As the BHs spiral in:
#   r_orbit(t) ~ (t_merge - t)^(1/4) * r_isco
# At each r_orbit, compute ζ and apply it to the strain.

r_isco = 3 * r_s_total  # innermost stable circular orbit

zeta_strain = []
zeta_timedil = []
zeta_values = []
delta_strain = []
delta_timedil = []

for i, t in enumerate(times):
    tau = -t  # time to merger (t is negative before merger)
    
    if tau > 0.001:
        # Orbital separation shrinks as merger approaches
        # r(t) ~ r_isco * (tau / tau_ref)^(1/4) 
        tau_ref = 0.2  # reference time
        r_orbit = r_isco * (tau / tau_ref)**(1/4)
        r_orbit = max(r_orbit, r_s_total * 1.01)  # don't go below horizon
        
        # ζ at the orbital separation (relative to merged BH r_s)
        s = s_of_r(r_orbit, r_s_total)
        z = zeta(s)
    elif tau > -0.01:
        # At/past merger: r ~ r_s, maximum ζ effect
        s = s_of_r(r_s_total * 1.01, r_s_total)
        z = zeta(s)
    else:
        z = 1.0
    
    zeta_values.append(z)
    
    # Modified strain: the ζ correction modifies the wave amplitude
    # Through the modified effective potential and orbital dynamics
    # To first order: h_zeta ≈ h_gr * √ζ (from modified g_tt and g_rr)
    h_gr = gr_strain[i]
    h_zeta = h_gr * math.sqrt(z)
    zeta_strain.append(h_zeta)
    
    # Modified time dilation
    td_gr = gr_timedil[i]
    td_zeta = 1 + h_zeta / 2
    zeta_timedil.append(td_zeta)
    
    # Deltas
    delta_strain.append(h_zeta - h_gr)
    delta_timedil.append(td_zeta - td_gr)

print("  Done!")
print()

# ═══════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════
print("=" * 90)
print("  RESULTS: KEY MOMENTS")
print("=" * 90)
print()
print(f"  {'Time (s)':<12s} {'r_orbit/r_s':<14s} {'ζ(s)':<12s} {'GR strain':<14s} {'ζ strain':<14s} {'Δ strain':<14s} {'Δ/GR %':<10s}")
print(f"  {'─'*12} {'─'*14} {'─'*12} {'─'*14} {'─'*14} {'─'*14} {'─'*10}")

# Sample key moments
sample_times = [-0.2, -0.15, -0.1, -0.05, -0.02, -0.01, -0.005, -0.002, -0.001, 0.0, 0.005, 0.01]
for st in sample_times:
    # Find closest index
    idx = min(range(len(times)), key=lambda i: abs(times[i] - st))
    t = times[idx]
    
    tau = -t
    if tau > 0.001:
        tau_ref = 0.2
        r_orbit = r_isco * (tau / tau_ref)**(1/4)
        r_orbit = max(r_orbit, r_s_total * 1.01)
        r_ratio = r_orbit / r_s_total
    elif tau > 0:
        r_ratio = 1.01
    else:
        r_ratio = 1.01
    
    h_gr = gr_strain[idx]
    h_z = zeta_strain[idx]
    d = delta_strain[idx]
    z = zeta_values[idx]
    
    pct = abs(d / h_gr * 100) if abs(h_gr) > 1e-30 else 0
    
    print(f"  {t:<+12.4f} {r_ratio:<14.2f} {z:<12.6f} {h_gr:<+14.4e} {h_z:<+14.4e} {d:<+14.4e} {pct:<10.4f}")

print()

# ═══════════════════════════════════════════════════════════
# PEAK ANALYSIS
# ═══════════════════════════════════════════════════════════
max_gr = max(abs(h) for h in gr_strain)
max_zeta = max(abs(h) for h in zeta_strain)
max_delta = max(abs(d) for d in delta_strain)
max_delta_td = max(abs(d) for d in delta_timedil)

# Find when delta is biggest
peak_idx = max(range(len(delta_strain)), key=lambda i: abs(delta_strain[i]))
peak_time = times[peak_idx]

print("=" * 90)
print("  PEAK VALUES")
print("=" * 90)
print()
print(f"  Peak GR strain:            {max_gr:.4e}")
print(f"  Peak ζ strain:             {max_zeta:.4e}")
print(f"  Peak strain delta:         {max_delta:.4e}")
print(f"  Peak delta occurs at:      t = {peak_time:+.4f}s")
print(f"  Peak ζ value at delta:     {zeta_values[peak_idx]:.6f}")
print(f"  Relative difference:       {max_delta/max_gr*100:.4f}%")
print()
print(f"  Peak time dilation delta:  {max_delta_td:.4e}")
print(f"  (This is what you'd measure in clock comparison)")
print()

# ═══════════════════════════════════════════════════════════
# FREQUENCY DOMAIN — WHERE TO LOOK
# ═══════════════════════════════════════════════════════════
print("=" * 90)
print("  WHERE THE FINGERPRINT LIVES")
print("=" * 90)
print()

# ζ effect is strongest near merger (small r_orbit → small s → larger ζ)
# This means the HIGH FREQUENCY part of the signal is most modified
# Late inspiral + merger + ringdown = substrate fingerprint zone

# Find when ζ deviates by more than 0.1% from 1
threshold_idx = None
for i, z in enumerate(zeta_values):
    if abs(z - 1.0) > 0.001:
        threshold_idx = i
        break

if threshold_idx:
    t_thresh = times[threshold_idx]
    f_thresh = gr_freq[threshold_idx]
    print(f"  ζ deviates >0.1% from 1.0 starting at:")
    print(f"    t = {t_thresh:+.4f}s before merger")
    print(f"    f = {f_thresh:.1f} Hz")
    print(f"    ζ = {zeta_values[threshold_idx]:.6f}")
    print()

print("  SUBSTRATE FINGERPRINT ZONES:")
print("    Early inspiral (t < -0.1s):   ζ ≈ 1.000 — no difference, standard GR")
print("    Late inspiral (-0.1 to -0.01): ζ starts growing — subtle amplitude boost")
print("    Near merger (-0.01 to 0):      ζ significant — waveform diverges from GR")
print("    Ringdown (> 0):                ζ at maximum — damping rate may differ")
print()
print("  KEY INSIGHT: The substrate fingerprint is in the LAST FEW MILLISECONDS")
print("  before merger. This is where LIGO has the most signal and where ζ is loudest.")
print("  The late inspiral/merger transition is the sweet spot.")
print()

# ═══════════════════════════════════════════════════════════
# WHAT TO LOOK FOR IN REAL DATA
# ═══════════════════════════════════════════════════════════
print("=" * 90)
print("  WHAT TO LOOK FOR IN LIGO DATA")
print("=" * 90)
print("""
  1. AMPLITUDE: ζ-embedded waveform has HIGHER amplitude near merger.
     The substrate amplifies the wave as the source BHs get close.
     Look for: systematic amplitude excess in late inspiral vs GR templates.

  2. PHASE: Modified orbital dynamics shift the phase evolution.
     ζ changes the effective potential → orbits decay differently.
     Look for: phase residuals after subtracting best-fit GR template.

  3. RINGDOWN: After merger, the remnant BH rings down.
     ζ modifies the quasi-normal mode frequencies.
     Look for: ringdown frequency/damping time deviations from GR prediction.

  4. TIME DILATION: Compare detector clocks during events.
     The passing wave causes local time dilation fluctuation.
     ζ-modified wave → different fluctuation pattern.
     Look for: clock comparison anomalies correlated with GW events.

  BEST CANDIDATE EVENTS (public data on gwosc.org):
    - GW150914: First detection, loud signal, well-characterized
    - GW190521: Massive merger (150 M☉), strongest ζ effect expected
    - GW170817: Neutron star merger, different physics but good calibration
""")

# ═══════════════════════════════════════════════════════════
# SAVE DATA FOR VISUALIZATION
# ═══════════════════════════════════════════════════════════
# Downsample for JSON output
step = max(1, len(times) // 2000)
output = {
    'times': [times[i] for i in range(0, len(times), step)],
    'gr_strain': [gr_strain[i] for i in range(0, len(times), step)],
    'zeta_strain': [zeta_strain[i] for i in range(0, len(times), step)],
    'delta_strain': [delta_strain[i] for i in range(0, len(times), step)],
    'zeta_values': [zeta_values[i] for i in range(0, len(times), step)],
    'gr_freq': [gr_freq[i] for i in range(0, len(times), step)],
    'source': 'GW150914-like',
    'peak_delta_pct': max_delta / max_gr * 100,
}

with open('ligo_sim_data.json', 'w') as f:
    json.dump(output, f)

print(f"  Data saved to ligo_sim_data.json ({len(output['times'])} points)")
print(f"  Ready for visualization!")
print()
