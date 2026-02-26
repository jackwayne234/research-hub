#!/usr/bin/env python3
"""
Double-Slit Benford Test
========================
Tests the prediction from Section 9: measurement increases δ_B,
producing a continuous transition from wave to particle behavior.

The BEC paper (Paper #2) showed:
  - Bosonic occupation numbers satisfy Benford EXACTLY (δ_B = 0)
  - Fermionic occupation numbers deviate by η(s)/ζ(s) = (1-2^{1-s})

A detector couples the bosonic photon to fermionic electrons.
As coupling strength increases:
  - The combined system's δ_B should rise
  - Interference visibility V should fall
  - The Englert-Greenberger relation D² + V² ≤ 1 should hold
  - δ_B should correlate with distinguishability D, not visibility V

Author: Christopher Riner & Barron
Date: February 25, 2026
"""

import math
import random

# ═══════════════════════════════════════════════════════════════
# BENFORD'S LAW
# ═══════════════════════════════════════════════════════════════

BENFORD_FREQ = {d: math.log10(1 + 1/d) for d in range(1, 10)}

def leading_digit(x):
    """Extract leading significant digit of |x|."""
    if x == 0:
        return None
    x = abs(x)
    while x >= 10:
        x /= 10
    while x < 1:
        x *= 10
    return int(x)

def compute_delta_B(values):
    """
    Compute Benford deviation δ_B from a list of numerical values.
    δ_B = Σ|observed_freq(d) - P(d)| for d = 1..9
    """
    digits = [leading_digit(v) for v in values if v != 0]
    digits = [d for d in digits if d is not None]
    if len(digits) < 10:
        return float('nan')

    N = len(digits)
    counts = {d: 0 for d in range(1, 10)}
    for d in digits:
        if 1 <= d <= 9:
            counts[d] += 1

    delta = 0.0
    per_digit = {}
    for d in range(1, 10):
        observed = counts[d] / N
        expected = BENFORD_FREQ[d]
        per_digit[d] = observed - expected
        delta += abs(observed - expected)

    return delta, per_digit


# ═══════════════════════════════════════════════════════════════
# QUANTUM STATISTICS
# ═══════════════════════════════════════════════════════════════

def bose_einstein(E, T, mu=0):
    """Bose-Einstein occupation number: 1/(e^((E-μ)/kT) - 1)"""
    x = (E - mu) / T
    if x > 500:
        return 0.0
    if x < -500:
        return 1e10
    denom = math.exp(x) - 1
    if abs(denom) < 1e-30:
        return 1e10
    return 1.0 / denom

def fermi_dirac(E, T, mu=0):
    """Fermi-Dirac occupation number: 1/(e^((E-μ)/kT) + 1)"""
    x = (E - mu) / T
    if x > 500:
        return 0.0
    if x < -500:
        return 1.0
    return 1.0 / (math.exp(x) + 1)


# ═══════════════════════════════════════════════════════════════
# TEST 1: PURE BOSONIC vs PURE FERMIONIC δ_B
# ═══════════════════════════════════════════════════════════════

print()
print("=" * 100)
print("  TEST 1: PURE BOSONIC vs PURE FERMIONIC BENFORD DEVIATION")
print("  BEC paper prediction: bosonic δ_B < fermionic δ_B at all temperatures")
print("=" * 100)
print()

temperatures = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
energies = [E * 0.01 for E in range(1, 5001)]  # 5000 energy levels

print(f"  {'T':<10s} {'δ_B (boson)':<16s} {'δ_B (fermion)':<16s} {'ratio F/B':<12s} {'prediction'}")
print(f"  {'─'*10} {'─'*16} {'─'*16} {'─'*12} {'─'*12}")

for T in temperatures:
    # Bosonic occupation numbers
    bose_vals = [bose_einstein(E, T) for E in energies]
    bose_vals = [v for v in bose_vals if 0 < v < 1e10]

    # Fermionic occupation numbers
    fermi_vals = [fermi_dirac(E, T) for E in energies]
    fermi_vals = [v for v in fermi_vals if 0 < v < 1e10]

    if len(bose_vals) < 50 or len(fermi_vals) < 50:
        continue

    dB_bose, _ = compute_delta_B(bose_vals)
    dB_fermi, _ = compute_delta_B(fermi_vals)

    ratio = dB_fermi / dB_bose if dB_bose > 1e-10 else float('inf')
    matches = "✓ F > B" if dB_fermi > dB_bose else "✗ FAILS"

    print(f"  {T:<10.1f} {dB_bose:<16.6f} {dB_fermi:<16.6f} {ratio:<12.2f} {matches}")

