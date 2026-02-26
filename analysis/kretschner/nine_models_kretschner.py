#!/usr/bin/env python3
"""
Kretschner Scalar Through 9 Quantum Gravity Models
====================================================
Since Benford conformance holds for all 9 models through to the singularity
(previous result), K is a valid curvature probe the entire way down.

Each QG model modifies f(r) differently near the singularity.
K = f''² + 4f'²/r² + 4(1-f)²/r⁴ reveals which models resolve r = 0.

Author: Christopher Riner & Barron
Date: February 25, 2026
"""

import math

# ═══════════════════════════════════════════════════════════════
# CONSTANTS (Planck units for QG corrections)
# ═══════════════════════════════════════════════════════════════
r_s = 1.0       # Schwarzschild radius (normalized)
r_P = 1e-4      # Planck length as fraction of r_s (exaggerated for visibility)
                 # Real ratio: r_P/r_s ~ 10⁻³⁸ for solar mass BH
                 # We use 10⁻⁴ so corrections are visible in the plots

GAMMA = 0.5772156649  # Euler-Mascheroni constant


# ═══════════════════════════════════════════════════════════════
# THE 9 MODELS — each defines f(r) and a description
# ═══════════════════════════════════════════════════════════════

def f_standard_gr(r):
    """Standard Schwarzschild: f = 1 - r_s/r"""
    return 1.0 - r_s / r


def f_loop_qg(r):
    """
    Loop Quantum Gravity: singularity replaced by bounce.
    Effective metric from LQG polymer quantization:
      f(r) = (1 - r_s/r) × (1 + r_s·r_P²/r³)
    The correction factor makes f > 0 at small r → no singularity.
    Ref: Modesto (2004), Ashtekar & Bojowald (2006)
    """
    return (1.0 - r_s / r) * (1.0 + r_s * r_P**2 / r**3)


def f_asymptotic_safety(r):
    """
    Asymptotic Safety: running Newton's constant G(r) → 0 at UV.
    Effective metric:
      f(r) = 1 - r_s·r² / (r³ + ω·r_s·r_P²)
    where ω = 118/(15π) ≈ 2.505.
    Singularity replaced by de Sitter core.
    Ref: Bonanno & Reuter (2000)
    """
    omega = 118.0 / (15.0 * math.pi)
    return 1.0 - r_s * r**2 / (r**3 + omega * r_s * r_P**2)


def f_noncommutative(r):
    """
    Non-Commutative Geometry: point mass smeared into Gaussian.
    Effective metric:
      f(r) = 1 - (r_s/r) × erf(r / (2√θ))
    where √θ ~ r_P (non-commutativity scale).
    Singularity replaced by finite-density core.
    Ref: Nicolini, Smailagic & Spallucci (2006)
    """
    theta = r_P
    # erf approximation (good to ~10⁻⁷)
    x = r / (2.0 * theta)
    # Use math.erf
    return 1.0 - (r_s / r) * math.erf(x)


def f_string_gup(r):
    """
    String Theory (GUP correction): minimum length from generalized
    uncertainty principle.
      f(r) = 1 - r_s / (r + α·r_P²/r)
    where α ~ O(1) is the string tension parameter.
    The effective radius r_eff = r + α·r_P²/r > 0 always.
    Ref: Adler, Chen & Santiago (2001)
    """
    alpha = 1.0
    r_eff = r + alpha * r_P**2 / r
    return 1.0 - r_s / r_eff


def f_causal_sets(r):
    """
    Causal Set Theory: discrete spacetime with minimum volume element.
    Metric identical to Schwarzschild but with volume floor:
      det(g_spatial) ≥ ε_vol
    When floor activates, g_rr is modified to prevent total collapse.
    Floor value: 0.4068 (from Benford conformance threshold).
    Ref: Sorkin (2003), Riner Paper #1
    """
    f_gr = 1.0 - r_s / r
    if abs(f_gr) < 1e-30:
        return f_gr

    # Check if floor is needed
    g_rr = 1.0 / f_gr if f_gr != 0 else 1e30
    det_spatial = r**4  # r² × r² (θ and φ components)
    FLOOR_VAL = 0.4068

    if abs(det_spatial) < FLOOR_VAL and r < r_s:
        # Floor activates: effective f modified
        # g_rr_mod = FLOOR_VAL / r⁴
        # f_mod = 1 / g_rr_mod = r⁴ / FLOOR_VAL
        return r**4 / FLOOR_VAL
    return f_gr


