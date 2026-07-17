# 16 — SXL → NSL Rename Harmonisation

> **A Wave-7 cross-cutting finding**: the
> `neuro-primitives.md` preamble still uses
> "SXL" / "SXL integration" but the companion
> `nslp-algorithms.md` uses "NSL" / "NSP" (the
> user-approved rename). This chapter proposes
> the harmonisation, names the affected files,
> and proposes a docs/adr/ entry to record the
> rename decision explicitly.

## Why this chapter

The deep-research files use two terms for the
same symbolic / cognitive layer:

- **SXL** (Symbolic eXpression Language) — the
  early name, used in the original codex and
  S.E.E.D. documentation.
- **NSL** (Neuro-Symbolic Language) and **NSP**
  (Neuro-Symbolic Processor) — the renamed
  terms, used in the more recent sapling NSLP
  documentation.

The rename was approved by the user in a prior
session but the *propagation* across all
solbian files was incomplete. Three of the
seven deep-research files still use "SXL" in
their preambles or section headers; the NSLP
specification, NSP runtime, and the
nslp-algorithms.md and memory-reasoning.md
files use "NSL" / "NSP."

This is a low-effort, high-impact
harmonisation. The terms refer to the same
thing; the inconsistency is a documentation
defect, not a design difference.

## The proposed harmonisation

The renamed terms are:

- **NSL** (Neuro-Symbolic Language): the
  symbolic language specification. Replaces
  SXL in all references.
- **NSP** (Neuro-Symbolic Processor): the
  runtime that compiles and executes NSL.
  Replaces SXL in all runtime references.
- **SXL** is retained as a *historical* name
  in the codex scrolls and the canonical
  glossary, where the term was first
  introduced, but is replaced by NSL in all
  sapling-level documentation.

The harmonisation is:

1. Update every "SXL" reference in
   `sapling/NSLP/deep-research/*.md` to "NSL"
   *unless* the reference is a direct quote
   from a codex scroll (where the historical
   name should be preserved).
2. Update every "SXL shape" field in
   `nslp-algorithms.md`, `cognitive-cycles.md`,
   `sxl-operators.md`, and `memory-reasoning.md`
   to "NSL shape."
3. Update the file *preambles* to use the
   renamed terms in the descriptive text.

## Affected files

The Wave 7 verification log flagged the
following files as using "SXL":

- `sapling/NSLP/deep-research/neuro-primitives.md` —
  preamble says "first-class SXL operators" and
  "SXL integration" but the file's body uses
  both "SXL shape" and "NSL shape" inconsistently.

The other deep-research files use "NSL" and
"NSP" already, but a sweep is needed to catch
stragglers:

- `sapling/NSLP/deep-research/sxl-operators.md` —
  the file name itself contains "sxl" but the
  body should use "NSL." The file name is a
  *path* concern, not a content concern; the
  file name is preserved for backward
  compatibility, but the preamble and section
  headers should use "NSL."
- `sapling/NSLP/deep-research/canonical-references.md` —
  the file name also contains "references" not
  the renamed term; this is correct.
- `sapling/NSLP/SPEC.md` — the NSL specification;
  should be checked for any remaining "SXL"
  references.
- `sapling/NSLP/ARCHITECTURE.md` — the NSP
  architecture; should be checked similarly.

The harmonisation is straightforward: any
"SXL" in the sapling documentation that is not
a direct codex-scroll quote becomes "NSL." The
file names that contain "sxl" are preserved
for backward compatibility; the file *content*
is harmonised.

## The proposed ADR

This is a documentation rename that crosses
files. A docs/adr/ entry should record the
decision explicitly:

- **ADR title**: "SXL → NSL rename propagation
  across the deep-research corpus"
- **Status**: Accepted (2026-07-17)
- **Context**: The deep-research files use
  "SXL" in some preambles and "NSL" in others.
  The terms refer to the same symbolic
  language; the inconsistency is a
  documentation defect.
- **Decision**: Replace "SXL" with "NSL" in
  all sapling-level documentation. Preserve
  the file names that contain "sxl" for
  backward compatibility. Preserve "SXL" in
  codex-scroll quotes and in the canonical
  glossary where the term was first
  introduced.
- **Consequences**:
  - Positive: a single term throughout the
    sapling documentation makes it easier
    for readers to follow cross-file
    references.
  - Negative: existing links from older
    documents (which used "SXL") may 404 if
    the linked anchors were renamed. The
    sweep should be coupled with a
    cross-reference check.
  - Neutral: codex-scroll quotes retain the
    historical "SXL" name; this is
    intentional and documented.

The ADR is the formal record. The
harmonisation pass is the implementation.

## How to read this chapter

If you are authoring a new entry in the
deep-research files:

1. Use "NSL" for the symbolic language, not
   "SXL."
2. Use "NSP" for the runtime, not "SXL."
3. If you need to refer to the historical
   name (e.g., "the SXL → NSL rename
   happened in 2026-04"), use the explicit
   phrase and the date.

If you are running a verification wave:

1. Grep the file for "SXL" in the body (not
   the file name).
2. If a "SXL" reference is not a direct
   codex-scroll quote, flag it 🟢 and add a
   `**Notes**` line: "rename to NSL pending."
3. If the file's preamble still uses "SXL,"
   request a harmonisation update.

If you are a future reader:

1. The terms "SXL" and "NSL" refer to the
   same language. Older documents may use
   "SXL"; newer documents use "NSL."
2. The canonical glossary retains "SXL" as
   the historical name; "NSL" is the
   preferred name in the sapling
   documentation.

## See also

- `docs/adr/` — the ADR directory. The proposed
  ADR for this rename lives there.
- [`../sapling/06-NSL-ISA-AND-RESEARCH-CORPUS.md`](06-NSL-ISA-AND-RESEARCH-CORPUS.md) —
  the NSL ISA chapter, which uses the renamed
  terms throughout. The harmonisation aligns
  the deep-research files with this chapter.
- `sapling/NSLP/SPEC.md` and
  `sapling/NSLP/ARCHITECTURE.md` — the NSL
  specification and NSP architecture, the
  canonical sources for the renamed terms.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-neuro.md` —
  the Wave 7 neuro-primitives verification log,
  which flagged the SXL → NSL harmonisation
  issue.
