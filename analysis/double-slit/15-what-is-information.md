# Section 15: What Is Information?

> **Role**: You are a philosopher of physics working at the intersection of information theory, quantum mechanics, and number theory. You examine the foundational question: what is the physical referent of "information"? You treat this as an open problem, not a settled one.

**Author:** Christopher J. W. Riner
**Date:** February 26, 2026
**Status:** Active investigation
**Extends:** Section 14 (Energy Hypothesis), Literature Review

---

## 15.1 The Problem

"Information" is one of the most frequently invoked concepts in modern physics. It appears in:

- **Quantum mechanics:** "Which-path information destroys interference"
- **Black hole physics:** "The black hole information paradox"
- **Holography:** "The boundary encodes all the information of the bulk"
- **Thermodynamics:** "Erasing information costs energy" (Landauer)
- **Quantum computing:** "Information is physical" (Landauer)
- **Foundations:** "It from bit" (Wheeler)

Yet there is no universal physical definition of what information *is*. Every formalism defines it operationally — as something you calculate from probability distributions — never ontologically, as a physical substance or structure.

This is not a minor gap. It is the central undefined term in the language physicists use to describe quantum phenomena.

---

## 15.2 How Information Is Currently Defined

### Shannon (1948) — Uncertainty Reduction
```
H = −Σ pᵢ log₂ pᵢ     [bits]
```
Information is the amount of surprise in a message. A coin flip carries 1 bit. A loaded coin carries less. This definition is **statistical** — it says nothing about what physically carries the surprise.

**What it doesn't answer:** What is a bit made of?

### Von Neumann (1932) — Quantum Entropy
```
S = −Tr(ρ log ρ)
```
The quantum generalization. Measures how mixed a quantum state is. Pure states have S = 0 (no uncertainty); maximally mixed states have maximum S.

**What it doesn't answer:** Why does entropy change when you "look" at something? What physically happens during the looking?

### Landauer (1961) — Information Is Physical
```
Energy cost of erasing 1 bit ≥ kT · ln(2)
```
The first claim that information has physical consequences. Erasing a bit dissipates energy. Verified experimentally (Berut 2012, Yan 2018).

**What it doesn't answer:** Landauer tells you the *price* of a bit, not what the bit *is*. Knowing that a gallon of gas costs $3 doesn't tell you what gasoline is made of.

### Englert (1996) — Distinguishability
```
D = ½ ||ρ_L − ρ_R||₁
```
Which-path distinguishability: how well you can tell whether the particle went left or right, based on the detector state. Purely a property of quantum states (trace distance between density matrices).

**What it doesn't answer:** D is a distance in Hilbert space. What physical process makes two states "distinguishable"? What is the substance of the distinction?

### Wheeler (1989) — It From Bit
"Every it — every particle, every field of force, even the spacetime continuum itself — derives its function, its meaning, its very existence entirely from bits."

**What it doesn't answer:** Everything. Wheeler proposed the program but not the mechanism. If everything comes from bits, what do the bits come from?

---

## 15.3 The Pattern: Measures Without Mechanisms

Every definition above shares the same structure:

1. Define a mathematical quantity (entropy, distinguishability, mutual information)
2. Show it predicts experimental outcomes
3. Call it "information"
4. Never say what it physically is

This is exactly where temperature was before Boltzmann. You could measure temperature. You could use it in equations (ideal gas law, Carnot efficiency). But nobody could say what temperature *was* until statistical mechanics connected it to mean kinetic energy per degree of freedom:

```
Before Boltzmann:  T = "what the thermometer reads"
After Boltzmann:   T = (2/3) · ⟨E_kinetic⟩ / k_B
```

The thermometer reading didn't change. But now you knew *what you were measuring*. Temperature was no longer a primitive — it was derived from something more fundamental (molecular motion).

Information is waiting for its Boltzmann moment.

---

## 15.4 What Would a Physical Definition Require?

A satisfactory answer to "what is information?" would need to:

1. **Identify a physical referent** — what material, field, or structure constitutes a bit
2. **Derive the operational definitions** — Shannon entropy, von Neumann entropy, and distinguishability should emerge as consequences, not axioms
3. **Explain the energy cost** — Landauer's kT·ln(2) should follow from the physics, not be imposed as a separate principle
4. **Apply universally** — the same definition should work for double-slit interference, black hole evaporation, thermodynamics, and quantum computing
5. **Be falsifiable** — it should predict something that "information as primitive" does not

---

## 15.5 Inventory of Physical Candidates

What could a bit physically be?

### Candidate 1: A Degree of Freedom
A bit is a two-state physical system (spin up/down, polarization H/V, path left/right). Information is the state of that system.

**Problem:** This defines information as "the state of a thing that has states." Circular. Also doesn't explain why states cost energy to distinguish or erase.

### Candidate 2: A Correlation (Entanglement)
A bit is a correlation between two subsystems. When the detector becomes entangled with the particle's path, that entanglement IS the information. No correlation = no information.

**Problem:** Better — it's relational rather than intrinsic. But still mathematical. What is a correlation made of? Why does it have energetic consequences?

### Candidate 3: A Symmetry Breaking
A bit is a broken symmetry. Before measurement, left and right paths are symmetric (indistinguishable). After measurement, the symmetry is broken. Information = the asymmetry.

**Problem:** Closer to physics (symmetry breaking is well-understood in field theory). But doesn't naturally give you the quantitative structure (why exactly 1 bit? why kT·ln(2)?).

