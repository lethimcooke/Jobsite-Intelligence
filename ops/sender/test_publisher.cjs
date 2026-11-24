// Tests for ops/sender/JsiPublisher.gs. Run: node ops/sender/test_publisher.cjs [prepare_batch.py output file]
// The optional argument is prepare_batch.py's printed output (SUBJECT/BODY): an end-to-end check that the batch
// decodes in the publisher and that the manifest it would publish passes the sender's own decodeManifest_ (Code.gs).
const assert = require('assert'), crypto = require('crypto'), zlib = require('zlib'), path = require('path'), fs = require('fs');
const S = require(path.join(__dirname, 'Code.gs'));
global.CFG = S.CFG;
const P = require(path.join(__dirname, 'JsiPublisher.gs'));
let passed = 0;
function test(name, fn) { try { fn(); passed++; } catch (e) { console.error('FAIL ' + name + ': ' + e.message); process.exitCode = 1; } }
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');
const b64 = (s) => Buffer.from(s, 'base64'), utf8 = (b) => Buffer.from(b).toString('utf8'), gunzip = (b) => zlib.gunzipSync(Buffer.from(b));
function encode(obj, prefix, date) {
  const raw = Buffer.from(JSON.stringify(obj), 'utf8');
  return { subject: `${prefix} v1 ${date} ${sha(raw)}`, body: zlib.gzipSync(raw).toString('base64').replace(/(.{76})/g, '$1\n') };
}
const day = (d) => Date.parse(d + 'T12:00:00Z');

// ---- send days
test('weekday is a send day', () => assert.ok(P.jsiIsSendDay_('2026-11-25', 3)));
test('weekend is not', () => assert.ok(!P.jsiIsSendDay_('2026-11-28', 6)));
test('Thanksgiving and the Friday after are not', () => { assert.ok(!P.jsiIsSendDay_('2026-11-26', 4)); assert.ok(!P.jsiIsSendDay_('2026-11-27', 5)); });
test('holidays match ops/routines/holidays.txt', () => {
  const txt = fs.readFileSync(path.join(__dirname, '..', 'routines', 'holidays.txt'), 'utf8');
  assert.deepStrictEqual(P.JPUB.HOLIDAYS, txt.split(/\r?\n/).filter(l => /^\d{4}-\d{2}-\d{2}$/.test(l.trim())).map(l => l.trim()));
});

// ---- prepared batch decoding
const PREP = { version: 1, kind: 'prepared', send_date: '2026-11-30', prepared_at: '2026-11-25T19:30:00+00:00',
  business: 'Jobsite Intelligence', max_total: 60, max_s1: 5, share: 15, aliases: { 'sites@asterfieldgroup.com': 'Houston Jobsite Intelligence' },
  dnc_emails: [], dnc_domains: [], entries: [{ outreach_id: 'JI-H14-S1-01', stage: 'S1', to: 'a@b.com', hook: { kind: 'NOI', id: 'TXR1594ZB', cited: '2026-11-05' } }] };
const enc = encode(PREP, 'JSI-PREPARED', '2026-11-30');
const dec = (e, today, now) => P.jsiDecodePrepared_(e.subject, e.body, today, now, sha, b64, utf8, gunzip);
test('prepared batch staged Wed before Thanksgiving decodes on Mon', () => assert.strictEqual(dec(enc, '2026-11-30', day('2026-11-30')).entries.length, 1));
test('prepared batch for another day is refused', () => assert.throws(() => dec(enc, '2026-12-01', day('2026-12-01')), /not 2026-12-01/));
test('edited prepared batch is refused', () => assert.throws(() => dec({ subject: enc.subject.replace(/.$/, '0'), body: enc.body }, '2026-11-30', day('2026-11-30')), /checksum/));
test("ASI's prepared subject is not ours", () => assert.throws(() => dec(encode(PREP, 'ASI-PREPARED', '2026-11-30'), '2026-11-30', day('2026-11-30')), /not a JSI/));
test('a batch for another business is refused', () => assert.throws(() =>
  dec(encode(Object.assign({}, PREP, { business: 'Austin Signage Intelligence' }), 'JSI-PREPARED', '2026-11-30'), '2026-11-30', day('2026-11-30')), /Austin Signage/));