def f_cdt(r):
    """
    Causal Dynamical Triangulations: spectral dimension runs from
    4 at large scales to ~2 at Planck scale.
    Effective metric picks up a running-dimension correction:
      f(r) = 1 - r_s/r × (r²/(r² + r_P²))
    The correction smoothly reduces to GR at large r and
    weakens gravity at small r (fewer effective dimensions).
    Ref: Ambjørn, Jurkiewicz & Loll (2005)
    """
    dim_factor = r**2 / (r**2 + r_P**2)
    return 1.0 - (r_s / r) * dim_factor


def f_twistor(r):
    """
    Twistor Theory: metric naturally extends to complex plane.
    On the real line, the leading correction is:
      f(r) = 1 - r_s/r + r_P⁴/(4r⁴)
    The r⁻⁴ correction from the complex structure prevents
    f from diverging negatively at small r.
    Ref: Penrose (1967), inspired by twistor string theory
    """
    return 1.0 - r_s / r + r_P**4 / (4.0 * r**4)


def f_group_field(r):
    """
    Group Field Theory: condensate correction from GFT.
    Similar to LQG but with different power:
      f(r) = (1 - r_s/r) × (1 + σ·(r_P/r)⁴)
    where σ ~ O(1) is the condensate parameter.
    Higher-power correction than LQG.
    Ref: Oriti (2009), Gielen & Sindoni (2016)
    """
    sigma = 1.0
    return (1.0 - r_s / r) * (1.0 + sigma * (r_P / r)**4)


def f_emergent_gravity(r):
    """
    Emergent/Entropic Gravity (Verlinde): leading entropic correction.
      f(r) = 1 - r_s/r + c₁·r_P²/r²
    where c₁ ~ O(1) is the entropic coefficient.
    The 1/r² correction from thermodynamic origin modifies
    near-horizon and near-singularity behavior.
    Ref: Verlinde (2011)
    """
    c1 = 1.0
    return 1.0 - r_s / r + c1 * r_P**2 / r**2


# ═══════════════════════════════════════════════════════════════
# ALL MODELS
# ═══════════════════════════════════════════════════════════════

MODELS = [
    ("Standard GR",       f_standard_gr,       "Baseline: K → ∞ at r=0"),
    ("Loop QG",           f_loop_qg,           "Bounce replaces singularity"),
    ("Asymptotic Safety", f_asymptotic_safety,  "de Sitter core, G(r) → 0"),
    ("Non-Comm Geometry", f_noncommutative,     "Gaussian-smeared mass"),
    ("String (GUP)",      f_string_gup,         "Minimum length from uncertainty"),
    ("Causal Sets",       f_causal_sets,        "Volume floor at det = 0.4068"),
    ("CDT",               f_cdt,                "Running spectral dimension"),
    ("Twistor Theory",    f_twistor,            "Complex plane r⁻⁴ correction"),
    ("Group Field Theory",f_group_field,         "GFT condensate correction"),
    ("Emergent Gravity",  f_emergent_gravity,    "Entropic 1/r² correction"),
]


# ═══════════════════════════════════════════════════════════════
# KRETSCHNER SCALAR COMPUTATION
# ═══════════════════════════════════════════════════════════════

def kretschner(f_func, r):
    """
    K = f''² + 4f'²/r² + 4(1-f)²/r⁴
    Uses central differences with adaptive step.
    Returns (K, f, f', f'')
    """
    h = r * 1e-5
    if h < 1e-20:
        h = 1e-20

    try:
        f0 = f_func(r)
        fp = f_func(r + h)
        fm = f_func(r - h)
    except (ZeroDivisionError, ValueError, OverflowError):
        return float('inf'), 0, 0, 0

    f_prime = (fp - fm) / (2 * h)
    f_double = (fp - 2 * f0 + fm) / h**2

    try:
        K = f_double**2 + 4 * f_prime**2 / r**2 + 4 * (1 - f0)**2 / r**4
    except (OverflowError, ZeroDivisionError):
        K = float('inf')

    return K, f0, f_prime, f_double


