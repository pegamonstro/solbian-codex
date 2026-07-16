# NSL ISA Specification v0.1.0

> **The instruction set of cognition.** Formal specification of
> the Neural Symbolic Language — 33 irreducible primitives,
> 5 composition rules, type system, and operational semantics.
>
> Status: **Draft** (sapling prototype)
> Governed by: `seed-cog3-specs.txt` §"4-layer SXL ISA"

## 1. Design Philosophy

### 1.1 The Primitive Test

An operator is **primitive** iff it cannot be expressed as a
composition of other NSL primitives. Formally: operator `op` is
primitive iff there exists no NSL expression `E` composed of
other primitives such that `⟦op⟧ = ⟦E⟧` for all inputs.

Operators failing this test are **composite procedures** — they
belong at the SXL operator layer, not in NSL.

### 1.2 The Completeness Criterion

The set is **complete** iff every cognitive operation
expressible in S.E.E.D. can be written as a composition of NSL
primitives. This includes all 14 SXL operators, all 22 SST
operators, and all 12 cognitive cycle phases.

### 1.3 Design Constraints

1. **No backend assumption.** Primitives operate on symbolic
   structures; backends are an implementation detail.
2. **Bounded non-determinism.** Primitives invoking neural
   inference (observe, derive) may vary across runs; this is
   explicit via confidence parameters.
3. **Side-effect tracking.** Every primitive is annotated with
   effect class: pure, read, write, or alloc.
4. **No recursion in primitives.** Primitives are non-recursive.
   Recursion is achieved through composition (call + branch).

## 2. The 33 Primitives

### 2.1 Taxonomy

| # | Group | Primitives | Count | Effect |
|---|-------|-----------|-------|--------|
| I | Object Lifecycle | `create`, `destroy`, `typeof` | 3 | alloc/write/read |
| II | Memory | `read`, `write` | 2 | read/write |
| III | Binding | `bind`, `unbind`, `resolve` | 3 | write/read |
| IV | Structure | `cons`, `car`, `cdr` | 3 | pure |
| V | Control Flow | `branch`, `iterate`, `sequence`, `parallel` | 4 | pure |
| VI | Subroutine | `call`, `return`, `yield` | 3 | pure |
| VII | Pattern | `match`, `unify`, `substitute` | 3 | pure |
| VIII | Comparison | `equal?`, `less?` | 2 | pure |
| IX | Channel | `send`, `recv`, `spawn` | 3 | write/read/alloc |
| X | Cognitive | `observe`, `assert`, `retract`, `query`, `derive` | 5 | read/write |
| XI | Meta | `reflect`, `evaluate` | 2 | read/pure |
| | **Total** | | **33** | |

### 2.2 Group I: Object Lifecycle

```
create   : Symbol → Cell              [alloc]
  Allocate a new symbolic cell with the given type tag.
  Irreducible: allocation is atomic — no composition creates a new identity.

destroy  : Cell → Nil                 [write]
  Deallocate cell and release resources. Cell reference becomes invalid.
  Irreducible: inverse of create. Requires GC integration for safety.

typeof   : Cell → Symbol             [read]
  Return the type tag of the cell (Goal, Belief, Plan, Memory, ...).
  Irreducible: type inspection is a single read.
```

### 2.3 Group II: Memory

```
read     : Cell × Key → Value         [read]
  Read value at Key from Cell. Key may be Symbol (field name) or Integer (index).
  Irreducible: the fundamental memory access. All higher retrieval composes from read + query + match.

write    : Cell × Key × Value → Cell  [write]
  Write Value to Key in Cell. Atomic: fully succeeds or has no effect.
  Irreducible: the fundamental memory mutation. Combined with create, the only way to modify state.
```

### 2.4 Group III: Binding

```
bind     : Symbol × Value × Env → Env [write]
  Extend Env with Symbol→Value. Shadows existing binding.
  Irreducible: creates an association — from lambda calculus, binding + application = all computation.

unbind   : Symbol × Env → Env         [write]
  Remove binding for Symbol from Env. No-op if not bound.
  Irreducible: inverse of bind. Destruction of association not expressible as bind + anything.

resolve  : Symbol × Env → Value|Nil  [read]
  Look up Symbol in Env. Returns bound Value or Nil. Innermost binding wins.
  Irreducible: name resolution is a single lookup — fundamental dereference operation.
```

### 2.5 Group IV: Structure

