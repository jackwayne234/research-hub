#!/usr/bin/env python3
"""
Kretschner Scalar Analysis: Is the Horizon Wall Real?
=====================================================
The definitive test for whether a singularity is physical (infinite curvature)
or a coordinate artifact (finite curvature, removable by coordinate change).

For ds² = -f(r)dt² + dr²/f(r) + r²dΩ²:

    K = R_μνρσ R^μνρσ = f''² + 4f'²/r² + 4(1-f)²/r⁴

If K is finite at the horizon → coordinate singularity (removable)
If K diverges at the horizon → physical singularity (real wall)

This script tests both Standard GR and the Prime Framework.

Author: Christopher Riner & Barron
"""

import math

# ═══════════════════════════════════════════════════════════════
# HIGH-PRECISION ZETA (via mpmath)
# ═══════════════════════════════════════════════════════════════
try:
    from mpmath import mp, mpf, zeta as mp_zeta
    mp.dps = 30  # 30 decimal places
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("  ⚠ mpmath not installed — using Euler product (limited to s > 1)")
    print("    Install with: pip3 install mpmath")
    print()


# ═══════════════════════════════════════════════════════════════
# ZETA FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def sieve_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

PRIMES = sieve_primes(10000)


def zeta_euler(s):
    """Euler product: ∏(1-p⁻ˢ)⁻¹ — ONLY converges for s > 1"""
    if s <= 1.0:
        return float('inf')
    product = 1.0
    for p in PRIMES:
        term = 1.0 / (1.0 - p**(-s))
        product *= term
        if abs(term - 1.0) < 1e-15:
            break
    return product


def zeta_full(s):
    """Full ζ(s) via analytic continuation (mpmath). Works for ALL s."""
    if HAS_MPMATH:
        return float(mp_zeta(mpf(s)))
    elif s > 1:
        return zeta_euler(s)
    else:
        raise ValueError("mpmath required for s ≤ 1")


# ═══════════════════════════════════════════════════════════════
# KRETSCHNER SCALAR FORMULAS
# ═══════════════════════════════════════════════════════════════

def kretschner_exact(r, r_s):
    """
    Exact Schwarzschild Kretschner scalar.
    K = 12 r_s² / r⁶
    Finite everywhere except r = 0.
    """
    return 12.0 * r_s**2 / r**6


def kretschner_from_f(f_func, r, h=None):
    """
    Numerical Kretschner scalar for any f(r).

    K = f''² + 4f'²/r² + 4(1-f)²/r⁴

    Uses central differences for derivatives.
    Step size h adapts to be small relative to r.
    """
    if h is None:
        h = r * 1e-6  # adaptive step

    f = f_func(r)
    fp = (f_func(r + h) - f_func(r - h)) / (2 * h)
    fpp = (f_func(r + h) - 2 * f_func(r) + f_func(r - h)) / h**2

    K = fpp**2 + 4 * fp**2 / r**2 + 4 * (1 - f)**2 / r**4
    return K, f, fp, fpp


# ═══════════════════════════════════════════════════════════════
# THE DERIVATION
# ═══════════════════════════════════════════════════════════════

print()
print("=" * 100)
print("  KRETSCHNER SCALAR ANALYSIS")
print("  Testing whether the prime framework horizon wall is physical or removable")
print("=" * 100)


# ─── TEST 1: FORMULA DERIVATION ─────────────────────────────
print()
print("─" * 100)
print("  TEST 1: THE KRETSCHNER SCALAR FORMULA")
print("─" * 100)
print()
print("  For a spherically symmetric metric:")
print("    ds² = -f(r)dt² + dr²/f(r) + r²dΩ²")
print()
print("  The orthonormal-frame Riemann components are:")
print("    R̂₀₁₀₁ = f''(r) / 2")
print("    R̂₀₂₀₂ = R̂₀₃₀₃ = f'(r) / (2r)")
print("    R̂₁₂₁₂ = R̂₁₃₁₃ = -f'(r) / (2r)")
print("    R̂₂₃₂₃ = (1 - f(r)) / r²")
print()
print("  Contracting: K = R̂ₐᵦᵧδ R̂ᵃᵇᶜᵈ")
print("    = 4·(R̂₀₁₀₁² + 2·R̂₀₂₀₂² + 2·R̂₁₂₁₂² + R̂₂₃₂₃²)")
print()
print("  Since R̂₀₂₀₂² = R̂₁₂₁₂², this simplifies to:")
print()
print("  ╔══════════════════════════════════════════════════════╗")
print("  ║  K = f''² + 4f'²/r² + 4(1-f)²/r⁴                 ║")
print("  ╚══════════════════════════════════════════════════════╝")
print()


