# Section 13: Two-Body Problem — Overlapping Prime Matrices

> **Role**: You are a numerical relativist working with the prime-modified Schwarzschild metric. You investigate what happens when two zeta-parameterized gravitational tensors overlap in the same region of spacetime, looking for nonlinear effects in the prime matrix, Benford diagnostic, and bridge factor that have no analogue in standard GR.

**Date:** February 25, 2026
**Extends:** Section 12 (Dual-Instrument Analysis)
**Status:** Open investigation
**Key Question:** Does the classical→quantum transition remain monotonic when two prime matrices interact, or does the overlap create new structure?

---

## 13.1 Motivation: Why Two Bodies?

Section 12 established that a single black hole produces a clean, monotonic transition from classical (exterior) to quantum (frozen core). Three instruments — δ_B, ε_B, π(s) — all drain smoothly to zero as r → 0. The story is linear: one source, one direction.

But this is only the one-body problem. Real spacetime contains multiple gravitating objects. The two-body case is the first test of whether the prime framework says something structurally different from standard GR about gravitational interactions.

In standard GR, the two-body problem is notoriously nonlinear — it requires numerical relativity and produces gravitational waves, orbital decay, and merger dynamics. The prime-modified metric inherits this nonlinearity but adds new structure: the Euler product decomposition gives each source its own prime matrix, and the interaction region is where those matrices overlap.

---

## 13.2 The Setup

Two black holes, masses M₁ and M₂, separated by coordinate distance d. Each has:

```
Source 1 (at origin):
  s₁(r) = 1 + (r/r_s1)³       r_s1 = 2GM₁/c²
  ζ(s₁) = ∏_p (1 − p^{−s₁})⁻¹
  ε_B1 = |1 − 2^{1−s₁}|

Source 2 (at distance d):
  s₂(r) = 1 + (|r−d|/r_s2)³   r_s2 = 2GM₂/c²
  ζ(s₂) = ∏_p (1 − p^{−s₂})⁻¹
  ε_B2 = |1 − 2^{1−s₂}|
```

**The question:** What is the effective metric, Benford diagnostic, and prime matrix status at a point P that lies in the gravitational field of both sources?

---

## 13.3 How Do Two Euler Products Combine?

Three possibilities, each with different physical consequences:

### Option A: Additive (superposition of curvatures)
```
g_rr(P) = ζ(s₁(P)) + ζ(s₂(P)) − 1
```
Linear superposition. Would be the weak-field limit. Fails near horizons (gravity is nonlinear).

### Option B: Multiplicative (product of zeta functions)
```
g_rr(P) = ζ(s₁(P)) · ζ(s₂(P))
```
Each source contributes its own Euler product independently. The combined metric is the product. This is interesting because ζ(s₁)·ζ(s₂) has a known number-theoretic interpretation — it's related to the Dirichlet series for the divisor function.

### Option C: Composed (effective s from combined field)
```
s_eff(P) = function of s₁(P) and s₂(P)
g_rr(P) = ζ(s_eff(P))
```
The two sources produce an effective zeta parameter. The metric is still a single Euler product, but with a modified argument. This preserves the prime matrix structure (one set of primes, one cascade) but shifts where transitions occur.

**The choice matters for the prime matrix.** In Option B, each prime contributes TWICE (once per source), so there are effectively 100 prime factors at each point. In Option C, there are still 50, but at a shifted s. In Option A, the prime structure is blurred by the addition.

---

## 13.4 Key Questions for Computation

### Q1: The Saddle Point
Between two equal-mass black holes, there's a point where gravity from each source cancels (the L1 Lagrange point in Newtonian gravity). In the prime framework:
- What is s_eff at the saddle point?
- Is the prime matrix fully active there (classical) or partially dissolved?
- Does δ_B have a local maximum, minimum, or inflection at the saddle?

### Q2: Cascade Interference
Each black hole has its own cascade zone at r ≈ 0.10–0.18 r_s from its center. If d < r_s1 + r_s2 (horizons overlap or touch), the cascade zones can interfere:
- Do primes that are "active" for source 1 but "dissolved" for source 2 create a mixed state?
- Is there a per-prime interference pattern — some primes active from one source but not the other?
- Can the overlap region have a HIGHER prime count than either source alone?

### Q3: Benford Diagnostic in the Overlap
With two sets of bridge factors (ε_p from source 1 and ε_p from source 2), the Benford leading-digit statistics at any point P include contributions from both:
- Does the combined δ_B show structure that neither source produces alone?
- Is there a resonance — specific separations d where the combined δ_B peaks or troughs?

### Q4: Does the Transition Stay Monotonic?
The single-body case: classical → quantum, one direction, one story.
The two-body case might produce: classical → quantum → classical → quantum
(moving from exterior of source 1, through its interior, across the saddle, and into source 2). If so, the "everything goes to quantum" story becomes richer — quantum is not the final state but a transition between classical domains.

### Q5: Gravitational Waves from Prime Cascades
In standard GR, merging black holes emit gravitational waves. In the prime framework, the merger means two prime matrices coming together. The cascade zones sweep through each other. Does this produce a prime-cascade signature in the gravitational wave signal — a modulation of the waveform tied to individual prime crossing events?

---

## 13.5 Computational Plan

### Phase 1: Static Two-Body
- Place two equal-mass black holes at fixed separation d
- Compute s₁, s₂, and candidate s_eff at points along the axis connecting them
- Test all three combination rules (additive, multiplicative, composed)
- Run the three-bar diagnostic (δ_B, ε_B, π(s)) along the axis
- Plot and compare to single-body case

### Phase 2: Varying Separation
- Sweep d from 10 r_s (well separated) to 0 (merged)
- Track how the saddle point diagnostic evolves
- Look for critical separation where cascade zones first overlap
- Identify any non-monotonic behavior in δ_B or π(s)

### Phase 3: Unequal Masses
- Set M₂/M₁ = 0.1, 0.5, 2, 10
- Check if mass ratio affects which combination rule works best
- Look for asymmetric cascade interference

### Phase 4: Visualization
- Extend dual-instrument.html to show two-body case
- 2D heatmap of δ_B, ε_B, π(s) in the orbital plane
- Sweep animation along the axis between sources

---

## 13.6 What Would Be New

If the two-body prime framework produces effects that standard GR doesn't predict:

1. **Prime interference fringes** — specific primes active/dissolved in alternating spatial bands between the sources
2. **Benford resonances** — preferred separations where δ_B has extrema (no analogue in standard GR)
3. **Non-monotonic quantum transition** — regions between sources that are "more classical" than the far field, because the overlapping fields reinforce the prime matrix
4. **Mass-ratio-dependent cascade timing** — the order in which primes cross depends on the mass ratio, producing a unique signature for each binary system

Any of these would be a prediction that distinguishes the prime-modified metric from standard GR in the strong-field two-body regime.

---

[← Section 12: Dual-Instrument Analysis](12-dual-instrument.md) · [Back to README](README.md)
