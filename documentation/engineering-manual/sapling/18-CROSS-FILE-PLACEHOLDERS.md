# 18 — Cross-File Placeholder Dependencies

> **A Wave-7 finding**: 19 of 51 entries in
> `memory-reasoning.md` are placeholder
> cross-references to `sxl-operators.md` and
> `cognitive-cycles.md` ("Covered in X.md").
> The Wave 7 verification pass flagged these
> as 🟢 `confirmed-curated` (the underlying
> concept is well-established, but the
> *sibling-file cross-reference* is not yet
> verified). This chapter documents the
> dependency, names the affected entries, and
> proposes how the dependency should be
> resolved in future waves.

## Why this chapter

`memory-reasoning.md` covers 51 entries across
6 sections: §1 Memory architectures, §2
Knowledge representation, §3 Reasoning
algorithms, §4 Distributed reasoning, §5
Causal reasoning, §6 Reinforcement learning.
The file is the *applied* side of the
deep-research corpus: how memory and
reasoning are integrated in the sapling's
cognitive engine.

Many of the entries in `memory-reasoning.md`
*depend* on entries in the *lower-level*
files:

- `sxl-operators.md` defines the symbolic
  operators (the *language*).
- `cognitive-cycles.md` defines the cognitive
  cycles (the *temporal* layer).
- `nslp-algorithms.md` defines the
  operator-level algorithms (the *runtime*
  layer).

The `memory-reasoning.md` file uses the
operators, runs the cycles, and applies the
algorithms. Its entries often cite
"Covered in `sxl-operators.md` §X" or
"Covered in `cognitive-cycles.md` §Y"
rather than re-citing the primary source.

This is a *cross-file placeholder
dependency*. The Wave 7 verification pass
flagged the 19 placeholder entries as 🟢
because the placeholder format is a valid
citation *within the deep-research corpus*
but is not a primary source. The entry's
*verification* depends on the *sibling
file's verification*.

## The 19 placeholder entries

The Wave 7 verification log lists the
placeholder entries. They are concentrated
in:

- **§3 Reasoning algorithms**: most entries
  cite a primary source in the reasoning
  literature but also cross-reference
  `sxl-operators.md` for the operator
  definitions.
- **§4 Distributed reasoning**: PBFT, Raft,
  CRDTs, etc. — the entries cite the
  consensus protocol's primary source but
  also cross-reference `sxl-operators.md` for
  the *symbolic* part of the protocol.
- **§6 Reinforcement learning**: Q-learning,
  DQN, A3C, PPO, SAC, etc. — the entries
  cite the algorithm's primary source but
  also cross-reference `cognitive-cycles.md`
  for the *cognitive* framing.

The Wave 7 verification pass resolved the
placeholder entries to 🟢 because:

- The *underlying concept* is well-established
  (Q-learning, DQN, A3C, etc. are textbook
  topics).
- The *primary source* is verified (Watkins
  1989/1992 for Q-learning, Mnih 2013/2015
  for DQN, Mnih 2016 for A3C, Schulman 2017
  for PPO, Haarnoja 2018 for SAC).
- The *sibling-file cross-reference* is to
  files that have *not yet been verified*.

After Wave 7 verified `sxl-operators.md` and
`cognitive-cycles.md`, the cross-references
are now also verified (indirectly). The
placeholder entries can be promoted from 🟢
to ✅ in a Wave 8 cross-file consistency pass.

## The proposed resolution

The cross-file placeholder dependencies
should be resolved in three steps:

1. **Wave 8 cross-file consistency pass**:
   for each `memory-reasoning.md` entry that
   cross-references a now-verified entry in
   `sxl-operators.md` or `cognitive-cycles.md`,
   promote the entry from 🟢 to ✅. The
   promotion can be mechanical: the
   verification log records the cross-reference;
   the next pass greps the sibling file and
   confirms the cross-referenced entry is ✅.
2. **Replace the placeholder format with a
   canonical-reference cross-link**: instead
   of "Covered in `sxl-operators.md` §X,"
   write "See `sxl-operators.md` §X (canonical
   reference: <URL>)." This makes the
   cross-reference a *first-class citation*
   rather than a placeholder.
3. **Add a `**Cross-references**` field**: the
   entry's `**Cross-references**` field lists
   every sibling file the entry depends on,
   with each sibling entry's current flag. A
   reader can see at a glance whether the
   sibling entry is verified.

The three-step resolution is mechanical and
low-effort. The first step (Wave 8 promotion)
can be done in a single grep; the second and
third steps require a small author pass per
file.

## Specific entries that need a resolution

The 19 placeholder entries in
`memory-reasoning.md` are:

- §3.1-§3.5 (Reasoning algorithms): 5
  entries that depend on `sxl-operators.md`
  for the operator definitions.
- §4.1-§4.7 (Distributed reasoning): 7
  entries that depend on `sxl-operators.md`
  for the symbolic-part operator
  definitions.
- §6.1-§6.10 (Reinforcement learning): 7
  entries that depend on `cognitive-cycles.md`
  for the cognitive-framing cycle
  definitions.

Each entry's cross-reference is listed in
the Wave 7 verification log. The next pass
should:

1. Open each `memory-reasoning.md` placeholder
   entry.
2. Open the cross-referenced entry in the
   sibling file.
3. Confirm the sibling entry is ✅ (it is,
   after Wave 7).
4. Promote the `memory-reasoning.md` entry
   from 🟢 to ✅.
5. Update the entry's `**Year / citation**`
   field to add the cross-reference as a
   proper canonical reference (per Resolution
   step 2 above).

## How to read this chapter

If you are running a verification wave:

1. After promoting entries, sweep all
   `**Cross-references**` (or "Covered in X.md")
   fields in the file.
2. For each cross-reference, open the
   sibling file and confirm the cross-referenced
   entry's flag.
3. If the sibling entry is ✅, the
   cross-referencing entry can be promoted
   from 🟢 to ✅ (assuming the cross-referencing
   entry's own primary source is also ✅).

If you are authoring a new entry that
cross-references a sibling file:

1. Use the format "See
   `sxl-operators.md` §X (canonical reference:
   <URL>)" rather than "Covered in
   `sxl-operators.md` §X."
2. Add a `**Cross-references**` field that
   lists every sibling file the entry
   depends on.

If you are a future reader:

1. A 🟢 flag on an entry with a
   `**Cross-references**` field means the
   entry's *concept* is verified but the
   *sibling files* are still in the process
   of being verified. Once the sibling
   files are verified, the entry's flag is
   promoted.
2. The cross-reference is a *first-class
   citation*, not a placeholder. The sibling
   file's entry is the primary source for
   the cross-referenced concept.

## See also

- [`../sapling/13-DETECTING-LLM-HALLUCINATIONS.md`](13-DETECTING-LLM-HALLUCINATIONS.md) —
  the LLM hallucination pattern. Cross-file
  placeholders can be confused with
  hallucinated citations; the resolution
  above makes the cross-reference explicit
  so a future verifier does not flag the
  cross-reference as a fabrication.
- [`../sapling/15-AUTHOR-LIST-PRECISION.md`](15-AUTHOR-LIST-PRECISION.md) —
  the author-list precision convention.
  Cross-references inherit the *author list*
  of the sibling file's entry; the precision
  convention applies to the cross-referenced
  entry, not the cross-referencing one.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-memreason.md` —
  the Wave 7 memory-reasoning verification
  log, which flagged the 19 placeholder
  entries and the cross-file dependency.
