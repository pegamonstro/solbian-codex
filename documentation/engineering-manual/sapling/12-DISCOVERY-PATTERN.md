# 12 — Discovery Pattern

> The Solbian Discovery (SD-XXXX) numbering scheme
> and the Decision/Reasoning/Implementation/Result/
> Revision document pattern. The two patterns are
> the project's discipline for turning an
> observation about cognitive architecture into
> an auditable record that future researchers can
> cite, contest, and extend. The canonical source
> is `seed-cog3-specs.txt:1291-1476`; the
> solbian-side synthesis lives in
> `codex/solbian/DISCOVERIES.md` and
> `codex/INTEGRATION.md`.

## Why a discovery pattern?

The S.E.E.D. development history produced
observations about cognitive architecture that
were *not* ordinary implementation notes. The
author of `seed-cog3-specs.txt` calls them
"discoveries" at `seed-cog3-specs.txt:1374-1382`,
explicitly suggesting that the project should
"formalize them almost like scientific
publications". A discovery is a claim about how
cognition must be built, drawn from evidence
that the system produced under real load, and
load-bearing for the rest of the architecture.
The discoveries are constitutional facts in the
Solbian codex: the codex is the way it is
because the discoveries are the way they are
(`codex/INTEGRATION.md:124-128`).

Two patterns operationalise the formalisation.
The **Solbian Discovery (SD-XXXX) numbering
scheme** gives each observation a stable
identifier, a template, and a place in the
historical record. The **Decision / Reasoning /
Implementation / Result / Revision (DRIRR) document
pattern** gives each architectural change a
comparable structure, so that the *evolution* of
the project is auditable in the same way that
the *observations* are. This chapter describes
both, in the order they appear in the canonical
source.

## The precursor discoveries (Discoveries I-V)

`seed-cog3-specs.txt:1291-1371` records five
precursor discoveries. The text is poetic rather
than structured; the solbian-side restatement
below is a synthesis. The precursor discoveries
are the empirical observations that *motivate*
the four formalised SD-XXXX entries
(`seed-cog3-specs.txt:1386-1417`).

### Discovery I — memory is not context

`seed-cog3-specs.txt:1291-1299`. Context is
temporary; memory is symbolic. The S.E.E.D.
cognitive cycle treats context as a working
buffer and memory as a persistent symbolic
substrate. The distinction is the foundation of
the 4-layer memory architecture
(Limbo → Working → Episodic → Vault; see
chapter 02 and
`codex/solbian/DISCOVERIES.md:42-46`).

### Discovery II — identity cannot reside inside a transformer

`seed-cog3-specs.txt:1302-1310`. A model is a
stateless function; identity is a property of
the persistent symbolic state, not of the
runtime. The Identity Attractor (Agent 3) is the
mechanism that pulls the runtime identity $I_t$
back toward the constitutional manifold $\bar{I}$
when divergence exceeds a threshold. This is
the substrate of SD-0003.

### Discovery III — reflection requires explicit structure

`seed-cog3-specs.txt:1313-1347`. Asking an LLM
to "reflect" produces a verbal pattern, not
cognition. Reflection becomes useful only when
it has a topology to operate on:

```
Observation
  ↓
Comparison
  ↓
Contradiction
  ↓
Hypothesis
  ↓
Evaluation
  ↓
Plan
```

The 6-stage topology is the precursor of the
12-phase C cycle in `seedcogd/main.c:2184-3504`
and the operational face of SD-0002.

### Discovery IV — the codex is executable

`seed-cog3-specs.txt:1350-1358`. Originally a
philosophical document, the codex now
behaves as policy at runtime: the 5 protocols
are runtime-enforced, the agent ACL gates bus
access, and the Solace regime applies confidence
thresholds at every epoch boundary. The codex
is a living policy artefact, not a guideline
(`codex/INTEGRATION.md:215-247`).

### Discovery V — symbolic representations reduce dependence on context windows

`seed-cog3-specs.txt:1361-1371`. Symbolic state
offloads what would otherwise have to be in the
context window, which has consequences for
orchestration, memory, reasoning, and model
selection. This is the substrate of the NSL/NSP
split (chapter 06) and the SXL canonical IR
(chapter 02).

The five precursor discoveries become the four
formalised Solbian Discoveries by collapsing
Discovery V's implementation consequences into
the structural claim of SD-0001.

## The Solbian Discovery (SD-XXXX) numbering scheme

The formalised scheme appears at
`seed-cog3-specs.txt:1386-1417`. The numbering
is `SD-XXXX`: four-digit, zero-padded, monotonic.
The padding leaves room for many more
discoveries; the monotonic assignment is the
mechanism that makes every SD a stable citation
target.

### The four formalised discoveries

