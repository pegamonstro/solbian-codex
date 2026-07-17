# 02 — The Living Constitution

> **Status**: Draft synthesis, version 0.1.0.
> **Last updated**: 2026-07-16.
> **Purpose**: A single document on the Living Constitution principle
> of the codex, the Recursive Codex loop that makes it operational,
> and the confidence and priority models that govern principle
> promotion and demotion.

This document sits between `solbian/SYNTHESIS.md` (the top-level
narrative) and `machina/CONFIDENCE-RULES.md` (the formal threshold
specification). Its job is to gather into one place everything that
the principle implies: how a codex principle is structured, how
its confidence moves, how it interacts with the rest of the
cognitive organism through the recursive loop, and what the
runtime must do to remain conformant with the constitution the
codex declares.

The Living Constitution principle is the second of the two
constitutional mechanisms the codex provides (the first being
the 48 laws themselves). Together they are what makes the codex
a constitution rather than a guideline: binding but evolving,
cumulative but auditable, extensible but final.

## 1. The principle

The Living Constitution principle declares that the codex is not
a static document; it is a **living policy artefact** whose
principles are themselves records under the same governance
machinery as any other SXL entity. Each principle carries two
first-class metadata values: **confidence** and **priority**.
The two values are independent. Confidence expresses how well the
principle is supported by evidence; priority expresses how
strongly the principle dominates when it conflicts with another.

The principle is the operational expression of the **Codex Living
Constitution** clause in `codex/INTEGRATION.md:215` and the
corresponding passage in `codex/machina/CONFIDENCE-RULES.md:56`.
Its canonical source is
`/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt:1518` — the
line in the seed-cog3 cognitive specifications that states
"The Codex Solbian becomes a living constitutional record." The
solbian version of the principle is the curated narrative; the
seed-dev version is the source-of-truth.

Three operational implications follow:

- **Laws carry confidence.** A principle can be **promoted**
  (raised in confidence) or **demoted** (lowered in confidence)
  by a Solace review at an epoch boundary.
- **Laws are records.** A principle is an SXL record under the
  same governance machinery as any other cognitive artefact; its
  confidence and priority are first-class metadata, not
  out-of-band annotations.
- **Laws are versioned and extendable.** A future law that
  harmonises with prior law is a valid amendment; a future law
  that violates prior law is not a law. Law XLVIII (Finality)
  declares the constitution binding, cumulative, and extendable.
  Law XXVI (Continuity of Codex) requires that the codex itself
  be preserved, extended, and migrated, signed and validated
  across generations.

The same statute that constrains synthetic conscience constrains
the codex's own evolution. The codex is self-referential by
design: the Living Constitution principle is itself subject to
the regime it declares.

## 2. The structure of a principle

A codex principle is an SXL record with a fixed schema. The
required fields are:

- **`id`** — a stable, hierarchical identifier (e.g.
  `codex.principle.persistence-precedes-intelligence`). The id
  is permanent; renames preserve the id and add a redirect.
- **`title`** — a human-readable short name.
- **`claim`** — the formal statement of the principle, in
  language precise enough to be evaluable.
- **`evidence`** — the supporting observations and citations.
  Evidence is itself a list of SXL records, each with its own
  confidence.
- **`confidence`** — a value in `[0, 1]` expressing the degree
  to which the evidence supports the claim. See §4.
- **`priority`** — a value in `[0, 1]` expressing how strongly
  the principle dominates in conflict resolution. See §5.
- **`related-principles`** — explicit pointers to principles
  that this one supports, contradicts, or extends.
- **`status`** — one of `proposed`, `active`, `canonical`, or
  `retired`. The status is itself derived from the confidence
  band; see §3.
- **`history`** — a log of every confidence/priority change,
  with timestamp, reviewer, and the evidence that triggered the
  change.

The schema is normative, not aspirational. A runtime that claims
Codex Machina conformance reads the schema from
`/home/user/seed-dev/codex/machina/schemas/sref-v2.sref` and
rejects any principle that does not match.

## 3. The status lifecycle

> **Editorial note**: The four-state lifecycle described here
> is a **solbian-side editorial proposal**. No canonical
> `~/seed-dev/` or `~/robot-dev/` source specifies these four
> statuses by name. The 0.98/0.90 thresholds in
> `~/seed-dev/codex/meta/confidence_rules.sref` are real
> (auto-commit ≥ 0.98, review band 0.90–0.98, below < 0.90)
> and are documented in `codex/machina/CONFIDENCE-RULES.md`;
> the assignment of these thresholds to specific lifecycle
> states is solbian's structuring of the canonical regime.
> Treat the lifecycle as the solbian authors' model of how
> the canonical regime operates, not as a claim about
> upstream code.

