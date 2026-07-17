# 17 — Bundle Citations and the 🟢 Flag Convention

> **A Wave-7 finding**: 10 of 52 entries in
> `sxl-operators.md` cite 2-3 primary sources
> under one entry. The bundle format makes
> the "single primary source" criterion hard
> to apply cleanly. The Wave 7 verification
> pass flagged these as 🟢 `confirmed-curated`
> (the underlying concept is well-established,
> but the entry bundles multiple primary
> sources). This chapter documents the
> bundle convention, names the affected
> entries, and proposes a resolution.

## Why this chapter

The `sxl-operators.md` file (52 entries) is
the *symbolic* side of the deep-research
corpus: knowledge representation, reasoning,
belief revision, causal inference, and
decision-theoretic operators. Many of these
operators have *evolved* over decades: a
1995 paper introduces the concept, a 2009
book formalises it, and a 2015 paper extends
it. The deep-research entries often cite the
*concept* (with a one-line description) and
the *multiple primary sources* (the
historical chain).

The bundle citation pattern is:

- **§1.3 Abstract Dialectical Frameworks
  (ADF)**: Brewka et al. 2011 (the
  technical report that introduces the
  framework) and Brewka et al. 2018
  (a later paper on cognitive computing
  applications) — same authors, evolution
  of the same framework.
- **§3.2 Simplex, branch-and-cut, and
  LP/MIP solvers**: Dantzig 1947 (simplex
  algorithm), Gomory 1958 (cutting planes),
  Land & Doig 1960 (branch-and-bound),
  Bixby 2000 (CPLEX modern form) — a
  chain of refinements to the same OR
  method family.
- **§5.1 Bayesian Networks — Variable
  Elimination**: Zhang & Poole 1994 (the
  basic VE algorithm) and Dechter 1996
  (the bucket-elimination framework) — two
  different formulations of VE.
- **§5.2 Belief Propagation (sum-product)**:
  Pearl 1982 (BP on Bayesian networks) and
  Kschischang, Frey, Loeliger 2001 (BP on
  factor graphs) — two different
  formulations of BP.
- **§6.1 Conceptual Graphs (CG)**:
  Sowa 1976/1984 (the foundational book
  *Conceptual Structures*) and ISO/IEC
  24707:2007 (the Common Logic standard
  that subsumes CG) — same concept, an
  evolving standard.
- **§6.2 Description Logic Knowledge Bases
  (DL-Lite, EL++)**: Calvanese et al. 2007
  (DL-Lite) and Baader, Brandt, Lutz 2005
  (EL++) — two different DL families.
- **§7.4 Genetic Algorithm (GA)**: Holland
  1975 (the foundational book *Adaptation
  in Natural and Artificial Systems*) and
  Goldberg 1989 (the classic textbook) —
  same concept, two foundational works.
- **§8.2 Forward Chaining with Datalog**:
  Ceri, Gottlob, Tanca 1989 (the
  foundational book *Logic Programming and
  Databases*) and Abiteboul, Hull, Vianu
  1995 (*Foundations of Databases*) — two
  textbook references on the same topic.
- **§10.1 Pearl's Causal Calculus
  (do-calculus)**: Pearl 1995 (the
  *Biometrika* paper) and Pearl 2009 (the
  *Causality* book) — same author, the
  paper that introduces do-calculus and
  the book that formalises it.
- **§11.2 Progol / Aleph**: Muggleton 1995
  (the Progol paper) and Srinivasan 2001
  (the Aleph manual) — Progol theory and
  its Aleph implementation.

Each bundle is a *single entry* in the file
but a *chain* of primary sources. The Wave 7
verification pass cannot apply the "single
primary source" criterion cleanly: which
source in the bundle is the *canonical* one?
The concept is well-established (the
operator exists in the literature) but the
entry's *citation* is a chain, not a single
paper.

The Wave 7 convention was to flag these as 🟢
`confirmed-curated` (the underlying concept is
well-known but the specific citation is
approximate). This is a reasonable default
but it is conservative: 10 of 52 entries
(19%) get 🟢 when most of them would be ✅ if
the entry cited a single primary source.

## The proposed resolution

There are two reasonable resolutions. The
sapling author agents should pick one and
apply it consistently across the corpus.

### Resolution A: Split bundle entries

Each bundled source becomes its own entry. For
example, §10.1 do-Calculus becomes:

- §10.1a do-Calculus (Pearl 1995, *Biometrika*)
- §10.1b do-Calculus formalisation (Pearl 2009,
  *Causality*)

The advantage: each entry has a single
canonical source, the "single primary source"
criterion applies cleanly, and most entries
become ✅.

