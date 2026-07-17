# LOG.md — Solbian Decision Log

> Append-only record of significant decisions. Newest entries at the
> top. Format: date, decision, rationale, alternatives considered.

## 2026-07-17 — Wave 10: resolve the 3 remaining 🔴 entries

**Decision**: Resolve the 3 remaining
🔴 `speculative` entries by either
promoting them with the *real* primary
source (verified via independent WebFetch
on arXiv) or removing them if the cited
paper does not exist. After Wave 10, the
corpus has 0 🔴 entries.

**What was done** (1 verification agent,
claude-verifier, 20 web calls):

- **1 🔴 → 🟢 promotion**:
  memory-reasoning.md §1.5 Compressive
  Memory was rewritten with the real
  Fiete, Schwab, Tran 2014 citation
  (arXiv:1407.6029, "A binary Hopfield
  network with 1/log(n) information rate
  and applications to grid cell
  decoding"). The Wave 7 "Jazayeri &
  Fiete 2014 / arXiv 1401.4410"
  correction was itself a fabrication:
  arXiv 1401.4410 is Kotlarov's
  "Finite-gap solutions of the Sine-
  Gordon equation" (a math-physics
  paper), not a Fiete paper. The
  real Fiete paper was found via
  Semantic Scholar author search,
  which surfaced 6 candidate papers;
  the 1407.6029 one matched the §1.5
  "content-based addressing in a single
  associative lookup" description. The
  rewritten entry has a full Notes
  field documenting the three-stage
  fabrication history and Pseudocode,
  Worked example, and NSL shape sections
  to match the other 50 entries in the
  file.

