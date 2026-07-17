# Verification Log

> **Append-only verification
> records for the cognitive-engine
> research knowledge base**.
> Each verifier (a human reviewer
> or the verification sub-agent)
> creates a file in this directory
> and appends entries as they
> confirm or correct algorithm
> profiles in the parent
> `~/solbian/sapling/NSLP/research/`
> files.
>
> **Last updated**: 2026-07-16.

## Why this directory exists

Every algorithm profile in the
knowledge base carries a
`confirmation` flag (see
`../README.md` for the full
ladder). The default flag for new
entries is 🟡 `unconfirmed`.
Promotion to first-class SXL
operator status in
`~/seed-dev/` requires
✅ `confirmed-canonical` or
🟢 `confirmed-curated`.

The verification directory is
the durable record of who
upgraded which entry and when.
Every entry added here is
append-only; corrections are
new entries that point at the
old ones.

## How verification works

For each 🟡 or 🟠 or 🔴 entry,
a verifier does the following:

1. **Read** the primary source
   (the cited paper or textbook
   chapter). For textbooks,
   read the chapter cited in
   the profile.
2. **Confirm** the year, author
   list, venue, and reference
   URL. If any is wrong, the
   verifier corrects the
   profile in the parent file
   and adds a verification
   entry here noting the
   correction.
3. **Re-derive** the worked
   example and the pseudocode
   from the primary source. If
   the worked example does not
   match the primary source,
   the verifier either fixes
   the worked example or
   downgrades the flag to
   🔴 `speculative` and
   re-flags the entry.
4. **Re-check** the complexity
   claim against the literature.
   If the complexity is wrong,
   the verifier updates the
   profile.
5. **Update** the flag in the
   profile.
6. **Add** a verification entry
   to the appropriate log file
   in this directory.

## File naming convention

Each verifier's log file is named
`<verifier-name>.md` (kebab-case
slug). Example:
`claude-verifier-2026-07-16.md`.

A single session can have
multiple log files (one per
verifier) if multiple verifiers
run in parallel.

## Entry format

Each entry in a log file uses
this format:

```markdown
## <entry-id> — <profile-name>

- **Verifier**: <name>
- **Date**: <YYYY-MM-DD>
- **Source consulted**: <URL
  or textbook chapter>
- **Action**: confirmed |
  corrected | downgraded
- **Old flag**: 🟡 unconfirmed
- **New flag**: ✅ confirmed-
  canonical
- **Notes**: <any issues found
  and how they were fixed>
```

## Example entry

```markdown
## agm-belief-revision — AGM
Belief Revision

- **Verifier**: claude-verifier
- **Date**: 2026-07-16
- **Source consulted**:
  https://www.cse.iitd.ac.in/~saro
  j/AGM/p510-alchourron.pdf
- **Action**: confirmed
- **Old flag**: 🟡 unconfirmed
- **New flag**: ✅ confirmed-
  canonical
- **Notes**: Year (1985),
  authors (Alchourrón, Gärdenfors,
  Makinson), venue (J. Symb.
  Logic 50(2): 510-530) all
  verified. The 8 AGM postulates
  correctly listed. Reference
  URL is the primary source.
```

## Files in this directory

- `claude-verifier-2026-07-16.md`
  — verification log from the
  initial 2026-07-16 session.
  7 entries spot-checked; 3
  promoted to ✅
  (Transformer attention,
  Dopamine RPE, plus
  textbook re-confirms of
  AIMA and Bishop); 4
  promoted to 🟢 (PAC,
  natural gradient, Hebbian,
  Valiant textbook re-confirm
  was already ✅) after URL
  fixes.
- `humans.md` — human-reviewer
  log; entries from manual
  review.

## How to add a verification entry

1. Read the profile in the
   parent file.
2. Look up the cited primary
   source.
3. Compare the profile to the
   source.
4. Open or append to the
   verifier's log file in this
   directory.
5. Add the entry in the format
   above.
6. Update the profile's flag in
   the parent file.

The verification log is the
authoritative record of who
flagged what when. The profile
flags are kept in sync but the
log is the source of truth.

## Promotion gate

An algorithm profile is
`ready-for-promotion` to
`~/seed-dev/codex/machina/`
only if:

- The flag is ✅
  `confirmed-canonical` or 🟢
  `confirmed-curated`.
- A verification entry exists
  in this directory recording
  the confirmation.
- The promotion is reviewed by
  a human before any code lands
  in `~/seed-dev/`.

See `../README.md` §"The
promotion path" for the full
flow.

## See also

- `../README.md` — overview,
  promotion criteria, cognitive-
  engine layer mapping.
- `../sxl-operators.md` —
  symbolic cognitive algorithms.
- `../cognitive-cycles.md` —
  cognitive cycle and time-
  series algorithms.
- `../neuro-primitives.md` —
  neuro-computational
  primitives.
- `../memory-reasoning.md` —
  memory architectures and
  reasoning algorithms.
- `../theorems-and-bounds.md` —
  mathematical backbone.
- `../nslp-algorithms.md` —
  operator-level deep
  mechanics.
- `../canonical-references.md`
  — the master reference list.
