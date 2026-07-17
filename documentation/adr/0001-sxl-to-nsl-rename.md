# ADR-0001: SXL → NSL Rename Propagation

- **Status**: Accepted
- **Date**: 2026-07-17
- **Deciders**: Solbian documentation steward (user-approved rename in
  prior session; this ADR records the propagation pass)
- **Supersedes**: —
- **Superseded by**: —

## Context

The deep-research corpus at
`/home/user/solbian/sapling/NSLP/deep-research/` uses two terms
for the same symbolic / cognitive layer:

- **SXL** (Symbolic eXpression Language) — the early name, used in
  the original codex and S.E.E.D. documentation.
- **NSL** (Neuro-Symbolic Language) and **NSP** (Neuro-Symbolic
  Processor) — the renamed terms, used in the more recent sapling
  NSLP documentation.

The rename was approved by the user in a prior session but the
*propagation* across all solbian files was incomplete. As of the
end of Wave 7, three of the seven deep-research files still used
"SXL" in their preambles or section headers; the NSLP
specification, NSP runtime, and the `nslp-algorithms.md` and
`memory-reasoning.md` files used "NSL" / "NSP."

This is a low-effort, high-impact harmonisation. The terms refer
to the same thing; the inconsistency is a documentation defect,
not a design difference. The Wave 7 cross-cutting finding
flagged the issue, and the design note
`documentation/engineering-manual/sapling/16-SXL-NSL-RENAME.md`
proposed the harmonisation with a record of the affected files.

## Decision

Replace "SXL" with "NSL" in all sapling-level documentation
under the deep-research corpus, applying the following rules:

1. **Field rename**: `**SXL shape**:` becomes `**NSL shape**:` —
   the field name is now a generic term for the entity form.
2. **Prose rename**: any reference to "SXL" in prose becomes
   "NSL" — including preambles, table entries, and process
   descriptions. The complementary rename "SXP" → "NSP" is
   applied where the two terms appear together (e.g.,
   "SXL/SXP operator layer" → "NSL/NSP operator layer").
3. **File names preserved**: the file name `sxl-operators.md`
   is kept for backward compatibility (it is referenced from
   other docs and the engineering manual). The body is
   renamed; the path is not.
4. **Verification logs preserved**: log file names containing
   "sxl" (e.g.,
   `claude-verifier-2026-07-17-wave7-sxl.md`) are historical
   and are not edited.
5. **Codex-scroll quotes preserved**: any direct quote from a
   codex scroll retains the historical "SXL" name.
6. **Canonical sources preserved**: the canonical specification
   documents (`sapling/NSLP/SPEC.md` and
   `sapling/NSLP/ARCHITECTURE.md`) are the source of truth for
   the SXL term and use it as a defined technical concept
   (SXL is the *data plane*; NSL is the *control plane*).
   These files are not part of the rename pass; the
   "SXL" → "NSL" mapping in them would be a semantic change
   rather than a documentation fix.
7. **Wave-6 file meta-commentary preserved**: the
   `nslp-algorithms.md` and `theorems-and-bounds.md` files
   include a "Naming note" that explicitly discusses the
   rename (`SXL/SST. This file uses NSL/NSP consistently. The
   earlier 4-file corpus ... retains SXL/SST because ...`).
   This meta-commentary is part of the historical record and
   is preserved; a future wave may update the commentary
   after Wave 8 brings the 4-file corpus into alignment.

## Alternatives Considered

| Alternative                                  | Pros                                                              | Cons                                                                                                | Why Rejected                                                                                                                                                  |
|----------------------------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Rename file `sxl-operators.md` to `nsl-operators.md` | Cleaner final state; no path mismatch.                          | Breaks every link from other docs (engineering-manual, the deep-research `README.md`, all 6 sibling deep-research files). Forces a multi-file anchor update. | File names are *path* concerns, not *content* concerns. Preserving the path keeps backward compatibility and avoids a cascade of broken links. |
| Wholesale rename in SPEC.md and ARCHITECTURE.md | Maximum consistency across all sapling docs.                    | The spec and architecture define SXL as a *distinct* technical concept (the data-plane language). Replacing SXL with NSL in them creates a semantic contradiction (NSL is the *control plane* in the same document). | The canonical sources are not glossary entries; they are the technical specification of the SXL term. The rename is about *propagation*, not *redefinition*. |
| Skip the rename entirely                      | No risk of breaking links or semantic confusion.                 | The documentation inconsistency remains; future readers continue to see "SXL" in some preambles and "NSL" in others. | The inconsistency is a real defect. The design note documents the user-approved rename; this ADR records the propagation pass.                                          |
| Update the "Naming note" in nslp-algorithms.md and theorems-and-bounds.md | Removes the now-stale "the 4-file corpus retains SXL/SST" claim.  | Out of scope of Wave 8 (which is a propagation pass, not a meta-commentary update). Modifying the "Naming note" requires re-verifying that the 4-file corpus is now aligned — this is what Wave 8 proves, so the update can come after this ADR. | Leave the meta-commentary intact for now; a follow-up wave can update the "Naming note" to reflect the new alignment.                                                                  |

## Consequences

### Positive

- A single term ("NSL") is used throughout the deep-research
  corpus. Readers following cross-file references no longer
  see "SXL" in one preamble and "NSL" in another.
- The `**NSL shape**` field name is now consistent across
  every entry in the deep-research corpus.
- The promotion path described in the README ("a
  ready-for-promotion algorithm becomes a first-class NSL
  operator") now uses the same vocabulary as the rest of
  the sapling documentation.

### Negative

- Existing links from older documents (which used "SXL") may
  404 if the linked anchors were renamed. The propagation
  pass should be coupled with a cross-reference check.
  Mitigation: a `grep -rn "SXL" sapling/NSLP/` was run after
  the rename and confirmed the only remaining "SXL"
  references in the deep-research files are (a) the
  `SXL_LANGUAGE_SPECIFICATION.md` file path in
  `sxl-operators.md` and `README.md` (preserved per the
  rules), and (b) the Wave-6 meta-commentary in
  `nslp-algorithms.md` and `theorems-and-bounds.md`
  (preserved per the rules).
- The "Naming note" in `nslp-algorithms.md` and
  `theorems-and-bounds.md` is now factually inaccurate
  (the 4-file corpus no longer "retains SXL/SST"). A
  future wave should update the note to reflect the
  post-Wave-8 state.

### Neutral

- Codex-scroll quotes retain the historical "SXL" name;
  this is intentional and documented.
- The canonical specification documents
  (`SPEC.md`, `ARCHITECTURE.md`) retain "SXL" as a
  defined technical term (the data plane); this is
  intentional and documented.
- File names containing "sxl" are preserved for
  backward compatibility; the rename is content-only.

## References

- `documentation/engineering-manual/sapling/16-SXL-NSL-RENAME.md`
  — the Wave 7 design note that proposed the harmonisation.
- `sapling/NSLP/SPEC.md` — the NSL specification (canonical
  source; not part of the rename pass).
- `sapling/NSLP/ARCHITECTURE.md` — the NSP architecture
  (canonical source; not part of the rename pass).
- `sapling/NSLP/deep-research/README.md` — the deep-research
  corpus overview, updated by this rename.
- `sapling/NSLP/deep-research/sxl-operators.md` — the file
  whose name preserves the historical "sxl" path; body
  renamed.
- `sapling/AGENTS.md`, `sapling/ENTITIES.md` — sapling-level
  docs updated by this rename.
- The Wave 7 verification log at
  `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-sxl.md`
  — the historical record of the cross-cutting finding
  (preserved; not edited by this rename).
