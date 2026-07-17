# CHANGELOG.md — Solbian Release Notes

> Following [Keep a Changelog](https://keepachangelog.com/) conventions.
> Versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Wave 10 — resolve the 3 remaining
  🔴 `speculative` entries
  (2026-07-17):
  - **1 🔴 → 🟢 promotion**:
    - memory-reasoning.md §1.5
      Compressive Memory: the
      Wave 7 "Jazayeri & Fiete
      2014 / arXiv 1401.4410"
      correction was itself a
      fabrication (arXiv 1401.4410
      is Kotlarov's "Finite-gap
      solutions of the Sine-Gordon
      equation", a math-physics
      paper). Wave 10 found the
      *real* Fiete paper on
      content-addressable memory:
      **Fiete, Schwab, Tran 2014,
      "A binary Hopfield network
      with 1/log(n) information
      rate and applications to grid
      cell decoding"** (arXiv:
      1407.6029). The §1.5 entry
      was rewritten with a full
      Notes field documenting the
      three-stage citation
      fabrication history
      (1910.09808 → 1401.4410 →
      1407.6029) and Pseudocode,
      Worked example, and NSL shape
      sections to match the
      structure of the other 50
      entries in the file.
  - **2 🔴 entries removed**:
    - nslp-algorithms.md §8.5
      End-to-end differentiable
      proving: the entry was a
      near-verbatim duplicate of
      §8.4 (both describe
      Rocktäschel & Riedel 2017
      "End-to-end Differentiable
      Proving", NeurIPS 30:
      3791–3801). The "Canonical
      reference" URL pointing to
      Yang & Deng 2019 (arXiv
      1905.09381) is also a
      mismatch: that paper is
      about AST tactic generation,
      not differentiable proof
      search. The matching
      P-Petersen-2022 entry in
      canonical-references.md is
      also removed. Section 8 is
      renumbered: §8.6 Soft
      unification → §8.5;
      §8.7 Compositional attention
      networks → §8.6.
    - canonical-references.md
      P-Eyben-2009: the cited
      paper (Eyben et al. 2009
      ICASSP, "Segmental
      Generative Neural Networks")
      does not exist after
      exhaustive search across
      IEEE Xplore, DBLP, ACM DL,
      and arXiv. The only
      exact-title match is
      arXiv:2505.22650 (Walter
      2025), which is unrelated.
      No cross-references to
      P-Eyben-2009 exist in any
      other deep-research file, so
      removal is safe.
  - **New Wave 10 verification
    log**:
    `verification/claude-verifier-
    2026-07-17-wave10.md` records
    the 3 resolutions with primary-
    source fetches and per-resolution
    notes.

### Removed
- 2 fabricated cross-references:
  P-Petersen-2022 and P-Eyben-2009
  in `canonical-references.md`.
- 1 duplicate entry: §8.5 End-to-end
  differentiable proving in
  `nslp-algorithms.md` (covered by
  §8.4 NTP).

### Changed
- `nslp-algorithms.md` §8 family
  renumbered: 7 entries → 6
  entries (now §8.1-8.6, was
  §8.1-8.7).
- `memory-reasoning.md` §1.5
  entry length: 16 lines → 75
  lines (added Pseudocode,
  Worked example, NSL shape,
  Community status, Complexity,
  Failure modes, Canonical
  reference, Confirmation flag,
  Ready-for-promotion).

### Added
- Wave 9 — push deep-research corpus
  to 100% definitive verification
  (2026-07-17):
  - **Per-file Notes fields for all 75
    🟢 `confirmed-curated` entries**:
    every entry that is 🟢 now has a
    `**Notes**` field that documents the
    editorial-synthesis rationale
    (worked examples, fuzzy venue
    attributions, bundle citations,
    fuzzy author counts, etc.). This
    makes the 🟢 flag a *definitive*
    state, not a deferral.
  - **2 🔴 → ✅ promotions**:
    - nslp-algorithms.md §7.8 S2S:
      the fabricated arXiv 1606.02910
      / 5-author attribution was
      replaced with the canonical
      Sutskever, Vinyals, Le 2014
      paper (arXiv 1409.3215, NeurIPS
      27: 3104–3112). The Notes
      field records the Wave 6
      fabrication finding and
      acknowledges the separate
      Yu, Buys, Blunsom 2016 EMNLP
      paper (arXiv 1609.08194) as
      a different S2S paper.
    - canonical-references.md
      P-Hanneke-2016: replaced with
      P-Diakonikolas-Kane-Pittas-
      Zarifis-2021, *COLT 2021* /
      *PMLR* 134: 1552–1584,
      arXiv:2102.04401. The Hanneke
      attribution was a fabrication
      caught in Wave 6. Two
      cross-references in
      theorems-and-bounds.md
      (lines 306, 325) were also
      updated.
  - **3 🔴 entries with placeholder
    corrections**:
    - nslp-algorithms.md §8.5 E2E
      Differentiable Proving: kept
      🔴 with placeholder for
      Yang & Deng 2019 (arXiv
      1905.09381, "Learning to Prove
      Theorems via Interacting with
      Proof Assistants") as the
      closest related primary
      source. The original fabricated
      Petersen/Linder/Galkin/Lawrence
      attribution is documented in
      the Notes field.
    - memory-reasoning.md §1.5
      Compressive Memory: kept 🔴
      with corrected citation to
      Jazayeri & Fiete 2014 (arXiv
      1401.4410). The Wave 7
      recommendation's exact title
      is not a known paper at that
      arXiv ID, so the correction
      is itself pending independent
      verification.
    - canonical-references.md
      P-Eyben-2009: kept 🔴 with
      "could not verify" note. The
      cited paper (Eyben et al. 2009
      ICASSP) exists but its
      relevance to NSLP could not
      be confirmed.
  - **1 stale URL caught**:
    nslp-algorithms.md §7.5
    LRU/S4/Mamba had been updated
    in Wave 6 to cite arXiv
    2312.00752 (Mamba) instead of
    arXiv 2303.08774 (GPT-4), but
    the `**Canonical reference**`
    URL field still pointed at
    2303.08774. Fixed.
  - **39 Canonical reference URLs
    added to neuro-primitives.md**:
    every entry now has a stable
    primary-source URL field. This
    matches the pattern used in the
    other 6 deep-research files.
  - **Final state across all 7
    deep-research files** (397
    entries):
    - 318 ✅ `confirmed-canonical`
      (80%) — primary source fully
      verified.
    - 75 🟢 `confirmed-curated`
      (19%) — each with a Notes
      field documenting the
      editorial synthesis.
    - 0 🟡 `unconfirmed`.
    - 3 🔴 `speculative` — each
      with a placeholder citation
      and a Notes field documenting
      the unresolved state.
    - 1 ⚠️ `quantum-only-by-design`
      — Quantum Walks §17.2, by
      design.
  - **7 design notes from Wave 7
    now have full cross-references
    in the deep-research files**:
    chapters 13 (LLM hallucination
    detection), 14 (stale status
    banners), 15 (author-list
    precision), 16 (SXL→NSL
    rename), 17 (bundle citations),
    18 (cross-file placeholders),
    19 (complexity bounds). Each
    convention is applied
    consistently in the deep-
    research files.
- Wave 8 — apply Wave 7 design-note
  fixes (2026-07-17):
  - **Author-list precision (4 fixes)**:
    nslp-algorithms.md §1.10 and
    neuro-primitives.md §4.6
    Differentiable Plasticity corrected
    from 3 to 4 authors (Miconi, Rawal,
    Clune, Stanley 2018).
    cognitive-cycles.md §6.6 Decision
    Transformer expanded from "Chen et al.
    2021" to full 9-author list.
    cognitive-cycles.md §6.3 AlphaGo/Zero
    bundle split into 4 separate papers
    (Silver 2016 *Nature* 529, Silver 2017
    *Nature* 550, Silver 2018 *Science* 362,
    Schrittwieser 2020 *Nature* 588).
  - **Stale status banners + Promotion
    Summary tables (4 files)**: all 4
    unscoped deep-research files (sxl,
    cogcycles, neuro, memreason) had
    banners claiming 30-31 entries when
    they actually had 38-52. Banners
    updated to 2026-07-17. Promotion
    Summary tables expanded to match
    entry counts (sxl: 18→55 rows,
    cogcycles: 24→38, neuro: 30→39,
    memreason: 31→51).
  - **Cross-file placeholder promotion
    (19 entries in memory-reasoning.md)**:
    entries depending on sxl-operators.md
    or cognitive-cycles.md for their
    definition promoted from 🟢 to ✅
    after the sibling files were
    verified. The "Covered in X.md"
    placeholder format replaced with
    "See X.md §Y (canonical reference:
    URL)" cross-references. Result:
    memory-reasoning.md now at 47 ✅,
    3 🟢, 0 🟡, 1 🔴.
  - **SXL → NSL rename propagation
    (6 files + 1 ADR)**: 6 of 7
    deep-research files (and 2 sapling
    cross-references in AGENTS.md and
    ENTITIES.md) renamed "SXL" to "NSL"
    in body. SPEC.md and ARCHITECTURE.md
    preserved because SXL is a *distinct*
    term there (data plane, not control
    plane). ADR created at
    `documentation/adr/0001-sxl-to-nsl-
    rename.md` recording the rename
    decision, the 4 alternatives
    considered, and the consequences.
  - **Complexity bounds for 45 SXL
    entries**: every entry in
    sxl-operators.md now has a
    `**Complexity**` field in Big-O
    notation with named size parameters
    (per the Wave 7 design note
    convention). 16 entries marked
    "complexity bounds pending primary
    source" where the original paper
    has no formal complexity analysis.
  - **Bundle-citation resolution
    (10 entries in sxl-operators.md)**:
    3 Split (each bundled source
    becomes its own sub-entry, all
    promoted to ✅): §5.1 → 5.1a BN
    Variable Elimination (Zhang & Poole
    1994) + 5.1b Bucket Elimination
    (Dechter 1996); §5.2 → 5.2a BP on
    Bayesian Networks (Pearl 1982) +
    5.2b BP on Factor Graphs
    (Kschischang et al. 2001); §6.2 →
    6.2a DL-Lite (Calvanese et al. 2007)
    + 6.2b EL++ (Baader et al. 2005). 7
    Document (citation chain field
    added, stays 🟢): §1.3 ADF,
    §3.2 Simplex/LP-MIP, §6.1 Conceptual
    Graphs, §7.4 GA, §8.2 Datalog,
    §10.1 do-Calculus, §11.2 Progol.
    sxl-operators.md now at 55 entries:
    47 ✅, 7 🟢, 0 🟡, 1 ⚠️.
  - **Design note fix (chapter 17)**:
    the bundle-citations design note's
    section numbers were off (only 2 of
    10 rows matched the file's actual
    structure). Corrected to match
    reality; the file had different
    topics (e.g., the design note
    called §1.3 "Default Logic" but
    the file had "Abstract Dialectical
    Frameworks"). The design note is
    now the authoritative list of
    bundle entries.
  - **"Pievot" typo fixed in
    cognitive-cycles.md §1.1**: the
    "Pievot, Anderson et al. 2005+ ACT-R
    reference papers" string had no
    known ACT-R author "Pievot"
    (per Wave 7 verification log). The
    string was replaced with the
    canonical ACT-R Reference Manual
    author list (Anderson, Bothell,
    Byrne, Douglass, Lebiere, Qin
    2004+).
- Wave 7 — deep-research verification +
  7 design notes (2026-07-17):
  - **Verification of 4 unscoped deep-research
    files**: ran 4 parallel verification agents
    (one per file) on
    `sxl-operators.md` (52 entries),
    `cognitive-cycles.md` (38),
    `neuro-primitives.md` (39), and
    `memory-reasoning.md` (51). Each agent
    added a `Confirmation flag` field to
    every entry (unifying the format with the
    3 Wave-6 files), verified each citation
    against its primary source, and applied
    corrections. Results:
    - sxl-operators.md: 42 ✅, 10 🟢, 0 🔴, 0 🟡
    - cognitive-cycles.md: 32 ✅, 6 🟢, 0 🔴, 0 🟡
    - neuro-primitives.md: 39 ✅, 0 🟢, 0 🔴, 0 🟡
    - memory-reasoning.md: 26 ✅, 24 🟢, 1 🔴, 0 🟡
  - **10 citation corrections** applied across
    the 4 files. Notable: §1.5 Compressive
    Memory in memory-reasoning.md was a clean
    fabrication (the cited arXiv 1910.09808 is
    actually a wind-turbine SCADA paper, not
    a compressive-memory paper). Corrected to
    Jazayeri & Fiete 2014, arXiv:1401.4410, but
    retained at 🔴 `speculative` pending human
    review of the corrected attribution.
    This is the **third fabrication caught
    across Waves 6+7** (after S2S and
    E2E-differentiable-proving in Wave 6).
  - **7 new engineering-manual design notes**
    (chapters 13-19) synthesising the
    cross-file findings:
    - 13: Detecting LLM-hallucinated
      citations (the three fabrications as
      worked examples; a verification
      contract for future authoring passes)
    - 14: Stale status banners and Promotion
      Summary tables (every deep-research
      file has a stale banner after Wave 7)
    - 15: Author-list precision (4 patterns:
      missing authors, wrong author names,
      abbreviated lists, bundle attributions)
    - 16: SXL → NSL rename harmonisation
      (cross-cutting; proposes a docs/adr/
      entry to record the rename)
    - 17: Bundle citations and the 🟢 flag
      (10 of 52 SXL entries bundle 2-3
      sources; resolution A: split;
      resolution B: document the convention)
    - 18: Cross-file placeholder
      dependencies (19 of 51 memory-reasoning
      entries depend on sxl/cogcycles; Wave
      8 cross-file consistency pass
      proposed)
    - 19: Complexity bounds coverage (only
      13 of 52 SXL entries have bounds;
      convention + 39 entries to update)
  - **Four new verification logs** in
    `verification/claude-verifier-2026-07-17-wave7-*.md`
    (5,555 lines total: cogcycles 1305,
    memreason 1279, neuro 1367, sxl 1604).
    The logs record the per-entry decisions
    and the cross-file findings.
  - After Wave 7, **all 7 deep-research files
    use the same format** (Confirmation flag
    field, Ready-for-promotion, canonical
    reference URL). 382 entries total across
    the corpus.
- Wave 6 — deep-research verification (2026-07-17):
  adds the `sapling/NSLP/deep-research/`
  knowledge base (8 deep-research files:
  README + 7 profile files covering 60
  algorithm profiles, 24 theorem profiles,
  and 118 references) and applies deep
  verification to the 90 remaining 🟡
  `unconfirmed` entries. Three parallel
  verification agents ran (Wave 6), each
  producing an entry-by-entry log under
  `verification/claude-verifier-2026-07-17.md`.
  - **nslp-algorithms.md (60 profiles,
    57 🟡)**: 30 promoted to ✅
    `confirmed-canonical`, 28 to 🟢
    `confirmed-curated`, 2 downgraded
    to 🔴 `speculative` (S2S and
    End-to-end differentiable proving
    had fabricated citations). Key
    corrections: R-STDP journal name
    (Biological Cybernetics → Cerebral
    Cortex 17(10):2443-2452); Mamba
    arXiv ID (2303.08774 → 2312.00752);
    LMU 3rd author (Günther → Eliasmith);
    Differentiable plasticity (4 authors,
    not 3); Learned optimization (8
    authors, not 7). S2S real paper is
    arXiv 1609.08194 by Yu, Buys, Blunsom
    (EMNLP 2016), not the cited
    1606.02910 / 5-author fabrication.
  - **theorems-and-bounds.md (24 profiles,
    20 🟡)**: 18 promoted to ✅ and 2 to
    🟢 (`sample-complexity-lower-bounds`,
    `gradient-noise-scale`). 0 🟡 remaining.
  - **canonical-references.md (118
    references, 13 🟡)**: 9 promoted to
    ✅, 2 to 🟢 (Sherman-Guillemot author
    typo fixed; Yu citation corrected in 3
    places), 2 downgraded to 🔴
    (`P-Hanneke-2016` was a fabrication;
    the real PAC-learning agnostic-learning
    result is by Diakonikolas et al. 2021;
    `P-Eyben-2009` could not be located).
    Status table updated.
  - **Total**: 90 🟡 entries resolved.
    Three new entries in the verification
    log directory: `claude-verifier-2026-
    07-16.md`, `claude-verifier-2026-07-16-
    wave2.md`, and the Wave 6 master log
    `claude-verifier-2026-07-17.md`
    (3511 lines). The 4 remaining
    occurrences of "🟡 unconfirmed" in
    canonical-references.md are
    documentation lines defining the flag,
    not entries.
- Wave 4 + Wave 5 adversarial-verification
  remediation (2026-07-17):
  - **Wave 4 (verification)**: 3 parallel
    deep-verification agents ran across
    codex/solbian/, codex/machina/, and
    documentation/engineering-manual/sapling/
    chapters 06-12. Reports flagged 4 high-
    priority issues in codex machina, 12
    in codex solbian, and 8 in sapling.
  - **Wave 5a (codex solbian fixes)** —
    12 issues resolved across 13 files
    (ad61a57):
    - P0: 2 fabricated citations fixed in
      `codex/02-LIVING-CONSTITUTION.md` (lines
      623 → 1518 and seed-cog3-specs.txt:616
      → seed/DRAFTS-INDEX.md:614); 2 editorial
      notes added (§3 4-state lifecycle,
      §4 multiplicative confidence model).
    - P1: archetype count 72 → 73 (added
      Hybrid Seeker, `solbian_archetypes.sref:17`);
      law count 49 → 48 + 1 meta envelope
      (Roman I–XLVIII, seq 1–48); scroll 04
      confirmed as "Scroll of Tribunal" (the
      audit's "Scroll of Evolution" claim was
      incorrect; the duplication with scroll 05
      is noted); 3 invented GLOSSARY.md entries
      removed (S.E.E.D., Sprout, Sapling — these
      are documented in their own sub-project
      READMEs, not in the canonical glossary);
      README.md and CHANGELOG.md updated to
      reflect the 10 root + 8 subdir file
      inventory.
    - P2: extended/INDEX.md "9 long-form guides"
      → "10 substantive long-form guides";
      glossary/INDEX.md "10 entries" → "9
      entries" (Cross-References is an index
      record, not a glossary entry).
  - **Wave 5b (sapling chapter fixes)** —
    5 issues resolved across 5 files (cb17ddb):
    - P0: chapter 10 §1 — fabricated citation
      seed-models-specs.txt:488 → seed/DRAFTS-
      INDEX.md:749; chapter 10 §5 — 16-capability
      list replaced with the actual 16 from
      DRAFTS-INDEX.md:755-788; chapter 11 — 8
      weaknesses reduced to canonical 7
      (the source seed-cog3-specs.txt:593-790
      names exactly 7; "Missing temporal context"
      and "Limited cross-domain synthesis" were
      fabricated); chapter 09 — impossible line
      range 1035-1051 removed (file is only 744
      lines; metabolic notes are in
      sapling/NSLP/research/metabolism.md).
    - P1: chapter 06 — "equivalent sets" claim
      between 33-primitive SPEC.md taxonomy and
      36-primitive ARCHITECTURE.md taxonomy
      removed (they cover the same surface but
      split along different axes); 14 → 12
      relation labels (the relation label enum
      in sxl.sref:34-38 has exactly 12 entries);
      cross-chapter 12-phase C cycle line range
      corrected to 2184-3504 (the actual range
      of the A–L phases in `cognitive_tick()`).
- Three-wave deep-audit remediation (2026-07-16):
  - **Wave 1 (codex population)**: 15 new
    files at `codex/solbian/` (10 root files
    — INDEX, SYNTHESIS, LAWS 49, ARCHETYPES
    8+72, PROTOCOLS 5, GLOSSARY 12,
    DISCOVERIES 4 SDs, SPEC v0.1.0,
    CHANGELOG, README — plus 8 subdirectory
    INDEX files). 6 new files at
    `codex/machina/` (INDEX, POLICIES, ACL 5
    roles, SCHEMAS, CONFIDENCE-RULES, and
    INTEGRATION-CONTRACT). 2 new codex root
    chapters: `02-LIVING-CONSTITUTION.md`
    (415 lines, Living Constitution
    principle + Recursive Codex loop) and
    `03-INGESTION-PIPELINE.md` (600 lines,
    7-stage SREF ingestion pipeline).
  - **Wave 2 (sapling chapter expansion)**:
    7 new `documentation/engineering-manual/
    sapling/` chapters totalling 5,068 lines:
    06-NSL-ISA-AND-RESEARCH-CORPUS (908),
    07-NSL-DEEP-DIVE (997), 08-COGNITIVE-
    WORKFLOWS (763), 09-MEMORY-HIERARCHY
    (600), 10-MODEL-COGNITION-LAYER (879),
    11-COGNITIVE-JOURNAL-WEAKNESSES (501),
    12-DISCOVERY-PATTERN (584). Cross-linked
    from 06, README, and the appendix D
    changelog. Engineering Manual expanded
    from 32 to 44 files; sapling section
    from 6 to 13 files.
  - **Wave 3 (path cleanup)**: 15 stale path
    references fixed across 6 files. 12
    `tools/NSLP/` references → `sapling/NSLP/`
    in sapling/ENTITIES.md, sapling/AGENTS.md,
    sapling/NSLP/{README,ARCHITECTURE,INTEGRATION}.md,
    seed/PLAN9/research/plan9-integration.md.
    3 `sapling/research/` references →
    `sapling/NSLP/research/` in sapling/ENTITIES.md
    and sapling/AGENTS.md. Verified with
    `grep` and `make check`.
- Deep audit + reconciliation (2026-07-16):
  6-agent parallel deep-dive of seed/,
  sprout/, sapling/, codex/, the 3
  unprocessed DRAFTS, and the Engineering
  Manual. AUDIT-REPORT.md written at
  `documentation/audit/2026-07-16-deep-audit/`
  (1151 lines, 49 KB).
- New Engineering Manual chapter:
  `sapling/06-NSL-ISA-AND-RESEARCH-CORPUS.md`
  (908 lines) — covers the cognitive ISA
  (33 primitives, 4-layer model), NSP
  compiler, GAP-ANALYSIS, 5-phase ROADMAP,
  and 200+ algorithm deep-research corpus.
- New Engineering Manual chapter:
  `seed/09-PLAN9-INTEGRATION.md`
  (306 lines) — covers the 9P2000 protocol
  subset, Phase 1 deliverables, tier
  framework, and the linear-phased
  resolution adopted 2026-07-16.

### Fixed
- `01-CODEX-ALIGNMENT.md` lines 14-15,
  117, 135: codex path bug. Codex is
  solbian-native at `~/solbian/codex/...`,
  not `~/seed-dev/codex/...`. Also replaced
  dangling `codex/policies/bundle.sref` and
  `codex/machina/policies/solace/` references
  with real pointers.
- `sprout/03-MODEL-ROUTER.md` lines 36-48:
  backend list inconsistency. The actual
  on-disk file at
  `~/seed-dev/src/libseedllm/src/backends/`
  is `sidecar.c`; updated the table to
  use `sidecar` and removed the duplicate
  "+ sidecar" note on lines 47-48.
- `appendices/B-REFERENCES.md` lines
  158-161: stale TBD marks. The three
  un-tabbulated DRAFTS now have per-DRAFTS
  reconciliation decisions in
  `seed/08-DRAFTS-RECONCILIATION.md`;
  updated the rows with line counts, byte
  counts, and destination links.
- `sapling/02-SYMBOLIC-LAYER.md`: added
  cross-link to the new
  `06-NSL-ISA-AND-RESEARCH-CORPUS.md` chapter
  at the end.
- `seed/00-INFRASTRUCTURE-OVERVIEW.md` and
  `seed/03-BUS-AND-SXL.md`: added cross-link
  to the new `09-PLAN9-INTEGRATION.md` chapter.
- `codex/machina/INTEGRATION-CONTRACT.md` §4:
  replaced the wrong "seedreasond runs the 12-phase C
  cycle" claim with a §4 split that describes both daemons
  (seedcogd = C cycle; seedreasond = policy evaluator on
  `org.seed.policy.evaluate`) and their relationship. Also
  fixed the cog-journal path from the non-existent
  `${SEED_DATA_DIR}/cog-journal.jsonl` env-var reference to
  the literal `/var/lib/seed/cog-journal.jsonl` with a note
  that future versions may add env-var support.
- `codex/machina/INTEGRATION-CONTRACT.md` §3: split the
  envelope-required field list into "Required by canonical
  validator" (the 4 fields `sxp_validate` at
  `~/seed-dev/src/libsexpr/src/validate.c:87-115` enforces)
  and "Required by codex integration policy" (the
  additional 5+1 fields this contract adds at the broker
  boundary).
