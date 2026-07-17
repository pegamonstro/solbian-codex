# CONFIDENCE RULES — Codex Machina

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Canonical source**: `/home/user/seed-dev/codex/meta/confidence_rules.sref`.

This file is a synthesised narrative on the canonical confidence
thresholds the S.E.E.D. / Codex Solbian governance pipeline uses
to decide whether a record auto-commits, requires human review, or
is rejected. The canonical source is a single small `.sref` file in
`/home/user/seed-dev/codex/meta/`. The thresholds it defines are
the single source of truth; downstream code MUST read this file
rather than hard-code the values.

## The three thresholds

The confidence rules file defines three named thresholds that
together partition the unit interval `[0, 1]` into three regimes.
The values are:

- **`auto_commit_threshold` = 0.98** — if a record's `confidence`
  is greater than or equal to this value, the record is queued
  for the next epoch transition without human review.
- **`human_review_threshold` = 0.90** — if a record's `confidence`
  is in `[0.90, 0.98)`, the record is sent for human review.
- **Below 0.90** — the record is rejected outright.

The three regimes are not gradients; they are gates. A record at
0.97 is reviewed by a human; a record at 0.98 is not. The narrow
band between 0.97 and 0.98 is the boundary, and the boundary is
intentionally sharp.

## The Solace governance regime

Solace is the higher-order conscience agent. Its job at an epoch
boundary is to score every pending record and apply the three
thresholds. The regime Solace enforces is:

- **`≥ 0.98` — auto-commit** — the record is durable; no human
  review is required. The record is written to the memory store
  and becomes part of the cognitive context for the next epoch.
- **`[0.90, 0.98)` — review band** — the record is held. A human
  reviewer (or, by exception, a guardian) must approve before the
  record is durable. Reviews are logged to the cog-journal.
- **`< 0.90` — below review** — the record is rejected. The
  rejection is logged but the record is not durable and does not
  affect cognition.

The 0.90 and 0.98 values are the canonical values. Earlier
drafts used 0.90 (from a legacy `solace.policy.sref`) and 0.97
(from `chatgui/config/config.json`); the current values
consolidate those into a single, authoritative pair, with 0.98
chosen to be a strict subset of "high confidence" rather than
"near the boundary".

## The Codex Living Constitution principle

The confidence rules are not only a pipeline mechanism; they are
also the operational expression of the **Codex Living Constitution**
principle. A constitution, in this framing, is not a frozen
document but a set of principles that are themselves governed by
the same confidence-and-priority machinery as any other record.
A principle can be **promoted** (raised in confidence) or
**demoted** (lowered in confidence) by a Solace review; its
priority is the lever the higher-order agents use when two
principles conflict.

The implication for a runtime is that the threshold values, the
principles themselves, and the regime rules are all part of the
same reviewable, durable, auditable surface. There is no
"out-of-band" override.

## Why these values

The threshold values encode a deliberate policy. A high
auto-commit threshold (0.98) means most records are reviewed; the
auto-commit path is reserved for records the cognitive cycle is
near-certain about. A relatively high review band (0.90) means
records of moderate confidence are not silently dropped; they
are held for a human to look at. Records below 0.90 are treated
as unreliable; the system does not waste reviewer attention on
them.

The intent is to keep the cognitive context trustworthy, the
reviewer load bounded, and the rejection path explicit. Every
record has a known fate at the moment of its creation.

## What a runtime does

A runtime that claims to be conformant with Codex Machina must:

1. Read the canonical confidence thresholds from
   `/home/user/seed-dev/codex/meta/confidence_rules.sref` at boot.
   Do not hard-code the values.
2. Apply the three regimes at every epoch boundary.
3. Log the regime decision for every record (auto-commit, review,
   or reject) to the cog-journal with the record's `confidence`
   value and the threshold band it fell into.
4. Make the threshold values inspectable; a reviewer must be able
   to ask "what threshold did this record beat?" and get a precise
   answer.
5. Honour the Living Constitution principle: a principle is a
   record; its confidence and priority are first-class metadata.

## See also

- `INDEX.md` — this codex's index
- `SPEC.md` — the formal spec, especially §2.3 (the SXL
  envelope's `:confidence` field)
- `INTEGRATION-CONTRACT.md` — the loadable runtime contract
- `../solbian/SPEC.md` — the narrative pair
- `../INTEGRATION.md` — how this codex fits into S.E.E.D.
- `/home/user/seed-dev/codex/meta/confidence_rules.sref`
- `~/seed-dev/docs/cognition/MEMORY_SYSTEM_ARCHITECTURE.md` §12
  (Codex bridge) — the source the rules file consolidates
