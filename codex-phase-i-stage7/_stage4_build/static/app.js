/* Codex Solbian — Phase I · Stage 4 UI + Stage 7 living loop (vanilla JS, no framework). */
'use strict';

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => (
  { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
));

const shortTime = (iso) => (iso ? String(iso).replace('T', ' ').slice(0, 16) : '—');
const shortPath = (p, n = 46) => {
  const s = String(p || '');
  return s.length <= n ? s : '…' + s.slice(-(n - 1));
};
const fmtBytes = (n) => {
  if (n == null) return '—';
  if (n < 1024) return n + ' B';
  if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';
  return (n / 1048576).toFixed(2) + ' MB';
};

const api = {
  async get(path) {
    const r = await fetch(path, { headers: { Accept: 'application/json' } });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(d.error || r.status + ' ' + r.statusText);
    return d;
  },
  async post(path, body) {
    const r = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {}),
    });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(d.error || r.status + ' ' + r.statusText);
    return d;
  },
};

function showError(sel, err) {
  const el = $(sel);
  if (!el) { console.error(err); return; }
  el.textContent = err && err.message ? err.message : String(err);
  el.classList.remove('hidden');
}
function clearError(sel) {
  const el = $(sel);
  if (el) el.classList.add('hidden');
}

const state = {
  convId: null,
  codex: {
    limit: 50, offset: 0, total: 0, docId: null, loaded: false,
    mode: 'working',
    cdLimit: 25, cdOffset: 0, cdTotal: 0, cdId: null,
  },
  engine: { limit: 50, offset: 0, total: 0, propId: null, loaded: false },
};

/* ============================ TABS ============================ */
function selectTab(name) {
  $$('.tab').forEach((b) => {
    const on = b.dataset.tab === name;
    b.classList.toggle('active', on);
    b.setAttribute('aria-selected', on ? 'true' : 'false');
  });
  $$('.panel').forEach((p) => p.classList.add('hidden'));
  const panel = document.getElementById('tab-' + name);
  if (panel) panel.classList.remove('hidden');
  if (name === 'codex' && !state.codex.loaded) {
    state.codex.loaded = true;
    loadCodex();
    loadCodexWorking();
    setCodexMode(state.codex.mode);
  }
  if (name === 'engine' && !state.engine.loaded) {
    state.engine.loaded = true;
    loadEngine();
  }
}

/* ============================ SOLACE ============================ */
async function loadConversations() {
  try {
    const data = await api.get('/api/solace/conversations');
    renderConvList(data.conversations || []);
  } catch (err) {
    $('#convEmpty').textContent = 'Could not load conversations: ' + err.message;
  }
}

function renderConvList(convs) {
  const ul = $('#convList');
  ul.innerHTML = '';
  const emptyNote = $('#convEmpty');
  emptyNote.classList.toggle('hidden', convs.length > 0);
  if (!convs.length) emptyNote.textContent = 'No conversations yet — create one.';
  convs.forEach((c) => {
    const li = document.createElement('li');
    if (c.id === state.convId) li.classList.add('active');
    li.innerHTML =
      '<div class="title">' + esc(c.title) + '</div>' +
      '<div class="meta">' + (c.message_count || 0) + ' message' + (c.message_count === 1 ? '' : 's') +
      ' · ' + esc(c.status) + ' · ' + esc(shortTime(c.updated_at || c.created_at)) + '</div>';
    li.addEventListener('click', () => openConversation(c.id));
    ul.appendChild(li);
  });
}

async function openConversation(id) {
  try {
    const data = await api.get('/api/solace/conversations/' + encodeURIComponent(id));
    state.convId = id;
    renderConversation(data.conversation);
    $$('#convList li').forEach((li) => li.classList.remove('active'));
    loadConversations();
  } catch (err) {
    $('#convView').classList.remove('empty');
    $('#convView').innerHTML = '<div class="error">Could not open conversation: ' + esc(err.message) + '</div>';
  }
}

