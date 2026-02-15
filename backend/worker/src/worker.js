export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return cors(new Response(null, { status: 204 }));

    try {
      if (req.method === 'GET' && url.pathname === '/api/ping') {
        return cors(json({ ok: true, ts: new Date().toISOString() }));
      }

      if (req.method === 'POST' && url.pathname === '/api/recon/add') {
        return cors(await addRecon(req, env));
      }

      if (req.method === 'GET' && url.pathname === '/api/recon/list') {
        return cors(await listRecon(url, env));
      }

      if (req.method === 'GET' && url.pathname === '/api/modules/list') {
        return cors(await listModules(url, env));
      }

      if (req.method === 'POST' && url.pathname === '/api/quest/generate') {
        return cors(await generateQuest(req, env));
      }

      if (req.method === 'POST' && url.pathname === '/api/feedback') {
        return cors(await addFeedback(req, env));
      }

      return cors(new Response('Not found', { status: 404 }));
    } catch (err) {
      return cors(json({ ok: false, error: String(err?.message || err) }, 500));
    }
  }
};

// -----------------------
// Recon → Modules
// -----------------------
async function addRecon(req, env) {
  const body = await req.json();
  const id = crypto.randomUUID();
  const created_at = new Date().toISOString();

  const type = (body.type || 'text').toLowerCase();
  const title = safeStr(body.title || '', 160);
  const source_url = safeStr(body.url || '', 2000);

  let text = String(body.text || '');
  if (type === 'url') {
    if (!source_url) return json({ ok: false, error: 'Missing url' }, 400);
    const fetched = await fetch(source_url, { headers: { 'User-Agent': 'QuestHandler/1.0' } });
    if (!fetched.ok) return json({ ok: false, error: 'Failed to fetch URL' }, 400);
    text = await fetched.text();
  }
  if (!text || text.trim().length < 10) return json({ ok: false, error: 'No usable recon text' }, 400);

  const extracted = await extractModulesFromRecon(text, env);

  await env.DB.prepare(`
    INSERT INTO recon_items (id, created_at, type, title, source_url, raw_text, parse_status, quality_score, quality_notes)
    VALUES (?, ?, ?, ?, ?, ?, 'parsed', ?, ?)
  `).bind(id, created_at, type, title, source_url, text, clamp01(extracted.quality_score ?? 0.5), safeStr(extracted.quality_notes ?? '', 900)).run();

  let createdCount = 0;
  for (const m of (extracted.modules || [])) {
    if (!isModuleValid(m)) continue;

    const mid = crypto.randomUUID();
    await env.DB.prepare(`
      INSERT INTO modules (id, created_at, title, summary, tags, vibe, weather_fit, duration_fit, range_fit, location_hint, confidence, payload)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      mid, created_at,
      safeStr(m.title, 120),
      safeStr(m.summary, 400),
      JSON.stringify(m.tags || []),
      m.vibe || null,
      JSON.stringify(m.weather_fit || ['auto']),
      JSON.stringify(m.duration_fit || ['60m']),
      JSON.stringify(m.range_fit || ['short-drive']),
      safeStr(m.location_hint || '', 240),
      clamp01(m.confidence ?? 0.6),
      JSON.stringify(m.payload || {})
    ).run();

    await env.DB.prepare(`
      INSERT INTO module_sources (module_id, recon_id, note) VALUES (?, ?, ?)
    `).bind(mid, id, 'Derived from recon').run();

    createdCount++;
  }

  // Season readiness snapshot (simple v1 heuristic)
  const counts = await env.DB.prepare(`SELECT COUNT(*) as n FROM modules`).first();
  const coreTarget = 14; // tweak later
  const readiness = Math.min(1, (counts?.n || 0) / coreTarget);

  return json({
    ok: true,
    recon_id: id,
    modules_created: createdCount,
    recon_status: {
      assessment: scoreLabel(extracted.quality_score ?? 0.5),
      quality_score: clamp01(extracted.quality_score ?? 0.5),
      quality_notes: safeStr(extracted.quality_notes ?? '', 900),
      season: {
        modules_total: counts?.n || 0,
        target: coreTarget,
        readiness_pct: Math.round(readiness * 100)
      },
      recommended_recon: extracted.recommended_recon || []
    }
  });
}

async function listRecon(url, env) {
  const limit = clampInt(url.searchParams.get('limit'), 1, 200, 50);
  const rows = await env.DB.prepare(`
    SELECT id, created_at, type, title, source_url, quality_score, quality_notes
    FROM recon_items
    ORDER BY created_at DESC
    LIMIT ?
  `).bind(limit).all();

  const mc = await env.DB.prepare('SELECT COUNT(*) AS n FROM modules').first();
  return json({ ok: true, items: rows.results || [], module_count: mc?.n || 0 });
}

async function listModules(url, env) {
  const limit = clampInt(url.searchParams.get('limit'), 1, 200, 80);
  const tag = (url.searchParams.get('tag') || '').trim().toLowerCase();

  const rows = await env.DB.prepare(`
    SELECT id, created_at, title, summary, tags, vibe, weather_fit, duration_fit, range_fit, location_hint, confidence, payload
    FROM modules
    ORDER BY confidence DESC, created_at DESC
    LIMIT ?
  `).bind(limit).all();

  let items = (rows.results || []).map(r => ({
    ...r,
    tags: safeJson(r.tags, []),
    weather_fit: safeJson(r.weather_fit, []),
    duration_fit: safeJson(r.duration_fit, []),
    range_fit: safeJson(r.range_fit, []),
    payload: safeJson(r.payload, {})
  }));

  if (tag) items = items.filter(m => (m.tags || []).map(x => String(x).toLowerCase()).includes(tag));
  return json({ ok: true, items });
}

// -----------------------
// Modules → Quest
// -----------------------
async function generateQuest(req, env) {
  const body = await req.json();
  const inputs = body.inputs || {};
  const avoid = Array.isArray(body.avoid_titles) ? body.avoid_titles : [];

  const rows = await env.DB.prepare(`
    SELECT id, title, summary, tags, vibe, weather_fit, duration_fit, range_fit, location_hint, confidence, payload
    FROM modules
    ORDER BY confidence DESC, created_at DESC
    LIMIT 16
  `).all();

  const modules = (rows.results || []).map(m => ({
    id: m.id,
    title: m.title,
    summary: m.summary,
    tags: safeJson(m.tags, []),
    vibe: m.vibe,
    weather_fit: safeJson(m.weather_fit, []),
    duration_fit: safeJson(m.duration_fit, []),
    range_fit: safeJson(m.range_fit, []),
    location_hint: m.location_hint,
    confidence: m.confidence,
    payload: safeJson(m.payload, {})
  }));

  const quest = await callAIJson(QUEST_AUTHOR_PROMPT + '\n\nINPUT:\n' + JSON.stringify({ inputs, avoid_titles: avoid, modules }), env);

  // normalize
  quest.id = quest.id || crypto.randomUUID();
  quest.created_at = quest.created_at || new Date().toISOString();
  quest.status = quest.status || 'proposed';
  quest.inputs = quest.inputs || inputs;

  return json(quest);
}

// -----------------------
// Feedback
// -----------------------
async function addFeedback(req, env) {
  const body = await req.json();
  const id = crypto.randomUUID();
  const created_at = new Date().toISOString();
  const kind = safeStr(body.kind || 'general', 40);
  const target_id = safeStr(body.target_id || '', 80);
  const rating = clampInt(body.rating, 1, 5, 3);
  const note = safeStr(body.note || '', 1000);

  await env.DB.prepare(`
    INSERT INTO feedback (id, created_at, kind, target_id, rating, note, action)
    VALUES (?, ?, ?, ?, ?, ?, 'none')
  `).bind(id, created_at, kind, target_id, rating, note).run();

  return json({ ok: true, feedback_id: id });
}

// -----------------------
// AI calls + prompts
// -----------------------
async function extractModulesFromRecon(text, env) {
  const userPrompt = GOLD_MODULE_PROMPT.replace('[PASTE RECON TEXT HERE]', text.slice(0, 24000));
  const out = await callAIJson(userPrompt, env);

  return {
    quality_score: clamp01(out.quality_score ?? 0.5),
    quality_notes: String(out.quality_notes || '').slice(0, 900),
    recommended_recon: Array.isArray(out.recommended_recon) ? out.recommended_recon.slice(0, 8) : [],
    modules: Array.isArray(out.modules) ? out.modules : []
  };
}

async function callAIJson(userContent, env) {
  const model = env.OPENROUTER_MODEL || 'anthropic/claude-3.5-sonnet';
  const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.OPENROUTER_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: 'You output ONLY valid JSON. No markdown. No extra text.' },
        { role: 'user', content: userContent }
      ],
      temperature: 0.6
    })
  });

  const data = await res.json();
  const content = data?.choices?.[0]?.message?.content;
  if (!content) throw new Error('AI returned empty response');

  try { return JSON.parse(content); }
  catch {
    const a = content.indexOf('{');
    const b = content.lastIndexOf('}');
    if (a >= 0 && b > a) return JSON.parse(content.slice(a, b + 1));
    throw new Error('AI did not return valid JSON');
  }
}

const QUEST_AUTHOR_PROMPT = `
You are THE HANDLER.
Design memorable real-world adventures for a parent+child.

Hard bans:
- No generic quests ("go for a walk", "find 5 things", "do something fun outside").
- Avoid vague steps. Prefer named anchors or strong locality hints.
- Safe, legal, kid-friendly.

Style:
- Calm. Cryptic. Short sentences.
- Frame quests as operations. Side quests are optional intelligence.

Return ONLY JSON with:
- title, hook
- 3–7 primary steps (id,text,primary,idx,done,xp)
- 2–4 side steps
- 2–5 artifacts incl. at least one False Signal
- modules_used + sources
- scoring + progress
Avoid reusing avoid_titles.

Return ONLY JSON.`;

const GOLD_MODULE_PROMPT = `
You are THE HANDLER's INTEL ANALYST.

Convert recon into QUEST MODULES.
Hard bans:
- No generic modules like "go for a walk", "find 5 things", "go to a park" without named anchor/details.
- No filler scavenger hunts.
- If recon is weak, return modules=[] and explain why.

Return ONLY JSON:
{
  "quality_score": 0.0-1.0,
  "quality_notes": "string",
  "recommended_recon": ["string", "..."],
  "modules": [
    {
      "title": "string",
      "summary": "string",
      "tags": ["..."],
      "vibe": "curious|chill|active|cozy|mystery|kid-picks|null",
      "weather_fit": ["auto","sunny","rainy","cold","hot","windy"],
      "duration_fit": ["30m","60m","2h","halfday"],
      "range_fit": ["walk","short-drive","long-drive"],
      "location_hint": "string",
      "confidence": 0.0-1.0,
      "payload": {
        "anchor": { "name": "string|null", "note": "string|null" },
        "why_memorable": "string",
        "beats": [
          { "kind": "step", "text": "..." },
          { "kind": "step", "text": "..." },
          { "kind": "boss_moment", "text": "..." },
          { "kind": "artifact", "type": "map|riddle|image|herring|token", "title": "string", "text": "string", "answer": null, "hint": null, "map_query": null }
        ]
      }
    }
  ]
}

Constraints:
- 0–4 modules max.
- Each module must have >= 2 steps + 1 boss_moment + 1 artifact.
- If recon mentions claims (filming/hours/events), add "needs verification" in notes.
- Also output recommended_recon strings to fill gaps.

Now process the recon:
[PASTE RECON TEXT HERE]
`;

// -----------------------
// Validation + utils
// -----------------------
function isModuleValid(m) {
  if (!m || typeof m !== 'object') return false;

  const title = String(m.title || '').toLowerCase();
  const summary = String(m.summary || '').toLowerCase();
  const banned = ['go for a walk','take a walk','go outside','find 5','find five','scavenger','do something fun','visit a park','go to the park'];
  if (banned.some(x => title.includes(x) || summary.includes(x))) return false;

  const beats = m?.payload?.beats;
  if (!Array.isArray(beats) || beats.length < 4) return false;

  const steps = beats.filter(b => b?.kind === 'step').length;
  const boss = beats.filter(b => b?.kind === 'boss_moment').length;
  const art  = beats.filter(b => b?.kind === 'artifact').length;
  if (steps < 2 || boss < 1 || art < 1) return false;

  const why = String(m?.payload?.why_memorable || '').trim();
  if (why.length < 20) return false;

  return true;
}

function scoreLabel(s) {
  s = clamp01(s);
  if (s >= 0.85) return 'EXCELLENT';
  if (s >= 0.65) return 'GOOD';
  if (s >= 0.45) return 'WEAK';
  return 'NOISE';
}

function clamp01(n){ n = Number(n); if (Number.isNaN(n)) return 0; return Math.max(0, Math.min(1, n)); }
function clampInt(n, min, max, dflt){
  const v = parseInt(n ?? '', 10);
  if (Number.isNaN(v)) return dflt;
  return Math.max(min, Math.min(max, v));
}
function safeStr(s, max){ return String(s || '').slice(0, max); }
function safeJson(s, dflt){
  try { return typeof s === 'string' ? JSON.parse(s) : (s ?? dflt); }
  catch { return dflt; }
}
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
}
function cors(res) {
  const h = new Headers(res.headers);
  h.set('Access-Control-Allow-Origin', '*');
  h.set('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  h.set('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  return new Response(res.body, { status: res.status, headers: h });
}
