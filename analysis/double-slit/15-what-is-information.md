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

1. **Identify a physical referent** — what material, field, or structure constitutes information
2. **Derive the operational definitions** — Shannon entropy, von Neumann entropy, and distinguishability should emerge as consequences, not axioms
3. **Explain the energy cost** — Landauer's kT·ln(2) should follow from the physics, not be imposed as a separate principle
4. **Apply universally** — the same definition should work for double-slit interference, black hole evaporation, thermodynamics, and quantum computing
5. **Be falsifiable** — it should predict something that "information as primitive" does not

---

## 15.5 The Answer: Information Is Order. It Lives in the Integers.

### The prime numbers are the foundation

The primes have no closed-form formula. Their distribution appears random. No algorithm can predict the next prime from the previous ones without checking. They are the irreducible, patternless atoms of arithmetic — *pure disorder*. But they are not information. They are the foundation that information is built on.

### The integers are the information

1, 2, 3, 4, 5, ... — a sequence with total regularity. Every integer has a unique place. The structure is complete, predictable, and infinite. This is where information lives: in the ordered structure that the primes produce.

The Fundamental Theorem of Arithmetic: every integer > 1 factors uniquely into primes. The perfectly disordered primes, through multiplication alone, produce the perfectly ordered integers. No information was put in. Order emerged.

The Euler product is the mathematical statement of this fact:

```
∏_p (1 − p⁻ˢ)⁻¹  =  Σ_n n⁻ˢ

  product over primes     sum over integers
    (foundation)           (information)
```

The left side is a product over primes — the foundation. The right side is a sum over integers — the information. They are identically equal. The foundation produces the order.

### Everything in spacetime has information

Anything that exists in a dimension — matter, light, fields, radiation — is ordered. It has structure. Therefore it has information, and that information can be measured with Benford's Law.

This follows directly from the metric. The spacetime metric is built from ζ(s), which is the sum over all integers. Anything that lives in that metric inherits the integer structure. To exist in spacetime *is* to carry order. There is no such thing as a physical entity with zero information — existence and order are the same thing.

### The proposal

- **Information = order**
- **Order = the structure of the integers**
- **Primes = the foundation** (not information themselves, but what information is built on)
- **Existence in spacetime = possession of order** (everything physical has information)
- **Benford's Law = the empirical signature of integer-generated order**
- **δ_B = the quantitative measure of how much order is present**

A physical system that conforms to Benford's Law is one whose internal structure reflects the integer structure — the order built on the prime foundation. A system that deviates from Benford has lost some of that structure. δ_B measures how much.