function renderConversation(conv) {
  const view = $('#convView');
  view.classList.remove('empty');
  const msgs = conv.messages || [];
  const msgHtml = msgs.length
    ? msgs.map((m) => (
        '<li class="role-' + esc(m.role || 'other') + '">' +
          '<div class="mhead"><span class="role">' + esc(m.role || '?') + '</span>' +
          ' · seq ' + esc(m.seq) + ' · ' + esc(shortTime(m.sent_at || m.created_at)) +
          ' · ' + esc(m.status) + '</div>' +
          '<div class="body">' + esc(m.body) + '</div>' +
        '</li>'
      )).join('')
    : '<li class="empty" style="border:none;background:none">No messages yet.</li>';

  view.innerHTML =
    '<div class="card">' +
      '<h2>' + esc(conv.title) + '</h2>' +
      '<div class="meta">conversation ' + esc(conv.id) + ' · status ' + esc(conv.status) +
        ' · participants ' + esc((conv.participants_list || []).join(', ') || '—') +
        ' · started ' + esc(shortTime(conv.started_at)) + '</div>' +
      (conv.notes ? '<div class="note">' + esc(conv.notes) + '</div>' : '') +
      '<div class="section-title">Messages <span class="hint">' + msgs.length + '</span></div>' +
      '<ol class="messages" id="msgList">' + msgHtml + '</ol>' +
      '<form id="msgForm" autocomplete="off">' +
        '<label for="msgRole">Role</label>' +
        '<select id="msgRole"><option value="jd">jd</option><option value="solace">solace</option></select>' +
        '<label for="msgBody">Message</label>' +
        '<textarea id="msgBody" placeholder="Write as jd…" required></textarea>' +
        '<label style="display:flex;gap:8px;align-items:center;margin-top:10px;font-size:12px;color:var(--ink-soft)">' +
          '<input type="checkbox" id="msgStub" style="width:auto"> append a WORKING stub Solace reply</label>' +
        '<div class="btn-row"><button class="btn small" type="submit">Append message</button>' +
          '<span class="note">Persists to <code>message</code> only.</span></div>' +
        '<div class="error hidden" id="msgError"></div>' +
      '</form>' +
    '</div>';

  const list = $('#msgList');
  if (list) list.scrollTop = list.scrollHeight;
  $('#msgForm').addEventListener('submit', sendMessage);
}

async function sendMessage(ev) {
  ev.preventDefault();
  clearError('#msgError');
  const role = $('#msgRole').value;
  const body = $('#msgBody').value.trim();
  if (!body) { showError('#msgError', new Error('Message body is empty.')); return; }
  const stub = $('#msgStub').checked;
  try {
    const data = await api.post('/api/solace/conversations/' + encodeURIComponent(state.convId) + '/messages',
      { role, body, stub_reply: stub });
    state.engine.loaded = false;         // proposals may have changed
    await openConversation(state.convId);
    const loop = data && data.living_loop;
    if (loop) {
      const note = document.createElement('div');
      note.className = 'layer-note';
      note.textContent = loop.ran === false
        ? 'Living loop did not run: ' + (loop.error || 'unknown error')
        : 'Living loop ran (' + (loop.kinds || []).join(', ') + '): proposals '
          + loop.proposals_before + ' → ' + loop.proposals_after
          + ' (new ' + loop.new_proposals + '). Review and accept in the Engine tab.';
      $('#convView').prepend(note);
    }
  } catch (err) {
    showError('#msgError', err);
  }
}

async function createConversation(ev) {
  ev.preventDefault();
  clearError('#newConvError');
  const title = $('#convTitle').value.trim();
  const participants = $('#convParticipants').value.trim();
  const notes = $('#convNotes').value.trim();
  try {
    const data = await api.post('/api/solace/conversations', { title, participants, notes });
    $('#newConvForm').reset();
    $('#convParticipants').value = 'jd, solace';
    $('#newConvForm').classList.add('hidden');
    await loadConversations();
    await openConversation(data.conversation.id);
  } catch (err) {
    showError('#newConvError', err);
  }
}

/* ============================ CODEX ============================ */
async function loadCodex() {
  try {
    const facets = await api.get('/api/codex/facets');
    fillSelect('#fstatus', (facets.statuses || []).map((x) => ({ value: x.value, label: x.value + ' (' + x.count + ')' })));
    fillSelect('#frole', (facets.roles || []).map((x) => ({ value: x.value, label: x.value + ' (' + x.count + ')' })));
    fillSelect('#fmedia', (facets.media_types || []).map((x) => ({ value: x.value, label: x.value + ' (' + x.count + ')' })));
    fillSelect('#froot', (facets.corpus_roots || []).map((r) => ({ value: r.id, label: shortPath(r.path, 40) + ' (' + r.document_count + ')' })));
    fillSelect('#cdkind', (facets.codex_kinds || []).map((x) => ({ value: x.value, label: x.value + ' (' + x.count + ')' })));
  } catch (err) {
    $('#docCount').textContent = 'facets failed';
  }
  loadDocuments();
}