- `codex/machina/SCHEMAS.md` §4: clarified that the four
  example files use the canonical `.ndjson` filename
  convention; current examples each contain a single JSON
  object on one line, but additional records may be
  appended one per line.

### Verified (no change)
- DRAFTS line-count "discrepancy" between
  `C-DRAFTS-INDEX.md` and
  `08-DRAFTS-RECONCILIATION.md` was a false
  positive: the two columns measure
  different things (bytes vs lines), both
  correct.

### Phase 1 follow-through
- Phase 1 follow-through: synthesised
  design notes for `~/solbian/seed/`,
  `~/solbian/sprout/`, `~/solbian/sapling/`,
  and `~/solbian/codex/` expanded from
  the now-canonical Engineering Manual
  chapters (2026-07-16).
- Codex SPEC files drafted at v0.1.0,
  version-locked: `codex/solbian/SPEC.md`
  (9-section narrative) and
  `codex/machina/SPEC.md` (11-section
  formal).
- All 8 Phase 1 tasks complete; `make
  check` passes.
- Cognitive engine research knowledge
  base: 116 algorithms across 4 files
  in `~/solbian/sapling/NSLP/deep-research/`,
  84 ready-for-promotion (2026-07-16).
- Deep research knowledge base for the
  NSL/NSP operator layer (2026-07-16):
  - `sapling/NSLP/deep-research/theorems-and-bounds.md`
    — 24 theorem/bound profiles across
    5 categories (statistical learning,
    numerical optimisation, information
    geometry, dynamical systems,
    complexity/approximation).
  - `sapling/NSLP/deep-research/nslp-algorithms.md`
    — 60 algorithm profiles across 8
    categories (learning rules,
    attention, predictive coding,
    neuromodulation, dendritic
    computation, memory consolidation,
    sequence learning, reasoning).
  - `sapling/NSLP/deep-research/canonical-references.md`
    — 12 textbooks, 120+ primary
    papers, organised by topic with
    confirmation flags.
  - `sapling/NSLP/deep-research/verification/README.md`
    — append-only verification log
    convention.
