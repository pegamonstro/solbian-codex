# NSL Primitive Derivation

> How the 33 NSL primitives were derived from mathematical
> foundations and why each is irreducible.
>
> Status: **Research notes** (sapling prototype)

## 1. Methodology

The primitive set was derived by:

1. **Top-down decomposition**: Starting from the 14 SXL
   operators and 12 cognitive cycle phases, decomposing each
   into the smallest operations that cannot be further broken
   down while preserving cognitive semantics.

2. **Bottom-up construction**: Starting from known minimal
   computational bases (lambda calculus, SKI combinators,
   π-calculus, abstract state machines), identifying which
   cognitive operations each base can and cannot express.

3. **Gap analysis**: Where top-down and bottom-up disagree,
   the gap reveals a missing primitive or a composite
   misidentified as primitive.

## 2. Mathematical Bases Analyzed

### 2.1 Lambda Calculus (Church, 1936)

**Primitives**: Abstraction (λx.M), Application (M N)

**What it provides**: Function definition and application.
Sufficient for all computable functions. Variables and
substitution are implicit.

**What it lacks**: Concurrency, state, communication, pattern
matching, introspection.

**NSL primitives derived**: `call` (application), `bind` +
`resolve` (abstraction + variable lookup), `substitute`
(β-reduction)

### 2.2 SKI Combinator Calculus (Schönfinkel, 1924; Curry, 1958)

**Primitives**: S = λxyz.xz(yz), K = λxy.x, I = λx.x

**What it provides**: Turing-complete computation without
variables. All lambda terms compilable to SKI.

**What it lacks**: Everything lambda calculus lacks, plus
readability and direct expression of data structures.

**NSL primitives derived**: SKI validates that `branch` +
`call` + closure over `bind`/`resolve` is sufficient for
Turing-completeness. No additional primitives beyond lambda
calculus derivations, but SKI provides the minimality proof:
if three combinators suffice for all computation, ~33
primitives for all cognition is conservative.

### 2.3 π-Calculus (Milner, 1999)

**Primitives**: Input a(x).P, Output āx.P, Parallel P|Q,
Restriction (νa)P, Replication !P, Choice P+Q, Nil 0

**What it provides**: Concurrency, communication, mobility
(channels as first-class values), scope extrusion.

**What it lacks**: State, data structures, introspection,
cognitive operations.

**NSL primitives derived**: `send` (= output), `recv` (= input),
`spawn` (= replication), `parallel` (= parallel composition),
`bind` + `resolve` (= restriction, scoped names)

### 2.4 Abstract State Machines (Gurevich, 1995)

**Three postulates**: Sequential time, abstract state, bounded
exploration.

**What it provides**: Formal semantics for state transitions.
Every algorithm can be modeled as an ASM.

**NSL primitives derived**: `read` + `write` (= state access
and update), `sequence` (= sequential time postulate)

### 2.5 Kowalski's Algorithm = Logic + Control (1979)

**Insight**: Separate the logic (what to compute) from the
control (how to compute it). Logic = declarative specification.
Control = procedural execution strategy.

**NSL primitives derived**: `derive` (= logic step), all five
composition rules (= control). This is the most important
single insight for NSL design: the primitive set is the
"logic" vocabulary; the composition rules are the "control"
grammar.

## 3. Primitive Families and Candidates

### 3.1 Memory/State (6 candidates → 3 primitives)

| # | Primitive | Source | Status |
|---|----------|--------|--------|
| 1 | `create` | ASM, Lisp | **Primitive** — allocation is atomic |
| 2 | `destroy` | ASM, Lisp | **Primitive** — inverse of create |
| 3 | `typeof` | Lisp, type theory | **Primitive** — single-read type inspection |
| - | `read` | ASM, all ISAs | **Primitive** (in Group II) |
| - | `write` | ASM, all ISAs | **Primitive** (in Group II) |
| - | `copy` | Derived need | **Composite** — create + iterate read/write |

### 3.2 Binding/Reference (6 candidates → 3 primitives)