function updateLayerNote() {
  const note = $('#codexLayerNote');
  if (note) {
    note.textContent = 'Living store layers — WORKING codex_document: '
      + (state.codex.cdTotal || 0)
      + ' · HISTORICAL source_document: ' + (state.codex.total || 0);
  }
}

function fillSelect(sel, options) {
  const el = $(sel);
  const current = el.value;
  el.innerHTML = '<option value="">all</option>' +
    options.map((o) => '<option value="' + esc(o.value) + '">' + esc(o.label) + '</option>').join('');
  if (options.some((o) => o.value === current)) el.value = current;
}

function codexQuery() {
  const params = new URLSearchParams();
  const q = $('#fq').value.trim();
  if (q) params.set('q', q);
  ['status', 'role', 'media', 'root'].forEach((f) => {
    const v = $('#f' + f).value;
    if (v) params.set(f, v);
  });
  params.set('limit', state.codex.limit);
  params.set('offset', state.codex.offset);
  return params.toString();
}

async function loadDocuments() {
  try {
    const data = await api.get('/api/codex/documents?' + codexQuery());
    state.codex.total = data.total;
    renderDocList(data.documents || []);
    updatePager(data.documents ? data.documents.length : 0);
  } catch (err) {
    $('#docList').innerHTML = '<li class="error">Could not load documents: ' + esc(err.message) + '</li>';
  }
}

function renderDocList(docs) {
  const ul = $('#docList');
  ul.innerHTML = docs.length ? '' : '<li class="empty">No matching documents.</li>';
  docs.forEach((d) => {
    const li = document.createElement('li');
    if (d.id === state.codex.docId) li.classList.add('active');
    let flags = '';
    try {
      const arr = JSON.parse(d.plurality_flags || '[]');
      if (arr.length) flags = ' · ' + arr.join(', ');
    } catch (e) { /* ignore */ }
    li.innerHTML =
      '<div class="path">' + esc(d.rel_path) + '</div>' +
      '<div class="meta">' + esc(d.status) + ' · ' + esc(d.probable_role || 'UNKNOWN') +
      ' · ' + fmtBytes(d.byte_size) + ' · ' + esc(d.media_type || '—') + esc(flags) + '</div>';
    li.addEventListener('click', () => openDocument(d.id));
    ul.appendChild(li);
  });
}

function updatePager(shown) {
  const total = state.codex.total;
  const start = total ? state.codex.offset + 1 : 0;
  const end = state.codex.offset + shown;
  $('#docCount').textContent = total + ' document' + (total === 1 ? '' : 's');
  $('#pageLabel').textContent = total ? (start + '–' + end + ' of ' + total) : '0 of 0';
  $('#prevPage').disabled = state.codex.offset <= 0;
  $('#nextPage').disabled = state.codex.offset + shown >= total;
  updateLayerNote();
}

async function openDocument(id) {
  try {
    const data = await api.get('/api/codex/documents/' + encodeURIComponent(id));
    state.codex.docId = id;
    renderDocument(data.document);
    $$('#docList li').forEach((li) => li.classList.remove('active'));
    loadDocuments();
  } catch (err) {
    $('#docView').classList.remove('empty');
    $('#docView').innerHTML = '<div class="error">Could not open document: ' + esc(err.message) + '</div>';
  }
}

function metaRow(label, value, mono) {
  return '<dt>' + esc(label) + '</dt><dd' + (mono ? ' class="mono"' : '') + '>' + esc(value == null || value === '' ? '—' : value) + '</dd>';
}

