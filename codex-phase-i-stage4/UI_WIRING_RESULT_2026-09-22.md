# Stage 4 UI ↔ Stage 5b Hybrid Synthesis — Wiring Result (2026-09-22)

Narrowly approved Phase I slice: wire the Stage 4 living-store UI to the
Stage 5b hybrid synthesis engine with **explicit** deterministic (default) and
optional LLM actions, a **quiet** Engine proposal list, and the existing
one-at-a-time Accept → WORKING control.

**CANONICAL: NONE.** No `CANONICAL` value was written anywhere. Accept remains
one explicit user action per proposal, max status `WORKING`. No auto-Accept.
Raw Journey messages and provenance are preserved. No framework/dependency was
added (Python stdlib + vanilla JS/CSS only). No git commit/push was performed.

---

## Files changed

| File | Change |
| --- | --- |
| `app.py` | new `synthesize_dialogue()` helper + `SynthesizeError`; quiet default filtering (`hybrid:*`, `Theme:*` hidden) with `include_themes`/`all` flags; `POST /api/engine/synthesize` route; `--hybrid-py` flag, server attr, `/api/meta` exposure |
| `static/index.html` | Solace conversation view: `Synthesize dialogue` + `Draft with LLM` controls + result area; Engine quiet toggles (`Show Theme:*`, `Show all archaeology`); banner copy |
| `static/app.js` | `synthesizeDialogue()`/`synthResultHtml()`; LLM confirm; Engine stale flag + refresh on open; quiet flag params; toggle wiring; refresh WORKING list after Accept |
| `static/style.css` | styles for `.engine-actions`, `.checks`/`.check` |
| `smoke_ui.py` | focused RED-first checks: static controls, endpoint validation/result, quiet/widening filters, LLM fail-closed, explicit Accept + revision/provenance, preserved messages, live-DB hash; archaeology-specific existing checks opt in with `all=1`; robust source_document provenance check |
| `README.md` | Engine surface/API docs: synthesize endpoint, quiet default, explicit-write semantics |
| `UI_WIRING_RESULT_2026-09-22.md` | this report (new) |

## Backup location

Timestamped backup of every modified original, created **before** editing:

```
/Users/archcore/solbian/codex-phase-i-stage4/backup_20260922-020204/
├── app.py
├── smoke_ui.py
├── README.md
└── static/
    ├── app.js
    ├── index.html
    └── style.css
```

---

## RED evidence (checks added before production changes)

Command: `python3 smoke_ui.py`

```
SMOKE UI FAILED — 158/183 checks passed
```

All 25 failures were the expected missing endpoint / controls / filtering:

```
- page offers explicit hybrid synthesis controls
- page offers quiet Engine toggles (themes / all archaeology)
- app.js wires the hybrid synthesize endpoint and quiet flags
- default engine listing is quiet (hybrid:* only): rows=57
- POST /api/engine/synthesize without conversation_id -> 400: status=405
- synthesize rejects route-unsafe conversation_id -> 400: status=405
- synthesize unknown conversation -> 404: status=405
- POST /api/engine/synthesize (deterministic) -> 200: status=405
- synthesis reports deterministic mode: None
- synthesis reports llm_requested false
- synthesis returncode is 0: None
- synthesis reports CANONICAL NONE / no_canonical
- synthesis created new hybrid:deterministic PROPOSED rows: 405 error body
- synthesis ran against the server living DB
- hybrid:deterministic PROPOSED rows exist: count=0
- hybrid Theme:* rows exist (exercise the quiet filter): count=0
- hybrid provenance links resolve to target conversation messages: links=0 msgs=16
- default engine listing contains only hybrid:* rows
- include_themes=1 shows Theme:* rows
- include_themes=1 still restricts to hybrid:*
- POST /api/engine/synthesize (llm) -> 200 with deterministic floor: status=405
- LLM unreachable: fail closed (no false success): None
- LLM fail-closed kept the deterministic floor
- a hybrid:deterministic PROPOSED row is available to Accept: proposed=53
- (pre-existing fragility) engine provenance resolves to a source_document path: resolved=0
```

Full log: `/tmp/stage4_red.log`.

---

## GREEN evidence

### 1. Stage 4 full HTTP smoke — fail-closed LLM branch (default)

Command: `python3 smoke_ui.py`

```
SMOKE UI PASSED — 189/189 checks
```

Representative new checks:

```
PASS  page offers explicit hybrid synthesis controls
PASS  page offers quiet Engine toggles (themes / all archaeology)
PASS  POST /api/engine/synthesize (deterministic) -> 200
PASS  synthesis created new hybrid:deterministic PROPOSED rows
PASS  hybrid provenance links resolve to target conversation messages
PASS  default engine listing contains only hybrid:* rows
PASS  default engine listing hides Theme:* rows
PASS  include_themes=1 widens the quiet list
PASS  all=1 widens beyond hybrid (archaeology visible)
PASS  LLM unreachable: fail closed (no false success)
PASS  LLM unreachable: zero hybrid:llm rows written
PASS  explicit Accept of hybrid proposal -> 200
PASS  Accept produced a WORKING codex_document linked by revision
PASS  Accept copied provenance onto document/revision
PASS  raw Journey messages preserved byte-for-byte
PASS  living store after hybrid synthesis: no CANONICAL value anywhere
PASS  live Stage 4 living DB byte-identical (sha256 unchanged)
```

Full log: `/tmp/stage4_green_final.log`.

### 2. Stage 4 full HTTP smoke — reachable LLM branch (engine mock)

Command: `SOLBIAN_LLM_MOCK=1 python3 smoke_ui.py`

