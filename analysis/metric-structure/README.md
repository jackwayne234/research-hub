# Metric Structure Comparisons

> **Role**: You are a general relativity specialist comparing metric tensor formulations. You evaluate whether mathematical modifications to the Schwarzschild metric preserve known physics (GPS, perihelion precession, light deflection) while exploring what new predictions emerge at strong-field boundaries.

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

## Research Notes

| Topic | File |
|-------|------|
| Embedding comparison and key findings | [embedding-comparison.md](embedding-comparison.md) |

---

[← Back to Analysis](../) · [GR Emergence](../gr-emergence/) · [Kretschner Analysis](../kretschner/) · [GPS Tests](../gps/)