function renderDocument(doc) {
  const view = $('#docView');
  view.classList.remove('empty');

  let flags = doc.plurality_flags;
  try {
    const arr = JSON.parse(flags || '[]');
    flags = arr.length ? arr.join(', ') : '—';
  } catch (e) { /* keep raw */ }

  const preview = doc.preview || { available: false, reason: 'no preview computed' };
  let previewHtml;
  if (preview.available) {
    const shown = preview.bytes_shown;
    const hint = 'read-only · ' + fmtBytes(shown) + ' of ' + fmtBytes(preview.size) +
      (preview.truncated ? ' · truncated at ' + fmtBytes(preview.cap) : '');
    previewHtml =
      '<div class="section-title">Text preview <span class="hint">' + esc(hint) + '</span></div>' +
      '<div class="mono" style="margin-bottom:6px;color:var(--ink-faint)">' + esc(preview.abs_path) + '</div>' +
      '<pre class="preview">' + esc(preview.text) + '</pre>';
  } else {
    previewHtml =
      '<div class="section-title">Text preview <span class="hint">not available</span></div>' +
      '<div class="note">' + esc(preview.reason || 'unavailable') +
      (preview.abs_path ? '<br><span class="mono">' + esc(preview.abs_path) + '</span>' : '') + '</div>';
  }

  view.innerHTML =
    '<div class="card">' +
      '<div class="panel-head"><h2>Document</h2><span class="badge badge-ok">read-only</span></div>' +
      '<dl class="meta-grid">' +
        metaRow('id', doc.id, true) +
        metaRow('rel_path', doc.rel_path, true) +
        metaRow('corpus root', doc.corpus_root_path, true) +
        metaRow('root class', doc.corpus_classification) +
        metaRow('media_type', doc.media_type) +
        metaRow('byte_size', doc.byte_size == null ? '—' : fmtBytes(doc.byte_size)) +
        metaRow('mtime', doc.mtime) +
        metaRow('sha256', doc.sha256, true) +
        metaRow('probable_role', doc.probable_role) +
        metaRow('inventory_status', doc.inventory_status) +
        metaRow('status', doc.status) +
        metaRow('plurality_flags', flags) +
        metaRow('attribution', doc.attribution) +
        metaRow('notes', doc.notes) +
        metaRow('created_at', doc.created_at) +
        metaRow('updated_at', doc.updated_at) +
      '</dl>' +
      previewHtml +
    '</div>';
}

/* ---- WORKING codex_document layer (Stage 7) ---- */
function setCodexMode(mode) {
  state.codex.mode = mode;
  $$('.seg').forEach((b) => b.classList.toggle('active', b.dataset.mode === mode));
  const working = mode === 'working';
  $('#codexWorkingPane').classList.toggle('hidden', !working);
  $('#codexHistoricalPane').classList.toggle('hidden', working);
  updateLayerNote();
}

function codexDocQuery() {
  const params = new URLSearchParams();
  const q = $('#cdq').value.trim();
  if (q) params.set('q', q);
  const k = $('#cdkind').value;
  if (k) params.set('kind', k);
  params.set('limit', state.codex.cdLimit);
  params.set('offset', state.codex.cdOffset);
  return params.toString();
}

async function loadCodexWorking() {
  try {
    const data = await api.get('/api/codex/codex-documents?' + codexDocQuery());
    state.codex.cdTotal = data.total;
    renderCodexDocList(data.codex_documents || []);
    updateCodexPager((data.codex_documents || []).length);
  } catch (err) {
    $('#codexDocList').innerHTML = '<li class="error">Could not load WORKING documents: ' + esc(err.message) + '</li>';
  }
}

function renderCodexDocList(docs) {
  const ul = $('#codexDocList');
  ul.innerHTML = docs.length ? '' : '<li class="empty">No WORKING codex_document rows yet. Accept a PROPOSED proposal in the Engine tab.</li>';
  docs.forEach((d) => {
    const li = document.createElement('li');
    if (d.id === state.codex.cdId) li.classList.add('active');
    li.innerHTML =
      '<div class="path">' + esc(d.title || d.id) + '</div>' +
      '<div class="meta"><span class="pill pill-working">' + esc(d.status) + '</span> ' +
      esc(d.kind || 'other') + ' · v' + esc(d.version) +
      ' · prov ' + (d.provenance_count || 0) + ' · ' + esc(shortTime(d.updated_at)) + '</div>';
    li.addEventListener('click', () => openCodexDocument(d.id));
    ul.appendChild(li);
  });
}

function updateCodexPager(shown) {
  const total = state.codex.cdTotal || 0;
  const start = total ? state.codex.cdOffset + 1 : 0;
  const end = state.codex.cdOffset + shown;
  $('#codexDocCount').textContent = total + ' WORKING document' + (total === 1 ? '' : 's');
  $('#cdPage').textContent = total ? (start + '–' + end + ' of ' + total) : '0 of 0';
  $('#cdPrev').disabled = state.codex.cdOffset <= 0;
  $('#cdNext').disabled = state.codex.cdOffset + shown >= total;
  updateLayerNote();
}

