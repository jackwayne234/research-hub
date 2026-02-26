# GR Emergence from Prime Number Structure

**Author:** Christopher J. W. Riner
**Related:** Paper #7 — *Emergence of General Relativity from the Prime Number Structure of the Riemann Zeta Function* (DOI: 10.5281/zenodo.18751909)

---

## Overview

This directory contains the iterative development of the core result: general relativity emerges from the Riemann zeta function. The Schwarzschild metric is reconstructed as g_tt = −1/ζ(s), g_rr = ζ(s), with the constraint ζ(s) × 1/ζ(s) = 1 encoding flat spacetime as the identity.

---

## Scripts

| # | Script | Description |
|---|--------|-------------|
| 1 | [gr_emergence_from_primes.py](gr_emergence_from_primes.py) | v1 — Builds metric from ζ(s) via Euler product, tests GPS 38.6 μs/day emergence |
| 2 | [gr_emergence_v2.py](gr_emergence_v2.py) | v2 — Uses Chebyshev ψ(x) and Riemann explicit formula instead of direct ζ |
| 3 | [gr_emergence_v3.py](gr_emergence_v3.py) | v3 — Frames as ζ(s) × 1/ζ(s) = 1 symmetry, inverts ζ to find s(r) |
| 4 | [gr_emergence_v4.py](gr_emergence_v4.py) | v4 — Full derivation with BEC bridge: bosonic gravity (ζ) vs fermionic matter (η) |

## Notes

| File | Description |
|------|-------------|
| [prime_to_gr_notes.md](prime_to_gr_notes.md) | Scratch notes — 3-phase test plan that seeded v1 |

---

## Key Result

The radial mapping s(r) = 1 + (r/r_s)³ with α = 3 reproduces standard Schwarzschild to machine precision at all radii, while the Euler product ∏(1−p⁻ˢ)⁻¹ diverges at s = 1 (the horizon) — a domain boundary, not a curvature singularity.

---

[← Back to Analysis](../) · [Kretschner Analysis](../kretschner/) · [Metric Structure](../metric-structure/) · [GPS Tests](../gps/)