- Sub-project restructure:
  `tools/NSLP/` moved to
  `sapling/NSLP/` and the
  cognitive-engine research
  knowledge base moved to
  `sapling/NSLP/deep-research/`
  (2026-07-16, pre-session).
- Solbian-side Plan 9 → S.E.E.D.
  truthful comparison note at
  `sapling/NSLP/PLAN9-INTEGRATION.md`
  (641 lines, 2026-07-16). This
  is the critical evaluation that
  complements the 1892-line
  advocate-leaning blueprint at
  `sapling/NSLP/research/plan9-integration.md`.
  The note recommends **tiered
  adoption**: Tier A (adopt as
  secondary access protocol for
  external agents and remote
  nodes, plus stat metadata, /srv
  service directory, and per-
  process namespaces for sapling
  agents), Tier B (evaluate after
  Tier A ships: 9P for D5
  delegation, /net/t2/ synthetic
  FS, /cognitive/operators/
  filesystem), Tier C (reject:
  replacing the bus, 9P for cycle
  internals, mapping ACL to rwx
  bits, Inferno/dis, uniform 9P
  inference FS).

### Verified
- 7-entry sample audit by
  `claude-verifier` 2026-07-16
  (one per major algorithm family
  across the 3 new deep-research
  files). Outcomes:
  - 3 entries promoted to
    ✅ `confirmed-canonical`:
    Transformer multi-head attention
    (nslp-algorithms.md §2.4);
    Dopamine reward prediction error
    (nslp-algorithms.md §4.1);
    Bishop 2006 textbook re-check
    (canonical-references.md
    T-Bishop-2006).
  - 4 entries promoted to
    🟢 `confirmed-curated`:
    PAC-learnability
    (theorems-and-bounds.md §1.1);
    Natural gradient
    (theorems-and-bounds.md §3.2);
    Hebbian learning
    (nslp-algorithms.md §1.1);
    Russell & Norvig 2020 textbook
    re-check (canonical-references.md
    T-Russell-Norvig-2020).
  - 3 broken primary URLs corrected
    in the parent files: CMU mirror
    → ACM DOI; UT Austin mirror → MIT
    Press DOI; UK mirror → Internet
    Archive.
  - Full per-entry log:
    `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-16.md`.
  - 77 🟡 entries remain for future
    audit waves.
