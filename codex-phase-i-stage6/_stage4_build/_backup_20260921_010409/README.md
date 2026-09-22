# Codex Solbian — Phase I · Stage 4 Two-Surface Prototype

A minimal local web UI over the Stage 3 SQLite store, with exactly two surfaces:

| Surface | Access | What it does |
| --- | --- | --- |
| **Solace** | read **+ write** `conversation` / `message` only | list conversations, open one, read messages, create a conversation, append a message as `jd` or `solace` (optional clearly-labelled `WORKING` stub reply) |
| **Codex Solbian** | **read-only** `source_document` | browse/filter the corpus index (path, status, role, media, root), see full metadata, and — where a local text file exists under a registered corpus root — read a capped 200 KB preview |

**CANONICAL: NONE.** The data model has no canonical value and the UI exposes no
"make canonical" control. The historical corpus is never written to.

Python standard library only (`http.server` + `sqlite3` + vanilla JS). No Flask,
no vector DB, no graph DB, no microservices, no SEED/GOLEM/Machina coupling.

---

## Run it

```bash
cd /Users/archcore/solbian/codex-phase-i-stage4
python3 app.py
# -> http://127.0.0.1:8787/
```

Useful flags:

```bash
python3 app.py --port 9000              # different port
python3 app.py --verbose                # per-request logging
python3 app.py --db /path/to/other.sqlite
SOLBIAN_DB=/path/to/other.sqlite python3 app.py
```

Then open the printed URL and switch between the **Solace** and **Codex Solbian**
tabs. The server stays in the foreground; `Ctrl-C` stops it.

### Verify (must exit 0)

```bash
python3 smoke_ui.py
```

It boots `app.py` on an ephemeral port against a throwaway copy of the store,
drives every endpoint over real HTTP, asserts the read-only guarantees, kills the
server, and exits `0` only if all checks pass.

---

## The store

```
data/codex_phase_i.sqlite      # Stage 4 working copy (created by setup_db.py)
```

`app.py` operates on a **local working copy** of the Stage 3 store, built once by
`setup_db.py`:

```bash
python3 setup_db.py                     # copy Stage 3 store + complete the ingest
python3 setup_db.py --force             # re-copy from Stage 3 first
python3 setup_db.py --no-sha256         # never open corpus files
```

Why a copy? Stage 4 must write conversations, and on this host the sandbox only
permits writes inside the Stage 4 workspace; the brief explicitly allows
"or copy into Stage 4 cwd". The Stage 3 store is opened **read-only** for the
copy and is left byte-for-byte untouched.

To run directly against the Stage 3 store instead (e.g. on JD's Mac where the
sibling path is writable):

```bash
python3 app.py --db /Users/archcore/solbian/codex-phase-i-stage3/codex_phase_i.sqlite
```

### What `setup_db.py` did

1. Copied the Stage 3 store (`codex_phase_i.sqlite`) into `data/`.
2. Applied the (idempotent) schema.
3. Topped up `source_document` from `baseline_inventory_full.json`, read-only.
   The full inventory has 966 entries but only 935 unique paths (31 repeat), and
   `UNIQUE(corpus_root_id, rel_path)` collapses the repeats, so the copy settles
   at **935 rows**. This step is idempotent: it is a no-op whether the copied
   Stage 3 store already holds the full index or only the 80-row sample.
4. Computed read-only `sha256` for 808 corpus files (files only, ≤ 20 MB, opened
   `"rb"` and never written).

Corpus access is exclusively read-only. No file under `/Users/archcore/solbian/codex`
is ever created, modified, moved or deleted.

---

## HTTP API

### Solace (writable: `conversation`, `message`)

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/solace/conversations` | list conversations + message counts |
| `POST` | `/api/solace/conversations` | create `{title, participants, notes}` (status fixed `WORKING`) |
| `GET` | `/api/solace/conversations/<id>` | conversation + ordered messages |
| `POST` | `/api/solace/conversations/<id>/messages` | append `{role: "jd"\|"solace", body, stub_reply?}` |

`stub_reply: true` on a `jd` message appends a placeholder `solace` message whose
body begins `[WORKING STUB — not LLM-backed]`. A real Solace engine is Stage 5 and
out of scope.

### Codex (read-only)

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/codex/documents` | list/filter: `q`, `status`, `role`, `media`, `root`, `limit`, `offset` |
| `GET` | `/api/codex/documents/<id>` | metadata + optional capped text preview |
| `GET` | `/api/codex/facets` | status / role / media / corpus-root counts |
| `GET` | `/api/codex/roots` | registered corpus roots |

Every non-`GET` method under `/api/codex/` returns **405** — there is no mutation
endpoint, no edit control, and no canonical elevation.

### Misc

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | the single-page two-tab UI |
| `GET` | `/healthz` | liveness + row counts |
| `GET` | `/api/meta` | store path, counts, writable/read-only tables, `canonical: NONE` |

### Preview rules

A preview is served only when all of these hold; otherwise the pane reports the
reason and shows metadata only:

* the document's corpus root is a real local directory (not a `CANDIDATE:` pointer);
* the resolved path stays inside that root (no `..` escape);
* the target is a regular file;
* the media type / extension is a text surface;
* the first bytes contain no NUL (binary files are refused);
* at most 200 KB is read (`truncated` is flagged when the file is larger).

The file is opened `"rb"` and only read — mtime is unchanged (asserted by the smoke
test).

---

## Files

| File | Purpose |
| --- | --- |
| `app.py` | stdlib HTTP server + API (the whole backend) |
| `static/index.html` | the two-tab shell |
| `static/app.js` | Solace + Codex client logic (vanilla JS) |
| `static/style.css` | calm, content-first styling |
| `setup_db.py` | build the Stage 4 working copy + complete the ingest |
| `schema.sql` | executable DDL (copied from Stage 3, unchanged) |
| `smoke_ui.py` | end-to-end HTTP smoke test (`exit 0`) |
| `data/codex_phase_i.sqlite` | the working store |
| `baseline_inventory_full.json` | full Stage 2 inventory (read-only input) |
| `README.md`, `DSH_RESULT.md` | docs |

---

## Guarantees

* **No corpus writes.** Nothing in this tree writes under `/Users/archcore/solbian/codex`.
* **Codex is read-only.** No code path inserts/updates/deletes `source_document`.
* **No CANONICAL.** The enum has no such value; the UI never offers one.
* **Plurality preserved.** `status`, verbatim `inventory_status` and
  `plurality_flags` are shown as-is; nothing is merged or flattened.
* **Historical SoT remains** `/Users/archcore/solbian/codex`; the store holds
  pointers and conversations, never replacements.