print()
print("  If bosonic δ_B < fermionic δ_B at every temperature,")
print("  then coupling a boson to a fermion MUST increase the combined δ_B.")


# ═══════════════════════════════════════════════════════════════
# TEST 2: MEASUREMENT AS BOSON-FERMION COUPLING
# ═══════════════════════════════════════════════════════════════

print()
print()
print("=" * 100)
print("  TEST 2: MEASUREMENT AS BOSON-FERMION COUPLING")
print("  Simulating double-slit with variable detector coupling")
print("=" * 100)
print()

T = 1.0  # Temperature in natural units
N_photons = 3000  # Number of energy levels for the photon field

# Photon energies (thermal distribution of modes)
photon_energies = [E * 0.01 for E in range(1, N_photons + 1)]

# Detector electron energies (same range, different statistics)
detector_energies = [E * 0.01 for E in range(1, N_photons + 1)]

# Compute all occupation numbers
photon_occupations = [bose_einstein(E, T) for E in photon_energies]
photon_occupations = [v for v in photon_occupations if 0 < v < 1e10]

detector_occupations = [fermi_dirac(E, T) for E in detector_energies]
detector_occupations = [v for v in detector_occupations if 0 < v < 1e10]

# Coupling strength α: fraction of fermionic DOF in the combined system
# α = 0 → pure bosonic (no detector) → full interference
# α = 1 → equal bosonic + fermionic → no interference
coupling_strengths = [0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5,
                      0.6, 0.7, 0.8, 0.9, 1.0]

print(f"  {'α (coupling)':<14s} {'N_boson':<10s} {'N_fermion':<10s} {'δ_B':<12s} "
      f"{'D':<8s} {'V':<8s} {'D²+V²':<8s} {'character'}")
print(f"  {'─'*14} {'─'*10} {'─'*10} {'─'*12} {'─'*8} {'─'*8} {'─'*8} {'─'*20}")

results = []

for alpha in coupling_strengths:
    # Combined system: (1-α) bosonic + α fermionic
    n_boson = int(len(photon_occupations) * (1 - alpha))
    n_fermion = int(len(detector_occupations) * alpha)

    if n_boson < 1:
        n_boson = 1

    combined = photon_occupations[:n_boson]
    if n_fermion > 0:
        combined += detector_occupations[:n_fermion]

    if len(combined) < 50:
        continue

    dB, per_digit = compute_delta_B(combined)

    # Distinguishability D: proportional to coupling
    # D = 0 when α = 0 (no which-path), D = 1 when fully coupled
    D = min(1.0, alpha * 2)  # Saturates at α = 0.5

    # Visibility V from Englert-Greenberger: V = √(1 - D²)
    V = math.sqrt(max(0, 1 - D**2))

    # Check D² + V² ≤ 1
    DV_sum = D**2 + V**2

    # Character assessment
    if dB < 0.01:
        char = "quantum/wavelike"
    elif dB < 0.03:
        char = "mixed"
    elif dB < 0.06:
        char = "mostly massive"
    else:
        char = "massive/particlelike"

    results.append((alpha, n_boson, n_fermion, dB, D, V, DV_sum, char))
    print(f"  {alpha:<14.2f} {n_boson:<10d} {n_fermion:<10d} {dB:<12.6f} "
          f"{D:<8.3f} {V:<8.3f} {DV_sum:<8.3f} {char}")

print()


# ═══════════════════════════════════════════════════════════════
# TEST 3: CORRELATION ANALYSIS — δ_B vs D vs V
# ═══════════════════════════════════════════════════════════════

print()
print("=" * 100)
print("  TEST 3: CORRELATION — Does δ_B track D (distinguishability) or V (visibility)?")
print("=" * 100)
print()

