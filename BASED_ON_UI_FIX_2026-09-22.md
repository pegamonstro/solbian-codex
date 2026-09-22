# based_on UI fix — 2026-09-22

Hybrid (and LLM) proposals store `based_on` as a JSON **object**
`{message_ids, engine, note}`, while Stage 5 plurality/etc. rows historically
used an **array**. `static/app.js` called `(p.based_on || []).join(...)`, which
throws when `based_on` is an object.

Fix: `formatBasedOn()` handles array / object / scalar. Backup of prior JS:
`backup_20260922-based-on-fix/app.js`. Hard-refresh the browser.