```
cons     : Value × Value → Pair       [pure]
  Construct pair (car . cdr). The universal constructor — all compound data from pairs.
  Irreducible: sole constructor for compound data. From Lisp: cons is universal.

car      : Pair → Value               [pure]
  Return first element of pair. Irreducible: fundamental accessor.

cdr      : Pair → Value               [pure]
  Return second element of pair. Irreducible: with car, complete pair deconstruction.
```

### 2.6 Group V: Control Flow

```
branch   : Boolean × Expr × Expr → Value  [pure*]
  If Boolean is true, evaluate first Expr; otherwise second.
  Irreducible: from SKI — no combination of S and K implements conditional evaluation.

iterate  : Seq × (Value→Value) × Value → Value  [pure*]
  Fold-left over Seq: for each element, apply fn with accumulated value.
  Irreducible: iteration over unbounded sequence not expressible as fixed composition.

sequence : Expr* → Value              [pure*]
  Evaluate each Expr left-to-right. Return last value.
  Irreducible: sequential composition is the fundamental control structure.
  From category theory: composition in the Kleisli category of the cognitive effect monad.

parallel : Expr* → Value*             [pure*]
  Evaluate each Expr concurrently. Return sequence of results. Partial success semantics.
  Irreducible: from π-calculus — P|Q is primitive, cannot reduce to sequential composition.
```
*May cause effects in evaluated sub-expressions.

### 2.7 Group VI: Subroutine

```
call     : Proc × Value* → Value      [pure*]
  Invoke procedure with arguments in fresh environment.
  Irreducible: from lambda calculus — application is primitive (β-reduction).

return   : Value → (exit procedure)   [pure]
  Exit current procedure early, return Value to caller.
  Irreducible: from CPS — non-local control transfer is primitive.

yield    : Value → (suspend with continuation)  [pure]
  Suspend current procedure, yield Value with captured continuation.
  Irreducible: from delimited continuations — shift/reset is primitive.
```

### 2.8 Group VII: Pattern

```
match    : Pattern × Value → Bindings|Nil  [pure]
  Match Pattern against Value. Success → variable bindings. Fail → Nil.
  Pattern types: literals, variables, wildcards, cons patterns, type patterns.
  Irreducible: from term rewriting — matching drives all rewrite rule application.

unify    : Value × Value → Substitution|Nil  [pure]
  Find most general unifier (MGU) of two Values. Occurs-check prevents infinite terms.
  Irreducible: from logic programming — unification subsumes matching and equality.

substitute : Substitution × Value → Value  [pure]
  Apply Substitution to Value, replacing all variables.
  Irreducible: from lambda calculus — β-reduction is substitution.
  From π-calculus — communication is name substitution.
```

### 2.9 Group VIII: Comparison

```
equal?   : Value × Value → Boolean    [pure]
  Structural equality. Atoms: same type and content. Pairs: recursive car and cdr.
  Irreducible: fundamental comparison. All other comparisons reduce to equal? + iterate.

less?    : Value × Value → Boolean    [pure]
  Total ordering. Numbers: numeric. Symbols: lexicographic. Pairs: lexicographic on (car, cdr).
  Irreducible: required for sorted structures and deterministic iteration. Not reducible to equal?.
```

### 2.10 Group IX: Channel

```
send     : Channel × Value → Nil      [write]
  Send Value on Channel. May block (synchronous) or queue (async).
  Irreducible: from π-calculus — output (āx.P) is primitive. Involves synchronization.

recv     : Channel → Value            [read]
  Receive Value from Channel. Blocks until available.
  Irreducible: from π-calculus — input (a(x).P) is primitive. Dual of send.

spawn    : Expr → Process             [alloc]
  Create concurrent process evaluating Expr. Returns Process handle.
  Irreducible: from π-calculus — process creation (!P) is primitive.
```

### 2.11 Group X: Cognitive

```
observe  : Sensor × Query → Observation  [read]
  Ingest data from external Sensor (perceptual input, bus topic, API).
  Returns SXL Observation entity with timestamp, confidence, content.
  Irreducible: the system boundary. No internal composition produces external information.

assert   : Proposition × Confidence → Nil  [write]
  Assert Proposition with Confidence [0,1] into cognitive state.
  If already exists, update confidence and record evidence chain.
  Irreducible: fundamental knowledge acquisition. Only way knowledge enters state (besides observe).

retract  : Proposition → Nil           [write]
  Withdraw previously asserted Proposition. Marked as retracted with timestamp.
  Irreducible: from AGM belief revision — contraction is primitive.

query    : Pattern × Scope → Result*   [read]
  Search memory for assertions matching Pattern within Scope.
  Results ordered by confidence descending. Each result: assertion, confidence, provenance.
  Irreducible: from relational algebra — selection (σ) is primitive.

derive   : Rule × Premise* → Conclusion  [read]
  Apply inference Rule to Premises to produce Conclusion with confidence.
  Rule types: logical (modus ponens, resolution), statistical (Bayesian), neural (LLM backend).
  Returns Nil if rule does not apply.
  Irreducible: from Kowalski — Algorithm = Logic + Control. Derive is the Logic step.
```

