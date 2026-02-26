# 8. The Benford Epsilon: Mass-Quantum Spectrum from the BEC Paper

[← Nine QG Models](07-nine-models.md) | [Index](README.md) | [Next: Double-Slit Prediction →](09-double-slit.md)

---

## 8.1 Origin: Paper #2 (Bose-Einstein Condensates + Benford's Law)

Paper #2 established that the Bose-Einstein distribution 1/(e^x - 1) is the **unique** quantum statistical distribution satisfying Benford's Law exactly at all temperatures. The key results:

- **Bosonic systems (BEC):** Completely monotone series with exclusively non-negative coefficients. δ_B = 0 at all temperatures — perfect Benford conformance.
- **Fermionic systems (Fermi-Dirac):** Alternating series. Produces calculable periodic deviations from Benford's Law: oscillations with period exactly 1 in log₁₀(T), amplitude governed by the Dirichlet eta function η(s).
- **Physical implication:** No fermion can have zero Benford deviation, implying that massless fermions cannot exist.

The boson-fermion bridge is the Dirichlet eta function:

> η(s) = (1 - 2^(1-s)) · ζ(s)

The factor **(1 - 2^(1-s))** involves only the prime p = 2 — the first prime is what separates bosonic from fermionic physics. In the prime framework (Paper #7), where g_rr = ζ(s(r)), this factor becomes radius-dependent through the mapping s(r).

## 8.2 Benford Deviation as a Mass-Quantum Spectrum

Paper #2's central finding reframes δ_B as more than a statistical diagnostic:

> **δ_B is not a threshold — it is the observable.** It measures the mass-quantum character of the system.

The spectrum:

| δ_B | Character | Physical meaning |
|-----|-----------|-----------------|
| 0 | Purely bosonic | Fully quantum (wavelike, delocalized, interference) |
| Small | Mostly bosonic | Predominantly quantum with slight massive tendency |
| Large | Mostly fermionic | Predominantly massive (particlelike, localized) |

**Nothing is ever fully one or the other.** Everything exists in a constant state between fully massive and fully quantum. δ_B measures where on this spectrum a system sits at any given moment.

## 8.3 The Bridge Factor as ε_B(r)

The boson-fermion bridge factor gives a natural, physics-derived definition of ε_B:

> **ε_B(s) = |1 - 2^(1-s)|**

This is the fermionic Benford deviation — the scale at which quantum statistics itself produces deviation from perfect Benford conformance. Through the mapping s(r), it becomes radius-dependent:

| r/r_s | s(r) | ε_B = \|1-2^(1-s)\| | Observed δ_B | δ_B < ε_B? | Character |
|-------|------|---------------------|-------------|------------|-----------|
| 100.0 | 6.74 | 0.981 | 0.028 | YES | Quantum |
| 10.0 | 3.65 | 0.841 | 0.028 | YES | Quantum |
| 2.0 | 1.73 | 0.396 | 0.003 | YES | Quantum |
| 1.1 | 1.05 | 0.035 | 0.002 | YES | Quantum |
| 1.01 | 1.01 | 0.007 | 0.004 | YES (barely) | Quantum |
| **1.001** | **1.001** | **0.0007** | **0.004** | **NO** | **Crossing point** |
| 0.99 | ~0.99 | 0.007 | 0.004 | YES | Quantum |
| 0.5 | ~0.5 | 0.414 | 0.005 | YES | Quantum |
| 0.1 | ~0.1 | 0.866 | 0.017 | YES | Quantum |
| 0.01 | ~0.01 | 0.986 | 0.015 | YES | Quantum |

Properties of ε_B(s):
- **ε_B → 1** as s → ∞ (far field): maximum separation between boson and fermion statistics
- **ε_B = 0.5** at s = 2 (moderate field): equal boson-fermion character
- **ε_B → 0** as s → 1 (horizon): **boson and fermion statistics merge**
- **ε_B grows again** for s < 1 (interior): bridge factor reopens symmetrically

## 8.4 The Horizon Crossing: Irreducible Fermionic Signature

The bridge factor vanishes at the horizon (s = 1, ε_B = 0), yet the observed Benford deviation is δ_B ≈ 0.004. This is the **only point in the entire trajectory** where δ_B exceeds ε_B.

Interpretation: at the horizon, bosonic and fermionic statistics are indistinguishable (η(1) = ln 2, finite, while ζ(1) diverges — but their ratio approaches zero). The non-zero δ_B at this point is an **irreducible fermionic signature** — a residual mass-like character of the geometry that cannot be eliminated by any representation of ζ(s). This is where the Euler product breaks, where the prime structure ends, and where the geometry carries its maximum massive character relative to the quantum baseline.

## 8.5 The Mass-Quantum Profile of a Black Hole Interior

Combining δ_B (observed) with the mass-quantum interpretation from Paper #2:

| r/r_s | δ_B | Mass-quantum character |
|-------|-----|----------------------|
| 10.0 | 0.028 | Marginal — far field, sparse data |
| 2.0 | 0.003 | Almost purely quantum/bosonic |
| 1.1 | 0.002 | Most quantum point in trajectory |
| 1.001 | 0.004 | Quantum, but approaching mass crossing |
| 0.99 | 0.004 | Just inside: still quantum |
| 0.5 | 0.005 | Slightly more massive |
| 0.3 | 0.013 | Trending toward mass |
| **0.1** | **0.017** | **Most massive point in trajectory** |
| 0.04 | 0.017 | Plateau at maximum mass character |
| 0.01 | 0.015 | **Recovering toward quantum** |

The geometry gets **more mass-like as you fall in**, peaks around r ≈ 0.1 r_s, then begins recovering toward quantum character. It never reaches either extreme. The interior of a black hole, viewed through the mass-quantum spectrum, is a smooth gradient — not a discontinuous collapse.