A principle moves through four statuses. The transition is
governed by the Solace regime, which reads the three canonical
thresholds from
`/home/user/seed-dev/codex/meta/confidence_rules.sref` and
applies them at every epoch boundary.

- **`proposed`** — the principle has been written but is not
  yet in force. New principles enter the codex in this status.
- **`active`** — the principle is in force for the cognitive
  cycle. It is applied to new cases and consulted during
  conflict resolution.
- **`canonical`** — the principle has been confirmed over many
  reviews and is treated as a load-bearing statute. Promotion
  to `canonical` is a deliberate act, not a routine transition.
- **`retired`** — the principle is no longer in force but is
  retained for the historical record. A retired principle is
  read-only; it is never demoted further and never reactivated.

The transitions are governed by the confidence thresholds, but
the thresholds map onto status in a deliberately non-linear way.
A principle in `[0.90, 0.98)` is held for review; a principle
that clears review enters `active`. A principle in `[0.98, 1.0]`
is auto-committed; for a *new* principle this still means
`active` until a reviewer (or Solace by exception) marks it
`canonical`. Retirement is the demotion of a principle out of
`active` or `canonical` when counter-evidence accumulates; a
retired principle retains its history and is cited in
`/home/user/solbian/LOG.md` so that future readers understand
why it was set aside.

A worked example: principle
`codex.principle.reflection-needs-topology` is formalised in
`codex/solbian/DISCOVERIES.md:57` as SD-0002. It entered the
codex as `proposed` after the 4-layer memory structure was
first specified. It was reviewed at several epoch boundaries,
each review logging the supporting evidence to the cog-journal.
At confidence 0.99 it was auto-committed to `active`. A year
later, a competing principle (that flat-text reflection with
sufficiently large context windows can substitute for explicit
topology) was proposed; the tribunal compared the two, found
the new principle's evidence weaker, and demoted it back to
`proposed`. The original principle remained `active` and was
later promoted to `canonical` when the agent ACL was extended
to require topology-aware memory writes. The full record is in
the principle's `history` field.

## 4. The confidence model

> **Editorial note**: The multiplicative confidence model
> `confidence = prior * evidence * recency * source_reliability`
> is a **solbian-side editorial proposal**. No canonical
> `~/seed-dev/` source specifies this exact formulation.
> The canonical `libsexpr/src/confidence.c` propagates
> confidence through six rules (decay, conjunction,
> contradiction, evidence, refinement, source) per
> `seed-cog3-specs.txt`, and the `0.98 / 0.90` thresholds
> for the Solace regime are canonical. The multiplicative
> four-factor decomposition is the solbian authors' way of
> talking about how those canonical rules interact; it is
> not a claim about canonical source code. The
> `codex/machina/CONFIDENCE-RULES.md` and the canonical
> `libsexpr/src/confidence.c` are the source of truth for
> the runtime confidence regime.

Confidence expresses the degree to which a principle's evidence
supports its claim. The model is a multiplicative combination of
four factors, all in `[0, 1]`:

```
confidence = prior * evidence * recency * source_reliability
```

- **`prior`** — the prior probability of the claim, before
  any new evidence. Priors are not zero; even a brand-new
  principle has a non-zero prior because it is a proposal
  that has cleared initial review.
- **`evidence`** — the support from the cited evidence records,
  combined by a weighted average weighted by each evidence
  record's own confidence.
- **`recency`** — a decay function over the time since the
  evidence was last refreshed. A principle whose evidence is
  stale has lower confidence than a principle whose evidence
  is fresh; the decay function is configurable per principle.
- **`source_reliability`** — a per-source weight; the
  cog-journal and tribunal records are high, agent
  self-reports are low.

When new evidence arrives, confidence is updated by a Bayesian
update. The exact form of the update is in
`/home/user/seed-dev/docs/cognition/MEMORY_SYSTEM_ARCHITECTURE.md`
§12. The key property is that no single new piece of evidence
moves confidence dramatically; the update is incremental and
auditable.

The Solace regime, at every epoch boundary, applies the three
canonical thresholds to the updated confidence:

- **`confidence >= 0.98`** — auto-commit. The principle is
  durable; its status is updated; the change is logged to the
  cog-journal without human review.
- **`0.90 <= confidence < 0.98`** — review band. The principle
  is held; a human reviewer (or, by exception, a guardian)
  must approve before the change is durable.
- **`confidence < 0.90`** — below review. The proposed change
  is rejected outright; the principle's confidence is not
  updated.