```
SMOKE UI PASSED — 187/187 checks
PASS  LLM reachable: hybrid:llm PROPOSED created
```

(The count is lower because the fail-closed branch has three LLM assertions vs
one for the reachable branch.) Full log: `/tmp/stage4_green_mock.log`.

### 3. Hybrid package smoke

Command: `cd /Users/archcore/solbian/codex-phase-i-stage5/codex-phase-i-stage5b-hybrid && python3 smoke_hybrid.py`

```
Results: ['PASS','PASS','PASS','PASS','PASS','PASS','PASS','PASS','PASS','PASS']
OVERALL: PASS
```

### 4. Independent reachable-LLM HTTP probe (ad-hoc, mock)

```
HTTP_STATUS 200
llm_requested True llm_drafted True
new_hybrid_llm_proposals 1 new_hybrid_proposals 55
no_canonical True canonical NONE auto_accepted False
db_hybrid_llm 1 db_hybrid_deterministic 54
PROBE_OK True
live_db_unchanged True
```

---

## Observed counts (throwaway copy of the living store, target `conv_5bbf3990a8ce4b47`)

| Quantity | Value |
| --- | --- |
| Deterministic synthesis (first call) | **54** `hybrid:deterministic` PROPOSED (13 non-theme + 41 `Theme:*`) |
| Default quiet list | 13 hybrid rows, **0** `Theme:*`, **0** `engine:stage5:*` |
| `include_themes=1` | 54 hybrid rows (themes now visible) |
| `all=1` | 111 rows (54 hybrid + 57 `engine:stage5:*` archaeology) |
| LLM unreachable | 0 `hybrid:llm` written, deterministic floor kept, error reported |
| LLM reachable (mock) | 1 `hybrid:llm` PROPOSED |
| Explicit Accept | 1 proposal → `WORKING` + `revision` + provenance copied |
| `CANONICAL` values/writes | **0** |

## Live DB integrity

The real Stage 4 living store was never passed to a writer; every test ran
against a throwaway copy in a temp dir (the smoke test copies
`data/codex_phase_i.sqlite`, boots the server with `--db <tmp>`, and the
synthesize endpoint always passes the server's own DB path).

| | SHA-256 |
| --- | --- |
| `data/codex_phase_i.sqlite` before | `727d9ef1c9aee4452f1dff4b5710852d294c57a3a4ab0cab4cfa9f46eabaa9b0` |
| `data/codex_phase_i.sqlite` after | `727d9ef1c9aee4452f1dff4b5710852d294c57a3a4ab0cab4cfa9f46eabaa9b0` |
| Stage 3 SoT store | unchanged (asserted) |
| Historical corpus `/Users/archcore/solbian/codex` | fingerprint unchanged (asserted) |

### Commands run

```bash
cd /Users/archcore/solbian/codex-phase-i-stage4
python3 smoke_ui.py                                   # 189/189 PASS (fail-closed)
SOLBIAN_LLM_MOCK=1 python3 smoke_ui.py                # 187/187 PASS (reachable/mock)
cd /Users/archcore/solbian/codex-phase-i-stage5/codex-phase-i-stage5b-hybrid
python3 smoke_hybrid.py                               # OVERALL PASS
shasum -a 256 /Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite
```

---

## API / UI summary

* `POST /api/engine/synthesize` `{conversation_id, llm: false}` — route-safe id
  validation (`[A-Za-z0-9_-]{1,128}`), DB existence check, argv list
  (`shell=False`), explicit cwd, timeout, captured output, always
  `--db <server living DB>`. Returns `returncode`, `stdout`/`stderr`, `mode`,
  `llm_requested`/`llm_drafted`/`llm_error`, before/after/new proposal counts,
  `no_canonical`, `canonical: "NONE"`. Non-zero → **503**, timeout → **504** —
  never a false success.
* Solace conversation view: **Synthesize dialogue** (deterministic, default) and
  **Draft with LLM** (explicit `confirm()`, fails closed). Success marks the
  Engine list stale and it refreshes when opened.
* Engine list quiet by default (`hybrid:*`, no `Theme:*`), widened by
  `include_themes=1` / `all=1` checkboxes, preserving search/status/pagination.
* Accept remains visible only for `PROPOSED`; after Accept the proposal and
  WORKING lists refresh.

## Remaining caveats

* **Pre-existing test fragility fixed (not a behavior change).**
  `engine provenance resolves to a source_document path` assumed the newest
  proposal was source_document-linked. The current live DB's newest rows are
  message-linked `durable` candidates, so the check now selects a proposal the
  DB records as `source_document`-linked. It was already failing before this
  slice on the current live DB.
* Existing checks that deliberately target non-hybrid archaeology
  (`engine:stage5:*`) now pass `all=1`, because the quiet default hides them.
  This is intended behavior.
* Quiet filtering applies the hybrid/`Theme:*` clauses together with any selected
  `status`; use `all=1` to include `engine:stage5:*` `WORKING` rows.
* On an unreachable LLM the endpoint returns **200** with `llm_drafted: false`
  and a populated `llm_error` (the deterministic floor succeeded); the UI shows
  an "LLM failed closed" warning and the engine error, never a false success.
* The hybrid engine status/staging copy used is
  `/Users/archcore/solbian/codex-phase-i-stage5/codex-phase-i-stage5b-hybrid/engine.py`
  (overridable via `--hybrid-py` / `SOLBIAN_HYBRID_PY`).
* `SOLBIAN_LLM_SMOKE=1` opts the smoke test into a real configured endpoint
  instead of the deterministic fail-closed path; `SOLBIAN_LLM_MOCK=1` uses the
  engine's deterministic mock LLM.