### 2.12 Group XI: Meta

```
reflect  : Query → CognitiveState      [read]
  Inspect system's own cognitive state: running procedures, assertions, decisions,
  outcomes, resource utilization, confidence calibration, error history.
  Irreducible: self-observation requires interpreter access. The "reflective tower" primitive.

evaluate : Expr × Env → Value          [pure*]
  Evaluate NSL expression in given environment. The metacircular evaluator.
  Irreducible: from universal Turing machines — an interpreter for its own language.
  The eval/apply loop is irreducible.
```

## 3. Composition Rules

NSL primitives compose through exactly **five** mechanisms.
There are no other composition forms.

### 3.1 Sequence `(seq E1 E2 ... En)`
```
Evaluate E1 through En in order. Return value of En.
If any Ei performs return, sequence terminates early.
⟦seq E1 E2⟧(σ) = ⟦E2⟧(⟦E1⟧(σ))
```

### 3.2 Branch `(branch cond then else)`
```
Evaluate cond. If truthy, evaluate then; otherwise else.
⟦branch true E1 E2⟧(σ)  = ⟦E1⟧(σ)
⟦branch false E1 E2⟧(σ) = ⟦E2⟧(σ)
```

### 3.3 Iterate `(iterate seq fn init)`
```
For each x in seq: acc = fn(x, acc). Return final acc.
Fold-left semantics: fn(xn, ... fn(x1, init) ...)
```

### 3.4 Parallel `(par E1 E2 ... En)`
```
Evaluate E1..En concurrently. No ordering constraint between Ei and Ej.
If any Ei fails, produces Nil in that position (partial success).
```

### 3.5 Call `(call proc arg1 ... argn)`
```
Invoke procedure with arguments in fresh environment.
⟦call proc a1...an⟧(σ) = ⟦body(proc)⟧(σ extended with {param_i → a_i})
```

### 3.6 Completeness Theorem (informal)

The five composition rules + 33 primitives are sufficient to express
all 14 SXL operators, all 22 SST operators, and all 12 cognitive
cycle phases. Proof by construction: each SXL operator and each
cognitive phase has a known NSL decomposition (see §5).

## 4. Type System

### 4.1 Base Types
```
Nil, Boolean, Integer, Float, Symbol, String,
Cell, Pair, Channel, Process, Procedure,
Pattern, Substitution, Environment, Rule, Sensor
```

### 4.2 Compound Types
```
Sequence = Pair*           (via cons)
Set      = Pair*           (via cons + equal?)
Map      = (Pair . Pair)*  (via cons + equal?)
SXL-Entity = Symbol × Fields  (type tag + keyed values)
```

### 4.3 Effect Types
```
Effect ::= pure | read | write | alloc
Effect composition: effects(seq E1 E2) = effects(E1) ∪ effects(E2)
```

## 5. Decomposition Proofs

### 5.1 SXL Operators as NSL Compositions

| SXL Operator | NSL Decomposition |
|-------------|-------------------|
| `compare` | `(seq (query ...) (match ...) (equal? ...))` |
| `infer` | `(derive modus-ponens (query ...))` |
| `explain` | `(seq (query ...) (derive backward-chain ...))` |
| `simulate` | `(seq (branch ...) (assert ...) (derive ...))` |
| `project` | `(seq (query ...) (derive forward-chain ...))` |
| `reflect` | `(seq (reflect ...) (query ...) (derive ...))` |
| `criticise` | `(seq (query ...) (match ...) (branch ...))` |
| `merge` | `(seq (query ...) (unify ...) (substitute ...) (assert ...))` |
| `split` | `(seq (match ...) (car ...) (cdr ...))` |
| `abstract` | `(seq (query ...) (match ...) (unify ...) (substitute ...))` |
| `reconcile` | `(seq (query ...) (unify ...) (branch ...) (assert ...) (retract ...))` |
| `evaluate` | `(seq (query ...) (derive ...) (compare ...))` |
| `reinforce` | `(seq (query ...) (assert ...))` with higher confidence |
| `decay` | `(seq (query ...) (retract ...))` for old/low-confidence assertions |

