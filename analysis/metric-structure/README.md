# Metric Structure Comparisons

**Author:** Christopher J. W. Riner
**Related:** Paper #7 — *Emergence of General Relativity from the Prime Number Structure of the Riemann Zeta Function* (DOI: 10.5281/zenodo.18751909)

---

## Overview

These scripts test where the prime-modified metric diverges from standard GR and how the zeta function should be embedded in the metric tensor. Key questions: Does the ζ pole at s = 1 produce a physical singularity? Does embedding ζ into all 4 components vs. using it as a scalar factor change physical predictions?

---

## Scripts

| # | Script | Description |
|---|--------|-------------|
| 1 | [black_hole_prime_metric.py](black_hole_prime_metric.py) | Compares prime metric vs standard GR at the horizon for solar-mass and Sgr A* black holes |
| 2 | [zeta_4d_pure.py](zeta_4d_pure.py) | Pure 4D comparison — all metric components scaled by ζ, no extra dimensions |
| 3 | [zenodo_zeta_4d_pure.py](zenodo_zeta_4d_pure.py) | Zenodo-submission copy of zeta_4d_pure.py |
| 4 | [zeta_embedded_vs_dimension.py](zeta_embedded_vs_dimension.py) | ζ embedded in metric vs ζ as separate scalar — physical consequences for BH and GPS |

---

## Key Finding

Both approaches (embedded and factored) reproduce standard Schwarzschild to high precision in the weak-field regime (GPS). They diverge only near the horizon (s → 1), where the Euler product's convergence boundary creates the domain wall identified in the Kretschner analysis.

---

## Session Notes

### 2026-02-25 — Embedding Comparison

**Takeaways:**
- Two valid approaches: ζ embedded into all 4 metric components vs ζ as a separate scalar factor — both reproduce weak-field physics (GPS match)
- Divergence only at the horizon (s → 1), where the Euler product hits its convergence boundary
- Pure 4D confirmed — no extra dimensions needed, ζ modifies existing metric rather than adding degrees of freedom
- Both solar-mass and Sgr A* black holes tested — prime metric matches standard GR in the exterior region

**Decisions:** Committed to embedded approach (ζ into g_tt and g_rr) for Paper 7. Kept zenodo_zeta_4d_pure.py as submission-ready duplicate.

**Open:** Does the factored approach have advantages for Kerr? Should zenodo_zeta_4d_pure.py be retired as a duplicate?

---

[← Back to Analysis](../) · [GR Emergence](../gr-emergence/) · [Kretschner Analysis](../kretschner/) · [GPS Tests](../gps/)