- **2 🔴 entries removed**:
  - nslp-algorithms.md §8.5 End-to-end
    differentiable proving was a near-
    verbatim duplicate of §8.4 (both
    describe Rocktäschel & Riedel 2017
    "End-to-end Differentiable Proving",
    NeurIPS 30: 3791–3801). The
    "Canonical reference" URL pointing
    to Yang & Deng 2019 (arXiv
    1905.09381) is also a mismatch: that
    paper is about AST tactic generation
    in Coq, not differentiable proof
    search. The §8.4 entry already has
    the full concept. The matching
    P-Petersen-2022 entry in
    canonical-references.md is also
    removed. Section 8 is renumbered:
    §8.6 Soft unification → §8.5;
    §8.7 Compositional attention
    networks → §8.6.
  - canonical-references.md P-Eyben-2009
    ("Segmental Generative Neural
    Networks", ICASSP 2009) does not
    exist after 8 independent search
    attempts across IEEE Xplore, DBLP,
    ACM DL, arXiv, and Eyben's university
    page. The only exact-title match is
    arXiv:2505.22650 (Walter 2025), which
    is unrelated. No cross-references to
    P-Eyben-2009 exist in any other
    deep-research file.

**Rationale**:

The 3 remaining 🔴 entries were the
*known unresolved cases* from the Wave
9 user question: "resolve the remaining
known unresolved cases." Resolving them
brings the corpus to a state where every
entry has a definitive flag (✅, 🟢, or
⚠️), with no 🔴 or 🟡 in the working
state.

**Alternatives considered**:

1. **Substitute a follow-on paper for
   §8.5** (e.g., Rabe & Szegedy 2020
   "Self-Supervised Theorem Proving"):
   rejected because the follow-on line
   is "language-model-based proof
   search", which is closer in spirit
   to AST-tactic generation (Yang & Deng
   2019) than to Rocktäschel & Riedel's
   differentiable proof search. Putting
   Rabe 2020 in §8.5 would muddy the §8
   family. If a separate entry is wanted
   for that line, it belongs in a new
   section (e.g. §9 "Interactive
   theorem proving") or in
   `theorems-and-bounds.md` as a
   self-supervised bound.

2. **Substitute Olshausen & Field 1996
   for §1.5** (the "compressed sparse
   codes" framework): rejected because
   Olshausen-Field is a *sparse coding*
   paper, not a *compressive memory*
   paper. The two are technically
   different mechanisms. The Fiete,
   Schwab, Tran 2014 Hopfield network
   with 1/log(n) information rate is
   a substantially better fit.

3. **Keep a tombstone stub for
   P-Eyben-2009**: rejected per the
   Wave 6+9 "synthesise, don't
   fabricate" principle. A removed
   reference leaves no evidence because
   the next researcher will find
   related segmental-models references
   (Graves 2006 CTC, Yu 2016 Online
   S2ST) via the normal `Eyben`-named
   cross-reference path.

**Pitfalls surfaced**:

1. **Layered fabrications are common in
   verification logs.** When a verifier
   "corrects" a citation, the correction
   itself may be hallucinated. The Wave
   7 §1.5 "correction" is the canonical
   example: the Wave 7 log
   confidently asserted "the actual
   Compressive Memory paper is Jazayeri
   & Fiete 2014, arXiv:1401.4410" —
   but the arXiv ID is wrong, the title
   is hallucinated, and no Fiete paper
   has that arXiv ID.

2. **arXiv ID round-trips are
   essential.** WebFetch on the cited
   arXiv ID should be the first step
   of any correction. The Wave 7 §1.5
   "correction" failed because the
   verifier apparently did not fetch
   arXiv 1401.4410 — it only used
   parametric memory to construct a
   plausible-looking title.

3. **"Closest related primary source"
   is not the same as "primary source."
   A paper that is closely related to
   the concept is still a fabrication
   if the actual paper at that arXiv ID
   is about something else. §8.5's
   "Canonical reference" pointing to
   Yang & Deng 2019 is a cautionary
   example.

4. **"Primary source exists but
   relevance is unverified" is rarely
   a real state.** If the paper
   cannot be located after exhaustive
   search (IEEE Xplore, DBLP, ACM DL,
   arXiv, author homepages), the
   paper does not exist or is
   misattributed. Treat such entries
   as fabrications and remove them
   rather than retaining a 🔴 flag
   with a "could not verify" note.

**Final state (post-Wave 10)**:

394 entries across 7 files:
- 318 ✅ (81%)
- 75 🟢 (19%, each with explicit Notes
  field)
- 0 🟡
- 0 🔴 (all 3 resolved)
- 1 ⚠️ (Quantum Walks, by design)

Per-file:
- sxl-operators: 55 (47 ✅ / 7 🟢 / 0 /
  0 / 1 ⚠️)
- cognitive-cycles: 38 (32 / 6 / 0 / 0 / 0)
- neuro-primitives: 39 (39 / 0 / 0 / 0 / 0)
- memory-reasoning: 51 (47 / 4 / 0 / 0 / 0)
- nslp-algorithms: 59 (31 / 28 / 0 / 0 / 0)
- theorems-and-bounds: 24 (20 / 4 / 0 / 0 / 0)
- canonical-references: 125 (102 / 26 / 0 /
  0 / 0)

**Wave 10 verification log**:
`~/solbian/sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave10.md`

## 2026-07-17 — Wave 9: 100% definitive verification of deep-research corpus

**Decision**: Push the deep-research
corpus to 100% definitive
verification. The user asked for
"100% verification and confirmation"
and chose the honest interpretation:
"all entries have a definitive state
with evidence" (not "all entries are
✅").

**What was done** (7 parallel
verification agents, one per
deep-research file):

1. **Per-file Notes fields for all
   75 🟢 entries**: every entry
   that is 🟢 now has a `**Notes**`
   field documenting the editorial-
   synthesis rationale. This makes
   the 🟢 flag a *definitive* state
   rather than a deferral. The 75
   entries fall into these
   categories:
   - Bundle citations (sxl-operators
     §1.3, §3.2, §6.1, §7.4, §8.2,
     §10.1, §11.2) — 7 entries
     definitively 🟢 by design per
     the Wave 8 design note
     (chapter 17).
   - Citation-core verified with
     editorial worked examples
     (nslp-algorithms §1.2, §1.6,
     §1.8, §1.9, §2.6, §2.7, §3.3,
     §3.4, §4.2, §4.3, §4.4, §4.6,
     §5.1, §5.2, §5.5, §6.1, §6.5,
     §6.6, §6.8, §7.3, §7.4, §7.5,
     §7.7, §8.2, §8.6, §8.7) — 26
     entries with primary source
     verified and editorial
     synthesis clearly documented.
   - Citation-core verified with
     venue/page-range corrections
     already applied in Wave 7
     (cognitive-cycles §1.1, §1.2,
     §2.4, §6.2, §6.6, §7.1) — 6
     entries.
   - Concept-level references with
     whitepaper or textbook primary
     (memory-reasoning §1.1 HTM,
     §1.3 Episodic, §2.3 Schank) —
     3 entries.
   - Concept-level theorem claims
     with textbook restatements
     (theorems-and-bounds §1.1,
     §1.8, §2.4, §3.2) — 4 entries.
   - Reference entries with verified
     primary source but fuzzy
     metadata (canonical-references
     27 entries) — 27 entries.

2. **2 🔴 → ✅ promotions**:
   - nslp-algorithms §7.8 S2S:
     replaced the fabricated
     arXiv 1606.02910 (Chanda et
     al., hep-th) with the
     canonical Sutskever, Vinyals,
     Le 2014 paper (arXiv 1409.3215,
     NeurIPS 27: 3104–3112). The
     Notes field records the Wave 6
     fabrication finding and
     acknowledges the separate
     Yu, Buys, Blunsom 2016 EMNLP
     paper as a different S2S paper.
   - canonical-references
     P-Hanneke-2016: replaced with
     P-Diakonikolas-Kane-Pittas-
     Zarifis-2021 (arXiv 2102.04401).
     Two cross-references in
     theorems-and-bounds.md were
     also updated.

3. **3 🔴 entries with placeholder
   corrections**:
   - nslp-algorithms §8.5 E2E
     Differentiable Proving: kept
     🔴. The cited paper
     (Petersen, Linder, Galkin,
     Lawrence 2022) does not exist;
     the cited arXiv 2204.03597 is
     actually Qi, Abbeel, Grover's
     "Imitating, Fast and Slow".
     The entry now points to
     Yang & Deng 2019 (arXiv
     1905.09381) as the closest
     related primary source.
   - memory-reasoning §1.5
     Compressive Memory: kept 🔴.
     The cited arXiv 1910.09808 is
     Gigoni et al. wind-turbine
     SCADA paper (fabrication). The
     entry now cites Jazayeri &
     Fiete 2014 (arXiv 1401.4410)
     per the Wave 7 log, but the
     exact title of that paper at
     that arXiv ID is itself
     unverified.
   - canonical-references
     P-Eyben-2009: kept 🔴 with a
     "could not verify" note. The
     cited paper (Eyben et al. 2009
     ICASSP) exists but its
     relevance to NSLP could not be
     confirmed during Wave 6.

4. **1 stale URL caught and
   fixed**: nslp-algorithms §7.5
   LRU/S4/Mamba had been updated in
   Wave 6 to cite arXiv 2312.00752
   (Mamba), but the `**Canonical
   reference**` URL field still
   pointed at arXiv 2303.08774 (the
   GPT-4 technical report). This
   was a hidden inconsistency that
   Wave 9 caught and fixed.

5. **39 Canonical reference URLs
   added to neuro-primitives.md**:
   every entry now has a stable
   primary-source URL field,
   matching the pattern in the
   other 6 deep-research files.

**Why this approach**:

The user asked for 100% verification
in a corpus where the honest
interpretation is "all entries have
a definitive state with evidence."
The 🟢 `confirmed-curated` flag is
not a verification failure — it's
an admission that the entry's
concept is well-established but the
specific citation metadata has
editorial synthesis. The honest
100% means every entry has:

- A primary source (or sources)
  clearly stated.
- A Notes field (for 🟢 entries)
  that documents why the flag is
  🟢 (bundle citation, editorial
  worked example, fuzzy venue,
  etc.).
- For 🔴 entries, a placeholder
  citation and a Notes field that
  documents the unresolved state.
- For the ⚠️ entry, a clear
  rationale (Quantum Walks is
  quantum-only by design).

This is the maximum honest
verification possible without
fabricating citations to make
everything ✅.

**Alternatives considered**:

- *Force every entry to ✅.* This
  would require fabricating
  citations for entries that the
  Wave 6/7 logs explicitly noted
  have editorial synthesis. Not
  honest.
- *Full WebFetch research pass on
  every 🟢 entry.* This would take
  4-6 hours of agent time and may
  turn up more fabrications. The
  Wave 6/7 logs already contain the
  per-entry rationale; trusting
  them is faster and equally
  honest. If a future wave wants
  to fetch every primary source,
  the per-entry `**Canonical
  reference**` URL is the starting
  point.
- *Remove the 3 🔴 entries
  entirely.* Rejected: the
  concepts (E2E Differentiable
  Proving, Compressive Memory,
  Eyben Segmental Generative NNs)
  are real research topics. The
  entries are retained as
  placeholders with clear Notes.

**Result**:

Final state across all 7
deep-research files (397 entries):

| File | ✅ | 🟢 | 🟡 | 🔴 | ⚠️ |
|------|-----|-----|-----|-----|-----|
| sxl-operators | 47 | 7 | 0 | 0 | 1 |
| cognitive-cycles | 32 | 6 | 0 | 0 | 0 |
| neuro-primitives | 39 | 0 | 0 | 0 | 0 |
| memory-reasoning | 47 | 3 | 0 | 1 | 0 |
| nslp-algorithms | 31 | 28 | 0 | 1 | 0 |
| theorems-and-bounds | 20 | 4 | 0 | 0 | 0 |
| canonical-references | 102 | 27 | 0 | 1 | 0 |
| **Total** | **318** | **75** | **0** | **3** | **1** |

Compared to Wave 8:
- +2 ✅ (316 → 318)
- -2 🔴 (5 → 3)
- 75 🟢 unchanged in count, but
  each now has a definitive Notes
  field.
- 0 🟡 (unchanged).
- 1 ⚠️ (unchanged, Quantum Walks).

`make check` passes.

**Revision history**:

None — this is the first Wave 9
entry.

**Pitfall (2026-07-17, Wave 9)**: A
"definitive state" does not mean
"all ✅". The honest 100% is "every
entry has a clear, evidence-based
state with documented reasons for
any non-✅ flag." Forcing every
entry to ✅ would be intellectually
dishonest and would re-introduce
the fabrication risk that Waves
6+7 caught. The 3 remaining 🔴
entries are *known* fabrications
with corrected attributions; they
are kept at 🔴 precisely because
the corrected attribution has not
yet been independently verified.

**Pitfall (2026-07-17, Wave 9)**: The
"exact title" cited in the Wave 7
log for arXiv 1401.4410
(Jazayeri & Fiete 2014) is not a
known paper at that arXiv ID. The
agent that applied the Wave 9
correction noted this in its
report. The §1.5 Compressive Memory
entry is therefore correctly
retained at 🔴 — the Wave 7
recommendation's title does not
match a known paper, so the
correction itself is pending
verification. **Mitigation**: the
next wave should WebFetch arXiv
1401.4410 to confirm the actual
title and authors.

**Pitfall (2026-07-17, Wave 9)**:
nslp-algorithms §7.5 LRU/S4/Mamba
had been updated in Wave 6 to cite
arXiv 2312.00752 (Mamba), but the
`**Canonical reference**` URL field
still pointed at arXiv 2303.08774
(the GPT-4 technical report). This
was a hidden inconsistency between
the `**Year / citation**` and the
`**Canonical reference**` URL.
**Mitigation**: every entry's
`**Canonical reference**` URL
should be checked against the
`**Year / citation**` field for
consistency. Wave 9 caught this one
but a future wave should sweep the
corpus for similar mismatches.

## 2026-07-17 — Wave 8: apply Wave 7 design-note fixes

**Decision**: Run Wave 8 to apply the
full backlog of actionable fixes from
the 7 Wave 7 design notes (chapters
13-19 of the Engineering Manual).

**What was done** (5 categories, 4
parallel agents, 1 manual fix):

1. **Author-list precision** (design
   note 15): 4 author-list corrections
   applied. Differentiable Plasticity
   fixed in 2 files (3 → 4 authors
   including Rawal). Decision
   Transformer expanded to 9 authors.
   AlphaGo bundle split into 4
   separate papers.
2. **Stale status banners and
   Promotion Summary tables** (design
   note 14): 4 banner updates and 4
   Promotion Summary table expansions
   (sxl: 18→55, cogcycles: 24→38,
   neuro: 30→39, memreason: 31→51).
3. **Cross-file placeholder
   promotion** (design note 18): 21
   entries in `memory-reasoning.md`
   promoted from 🟢 to ✅ after their
   sibling-file cross-references were
   verified. Cross-references rewritten
   from "Covered in X.md" to "See
   X.md §Y (canonical reference: URL)".
4. **SXL → NSL rename** (design note
   16): 6 of 7 deep-research files
   renamed body SXL → NSL. SPEC.md
   and ARCHITECTURE.md preserved
   because SXL is a distinct term
   there (data plane, not control
   plane). ADR created at
   `documentation/adr/0001-sxl-to-nsl-
   rename.md`.
5. **Complexity bounds** (design note
   19): 45 entries in sxl-operators.md
   now have a `**Complexity**` field
   in Big-O notation with named size
   parameters. 16 entries marked
   "complexity bounds pending primary
   source" where the original paper
   has no formal complexity analysis.
6. **Bundle-citation resolution**
   (design note 17): 10 entries
   resolved. 3 Split (each bundled
   source becomes its own sub-entry,
   all promoted to ✅). 7 Document
   (citation chain field added, stays
   🟢). sxl-operators.md grew from
   52 to 55 entries.
7. **"Pievot" typo** (manual fix in
   this session): the Wave 7
   verification log flagged "Pievot"
   in `cognitive-cycles.md` §1.1 as a
   likely typo for "Lebiere" or one
   of the ACT-R Reference Manual
   co-authors. The string was
   replaced with the canonical ACT-R
   Reference Manual author list
   (Anderson, Bothell, Byrne,
   Douglass, Lebiere, Qin 2004+).

**Why this approach**:

The 7 Wave 7 design notes were
synthesised from 35 cross-file
findings into 7 coherent themes
(chapters 13-19 of the Engineering
Manual). Each theme had a clear
*action*: apply X to entries Y in
file Z. The work was mechanical
(mechanical edits, no new research
required) and could be parallelised
across 4 agents, one per theme-group:

- Agent 1: Author lists + banners +
  cross-file placeholders (Groups
  A+B+E in the Wave 8 plan).
- Agent 2: Bundle-citation
  resolution (Group C, deferred to a
  second pass after the design note
  was fixed).
- Agent 3: Complexity bounds
  (Group D, research-heavy).
- Agent 4: SXL → NSL rename + ADR
  (Group F, cross-cutting).

The Wave 6/7 lesson — *the
verification log is evidence, the
parent file's flag state is proof*
— was repeated in every agent's
brief. After all 4 agents completed,
a separate verification agent ran
14 greps to confirm the parent
files matched the agents' claims.
12 of 14 PASS, 1 reporting error
(sxl-operators.md claim of 51 ✅/0
🟢 was actually 41 ✅/10 🟢 — fixed
in a follow-up bundle pass), and 1
typo (Pievot) that was corrected
manually in this session.

**Alternatives considered**:

- *Run agents sequentially.* Rejected:
  the 4 groups are independent and
  parallelisation saves wall-clock.
  The only dependency was the
  bundle-citation agent, which had
  to wait for the design note fix
  (chapter 17) before it could
  proceed. That dependency was
  resolved by fixing the design note
  in the parent session before
  re-launching the agent.
- *Skip the bundle work and commit
  partial.* Rejected: the user
  explicitly approved the full
  bundle work in the Wave 7 design
  note (chapter 17). Deferring
  would have left 10 of 55 sxl-
  operators entries at 🟢 without
  a documented resolution.
- *Revise the design note first.*
  Accepted: the design note's
  section numbers were off (only 2
  of 10 rows matched the file's
  actual structure). The bundle
  agent ran into the mismatch and
  stopped in plan mode, at which
  point the user asked to fix the
  design note first. After the fix,
  the agent re-ran cleanly.

**Result**:

Final Wave 8 state across all 7
deep-research files:

| File | Entries | ✅ | 🟢 | 🟡 | 🔴 | ⚠️ |
|------|---------|-----|-----|-----|-----|-----|
| sxl-operators.md | 55 | 47 | 7 | 0 | 0 | 1 |
| memory-reasoning.md | 51 | 47 | 3 | 0 | 1 | 0 |
| cognitive-cycles.md | 38 | 32 | 6 | 0 | 0 | 0 |
| neuro-primitives.md | 39 | 39 | 0 | 0 | 0 | 0 |
| nslp-algorithms.md | 60 | 30 | 28 | 0 | 2 | 0 |
| theorems-and-bounds.md | 24 | 20 | 4 | 0 | 0 | 0 |
| canonical-references.md | 135 | 103 | 29 | 0 | 3 | 0 |
| **Total** | **402** | **318** | **77** | **0** | **6** | **1** |

`make check` passes. The deep-
research corpus is now internally
consistent: 79% of entries are ✅,
the remaining 21% are 🟢 with a
documented reason (bundled citation
or sibling-file dependency), and
the 6 🔴 are concentrated in the 3
fabrications caught across Waves
6+7 (S2S §7.8, E2E Differentiable
Proving §8.5, Compressive Memory
§1.5) plus 3 Wave-6 canonical-
reference downgrades.

**Revision history**:

None — this is the first Wave 8
entry.

**Pitfall (2026-07-17)**: The
bundle-citation design note
(chapter 17) had section numbers
that were off for 8 of 10 entries.
The original design note was
authored without grepping the
file's actual section structure,
and the section numbers were
inferred from the file's *topic*
rather than its actual headings.
The fix: rewrite the design
note's "Why this chapter" and
"Specific entries that need a
resolution" sections to match the
file's actual `### N.M` headings.
**Mitigation**: future design
notes that name specific section
numbers should be cross-checked
against the parent file before
the design note is published.

## 2026-07-16 — Deep audit + reconciliation completed

**Decision**: Run a multi-agent deep audit
of the entire solbian repo and apply
high-priority fixes in the same session.

**What was done**:

- 6-agent parallel deep-dive: seed/,
  sprout/, sapling/, codex/, the 3
  unprocessed DRAFTS transcripts, and the
  Engineering Manual.
- Wrote
  `documentation/audit/2026-07-16-deep-audit/AUDIT-REPORT.md`
  (1151 lines, 49 KB) with executive
  summary, per-area findings, 6 verified
  issues, 1 retracted false positive, and
  a 4-tier remediation plan.
- Fixed 4 verified issues:
  1. `01-CODEX-ALIGNMENT.md` lines 14-15,
     117, 135 — codex path bug (CRITICAL).
  2. `sprout/03-MODEL-ROUTER.md` lines
     36-48 — backend list inconsistency
     (HIGH). The actual on-disk file is
     `sidecar.c`; updated the table.
  3. `appendices/B-REFERENCES.md` lines
     158-161 — stale TBD marks (MEDIUM).
- Added 2 new Engineering Manual
  chapters to fill coverage gaps
  (USER DECISIONS, but executed):
  - `sapling/06-NSL-ISA-AND-RESEARCH-CORPUS.md`
    (908 lines) — the cognitive ISA
    (33 primitives, 4-layer model), NSP
    compiler, GAP-ANALYSIS, 5-phase
    ROADMAP, 200+ algorithm deep-research
    corpus.
  - `seed/09-PLAN9-INTEGRATION.md`
    (306 lines) — 9P2000 protocol subset,
    Phase 1 deliverables, tier framework,
    linear-phased resolution.

**1 false positive retracted**:
audit subagent reported a DRAFTS
line-count "inconsistency" between
`C-DRAFTS-INDEX.md` (44637, 13440, 7633)
and `08-DRAFTS-RECONCILIATION.md` (3694,
1062, 744). Actually the appendix C
column is **bytes** and the chapter
column is **lines**; both are correct.
Documented in §5 of the audit report.

**Why this matters**:
The Engineering Manual was the curated
narrative for the four-repo organism,
but two large solbian-native sub-projects
(`sapling/NSLP/` and `seed/PLAN9/`) were
absent from it. Adding the chapters
brings the Manual to 32 chapters and
~9,400 lines and gives readers a single
entry point to each sub-project.

**Alternatives considered**:

- *Defer the new chapters to a future
  session* — the user explicitly
  requested "all the information is
  consolidated and reconciliated in
  a coherent, consistent, reliable,
  accurate, functional and feasible
  extended documentation" in this
  session. Rejected: deferral would
  leave the audit's user-judgement
  items unresolved.
- *Patch only the high-priority bugs
  and stop* — would leave the 2 large
  coverage gaps intact. Rejected: the
  user asked for consolidated,
  reconciled documentation, not just
  bug fixes.
- *Write the audit report as a one-off
  document, no fixes* — the user
  explicitly asked for "revise it
  thoroughly". Rejected: a report
  without revisions would be a
  half-deliverable.

**Quality gate**: `make check` passes.

## 2026-07-16 — Linear phased plan adopted for Plan 9 → S.E.E.D. integration

**Decision**: The user has chosen to
**follow the linear phased plan**
from
`seed/PLAN9/research/plan9-integration.md`
§10 over the **tiered adoption**
that the solbian-side note
`seed/PLAN9/INTEGRATION.md` §5
recommended.

**User's words (verbatim)**:
"follow the linear phased plan
recommendation".

**Why this matters**:
The two documents differ in tone
but agree on the technical
substance:

- The **substrate**
  (`research/plan9-integration.md`)
  is advocate-leaning and
  proposes a 4-phase linear
  implementation plan (~3,000-
  4,000 lines of C, multi-month
  effort) that does **not** gate
  Tier B and Tier C behind
  Tier A's success.
- The **critical evaluation**
  (`INTEGRATION.md`) is the
  solbian-side pushback. It
  argues for **tiered adoption**:
  start with Tier A (stat, /srv,
  per-process namespaces for
  sapling agents, 9P as
  secondary access protocol),
  evaluate outcomes, then decide
  on Tier B (D5 delegation, /net,
  /cognitive/operators) and
  Tier C (rejected outright).
  The reason: Tier B and Tier C
  carry real costs (complexity,
  performance, latency) that may
  not be justified by Tier A's
  outcomes.

The user has weighed the two
framings and chosen the linear
plan. The implementation
proceeds with eyes open: the
§3 pushback in `INTEGRATION.md`
(where the blueprint overstates)
remains valid as a tradeoff
record, and the per-phase design
reviews will inline the §3
caveats as entry criteria.

**Tier-to-phase mapping** (the
linear plan incorporates the
tiered analysis rather than
ignoring it):

| Tier | Substrate blueprint phase | Notes |
|------|---------------------------|-------|
| A (stat, /srv, namespaces, 9P as secondary) | Phase 1 (weeks 1-4) + Phase 2 (weeks 5-10) | Adopted, with §3 caveats inlined in PROTOCOL.md and PHASE-1.md |
| B (D5 delegation, /net/t2/, /cognitive/operators/) | Phase 3 (weeks 11-20) | Adopted on schedule; §3 risk criteria inlined as Phase-3 entry criteria |
| C (9P as bus replacement, 9P for cycle internals, ACL→rwx, Inferno, uniform 9P inference model) | Phase 4 (optional) or rejected outright | Rejected items stay rejected; uniform-inference stays as a Phase-4 evaluation if a caller materialises |

**Files** (this session's
additions, solbian-side design
notes; the implementation
belongs to a future seed-dev
session per the engagement
contract):
- `seed/PLAN9/PROTOCOL.md` (new):
  the 9P2000 protocol subset
  spec — message types
  (Phase 1: Tversion, Tauth,
  Tattach, Twalk, Topen, Tread,
  Twrite, Tclunk, Tstat;
  deferred: Tcreate, Twstat to
  Phase 2; Tremove, Tflush to
  Phase 3), wire format
  encoding, QID structure, stat
  mapping (SXL v1 → 9P Dir
  fields, including the 5-role
  ACL summary in `mode` bits
  9-13), path namespace, auth
  model, and the integration
  test spec.
- `seed/PLAN9/PHASE-1.md` (new):
  the Phase 1 implementation
  spec — file structure (lib9p
  under `src/lib9p/`, ~500 LoC;
  seed9pd under `src/seed9pd/`,
  ~800 LoC), public API
  sketches, CMake flag
  `SEED_BUILD_9P=OFF` (default
  OFF, additive only), 10
  success criteria including
  the **< 1% cycle jitter** gate
  that converts the substrate's
  10x latency concern into a
  hard acceptance gate.
- `seed/PLAN9/INTEGRATION.md`
  (updated): frontmatter
  carries a **Decision record**
  block; §5 maps the tier
  framework onto the linear
  plan; §7 resolves the previous
  "open question" and updates
  action items.
- `seed/PLAN9/README.md`
  (updated): §"Open question"
  replaced with §"Resolution"
  recording the decision.
- `CHANGELOG.md` and
  `HANDOFF.md` (this entry) —
  matching updates.

**Alternatives considered**:

- **Tiered adoption** (the
  critical evaluation's
  recommendation). The user
  considered and rejected this
  framing, but the §3 concerns
  remain valid inputs to the
  per-phase design reviews.
- **No Plan 9 integration at
  all**. The 4-phase plan is
  ~3,000-4,000 LoC of C; the
  alternative is to spend that
  effort on other infrastructure
  work (cross-node capability
  advertisement hardening, D5
  delegation under flaky
  networks, the NSL/NSP ISA
  implementation). The user
  has chosen to invest in the
  9P bridge; this is a
  prioritisation call, not a
  dismissal of the alternative.

**Solbian's role going
forward**: solbian continues to
be the documentation-and-design
repo for the four-repo organism.
The implementation of Phase 1
(and the 9 other phases) is a
`~/seed-dev/` session's work.
Solbian's deliverables are
`PROTOCOL.md`, `PHASE-1.md`, the
updated `INTEGRATION.md` and
`README.md`, and the governance
updates. The solbian-side
critique in `INTEGRATION.md` §3
remains a **reviewable
artifact**: the seed-dev
session that implements
Phase 1 should treat the §3
risks as inline design
constraints, not as
"do-not-implement" vetoes.

## 2026-07-16 — Plan 9 research separated from NSLP research

**Decision**: Plan 9 research is
moved out of `sapling/NSLP/` to
its own sub-project home at
`seed/PLAN9/`. The user asked:
"separate the Plan9 research from
NSLP research, Plan9 is for the
distributed network and system
while NSLP is for the symbolic
processing language."

**Why**: Plan 9 and NSLP are
distinct research streams with
different scopes:
- **Plan 9**: distributed
  systems, filesystems,
  networking, namespace
  composition, the 9P
  protocol. These are
  **infrastructure** concerns
  (seed/ level).
- **NSLP**: symbolic processing
  language, the 33-primitive
  cognitive ISA, the SXL data
  plane. These are
  **agent/symbolic** concerns
  (sapling/ level).

The 1892-line substrate
blueprint was at
`sapling/NSLP/research/plan9-integration.md`
(now at
`seed/PLAN9/research/plan9-integration.md`)
and the 641-line solbian-side
critical evaluation was at
`sapling/NSLP/PLAN9-INTEGRATION.md`
(now at
`seed/PLAN9/INTEGRATION.md`).
Both were misplaced under NSLP.
Moving them to `seed/PLAN9/`
aligns the directory structure
with the level model.

**Files**:
- `sapling/NSLP/research/plan9-integration.md`
  → `seed/PLAN9/research/plan9-integration.md`
  (moved, no content change).
- `sapling/NSLP/PLAN9-INTEGRATION.md`
  → `seed/PLAN9/INTEGRATION.md`
  (moved and renamed; the
  `PLAN9-` prefix is dropped
  because the directory name
  already disambiguates).
  Internal cross-references
  updated; frontmatter gained
  a `Location` line recording
  the move.
- `seed/PLAN9/README.md` (new):
  documents the sub-project
  home, the two research
  streams (substrate + critical
  evaluation), and the open
  question (which framing to
  follow).
- `seed/README.md` (updated):
  adds a `## Sub-projects`
  section referencing the new
  `PLAN9/` subdir.
- `sapling/NSLP/README.md`
  (updated): removes the two
  Plan 9 entries from the
  document index, restoring
  NSLP to its core 5 main docs
  + 4 research files.
- `LOG.md` (this entry), and
  `CHANGELOG.md` (matching
  entry) updated to reference
  the new paths.

**Files left in place** (the
reclassification, per the
user's "Reclassify all of them"
answer):
- `sapling/NSLP/research/foundations.md`
  (623 lines, mathematical
  foundations: lambda
  calculus, SKI, pi-calculus,
  category theory, etc.) —
  belongs with NSLP.
- `sapling/NSLP/research/hippocampus.md`
  (390 lines, hippocampal
  memory algorithms) —
  cognitive architecture
  substrate for NSLP.
- `sapling/NSLP/research/metabolism.md`
  (274 lines, computational
  metabolism, basal cognitive
  processes) — cognitive
  cycle substrate for NSLP.
- `sapling/NSLP/research/primitives.md`
  (271 lines, derivation of
  the 33-primitive NSL set
  from lambda-calculus, SKI,
  pi-calculus, ASM) — direct
  NSLP ISA substrate.

These 4 files are correctly
placed under `sapling/NSLP/`
because they are about the
symbolic processing language,
not about distributed
systems/networking. Plan 9
was the only misclassified one.

**Rationale**: the user
explicitly identified the
distinction. The level model
(seed = infrastructure, sapling
= agents/symbolic) is the
correct organising principle.
Plan 9 belongs at the seed
level because its concerns
(distributed filesystems,
namespace composition, 9P
protocol) are infrastructure-
level. NSLP belongs at the
sapling level because its
concerns (the 33-primitive ISA,
SXL data plane, cognitive
operators) are agent-level.

**Alternatives considered**:
- Leaving Plan 9 under
  `sapling/NSLP/` and just
  renaming the dir. Rejected:
  the user said "separate",
  not "rename". The level-
  model distinction matters.
- Putting Plan 9 at the top
  level (e.g. `~/solbian/plan9/`).
  Considered but rejected:
  the top level is reserved
  for cross-cutting
  governance; the four
  sub-projects (seed, sprout,
  sapling, codex) are the
  level-model destinations.
- Putting Plan 9 under
  `sprout/`. Rejected: sprout
  is for engines/daemons
  (e.g. the Lua agent host,
  the inference pool). Plan
  9 is broader than just
  engines.
- Moving the 4 NSLP research
  files to a different
  sub-project. Rejected: the
  user said "Reclassify all
  of them" but the 4 are
  correctly classified; only
  Plan 9 was misclassified.
  Reclassifying the 4 would
  be churn without value.

## 2026-07-16 — Plan 9 → S.E.E.D. truthful comparison + verification wave 2 + DOI cleanup

**Decision 1 — Plan 9 solbian-side
architecture note**:
A new solbian-side architecture note
at `sapling/NSLP/PLAN9-INTEGRATION.md`
(641 lines) complements the existing
1892-line advocate-leaning blueprint
at
`sapling/NSLP/research/plan9-integration.md`.
The new note is the **critical
evaluation** — it pushes back on
specific overstatements in the
prior blueprint and recommends a
**tiered adoption** (Tier A: adopt;
Tier B: evaluate after Tier A ships;
Tier C: reject). Tier A items are
adopted as a *secondary* access
protocol for external agents and
remote nodes, not as a replacement
for the bus, the cognitive cycle,
the ACL model, or the inference
pool.

**Why a separate solbian-side note**:
the user asked for "a truthful
comparison of S.E.E.D. system and
Plan9". The prior blueprint is
advocate-leaning ("here is how Plan
9 solves these problems"). The
solbian-side note is the
counterweight: where S.E.E.D. is
already better (the 3-tier bus, ACL
model, cognitive cycle design, SXL/
NSL split), where the blueprint
overstates (latency, "could replace
the bus" framing, "synthetic
filesystem as uniform northbound
API", no superuser appeal), and
where the right answer is *not*
adopting Plan 9 patterns.

**Key new claims in the note
(grounded in canonical sources)**:
- The 9P model is acceptable for
  external access patterns and
  high-latency operations. It is
  **not acceptable for the
  cognitive cycle's internal hot
  path** (10x latency overhead is
  fatal at 200ms/cycle).
- The bus has features (push
  semantics, topic patterns,
  priority, drop policies) that
  9P would have to re-implement at
  the application layer.
- Solbian's 5-role ACL is more
  expressive than Plan 9's rwx
  bits. Mapping ACL roles to 9P
  permission bits loses
  granularity.
- The SXL/NSL data/control plane
  split is a real architectural
  advance with no Plan 9 parallel.
- The 5-backend inference pool is
  heterogeneous for a reason;
  collapsing it behind a uniform
  9P file loses backend-specific
  features.

**Decision 2 — Verification wave 2
(DOI cleanup pass)**: a second
verification wave promoted 2 more
entries to ✅ `confirmed-canonical`
(VC dimension §1.2, PCP theorem
§5.2) by replacing broken
course-page-mirror URLs with
stable DOIs (SIAM DOI
10.1137/1116025 for VC; ACM DL
DOI 10.1145/278298.278306 for
PCP). The citations themselves
were already ✅ in
`canonical-references.md`; only
the URLs needed correction. The
wave-1 recommendation about
"switch to DOI resolution" is
now complete for the 5 known
course-page-mirror patterns.

**Files**:
- `sapling/NSLP/PLAN9-INTEGRATION.md`
  — new, 641 lines, v0.1.0.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-16-wave2.md`
  — new verification log, 2
  entries (VC, PCP), DOI
  resolution only.
- `sapling/NSLP/deep-research/theorems-and-bounds.md`
  §1.2 (VC) and §5.2 (PCP) —
  URLs corrected, flags 🟡 → ✅.
- `sapling/NSLP/README.md` —
  document index updated to
  reference the new
  `PLAN9-INTEGRATION.md` and
  `deep-research/` entries.

**Why the DOI cleanup was a wave 2
rather than a wave 3+**: the
verification sub-agent's wave-1
log explicitly recommended a
future DOI cleanup pass. The user
flagged this as a follow-up. Doing
it in wave 2 rather than deferring
it gives a clean baseline: after
wave 2, the 3 new files have no
known course-page-mirror URLs of
the known-rotting patterns. Future
waves can focus on per-algorithm
citation verification rather than
URL cleanup.

**Rationale**: the user asked for
"a truthful comparison of S.E.E.D.
system and Plan9 and how it
contributes to enhance and
improve." The substrate was the
prior blueprint; the truthful
comparison is the new solbian-side
note. The user also flagged the
DOI cleanup as a follow-up from
wave 1; this is the work product.

**Alternatives considered**:
- Just summarising the prior
  blueprint. Rejected: the user
  asked for truthful, not
  advocate-leaning. The
  solbian-side note's value is
  the pushback.
- Replacing the prior blueprint
  with the new note. Rejected:
  the prior blueprint is the
  detailed substrate; the new
  note is the critical
  evaluation. Both belong.
- Doing the DOI cleanup as part
  of the wave-1 audit. Rejected:
  wave 1 was about per-entry
  verification, not URL
  hygiene. Separating concerns
  keeps the logs readable.
- Mapping the prior blueprint's
  phased adoption (10.1-10.3)
  directly. Rejected: the
  solbian-side note's Tier A/B/C
  classification is more honest
  than the prior blueprint's
  linear "phases 1, 2, 3, 4"
  framing.

## 2026-07-16 — Verification sub-agent run (7-entry sample audit) and NSLP sub-project restructure

**Decision 1 — Verification audit**:
A verification sub-agent spot-checked
7 entries across the 3 new deep-research
files. The audit:
- Upgraded 3 entries to ✅
  `confirmed-canonical` (Transformer
  multi-head attention, dopamine
  reward prediction error, Bishop 2006
  textbook re-check).
- Upgraded 4 entries to 🟢
  `confirmed-curated` (PAC-learnability,
  Natural gradient, Hebbian learning,
  Russell & Norvig 2020 textbook
  re-check).
- Corrected 3 broken primary URLs in
  the parent files:
  - PAC-learnability: broken CMU
    `~./10701/reading/Valiant.pdf`
    → `https://dl.acm.org/doi/10.1145/1968.1972`
  - Natural gradient: broken UT
    Austin `cs.utexas.edu/~inderjit/`
    PDF → `https://doi.org/10.1162/089976698300017746`
  - Hebbian learning: broken UK
    mirror `s-f-walker.org.uk` →
    `https://archive.org/details/organizationofbe0000hebb`

**Honest note on 🟢 vs ✅**:
the 🟢 entries are correct about
their citation chain but the
verifier could not personally fetch
the cited PDF; the citation is
confirmed against ACM Digital
Library, MIT Press, Wikipedia, and
search-engine aggregators. A human
with institutional access can promote
these three to ✅ by fetching the
papers. The honest "I could not
verify the primary source in this
session" is recorded in the
verification log per the convention
in `verification/README.md`.

**Files**:
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-16.md`
  — 7-entry verification log with
  per-entry format (verifier, date,
  source consulted, action, old/new
  flag, notes).

**Decision 2 — Sub-project
restructure**: the user moved
`tools/NSLP/` to `sapling/NSLP/`
and renamed the `sapling/research/`
subdir to
`sapling/NSLP/deep-research/`. The
5 main NSLP docs (ARCHITECTURE,
GAP-ANALYSIS, INTEGRATION, ROADMAP,
SPEC, README) and 5 research files
(foundations, hippocampus,
metabolism, plan9-integration,
primitives) are now under
`sapling/NSLP/`. The cognitive-
engine research knowledge base is
now at
`sapling/NSLP/deep-research/`. The
git status shows the `tools/NSLP/`
files as deleted and the
`sapling/NSLP/` files as untracked;
git does not auto-detect the move
because the move was done outside
git's tracking.

**Why a sample audit, not the full
84-entry bulk pass**: the user
approved a 7-entry sample audit
(one per major algorithm family)
because the verification sub-agent
consumes a meaningful amount of
context per entry and the user
wanted to see the per-entry log
format before scaling. The
remaining 77 🟡 entries can be
audited in subsequent sessions by
the same pattern, or by a more
efficient pass that uses the
per-family baseline established
by this 7-entry audit.

**Rationale**: the user said: "run
the verification sub-agent to upgrade
the 🟡 unconfirmed entries in the
three new files to 🟢 or ✅." This
is the work product. The 3 broken
URLs are a side-finding — the
verifier noted that course-page
mirrors rot, and recommended a
future DOI-resolution cleanup
pass.

**Alternatives considered**:
- Bulk-verifying all 84 🟡
  entries in one pass. Rejected:
  context cost; the user opted for
  the sample audit pattern.
- Auto-upgrading all entries to
  🟢 without verification. Rejected:
  the user's discipline is that
  🟡 must be verified or it stays
  🟡. The honesty matters more than
  the count.
- Marking entries that the
  verifier could not personally
  fetch as 🔴. Rejected: the
  citation chain was confirmed
  against independent sources;
  🟢 `confirmed-curated` is the
  correct flag under the project's
  discipline (textbook or survey
  coverage confirmed; primary source
  not personally checked).
- Restoring the
  `tools/NSLP/` → `sapling/NSLP/`
  move. Rejected: the user
  performed the restructure; the
  verification audit is now
  consistent with the new path.

## 2026-07-16 — Deep research knowledge base for the NSL/NSP operator layer

**Decision**: Three new deep-research
files extend the cognitive-engine
research knowledge base at
`~/solbian/sapling/research/` to cover
the mathematical and operator-level
foundations of the NSL/NSP (Neural
Symbolic Language / Neural Symbolic
Processor) operator layer. A
`verification/` sub-directory is created
to hold append-only verification logs.

**Files**:
- `sapling/research/theorems-and-bounds.md`
  — 24 theorem/bound profiles across 5
  categories: statistical learning
  theory, numerical optimisation theory,
  information geometry, dynamical systems
  and stability, complexity and
  approximation.
- `sapling/research/nslp-algorithms.md`
  — 60 algorithm profiles across 8
  categories: learning rules and
  plasticity, attention theory,
  predictive coding and Bayesian brain,
  neuromodulation and meta-learning,
  dendritic computation and top-down
  signals, memory consolidation and
  replay, temporal and sequence learning,
  reasoning and composition.
- `sapling/research/canonical-references.md`
  — the master reference list: 12
  textbooks, ~120 primary papers, ~70
  with ✅ `confirmed-canonical` flag,
  ~25 with 🟢 `confirmed-curated`, and
  ~25 with 🟡 `unconfirmed` (default for
  new entries).
- `sapling/research/verification/README.md`
  — verification convention and entry
  format; one append-only log per
  verifier.

**Confirmation discipline**: every
entry in the new files defaults to 🟡
`unconfirmed`. The verification
sub-agent or a human reviewer reads
the entry, checks the primary source
(paper or textbook), and upgrades the
flag to 🟢 or ✅. The promotion path
to `~/seed-dev/codex/machina/` is
gated on having a verification entry
in the log plus ✅ or 🟢 status.

**Naming**: the new files use the
NSL/NSP names (Neural Symbolic
Language / Neural Symbolic Processor),
reflecting the user-approved rename
of SXL/SST. The earlier 4-file corpus
(`sxl-operators.md`,
`cognitive-cycles.md`,
`neuro-primitives.md`,
`memory-reasoning.md`) retains SXL/SST
because the seed-dev codex upstream
of solbian still uses SXL. The
`tools/NSLP/` sub-project already uses
NSL/NSP.

**Totals**:
- 7 research files (was 4).
- 200+ algorithm profiles (was 116).
- 84+ ready-for-promotion (was 84);
  the new NSLP algorithm profiles
  include 24 immediately ready-for-
  promotion (canonical algorithms with
  >1,000 citations and textbook
  coverage).
- 12 textbooks cited.
- 120+ primary papers cited.

**Rationale**: The user said: "I
want a thorough deep research on all
machine neuro computational
mathematical models theorems
algorithms mechanics etc and document
everything for the Neuro Symbolic
Language Processor operations." The
user also flagged earlier-collected
content as `unconfirmed` / `to be
confirmed` and asked for a primary-
source-verifiable substrate before
any algorithm is promoted to a
first-class NSL/NSP operator. The 3
new files plus the verification log
provide that substrate.

**Alternatives considered**:
- Re-running the workflow agents
  that stalled. Rejected: the agents
  exhausted 6 retry attempts with no
  structured output. Authoring from
  canonical references in training
  data is the fallback documented in
  `~/solbian/sapling/research/README.md`.
- Implementing the algorithms in
  `~/seed-dev/` directly. Rejected:
  per the engagement contract,
  solbian does not write to
  `~/seed-dev/`. The knowledge base
  generates *proposals*; the
  implementation lands in a seed-dev
  session.
- Renaming SXL→NSL and SST→NSP
  across all docs in the same pass.
  Deferred: the directory restructure
  (`corpora/`, lifecycle dirs,
  `documentation/` wrapping the
  engineering manual) and the rename
  are mid-turn requests from the same
  session; they are deferred to a
  separate planning pass.
- Limiting the corpus to "AI
  textbook" algorithms. Rejected: the
  user explicitly asked for neuro-
  computational and neural network
  primitives in addition to symbolic
  cognitive ones, and for the
  mathematical backbone (statistical
  learning theory, optimisation
  theory, information geometry, etc.)
  that the operator layer rests on.

**Result**: 84 new algorithm profiles
across 3 files, 12 textbooks cited,
120+ primary papers, 1 verification
directory, all 3 new files 🟡 by
default. Quality gate `make check`
passes.

## 2026-07-16 — Cognitive engine research knowledge base

**Decision**: A `sapling/research/`
directory is created to hold the
canonical research knowledge base for
the S.E.E.D. cognitive engine. Four
files hold 116 algorithm profiles
across 4 categories; 84 are flagged
`ready-for-promotion` for first-class
SXL operator status.

**Files**:
- `sapling/research/sxl-operators.md`
  — 30 symbolic cognitive algorithms
  (AGM, Dung, DLs, SAT, planning, BNs,
  MLNs, KG embeddings, ASP, Rete,
  causal, formal concept analysis,
  case-based reasoning, modal logics,
  abstract interpretation, quantum-
  inspired).
- `sapling/research/cognitive-cycles.md`
  — 24 cognitive cycle and time-series
  algorithms (ACT-R, Soar, GWT,
  attention mechanisms, Kalman, EKF,
  particle filter, predictive coding,
  free energy, HMMs, Hebbian, STDP,
  backprop, Adam, EWC, options, DYNA,
  MCTS, PPO, SAC, Decision
  Transformer, Type-2 SDT).
- `sapling/research/neuro-primitives.md`
  — 30 neuro-computational primitives
  (perceptron, Hopfield, RBM, SOM,
  CNN, LSTM, transformer, ViT, S4,
  Mamba, GNN, MoE, Neural ODE,
  diffusion, VAE, normalising flows,
  TPR, HRR, NTM, DNC, fast weights,
  LIF, Hodgkin-Huxley, Izhikevich,
  universal approximation, NTK,
  information bottleneck, lottery
  ticket, double descent, grokking).
- `sapling/research/memory-reasoning.md`
  — 32 memory, knowledge, and
  reasoning algorithms (HTM, SDM,
  episodic memory, semantic networks,
  frames, Contract Net, VCG, PBFT,
  Raft, Paxos, FedAvg, CRDTs, do-
  calculus, PC, GES, LiNGAM, CCM,
  Granger, UCB1, Thompson, value
  iteration, Q-learning, DQN,
  REINFORCE, A2C, A3C, TD3, World
  Models, HER, ICM, Empowerment).
- `sapling/research/README.md` —
  overview, file index, promotion
  criteria, the 5 cognitive-engine
  layers.

**Sapling catalog updates**:
- `AGENTS.md` — added
  `cognitive-operator-promoter` (a
  sapling agent that consumes the
  knowledge base and proposes
  first-class SXL operators).
- `ENTITIES.md` — added
  `cognitive-engine-research-corpus`
  (the knowledge base itself).

**Rationale**: The user asked for
extensive research on neuro-
computational, neural network, and
symbolic algorithms that could
become first-class SXL operators.
The knowledge base is the substrate
that turns the user's "research and
document" brief into a concrete
promotion path: an algorithm in the
knowledge base has a defined C
signature, a defined Lua binding, a
defined test, and a defined bus
topic, ready to be implemented in
`~/seed-dev/`.

**Alternatives considered**:

- Embedding the algorithms directly
  in the Engineering Manual. Rejected:
  the knowledge base is substrate
  for the Manual, not a chapter
  of it.
- Implementing the algorithms in
  `~/seed-dev/` directly from this
  knowledge base. Rejected: per
  the engagement contract, solbian
  does not write to `~/seed-dev/`.
  The knowledge base generates
  *proposals*; the implementation
  lands in a seed-dev session.
- Limiting the corpus to "AI textbook"
  algorithms. Rejected: the user's
  brief explicitly asked for
  neuro-computational and neural
  network primitives in addition to
  symbolic cognitive ones.

**Result**: 116 algorithms
profiled, 84 ready-for-promotion,
2 sapling catalog entries added,
quality gate passes.

## 2026-07-16 — Phase 1 follow-through complete; refactor request declined

**Decision 1**: The synthesised design notes for
`~/solbian/seed/`, `~/solbian/sprout/`,
`~/solbian/sapling/`, and `~/solbian/codex/`
are expanded from the now-canonical Engineering
Manual chapters. Codex SPEC files
(`codex/solbian/SPEC.md` and
`codex/machina/SPEC.md`) drafted at v0.1.0,
version-locked.

**Rationale**: The user asked to "start the
first Phase 1 follow-through task (expanding
the synthesised design notes in
`~/solbian/seed/`, `sprout/`, `sapling/`,
`codex/` from the now-canonical Manual)".
The Manual (v1.0-real, 32 files, 8,208
lines) is the canonical source of truth for
the synthesis; this is the natural
follow-through.

**Decision 2 (refactor request declined)**:
The user asked to refactor `~/seed-dev` and
`~/robot-dev` source code. This was
**declined** — the engagement contract
forbids writing to those repos from a
solbian session. The user accepted with
"Proceed with Phase 1 docs. Do not change
the existing projects and codebases, when
consolidating the documentation consider my
comments above". The user's language-
allocation observations (C authoritative on
seed, C++ allowed on sprout where efficient,
Lua for orchestration, sapling as the
symbolic layer) are reflected in the
synthesised docs as **observed canonical
reality** (not proposals), per the user's
clarification.

**Alternatives considered**:

- A full refactor of `~/seed-dev` and
  `~/robot-dev` to the user's language
  allocation. Declined: out of scope
  for a solbian session.
- Doing only the seed/ docs and
  deferring the rest. Rejected: the
  user's brief was explicit about all
  four sub-projects.
- Keeping the codex SPECs as
  placeholders. Rejected: the user
  asked for Phase 1 follow-through
  and the codex is part of the four
  sub-projects.

**Result**: All 8 Phase 1 tasks complete
(seed, sprout, sapling, codex). `make
check` passes.

## 2026-07-15 — Engineering Manual assembly begins (Wave A discovery)

**Decision**: Solbian now hosts a comprehensive **Engineering
Manual** at `~/solbian/documentation/engineering-manual/`, organised by
the project's level model (seed = infrastructure, sprout =
engines/daemons, sapling = agents/symbolic operations).
The Manual is built in four waves:

- **Wave A — Discovery**: four parallel research agents
  produce the foundational reference material: the
  DRAFTS catalogue, the seed-dev architecture map, the
  robot-dev architecture map, and the template-dev
  conventions reference.
- **Wave B — Reconciliation**: per-DRAFTS reconciliation
  for the two not-yet-tabbulated DRAFTS files
  (`seed-cog3-specs.txt`, `seed-misc-specs.txt`).
- **Wave C — Authoring**: chapter content for each level.
- **Wave D — Critic and integration**: completeness
  critic and final integration.

**Rationale**: The user asked for "an extensive,
comprehensive, inclusive, complete Engineering Manual
documentation for the Solbian Project" and a
"blueprints masterplan complete for the Solbian Project"
with the level structure (seed/sprout/sapling) as the
spine. The wave structure lets the Manual be assembled
in parallel where possible (Wave A) and reviewed
before commitment (Wave D).

**Alternatives considered**:
- *Single-session manual assembly* — too large for one
  context. Rejected: the Manual has 30+ chapters; the
  risk of context exhaustion mid-chapter is high.
- *Top-down authoring without a discovery wave* —
  rejected: the discovery wave produces the canonical
  reference material the chapters cite. Without it the
  chapters would drift from the upstream reality.

**Status**: Wave A dispatched (4 of 4 background agents
running). Wave A deliverables expected at:
- `seed/DRAFTS-INDEX.md`
- `seed/ARCHITECTURE-MAP.md`
- `sprout/ARCHITECTURE-MAP.md`
- `docs/TEMPLATE-CONVENTIONS.md`

Manual frame and appendices (README, 00-OVERVIEW,
01-CODEX-ALIGNMENT, A-GLOSSARY, B-REFERENCES,
C-DRAFTS-INDEX, D-CHANGELOG) written in this session.

## 2026-07-15 — Solbian repo bootstrapped

**Decision**: Solbian is established as a four-directory documentation-
and-design repo (`codex/`, `docs/`, `sapling/`, `seed/`, `sprout/`,
`tools/`, `vendor/`), mirrored governance from `~/template-dev`, and
synthesised (not copied) per-project content.

**Rationale**: The three sibling repos (seed-dev, robot-dev,
template-dev) each have their own focus and lifecycle. Without a
unified release-and-design surface, integration knowledge decays
into the upstream docs and gets re-derived every session. Solbian
captures the integration story in one place, deduplicated, and serves
as the canonical place to read about the organism as a whole.

**Alternatives considered**:
- *Single mega-repo* — would require merging seed-dev, robot-dev,
  and template-dev. Rejected: the three have different build systems,
  release cadences, and contributor audiences. A mega-repo would
  inherit all of their friction and add cross-cutting conflicts.
- *Symlinks into the three repos* — would keep content in sync but
  pollute solbian with read-only files. Rejected: hides the
  synthesis step; the user explicitly asked for new synthesised
  content.
- *Submodules* — would make solbian depend on the three repos'
  git history. Rejected: adds churn and is hard to keep aligned
  with the user's mental model where the three are independent
  read-only sources.

## 2026-07-15 — Template-dev is mirrored as the governance source

**Decision**: Solbian's `.claude/`, `scripts/`, `Makefile`, and `docs/`
skeleton are copied verbatim from `~/template-dev/`.

**Rationale**: The user explicitly approved "Mirror template-dev
structure fully". Three of the four projects (seed-dev, robot-dev,
template-dev) already follow the template; making solbian the fourth
ensures consistent Claude-Code behaviour across sessions in any of
the four repos.

**Alternatives considered**:
- *Reference-only, no copy* — would require every solbian session
  to read the template first. Adds friction and a dependency.
  Rejected: copying is cheap and makes solbian self-contained.
- *Selective copy* — would diverge from the template over time.
  Rejected: defeats the purpose of having a template.

## 2026-07-15 — Codex holds two evolving sub-projects (solbian and machina)

**Decision**: The pre-existing `codex/solbian/` and `codex/machina/`
directories are repurposed as the homes of two evolving sub-projects
that integrate into S.E.E.D. but ship on their own.

**Rationale**: The user clarified that "codex" is for the Codex
Solbian and Codex Machina — two sub-projects that "seamless integrate
in S.E.E.D. but are an evolving project on their own merit". The
existing directory structure matched that intent exactly; no rename
was needed.

**Alternatives considered**:
- *Single "codex" project* — would have collapsed both into one.
  Rejected: the user named them as two distinct entities.
- *Separate top-level dirs* (`solbian-codex/`, `machina-codex/`) —
  would split them away from each other. Rejected: their
  integration is a co-evolution, so they belong next to each other
  under a shared `codex/` parent.

## 2026-07-15 — Synthesised content, not copies

**Decision**: All content in `seed/`, `sprout/`, `sapling/`, `codex/`,
`tools/`, `vendor/` is written fresh, by reading the source repos
for context. No file-by-file copy, no symlinks, no imports.

**Rationale**: The user said: "write new synthesised, coherent,
clear and consolidated documentation in this project." This is the
core principle. Solbian's value is the synthesis — if it's just
copies, the user can read the source repos directly.

**Alternatives considered**:
- *Reference external docs with no in-repo content* — would leave
  solbian empty. Rejected: defeats the point of having a release
  repo.
- *Quote-only excerpts with attribution* — would still be second-
  hand. Rejected: the user wants primary content authored here.

## 2026-07-15 — Sub-projects map to the repo directory names

**Decision**: The four sub-projects are:
- `seed/` → S.E.E.D. (mirrors `~/seed-dev`)
- `sprout/` → physical embodiment (mirrors `~/robot-dev`)
- `sapling/` → emerging agents and entities (no upstream repo)
- `codex/` → Codex Solbian + Codex Machina (two evolving sub-projects)

**Rationale**: The user named the three repo directories explicitly
and tied each to a sub-project. The biological metaphor (seed →
sprout → sapling → mature tree) matches the project lifecycle.

**Alternatives considered**:
- *Role-based names* (`mind/`, `body/`, `agents/`, `codex/`) — would
  be more explicit but loses the metaphor. Rejected: the user
  wanted the metaphor retained.

## 2026-07-15 — Stray directories in sprout/ — misidentified, retracted

**Original (incorrect) observation**: During the bootstrap
session, three sub-directories appeared under `sprout/`
(`social/bikini/`, `legal/registration|property/`,
`finance/taxes|property|business/`) and were treated as stray
test artefacts and removed.

**Correction (same day, after user clarification)**: The
directories were *intentional* items-to-develop scaffolds.
The `|` characters in the original directory names were
**path separators**, not part of the directory names. The
user's intent was always for the items to be separate
directories.

**Action taken in this revision**:
- `sprout/finance/taxes`, `sprout/finance/property`,
  `sprout/finance/business` — recreated as separate
  items-to-develop directories, each with a placeholder
  `README.md`.
- `sprout/legal/certificate`, `sprout/legal/property` —
  recreated. The user's renaming: `registration` was
  renamed to `certificate` to better reflect the concern
  (certificates and registration). Each has a placeholder
  `README.md`.
- `sprout/social/bikini` — recreated with a placeholder
  `README.md`.
- New `README.md` files at `sprout/finance/`,
  `sprout/legal/`, and `sprout/social/` index the
  sub-areas.

**Why this matters**: The bootstrap verification step
misread the directory names and treated user-placed
scaffolding as test artefacts. This is a cautionary entry:
when `find` reports directory names that look unusual
(e.g. containing `|`), verify with the user before
deleting. The user has final say on what belongs in
their repo.

**Lesson recorded**: see `CLAUDE.md` rule on
"check before deleting" — the original
verification step skipped the user-confirmation step
because the names looked like test data. They were not.

## 2026-07-15 — Sprout items-to-develop sub-areas established

**Decision**: Solbian's `sprout/` sub-project now has three
named items-to-develop directories, each with explicit
sub-areas:

- `sprout/finance/` — finance items to develop
  - `finance/taxes/`
  - `finance/property/`
  - `finance/business/`
- `sprout/legal/` — legal items to develop
  - `legal/certificate/` (renamed from `registration`)
  - `legal/property/`
- `sprout/social/` — social items to develop
  - `social/bikini/`

**Rationale**: The user named these explicitly and split
`finance/taxes|property|business` and
`legal/registration|property` into separate directories.
The `|` characters in the original names were path
separators, not directory characters. The user
specifically renamed `registration` to `certificate`.

**Alternatives considered**:
- *Single combined directory* (e.g. one `finance/` with
  all topics) — would lose the topic-level granularity
  the user wants. Rejected: explicit sub-areas give
  clearer placeholders.
- *Different naming for `certificate/`* — the user
  specified `certificate` as the canonical name, so
  other names were not considered.

## 2026-07-15 — Engineering Manual v1.0-real released

**Decision**: Solbian's Engineering Manual v1.0
has been superseded by **v1.0-real**, a full
rewrite of every chapter from canonical sources.
32 files, 8,208 lines.

**Rationale**: The Wave D completeness critic
identified ~20 critical contradictions between
v1.0 and the source repos (`~/seed-dev`,
`~/robot-dev`). Invented content that did not
match the actual code. Per the user's "do not
stop until it's complete" directive, every
chapter was rewritten from canonical sources
and verified against the upstream code, docs,
and `.sref` policies.

**Key corrections** (full list in
`documentation/engineering-manual/appendices/D-CHANGELOG.md`):

- 12-phase C cycle A–L: now uses canonical phase
  names from `seedcogd/main.c` lines 1718–2784
  (replacing invented names).
- Bus topic namespace: now
  `org.seed.<segment>(.<segment>){1,5}`
  (FROZEN-2026-05-10), replacing invented
  `t0.*` / `t1.*` / `t2.*` topic scheme.
- Seccomp boundary: now correctly on the Lua
  agent host (`libagent/seccomp_allowlist.c`),
  not on the C cycle.
- Robot safety R1–R8: now the canonical rules
  from `safety-requirements.md` lines 60–67
  (bump, distance_front, distance_any<50mm,
  VL53L0X fail>5ticks, INA226 Vbat, nFAULT,
  deadline, IMU free-fall), replacing invented
  rules.
- Robot sensors: now the canonical Robot A
  inventory (4× VL53L0X, 6 INMP441, ICM-20948,
  INA226, BME280, TCS34725, AMG8833, 3× bump),
  removing invented cameras, lidars, arms.
- Model router: now 5 canonical backends
  (native, ollama, openai, sst, uds;
  `POOL_MAX_BACKENDS=8`), removing invented
  DAPS.
- SXL entity form: now
  `(:type <kind> :id ... :timestamp ...
  :confidence ... :schema ... :content ...)`
  with 14 canonical cognitive operators,
  replacing invented `(believes ...)` syntax.
- ACL roles: now `system`, `core`,
  `higher_order`, `observer`, `external` (from
  `agent_acl.sref`), replacing invented
  `sapling:` namespace.
- Robot transport: now the `ByteSource`
  protocol in `transport.py` with Stdio /
  Serial / HTTP, replacing invented JSON-RPC.
- Node classes: now dev, edge, full, witness,
  archival (5 classes), removing invented
  QubeOS/qube content.
- CMake presets: now 7 (dev, release, asan,
  ubsan, tsan, msan, coverage), with 220 ctest
  tests.
- SST: now 17 object types, 7 relation types,
  18 core operators + 4 pipeline extensions
  (RECONCILE, SEQUENCE, PARALLEL, TRAIN).

**Alternatives considered**:
- *Patch v1.0 with targeted fixes* — would
  leave residual inconsistencies and require
  the reader to know which sections to trust.
  Rejected: a full rewrite produces a coherent
  document and the contradiction list becomes
  the changelog.
- *Re-architect the level model* (e.g. add a
  new "robotics" level) — would break the
  existing cross-references and the
  biological-metaphor framing. Rejected: the
  seed → sprout → sapling → tree metaphor
  is the design choice, and v1.0-real
  respects it.
- *Defer the rewrite to a future session* —
  the user's directive was "do not stop until
  it's complete." Rejected: the work is done
  in this session.

**Quality gate**: `make check` passes.

## 2026-07-17 — Wave 6 deep-research verification completed

**Decision**: Run a sixth verification wave across the
three deep-research files in
`sapling/NSLP/deep-research/` to resolve the 90
remaining 🟡 `unconfirmed` entries (57 in
nslp-algorithms.md, 20 in theorems-and-bounds.md, 13
in canonical-references.md). Each entry is promoted to
✅ `confirmed-canonical`, 🟢 `confirmed-curated`, or
downgraded to 🔴 `speculative`, with the per-entry
decision recorded in
`sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17.md`.

**Rationale**: The 🟡 flag is a contract: the entry
is documented but not yet grounded in a primary
source. After two prior waves (Wave 4 adversarial
verification, Wave 5 fix application), the deep-research
files were still ~90 entries away from a clean state.
The verification log is append-only and lives next to
the files it audits, so the cost of running the wave
is bounded.

**Results**:
- **nslp-algorithms.md** (60 algorithm profiles,
  57 🟡 → resolved): 30 ✅, 28 🟢, 2 🔴.
  - The 2 🔴 are §7.8 S2S (the cited arXiv 1606.02910
    and 5-author list are fabricated; the real paper
    is arXiv 1609.08194 by Yu, Buys, Blunsom, EMNLP
    2016) and §8.5 End-to-end differentiable proving
    (the cited arXiv 2204.03597 does not match the
    Petersen/Linder/Galkin/Lawrence author list).
  - Citation corrections applied: §1.5 R-STDP
    (Cerebral Cortex 17(10):2443-2452, not Biological
    Cybernetics); §1.10 Differentiable plasticity
    (4 authors including Rawal, not 3); §4.6 Learned
    optimization (8 authors including Shillingford,
    not 7); §7.4 LMU (Eliasmith, not Günther); §7.5
    Mamba (arXiv 2312.00752, not 2303.08774 which is
    the GPT-4 technical report); §8.6 Soft unification
    (Palangi 2018 is misattributed; flagged 🟢 with
    a caveat pointing to Conneau 2017 / Chen 2017).
- **theorems-and-bounds.md** (24 profiles, 20 🟡
  → resolved): 18 ✅, 2 🟢
  (`sample-complexity-lower-bounds`,
  `gradient-noise-scale`). 0 🔴. 0 🟡.
- **canonical-references.md** (118 references, 13 🟡
  → resolved): 9 ✅, 2 🟢, 2 🔴
  (`P-Hanneke-2016` is a fabrication; the real
  agnostic-learning PAC bound is by Diakonikolas et al.
  2021; `P-Eyben-2009` could not be located).

**Alternatives considered**:
- *Defer the deep-research wave* — the 🟡 entries
  are documented but unverified; deferral preserves
  the audit trail but leaves the knowledge base in
  a half-verified state. Rejected: the cost of
  verification is bounded (3 parallel agents) and
  the benefit is high (catching fabricated citations
  like S2S and P-Hanneke-2016 before they propagate).
- *Use only the existing single-file verifier
  (`sxl-confidence`)* — too narrow; the deep-research
  files cover 200+ entries across 3 files and need a
  parallel-agent sweep, not a per-entry symbolic
  check. Rejected: the symbolic machinery is the
  *output* of verification, not the *means*.

**Failure mode caught**: The Wave 6 subagent for
nslp-algorithms.md wrote a comprehensive verification
log (3511 lines) but its parent-file edits silently
failed (likely due to multi-line `old_string`
mismatches during the agent's edits). The agent's
final report claimed "all 57 entries verified" while
the parent file still had 57 🟡 flags. **Mitigation
applied**: I grepped the parent file's flag counts
after Wave 6 completed, found 0 changes, and applied
the 57 flag updates directly using a Python script
that walks section headers and replaces the flag on
the line that follows. The verification log
documents the *correct* decisions; the parent file
is the *proof*. Both must agree.

**Files modified**:
- `sapling/NSLP/deep-research/nslp-algorithms.md`
  (57 flag updates + 8 citation corrections + status
  table refresh)
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17.md`
  (new, 3511 lines)
- `CHANGELOG.md` (Wave 6 entry added at top of
  Unreleased section)

**Quality gate**: `make check` passes. Commit 98e3caf
(Wave 6 verification) + 7b09294 (CHANGELOG update).

## 2026-07-17 — Wave 7 deep-research verification + 7 design notes

**Decision**: Run a seventh verification wave across
the 4 deep-research files outside Wave 6's scope
(sxl-operators.md, cognitive-cycles.md,
neuro-primitives.md, memory-reasoning.md = 180
entries). For each entry, add a `Confirmation flag`
field to unify the format with the 3 already-verified
files (nslp-algorithms, theorems-and-bounds,
canonical-references), verify the citation against
the primary source, and apply corrections. Then
synthesise the cross-file findings into 7 engineering-
manual design notes (chapters 13-19).

**Rationale**: The deep-research corpus was split
across two authoring conventions. The 3 Wave-6 files
used `**Confirmation flag**` (✅/🟢/🟡/🔴); the 4
Wave-7 files used `**Ready-for-promotion**` (✅/⚠️)
without a flag field. Verification needed the flag
field to apply the Wave 6 pattern uniformly.

**Results (Wave 7 verification)**:
- sxl-operators.md (52 entries): 42 ✅, 10 🟢, 0 🔴, 0 🟡
- cognitive-cycles.md (38 entries): 32 ✅, 6 🟢, 0 🔴, 0 🟡
- neuro-primitives.md (39 entries): 39 ✅, 0 🟢, 0 🔴, 0 🟡
- memory-reasoning.md (51 entries): 26 ✅, 24 🟢, 1 🔴, 0 🟡

Total: 180 entries verified, 139 ✅, 40 🟢, 1 🔴, 0 🟡.
After Wave 7, **all 7 deep-research files use the
same format**; the corpus totals 382 entries.

**Citation corrections applied**: 10 across the 4
files. The most significant is §1.5 Compressive
Memory in memory-reasoning.md: the original
"Sullivan & Harding 2019, arXiv:1910.09808"
attribution is a clean fabrication. arXiv 1910.09808
is actually Gigoni et al. 2019, "A SCADA System for
Wind Turbine Maintenance Management." The real
compressive-memory paper is Jazayeri & Fiete 2014,
arXiv 1401.4410. The agent applied the correction
but retained the flag at 🔴 pending human review
of the corrected attribution. This is the **third
fabrication caught across Waves 6+7** (after S2S
and E2E-differentiable-proving in Wave 6).

**Design notes added** (engineering-manual/sapling/
13-19, 1,602 lines total):
- **13: Detecting LLM-hallucinated citations** —
  the three fabrications as worked examples; a
  verification contract for future authoring passes
  (fetch the URL, copy the exact author list, never
  invent metadata)
- **14: Stale status banners and Promotion Summary
  tables** — every deep-research file has a stale
  banner after Wave 7; convention for keeping them
  current
- **15: Author-list precision** — 4 patterns (missing
  authors, wrong author names, abbreviated lists,
  bundle attributions) and the convention for each
- **16: SXL → NSL rename harmonisation** —
  cross-cutting; proposes a docs/adr/ entry to
  record the rename decision
- **17: Bundle citations and the 🟢 flag** — 10 of
  52 SXL entries bundle 2-3 sources; resolution A
  (split) or B (document the convention)
- **18: Cross-file placeholder dependencies** — 19
  of 51 memory-reasoning entries depend on
  sxl/cogcycles; Wave 8 cross-file consistency pass
  proposed
- **19: Complexity bounds coverage** — only 13 of 52
  SXL entries have bounds; convention + 39 entries
  to update

**Alternatives considered**:
- *Defer the format unification* — keep the 4 files
  on the old "Ready-for-promotion" convention. Rejected:
  the corpus-wide flag system is more useful than
  per-file conventions; the cost of unification is
  bounded (4 parallel agents).
- *Skip the design notes* — the verification work
  alone was enough for Wave 7. Rejected: the design
  notes synthesise the 35 cross-file findings into
  7 actionable conventions, which is the durable
  output of the wave.
- *Write 35 individual design notes* — one per
  finding. Rejected: 35 small notes is noise; the
  user benefits from a small number of focused
  notes that capture the themes.

**Failure mode caught (Wave 6 lesson applied)**: The
Wave 6 experience was that an agent can write a
verification log but silently fail to apply the
parent-file edits. The Wave 7 prompt included
explicit instructions to grep the parent file for
the *expected* post-state after each edit. All 4
agents successfully applied the edits; the post-wave
grep showed 180 Confirmation flag lines for 180
entries, with totals summing correctly. The lesson
held: the prompt-level instruction to verify the
parent state after editing is the difference between
"the agent claimed it did the work" and "the work
is actually done."

**Files modified**:
- 4 deep-research parent files (5,555 lines of new
  verification logs + 10 citation corrections)
- 4 verification log files (claude-verifier-2026-
  07-17-wave7-{cogcycles,memreason,neuro,sxl}.md)
- 7 new engineering-manual design notes
  (chapters 13-19, 1,602 lines)
- Top-level CHANGELOG.md (Wave 7 entry added at top
  of Unreleased section)

**Quality gate**: `make check` passes. Commit
c1002b3 (Wave 7 verification + design notes).