### 5.2 SST Operators as NSL Compositions

All 22 SST operators (OBSERVE through TRAIN) decompose into
combinations of the 33 NSL primitives. SST_OP_REFLECT, for
example, decomposes into `(seq (reflect ...) (query ...)
(derive ...) (assert ...))`. The SST operator set is a
convenience layer — not an irreducible ISA.

## 6. Operational Semantics

### 6.1 State Model
```
σ = (μ, ε, κ, χ, π)
  μ : Cell → (Type × Fields)    — memory (symbolic cells)
  ε : Symbol → Value            — environment (bindings)
  κ : Channel → Queue[Value]    — channels (pending messages)
  χ : Continuation*             — continuation stack
  π : Process*                  — active processes
```

### 6.2 Selected Small-Step Rules

**Assert:**
```
σ = (μ, ε, κ, χ, π)
μ' = μ ∪ {fresh_id → (:assertion, {content: p, confidence: c})}
───────────────────────────────────────────── assert
(σ, assert p c) → ((μ', ε, κ, χ, π), nil)
```

**Derive (backend invocation):**
```
backend = select_backend(rule, premises, σ)
conclusion = invoke_backend(backend, rule, premises)
────────────────────────────────────────────── derive
(σ, derive rule premises) → (σ, conclusion)
```

**Sequence:**
```
(σ, E1) → (σ', E1')
───────────────────────── seq-step
(σ, seq E1 E2) → (σ', seq E1' E2)

───────────────────────── seq-value
(σ, seq V E2) → (σ, E2)
```

### 6.3 Non-Determinism Bounds

`derive`, `observe`, and `evaluate` may produce different
results across invocations (LLM non-determinism). This is
bounded:
- **derive**: same rule + premises + random seed → same conclusion
- **observe**: external world not deterministic; repeated
  observations of same sensor at same time not guaranteed identical
- **evaluate**: seed-deterministic, same as derive

## 7. Mathematical Foundations

### 7.1 Lambda Calculus
NSL is a conservative extension: `call` + `bind` + `resolve` =
β-reduction. The Y combinator is expressible via `evaluate`.

### 7.2 π-Calculus
Channel group (send, recv, spawn) directly embeds π-calculus:
send = āx.P, recv = a(x).P, spawn = !P, parallel = P|Q.

### 7.3 SKI Combinators
```
K = (lambda (x) (lambda (y) x))
S = (lambda (x) (lambda (y) (lambda (z) ((x z) (y z)))))
I = (S K K)
```
SKI is Turing-complete; NSL inherits this via branch + iterate + call.

### 7.4 Term Rewriting
Pattern group (match, unify, substitute) provides the substrate:
match = LHS matching, substitute = RHS instantiation,
evaluate = application. All convergent TRS are expressible.

### 7.5 Category Theory
NSL primitives form a symmetric monoidal category:
- Objects: NSL types
- Morphisms: primitives and compositions
- Composition: sequence
- Tensor product: parallel
- Cognitive effect monad T: Value → Value with effects

### 7.6 Information Geometry
Belief updating via natural gradient on statistical manifold.
Fisher metric (Chentsov's theorem: unique invariant metric).
Derive's confidence propagation follows geodesic paths.

## 8. Key References

- Church, A. (1936). "An unsolvable problem of elementary number theory." *Am. J. Math.*
- Schönfinkel, M. (1924). "Über die Bausteine der mathematischen Logik."
- Curry, H. B. & Feys, R. (1958). *Combinatory Logic.*
- Milner, R. (1999). *Communicating and Mobile Systems: the π-Calculus.*
- Kowalski, R. (1979). "Algorithm = Logic + Control." *CACM.*
- Plotkin, G. D. (1975). "Call-by-name, call-by-value, and the λ-calculus." *TCS.*
- Felleisen, M. (1988). "The theory and practice of first-class prompts." *POPL '88.*
- Amari, S. (2016). *Information Geometry and Its Applications.* Springer.
- Kanerva, P. (1988). *Sparse Distributed Memory.* MIT Press.
- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nat. Rev. Neurosci.*
- Ramsauer, H. et al. (2020). "Hopfield Networks is All You Need." *ICLR 2021.*
- Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985).
  "On the logic of theory change: Partial meet contraction and revision functions." *J. Symb. Logic.*