async function openCodexDocument(id) {
  try {
    const data = await api.get('/api/codex/codex-documents/' + encodeURIComponent(id));
    state.codex.cdId = id;
    renderCodexDocument(data.codex_document);
    $$('#codexDocList li').forEach((li) => li.classList.remove('active'));
    loadCodexWorking();
  } catch (err) {
    $('#codexDocView').classList.remove('empty');
    $('#codexDocView').innerHTML = '<div class="error">Could not open WORKING document: ' + esc(err.message) + '</div>';
  }
}

function renderCodexDocument(doc) {
  const view = $('#codexDocView');
  view.classList.remove('empty');
  const prov = doc.provenance || [];
  const provHtml = prov.length
    ? prov.map((v) => {
        const target = v.source_rel_path
          ? esc(v.source_rel_path)
          : esc((v.source_kind || 'unknown') + ':' + (v.source_id || '—'));
        return '<li><span class="mono">' + esc(v.source_kind) + '</span> · ' + target +
          ' <span class="hint">[' + esc(v.confidence || '—') + '/' + esc(v.status || '—') + ']</span>' +
          (v.note ? '<div class="note">' + esc(v.note) + '</div>' : '') + '</li>';
      }).join('')
    : '<li class="empty">No provenance links.</li>';
  const revs = doc.revisions || [];
  const revHtml = revs.length
    ? revs.map((r) => '<li class="mono">' + esc(r.id) + ' · proposal ' + esc(r.proposal_id || '—') +
        ' · v' + esc(r.prev_version) + '→v' + esc(r.next_version) +
        ' <span class="hint">[' + esc(r.status) + ']</span>' +
        (r.diff_summary ? '<div class="note">' + esc(r.diff_summary) + '</div>' : '') + '</li>').join('')
    : '<li class="empty">No revision recorded.</li>';

  view.innerHTML =
    '<div class="card">' +
      '<div class="panel-head"><h2>' + esc(doc.title || doc.id) + '</h2>' +
        '<span class="badge badge-working">status ' + esc(doc.status) + '</span></div>' +
      '<dl class="meta-grid">' +
        metaRow('id', doc.id, true) +
        metaRow('kind', doc.kind) +
        metaRow('status', doc.status) +
        metaRow('version', doc.version) +
        metaRow('source_document_id', doc.source_document_id || '—', true) +
        metaRow('attribution', doc.attribution, true) +
        metaRow('created_at', doc.created_at) +
        metaRow('updated_at', doc.updated_at) +
      '</dl>' +
      '<div class="section-title">Body <span class="hint">consolidated WORKING content — read-only here</span></div>' +
      '<pre class="preview">' + esc(doc.body || '(no body)') + '</pre>' +
      '<div class="section-title">Revision <span class="hint">' + revs.length + '</span></div>' +
      '<ul class="messages">' + revHtml + '</ul>' +
      '<div class="section-title">Provenance <span class="hint">' + prov.length + '</span></div>' +
      '<ul class="messages">' + provHtml + '</ul>' +
    '</div>';
}

/* ============================ ENGINE ============================ */
async function loadEngine() {
  try {
    const meta = await api.get('/api/engine/meta');
    const statuses = meta.proposal_statuses || [];
    fillSelect('#estatus', statuses.map((s) => ({ value: s, label: s })));
    const badge = $('#dbBadge');
    if (badge && meta.exists) {
      badge.title = (badge.title || '') + '\nengine store: ' + meta.engine_db +
        '\nproposals: ' + ((meta.counts || {}).proposal || 0) + '\nCANONICAL: ' + (meta.canonical || 'NONE');
    }
  } catch (err) {
    $('#propCount').textContent = 'engine meta failed';
  }
  loadProposals();
}

function engineQuery() {
  const params = new URLSearchParams();
  const q = $('#eq').value.trim();
  if (q) params.set('q', q);
  const s = $('#estatus').value;
  if (s) params.set('status', s);
  params.set('limit', state.engine.limit);
  params.set('offset', state.engine.offset);
  return params.toString();
}