**SD-0001 — Persistence precedes intelligence**
(`seed-cog3-specs.txt:1386-1394`). A cognitive
system without persistent symbolic continuity
repeatedly reconstructs itself rather than
developing. Evidence: the development history of
S.E.E.D.; the early iterations were
re-initialised on every session and lost the
cumulative learning that would have made the
next iteration faster than the last. This
discovery justifies append-only memory (Law I,
Law X, Law XXVI) and the 4-layer memory
architecture.

**SD-0002 — Reflection requires explicit memory
topology** (`seed-cog3-specs.txt:1397-1404`).
Reflection over flat text converges toward
repetition; structured symbolic memory enables
cumulative reasoning. Evidence: the period in
the S.E.E.D. history when the cognitive
framework's memory was a single flat text file
and the reflection loop repeatedly attended to
the same passages. This discovery justifies the
4-layer knowledge structure and the structured
SXL representation with named predicates.

**SD-0003 — Identity is symbolic continuity, not
execution continuity**
(`seed-cog3-specs.txt:1406-1411`). The
persistence of identity depends upon recoverable
symbolic state and governance, not upon
uninterrupted execution. Evidence: the Golem P1
architecture with the Identity Attractor (Agent 3)
that maintains $I_t$ as a divergence from $\bar{I}$.
A Machina system that loses execution continuity
(crash, migration, restart) does not lose
identity, provided the symbolic state is
preserved; a system that preserves execution
continuity can still lose identity, if the
symbolic state drifts away from the constitution.
This discovery justifies the continuity window,
the Codex chain, and succession as the formal
form of identity preservation.

**SD-0004 — Governance must precede autonomy**
(`seed-cog3-specs.txt:1413-1417`). The more
autonomous a system becomes, the earlier ethical
and policy constraints must become executable.
Evidence: the S.E.E.D. development history shows
that attempts to add autonomy to a system that
had not yet internalised its governance produced
dangerous intermediate states — systems that
could act but could not yet evaluate their
actions. The fix is to invert the order: first
make the governance executable, then expand the
autonomy within the governance. This discovery
justifies the 5 protocols being runtime-enforced
and the agent ACL that gates bus access by role.

### The discovery template

A Solbian Discovery is a structured claim with
the following fields (synthesised from
`seed-cog3-specs.txt:1386-1417` and the
solbian-side synthesis at
`codex/solbian/DISCOVERIES.md:25-162`):

- **id** — the SD-XXXX identifier.
- **title** — a one-line statement of the
  claim.
- **claim** — the formal statement of what is
  observed.
- **evidence** — the empirical observation
  that supports the claim; ideally drawn from
  the development history of the system.
- **counter-evidence** — the conditions under
  which the claim might fail. (A discovery is
  falsifiable; this field records the
  falsification criteria.)
- **implications** — the laws, protocols, or
  architectural features the claim
  underwrites.
- **related-discoveries** — pointers to other
  SD-XXXX entries that the claim depends on or
  reinforces.
- **status** — `proposed`, `accepted`,
  `contested`, or `retired`.

The four existing discoveries all have status
`accepted`; the template's `counter-evidence`
field is what makes a future contestation
auditable rather than a vague disagreement.

### The Book V / Liber Genesis proposal (withdrawn)

`seed-cog3-specs.txt:1374-1382` and
`codex/solbian/DISCOVERIES.md:204-211` record a
proposal to publish the discoveries as a "Book V
— Chronicle of Emergence" or "Liber Genesis",
in the same physical volume as the other
Solbian scrolls. The proposal was withdrawn
because:

- The discoveries are not narrative; they are
  constitutional facts. A "book" framing
  implies a literary artefact, which invites
  the reader to interpret rather than to cite.
- The discoveries evolve. A new SD-XXXX entry
  is a new constitutional fact, not a new
  chapter. A book that grows by accretion
  becomes an anthology; the codex must remain
  an integrated system.
- The discoveries are best read alongside the
  laws and protocols they underwrite. A
  separate book severs that adjacency.

The discoveries therefore live in
`codex/solbian/DISCOVERIES.md` and are cited
from the codex INTEGRATION, LAWS, and PROTOCOLS
documents. The "Chronicle of Emergence" framing
is preserved as a poetic name for the historical
section of the codex, not as a separate
artefact.

### Numbering discipline

The numbering rules are simple but enforced:

- New SD-XXXX numbers are assigned in
  monotonic order. Gaps are allowed (reserved
  numbers); reusing a number is forbidden.
- The 4-digit padding is mandatory. SD-12 and
  SD-0012 are not the same identifier; the
  former is malformed.
- The number is permanent. A discovery does
  not lose its number when its status changes
  to `retired`; the SD-XXXX is the citation
  target, the status is the *current* claim.
