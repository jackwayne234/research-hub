# 2. The Kretschner Scalar

[← Background](01-background.md) | [Index](README.md) | [Next: Results →](03-results.md)

---

## 2.1 Derivation

For a static, spherically symmetric metric of the form:

> ds² = -f(r) dt² + f(r)⁻¹ dr² + r² dΩ²

the non-zero orthonormal-frame Riemann tensor components are:

| Component | Expression |
|-----------|------------|
| R̂₀₁₀₁ | f''(r) / 2 |
| R̂₀₂₀₂ = R̂₀₃₀₃ | f'(r) / (2r) |
| R̂₁₂₁₂ = R̂₁₃₁₃ | -f'(r) / (2r) |
| R̂₂₃₂₃ | (1 - f(r)) / r² |

The Kretschner scalar is obtained by full contraction:

> K = R̂_abcd R̂^abcd = 4(R̂₀₁₀₁² + 2R̂₀₂₀₂² + 2R̂₁₂₁₂² + R̂₂₃₂₃²)

Since R̂₀₂₀₂² = R̂₁₂₁₂², this simplifies to:

> **K = f''(r)² + 4f'(r)²/r² + 4(1 - f(r))²/r⁴**

## 2.2 Schwarzschild Evaluation

For f(r) = 1 - r_s/r:
- f'(r) = r_s/r²
- f''(r) = -2r_s/r³

Substituting:

> K = (-2r_s/r³)² + 4(r_s/r²)²/r² + 4(r_s/r)²/r⁴
> K = 4r_s²/r⁶ + 4r_s²/r⁶ + 4r_s²/r⁶
> **K = 12r_s²/r⁶**

At the event horizon (r = r_s):

> **K(r_s) = 12/r_s⁴** (finite)

At the physical singularity (r → 0):

> K → ∞ (divergent)

## 2.3 Numerical Verification

The formula K = f'' ² + 4f'²/r² + 4(1-f)²/r⁴ was verified numerically against the exact expression K = 12r_s²/r⁶ using central-difference derivatives across the range r/r_s ∈ [1.001, 100]. Agreement was found to within relative error < 10⁻³ at all radii (limited by finite-difference step size, not the formula).