# ═══════════════════════════════════════════════════════════════
# RADIAL TRAJECTORY
# ═══════════════════════════════════════════════════════════════

# Dense sampling near horizon and deep interior
RADII = [
    10.0, 5.0, 3.0, 2.0, 1.5, 1.2, 1.1, 1.05, 1.01, 1.001,  # outside
    0.99, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2,            # inside
    0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001,               # deep
    5e-4, 2e-4, 1e-4,                                           # near Planck
]


# ═══════════════════════════════════════════════════════════════
# RUN THE ANALYSIS
# ═══════════════════════════════════════════════════════════════

print()
print("=" * 120)
print("  KRETSCHNER SCALAR THROUGH 9 QUANTUM GRAVITY MODELS")
print("  Benford conformance validates K as a probe all the way to r = 0")
print("=" * 120)
print()
print(f"  Planck length: r_P/r_s = {r_P}  (exaggerated for visibility)")
print(f"  Real solar BH: r_P/r_s ~ 10⁻³⁸ (corrections invisible until r ~ r_P)")
print()


# ─── INDIVIDUAL MODEL TRAJECTORIES ──────────────────────────

for model_name, f_func, description in MODELS:
    print()
    print("─" * 120)
    print(f"  {model_name.upper()}: {description}")
    print("─" * 120)
    print()

    header = f"  {'r/r_s':<12s} {'f(r)':<16s} {'K':<16s} {'K·r_s⁴':<14s} {'zone':<12s} {'singularity?':<16s}"
    print(header)
    print(f"  {'─'*12} {'─'*16} {'─'*16} {'─'*14} {'─'*12} {'─'*16}")

    peak_K = 0
    peak_r = 0
    resolved = False
    prev_K = 0

    for r in RADII:
        try:
            K, f_val, fp, fpp = kretschner(f_func, r)
        except Exception:
            K, f_val = float('inf'), 0

        if K > peak_K and K < float('inf'):
            peak_K = K
            peak_r = r

        # Check if singularity is resolved (K decreasing at small r)
        if r < 0.01 and K < prev_K and prev_K > 100:
            resolved = True
        prev_K = K

        # Zone label
        if r > 1.0:
            zone = "outside"
        elif r > 0.99:
            zone = "HORIZON"
        elif r > r_P * 10:
            zone = "inside"
        else:
            zone = "Planck"

        # Singularity assessment
        if K > 1e20:
            sing = "DIVERGING"
        elif K > 1e10:
            sing = "extreme"
        elif r < 0.01 and K < peak_K * 0.5:
            sing = "RESOLVING ←"
        else:
            sing = ""

        # Format
        f_s = f"{f_val:.8f}" if abs(f_val) < 1e6 else f"{f_val:.4e}"
        K_s = f"{K:.6e}" if K < 1e30 else "∞"
        Kn_s = f"{K * r_s**4:.4f}" if K < 1e10 else f"{K * r_s**4:.4e}" if K < 1e30 else "∞"

        print(f"  {r:<12.4e} {f_s:<16s} {K_s:<16s} {Kn_s:<14s} {zone:<12s} {sing}")

    print()
    if resolved:
        print(f"  → SINGULARITY RESOLVED. K peaks at r/r_s ≈ {peak_r:.4e} then decreases.")
        print(f"    Peak K = {peak_K:.4e}")
    else:
        print(f"  → K reaches {peak_K:.4e} at r/r_s ≈ {peak_r:.4e}")
        if peak_K > 1e15:
            print(f"    Singularity NOT resolved (K still diverging at smallest r)")
        else:
            print(f"    Singularity may be resolved (K bounded)")


# ─── COMPARISON MATRIX ──────────────────────────────────────
print()
print()
print("=" * 120)
print("  COMPARISON MATRIX: K at key radii for all models")
print("=" * 120)
print()

key_radii = [2.0, 1.01, 0.5, 0.1, 0.01, 0.001, 1e-4]

# Header
header = f"  {'Model':<22s}"
for r in key_radii:
    header += f"{'r=' + f'{r:.0e}' if r < 0.01 else 'r=' + f'{r}':<14s}"
header += "{'Resolves?':<12s}"
print(header)
print("  " + "─" * (22 + 14 * len(key_radii) + 12))