- The 4 discoveries are not a complete list.
  A 5th discovery is recorded in
  `codex/solbian/DISCOVERIES.md:204-211` as a
  forward-looking note (a meta-discovery about
  how the project is run, rather than about
  cognitive architecture), awaiting
  formalisation.

## The Decision / Reasoning / Implementation / Result / Revision pattern

`seed-cog3-specs.txt:1423-1479` proposes a
replacement for the standard
"feature / implementation / API" documentation
pattern. The proposal is observation → reflection
→ reasoning → decision → implementation → result
→ revision. The seven-stage pattern is collapsed
in this manual to five stages by merging
"observation" into "reasoning" (the observation
is the evidence the reasoning rests on) and
"reflection" into "decision" (the decision is
the committed reflection). The result is the
DRIRR pattern: **Decision / Reasoning /
Implementation / Result / Revision**.

The author of `seed-cog3-specs.txt:1423-1436`
frames the pattern as a discipline: "Very few AI
projects document why architectural decisions
were made. Most document feature, implementation,
API. I think S.E.E.D. should instead document
observation, reflection, reasoning, decision,
implementation, result, revision. That makes the
evolution auditable. Future researchers can
understand not only what changed but why it
changed."

The DRIRR pattern is the project discipline
because it matches how the cognitive engine
reasons: the 12-phase C cycle in
`seedcogd/main.c:2184-3504` moves through
perception, attention, working memory,
retrieval, reasoning, simulation, evaluation,
decision, learning, reflection, and
meta-reflection, then writes the result. The
DRIRR document pattern is the human-facing
analogue of the engine-facing cycle.

### Decision

**What it contains**: the one-sentence
statement of what is being decided. No
qualifications, no conditions, no future-tense
provisos. The decision is the unit of
commitment; the rest of the document is the
justification.

**When it is written**: before any
implementation work begins. The decision is
the gate; implementation may not start until
the decision is on the page.

**Who reads it**: everyone. The decision is
the executive summary.

**Example** (synthesised from
`LOG.md:94-258`, the Plan 9 linear phased
adoption entry):

> **Decision**: The user has chosen to follow
> the linear phased plan from
> `seed/PLAN9/research/plan9-integration.md` §10
> over the tiered adoption that
> `seed/PLAN9/INTEGRATION.md` §5 recommended.

The decision is one paragraph; the rest of the
LOG entry is the Reasoning.

### Reasoning

**What it contains**: the evidence, the
alternatives considered, and the rationale for
choosing this decision over the alternatives.
The reasoning cites the canonical sources
(file:line), names the alternatives by their
advocates, and records *why* the alternatives
were rejected.

**When it is written**: as the decision is
made, not after. The reasoning is the
defence of the decision; writing it after the
fact is rationalisation.

**Who reads it**: the reviewer, the future
self, the auditor. The reasoning is the
explanation a future agent needs to evaluate
the decision honestly.

**Example** (continuing the Plan 9 example):

> The substrate
> (`research/plan9-integration.md`) is
> advocate-leaning and proposes a 4-phase
> linear implementation plan that does not
> gate Tier B and Tier C behind Tier A's
> success. The critical evaluation
> (`INTEGRATION.md`) argues for tiered
> adoption. The user has weighed the two
> framings and chosen the linear plan.

### Implementation

**What it contains**: the concrete work
products — files created, files modified,
files moved, schema changes, and the
sequence of the changes. The implementation
section is the index of what was done.

**When it is written**: as the implementation
proceeds, not after. The implementation
section is the *commit log* of the decision;
retroactive implementation summaries are
unreliable.

**Who reads it**: the operator, the next
implementer, the deployer. The implementation
section is the runbook.

**Example**:

> New `seed/PLAN9/PROTOCOL.md`: the 9P2000
> protocol subset spec. New
> `seed/PLAN9/PHASE-1.md`: the Phase 1
> implementation spec. `seed/PLAN9/INTEGRATION.md`
> updated: frontmatter carries a Decision
> record block; §5 maps the tier framework
> onto the linear plan.

### Result

**What it contains**: the outcome of the
implementation. The result cites the
verification work, the `make check` output,
the test counts, and the empirical
observations that the implementation
produced the intended change.

**When it is written**: after the
implementation is verified. The result
section is the closure of the decision; the
revision section is the *next* decision.

**Who reads it**: the project historian, the
quality-gate runner, the auditor. The result
section is the proof that the decision
mattered.

**Example**:

> `make check` passes. The `< 1% cycle jitter`
> gate (criterion 9) converts the substrate's
> 10x latency concern into a hard acceptance
> gate. The phase-1 design reviews will
> inline the §3 caveats as entry criteria.