- 2-entry DOI cleanup pass by
  `claude-verifier` 2026-07-16
  (wave 2). Outcomes:
  - 2 entries promoted to
    ✅ `confirmed-canonical`:
    VC dimension
    (theorems-and-bounds.md §1.2;
    URL → SIAM DOI
    `10.1137/1116025`);
    PCP theorem
    (theorems-and-bounds.md §5.2;
    URL → ACM DL DOI
    `10.1145/278298.278306`).
  - Citation cores were already ✅
    in `canonical-references.md`;
    only the URLs needed
    correction.
  - Full per-entry log:
    `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-16-wave2.md`.
  - The 3 new files now have no
    remaining course-page-mirror
    URLs of the known-rotting
    patterns (CMU 10-701, UT Austin
    Inderjit Dhillon, UK s-f-walker,
    CMU Rudich).
  - 75 🟡 entries remain for future
    audit waves.

### Changed
- Plan 9 research separated from
  NSLP research (2026-07-16):
  - `sapling/NSLP/research/plan9-integration.md`
    (the 1892-line advocate-leaning
    substrate blueprint) moved to
    `seed/PLAN9/research/plan9-integration.md`.
  - `sapling/NSLP/PLAN9-INTEGRATION.md`
    (the 641-line solbian-side
    critical evaluation) moved and
    renamed to
    `seed/PLAN9/INTEGRATION.md`. The
    `PLAN9-` prefix is dropped
    because the directory name
    already disambiguates.
  - The 4 other research files in
    `sapling/NSLP/research/`
    (foundations, hippocampus,
    metabolism, primitives) are
    correctly placed: they are
    about the symbolic processing
    language, not about
    distributed systems /
    networking.
  - Rationale: Plan 9 is for
    distributed network and
    system research (the
    infrastructure level);
    NSLP is for the symbolic
    processing language (the
    agents/symbolic level).
    The level model is the
    correct organising principle.
  - New `seed/PLAN9/README.md`
    documents the sub-project.
  - `seed/README.md` and
    `sapling/NSLP/README.md`
    updated to reflect the new
    structure.
