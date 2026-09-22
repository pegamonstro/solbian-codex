# DSH_RESULT — Stage 4 Two-Surface Prototype

**STATUS: COMPLETE**
**As-of:** 2026-09-21 · **CANONICAL: NONE**
**CWD:** `/Users/archcore/solbian/codex-phase-i-stage4/`

---

## What was built

A minimal local two-surface UI over the Stage 3 SQLite store, Python stdlib only
(`http.server` + `sqlite3`), one HTML shell + vanilla JS. No Flask/FastAPI, no
vector DB, no graph DB, no SEED/GOLEM/Machina.

| Deliverable | Status |
| --- | --- |
| `app.py` — local server + JSON API | done |
| `static/index.html`, `static/app.js`, `static/style.css` — two tabs | done |
| `setup_db.py` — working-copy build + full ingest completion | done |
| `schema.sql` — DDL (copied from Stage 3, unchanged) | done |
| `smoke_ui.py` — HTTP checks, `exit 0` | done |
| `README.md` — run instructions | done |
| `DSH_RESULT.md` — this file | done |

### Solace tab
Lists conversations (with message counts), opens one, renders ordered messages,
creates a conversation, and appends a message as `jd` or `solace`. Optional stub
reply is implemented and unmistakably labelled `[WORKING STUB — not LLM-backed]`.
Writes touch **only** `conversation` and `message`.

### Codex tab
Browse/filter `source_document` by free text, `status`, `probable_role`,
`media_type` and corpus root; paged detail pane shows the full metadata row
(`id`, `rel_path`, `corpus_root`, `media_type`, `byte_size`, `mtime`, `sha256`,
`probable_role`, verbatim `inventory_status`, `status`, `plurality_flags`, `notes`,
`attribution`, timestamps) plus an optional read-only text preview. No edit,
rename, delete or canonical control exists; every non-GET under `/api/codex/`
returns 405.

---

## How JD runs it

```bash
cd /Users/archcore/solbian/codex-phase-i-stage4
python3 app.py
# open http://127.0.0.1:8787/
```

Flags: `--port N`, `--host`, `--db PATH`, `--verbose`. The store path can also be
set with `SOLBIAN_DB`.

---

## Verification (all run in this session)

### `python3 smoke_ui.py` → exit 0

Boots `app.py` on an ephemeral port against a throwaway copy of the store, drives
every endpoint over real HTTP, asserts the safety properties, kills the server.

```
PASS  server boots and /healthz returns 200
PASS  GET / returns 200
PASS  page has both tabs
PASS  page states CANONICAL: NONE
PASS  page has no canonical form control
PASS  GET /static/style.css returns 200
PASS  GET /static/app.js returns 200
PASS  GET /healthz -> 200 ok
PASS  healthz reports CANONICAL NONE
PASS  source_document rows present
PASS  GET /api/meta -> 200
PASS  meta writable tables are conversation+message only
PASS  meta marks source_document read-only
PASS  meta count matches healthz
PASS  GET /api/codex/facets -> 200
PASS  facets expose statuses
PASS  facets expose corpus roots
PASS  no CANONICAL value exists in the data model
PASS  GET /api/codex/documents -> 200
PASS  document list respects limit
PASS  document list reports a total
PASS  listed document carries 'id' / 'rel_path' / 'status' / 'corpus_root_path' / 'probable_role'
PASS  GET document detail -> 200
PASS  document detail is flagged read_only
PASS  document detail includes a preview block
PASS  text preview is available for a real corpus file
PASS  text preview returns content
PASS  text preview is flagged read-only
PASS  text preview honours the 200KB cap
PASS  previewing a corpus file does not change its mtime
PASS  POST/PUT/PATCH/DELETE /api/codex/documents rejected (405)
PASS  PUT/PATCH/DELETE /api/codex/documents/<id> rejected (405)
PASS  no canonical elevation endpoint exists
PASS  GET /api/solace/conversations -> 200
PASS  conversation list is a list
PASS  POST create conversation -> 201
PASS  created conversation is WORKING
PASS  POST jd message -> 201
PASS  jd message role persisted
PASS  stub reply is appended and labelled WORKING
PASS  POST solace message -> 201
PASS  invalid message role rejected (400)
PASS  empty message body rejected (400)
PASS  conversation detail returns messages
PASS  messages are ordered by seq
PASS  both jd and solace messages persisted
PASS  conversation list grew by one
PASS  source_document rows were not mutated by any request
PASS  conversation row persisted to SQLite
PASS  message rows persisted to SQLite
PASS  unknown route -> 404
PASS  server process stopped

SMOKE UI PASSED — 61/61 checks
```

Exit code: **0**.

### Live server spot-check (`python3 app.py --port 8791`)

```
GET /healthz  -> ok:true, source_documents:935, conversations:0, canonical:"NONE"
GET /api/meta -> writable:[conversation,message], read_only:[source_document,corpus_root]
GET /api/codex/documents?limit=1 -> total:935
POST /api/solace/conversations   -> 201, id conv_…, status WORKING
```