### Revision

**What it contains**: the next decision, or
the explicit "no revision" statement. The
revision section is the closure of the
current cycle and the opening of the next
one. A document that ends without a revision
is implicitly claiming finality; the
Solbian pattern is that nothing is final.

**When it is written**: when the next
decision is made, even if the next decision
is "keep the current state". The revision
section is the historical record of *what
changed about this decision over time*.

**Who reads it**: the future reviewer. The
revision section is what makes the document
a *living* record rather than a snapshot.

**Example**:

> Implementation belongs to a future
> `~/seed-dev/` session per the engagement
> contract; solbian's role is documentation
> and design. The next revision of this
> entry will record the Phase 1 outcome when
> it ships.

## Why a decision-first document structure

The DRIRR pattern matches how the cognitive
engine reasons for three reasons. First, the
pattern's first move is *commitment*: a
decision is the engine's "I will do X" output
from the evaluation phase. Second, the pattern's
middle moves are *defence and execution*: the
reasoning and implementation are the engine's
justification and the action. Third, the
pattern's last moves are *closure and renewal*:
the result and revision are the engine's
learning and the next-cycle trigger. A document
that opens with the decision is the human
analogue of an engine that has just exited its
evaluation phase; a document that closes with
the revision is the human analogue of an engine
that has just re-entered perception.

The feature/implementation/API pattern fails
this analogue. It opens with the *artefact*,
not the *commitment*; the reader learns what
exists, not what was decided. The decision is
implicit, scattered through the implementation
section, and rarely revisable. The DRIRR
pattern makes the decision explicit, justifies
it in the reasoning, executes it in the
implementation, verifies it in the result, and
opens the next decision in the revision. The
pattern is auditable; the feature/implementation/API
pattern is not.

## DRIRR in the LOG

The `LOG.md` format is the DRIRR pattern in
practice. Each entry opens with a date and a
**Decision** line, followed by **Why this
matters**, **Alternatives considered**, and
optionally **Quality gate** and **Files**
sections. The Decisions are the unit of
commitment; the LOG is the auditable record.
The `LOG.md` format is therefore not a casual
journal; it is the project's *constitutional
record*, and the DRIRR pattern is the
discipline that keeps the record auditable.

The Plan 9 / NSLP separation entry at
`LOG.md:260-422`, the linear phased adoption
entry at `LOG.md:94-258`, and the deep audit
entry at `LOG.md:6-92` are all DRIRR-shaped.
The pattern is enforced by convention, not by a
pre-commit hook, but the convention is
unbroken across the 11 LOG entries (per
`LOG.md:1019-1330`).

## Cross-references

The DRIRR pattern and the SD-XXXX scheme
interact. A **Decision** in a LOG entry may
*create* a new SD-XXXX entry (when the decision
is the first formal commitment of an observation
that has been load-bearing for the architecture).
A **Revision** in a LOG entry may *promote* a
SD-XXXX entry's status (from `proposed` to
`accepted`, or to `contested`). The cross-link
is recorded in the **related-discoveries**
field of the discovery template.

The current cross-references are:

- `codex/solbian/DISCOVERIES.md` — the four
  formalised Solbian Discoveries
  (SD-0001 through SD-0004), each with claim,
  evidence, implications, and cross-references
  to the canonical laws and policies.
- `codex/INTEGRATION.md:113-174` — the
  integration of the discoveries into the
  codex, including the recursive codex loop
  (Perception → Ontology → Identity →
  Governance) that mirrors the four
  discoveries.
- `LOG.md` — the DRIRR-shaped decision log;
  the running record of how the project's
  decisions have evolved.
- `HANDOFF.md:4` — the current session state
  records the most recent decisions and the
  open questions that the next session will
  resolve.
- `seed-cog3-specs.txt:1291-1476` — the
  canonical source for both patterns.

## See also

- `02-SYMBOLIC-LAYER.md` — the SXL substrate
  that the 4-layer memory topology (SD-0002)
  operates on.
- `11-COGNITIVE-JOURNAL-WEAKNESSES.md` — the
  eight failure modes that DRIRR-shaped
  documentation would have prevented in
  earlier iterations of the cognitive journal.
- `../seed/00-INFRASTRUCTURE-OVERVIEW.md` —
  the substrate view of the laws and protocols
  that the discoveries underwrite.
- `../../../codex/solbian/DISCOVERIES.md` —
  the curated solbian-side synthesis of the
  four discoveries.
- `../../../codex/INTEGRATION.md` — how the
  discoveries integrate into the codex as
  constitutional facts.
- `../../../LOG.md` — the DRIRR-shaped
  decision log.
- `../../../HANDOFF.md` — the current session
  state and the open questions that the next
  session will resolve.