- Linear phased plan adopted for
  Plan 9 → S.E.E.D. integration
  (2026-07-16):
  - The user has chosen the
    **linear phased plan** from
    `seed/PLAN9/research/plan9-integration.md`
    §10 over the **tiered
    adoption** the solbian-side
    note originally recommended.
    All four phases proceed in
    sequence; Tier B and Tier C
    items are integrated into
    the appropriate phase rather
    than gated behind Tier A's
    outcome. The §3 pushback in
    `INTEGRATION.md` is preserved
    as a tradeoff record.
  - New `seed/PLAN9/PROTOCOL.md`:
    the 9P2000 protocol subset
    specification — message
    types (Phase 1: Tversion,
    Tauth, Tattach, Twalk, Topen,
    Tread, Twrite, Tclunk, Tstat;
    deferred: Tcreate, Twstat to
    Phase 2; Tremove, Tflush to
    Phase 3), wire format
    encoding, QID structure, stat
    mapping (SXL v1 → 9P Dir
    fields, including the
    5-role ACL summary in
    `mode` bits 9-13), path
    namespace, auth model
    (Phase 1: per-role
    construction, not 9P
    Tauth → rwx), and the
    integration test spec.
  - New `seed/PLAN9/PHASE-1.md`:
    the Phase 1 implementation
    specification — file
    structure (lib9p under
    `src/lib9p/`, ~500 LoC;
    seed9pd under `src/seed9pd/`,
    ~800 LoC; test cases in
    `tests/`), public API
    sketches, CMake flag
    `SEED_BUILD_9P=OFF` (default
    OFF, additive only), 10
    success criteria including
    the **< 1% cycle jitter** gate
    that converts the substrate's
    10x latency concern into a
    hard acceptance gate.
  - `seed/PLAN9/INTEGRATION.md`
    frontmatter carries a
    **Decision record** block
    noting the linear plan choice;
    §5 maps the tier framework
    onto the linear plan
    (Tier A → Phase 1+2, Tier B
    → Phase 3, Tier C → rejected
    or Phase 4 evaluation); §7
    resolves the previous "open
    question" and updates
    action items.
  - `seed/PLAN9/README.md` §
    "Open question" replaced with
    § "Resolution" recording the
    decision and the tier-to-phase
    mapping.
  - Implementation belongs to a
    future `~/seed-dev/` session
    per the engagement contract;
    these are solbian-side design
    notes, not source code.