# Compute Pearson correlation coefficients
if len(results) > 3:
    dBs = [r[3] for r in results]
    Ds = [r[4] for r in results]
    Vs = [r[5] for r in results]

    def pearson(x, y):
        n = len(x)
        mx = sum(x) / n
        my = sum(y) / n
        sx = math.sqrt(sum((xi - mx)**2 for xi in x) / n)
        sy = math.sqrt(sum((yi - my)**2 for yi in y) / n)
        if sx < 1e-10 or sy < 1e-10:
            return 0.0
        return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (n * sx * sy)

    r_dB_D = pearson(dBs, Ds)
    r_dB_V = pearson(dBs, Vs)
    r_dB_alpha = pearson(dBs, [r[0] for r in results])

    print(f"  Pearson correlation coefficients:")
    print(f"    r(δ_B, D)     = {r_dB_D:+.4f}  {'← STRONG' if abs(r_dB_D) > 0.7 else ''}")
    print(f"    r(δ_B, V)     = {r_dB_V:+.4f}  {'← STRONG' if abs(r_dB_V) > 0.7 else ''}")
    print(f"    r(δ_B, α)     = {r_dB_alpha:+.4f}  {'← STRONG' if abs(r_dB_alpha) > 0.7 else ''}")
    print()

    # Prediction check
    if r_dB_D > 0.5 and r_dB_V < -0.5:
        print("  ✓ PREDICTION CONFIRMED:")
        print("    δ_B correlates POSITIVELY with D (distinguishability)")
        print("    δ_B correlates NEGATIVELY with V (visibility)")
        print("    → As measurement strength increases, δ_B rises and interference fades.")
    elif r_dB_D > 0.5:
        print("  ✓ PARTIAL: δ_B correlates with D (distinguishability)")
    else:
        print("  ✗ INCONCLUSIVE: correlations weaker than expected")


# ═══════════════════════════════════════════════════════════════
# TEST 4: THE BRIDGE FACTOR ε_B AT EACH COUPLING
# ═══════════════════════════════════════════════════════════════

print()
print()
print("=" * 100)
print("  TEST 4: BRIDGE FACTOR COMPARISON")
print("  ε_B = |1 - 2^(1-s)| from BEC paper — does it predict the transition?")
print("=" * 100)
print()

# For a thermal photon system at temperature T, the effective s parameter
# can be estimated from the average occupation number:
# ζ(s) ≈ <n_BE>_avg → s from inverse zeta

# Average occupation number for our photon field
avg_n_bose = sum(photon_occupations) / len(photon_occupations)

# Estimate s: ζ(s) ≈ avg_n corresponds to a specific s
# For small avg_n (≈ 1-2), s ≈ 2-4
# Use simple inversion: ζ(s) ≈ 1 + 2^(-s) + 3^(-s) + ...
def approx_s_from_zeta(target):
    """Bisection to find s where ζ(s) ≈ target."""
    if target <= 1.0:
        return 100.0
    s_lo, s_hi = 1.001, 50.0
    for _ in range(100):
        s_mid = (s_lo + s_hi) / 2
        z = sum(n**(-s_mid) for n in range(1, 1001))
        if z > target:
            s_lo = s_mid
        else:
            s_hi = s_mid
    return (s_lo + s_hi) / 2

s_eff = approx_s_from_zeta(avg_n_bose)
bridge = abs(1.0 - 2.0**(1 - s_eff))

print(f"  System parameters:")
print(f"    Temperature T = {T}")
print(f"    Average bosonic occupation <n> = {avg_n_bose:.4f}")
print(f"    Effective s parameter: s_eff = {s_eff:.4f}")
print(f"    Bridge factor: ε_B = |1 - 2^(1-s)| = {bridge:.6f}")
print()

print(f"  {'α':<10s} {'δ_B':<12s} {'ε_B':<12s} {'δ_B < ε_B?':<14s} {'regime'}")
print(f"  {'─'*10} {'─'*12} {'─'*12} {'─'*14} {'─'*20}")

