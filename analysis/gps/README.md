# GPS Time Dilation Tests

**Author:** Christopher J. W. Riner
**Related:** Paper #5 — *River Velocity as Time Dilation: GPS Comparison* (DOI: 10.5281/zenodo.18705437); Paper #7 — *Emergence of GR from Prime Number Structure*

---

## Overview

These scripts validate the prime-modified metric against the GPS 38.6 μs/day time dilation — the most precisely measured gravitational effect on Earth. Three methods compared hour-by-hour over a full 24-hour UTC cycle: standard GR (g_tt), the beta parameter (β = √(r_s/r)), and ζ-modified g_tt.

---

## Files

| # | File | Description |
|---|------|-------------|
| 1 | [gps_24hr_comparison.py](gps_24hr_comparison.py) | Standard GR vs β parameter, hour-by-hour tables |
| 2 | [gps_24hr_zeta_on_time.py](gps_24hr_zeta_on_time.py) | Adds ζ(s)-modified g_tt as third method |
| 3 | [gps-analysis.html](gps-analysis.html) | Interactive browser visualization of GPS results |

## Research Notes

| Topic | File |
|-------|------|
| GPS validation results and next steps | [gps-validation.md](gps-validation.md) |

---

[← Back to Analysis](../) · [GR Emergence](../gr-emergence/) · [Metric Structure](../metric-structure/) · [Kretschner Analysis](../kretschner/)