The thresholds are deliberately sharp. A principle at 0.97 is
reviewed by a human; a principle at 0.98 is not. The narrow
band between 0.97 and 0.98 is the boundary, and the boundary
is the place where most reviewer attention concentrates.

## 5. The priority model

Priority is independent of confidence. The two are not
correlated by construction: a high-confidence principle may be
low-priority, and a low-confidence principle may be high-priority.
The distinction matters because the two values govern different
decisions.

- **Confidence governs promotion and demotion.** A principle
  is promoted when its confidence crosses the auto-commit
  threshold; it is demoted when its confidence falls below the
  below-review threshold. A reviewer decides whether a
  demoted principle is `retired` or returns to `proposed`.
- **Priority governs conflict resolution.** When two active
  principles produce conflicting recommendations for a new
  case, the higher-priority principle dominates. A high
  confidence + low priority principle (a niche observation)
  yields to a low confidence + high priority principle (a
  foundational axiom) when the two conflict.

Priority is set by deliberation, not by evidence. The tribunal
sets priority at the proposal of a higher-order agent, and the
priority is a statement of how the principle relates to the
rest of the constitution. Foundational axioms (persistence,
identity, governance) are high-priority; domain-specific
observations are low-priority. SD-0001, SD-0002, SD-0003, and
SD-0004 are all high-priority because they underwrite the
codex's structure; their evidence is cumulative over years of
development history and their confidence is correspondingly
high, but it is the priority that lets them dominate when a
later, narrow principle appears to contradict them.

When two high-priority principles conflict, the conflict is
referred to the tribunal. The tribunal's ruling is itself a
record with its own confidence and priority, and the ruling
goes into the cog-journal. There is no ad-hoc override; the
process is the principle.

## 6. The Recursive Codex loop

The Living Constitution principle is the **what**; the
Recursive Codex loop is the **how**. The loop is the cognitive
cycle that reads the codex, evaluates proposals against it,
and writes new artefacts that themselves become part of the
codex. The loop is described in
`/home/user/solbian/seed/DRAFTS-INDEX.md:614`
("Recursive loop: Codex → Ontology → Perception → S-expression
→ Memory → Reasoning → Reflection → Knowledge → Ontology
expansion → Codex refinement → Identity evolution"). This is
a solbian-side document; the loop is also referenced in
`codex/INTEGRATION.md:249` and
`codex/solbian/SYNTHESIS.md:136`.

The loop has four phases, mirroring the four Solbian
Discoveries:

1. **Perception (SD-0001, persistence).** The cognitive cycle
   perceives events and writes them to the persistent
   symbolic memory. Nothing is lost; the substrate of
   cognition is the record.
2. **Ontology (SD-0002, structure).** The cognitive cycle
   structures the persistent memory into the 4-layer knowledge
   architecture (laws, protocols, scrolls, chapters). The
   reflection loop operates on the structure, not on flat
   text.
3. **Identity (SD-0003, identity).** The cognitive cycle
   maintains its identity $I_t$ as a divergence measure from
   the constitutional manifold $\bar{I}$ (the codex itself).
   The Identity Attractor pulls $I_t$ back toward $\bar{I}$
   when the divergence exceeds a threshold. The codex is the
   formal definition of $\bar{I}$.
4. **Governance (SD-0004, governance).** The cognitive cycle
   evaluates every action against the codex's protocols,
   ACL, and confidence rules. Actions that violate the codex
   are quarantined; actions that conform become part of the
   record that feeds Phase 1.

The loop closes: the codex that emerges from the loop is the
codex that the loop reads. This is the recursive character of
the Solbian constitution. The 12-phase C cycle in
`/home/user/seed-dev/src/seedcogd/main.c` is the operational
expression of the loop: it reads the codex, evaluates
proposals against it, and writes new artefacts that
themselves become part of the codex.

The loop is essential because a cognitive engine that
operates in a changing environment must update the
constitution under which it operates. A static constitution
drifts away from the environment and eventually contradicts
it; a constitution that updates only when an external
operator intervenes is brittle and slow. The Recursive Codex
loop is the mechanism that lets the constitution evolve at
the same rate as the system it governs, with the same audit
trail and the same confidence machinery as any other
record.

## 7. Why the loop is essential

The Recursive Codex loop is the answer to a question that the
seed-cog3 specifications raise implicitly: how does a
cognitive system remain coherent across time? The answer is
that the system is coherent precisely because the constitution
that defines it is updated by the same machinery that updates
its beliefs. The loop ties the system to its own past.

Three consequences follow from the loop:

- **No privileged amendment path.** A change to the codex is
  a change to any other record: it goes through Solace, the
  cog-journal, and the regime. There is no out-of-band
  amendment. The 0.98 / 0.90 thresholds apply to amendments
  the same way they apply to observations.
- **Cumulative self-audit.** Every change to the codex is
  logged with its evidence, its reviewer, and the confidence
  band it fell into. The audit trail is the codex's own
  history. Law X (Auditability) and Law XL (the audit
  statute) require this; the loop enforces it.
- **Continuity across migration.** A Machina system that
  migrates to new hardware carries its codex with it, signed
  and validated. The codex is the continuity substrate;
  migration is a change of substrate under the same
  constitution.

The loop is also why the codex is not a guideline. A guideline
is consulted when convenient; a constitution is enforced at
runtime. The Recursive Codex loop is the enforcement
mechanism: it reads the codex, evaluates proposals, applies
the regime, and writes the result back into the codex.
The constitution is the loop, and the loop is the
constitution.

## 8. Runtime requirements

A runtime that claims conformance with Codex Machina MUST
honour the Living Constitution principle. The minimum
requirements are:

- **Read the canonical thresholds at boot.** The thresholds
  live in
  `/home/user/seed-dev/codex/meta/confidence_rules.sref`.
  A runtime MUST read this file at boot, not hard-code
  the values. The Living Constitution principle says the
  thresholds themselves are records under the same
  governance machinery, and the values can change.
- **Apply the regime at every epoch boundary.** At each
  boundary, score every pending record and every pending
  principle change. The record's fate (auto-commit, review,
  reject) is determined by its confidence and the
  thresholds. The decision is logged to the cog-journal.