test('a non-Jobsite ID in the batch is refused', () => assert.throws(() =>
  dec(encode(Object.assign({}, PREP, { entries: [{ outreach_id: 'V5H-S1-01', stage: 'S1' }] }), 'JSI-PREPARED', '2026-11-30'), '2026-11-30', day('2026-11-30')), /non-Jobsite/));
test('prepared batch older than 6 days is refused', () => assert.throws(() =>
  dec(encode(Object.assign({}, PREP, { prepared_at: '2026-11-23T12:00:00+00:00' }), 'JSI-PREPARED', '2026-11-30'), '2026-11-30', day('2026-11-30')), /too old/));

// ---- NOI hook freshness
const H = (o) => Object.assign({ kind: 'NOI', id: 'TXR1594ZB', cited: '2026-11-05' }, o);
const ACT = { rows: [{ status: 'ACTIVE', date: '2026-11-05' }, { status: 'ACTIVE', date: '2026-08-07' }] };
test('active, cited date on record, within 45 days: passes', () => assert.strictEqual(P.noiProblem_(H(), ACT, '2026-11-30'), ''));
test('day 45 passes (Orizon case)', () => assert.strictEqual(P.noiProblem_(H(), ACT, '2026-12-20'), ''));
test('day 46 is stale (786 Dumpsters case)', () => assert.match(P.noiProblem_(H(), ACT, '2026-12-21'), /46 days.*over 45/));
test('cited date not on the live record is stale (Hero Portables case)', () => assert.match(P.noiProblem_(H({ cited: '2026-10-08' }), ACT, '2026-11-13'), /not on the live record/));
test('authorization no longer active is stale', () => assert.match(P.noiProblem_(H(), { rows: [{ status: 'TERMINATED', date: '2026-11-05' }] }, '2026-11-30'), /TERMINATED/));
test('authorization gone is stale', () => assert.match(P.noiProblem_(H(), { rows: [] }, '2026-11-30'), /not found/));
test('Central Registry down is not assumed fine', () => assert.match(P.noiProblem_(H(), { unavailable: true }, '2026-11-30'), /unavailable/));
test('follow-up with no hook passes', () => assert.strictEqual(P.noiProblem_({ kind: 'NONE' }, {}, '2026-11-30'), ''));
test('an ASI hook kind is refused', () => assert.match(P.noiProblem_({ kind: 'TABS', id: 'x' }, {}, '2026-11-30'), /unknown hook kind/));
test('Central Registry rows from five files merge; all files down = unavailable', () => {
  assert.deepStrictEqual(P.jsiNoiFact_([[], null, [{ additional_id_status: 'ACTIVE', affil_begin_dt: '2026-11-05T00:00:00.000' }], [], []]),
    { rows: [{ status: 'ACTIVE', date: '2026-11-05' }] });
  assert.deepStrictEqual(P.jsiNoiFact_([null, null, null, null, null]), { unavailable: true });
  assert.deepStrictEqual(P.jsiNoiFact_([[], [], [], [], []]), { rows: [] });
});

// ---- publish decisions: one business never blocks or satisfies the other
const PREPD = { entries: [{}] }, MINE = { business: 'Jobsite Intelligence', entries: [{}], dry_run_only: false };
const ASIM = { business: 'Austin Signage Intelligence', entries: [{}, {}], dry_run_only: false };
const D = (o) => P.jsiPublishDecision_(Object.assign({ sendDay: true, manifestsToday: [], liveRowsToday: 0, prepared: PREPD }, o)).action;
test('no Jobsite manifest with a prepared batch publishes', () => assert.strictEqual(D({}), 'PUBLISH'));
test("ASI's manifest today does not count as ours", () => assert.strictEqual(D({ manifestsToday: [ASIM] }), 'PUBLISH'));
test('rerun after publishing keeps ours', () => assert.strictEqual(D({ manifestsToday: [ASIM, MINE] }), 'KEEP'));
test('Jobsite rows already sending: never republish', () => assert.strictEqual(D({ manifestsToday: [], liveRowsToday: 2 }), 'SENDING'));
test('a test manifest is not live', () => assert.strictEqual(D({ manifestsToday: [Object.assign({}, MINE, { dry_run_only: true })] }), 'PUBLISH'));
test('empty manifest is replaced', () => assert.strictEqual(D({ manifestsToday: [Object.assign({}, MINE, { entries: [] })] }), 'PUBLISH'));
test('no prepared batch: MISSING', () => assert.strictEqual(D({ prepared: null }), 'MISSING'));
test('holiday: nothing', () => assert.strictEqual(D({ sendDay: false }), 'NONE'));
test('published manifest drops hook fields and keeps entry order', () => {
  const m = P.jsiBuildManifest_(PREP, [{ outreach_id: 'JI-1', hook: { kind: 'NOI' }, to: 'a' }, { outreach_id: 'JI-2', hook: { kind: 'NONE' }, to: 'b' }], '2026-11-30T12:10:00+00:00');
  assert.deepStrictEqual(m.entries, [{ outreach_id: 'JI-1', to: 'a' }, { outreach_id: 'JI-2', to: 'b' }]);
  assert.strictEqual(m.business, 'Jobsite Intelligence'); assert.strictEqual(m.dry_run_only, false); assert.strictEqual(m.share, 15);
});