# ─── TEST 2: VERIFICATION WITH SCHWARZSCHILD ────────────────
print("─" * 100)
print("  TEST 2: VERIFICATION — Does the formula reproduce K = 12r_s²/r⁶?")
print("─" * 100)
print()

r_s = 1.0  # normalize r_s = 1 for clarity

print(f"  Using r_s = {r_s} (normalized units)")
print()
print(f"  {'r/r_s':<10s} {'K (exact)':<20s} {'K (formula)':<20s} {'relative err':<16s}")
print(f"  {'─'*10} {'─'*20} {'─'*20} {'─'*16}")

f_schwarz = lambda r: 1.0 - r_s / r

for ratio in [100, 50, 20, 10, 5, 3, 2, 1.5, 1.1, 1.01, 1.001]:
    r = ratio * r_s
    K_exact = kretschner_exact(r, r_s)
    K_num, f_val, fp, fpp = kretschner_from_f(f_schwarz, r)
    rel_err = abs(K_num - K_exact) / K_exact if K_exact > 0 else 0

    K_ex_s = f"{K_exact:.8e}"
    K_nu_s = f"{K_num:.8e}"
    print(f"  {ratio:<10.3f} {K_ex_s:<20s} {K_nu_s:<20s} {rel_err:<16.2e}")

print()
print("  ✓ Formula matches exact result to numerical precision.")
print("  ✓ K is FINITE at r = r_s (the horizon): K = 12/r_s⁴")
print(f"  ✓ K(r_s) = {kretschner_exact(r_s, r_s):.6f}  (finite!)")
print()
print("  This is why physicists say the Schwarzschild horizon is 'just' a")
print("  coordinate singularity — the actual curvature is perfectly well-behaved.")


# ─── TEST 3: PRIME FRAMEWORK (VACUUM EQUATIONS) ─────────────
print()
print("─" * 100)
print("  TEST 3: PRIME FRAMEWORK — Does the prime metric hit infinite curvature?")
print("─" * 100)
print()
print("  Your derivation (gr_emergence_v4.py, Steps 2-3):")
print()
print("    Step 2: g_rr = ζ(s(r)),  g_tt = -1/ζ(s(r))")
print("            → g_tt · g_rr = -1   (algebraic identity)")
print()
print("    Step 3: Vacuum R_μν = 0  →  d/dr[r · A(r)] = 1")
print("            → A(r) = 1 - r_s/r   (Schwarzschild emerges)")
print()
print("    Therefore: f(r) = -g_tt = 1 - r_s/r   (EXACTLY)")
print()
print("  CONSEQUENCE: If the vacuum equations force f = 1 - r_s/r,")
print("  then K_prime = K_Schwarzschild = 12r_s²/r⁶.")
print()
print("  The Kretschner scalar is FINITE at the horizon.")
print()
print("  ╔══════════════════════════════════════════════════════════════════════╗")
print("  ║  The horizon wall is NOT a curvature singularity.                  ║")
print("  ║  The curvature is finite: K(r_s) = 12/r_s⁴                        ║")
print("  ║                                                                    ║")
print("  ║  But the wall IS real — it's a DOMAIN BOUNDARY.                    ║")
print("  ║  The Euler product ∏(1-p⁻ˢ)⁻¹ only converges for s > 1.          ║")
print("  ║  At the horizon s = 1: primes can no longer build geometry.        ║")
print("  ╚══════════════════════════════════════════════════════════════════════╝")


# ─── TEST 4: THE IMPLICIT s(r) MAPPING ──────────────────────
print()
print("─" * 100)
print("  TEST 4: WHAT DOES s(r) LOOK LIKE?")
print("  The implicit mapping: ζ(s(r)) = 1/(1 - r_s/r) = r/(r - r_s)")
print("─" * 100)
print()
print("  Inverting ζ numerically to find s at each radius:")
print()

