# ADMISSION_REGISTER — Phase II gate candidates
**As-of:** 2026-09-21 ~02:24 PT · **CANONICAL:** NONE  
**Authority:** SPEC 14 admission test  
**Scoring axes:** Problem · Necessity · Simplicity · Boundary · Reversibility · Evidence  
**Verdicts:** **ADMIT** (Phase II feature) · **ADMIT-thin** (small reversible slice only) · **DEFER** · **REJECT** · **OPS** (preservation/ops — not a product feature admission)

**Partner defaults applied:** Prefer HOLD on the Phase II *gate* unless a concrete living-loop failure requires a thin slice. Historical temptation alone never admits.

## How to read a row

- **ADMIT / ADMIT-thin** = may enter a future Phase II *thin* backlog if JD opens the gate.
- **DEFER** = automatic or judgment deferral; revisit only with new demonstrated failure.
- **REJECT** = wrong for Codex Phase product shape (or conflates RELATED projects).
- **OPS** = do the work as ops/preservation; do **not** count as Phase II feature scope.

---

## Register

| ID | Candidate | Origin | Problem | Necessity (fails without?) | Simplicity | Boundary | Reversibility | Evidence | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | Real Solace LLM (replace stub) | Historical + Stage 4 stub | Stub replies are not useful dialogue | Loop **works** without LLM; quality gap only | External model/cmd | New service/dependency | Yes (flag OFF) | Demonstrated stub label; **no** loop failure | **DEFER** | SPEC 14 auto-adjacent; optional Stage 5 `--llm` already exists OFF |
| C02 | Vector search over corpus | Historical plans | Keyword browse may miss related text | Browse works; 935 docs navigable | Embedding store | New subsystem | Partial | Hypothetical | **DEFER** | Automatic deferral (SPEC 14) |
| C03 | Graph DB / ontology layer | Historical | Relationships are SQLite rows | Engine already writes `relationship` | Heavy | New conceptual layer | Hard | Hypothetical | **DEFER** | Automatic deferral |
| C04 | Blockchain / memory_blockchain | RELATED `projects/` | Durability narrative | SQLite + git backups suffice for Phase I | High complexity | External project | Hard | None for loop | **DEFER** | Automatic deferral; RELATED |
| C05 | S.E.E.D. coupling | RELATED / Helios | Adjacent ecosystem | Loop does not need SEED | Coupling | **Boundary break** | Risky | Architecture smell | **DEFER** | Automatic deferral |
| C06 | GOLEM coupling | Historical summaries | — | Not required | Coupling | Boundary break | Risky | None | **DEFER** | Automatic deferral |
| C07 | Codex Machina coupling | RELATED sibling | — | Separate repo by design | Coupling | Boundary break | Risky | Smell | **DEFER** | Automatic deferral |
| C08 | Multi-agent / agent frameworks | `source_original/agents/` | Parallel personas | Single JD↔Solace is Phase I | Framework sprawl | Boundary | Hard | Temptation only | **DEFER** | Automatic deferral |
| C09 | External channels (Slack/email/etc.) | Historical | Reach JD elsewhere | Local UI loop works | Integrations | External | Medium | None | **DEFER** | Automatic deferral |
| C10 | Hardware / Homelab runtime binding | Hardware srefs | Deploy on RPi/Helios | Dev loop is local Mac | Ops coupling | Infra | Medium | Ops, not product | **DEFER** | Keep as ops later; not Phase II feature |
| C11 | Autopilot / silent auto-accept proposals | Temptation vs Stage 7 | Faster growth | **Would violate** controlled consolidation | Dangerous “simplicity” | Policy break | Hard to undo socially | Explicitly out of Stage 7 scope | **REJECT** | Breaks SPEC 08 / Stage 7 hard rule |
| C12 | Elevate WORKING → CANONICAL in product | Historical canon wish | “Finished” docs | Phase I forbids; plurality unresolved | Political, not technical | Doctrine | Damaging if wrong | Plurality A/B/B′/C still open | **REJECT** (Phase II gate) | Canon picks = JD conversation topics, not features |
| C13 | Merge law catalogues / protocol 5↔8 / scroll ordinals | Stage 2 contradictions | “One true tree” | System **correctly** preserves plurality | Destructive merge | Corrupts source story | Poor | Stage 6 proves non-collapse | **REJECT** | Analysis may *discuss*; never silent merge |
| C14 | Better durable analyzer quality | Stage 5/7 friction | Proposals shallow vs human synthesis | Loop works; analysis thin | Improve deterministic rules / prompts behind existing CLI | Stays in Engine | Yes | Stage 5: durable skipped on empty messages; synthetic path works; living use will show gaps | **ADMIT-thin** | Only if JD daily use shows repeated weak proposals — still reversible |
| C15 | Living-store export / backup | Stage 7 living SQLite | Single-file loss risk | Preserve step fragile without backup | `sqlite3 .backup` / scripted export | Ops-ish | Yes | Living store is product SoT for new writes | **ADMIT-thin** | Small reversible; pairs with ops backups |
| C16 | GitHub mirror of Phase I *code* (product SoT) | Consolidation + Stage worktrees | Code lives in Mac stageN dirs | Collaboration / recovery | Push stage trees or unified `phase-i` tree to `solbian-codex` branch | Repo hygiene | Yes | GH already product hub; stage code not yet unified mirror | **ADMIT-thin** | Product code SoT ≠ corpus SoT; reversible |
| C17 | UI polish unblocking JD daily use | Stage 4/7 friction | Friction finding Accept / WORKING docs | Loop works; UX may block habit | CSS/JS only on existing surfaces | None new | Yes | smoke 149/149 proves API; daily UX unmeasured here | **ADMIT-thin** | Admit only concrete blockers JD names |
| C18 | Gitea backup of Phase I codebase | **JD ops ask (explicit)** | Homelab preservation | Not a loop failure | Mirror/bundle | Ops | Yes | Pending consol items; JD already requested | **OPS** | **Not** Phase II feature admission — preservation |
| C19 | Mac corpus protected archive tag on GH | Stage 2 underdeveloped #12 | Historical tip ≠ GH main WORKING | Corpus already on Mac; GH tip is WORKING | Tag/branch only | Archive hygiene | Yes | Suggestion only in Stage 2 | **OPS** | Archive ref — not a Phase II feature |
| C20 | Covenant / constitution recovery features | Underdeveloped areas | Thin SOURCE dialogue | Engine can propose discussion topics already | Content work, not infra | Doctrine | Content-reversible | Topics for Solace, not builds | **DEFER** | Conversation topics ≠ features |
| C21 | Full-text search (SQLite FTS5) | Stage 4 browse friction | Keyword find across bodies | Facets+path search exist | FTS5 in same DB | Small | Yes | Mild friction possible | **DEFER** | Prefer evidence from JD use before ADMIT-thin |
| C22 | Distributed / multi-user sync | Historical | Multi-machine | Single-user Phase I | Sync stack | Distributed systems | Hard | Hypothetical | **DEFER** | Automatic deferral class |
| C23 | DAO / tokenomics integration | RELATED `dao_foundation` | Governance experiment | Unrelated to loop | External | Boundary | — | RELATED | **REJECT** | Out of Codex Phase I/II product core |
| C24 | SeedNet / C runtime experiments | Untracked `core/` `tests/` | Runtime demos | Unrelated | Separate | Boundary | — | RELATED/EXPERIMENT | **REJECT** | Keep fenced |

---

## Scorecard summary

| Verdict | Count | IDs |
| --- | --- | --- |
| **ADMIT** (full) | 0 | — |
| **ADMIT-thin** | 4 | C14, C15, C16, C17 |
| **DEFER** | 12 | C01–C10, C20–C22 |
| **REJECT** | 5 | C11, C12, C13, C23, C24 |
| **OPS** | 2 | C18, C19 |

## Phase II gate implication

- **No full ADMIT** items.
- At most **ADMIT-thin** slices — and only if JD opens a *thin* Phase II (or a pre-gate maintenance window).
- Default Partner recommendation: **HOLD** the Phase II feature gate; proceed with **OPS** (C18) and optional ADMIT-thin only when evidenced.
- See `RECOMMENDED_NEXT.md` and `REASSESSMENT_REPORT.md` §H.
