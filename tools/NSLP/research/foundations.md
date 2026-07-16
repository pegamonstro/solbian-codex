# Mathematical Foundations of NSL

> The seven algorithmic pillars underlying the NSL ISA:
> fixed-point combinators, CPS, abstract interpretation,
> term rewriting, category theory, information geometry,
> and optimal transport.
>
> Status: **Research notes** (sapling prototype)

---

## 1. Fixed-Point Combinators for Recursive Cognition

### 1.1 The Problem

NSL primitives are non-recursive. Recursive cognitive
operations (self-reflection, iterative improvement,
recursive planning) must be built from non-recursive parts.

### 1.2 The Solution: Y Combinator

```
Y = λf. (λx. f (x x)) (λx. f (x x))
```

In NSL, the Y combinator enables recursion without requiring
a recursive primitive:

```
(define (fix f)
  (call (lambda (x) (call f (call x x)))
        (lambda (x) (call f (call x x)))))
```

### 1.3 Cognitive Applications

**Self-improvement loop:**
```
(define self-improve
  (fix (lambda (self state)
    (seq
      (reflect current-state)
      (derive improvement-rule)
      (branch (equal? improvement nil)
        state
        (call self (evaluate improvement state)))))))
```

**Recursive planning:**
```
(define decompose-plan
  (fix (lambda (recur goal)
    (seq
      (query (:type plan :goal goal))
      (branch (equal? plan nil)
        (seq (derive plan-strategy goal)
             (iterate (car plan) recur nil))
        plan)))))
```

### 1.4 The Z Combinator (Call-by-Value)