// ---- alerts only when action is needed
const W = (o) => Object.assign({ sendDay: true, today: '2026-11-30', at: '7:50 AM', manifestOk: true, preparedOk: true, mode: 'LIVE', senderTrigger: true, publisherTrigger: true, retries: [] }, o);
test('all in place: no alert', () => assert.strictEqual(P.jsiWatchdogReport_(W()), null));
test('holiday: no alert', () => assert.strictEqual(P.jsiWatchdogReport_(W({ sendDay: false, manifestOk: false })), null));
test('missing manifest alert names Jobsite, what was retried and what to do', () => {
  const r = P.jsiWatchdogReport_(W({ manifestOk: false, preparedOk: false, retries: ['06:12 MISSING: no JSI prepared batch for today'] }));
  assert.match(r.subject, /^ACTION NEEDED: JSI pre-send/); assert.match(r.body, /06:12 MISSING/); assert.match(r.body, /run the JSI close-out/);
});
test('JSI publisher triggers missing alerts', () => assert.match(P.jsiWatchdogReport_(W({ publisherTrigger: false })).body, /installJsiPublisher/));
const MAN2 = { entries: [{ outreach_id: 'JI-a', to: 'x@y.com' }, { outreach_id: 'JI-b', to: 'z@y.com' }] };
test('all sent or skipped: no alert', () => assert.strictEqual(P.jsiConfirmReport_('2026-11-30', MAN2, { 'JI-a': 'sent', 'JI-b': 'skipped' }), null));
test('unsent entries alert', () => assert.match(P.jsiConfirmReport_('2026-11-30', MAN2, { 'JI-a': 'sent' }).body, /1 of 2 Jobsite/));

