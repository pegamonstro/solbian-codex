# Codex Solbian — Phase I · Stage 5 Codex Engine Prototype

**As-of:** 2026-09-21 · **Engine:** `stage5-1.0.0` · **CANONICAL: NONE**

A deliberately boring, inspectable engine that turns the preserved Stage 3 source
index into **observations** and **PROPOSED records**. Python standard library +
`sqlite3` only. No network, no vector DB, no graph DB, no hidden model calls.

- `engine.py` — deterministic analyzers + CLI (`run`, `list-proposals`, `show`, `list-runs`)
- `smoke_engine.py` — end-to-end verification, exits `0`
- `schema_engine.sql` — the one table the engine adds (`analysis_run`)
- `data/codex_phase_i.sqlite` — the local working copy the engine writes to

---

## The one rule

The engine proposes; it never decides. Every row it writes has status
`PROPOSED` or `WORKING`, carries the marker `engine:stage5:<kind>:<run_id>`, and
links back to at least one `source_document` and/or `message` through
`provenance_link`. The word `CANONICAL` is not written anywhere — the content
status enum does not contain it and a guard scans for it before and after every run.

| Layer | Meaning | Stored as |
| --- | --- | --- |
| SOURCE | the preserved corpus | `source_document` / `message` rows, **never touched** |
| INTERPRETATION | what the engine inferred | the literal tag `INTERPRETATION` in `notes`/`body` |
| PROPOSAL | a drafted next step for a human | `proposal.status = 'PROPOSED'` |

---

## Store: read the SoT, write a working copy

The Stage 3 store is the source of truth and is treated **read-only**:

```
SoT (read-only)   /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite   (935 source_document rows)
working copy      ./data/codex_phase_i.sqlite                                          (created on first run)
```

The first `run` copies the SoT into `data/` (the same pattern Stage 4 uses; the
current file sandbox only permits writes inside this workspace). Every run then
verifies that `source_document` is byte-identical by row count and digest, and
the smoke test additionally checks that the SoT's `sha256` and the Mac corpus
fingerprint are unchanged.

Point the engine anywhere with `--db`, including the SoT on a machine where it
is writable:

```bash
python3 engine.py --db /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite run
```

`--db` resolving inside the Mac corpus (`/Users/archcore/solbian/codex`) is
refused with exit code 2.

---

## Quickstart

```bash
cd /Users/archcore/solbian/codex-phase-i-stage5
python3 engine.py run                 # analyze, write PROPOSED rows
python3 engine.py list-proposals      # inspect what was proposed
python3 engine.py show <id|prefix>    # read one proposal with its provenance
python3 engine.py list-runs           # inspect analysis_run bookkeeping
python3 smoke_engine.py               # verify everything; exits 0
```

Example:

```
Codex Phase I — Stage 5 engine stage5-1.0.0  (LLM: OFF)
store : /Users/archcore/solbian/codex-phase-i-stage5/data/codex_phase_i.sqlite
SoT   : /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite (read-only)
source_document before: 935
[plurality     ] status=OK run=arun_f8d2bae872f7a39f  proposal=6, provenance_link=52
[duplicates    ] status=OK run=arun_84776e534c98155c  proposal=7, provenance_link=22, relationship=13
[underdeveloped] status=OK run=arun_08768a4f7679827f  concept=20, proposal=20, provenance_link=314, relationship=120
[durable       ] status=OK run=arun_f05454b551f2323a  no writes
[discussion    ] status=OK run=arun_f14f2aab47452100  proposal=11, provenance_link=52
source_document after : 935 (unchanged)
store totals      : proposal=44, concept=20, relationship=133, provenance_link=440
```

### CLI

```
engine.py [--db PATH] [--sot PATH] <command>

run              --kind all|plurality,duplicates,...   analyses to run
                 --llm                                  enable the optional LLM hook (off)
                 --dry-run                              compute, then roll back (no rows committed)
                 --reset                                delete engine-created rows first
                 --refresh-db                           re-copy the SoT into the working copy
                 --min-freq N                           underdeveloped-token threshold (default 5)
                 --max-findings N                       per-analyzer cap (default 20)
list-proposals   --status PROPOSED   --limit N   --json
show <id|prefix> --json
list-runs        --json
```

---

## Analyses

All five are deterministic and inspectable; ids are content-derived so re-runs
never duplicate rows.

1. **`plurality`** — reads `plurality_flags` (law / protocol / scroll /
   sref-artefact / scroll-ordinal / scroll-20) and emits one
   *"preserve plurality — do not merge"* proposal per flag, plus a coverage-gap
   proposal for law/protocol/scroll paths that lack the matching flag, plus a
   scroll-20 check if the anomaly flag is missing. Nothing is renumbered.
