# 14 — Stale Status Banners and Promotion Summary Tables

> **A Wave-7 finding**: every deep-research file
> carries a `**Status (YYYY-MM-DD)**` banner in its
> preamble and a `## Promotion Summary` table at
> the end. After Wave 7 verification, all 4
> banner / table pairs are stale. This chapter
> documents the staleness, names the convention
> that should keep them current, and lists the
> specific updates needed.

## Why this chapter

The 4 unscoped deep-research files each open with
a status banner like:

> **Status (2026-07-16)**: 30 algorithms profiled
> across 8 categories. 18 are flagged
> ready-for-promotion.

…and close with a `## Promotion Summary` table
that aggregates the `**Ready-for-promotion**`
flags. After Wave 7 verification, *every* one of
these banner / table pairs is wrong:

- The banner date is from the *authoring* pass,
  not the *verification* pass.
- The banner entry count is from the *original*
  authoring pass, not the current entry count
  (most files gained entries between authoring
  and verification).
- The banner ready-for-promotion count is from
  the authoring pass's optimistic flag, not the
  verification pass's stricter one.
- The Promotion Summary table at the bottom
  lists only a *subset* of the entries, with
  mismatched category labels in some cases.

This is a Wave 8 housekeeping item. The
verification wave *upgrades* the per-entry flags
but does not update the file-level summary; the
two are out of sync by design. A separate pass
must reconcile them.

## The convention that should keep them current

The deep-research files should follow three rules
to keep the banners and tables in sync:

1. **The status banner is updated on every
   authoring pass and on every verification
   pass.** A simple rule: when the last entry's
   flag changes, the banner must change. When a
   new entry is added, the banner's entry count
   must change.

2. **The status banner's date is the date of the
   *last* flag change, not the date of the last
   authoring pass.** A banner dated 2026-07-16
   that describes post-Wave-7 (2026-07-17) flag
   state is incorrect; the date must be the date
   the flags were last changed.

3. **The Promotion Summary table at the end of
   each file has one row per entry.** Bundling
   multiple entries into one row (e.g., "RBM /
   CD", "LSTM / GRU", "NTM / DNC") is acceptable
   in the body, but the summary table must list
   each entry by its `### N.M` heading so the
   reader can find the entry from the table.

## Specific updates needed

The Wave 7 verification log records the
discrepancies per file. The next authoring pass
should:

### `sxl-operators.md`

- **Banner**: claims "30 algorithms profiled
  across 8 categories; 18 are flagged
  ready-for-promotion." Should be "52 entries
  across 17 categories; 51 ready-for-promotion,
  1 ⚠️ (Quantum Walks §17.2, by design)."
- **Promotion Summary table** (§18): lists 18 of
  52 entries, with mismatched category labels
  (e.g., "Quantum" missing; "Belief revision"
  lists only 1 of 3 belief-revision algorithms).
  Should list all 52.

### `cognitive-cycles.md`

- Banner / summary table state: not flagged as
  stale in the Wave 7 verification log, but the
  5 citation corrections applied to the body
  (Bayesian Surprise venue, Synaptic Tagging
  pages, Hippocampal Replay title, DYNA venue,
  Type-2 SDT journal) should be reflected in any
  summary that names them.

### `neuro-primitives.md`

- **Banner**: claims "30 algorithms profiled
  across 7 categories. 24 flagged
  ready-for-promotion." Should be "39 entries
  across 8 categories; 39 ✅
  `confirmed-canonical`."
- **Promotion Summary table** (§8): has 30 rows
  but the file has 39 entry headers. The
  discrepancy is because some entries are
  combined (e.g., 1.5 Boltzmann + RBM is one
  row "RBM / CD"). The table should be expanded
  to 39 rows to fully align with the entry list.

### `memory-reasoning.md`

- **Banner**: claims "32 algorithms profiled,
  26 ready-for-promotion." Should be "51
  entries; 26 ✅, 24 🟢, 1 🔴
  (Compressive Memory §1.5)."
- **Promotion Summary table** (§7): only lists
  31 of 51 algorithms; missing ACT-R, Compressive
  Memory, CDCL, SimAnneal, GA, CMA-ES, PSO, Ant
  Colony, Rete, ASP, 1.4 ACT-R, 6.8 PPO, 6.9 SAC,
  and 6.10 AlphaZero/MuZero. The table needs to
  be updated to match the new flag distribution.

## Why this matters

The status banner is the *first* thing a reader
sees. If it is wrong, the reader's mental model
of the file is wrong. A reader who sees
"30 algorithms, 18 ready" will skip entries that
are actually ready; a reader who sees "30
algorithms" will not know to look for the 9
additional entries the verification wave added.

The Promotion Summary table is the *last* thing a
reader sees. If it is incomplete, the reader
cannot use it to navigate the file. The summary
table is the file's "table of contents" — if it
is wrong, the file's navigability is degraded.

Both are *low-effort, high-impact* updates. A
single authoring pass can refresh all four files
in less than an hour. The convention proposed
above ensures the staleness does not recur.

## How to read this chapter

If you are running a verification wave:

1. After promoting entries, run a grep for
   `**Status (` and `## Promotion Summary` in
   each file. Confirm the banner's entry count
   and ready-for-promotion count match the
   post-wave flag state. If they do not, fix
   them as part of the same wave.

2. Confirm the Promotion Summary table lists
   every entry. If entries are missing, add
   them with their new flag.

3. Record the banner / table update in the
   verification log's `## Parent-file changes`
   section.

If you are authoring a new entry:

1. Update the status banner's entry count.
2. If your new entry introduces a new
   category, update the banner's category
   count.
3. Add a row to the Promotion Summary table
   for your new entry.

If you are a human reviewer:

1. Read the banner first. Confirm it matches
   the file's actual state.
2. If the banner is stale, request a refresh
   before relying on the file.

## See also

- [`../sapling/12-DISCOVERY-PATTERN.md`](12-DISCOVERY-PATTERN.md) — the
  DRIRR document pattern. The banner is the
  file's "Result" section; the Promotion
  Summary table is the file's "Revision"
  pointer. Both should be updated together
  when a verification wave lands.
- [`../sapling/13-DETECTING-LLM-HALLUCINATIONS.md`](13-DETECTING-LLM-HALLUCINATIONS.md) —
  the LLM-hallucinated citation pattern. Some
  of the stale banner counts may themselves be
  LLM hallucinations; Wave 7's "differentiable
  plasticity has 4 authors" finding is an
  example of an LLM-hallucinated count
  (different entry counts in different files
  for the same paper).
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-*.md` —
  the four Wave 7 verification logs, each with
  a "Stale file header" or "Stale Status
  banner" finding in the design-notes section.