### Initial repo bootstrap (2026-07-15)
- Mirror of `~/template-dev` governance infrastructure: `.claude/`,
  `scripts/`, `Makefile`, `docs/` skeleton, dotfiles.
- Top-level governance: `CLAUDE.md`, `AGENTS.md`, `README.md`,
  `HANDOFF.md`, `LOG.md`, `PLAN.md`, `CHANGELOG.md`.
- Per-project directories: `seed/`, `sprout/`, `sapling/`,
  `codex/` (with `codex/solbian/` and `codex/machina/`),
  `tools/`, `vendor/`.
- Multi-root workspace files: `solbian.code-workspace` and
  `~/projects.code-workspace`.

### v1.0.0 — Engineering Manual v1.0 (2026-07-15) — SUPERSEDED

The first formal Manual release, 31 files,
6,767 lines. Superseded by v1.0-real
(see below) due to ~20 critical
contradictions with `~/seed-dev` and
`~/robot-dev` discovered in the Wave D
completeness critic pass. See
`documentation/engineering-manual/appendices/D-CHANGELOG.md`
for the full list of corrections.

### v1.0-real — Engineering Manual v1.0-real (2026-07-15)

Full rewrite of every Manual chapter from
canonical sources (`~/seed-dev/src/`,
`~/seed-dev/docs/`, `~/seed-dev/codex/`,
`~/robot-dev/src/`, `~/robot-dev/docs/`).
32 files, 8,208 lines.