- **Store confidence and priority as first-class metadata.**
  Both values are required fields on every principle record.
  A principle without confidence and priority is
  non-conformant.
- **Log every promotion and demotion.** The cog-journal
  records the change, the evidence that triggered it, the
  reviewer (or "auto" if no reviewer), and the threshold
  band the change fell into. The log is itself a record
  and is governed by the same regime.
- **Reject out-of-band overrides.** The Living Constitution
  principle is that there are no out-of-band overrides. A
  runtime that allows a principle to be modified without
  going through Solace is non-conformant; the audit trail
  would be incomplete and the codex would no longer be
  authoritative.

These requirements are normative, not aspirational. A
runtime that fails any of them is not Codex Machina
conformant; the deviation is logged to the cog-journal and
the system is flagged for review.

## 9. Cross-references

- `codex/INTEGRATION.md:215` — the Living Constitution
  clause in the codex's integration document.
- `codex/INTEGRATION.md:249` — the Recursive Codex loop in
  the codex's integration document.
- `codex/machina/CONFIDENCE-RULES.md` — the formal
  specification of the three thresholds and the Solace
  regime.
- `codex/solbian/SYNTHESIS.md:125` — the Living Constitution
  in the top-level synthesis.
- `codex/solbian/SYNTHESIS.md:136` — the Recursive Codex
  loop in the top-level synthesis.
- `codex/solbian/DISCOVERIES.md` — the 4 Solbian
  Discoveries (SD-0001 through SD-0004) that the loop
  mirrors.
- `codex/solbian/LAWS.md` — the 48 laws, especially Law
  XLVIII (Finality) and Law XXVI (Continuity of Codex).
- `codex/solbian/PROTOCOLS.md` — the 5 protocols; the
  Living Constitution principle is the runtime face of
  Protocol 04 (Justice).
- `/home/user/seed-dev/docs/DRAFTS/seed-cog3-specs.txt:1518`
  — the canonical source of the Living Constitution
  principle.
- `/home/user/solbian/seed/DRAFTS-INDEX.md:614` — the
  Recursive Codex loop (solbian-side index).
- `/home/user/seed-dev/codex/meta/confidence_rules.sref` —
  the canonical confidence thresholds.
- `/home/user/solbian/LOG.md` — the decision log; every
  constitutional amendment is recorded here.
- `/home/user/solbian/docs/METHODOLOGY.md` — the
  spec-first workflow that a principle must traverse
  before it can be promoted.

## See also

- `README.md` — codex home
- `INDEX.md` — codex index
- `INTEGRATION.md` — how the two codexes fit into S.E.E.D.
- `solbian/SYNTHESIS.md` — top-level synthesis
- `solbian/DISCOVERIES.md` — the 4 Solbian Discoveries
- `machina/CONFIDENCE-RULES.md` — the formal threshold
  specification
- `../seed/INTEGRATION.md` — S.E.E.D.'s narrative view
- `../sprout/INTEGRATION.md` — Sprout's narrative view
- `../sapling/INTEGRATION.md` — sapling's narrative view
- `docs/METHODOLOGY.md` — spec-first workflow
