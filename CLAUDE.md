# Research Hub — AI Navigation Guide

## Owner
Christopher Jack Wayne Riner (CJ). AI assistant: Barron (named after his favorite cat).

## What This Is
A self-contained research dashboard and interactive visualization hub.
Serves as the central portal for CJ's independent physics and mathematics research.
No build step — open index.html in a browser or serve via GitHub Pages.

## Directory Structure
```
research-hub/
├── index.html              # Main dashboard (floating-window OS-style UI)
├── shared.css              # Shared styles for all sub-pages
├── pages/                  # Content pages (loaded as iframes from index.html)
│   ├── big-picture.html    # Substrate cycle theory overview
│   ├── daily-practice.html # Math practice tracker
│   ├── math-journey.html   # Notation learning progress
│   ├── projects.html       # Active research projects
│   ├── publications.html   # 6 published Zenodo papers
│   ├── research-feed.html  # Automated paper feed
│   ├── speculative.html    # Untested theoretical directions
│   ├── substrate.html      # 6th dimension substrate theory
│   ├── visualizations.html # Gallery of 7 interactive visualizations
│   ├── log-roadmap.html    # Session log and roadmap
│   ├── status.html         # Tool/visualization status report
│   └── working-index.html  # Working scratchpad
├── simulators/             # Interactive HTML visualizations
│   ├── metric.html         # 5D Prime-Modified Metric (flagship)
│   ├── blackhole-simulator.html
│   ├── orbit-simulator.html
│   ├── substrate-explorer.html
│   ├── expedition.html     # Space expedition game
│   ├── outpost.html
│   └── (5 more visualization HTMLs)
├── analysis/               # Python analysis scripts + HTML visualizations
│   ├── zeta_4d_pure.py     # 4D zeta function analysis
│   ├── ligo_gw150914_analysis.py
│   ├── gw150914_visualization.html  # LIGO substrate fingerprint
│   └── (more analysis files)
├── tools/                  # Utility tools
│   ├── editor.html         # Manuscript editor (self-contained, no CDN)
│   ├── calculator.html     # Math calculator widget
│   ├── git-viewer.py       # Local git repository viewer
│   └── (more tool files)
├── data/                   # JSON data files for visualizations
├── drafts/                 # Active paper drafts (.docx)
├── archive/                # Superseded files
│   ├── tools/              # Old tool versions
│   └── logs/               # AI conversation transcripts
└── README.md               # Human-facing project overview
```

## Research Context
Three interconnected threads:
1. **Mathematics** — Prime numbers, zeta functions, causal set theory
2. **Physics** — Benford's Law in gravitational systems, 5D prime-modified Schwarzschild metric, substrate theory
3. **Engineering** — Optical computing, ternary logic, CubeSat lens design

## Key Files
- `index.html` — Entry point. OS-style UI with sidebar navigation and floating windows.
- `pages/publications.html` — Lists all 6 Zenodo papers with DOIs.
- `simulators/metric.html` — The flagship 5D prime metric visualization.
- `analysis/gw150914_visualization.html` — Real LIGO data with zeta-predicted overlay.

## Published Papers (6 total)
1. Modified Schwarzschild Metric via Benford's Law
2. Bose-Einstein Condensates + Benford's Law
3. Wavelength-Division Ternary Logic
4. Optical AI Accelerator
5. River Velocity as Time Dilation: GPS Comparison
6. Prime Numbers as Causal Set Theory

## GitHub
- Repo: github.com/jackwayne234/research-hub
- Live: https://jackwayne234.github.io/research-hub/