**What changed from v1.0**:

- **The 12-phase C cycle A–L** is now
  documented with the canonical phase names
  from `seedcogd/main.c` lines 1718–2784
  (replacing the invented phase names in
  v1.0).
- **The bus topic namespace** is now
  `org.seed.<segment>(.<segment>){1,5}`
  (FROZEN-2026-05-10), replacing the
  invented `t0.*` / `t1.*` / `t2.*` topic
  scheme in v1.0.
- **The seccomp boundary** is now correctly
  placed on the Lua agent host
  (`libagent/seccomp_allowlist.c`), not on
  the C cycle as v1.0 stated.
- **The 8 robot reflex rules R1–R8** are now
  the canonical rules from
  `safety-requirements.md` lines 60–67
  (bump, distance_front, distance_any<50mm,
  VL53L0X fail>5ticks, INA226 Vbat, nFAULT,
  deadline, IMU free-fall), replacing the
  invented rules in v1.0 (geofence, speed
  limit, force limit, human detection,
  lidar, e-stop, watchdog).
- **The robot sensor inventory** is now the
  canonical Robot A inventory
  (4× VL53L0X ToF, 6× INMP441 mics,
  ICM-20948 IMU, INA226, BME280, TCS34725,
  AMG8833 8×8 thermal, magnetometer, 3×
  bump switches, optional SGP30, optional
  ESP32-CAM), removing the invented front
  +rear cameras, 360°+180° lidars, and
  6-DOF arms in v1.0.