async function loadProposals() {
  try {
    const data = await api.get('/api/engine/proposals?' + engineQuery());
    state.engine.total = data.total;
    renderProposalList(data.proposals || []);
    updatePropPager(data.proposals ? data.proposals.length : 0);
  } catch (err) {
    $('#propList').innerHTML = '<li class="error">Could not load proposals: ' + esc(err.message) + '</li>';
  }
}

function renderProposalList(props) {
  const ul = $('#propList');
  ul.innerHTML = props.length ? '' : '<li class="empty">No matching proposals.</li>';
  props.forEach((p) => {
    const li = document.createElement('li');
    if (p.id === state.engine.propId) li.classList.add('active');
    li.innerHTML =
      '<div class="path">' + esc(p.summary || p.id) + '</div>' +
      '<div class="meta">' + esc(p.status) + ' · prov ' + (p.provenance_count || 0) +
      ' · ' + esc(shortTime(p.created_at)) + ' · ' + esc(shortPath(p.id, 30)) + '</div>';
    li.addEventListener('click', () => openProposal(p.id));
    ul.appendChild(li);
  });
}

function updatePropPager(shown) {
  const total = state.engine.total;
  const start = total ? state.engine.offset + 1 : 0;
  const end = state.engine.offset + shown;
  $('#propCount').textContent = total + ' proposal' + (total === 1 ? '' : 's');
  $('#propPage').textContent = total ? (start + '–' + end + ' of ' + total) : '0 of 0';
  $('#propPrev').disabled = state.engine.offset <= 0;
  $('#propNext').disabled = state.engine.offset + shown >= total;
}

async function openProposal(id) {
  try {
    const data = await api.get('/api/engine/proposals/' + encodeURIComponent(id));
    state.engine.propId = id;
    renderProposal(data.proposal);
    $$('#propList li').forEach((li) => li.classList.remove('active'));
    loadProposals();
  } catch (err) {
    $('#propView').classList.remove('empty');
    $('#propView').innerHTML = '<div class="error">Could not open proposal: ' + esc(err.message) + '</div>';
  }
}

function renderProposal(p) {
  const view = $('#propView');
  view.classList.remove('empty');

  const prov = p.provenance || [];
  const provHtml = prov.length
    ? prov.map((v) => {
        const target = v.source_rel_path
          ? esc(v.source_rel_path)
          : esc((v.source_kind || 'unknown') + ':' + (v.source_id || '—'));
        return '<li><span class="mono">' + esc(v.source_kind) + '</span> · ' + target +
          ' <span class="hint">[' + esc(v.confidence || '—') + '/' + esc(v.status || '—') + ']</span>' +
          (v.note ? '<div class="note">' + esc(v.note) + '</div>' : '') + '</li>';
      }).join('')
    : '<li class="empty">No provenance links.</li>';

  const rels = p.relationships || [];
  const relHtml = rels.length
    ? rels.map((r) => '<li class="mono">' + esc(r.from_kind) + ':' + esc(r.from_id) +
        ' --' + esc(r.rel_type) + '--> ' + esc(r.to_kind) + ':' + esc(r.to_id) +
        ' <span class="hint">[' + esc(r.confidence || '—') + ']</span></li>').join('')
    : '';

  const canAccept = p.status === 'PROPOSED';
  const acceptHtml = canAccept
    ? '<div class="actions" style="margin:8px 0 4px">' +
        '<button class="btn small primary" id="acceptProposal" type="button">Accept → WORKING</button>' +
        '<span class="note">Controlled consolidation: creates a WORKING <code>codex_document</code> + ' +
        '<code>revision</code> and copies provenance. One proposal at a time; never canonical.</span></div>'
    : '<div class="layer-note">' + esc(p.status === 'WORKING'
        ? 'Accepted into WORKING Codex content.'
        : 'No consolidation action for status ' + p.status + '.') + '</div>';

  view.innerHTML =
    '<div class="card">' +
      '<div class="panel-head"><h2>Proposal</h2>' +
        '<span class="badge ' + (canAccept ? 'badge-proposed' : 'badge-working') + '">' +
        esc(p.status) + '</span></div>' +
      acceptHtml +
      '<dl class="meta-grid">' +
        metaRow('id', p.id, true) +
        metaRow('status', p.status) +
        metaRow('attribution', p.attribution, true) +
        metaRow('created_at', p.created_at) +
        metaRow('updated_at', p.updated_at) +
        metaRow('based_on', (p.based_on || []).join(', ') || '—', true) +
      '</dl>' +
      '<div class="section-title">Summary</div>' +
      '<div>' + esc(p.summary) + '</div>' +
      '<div class="section-title">Body</div>' +
      '<pre class="preview">' + esc(p.body || '(no body)') + '</pre>' +
      '<div class="section-title">Provenance <span class="hint">' + prov.length + '</span></div>' +
      '<ul class="messages">' + provHtml + '</ul>' +
      (rels.length
        ? '<div class="section-title">Relationships <span class="hint">' + rels.length + '</span></div>' +
          '<ul class="messages">' + relHtml + '</ul>'
        : '') +
    '</div>';

  const acceptBtn = $('#acceptProposal');
  if (acceptBtn) acceptBtn.addEventListener('click', () => acceptProposal(p.id));
}

