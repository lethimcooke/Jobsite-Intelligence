// Dry-run the JSI publisher's morning re-check on a staged batch, with the live Central Registry, from the PC.
// Publishes nothing and touches no Gmail.  node ops/sender/dry_publish.cjs <prepare_batch.py output file> [today YYYY-MM-DD]
const fs = require('fs'), path = require('path'), crypto = require('crypto'), zlib = require('zlib');
const H = require(path.join(__dirname, 'hook_facts.cjs'));
const P = require(path.join(__dirname, 'JsiPublisher.gs'));
const txt = fs.readFileSync(process.argv[2], 'utf8');
const subject = /SUBJECT: (.+)/.exec(txt)[1].trim(), body = txt.split(/BODY:\r?\n/)[1];
const today = process.argv[3] || subject.split(' ')[2];
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');
const p = P.jsiDecodePrepared_(subject, body, today, Date.parse(today + 'T11:00:00Z'), sha, (s) => Buffer.from(s, 'base64'),
  (b) => Buffer.from(b).toString('utf8'), (b) => zlib.gunzipSync(Buffer.from(b)));
(async () => {
  const res = [];
  for (const e of p.entries) { const f = await H.fact(e.hook); res.push({ id: e.outreach_id, stage: e.stage, kind: e.hook.kind, hook_id: e.hook.id, fact: f, problem: H.problem(e.hook, f, today) }); }
  console.log(JSON.stringify({ today, prepared: subject, checked_at: new Date().toISOString(),
    pass: res.filter(r => !r.problem).length, drop: res.filter(r => r.problem).length, results: res }, null, 1));
})();
