# 11. Computational Resources

[← Next Steps](10-next-steps.md) | [Index](README.md) | [References →](references.md)

---

All numerical results were produced by scripts in the parent directory:

**Kretschner analysis:** `../kretschner_scalar.py`
- Python 3 with mpmath 1.4.0 for analytic continuation of ζ(s)
- Euler product over first 10,000 primes for s > 1
- Central-difference numerical derivatives for K verification

**Nine-model Kretschner analysis:** `../nine_models_kretschner.py`
- Python 3, pure standard library (math module only)
- 10 models: Standard GR + 9 quantum gravity (Loop QG, Asymptotic Safety, Non-Comm Geometry, String/GUP, Causal Sets, CDT, Twistor, Group Field Theory, Emergent Gravity)
- Central-difference numerical derivatives with adaptive step size
- 29 radial positions from r/r_s = 10 to 10⁻⁴
- Comparison matrix, Benford epsilon concept, singularity resolution verdict

**Benford trajectory:** `../../simulators/benford_blackhole_bars.html`
- 40 pre-computed radial positions from r/r_s = 10.0 to 0.01
- Per-digit deviations ε(d) and total deviation delta_B at each position
- Metric components g_tt, g_rr, g_θθ, g_φφ, g_δ with floor regularization
- Interactive visualization with real-time HUD and delta chart

**GR emergence with BEC bridge:** `../gr_emergence_v4.py`
- Complete monotonicity proof for ζ(s)
- Boson-fermion bridge: η(s) = (1-2^(1-s))·ζ(s)
- GPS verification of emerged metric