async function acceptProposal(id) {
  const btn = $('#acceptProposal');
  if (btn) { btn.disabled = true; btn.textContent = 'Consolidating…'; }
  try {
    const data = await api.post('/api/engine/proposals/' + encodeURIComponent(id) + '/accept',
      { actor: 'stage4-ui' });
    const doc = data.codex_document || {};
    const out = $('#engineRunOut');
    out.classList.remove('hidden');
    out.innerHTML =
      '<div class="readonly-banner">Consolidated proposal <span class="mono">' + esc(id) + '</span> → ' +
      '<strong>' + esc(doc.status) + '</strong> <code>codex_document</code> ' +
      '<span class="mono">' + esc(doc.id) + '</span>' +
      ' · revision ' + esc((data.revision || {}).id || '—') +
      ' · provenance copied ' + esc(data.provenance_copied) +
      (data.already_accepted ? ' · already accepted' : '') +
      ' · CANONICAL ' + esc(data.canonical) + '</div>';
    state.engine.loaded = false;
    state.codex.loaded = false;   // WORKING list changed
    await loadEngine();
    await openProposal(id);
    loadMeta();
  } catch (err) {
    $('#engineRunOut').classList.remove('hidden');
    $('#engineRunOut').innerHTML = '<div class="error">Accept failed: ' + esc(err.message) + '</div>';
    if (btn) { btn.disabled = false; btn.textContent = 'Accept → WORKING'; }
  }
}

async function runLivingLoop() {
  const out = $('#engineRunOut');
  const btn = $('#engineRunLoop');
  out.classList.remove('hidden');
  out.innerHTML = '<div class="readonly-banner">Running the living loop against the living store…</div>';
  btn.disabled = true;
  try {
    const data = await api.post('/api/engine/run', {});
    out.innerHTML =
      '<div class="readonly-banner">Living loop · exit ' + esc(data.returncode) +
      ' · kinds ' + esc((data.kinds || []).join(', ')) +
      ' · proposals ' + esc(data.proposals_before) + ' → ' + esc(data.proposals_after) +
      ' (new ' + esc(data.new_proposals) + ') · WORKING codex_document ' + esc(data.codex_documents) +
      ' · CANONICAL ' + esc(data.canonical) + '</div>' +
      '<pre class="preview">' + esc(data.stdout_tail || '') +
      (data.stderr ? '\n[stderr]\n' + esc(data.stderr) : '') + '</pre>' +
      (data.ran ? '' : '<div class="error">living loop reported a non-zero exit</div>');
    state.engine.loaded = false;
    await loadEngine();
    loadMeta();
  } catch (err) {
    out.innerHTML = '<div class="error">Living loop failed: ' + esc(err.message) + '</div>';
  } finally {
    btn.disabled = false;
  }
}

async function runEngineDryRun() {
  const out = $('#engineDryRunOut');
  const btn = $('#engineDryRun');
  out.classList.remove('hidden');
  out.innerHTML = '<div class="readonly-banner">Running Stage 5 engine with --dry-run on a throwaway copy…</div>';
  btn.disabled = true;
  try {
    const data = await api.post('/api/engine/dry-run', {});
    const ok = data.engine_db_unchanged && data.returncode === 0;
    out.innerHTML =
      '<div class="readonly-banner">dry-run · read-only · canonical ' + esc(data.canonical) +
      ' · exit ' + esc(data.returncode) + ' · engine store unchanged: ' + esc(data.engine_db_unchanged) +
      '<br><span class="mono">' + esc(data.ran_on) + '</span></div>' +
      '<pre class="preview">' + esc((data.stdout || '') + (data.stderr ? '\n[stderr]\n' + data.stderr : '')) + '</pre>';
    if (!ok) out.insertAdjacentHTML('beforeend', '<div class="error">dry-run reported a non-zero exit</div>');
  } catch (err) {
    out.innerHTML = '<div class="error">Dry-run failed: ' + esc(err.message) + '</div>';
  } finally {
    btn.disabled = false;
  }
}

