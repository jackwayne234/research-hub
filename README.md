# Riner Research Hub

**[Launch Live Dashboard](https://jackwayne234.github.io/research-hub/)**

An interactive research dashboard for independent physics, mathematics, and engineering research by Christopher Riner. 7 published papers, 7 interactive visualizations.

No build step required — pure HTML/CSS/JS. Open `index.html` locally or visit the live site above.

---

## Interactive Visualizations

| Visualization | Description |
|---|---|
| [Prime-Modified Metric](https://jackwayne234.github.io/research-hub/simulators/metric.html) | Flagship — Schwarzschild metric parameterized by ζ(s) |
| [GW150914 Zeta Fingerprint](https://jackwayne234.github.io/research-hub/analysis/gw150914_visualization.html) | Real LIGO data overlaid with zeta-predicted waveform |
| [Wormhole 3D Interactive](https://jackwayne234.github.io/research-hub/simulators/wormhole_3d_interactive.html) | 3D wormhole geometry from orbiting black holes |
| [Dimension Stack Chart](https://jackwayne234.github.io/research-hub/simulators/dimension_stack_chart.html) | Metric components stacked — contributions from far field to singularity |
| [Black Hole Simulator](https://jackwayne234.github.io/research-hub/simulators/blackhole-simulator.html) | Fall through the horizon, watch metric components evolve |
| [Einstein-Benford Black Hole](https://jackwayne234.github.io/research-hub/simulators/einstein_benford_blackhole.html) | Original Benford metric visualization |
| [Benford BH Bars](https://jackwayne234.github.io/research-hub/simulators/benford_blackhole_bars.html) | Bar chart analysis of Benford distributions in black hole data |

## Published Papers

| # | Title | Link |
|---|---|---|
| 1 | Modified Schwarzschild Metric via Benford's Law | [Zenodo 18553466](https://zenodo.org/records/18553466) |
| 2 | Bose-Einstein Condensates + Benford's Law | [Zenodo 18510250](https://zenodo.org/records/18510250) |
| 3 | Wavelength-Division Ternary Logic | [Zenodo 18437600](https://zenodo.org/records/18437600) |
| 4 | Optical AI Accelerator | [Zenodo 18501296](https://zenodo.org/records/18501296) |
| 5 | River Velocity as Time Dilation: GPS Comparison | [Zenodo 18705437](https://zenodo.org/records/18705437) |
| 6 | Prime Numbers as Causal Set Theory | [Zenodo 18731508](https://zenodo.org/records/18731508) |
| 7 | Emergence of General Relativity from the Prime Number Structure of the Riemann Zeta Function | [Zenodo 18751909](https://zenodo.org/records/18751909) |

## Directory Structure

```
research-hub/
├── index.html          Main dashboard (OS-style floating-window UI)
├── shared.css          Shared styles
├── pages/              Content pages (publications, projects, math journey, etc.)
├── simulators/         Interactive HTML visualizations (12 files)
├── analysis/           Python scripts + HTML analysis tools
├── tools/              Editor, calculator, git viewer
├── data/               JSON data for visualizations
├── drafts/             Active paper drafts
└── archive/            Superseded tool versions and conversation logs
```

## Research Threads

1. **Mathematics** — Prime numbers, zeta functions, causal set theory
2. **Physics** — Benford's Law in gravitational systems, prime-modified Schwarzschild metric
3. **Engineering** — Wavelength-division ternary optical computing, CubeSat lens design

## License

MIT