This is not a metaphor. In the BEC analysis (Paper #2), δ_B = 0 corresponds to the quantum/bosonic regime — maximum order. Large δ_B corresponds to the massive/classical regime — order broken. The spectrum is continuous. Nothing is ever purely one or the other.

---

## 15.6 The Metric as Order × Disorder

In the prime-modified Schwarzschild metric (Paper #1), spacetime itself carries this structure:

```
ζ(s) × 1/ζ(s) = 1

g_tt  ×  g_rr   = −1
```

- **ζ(s)** — the sum over integers — encodes the ordered face of the metric (time component)
- **1/ζ(s)** — the Möbius inversion, encoding the prime foundation — is the foundation face (radial component)
- **Their product is the identity** — information and its foundation are inseparable; neither exists without the other

The metric *is* the statement that information (order/integers) and its foundation (primes) coexist at every point in spacetime. The parameter s = 1 + (r/r_s)³ controls how much of each face is visible. Far from a mass (large s), the integer structure dominates — the system is ordered, quantum effects are small. Near a singularity (s → 1), the structure dissolves — the Euler product diverges, the integers lose their grip, and order breaks down.

---

## 15.7 Why Benford's Law Is the Right Measure

Benford's Law states that in naturally occurring datasets, the first digit d appears with probability:

```
P(d) = log₁₀(1 + 1/d)
```

This distribution is not arbitrary. It is the *unique* distribution that is:
- **Scale invariant** — it doesn't change if you switch units (meters to feet, dollars to yen)
- **Base invariant** — it holds in any number base, not just base 10
- **Multiplicatively generated** — it emerges from any process involving multiplication of independent factors

These are exactly the properties of the integer structure generated by primes. Multiplication of primes produces integers. The logarithmic spacing of the Benford distribution reflects the logarithmic spacing of prime factorizations.

Benford conformance is universal because the integers are universal. Any system whose structure is generated multiplicatively — which includes nearly all physical systems (exponential growth, power laws, scale-free processes) — inherits the Benford signature.

### Connection to the Principle of Least Action

The principle of least action states that physical systems follow the path that extremizes the action integral: δS = 0, where S = ∫ L dt. Nature chooses the most efficient path — no wasted motion, no unnecessary structure.

Benford's distribution is the least-action distribution for first digits. It is what you get when a system follows the most natural multiplicative path — no extra constraints imposed, no artificial structure added, just the path of least resistance through the integer structure. Scale invariance (the defining property of the Benford distribution) is the first-digit equivalent of the variational principle: the distribution that doesn't change under rescaling is the one that requires no additional information to specify.

This parallel is not coincidental. The principle of least action governs *dynamics* — how systems evolve in time. Benford's Law governs *statistics* — how naturally ordered systems distribute their values. Both are statements about what happens when nature is left alone: it follows the most efficient path. In the prime framework, both trace back to the same source — the integer structure built on the prime foundation. The action principle selects the path; Benford's Law is the statistical signature that the path was selected naturally.

**What δ_B measures:**
- **δ_B ≈ 0:** The system's first-digit distribution matches Benford. The integer structure is intact. Maximum order. Quantum/bosonic.
- **δ_B large:** The system deviates from Benford. The integer structure is broken. Order lost. Mass-like/classical.
- **δ_B intermediate:** Partial order. The system sits somewhere on the quantum-to-mass spectrum.

This has been empirically tested:
- **BEC transitions** (Paper #2): δ_B tracks the quantum-to-classical crossover continuously
- **Kretschner scalar** (Sections 10–12): δ_B maps the singularity-to-exterior transition in black hole spacetimes
- **Practical applications:** Benford conformance tests the reliability of AI models, financial data integrity, and any dataset where natural order should be present

---

## 15.8 Entropy Is the Return to Benford

The Second Law of Thermodynamics says entropy always increases. But "disorder" has never been grounded physically. In this framework, it is:

**Entropy increase = return to Benford conformance.** A system naturally relaxes toward the least-action distribution — the Benford distribution — where no prime is favored over any other. δ_B decreases over time. That is what entropy *is*: the drive back to the natural integer structure.

Building anything — a crystal, an organism, a machine — means moving *away* from Benford. Imposing structure on the prime foundation. Favoring certain configurations. That costs energy, because you are fighting the principle of least action.

```
Building (structure):   δ_B increases    (costs energy, fights least action)
Entropy (relaxation):   δ_B decreases    (releases energy, follows least action)
Equilibrium:            δ_B → 0          (Benford conformance, the natural state)
```

Landauer's kT·ln(2) is the energy cost of moving one bit away from Benford — imposing one binary constraint on the prime foundation. The Second Law says the universe will undo that constraint given enough time. Heat death is Benford conformance: everything relaxed back to the foundation.

### Macro vs. micro

This picture has an important subtlety. Individual components of a system can and do deviate from Benford — they have mass, structure, constraints. A single atom in a crystal is highly constrained. But a system *works* — is natural, functional, stable — when the macro-level statistics are Benford-like.

A healthy financial market: each transaction has specific structure, but the aggregate of all transactions follows Benford. When someone fabricates data, the macro-level Benford conformance breaks. The system stops working.

A Bose-Einstein condensate: each atom is in the ground state (maximally constrained), but the condensate as a whole is maximally Benford-conformant. The information is a macro-level property, not a per-component property.

This is why Benford is diagnostic: it tests whether the macro-level order is natural. Individual deviations are expected and necessary (structure requires them). But when the aggregate deviates, something has gone wrong — the system is being driven by artificial constraints rather than the natural integer structure.

---

## 15.9 The Operational Definitions Follow (Previously Axioms, Now Consequences)

If information = order (integer structure), then the existing operational definitions become *consequences*, not axioms:

### Shannon entropy
Shannon's H = −Σ pᵢ log₂ pᵢ measures how far a probability distribution deviates from the structure that would be present if the system were fully ordered. It quantifies surprise *relative to* the integer-generated baseline. Maximum entropy = maximum deviation from order = minimum information.

### Landauer's principle
Erasing a bit costs kT·ln(2) because you are destroying order — removing integer structure from the physical system. The energy cost is the thermodynamic price of undoing what the primes generated. You cannot erase order for free because the Second Law protects the integer structure.

### Englert's distinguishability
D measures how much integer structure the detector has captured from the system. Full distinguishability (D = 1) means the detector has absorbed the complete path information — the full order. No distinguishability (D = 0) means no order has been transferred. The complementarity relation D² + V² = 1 becomes a conservation law: order is conserved between the interference pattern (V) and the detector (D).

### Wheeler's "it from bit"
Wheeler was right that physical reality derives from information, but wrong about the unit. It's not "it from bit." It's **order from primes**. The bit (binary distinction) is a consequence of the simplest prime (p = 2), not the foundation.

---

## 15.10 The Role of p = 2

The bridge factor ε_B = |1 − 2^{1−s}| plays a special role in this framework, but it is not the *definition* of information. It is the simplest generator.

p = 2 is the smallest prime. It creates the most fundamental binary partition: even vs. odd. In the Euler product, the p = 2 factor governs the sign alternation between the bosonic series ζ(s) = Σ n⁻ˢ and the fermionic series η(s) = Σ (−1)^{n+1} n⁻ˢ:

```
η(s) = (1 − 2^{1−s}) · ζ(s)
```

The factor (1 − 2^{1−s}) is what connects the boson sector to the fermion sector. It is the bridge between the two fundamental types of particle statistics. In the double-slit experiment, the measurement asks a binary question (which slit?), which activates the p = 2 factor specifically.

But p = 2 is one generator among infinitely many. Higher primes (3, 5, 7, ...) generate deeper structural complexity:

```
p = 2  →  binary distinction (even/odd, left/right, boson/fermion)
p = 3  →  first non-binary structure (ternary relationships)
p = 5  →  deeper structural complexity
  ⋮
all p  →  complete integer structure (all information)
```

Information is the full order — all integers, all primes contributing. The bit (p = 2) is where it starts, not where it ends.

---

## 15.11 Testable Consequences

1. **δ_B should track distinguishability.** In any experiment where which-path information is varied continuously (e.g., partial erasure, weak measurement), δ_B computed from the experimental data should correlate with Englert's D. This connects the Benford framework to standard quantum mechanics quantitatively.

2. **Benford conformance should predict quantum coherence.** Systems that conform to Benford's Law should exhibit quantum behavior (interference, entanglement). Systems that deviate should behave classically. This is already consistent with the BEC results but should be tested in other systems (superconductors, superfluids, photonic crystals).

3. **The energy cost of measurement should correlate with δ_B shift.** When a measurement changes δ_B by Δδ_B, the energy dissipated should be proportional to Δδ_B · kT. This connects Landauer to Benford quantitatively.

4. **Benford deviation should detect unreliable models.** Any predictive model (AI, climate, financial) whose outputs deviate from Benford when the underlying phenomenon should conform is unreliable — it has failed to capture the natural order. This is a practical, immediately testable application.

5. **The black hole information paradox reframes.** If information = integer-generated order, and the Euler product diverges at s → 1 (the singularity), then information isn't "destroyed" — the integer structure itself breaks down. The question "where does the information go?" dissolves because "information" requires the integer structure to be defined, and that structure requires s > 1.

---

## 15.12 The Analogy Table

| Concept | Before grounding | After grounding |
|---------|-----------------|-----------------|
| Temperature | "What thermometer reads" | Mean kinetic energy per DOF |
| Pressure | "Force per unit area" | Momentum transfer from molecular collisions |
| Entropy | "Disorder" (vague) | k_B · ln(Ω) — log of accessible microstates |
| Entropy (this work) | "Disorder" (still vague) | Return to Benford conformance — δ_B → 0 via least action |
| **Information** | **"Bits" (undefined)** | **Order — the integer structure built on the prime foundation, measured by Benford conformance (δ_B)** |

---

## 15.13 Open Questions

1. **Can δ_B = D be shown formally?** The Benford deviation and Englert's distinguishability should be related. Deriving the exact relationship would connect the prime framework to standard QM.

2. **What is the role of individual primes beyond p = 2?** The full integer structure involves all primes. In what physical situations do p = 3, p = 5, etc. become individually relevant? Multi-slit experiments are one candidate (see Section 15.9), but this needs formal development.

3. **Does Benford conformance hold in quantum gravity regimes?** Near the Planck scale, does δ_B → 0 (maximum order) or does the integer structure itself break down? The answer distinguishes between different quantum gravity programs.

4. **Is there a conservation law for order?** The complementarity relation D² + V² = 1 suggests that order is conserved — it moves between system and detector but is never created or destroyed. Can this be generalized beyond the double-slit?

5. **What breaks the order?** If primes generate order through multiplication, what physical process undoes it? Decoherence is the standard answer, but in this framework it should be describable as a loss of multiplicative structure — the system's first-digit distribution drifting away from Benford.

---

[← Section 14: Energy Hypothesis](14-energy-hypothesis.md) · [Literature Review](literature.md) · [Back to README](README.md)