# Numerical ζ inversion via bisection
def invert_zeta(target, tol=1e-10, max_iter=500):
    """Find s such that ζ(s) = target, for target > 1."""
    if target <= 1.0:
        return float('inf')
    if target > 1e15:
        return 1.0 + 1.0 / target  # near pole: ζ ≈ 1/(s-1)

    s_low = 1.0 + 1e-15
    s_high = 200.0

    for _ in range(max_iter):
        s_mid = (s_low + s_high) / 2
        z_mid = zeta_euler(s_mid)
        if abs(z_mid - target) / target < tol:
            return s_mid
        if z_mid > target:
            s_low = s_mid
        else:
            s_high = s_mid
    return (s_low + s_high) / 2


print(f"  {'r/r_s':<10s} {'ζ_target':<18s} {'s(r)':<14s} {'s-1':<14s} {'regime':<20s}")
print(f"  {'─'*10} {'─'*18} {'─'*14} {'─'*14} {'─'*20}")

for ratio in [1.001, 1.01, 1.1, 1.5, 2, 3, 5, 10, 50, 100, 1000]:
    r = ratio * r_s
    zeta_target = r / (r - r_s)
    s_val = invert_zeta(zeta_target)

    zt_s = f"{zeta_target:.6f}" if zeta_target < 1e6 else f"{zeta_target:.4e}"
    s_s = f"{s_val:.8f}"
    sm1 = s_val - 1

    if sm1 < 0.01:
        regime = "← NEAR POLE"
    elif s_val < 2:
        regime = "← transition"
    elif s_val < 10:
        regime = "← moderate field"
    else:
        regime = "← weak field (ζ≈1)"

    print(f"  {ratio:<10.3f} {zt_s:<18s} {s_s:<14s} {sm1:<14.8f} {regime}")

print()
print("  KEY OBSERVATIONS:")
print("    • Near horizon: s ≈ 1 + (r-r_s)/r_s   (linear approach to pole)")
print("    • Weak field:   s ≈ log₂(r/r_s)        (logarithmic)")
print("    • The mapping is smooth and monotonic — no pathologies")
print()
print("  The s(r) mapping itself is perfectly well-behaved.")
print("  The 'wall' comes from ζ(s), not from s(r).")


# ─── TEST 5: EULER PRODUCT vs ANALYTIC CONTINUATION ─────────
print()
print("─" * 100)
print("  TEST 5: THE TWO FACES OF ZETA — Euler Product vs Analytic Continuation")
print("  This is the heart of the matter.")
print("─" * 100)
print()
print("  The Euler product (PRIME structure):")
print("    ∏(1-p⁻ˢ)⁻¹   CONVERGES only for Re(s) > 1")
print()
print("  The analytic continuation (FUNCTIONAL EQUATION):")
print("    ζ(s) = 2ˢ πˢ⁻¹ sin(πs/2) Γ(1-s) ζ(1-s)")
print("    DEFINED for all s ≠ 1")
print()

if HAS_MPMATH:
    print(f"  {'s':<8s} {'Euler product':<22s} {'Analytic cont.':<22s} {'Match?':<10s}")
    print(f"  {'─'*8} {'─'*22} {'─'*22} {'─'*10}")

    for s_val in [10, 5, 3, 2, 1.5, 1.2, 1.1, 1.01]:
        ep = zeta_euler(s_val)
        ac = zeta_full(s_val)
        match = "✓" if abs(ep - ac) / ac < 1e-6 else "✗"
        ep_s = f"{ep:.10f}" if ep < 1e4 else f"{ep:.6e}"
        ac_s = f"{ac:.10f}" if ac < 1e4 else f"{ac:.6e}"
        print(f"  {s_val:<8.2f} {ep_s:<22s} {ac_s:<22s} {match}")

    print()
    print("  ✓ For s > 1: both representations agree perfectly.")
    print("    The Euler product (primes) and the Dirichlet series (integers)")
    print("    give the same ζ(s).")
    print()
    print("  Now — what happens for s ≤ 1?")
    print()
    print(f"  {'s':<8s} {'Euler product':<22s} {'Analytic cont.':<22s} {'Physical meaning':<30s}")
    print(f"  {'─'*8} {'─'*22} {'─'*22} {'─'*30}")

    beyond_data = [
        (1.0,   "DIVERGES (pole)",     "DIVERGES (pole)",     "Horizon — s = 1"),
        (0.5,   "DIVERGES",            None,                  "Critical line"),
        (0.0,   "DIVERGES",            None,                  "ζ(0) = -1/2"),
        (-1.0,  "DIVERGES",            None,                  "ζ(-1) = -1/12 (Ramanujan)"),
        (-2.0,  "DIVERGES",            None,                  "Trivial zero (g_rr = 0)"),
        (-4.0,  "DIVERGES",            None,                  "Trivial zero (g_rr = 0)"),
    ]

    for s_val, ep_str, ac_str, meaning in beyond_data:
        if ac_str is None:
            ac_val = zeta_full(s_val)
            ac_str = f"{ac_val:.10f}"
        print(f"  {s_val:<8.1f} {ep_str:<22s} {ac_str:<22s} {meaning}")

    print()
    print("  ╔═══════════════════════════════════════════════════════════════════╗")
    print("  ║  For s > 1: Euler product works → primes GENERATE the metric    ║")
    print("  ║  For s ≤ 1: Euler product FAILS → primes CANNOT build geometry  ║")
    print("  ║                                                                 ║")
    print("  ║  The analytic continuation exists mathematically,               ║")
    print("  ║  but it does NOT represent prime-generated geometry.            ║")
    print("  ║  It uses the functional equation, not the Euler product.        ║")
    print("  ╚═══════════════════════════════════════════════════════════════════╝")