/* ============================ INIT ============================ */
async function loadMeta() {
  try {
    const m = await api.get('/api/meta');
    $('#dbBadge').textContent = 'store · ' + shortPath(m.db, 34);
    $('#dbBadge').title = m.db + '\nsource_document: ' + m.counts.source_document +
      '\nconversations: ' + m.counts.conversation +
      '\nengine db: ' + (m.engine_db || '—') + '\nCANONICAL: ' + m.canonical;
    const wb = $('#workingBadge');
    if (wb) {
      wb.textContent = 'WORKING codex_document: ' + (m.counts.codex_document || 0);
      wb.title = 'WORKING Codex content in the living store; consolidation max status '
        + 'is WORKING. CANONICAL: ' + m.canonical;
    }
  } catch (err) {
    $('#dbBadge').textContent = 'store unavailable';
  }
}

function wireCodex() {
  $('#codexFilters').addEventListener('submit', (e) => {
    e.preventDefault();
    state.codex.offset = 0;
    loadDocuments();
  });
  $('#codexReset').addEventListener('click', () => {
    $('#codexFilters').reset();
    state.codex.offset = 0;
    loadDocuments();
  });
  $('#prevPage').addEventListener('click', () => {
    state.codex.offset = Math.max(0, state.codex.offset - state.codex.limit);
    loadDocuments();
  });
  $('#nextPage').addEventListener('click', () => {
    state.codex.offset += state.codex.limit;
    loadDocuments();
  });
  // WORKING codex_document layer
  $('#codexDocFilters').addEventListener('submit', (e) => {
    e.preventDefault();
    state.codex.cdOffset = 0;
    loadCodexWorking();
  });
  $('#codexDocReset').addEventListener('click', () => {
    $('#codexDocFilters').reset();
    state.codex.cdOffset = 0;
    loadCodexWorking();
  });
  $('#cdPrev').addEventListener('click', () => {
    state.codex.cdOffset = Math.max(0, state.codex.cdOffset - state.codex.cdLimit);
    loadCodexWorking();
  });
  $('#cdNext').addEventListener('click', () => {
    state.codex.cdOffset += state.codex.cdLimit;
    loadCodexWorking();
  });
  $$('.seg').forEach((b) => b.addEventListener('click', () => setCodexMode(b.dataset.mode)));
}

function wireEngine() {
  $('#engineFilters').addEventListener('submit', (e) => {
    e.preventDefault();
    state.engine.offset = 0;
    loadProposals();
  });
  $('#engineReset').addEventListener('click', () => {
    $('#engineFilters').reset();
    state.engine.offset = 0;
    loadProposals();
  });
  $('#elimit').addEventListener('change', () => {
    state.engine.limit = parseInt($('#elimit').value, 10) || 50;
    state.engine.offset = 0;
    loadProposals();
  });
  $('#propPrev').addEventListener('click', () => {
    state.engine.offset = Math.max(0, state.engine.offset - state.engine.limit);
    loadProposals();
  });
  $('#propNext').addEventListener('click', () => {
    state.engine.offset += state.engine.limit;
    loadProposals();
  });
  $('#engineDryRun').addEventListener('click', runEngineDryRun);
  $('#engineRunLoop').addEventListener('click', runLivingLoop);
}

document.addEventListener('DOMContentLoaded', () => {
  $$('.tab').forEach((b) => b.addEventListener('click', () => selectTab(b.dataset.tab)));
  $('#newConvToggle').addEventListener('click', () => $('#newConvForm').classList.toggle('hidden'));
  $('#newConvCancel').addEventListener('click', () => $('#newConvForm').classList.add('hidden'));
  $('#newConvForm').addEventListener('submit', createConversation);
  wireCodex();
  wireEngine();
  loadMeta();
  loadConversations();
});