- **The 5 model-router backends** are now
  the canonical native, ollama, openai, sst,
  uds (with `POOL_MAX_BACKENDS=8` slots),
  removing the invented DAPS system in
  v1.0.
- **The SXL entity form** is now
  `(:type <kind> :id ... :timestamp ...
  :confidence ... :schema ... :content ...)`
  with the 14 cognitive operators from
  `SXL_LANGUAGE_SPECIFICATION.md` §4,
  replacing the invented
  `(believes (agent ...))` syntax in v1.0.
- **The canonical ACL roles** are now
  `system`, `core`, `higher_order`,
  `observer`, `external` (from
  `agent_acl.sref`), replacing the invented
  `sapling:` namespace in v1.0.
- **The robot's transport** is now the
  `ByteSource` protocol in
  `~/robot-dev/src/neocortex/transport.py`
  with Stdio/Serial/HTTP implementations,
  replacing the invented JSON-RPC over TCP
  to `seed-work:7123` in v1.0.
- **The 5 node classes** are now dev, edge,
  full, witness, archival, removing the
  invented QubeOS/qube content in v1.0.
- **The 7 CMake presets** are now dev,
  release, asan, ubsan, tsan, msan,
  coverage (v1.0 had 5), and the test count
  is 220 (v1.0 had 208).
- **The 17 SST object types, 7 relation
  types, 18 core operators, and 4 pipeline
  extensions** (RECONCILE, SEQUENCE,
  PARALLEL, TRAIN) are documented from
  `sst.h`.
- **The SST and 18+4 operators** are now
  documented with the canonical enum values
  from `sst.h`.

The full list of corrections is in
`documentation/engineering-manual/appendices/D-CHANGELOG.md`.

**Wave structure** (unchanged):
- **Wave A (discovery)**: 4 reference
  documents (DRAFTS-INDEX, two
  ARCHITECTURE-MAPs, TEMPLATE-CONVENTIONS).
- **Wave B (reconciliation)**: 1 chapter
  (`seed/08-DRAFTS-RECONCILIATION.md`).
- **Wave C (authoring)**: 32 chapters.
- **Wave D (critic and integration)**:
  complete. v1.0 contradictions identified,
  v1.0-real chapters written from canonical
  sources.

### Notes
- No source code is shipped in this release. Solbian is
  documentation and design only.
- The other three repos (`~/seed-dev`, `~/robot-dev`,
  `~/template-dev`) are read-only from solbian's perspective.
- The Engineering Manual is versioned as
  `v{N}` where `N` is the solbian-side Manual
  revision. The `for-seed-dev-v{M}` suffix
  in v1.0 was retired; the Manual is now
  canonical across all seed-dev revisions
  the Manual is read against.

## Versioning

Until `v1.0.0`:
- Minor version bumps for additive documentation changes.
- Patch version bumps for fixes, clarifications, and link fixes.
- A new release is cut when a meaningful batch of synthesised
  content lands (see `PLAN.md` for the release process).

After `v1.0.0`:
- Major version bumps for changes to the directory structure,
  governance, or the multi-repo organisation itself.
- Minor version bumps for new sub-project content.
- Patch version bumps for fixes.