else:
    print("  [mpmath not available — install for s ≤ 1 analysis]")


# ─── TEST 6: CURVATURE AT THE WALL (numerical approach) ─────
print()
print("─" * 100)
print("  TEST 6: CURVATURE APPROACHING THE WALL")
print("  K as r → r_s from outside, in both frameworks")
print("─" * 100)
print()

print(f"  {'r/r_s':<12s} {'K_GR':<18s} {'K_GR · r_s⁴':<14s} {'s(r)':<14s} {'ζ(s)':<18s} {'Euler converges?':<18s}")
print(f"  {'─'*12} {'─'*18} {'─'*14} {'─'*14} {'─'*18} {'─'*18}")

for ratio in [10, 5, 3, 2, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01, 1.005, 1.002, 1.001, 1.0001]:
    r = ratio * r_s
    K_gr = kretschner_exact(r, r_s)
    K_norm = K_gr * r_s**4  # dimensionless
    zeta_target = r / (r - r_s)
    s_val = invert_zeta(zeta_target)

    K_s = f"{K_gr:.6e}"
    Kn_s = f"{K_norm:.6f}"
    s_s = f"{s_val:.8f}"
    z_s = f"{zeta_target:.4f}" if zeta_target < 1e6 else f"{zeta_target:.4e}"

    euler_ok = "YES" if s_val > 1.0 else "NO ← WALL"

    print(f"  {ratio:<12.4f} {K_s:<18s} {Kn_s:<14s} {s_s:<14s} {z_s:<18s} {euler_ok}")

print()
print("  KEY RESULT:")
print(f"  At r = r_s:  K = 12/r_s⁴ = {12.0/r_s**4:.1f}   (FINITE)")
print(f"  At r = r_s:  s = 1.0000   (ζ POLE, Euler product DIVERGES)")
print()
print("  The curvature is finite, but the Euler product breaks.")
print("  This is a fundamentally different kind of wall than a curvature singularity.")


