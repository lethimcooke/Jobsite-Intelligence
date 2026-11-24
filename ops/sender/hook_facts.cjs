// Live NOI hook facts from the PC, with the same source and rule the JSI publisher uses (JsiPublisher.gs noiProblem_).
// Library: const H = require('./hook_facts.cjs'); await H.fact(hook); H.problem(hook, fact, today)
// CLI:     node ops/sender/hook_facts.cjs <hooks.json: [{id, hook}]> <send date YYYY-MM-DD> [--facts <offline.json>]
//          --facts {"TXR15....": {rows: [...]}} replaces the network (tests and replays of a saved hook_recheck.js run).
const path = require('path'), fs = require('fs');
const S = require(path.join(__dirname, 'Code.gs'));
global.CFG = S.CFG;
const P = require(path.join(__dirname, 'JsiPublisher.gs'));
let offline = null;
async function getJson(url) {
  for (let i = 0; i < 2; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch (e) { /* retry */ } }
  return null;
}
async function fact(h) {
  if (!h || h.kind !== 'NOI') return {};
  if (offline) return offline[h.id] || { rows: [] };
  const where = encodeURIComponent(`program_code='STORM' AND additional_id_text='${String(h.id).replace(/[^A-Z0-9]/g, '')}'`);
  const res = [];
  for (const ds of P.JPUB.TCEQ_FILES)
    res.push(await getJson(`https://data.texas.gov/resource/${ds}.json?$select=additional_id_status,affil_begin_dt&$limit=50&$where=${where}`));
  return P.jsiNoiFact_(res);
}
const problem = (h, f, today) => P.noiProblem_(h, f, today);
module.exports = { fact, problem };
if (require.main === module) {
  const args = process.argv.slice(2), fi = args.indexOf('--facts');
  if (fi >= 0) { const raw = JSON.parse(fs.readFileSync(args[fi + 1], 'utf8')); offline = raw.records || raw; args.splice(fi, 2); }
  const items = JSON.parse(fs.readFileSync(args[0], 'utf8')), today = args[1];
  (async () => {
    const out = [];
    for (const it of items) { const f = await fact(it.hook); out.push({ id: it.id, kind: it.hook.kind, hook_id: it.hook.id, fact: f, problem: problem(it.hook, f, today) || '' }); }
    console.log(JSON.stringify({ today, tceq_available: !out.some(r => r.fact && r.fact.unavailable), results: out }, null, 1));
  })();
}