| # | Primitive | Source | Status |
|---|----------|--------|--------|
| 7 | `bind` | λ-calculus | **Primitive** — creates association |
| 8 | `unbind` | λ-calculus (inverse) | **Primitive** — destroys association |
| 9 | `resolve` | λ-calculus | **Primitive** — name resolution |
| - | `link` | Graph theory | **Composite** — write with relation field |
| - | `unlink` | Graph theory | **Composite** — write with relation removal |
| - | `fresh` | π-calculus (ν) | **Composite** — create + typeof (new symbol) |

### 3.3 Control Flow (6 candidates → 4 primitives)

| # | Primitive | Source | Status |
|---|----------|--------|--------|
| 13 | `sequence` | Category theory | **Primitive** — sequential composition |
| 14 | `parallel` | π-calculus (P|Q) | **Primitive** — concurrent composition |
| 15 | `branch` | All ISAs | **Primitive** — conditional evaluation |
| 16 | `iterate` | All ISAs | **Primitive** — unbounded iteration |
| - | `guard` | π-calculus (choice) | **Composite** — pattern over channels |
| - | `match` | Term rewriting | **Primitive** (in Group VII) |

### 3.4 Communication (6 candidates → 3 primitives)

| # | Primitive | Source | Status |
|---|----------|--------|--------|
| 19 | `send` | π-calculus (output) | **Primitive** — synchronized send |
| 20 | `recv` | π-calculus (input) | **Primitive** — synchronized receive |
| 21 | `spawn` | π-calculus (!P) | **Primitive** — process creation |
| - | `emit` | Pub-sub | **Composite** — spawn + send (fire-and-forget) |
| - | `wait` | Temporal logic | **Composite** — recv on timer channel |
| - | `invoke` | RPC | **Composite** — send + recv (request-reply) |

### 3.5 Transformation (5 candidates → 3 primitives)

| # | Primitive | Source | Status |
|---|----------|--------|--------|
| 25 | `evaluate` | λ-calculus, UTMs | **Primitive** — metacircular evaluation |
| - | `compare` | Lisp | **Composite** — `equal?` + `less?` |
| - | `transform` | Term rewriting | **Composite** — `match` + `substitute` |
| - | `abstract` | Category theory | **Composite** — `unify` + `substitute` |
| - | `instantiate` | Category theory | = `substitute` |

### 3.6 Metacognitive (6 candidates → 2 primitives)

| # | Primitive | Source | Status |
|---|----------|--------|--------|
| 30 | `reflect` | Reflective towers | **Primitive** — self-observation |
| - | `benchmark` | Self-assessment | **Composite** — reflect + evaluate + compare |
| - | `trace` | Debugging | **Composite** — reflect execution-trace |
| - | `suspend` | OS schedulers | = `yield` |
| - | `resume` | OS schedulers | = `call` with continuation |
| - | `prioritize` | Scheduling theory | Scheduling policy, not a primitive |

### Additional Groups (from bottom-up analysis)

### 3.7 Structural (3 primitives)
`cons`, `car`, `cdr` — from Lisp: the universal constructor and
accessors. Without these, only atomic values exist.

### 3.8 Pattern (3 primitives)
`match`, `unify`, `substitute` — from term rewriting and logic
programming. Pattern matching drives all rule application;
unification is the engine of logic; substitution instantiates.

### 3.9 Comparison (2 primitives)
`equal?`, `less?` — structural equality and total ordering.
Required for sorted data structures, deterministic iteration,
and set operations. Not reducible to each other.

### 3.10 Subroutine (3 primitives)
`call`, `return`, `yield` — from lambda calculus + delimited
continuations. `call` = β-reduction. `return` = non-local
control transfer (CPS). `yield` = delimited continuation
capture (shift/reset).