2. **`duplicates`** — groups the index by lowercased basename. Groups with ≥2
   non-directory files get one proposal each (with `BASENAME_COLLISION`
   relationship rows); directory-only collisions get one aggregate proposal.
   A human decides whether the copies are the same work, plural, or unrelated.
3. **`underdeveloped`** — counts tokens in document titles, drops structural
   words, and reports tokens above `--min-freq` that have **no dedicated
   document, glossary entry or stored definition**. Each becomes a `PROPOSED`
   `concept` candidate plus a proposal and `MENTIONED_IN` relationship rows.
4. **`durable`** — if `message` rows exist, messages ≥280 characters become
   *durable candidate* proposals with a stored quote, confidence
   `TEXT-SUPPORTED`, and an `INTERPRETATION` label. The Stage 3 store has no
   conversations, so today this records `skipped: no message rows` and writes
   nothing (the smoke test exercises it with a synthetic fixture).
5. **`discussion`** — synthesises *discussion-topic* proposals for the gaps the
   other analyzers find: underdeveloped tokens, plurality anomalies, and large
   duplicate clusters. These are questions, confidence `SYNTHESIS`, never answers.

### Idempotency / re-runs

* Every proposal / concept / relationship / provenance row id is
  `sha1(kind + natural key)`, so a re-run **updates in place** — counts and ids
  are stable (asserted by the smoke test).
* Re-runs refresh engine-owned `summary`/`body`/`notes`, but never overwrite a
  human's `status` or a concept `definition`.
* `analysis_run` ids are `arun_<sha1(kind, engine_version)>`, so re-running a
  kind updates the same bookkeeping row rather than appending history.
* `--reset` deletes only rows carrying the `engine:stage5:*` marker (and links
  whose subject/endpoint is such a row) before re-running — it never touches
  source data.
* `--dry-run` keeps the whole pass in one transaction, prints the summary, then
  rolls back; no rows are committed.

---

## What is written

Into the existing Stage 3 tables (in the working copy):

| Table | What the engine adds | Status |
| --- | --- | --- |
| `proposal` | drafted additions / reviews / discussion topics | `PROPOSED` |
| `concept` | concept candidates from underdeveloped tokens | `PROPOSED` |
| `relationship` | title-level candidate links (`BASENAME_COLLISION`, `MENTIONED_IN`, `PROPOSES_CONCEPT`, …) | `PROPOSED` |
| `provenance_link` | one link per proposal/concept to a source (and quotes for messages) | `PROPOSED` / `WORKING` |
| `analysis_run` | run bookkeeping + `summary_json` | `RUNNING` / `OK` / `ERROR` |

Confidence values: `TITLE-LEVEL` for path/title reasoning, `SYNTHESIS` for
derived discussion topics, `TEXT-SUPPORTED` only when a quote is stored
(durable messages). Never `CANONICAL`.

**Forbidden and enforced:** mutating `source_document`; inventing a canonical
value; writing the Mac corpus; merging catalogues; deleting historical pointers.

---

## Optional LLM (default OFF)

`--llm` does nothing unless `SOLBIAN_LLM_CMD` points at an external command:

```bash
SOLBIAN_LLM_CMD='my-llm-cli --quiet' python3 engine.py run --llm
```

The prompt is the corpus-index summary on stdin, output is stored as a
`PROPOSED` proposal labelled `INTERPRETATION (LLM-generated…)`, linked to the
context documents, and never consolidated. With no backend configured the flag
prints a notice and the deterministic run proceeds unchanged.

---

## Verify

```bash
python3 smoke_engine.py     # 37 checks, exit 0
```

It runs against throwaway copies and asserts: ≥1 proposal each with provenance;
`PROPOSED`/`WORKING` only; no `CANONICAL` anywhere; `source_document` count and
digest unchanged; SoT `sha256` and Mac corpus fingerprint unchanged; idempotent
re-runs; working inspectors; no-op dry-run; the durable path with a synthetic
conversation; the Mac-corpus write guard; and `--llm` defaulting off.

---

## Optional Stage 4 wiring

Stage 4 was **not modified** and does not need to be. If a thin admin surface is
wanted later, point Stage 4's read-only *Codex Solbian* surface at
`data/codex_phase_i.sqlite` and render `proposal` / `concept` / `provenance_link`
as a read-only list plus `engine.py show <id>`. The engine owns all writes;
the UI should own none.