The disadvantage: the file's structure
expands. 10 bundle entries become 20-30
single-source entries, increasing the file
size and the navigation load.

### Resolution B: Document the bundle convention

Each bundle entry stays as one entry but the
`**Year / citation**` field is reformatted to
make the chain explicit:

> **Year / citation**: Reiter 1980 (default
> logic foundations); Antoniou 1997 (default
> logic semantics in *AI* 93(1-2): 237–263);
> Brewka 1994 (prioritised default logic).
> The three sources are bundled because the
> entry describes the *concept* (default
> logic), not a single paper.

The advantage: the file's structure is
preserved. The bundle convention is
documented; future verifiers know what to
expect.

The disadvantage: the entry remains 🟢
because no single primary source can be
verified.

The sapling project should pick one
resolution and apply it across the corpus.
The Wave 7 verification log notes the
affected entries by section number so the
resolution can be applied mechanically.

## Specific entries that need a resolution

The following 10 entries in
`sxl-operators.md` are bundled:

| § | Operator | Bundle | Recommended |
|---|----------|--------|-------------|
| 1.3 | Abstract Dialectical Frameworks (ADF) | Brewka et al. 2011 + Brewka et al. 2018 | Document |
| 3.2 | Simplex / branch-and-cut / LP-MIP | Dantzig 1947 + Gomory 1958 + Land & Doig 1960 + Bixby 2000 | Document |
| 5.1 | BN Variable Elimination | Zhang & Poole 1994 + Dechter 1996 | Split |
| 5.2 | Belief Propagation (sum-product) | Pearl 1982 + Kschischang, Frey, Loeliger 2001 | Split |
| 6.1 | Conceptual Graphs (CG) | Sowa 1976/1984 + ISO/IEC 24707:2007 | Document |
| 6.2 | DL-Lite / EL++ | Calvanese et al. 2007 + Baader, Brandt, Lutz 2005 | Split |
| 7.4 | Genetic Algorithm (GA) | Holland 1975 + Goldberg 1989 | Document |
| 8.2 | Forward Chaining with Datalog | Ceri, Gottlob, Tanca 1989 + Abiteboul, Hull, Vianu 1995 | Document |
| 10.1 | do-Calculus (Pearl) | Pearl 1995 + Pearl 2009 | Document |
| 11.2 | Progol / Aleph | Muggleton 1995 + Srinivasan 2001 | Document |

The recommended column is the agent's
recommendation based on the entry's content.
The "Split" rows are entries where the two
sources describe *different algorithms or
frameworks* (e.g., Zhang & Poole 1994's basic
VE is a different algorithm from Dechter
1996's bucket-elimination framework; BP on
Bayesian nets and BP on factor graphs are
two different formulations; DL-Lite and
EL++ are two different DL families). The
"Document" rows are entries where the
sources describe the *same concept* at
different levels of formality or stages of
evolution (e.g., Holland 1975 and Goldberg
1989 are both about genetic algorithms;
Pearl 1995 and Pearl 2009 are both about
do-calculus; Brewka 2011 and 2018 are by
the same authors on the same framework).

## How to read this chapter

If you are authoring a new entry:

1. If your entry cites a single primary
   source, the entry is ✅.
2. If your entry cites two sources that
   describe the *same concept*, write the
   entry as one entry and use the "Document"
   format (Resolution B).
3. If your entry cites two sources that
   describe *different algorithms or
   frameworks*, split the entry into two
   (Resolution A).

If you are running a verification wave:

1. For each entry, identify the bundled
   sources.
2. Apply the resolution (A or B) consistently.
3. Re-flag the entry: split entries become
   ✅ if their primary source is verified;
   documented bundles stay 🟢 unless the
   entry's primary source is verified.

If you are a future reader:

1. The 🟢 flag on a bundle entry is not a
   failure — it is the convention. The
   underlying concept is well-established;
   the entry's *citation* is a chain, not a
   single paper.
2. Open the entry's `**Canonical reference**`
   URL (or URLs) to find the primary source.

## See also

- [`../sapling/12-DISCOVERY-PATTERN.md`](12-DISCOVERY-PATTERN.md) — the
  DRIRR document pattern. The bundle
  convention is the DRIRR pattern's
  "Reasoning" section applied to citation
  metadata: the *reason* for the bundle is
  the entry's concept-level scope.
- [`../sapling/15-AUTHOR-LIST-PRECISION.md`](15-AUTHOR-LIST-PRECISION.md) —
  the author-list precision convention.
  Bundle entries often have multiple author
  lists (one per source); the precision
  convention applies to *each* list, not to
  the bundle as a whole.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-sxl.md` —
  the Wave 7 SXL verification log, which
  flagged the bundle-citation pattern and
  the 10 affected entries.