The canary conversation created during this check was removed afterwards, so the
shipped store has `conversation=0`, `message=0`.

### Store build (`python3 setup_db.py`)

First build (Stage 3 then held 80 rows):

```
copied Stage 3 store -> data/codex_phase_i.sqlite
inventory entries : 966 (935 unique paths)
source_document   : 935 rows (+855 new, ~111 refreshed, sha256=808)
table counts      : {"corpus_root": 6, "source_document": 935, ...}
```

From-scratch rebuild (after the environment's own full-ingest, next section):

```
copied from stage3: True
inventory entries : 966 (935 unique paths)
source_document   : 935 rows (+0 new, ~966 refreshed, sha256=808)
```

Final shipped store: `source_document=935` (803 files, 132 directories), 803 rows
with `sha256`, 766 with non-empty `plurality_flags`, `conversation=0`, `message=0`.

### Corpus integrity

* No file under `/Users/archcore/solbian/codex` (excluding `.git/`) has an mtime
  after session start (`find … -newermt '2026-09-21 00:16:00'` → empty).
* `source_original/` newest mtime is `2026-02-20T12:06:29` — unchanged.
* `.git/` files carry mtime `00:09:26`, i.e. from environment setup *before* this
  session; no git command was run against the corpus during the session.
* Only read access occurred: `open(..., "rb")` for hashing, and capped `open(..., "rb")`
  previews.

### Environment note: the Stage 3 store changed *outside* Stage 4

At `00:18:51`, mid-session, the environment's own full-ingest ran against the
Stage 3 store directly. `ingest_full.log` records it:

```
db : /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite
source_documents : 935 (from 966 sample entries; sha256 computed=0)
```

The same instant, Stage 3's `baseline_inventory_full.json` was replaced (281 KB →
558 KB) with a version that carries **both** `entries` and `entries_sample`, which
is why the Stage 3 `ingest_baseline.py` then produced 935 rows where it had
previously produced 0 (and 80 total). This is the process that made the brief's
"~966 `source_document` rows already ingested" true — it happened after this
session began.

**No Stage 4 code wrote to the Stage 3 store.** A controlled probe
(`python3 setup_db.py --db data/probe.sqlite --no-sha256`) left Stage 3
byte-identical (`size=577536`, same `mtime_ns`), confirming `setup_db.py` only
ever reads its `--source`. Stage 4's working copy was then rebuilt from the
now-935-row Stage 3 store, so the two agree.

---

## Deviations and notes

1. **Working copy instead of the Stage 3 file in place.** The task asked to open
   the Stage 3 store read-write for conversations, but on this host the file
   sandbox denies writes outside the Stage 4 workspace (`touch` in the Stage 3
   directory → *Operation not permitted*). The brief explicitly permits the
   fallback "or copy into Stage 4 cwd", so `setup_db.py` makes
   `data/codex_phase_i.sqlite` and the app writes there. Running outside the
   sandbox, JD can point at Stage 3 directly with
   `python3 app.py --db /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite`.

2. **`source_document` settles at 935 rows, not 966.** The full inventory has 966
   entries but only 935 unique `rel_path` values (31 repeat), and
   `UNIQUE(corpus_root_id, rel_path)` collapses the repeats. At session start the
   Stage 3 store held only **80** rows (its ingest read the key `entries_sample`
   while the inventory's array is `entries`), so Stage 4's `setup_db.py` also
   completes the ingest into its working copy; the environment's own full-ingest
   later brought Stage 3 to the same 935. Setup is idempotent either way.

3. **Preview cap.** 200 KB, read-only, path-confined to a registered corpus root;
   binary (NUL-containing) and non-text media are metadata-only.

4. **Stub reply.** Optional; server-side, clearly prefixed `[WORKING STUB — not
   LLM-backed]`. A real Solace LLM remains Stage 5 and out of scope.

5. **`schema.sql`** was copied verbatim from Stage 3 into Stage 4 so the working
   copy is self-contained; it is unchanged DDL.

---

## Forbidden-item compliance

| Forbidden | Status |
| --- | --- |
| Modify historical corpus `/Users/archcore/solbian/codex` | **Not done** — read-only opens only; mtimes unchanged |
| CANONICAL controls / values | **Absent** — not in the enum, not offered by the UI, no endpoint (405) |
| Vector / graph / SEED / GOLEM / Machina | **Absent** — plain SQLite rows and one stdlib HTTP server |
| Heavy frameworks | **Absent** — Python stdlib + vanilla JS only |

---

## Reproduce from scratch

```bash
cd /Users/archcore/solbian/codex-phase-i-stage4
rm -f data/codex_phase_i.sqlite
python3 setup_db.py        # builds the working copy from Stage 3 (read-only)
python3 smoke_ui.py        # exit 0
python3 app.py             # http://127.0.0.1:8787/
```