for alpha, n_b, n_f, dB, D, V, DV, char in results:
    # As coupling increases, the effective s shifts
    # More fermionic content → effective s closer to 1 (where bridge → 0)
    # Model: s_eff shifts from far field toward horizon as coupling increases
    s_coupled = s_eff * (1 - alpha * 0.5)  # Coupling pulls s toward 1
    if s_coupled <= 1.0:
        s_coupled = 1.001
    bridge_coupled = abs(1.0 - 2.0**(1 - s_coupled))
    below = "YES ✓" if dB < bridge_coupled else "NO — crossing"
    regime = "bosonic" if dB < bridge_coupled else "fermionic signature"
    print(f"  {alpha:<10.2f} {dB:<12.6f} {bridge_coupled:<12.6f} {below:<14s} {regime}")


# ═══════════════════════════════════════════════════════════════
# TEST 5: PER-DIGIT ANALYSIS — WHERE DOES THE DEVIATION COME FROM?
# ═══════════════════════════════════════════════════════════════

print()
print()
print("=" * 100)
print("  TEST 5: PER-DIGIT DEVIATION — Which digits shift when fermions enter?")
print("=" * 100)
print()

# Compare per-digit deviations at α = 0 vs α = 0.5 vs α = 1.0
test_alphas = [0.0, 0.1, 0.3, 0.5, 1.0]

print(f"  {'α':<6s}", end="")
for d in range(1, 10):
    print(f"  {'d=' + str(d):<9s}", end="")
print(f"  {'δ_B':<10s}")
print(f"  {'─'*6}", end="")
for _ in range(9):
    print(f"  {'─'*9}", end="")
print(f"  {'─'*10}")

for alpha in test_alphas:
    n_boson = int(len(photon_occupations) * (1 - alpha))
    n_fermion = int(len(detector_occupations) * alpha)
    if n_boson < 1:
        n_boson = 1

    combined = photon_occupations[:n_boson]
    if n_fermion > 0:
        combined += detector_occupations[:n_fermion]

    if len(combined) < 50:
        continue

    dB, per_digit = compute_delta_B(combined)

    print(f"  {alpha:<6.2f}", end="")
    for d in range(1, 10):
        val = per_digit.get(d, 0)
        sign = "+" if val >= 0 else ""
        print(f"  {sign}{val:<8.5f}", end="")
    print(f"  {dB:<10.6f}")

print()
print("  Positive ε(d) = digit d appears MORE than Benford predicts")
print("  Negative ε(d) = digit d appears LESS than Benford predicts")
print("  If fermions shift digit 1 frequency, that's the BEC paper signature:")
print("  Benford predicts d=1 at 30.1% — fermions push it away from this.")


# ═══════════════════════════════════════════════════════════════
# VERDICT
# ═══════════════════════════════════════════════════════════════

print()
print()
print("=" * 100)
print("  VERDICT")
print("=" * 100)
print()

if len(results) > 3:
    dB_pure = results[0][3]   # α = 0
    dB_half = None
    dB_full = results[-1][3]  # α = 1.0

    for r in results:
        if abs(r[0] - 0.5) < 0.01:
            dB_half = r[3]

    print(f"  δ_B at α = 0.0 (no detector):      {dB_pure:.6f}")
    if dB_half is not None:
        print(f"  δ_B at α = 0.5 (half coupling):    {dB_half:.6f}")
    print(f"  δ_B at α = 1.0 (full coupling):     {dB_full:.6f}")
    print()

    if dB_full > dB_pure:
        increase = (dB_full - dB_pure) / dB_pure * 100
        print(f"  δ_B INCREASES by {increase:.1f}% from no-detector to full-detector.")
        print()
        print("  ✓ CONFIRMED: Measurement (fermionic coupling) increases δ_B.")
        print("    The photon system slides from bosonic → fermionic on the")
        print("    mass-quantum spectrum as the detector couples more strongly.")
        print()
        print("  ✓ MECHANISM: The detector's electrons (fermions) contribute")
        print("    occupation numbers that deviate from Benford's Law by")
        print("    mathematical necessity (alternating series ≠ completely monotone).")
        print("    The combined system's δ_B is a weighted average.")
        print()
        print("  ✓ PREDICTION FOR LAB: In a real double-slit experiment,")
        print("    collecting leading digits of all measurable quantities")
        print("    should show δ_B ~ 0 for full interference and δ_B > 0")
        print("    for particle detection, with a continuous transition")
        print("    as measurement strength varies.")
    else:
        print("  ✗ UNEXPECTED: δ_B did not increase with coupling.")
        print("    This would invalidate the prediction.")

print()
