# 1. Background

[← Index](README.md) | [Next: The Kretschner Scalar →](02-kretschner-scalar.md)

---

In Paper #7, we demonstrated that the Schwarzschild metric emerges from the Riemann zeta function through a three-step derivation:

1. **Postulate:** The metric components are identified with ζ(s):
   - g_rr(r) = ζ(s(r))
   - g_tt(r) = -1/ζ(s(r))

2. **Number-theoretic identity:** ζ(s) × 1/ζ(s) = 1 guarantees g_tt · g_rr = -1 at every radius, an algebraic consequence of the identity rather than a solution to coupled differential equations.

3. **Vacuum constraint:** Imposing R_μν = 0 (vacuum Einstein equations) with the AB = 1 condition reduces the field equations to d/dr[r · A(r)] = 1, which integrates to A(r) = 1 - r_s/r under asymptotic flatness.

The metric that emerges is exactly Schwarzschild:

> ds² = -(1 - r_s/r) dt² + (1 - r_s/r)⁻¹ dr² + r² dΩ²

The parameter s(r) is defined implicitly by ζ(s) = r/(r - r_s), giving:
- Near the horizon (r → r_s): s → 1⁺ (the pole of ζ)
- In the weak field (r ≫ r_s): s ≈ log₂(r/r_s)

The analysis in Paper #7 concluded that the event horizon represents a "wall" because the Euler product ∏(1-p⁻ˢ)⁻¹ diverges at s = 1. The present note investigates the nature of this wall using curvature invariants.