// ---- installer: only JSI triggers, never ASI's or runSender
function fakeScriptApp(initial) {
  let triggers = initial.map(h => ({ h, getHandlerFunction() { return this.h; } }));
  const builder = (h) => { const b = { timeBased: () => b, atHour: () => b, nearMinute: () => b, everyDays: () => b, inTimezone: () => b,
    create: () => { triggers.push({ h, getHandlerFunction() { return this.h; } }); } }; return b; };
  return { getProjectTriggers: () => triggers.slice(), deleteTrigger: (t) => { triggers = triggers.filter(x => x !== t); }, newTrigger: builder,
    count: () => triggers.reduce((o, t) => (o[t.h] = (o[t.h] || 0) + 1, o), {}) };
}
global.Logger = { log() {} };
const ASI_TRIGGERS = { runSender: 1, publishManifest: 4, watchdog: 1, confirmSends: 1 };
test('installer adds 4 publish + watchdog + confirm and leaves ASI triggers alone', () => {
  global.ScriptApp = fakeScriptApp(['runSender', 'publishManifest', 'publishManifest', 'publishManifest', 'publishManifest', 'watchdog', 'confirmSends']);
  P.installJsiPublisher();
  assert.deepStrictEqual(global.ScriptApp.count(), Object.assign({}, ASI_TRIGGERS, { jsiPublishManifest: 4, jsiWatchdog: 1, jsiConfirmSends: 1 }));
});
test('installer rerun does not duplicate', () => {
  P.installJsiPublisher(); P.installJsiPublisher();
  assert.deepStrictEqual(global.ScriptApp.count(), Object.assign({}, ASI_TRIGGERS, { jsiPublishManifest: 4, jsiWatchdog: 1, jsiConfirmSends: 1 }));
});
test('rollback removes only the JSI triggers', () => { P.removeJsiPublisher(); assert.deepStrictEqual(global.ScriptApp.count(), ASI_TRIGGERS); });
test('JSI watchdog fires after its last publish run and before sending starts', () => {
  const m = P.jsiScheduleMargins_();
  assert.ok(m.lastPublishDone < m.watchdogEarliest, JSON.stringify(m));
  assert.ok(m.watchdogEarliest < m.sendStart + 15, JSON.stringify(m));
});
test('JSI publish runs sit between ASI runs (6:00, 6:20, 6:40, 7:00)', () => {
  const asi = [360, 380, 400, 420];
  P.JPUB.PUBLISH_AT.forEach(x => asi.forEach(a => assert.ok(Math.abs(x[0] * 60 + x[1] - a) >= 10, JSON.stringify(x))));
});
test('function names never collide with ASI Publisher.gs globals', () => {
  const src = fs.readFileSync(path.join(__dirname, 'JsiPublisher.gs'), 'utf8');
  const names = [...src.matchAll(/^function (\w+)/gm)].map(m => m[1]);
  const asi = ['isSendDay_', 'decodePrepared_', 'parseTabs_', 'hookProblem_', 'publishDecision_', 'buildManifest_', 'watchdogReport_',
    'confirmReport_', 'scheduleMargins_', 'installPublisher', 'removePublisher', 'todayInfo_', 'liveRowsToday_', 'preparedForToday_',
    'fetchJson_', 'fetchHookFact_', 'publishManifest', 'watchdog', 'confirmSends', 'testAlert', 'pubLog_'];
  const code = [...fs.readFileSync(path.join(__dirname, 'Code.gs'), 'utf8').matchAll(/^function (\w+)/gm)].map(m => m[1]);
  names.forEach(n => { assert.ok(asi.indexOf(n) < 0 && code.indexOf(n) < 0, n); });
  assert.ok(!/^var (PUB|CFG)\b/m.test(src));
});

// ---- end to end on a real prepared batch: Python stages it, the publisher publishes, the sender accepts it
const out = process.argv[2];
if (out && fs.existsSync(out)) {
  const txt = fs.readFileSync(out, 'utf8'), subject = /SUBJECT: (.+)/.exec(txt)[1].trim(), body = txt.split(/BODY:\r?\n/)[1];
  const date = subject.split(' ')[2], now = day(date) - 6 * 3600000;
  const p = P.jsiDecodePrepared_(subject, body, date, now, sha, b64, utf8, gunzip);
  test('end to end: real prepared batch decodes in the publisher', () => assert.ok(p.entries.length > 0));
  test('end to end: every S1 carries an NOI hook', () => assert.ok(p.entries.filter(e => e.stage === 'S1').every(e => e.hook.kind === 'NOI' && /^TXR15/.test(e.hook.id))));
  const kept = p.entries.slice(1);
  const man = P.jsiBuildManifest_(p, kept.length ? kept : p.entries, new Date(now).toISOString().replace(/\.\d{3}Z$/, '+00:00'));
  const m = encode(man, 'ASI-MANIFEST', date);
  const d2 = S.decodeManifest_(m.subject, m.body, date, now + 1800000, sha, b64, utf8, gunzip);
  test("end to end: published manifest passes the sender's own decoder", () => assert.strictEqual(d2.entries.length, man.entries.length));
  test('end to end: live, Jobsite, sites@, no hook fields', () => {
    assert.strictEqual(d2.dry_run_only, false); assert.strictEqual(d2.business, 'Jobsite Intelligence');
    assert.ok(d2.entries.every(e => !('hook' in e) && e.from_alias === 'sites@asterfieldgroup.com' && e.draft_id && e.body_sha256));
  });
  test('end to end: refused the next day (no stale publish)', () => assert.throws(() => S.decodeManifest_(m.subject, m.body, '2026-12-31', now + 30 * 86400000, sha, b64, utf8, gunzip)));
  console.log('end to end: ' + subject);
}
console.log(`JSI publisher tests: ${passed} passed` + (process.exitCode ? ' (with failures)' : ''));