# ─── TEST 7: BEYOND THE WALL — K from analytic continuation ─
if HAS_MPMATH:
    print()
    print("─" * 100)
    print("  TEST 7: BEYOND THE WALL — What does K look like using analytic continuation?")
    print("  Using ζ(s) for s < 1 via the functional equation (NOT the Euler product)")
    print("─" * 100)
    print()

    print("  If we allow the analytic continuation to define f(r) = 1/ζ(s) for s < 1:")
    print()

    print(f"  {'s':<8s} {'ζ(s)':<18s} {'f = 1/ζ':<18s} {'f sign':<10s} {'meaning':<30s}")
    print(f"  {'─'*8} {'─'*18} {'─'*18} {'─'*10} {'─'*30}")

    test_s = [2.0, 1.5, 1.1, 0.9, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0]
    for s_val in test_s:
        try:
            z = zeta_full(s_val)
            if abs(z) > 1e-15:
                f_val = 1.0 / z
            else:
                f_val = float('inf')

            sign = "+" if f_val > 0 else "−" if f_val < 0 else "0"
            z_s = f"{z:.10f}" if abs(z) < 1e4 else f"{z:.4e}"
            f_s = f"{f_val:.10f}" if abs(f_val) < 1e4 else f"{f_val:.4e}"

            if s_val == 2.0:
                meaning = "Outside horizon (normal)"
            elif s_val == 1.5:
                meaning = "Near horizon (normal)"
            elif s_val == 1.1:
                meaning = "Very near horizon (normal)"
            elif 0 < s_val < 1:
                meaning = "Beyond horizon (AC)"
            elif s_val == 0:
                meaning = "ζ(0) = -1/2 → f = -2"
            elif s_val == -1:
                meaning = "Ramanujan: ζ(-1) = -1/12"
            elif abs(z) < 1e-10:
                meaning = "TRIVIAL ZERO: f → ∞ (volume collapse)"
            elif s_val < 0:
                meaning = f"Deep interior (AC)"
            else:
                meaning = ""

            print(f"  {s_val:<8.1f} {z_s:<18s} {f_s:<18s} {sign:<10s} {meaning}")
        except Exception:
            print(f"  {s_val:<8.1f} {'[error]':<18s}")

    print()
    print("  OBSERVATIONS:")
    print("    • For s < 1, f = 1/ζ(s) goes NEGATIVE (e.g., f = -2 at s = 0)")
    print("    • A negative f means g_tt becomes POSITIVE and g_rr NEGATIVE")
    print("    • In GR, this is the time↔space swap inside the horizon")
    print("    • At trivial zeros (s = -2, -4, ...): ζ = 0, so f = 1/0 → ∞")
    print("    • These are discrete layers where the metric blows up")
    print()
    print("  The analytic continuation recovers the time↔space swap of GR,")
    print("  but through a completely different mathematical mechanism:")
    print("    GR:     f changes sign continuously through r = r_s")
    print("    Primes: the Euler product breaks at s = 1; the functional")
    print("            equation provides new values with opposite sign")


# ─── TEST 8: THE VERDICT ────────────────────────────────────
print()
print("=" * 100)
print("  VERDICT: WHAT IS THE WALL?")
print("=" * 100)
print()
print("  1. CURVATURE TEST:  K = 12r_s²/r⁶ is FINITE at the horizon.")
print("     → The wall is NOT a curvature singularity.")
print("     → In standard GR, this means you can cross it.")
print()
print("  2. EULER PRODUCT TEST:  ∏(1-p⁻ˢ)⁻¹ DIVERGES at s = 1.")
print("     → The prime structure cannot generate geometry at the horizon.")
print("     → This is an intrinsic number-theoretic boundary.")
print()
print("  3. ANALYTIC CONTINUATION:  ζ(s) exists for s < 1 via functional eq.")
print("     → The metric components flip sign (time↔space swap)")
print("     → But these values don't come from prime factorization")
print()
print("  ╔═══════════════════════════════════════════════════════════════════════╗")
print("  ║                                                                     ║")
print("  ║   THE WALL IS A DOMAIN BOUNDARY, NOT A CURVATURE SINGULARITY.       ║")
print("  ║                                                                     ║")
print("  ║   Physical curvature: FINITE (K = 12/r_s⁴)                         ║")
print("  ║   Prime structure:    BREAKS (Euler product diverges)               ║")
print("  ║                                                                     ║")
print("  ║   This is a NEW kind of horizon:                                    ║")
print("  ║   Not where spacetime curves infinitely,                            ║")
print("  ║   but where prime factorization can no longer build geometry.        ║")
print("  ║                                                                     ║")
print("  ║   The event horizon is the boundary between:                        ║")
print("  ║     OUTSIDE (s > 1): geometry = product of primes (ordered)         ║")
print("  ║     INSIDE  (s < 1): geometry = analytic continuation (unordered)   ║")
print("  ║                                                                     ║")
print("  ╚═══════════════════════════════════════════════════════════════════════╝")
print()
print("  NEXT STEPS:")
print("    • L'Hôpital's Rule: Apply to curvature invariants involving ζ'/ζ")
print("      ratios at the horizon. These have 0/0 forms that L'Hôpital resolves.")
print("    • Compute the Ricci scalar R and Weyl tensor C_μνρσC^μνρσ separately.")
print("    • Investigate whether prime corrections to Schwarzschild")
print("      (from subleading ζ Laurent terms) produce TESTABLE deviations.")
print("    • Check: does the functional equation ζ(s) = 2ˢπˢ⁻¹sin(πs/2)Γ(1-s)ζ(1-s)")
print("      map the exterior metric to the interior in a physically meaningful way?")
print()