For strict evaluation (NSL's default), the Z combinator:
```
Z = λf. (λx. f (λv. x x v)) (λx. f (λv. x x v))
```
This avoids infinite expansion in applicative order.

### 1.5 Lawvere's Fixed-Point Theorem

In Cartesian Closed Categories (CCCs), a point-surjective
morphism `f: A -> B^A` implies every endomorphism `g: B -> B`
has a fixed point. This is the categorical foundation for
self-reference: any cognitive system capable of representing
its own state can implement self-improvement as a fixed-point
iteration.

**Significance**: The `reflect` primitive combined with `evaluate`
and `call` provides the categorical structure needed for
Lawvere's theorem — making self-reference a theorem rather
than a paradox.

### 1.6 Key References
- Curry, H. B. & Feys, R. (1958). *Combinatory Logic.*
- Barendregt, H. P. (1984). *The Lambda Calculus.*
- Lawvere, F. W. (1969). "Diagonal arguments and Cartesian closed categories."


## 2. Continuation-Passing Style for Cognitive Control Flow

### 2.1 The Insight

In CPS, every function receives a continuation `k` representing
"the rest of the computation." All control transfers (calls,
returns, exceptions, interrupts) become uniform function calls.

```
Direct style:   f(g(x))
CPS:            g(x, λv. f(v, k))
```

| Control Transfer | CPS Representation |
|---|---|
| Function call | Construct continuation, pass to callee |
| Return | Invoke current continuation with result |
| Conditional | Two continuations (then/else) |
| Exception | Exception continuation alongside normal continuation |
| Interrupt | Replace current continuation with handler |
| Yield | Capture continuation, return (cont, value) pair |

### 2.2 Why CPS for NSL

1. **Uniform control**: Interrupts, task switching,
   metacognitive reflection, and error handling all become
   the same mechanism — calling a continuation.

2. **Explicit control flow**: The NSP compiler can analyze
   and optimize cognitive workflows by examining continuation
   structures. Dead code, redundant reflection, and
   oscillating belief updates become statically detectable.

3. **Serializable cognition**: A continuation captures the
   entire cognitive state at a point. This enables:
   - Checkpointing cognitive workflows
   - Migrating cognition between nodes
   - Time-travel debugging of cognitive processes

### 2.3 CPS Transformation of NSL Workflows

```
;; NSL source
(workflow decide
  (seq
    (observe context)
    (query (:type beliefs) context)
    (derive action best-of candidates)
    (assert action)))

;; After CPS transformation (intermediate representation):
(define (decide-cps context k0)
  (observe-cps context
    (lambda (ctx-val)
      (query-cps (:type beliefs) ctx-val
        (lambda (beliefs)
          (derive-cps action (best-of candidates)
            (lambda (act)
              (assert-cps act
                (lambda (_) (k0 act))))))))))
```

### 2.4 Delimited Continuations: the `yield` Primitive

```
;; yield = shift (delimited continuation capture)
(define (yield value)
  (shift (lambda (k) (cons value k))))

;; Generator for hypotheses:
(workflow generate-hypotheses
  (seq
    (bind hyps (query (:type hypothesis)))
    (iterate hyps (lambda (h _) (yield h)))))
```

### 2.5 Key References
- Plotkin, G. D. (1975). "Call-by-name, call-by-value, and the λ-calculus." *TCS.*
- Fischer, M. J. (1972). "Lambda calculus schemata." *LCS.*
- Appel, A. W. (1992). *Compiling with Continuations.* Cambridge.
- Felleisen, M. (1988). "The theory and practice of first-class prompts." *POPL.*
- Danvy, O. & Filinski, A. (1990). "Abstracting control." *LFP.*


## 3. Abstract Interpretation for Symbolic Evaluation

### 3.1 The Problem

Cognitive operations may diverge, produce infinite belief
sets, or oscillate. We need sound approximations that
terminate.

### 3.2 The Solution

Abstract interpretation (Cousot & Cousot, 1977) provides:
- A **concrete domain** D (actual cognitive states)
- An **abstract domain** A (finite approximations)
- **Abstraction function** α: D → A
- **Concretization function** γ: A → D
- Galois connection: α and γ form an adjunction

```
forall d in D: d ⊑ γ(α(d))      ;; Soundness
forall a in A: α(γ(a)) ⊑ a       ;; Precision
```

### 3.3 Cognitive Abstract Domains

| Concrete | Abstract | Application |
|---|---|---|
| Belief confidence [0,1] | {LOW, MED, HIGH} | Belief triage |
| Memory (unbounded terms) | Type + size | Resource analysis |
| Cognitive state (full) | State signature | Change detection |
| Expression (unbounded) | Type + effect | Static analysis |

### 3.4 Abstract Semantics for NSL Primitives

```
(define (abstract-evaluate expr state)
  (match expr
    ((`read ,loc)
     (values (abstract-read loc)
             (consume-tokens 1 state)))
    ((`match ,pat ,val)
     (values (abstract-match pat val)
             (consume-tokens 5 state)))
    ((`evaluate ,term)
     (values (abstract-beta-reduce term)
             (consume-tokens MAX-ESTIMATED state)))
    ((`iterate ,body ,init)
     ;; Widen after k unrolls for termination
     (bind unrolled (abstract-unroll body MAX-UNROLL))
     (values (abstract-fixpoint unrolled init)
             (consume-tokens (* MAX-UNROLL 5) state)))))

(define (abstract-unroll body max-n)
  ;; Unroll iteration up to max-n for analysis
  (define (loop state n)
    (branch (>= n max-n)
      (widen state)  ;; Conservative over-approximation
      (match (abstract-evaluate body state)
        ((,next ,_) (loop next (+ n 1))))))
  (loop body 0))

(define (widen state)
  ;; Widen operator: join with termination guarantee
  ;; Ensures analysis completes in bounded time
  (abstract-join state previous-state))
```

### 3.5 Applications

**Termination guarantee**:
```
(abstract-interpret workflow initial-state)
-> ({time: ≤500ms, memory: ≤10KB}, safe | may-diverge)
```

**Oscillation detection**:
Detects when belief updates cycle without convergence.

**Resource budgeting**:
Guarantees token consumption is bounded before execution.

### 3.6 Key References
- Cousot, P. & Cousot, R. (1977). "Abstract interpretation: a unified lattice model." *POPL.*
- Cousot, P. & Cousot, R. (1979). "Systematic design of program analysis frameworks." *POPL.*
- Nielson, F., Nielson, H. R., & Hankin, C. (1999). *Principles of Program Analysis.* Springer.


## 4. Term Rewriting Systems for Cognitive Transformation

### 4.1 The Connection

Cognitive operations transform symbolic structures. This is
exactly what term rewriting systems (TRS) formalize:
- **Terms**: SXL expressions (beliefs, goals, plans)
- **Rewrite rules**: NSL primitive semantics
- **Reduction**: NSL expression evaluation
- **Normal form**: Final cognitive state

### 4.2 Convergence

A TRS is **convergent** if:
- **Confluent (Church-Rosser)**: `t ->* u` and `t ->* v` implies
  `exists w. u ->* w` and `v ->* w` — unique normal forms
- **Terminating**: No infinite reduction sequences

For NSL, convergence ensures deterministic, bounded cognition.

### 4.3 Critical Pair Analysis

Critical pair = overlap between two rule left-hand sides:

```
Rule 1: (assert P c) → (write P :confidence c)
Rule 2: (retract P) → (write P :confidence 0)
Critical pair: (assert P c1) vs (retract P)
→ Need conflict resolution strategy
```

The NSP detects critical pairs at compile time and inserts
resolution strategies (e.g., recency-based, priority-based).

### 4.4 Complete Rewrite System for Cognitive Semantics

```
;; Verification procedure
(define (verify-confluence rules)
  ;; 1. Prove termination via well-founded ordering
  (branch (not (proves-termination rules))
    (error "Cannot verify confluence: non-terminating"))

  ;; 2. Find all critical pairs
  (bind critical-pairs (find-critical-pairs rules))

  ;; 3. Check each is joinable
  (iterate critical-pairs (lambda (cp)
    (branch (not (joinable? (left cp) (right cp) rules))
      (error "Non-joinable critical pair" cp))))

  ;; 4. By Newman's Lemma: terminating + locally confluent = confluent
  :confluent)
```

### 4.5 Neuro-Symbolic Rewriting

Recent work (Petruzzellis et al., 2025) shows that neural
networks can learn convergent TRS from examples. For NSL:
- LLM backends propose candidate rewrite rules
- NSP checks convergence (termination + confluence)
- Convergent rules are promoted to the cognitive rule base
- Non-convergent rules are rejected or revised

```
(workflow learn-cognitive-rules
  (seq
    (bind candidates (query (:type proposed-rule)))
    (iterate candidates (lambda (rule)
      (branch (verify-confluence (list rule))
        (assert ((:type cognitive-rule) (:content rule)))
        (emit :warning
          (format "Rejected non-convergent: ~a" rule)))))))
```

### 4.6 Key References
- Baader, F. & Nipkow, T. (1998). *Term Rewriting and All That.* Cambridge.
- Klop, J. W. (1992). "Term rewriting systems." *Handbook of Logic in CS.*
- Knuth, D. E. & Bendix, P. B. (1970). "Simple word problems in universal algebras."
- Petruzzellis, F., Testolin, A., & Sperduti, A. (2025). "Learning neuro-symbolic convergent term rewriting systems." arXiv:2507.19372.
- Newman, M. H. A. (1942). "On theories with a combinatorial definition of 'equivalence'."


## 5. Category Theory for Cognitive Structure

### 5.1 Cognitive Effect Monad

NSL primitives with side effects form a monad T:

```
T : Type → Type                -- the effect type constructor
unit : A → T(A)                -- pure value into effect context
bind : T(A) × (A → T(B)) → T(B)  -- sequenced effects
```

Monad laws:
```
bind(unit(a), f) = f(a)            -- left identity
bind(m, unit) = m                  -- right identity
bind(bind(m, f), g) = bind(m, λx. bind(f(x), g))  -- associativity
```

In NSL, `sequence` is monadic bind, pure primitives are `unit`.

### 5.2 Cognitive Monads

| Monad | Effect | T(A) | NSL Use |
|---|---|---|---|
| Reader | Read-only context | Context → A | `resolve` name lookup |
| State | Read-write memory | State → (A, State) | `read`/`write` |
| Nondeterminism | Choice | Set(A) | `branch` exploration |
| Continuation | Control flow | (A → R) → R | `return`/`yield` |
| Probability | Uncertainty | Dist(A) | `derive` probabilistic |

Monad transformers compose effects:
```
;; Cognitive process: Reader + State + Nondeterminism
(define (cognitive-monad ctx s)
  (lambda (action)
    (match (action ctx s)
      (((,results ,new-s))
       (map (lambda (a) (a ctx new-s)) results)))))
```

### 5.3 Natural Transformations as Perspective Shifts

A natural transformation α: F → G applied at object X gives
α_X: F(X) → G(X) such that for all f: X → Y:

```
α_Y ∘ F(f) = G(f) ∘ α_X    (commutativity)
```

**Cognitive examples**:

```
;; Symbol → Vector embedding
embed :: Symbolic → Embedded
;; Must commute with substitution:
;; embed(substitute(t, σ)) = embed(t)[embed(σ)]

;; Concrete → Abstract
abstract :: Pattern → Concept
;; abstract(transform(p, r)) = transform(abstract(p), abstract(r))
```

**Significance**: Naturality ensures representation changes
preserve semantic structure. If embedding didn't commute
with substitution, the embedding would be semantically
incoherent.

### 5.4 Symmetric Monoidal Structure

NSL primitives form a symmetric monoidal category:
- **Objects**: NSL types
- **Morphisms**: Primitives and compositions
- **⊗ (tensor)**: `parallel`
- **I (unit)**: Nil, empty parallel composition
- **∘ (composition)**: `sequence`
- **Braiding**: `parallel A B ≅ parallel B A`

### 5.5 Key References
- Mac Lane, S. (1971). *Categories for the Working Mathematician.* Springer.
- Moggi, E. (1991). "Notions of computation and monads." *Information and Computation.*
- Wadler, P. (1992). "The essence of functional programming." *POPL.*


## 6. Information Geometry for Belief Updating

### 6.1 The Statistical Manifold

Beliefs are probability distributions over cognitive states.
The space of all possible beliefs forms a statistical manifold:
- **Points**: Probability distributions p(x;θ)
- **Coordinates**: Parameters θ
- **Metric**: Fisher information matrix g_ij(θ)
- **Distance**: Fisher-Rao geodesic distance

### 6.2 Chentsov's Theorem

The Fisher metric is the **unique** invariant metric on the
probability simplex under sufficient statistics. There is no
other consistent choice. This means: if you want to update
beliefs in a way that is invariant under reparameterization,
you must use the Fisher metric.

```
g_ij(θ) = E_x[ (∂log p(x;θ)/∂θ_i) · (∂log p(x;θ)/∂θ_j) ]
```

### 6.3 Natural Gradient for Belief Updates

Standard gradient treats all parameter directions equally,
but the probability simplex is curved:

```
;; Standard gradient: θ -= η · ∇L
;; Natural gradient:  θ -= η · G^{-1}(θ) · ∇L

(define natural-gradient-update
  (lambda (belief observation)
    (bind likelihood (log-probability observation belief))
    (bind grad (gradient likelihood belief.params))
    (bind fisher (fisher-matrix belief))
    ;; Natural = inverse Fisher times gradient
    (bind natural-grad (solve-linear fisher grad))
    (update belief (- belief.params (* learning-rate natural-grad)))))
```

### 6.4 Relation to Kalman Filter

Online natural gradient is equivalent to the extended Kalman
filter:

| Kalman Filter | Natural Gradient |
|---|---|
| State estimate x̂_t | Parameter θ_t |
| Covariance P_t | Fisher⁻¹ F_t⁻¹ |
| Innovation y_t - Hx̂_t | Prediction error |
| Kalman gain K_t | F_t⁻¹ · ∇L |

### 6.5 Confidence Propagation

The 6 confidence propagation rules in `libsexpr/confidence.c`
approximate geodesic paths on the statistical manifold:
- AND: confidence combines multiplicatively (independent evidence)
- OR: confidence combines via inclusion-exclusion
- NOT: confidence = 1 - confidence
- TRANSFER: confidence propagates along inference edges
- The Fisher-Rao distance between two confidence values
  measures how much evidence separates them

### 6.6 Amari's α-Connections

```
α = +1: e-connection (dually flat for exponential families)
α = 0:  Levi-Civita (Riemannian/metric)
α = -1: m-connection (dually flat for mixture families)
```

The e- and m-connections are dual under the Fisher metric.
The EM algorithm alternates between e- and m-projections.

### 6.7 Key References
- Amari, S. (2016). *Information Geometry and Its Applications.* Springer.
- Amari, S. (1998). "Natural gradient works efficiently in learning." *Neural Computation.*
- Chentsov, N. N. (1982). *Statistical Decision Rules and Optimal Inference.* AMS.
- Amari, S. & Nagaoka, H. (2000). *Methods of Information Geometry.* AMS.


## 7. Optimal Transport for Concept Mapping

### 7.1 The Problem

Given concept spaces A and B (each with weighted symbolic
structures), find the optimal mapping that minimizes
"cognitive work."

### 7.2 Wasserstein Distance

```
W_p(μ, ν) = (inf_γ ∫ d(x,y)^p dγ(x,y))^{1/p}
```

where γ is a transport plan — a joint distribution over
A × B that moves probability mass from μ to ν at minimum cost.

```
(define wasserstein-distance
  (lambda (mu nu cost-matrix)
    ;; Solve: min Σ T[i,j] · C[i,j]
    ;; s.t.  Σ_j T[i,j] = μ[i]
    ;;       Σ_i T[i,j] = ν[j]
    ;;       T[i,j] ≥ 0
    (bind T (solve-transport-lp mu nu cost-matrix))
    (sum (* T cost-matrix))))
```

### 7.3 Cognitive Applications

**Analogy as optimal transport**:
"A is to B as C is to ?" becomes: find D that minimizes
W_p(transform(A→B), transform(C→D)).

```
(define analogical-mapping
  (lambda (source target)
    ;; Optimal transport between conceptual domains
    (bind feature-cost
      (lambda (sc tc) (- 1 (semantic-similarity sc tc))))
    (bind structural-cost
      (gromov-wasserstein source.graph target.graph))
    (fused-gromov-wasserstein source target feature-cost structural-cost 0.5)))
```

**Concept alignment across nodes**: When two nodes have
different ontologies, the Fused Gromov-Wasserstein (FGW)
distance handles both feature-level and structural differences.

**Belief revision as transport**: Updating a belief
distribution μ to incorporate evidence ν can be formulated
as optimal transport from μ to a distribution balancing
prior and evidence.

### 7.4 NSL Primitives

`unify` is a special case of optimal transport: find the
substitution (transport plan) making two terms identical
at minimum syntactic cost. `derive analogical` extends
this to optimal transport over semantic spaces.

| NSL Primitive | Optimal Transport Concept |
|---|---|
| `unify` | Syntactic transport (minimal substitution) |
| `match` | Feature alignment pattern-target |
| `equal?` | Zero-cost transport (identical concepts) |
| `derive analogical` | Semantic OT between domains |

### 7.5 Key References
- Villani, C. (2009). *Optimal Transport: Old and New.* Springer.
- Peyre, G. & Cuturi, M. (2019). "Computational optimal transport." *Foundations and Trends in ML.*
- Taylor, J. et al. (2025). "Beyond Letters: Optimal Transport as a Model for Sub-Letter Orthographic Processing."
- Thual, A. et al. (2022). "Aligning individual brains with Fused Unbalanced Gromov-Wasserstein." *NeurIPS.*


## 8. NSP Compilation Pipeline

The seven pillars integrate into the NSP compiler as follows:

```
NSL Source
    |
    v
[CPS Transform]         — uniform control flow via continuations
    |
    v
[Term Rewriting]        — reduce cognitive transforms to rewrite steps
    |
    v
[Abstract Interpretation] — static analysis (bounds, termination, oscillation)
    |
    v
[Monadic Lift]          — thread cognitive effects through state monad
    |
    v
[Fixed-Point Optimize] — optimize recursion via Y combinator
    |
    v
[OT Schedule]           — schedule parallel ops via transport cost
    |
    v
NSP Executable
```

### Pillar-to-Primitive Map

| Pillar | NSL Primitives | Role |
|---|---|---|
| Fixed-point | `call`, `evaluate` | Recursive self-improvement |
| CPS | `return`, `yield` | Control flow, serializability |
| Abstract interpretation | All (compiler) | Termination, safety guarantees |
| Term rewriting | `match`, `unify`, `substitute` | Rule application |
| Category theory | `sequence`, `parallel` | Composition, effects |
| Information geometry | `derive`, `assert` | Belief updating |
| Optimal transport | `unify`, `derive analogical` | Concept alignment |
