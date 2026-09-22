/* Codex Solbian — Phase I · Stage 4 — two-surface client (vanilla JS, no framework). */
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
  codex: { limit: 50, offset: 0, total: 0, docId: null },
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
    await api.post('/api/solace/conversations/' + encodeURIComponent(state.convId) + '/messages',
      { role, body, stub_reply: stub });
    await openConversation(state.convId);
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
  } catch (err) {
    $('#docCount').textContent = 'facets failed';
  }
  loadDocuments();
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

/* ============================ INIT ============================ */
async function loadMeta() {
  try {
    const m = await api.get('/api/meta');
    $('#dbBadge').textContent = 'store · ' + shortPath(m.db, 34);
    $('#dbBadge').title = m.db + '\nsource_document: ' + m.counts.source_document +
      '\nconversations: ' + m.counts.conversation + '\nCANONICAL: ' + m.canonical;
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
}

document.addEventListener('DOMContentLoaded', () => {
  $$('.tab').forEach((b) => b.addEventListener('click', () => selectTab(b.dataset.tab)));
  $('#newConvToggle').addEventListener('click', () => $('#newConvForm').classList.toggle('hidden'));
  $('#newConvCancel').addEventListener('click', () => $('#newConvForm').classList.add('hidden'));
  $('#newConvForm').addEventListener('submit', createConversation);
  wireCodex();
  loadMeta();
  loadConversations();
});
