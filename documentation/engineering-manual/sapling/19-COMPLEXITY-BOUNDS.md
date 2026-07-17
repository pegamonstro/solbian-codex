# 19 — Complexity Bounds Coverage in the Operator Profile

> **A Wave-7 finding**: only 13 of 52 entries
> in `sxl-operators.md` include a
> `**Complexity**` field. For a file that
> promotes first-class SXL operators, missing
> complexity bounds makes the operator
> selection less principled. This chapter
> documents the gap, names the entries that
> are missing the field, and proposes how to
> add bounds for the remaining 39 entries.

## Why this chapter

`sxl-operators.md` is the *symbolic* side of
the deep-research corpus: 52 entries covering
knowledge representation, reasoning, belief
revision, causal inference, and
decision-theoretic operators. The file's
purpose is to profile each operator for
*promotion* to a first-class NSL operator in
the sapling's cognitive engine.

Operator selection — choosing which operator
to apply to a given problem — depends on the
operator's complexity bounds. A reader who is
deciding between forward chaining (linear in
rule count) and backward chaining
(exponential in the worst case) needs both
bounds to make the call. A complexity-free
profile forces the reader to look up the
bounds elsewhere, which breaks the file's
"promote-once, reference-often" purpose.

The Wave 7 verification pass recorded the
complexity coverage:

- 13 of 52 entries have a `**Complexity**`
  field.
- 39 of 52 entries do not.

The 13 entries with bounds are §1.1, §1.2,
§1.3, §2.1, §2.2, §2.3, §3.1, §5.5, §6.5,
§7.1, §8.3, §15.1, §15.2 — a mix of
foundational and applied operators. The 39
entries without bounds are spread across the
other categories.

## The proposed convention

Future authoring passes on the deep-research
files should follow this convention for the
`**Complexity**` field:

1. **Every entry has a `**Complexity**`
   field.** The field describes the
   algorithm's time and space complexity in
   terms of the input's natural size
   parameters. Example: "O(|R| · |F|) per
   forward-chaining step, |R| = rule count,
   |F| = fact count; O(|F|) space."

2. **The complexity bounds are in Big-O
   notation, with the size parameters
   named.** A reader should be able to
   read the bounds and substitute their
   input's size to estimate the cost. A
   bare "exponential" or "polynomial" is
   insufficient.

3. **The complexity bounds are sourced to
   the primary source.** The primary
   source's complexity analysis is the
   ground truth; the entry's
   `**Complexity**` field quotes or
   paraphrases the source's analysis. If
   the source does not provide a
   complexity analysis (rare for
   well-established algorithms), the
   entry's `**Notes**` field records
   "complexity bounds pending primary
   source."

4. **The complexity bounds are in
   "input-size" terms, not "problem-size"
   terms.** For example, a SAT solver's
   complexity is given in terms of the
   number of variables and clauses, not
   in terms of "the size of the problem."

5. **The complexity bounds distinguish
   worst-case, average-case, and
   amortised complexity when relevant.**
   For example, a union-find data
   structure's amortised complexity is
   near-constant, not the worst-case
   O(log n).

## Specific entries that need a complexity field

The 39 entries in `sxl-operators.md`
without a `**Complexity**` field are:

- §1.4-§1.7 (Belief revision: 4 entries)
- §3.2-§3.6 (SAT and CSP: 5 entries)
- §4.1-§4.6 (Probabilistic reasoning: 6
  entries)
- §5.1-§5.4 (Bayesian network inference: 4
  entries)
- §6.1-§6.4 (Description logics: 4 entries)
- §7.1-§7.4 (Modal and temporal logics: 4
  entries)
- §8.1-§8.2 (Logic programming: 2 entries)
- §9.1-§9.3 (Constraint satisfaction: 3
  entries)
- §10.1-§10.4 (Causal inference: 4 entries)
- §11.1-§11.2 (Decision theory: 2 entries)
- §12.1-§12.2 (Game theory: 2 entries)
- §13.1-§13.2 (Argumentation: 2 entries)
- §14.1-§14.2 (Planning: 2 entries)
- §16.1 (Additional: 1 entry)
- §17.1-§17.2 (Quantum: 2 entries)

For each entry, the next authoring pass
should:

1. Open the primary source (per the
   `**Canonical reference**` URL).
2. Find the complexity analysis in the
   source's main result (typically the
   theorem section).
3. Write the `**Complexity**` field as
   "O(f(n)) per operation; space O(g(n))."
4. Add a `**Notes**` line citing the
   theorem number or page in the source.

## How to read this chapter

If you are authoring a new entry:

1. Add a `**Complexity**` field.
2. Use Big-O notation with named size
   parameters.
3. Source the bounds to the primary
   source.

If you are running a verification wave:

1. Sweep the file for `**Complexity**`
   fields.
2. If an entry is missing the field, flag
   it 🟢 and add a `**Notes**` line:
   "complexity bounds pending."
3. If an entry has a `**Complexity**` field
   but the bounds are not in Big-O notation
   or do not name the size parameters,
   request a precision update.

If you are a future reader:

1. The `**Complexity**` field is a
   first-class field of the entry's
   profile, not optional. A missing
   field is a documentation defect, not
   a sign of an unbounded algorithm.
2. The bounds are worst-case unless
   otherwise noted. For amortised
   complexity, see the `**Notes**` field.

## See also

- [`../sapling/02-SYMBOLIC-LAYER.md`](02-SYMBOLIC-LAYER.md) — the
  symbolic layer chapter, which discusses
  the operator selection problem and the
  role of complexity bounds in NSL.
- [`../sapling/06-NSL-ISA-AND-RESEARCH-CORPUS.md`](06-NSL-ISA-AND-RESEARCH-CORPUS.md)
  — the NSL ISA chapter, which includes
  the operator selection algorithm and
  its complexity analysis.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-sxl.md` —
  the Wave 7 SXL verification log, which
  flagged the complexity-bounds coverage
  gap.