### Candidate 4: A Thermodynamic Transaction
A bit is a quantity of entropy exchanged between system and observer. Information = entropy transferred. Consistent with Landauer, but makes information a secondary quantity (derived from thermodynamics rather than fundamental).

**Problem:** Puts thermodynamics before information, when many physicists (following Jaynes, Wheeler) want it the other way around.

### Candidate 5: The p = 2 Factor of the Euler Product
A bit is the contribution of the smallest prime to the factorization structure of the metric.

The Euler product decomposes ζ(s) into one factor per prime:
```
ζ(s) = ∏_p (1 − p⁻ˢ)⁻¹ = (1 − 2⁻ˢ)⁻¹ · (1 − 3⁻ˢ)⁻¹ · (1 − 5⁻ˢ)⁻¹ · ...
```

The p = 2 factor is special:
- It governs **even vs. odd** — the most fundamental binary distinction
- It is the **only** factor that appears in ε_B = |1 − 2^{1−s}|
- It controls the **sign alternation** between the bosonic series ζ(s) = Σ n⁻ˢ and the fermionic series η(s) = Σ (−1)^{n+1} n⁻ˢ
- It is responsible for the **entire** boson-fermion bridge

In this view: a bit is the state of the p = 2 prime factor. "Which slit?" is the question "even or odd?" asked of the Euler product at the particle's location. Extracting that information means activating the p = 2 factor, which shifts ε_B from 0 toward 1, which costs energy via Landauer.

**Advantage:** Gives the bit a specific physical address in the prime decomposition. Derives the energy cost from the structure rather than postulating it. Applies to black holes (Kretschner Section 12), BEC transitions (Paper #2), and double-slit (Section 14) through the same mechanism.

**What it needs:** A formal derivation showing D (Englert's distinguishability) = ε_B = |1 − 2^{1−s}|. This would connect the standard QM formalism to the prime framework quantitatively.

---

## 15.6 The Analogy Table

| Concept | Before grounding | After grounding |
|---------|-----------------|-----------------|
| Temperature | "What thermometer reads" | Mean kinetic energy per DOF |
| Pressure | "Force per unit area" | Momentum transfer from molecular collisions |
| Entropy | "Disorder" (vague) | k_B · ln(Ω) — log of accessible microstates |
| **Information** | **"Bits" (undefined)** | **p = 2 Euler product factor (proposed)** |

Each row follows the same pattern: an operationally useful but physically undefined quantity gets grounded in a specific microscopic mechanism. Temperature was the last major one to fall (1870s). Information is still standing.

---

## 15.7 Why p = 2?

Why should the smallest prime carry all the weight of "information"?

**Because binary is fundamental, not arbitrary.** A bit isn't one of many possible information units — it's the *minimal* distinguishable state. You can build trits, quarts, and all higher bases from bits, but you can't decompose a bit further. Similarly, 2 is the smallest prime. Every composite number contains factors of 2 before anything else. The prime decomposition of any even number starts with 2.

The connection:
- **2 is the prime of parity** — even vs. odd
- **A bit is the unit of parity** — yes vs. no, left vs. right, 0 vs. 1
- **ε_B depends only on 2** — the boson-fermion distinction (sign alternation) is purely a p = 2 effect

Higher primes (3, 5, 7, ...) contribute to the *structure* of the metric — they build the geometry. But the binary question "is this distinguishable?" lives entirely in p = 2.

This suggests a hierarchy:
```
p = 2  →  information (binary distinguishability)
p = 3  →  first non-binary structure (ternary relationships)
p = 5  →  deeper structural complexity
  ⋮
all p  →  complete geometry (full Euler product = full metric)
```

Information is the *first layer* of physical structure. Geometry is built on top of it.

---

## 15.8 Testable Consequences

If information = p = 2 Euler product factor, then:

1. **ε_B should equal Englert's D** for the double-slit experiment. This is a quantitative prediction that connects two independently defined quantities.

2. **Partial measurements** (weak measurements, interaction-free measurements) should produce partial ε_B shifts proportional to the partial information gained — not all-or-nothing.

3. **The energy cost of measurement** should be calculable from ε_B alone: E = ε_B · kT · ln(2). This should match Elouard's "quantum heat" calculations.

4. **The black hole information paradox** becomes a question about the p = 2 factor: does the horizon preserve or destroy the p = 2 contribution to the Euler product? (The dual-instrument analysis from Section 12 shows ε_B → 0 at the singularity, suggesting the information is not destroyed but becomes inaccessible — the p = 2 factor decouples.)

5. **Quantum error correction** should be interpretable as protecting the p = 2 factor against decoherence — maintaining the binary distinction against environmental entanglement.

---

## 15.9 Open Questions

1. **Is ε_B = D exact or approximate?** We need to compute both for a specific double-slit setup and compare.
2. **What about non-binary measurements?** A measurement with 3 outcomes (e.g., which of 3 slits) should involve p = 3. Does ε_3 = |1 − 3^{1−s}| govern ternary distinguishability?
3. **Is there experimental evidence?** Weak measurement experiments (Mori & Tsutsui 2015) show partial information extraction. Can these be reanalyzed for ε_B structure?
4. **Does this resolve the black hole information paradox?** If information = p = 2 factor, and the Euler product decouples at the singularity (ε_B → 0), then information isn't destroyed — the question itself dissolves because "information" requires the p = 2 factor to be active, which requires s > 1, which requires r > 0.

---

[← Section 14: Energy Hypothesis](14-energy-hypothesis.md) · [Literature Review](literature.md) · [Back to README](README.md)