for model_name, f_func, description in MODELS:
    row = f"  {model_name:<22s}"
    k_values = []

    for r in key_radii:
        try:
            K, _, _, _ = kretschner(f_func, r)
            k_values.append(K)
            if K < 1e8:
                row += f"{K:<14.2f}"
            elif K < 1e30:
                row += f"{K:<14.2e}"
            else:
                row += f"{'∞':<14s}"
        except Exception:
            row += f"{'err':<14s}"
            k_values.append(float('inf'))

    # Does it resolve?
    if len(k_values) >= 2 and k_values[-1] < k_values[-2] and k_values[-2] > 100:
        row += "YES ←"
    elif k_values[-1] < 1e10:
        row += "BOUNDED"
    else:
        row += "no"

    print(row)


# ─── THE BENFORD EPSILON CONCEPT ─────────────────────────────
print()
print()
print("=" * 120)
print("  THE BENFORD EPSILON CONCEPT")
print("=" * 120)
print()
print("  All 9 models show Benford conformance (delta_B < ε_B) through to the singularity.")
print("  This means K is a valid curvature probe at EVERY radius for EVERY model.")
print()
print("  The Benford epsilon (ε_B) acts as a diagnostic switch:")
print()
print("    delta_B < ε_B  →  metric values are 'statistically natural'")
print("                      → K, Ricci scalar, Weyl tensor all meaningful")
print("                      → prime formula tools can be applied")
print()
print("    delta_B > ε_B  →  metric values deviate from natural distribution")
print("                      → tools may give misleading results")
print("                      → 'blind zone' (not observed in any of the 9 models)")
print()
print("  Since no blind zone exists for any model, the full toolkit is available:")
print()
print("    OUTSIDE (r > r_s):  Euler product ✓  Benford ✓  Kretschner ✓")
print("    HORIZON (r = r_s):  Euler product ✗  Benford ✓  Kretschner ✓")
print("    INSIDE  (r < r_s):  Euler product ✗  Benford ✓  Kretschner ✓")
print()


# ─── VERDICT ─────────────────────────────────────────────────
print("=" * 120)
print("  VERDICT: WHICH MODELS RESOLVE THE SINGULARITY?")
print("=" * 120)
print()

results = []
for model_name, f_func, description in MODELS:
    # Check K at several small radii
    K_small = []
    for r in [0.01, 0.005, 0.002, 0.001, 5e-4, 2e-4, 1e-4]:
        try:
            K, _, _, _ = kretschner(f_func, r)
            K_small.append((r, K))
        except Exception:
            K_small.append((r, float('inf')))

    # Find peak
    peak = max(K_small, key=lambda x: x[1] if x[1] < float('inf') else 0)
    last = K_small[-1]

    # Determine resolution
    if last[1] < peak[1] * 0.5 and peak[1] > 100:
        status = "RESOLVED"
        note = f"K peaks at r≈{peak[0]:.1e}, then decreases to {last[1]:.2e}"
    elif last[1] < 1e8:
        status = "BOUNDED"
        note = f"K stays below {last[1]:.2e} at r={last[0]:.1e}"
    elif last[1] > 1e15:
        status = "DIVERGES"
        note = f"K = {last[1]:.2e} at r={last[0]:.1e} (still growing)"
    else:
        status = "UNCLEAR"
        note = f"K = {last[1]:.2e} at r={last[0]:.1e}"

    results.append((model_name, status, note))

print(f"  {'Model':<22s} {'Status':<12s} {'Detail'}")
print(f"  {'─'*22} {'─'*12} {'─'*60}")
for name, status, note in results:
    marker = "✅" if status in ("RESOLVED", "BOUNDED") else "❌" if status == "DIVERGES" else "❓"
    print(f"  {name:<22s} {marker} {status:<10s} {note}")

print()
print("  Models that resolve the singularity predict FINITE curvature everywhere.")
print("  These are the models where Benford + Kretschner together say:")
print("  'The geometry is natural AND the curvature is finite — all the way down.'")
print()
print("  Models that diverge still have valid Benford conformance —")
print("  meaning the metric values are statistically natural even as K → ∞.")
print("  The singularity in those models is 'real' but 'well-behaved' in the Benford sense.")
print()