### 3.11 Cognitive (5 primitives)
`observe`, `assert`, `retract`, `query`, `derive` — the
cognitive-specific primitives. These are what make NSL a
*cognitive* ISA rather than a general-purpose computational
ISA. `observe` = system boundary. `assert`/`retract` =
knowledge acquisition/removal (AGM). `query` = memory
retrieval (relational σ). `derive` = inference step
(Kowalski's Logic).

## 4. Audit Summary: 48 Candidates → 33 Primitives

**Demoted to composite (15)**: copy, link, unlink, fresh,
guard, emit, wait, invoke, compare, transform, abstract,
instantiate, benchmark, trace, prioritize

**Suspend/resume demoted**: = `yield` and `call`+continuation

**Final 33**: create, destroy, typeof, read, write, bind,
unbind, resolve, cons, car, cdr, branch, iterate, sequence,
parallel, call, return, yield, match, unify, substitute,
equal?, less?, send, recv, spawn, observe, assert, retract,
query, derive, reflect, evaluate

## 5. Completeness Verification

### SXL Operators (14/14 covered)

| SXL Operator | NSL Decomposition |
|-------------|-------------------|
| compare | `(seq (query ...) (match ...) (equal? ...) (less? ...))` |
| infer | `(derive modus-ponens (query premises ...))` |
| explain | `(seq (query ...) (derive backward-chain ...))` |
| simulate | `(seq (branch ...) (assert ...) (derive ...))` |
| project | `(seq (query ...) (derive forward-chain ...))` |
| reflect | `(seq (reflect ...) (query ...) (derive ...))` |
| criticise | `(seq (query ...) (match ...) (branch ...))` |
| merge | `(seq (query ...) (unify ...) (substitute ...) (assert ...))` |
| split | `(seq (match ...) (car ...) (cdr ...))` |
| abstract | `(seq (query ...) (match ...) (unify ...) (substitute ...))` |
| reconcile | `(seq (query ...) (unify ...) (branch ...) (assert ...) (retract ...))` |
| evaluate | `(seq (query ...) (derive ...) (equal? ...))` |
| reinforce | `(seq (query ...) (assert ...))` with higher confidence |
| decay | `(seq (query ...) (retract ...))` for old/low-confidence |

### SST Operators (22/22 covered)

All 22 SST operators decompose into NSL primitives. Example:
SST_OP_REFLECT → `(seq (reflect ...) (query ...) (derive ...) (assert ...))`

### Cognitive Cycle Phases (12/12 covered)

Each phase A-L in `seedcogd/main.c` is expressible as an
NSL workflow. For example, Phase C (Hippocampus Consolidation):
```
(workflow hippocampus-consolidation
  (seq
    (query (:type memory :source this-node) recent-window)
    (iterate results
      (lambda (entry acc)
        (seq
          (match (:content ?c :confidence ?conf) entry)
          (branch (< ?conf consolidation-threshold)
            (retract entry)
            (seq
              (derive generalize entry)
              (assert (:type knowledge :content ?c) (+ ?conf 0.05))))))
      nil)))
```

## 6. Key References

- Church, A. (1932). "A set of postulates for the foundation of logic." *Annals of Mathematics.*
- Church, A. (1936). "An unsolvable problem of elementary number theory." *Am. J. Math.*
- Schönfinkel, M. (1924). "Über die Bausteine der mathematischen Logik." *Mathematische Annalen.*
- Curry, H. B. & Feys, R. (1958). *Combinatory Logic.* North-Holland.
- Milner, R. (1999). *Communicating and Mobile Systems: the π-Calculus.* Cambridge.
- Milner, R., Parrow, J., & Walker, D. (1992). "A calculus of mobile processes." *Information and Computation.*
- Gurevich, Y. (1995). "Evolving algebras 1993: Lipari guide." In *Specification and Validation Methods.* Oxford.
- Kowalski, R. (1979). *Algorithm = Logic + Control.* CACM 22(7):424-436.
- Barendregt, H. P. (1984). *The Lambda Calculus: Its Syntax and Semantics.* North-Holland.
- Baader, F. & Nipkow, T. (1998). *Term Rewriting and All That.* Cambridge.
- Klop, J. W. (1992). "Term rewriting systems." In *Handbook of Logic in Computer Science.* Oxford.
- Robinson, J. A. (1965). "A machine-oriented logic based on the resolution principle." *JACM* 12(1):23-41.
- Alchourrón, C. E., Gärdenfors, P., & Makinson, D. (1985). "On the logic of theory change." *J. Symb. Logic* 50(2):510-530.
- Felleisen, M. (1988). "The theory and practice of first-class prompts." *POPL '88.*
