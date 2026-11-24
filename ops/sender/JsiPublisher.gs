/**
 * Jobsite Intelligence publisher: a second entry in the ASI Sender Apps Script project, next to ASI's Publisher.gs.
 * It uses Code.gs's CFG and helpers (loadManifests_, checkEntry_, gatherFacts_, sha256Hex_, sha256Utf8_, log_,
 * parseAddresses_) and shares nothing else with ASI's publisher: every name here starts with "jsi"/"JSI", it reads
 * only "JSI-PREPARED v1" drafts, counts only JI- Sender Log rows, and installs and removes only its own triggers.
 * A blocker in one business's publish leaves the other free (STATUS.md "JSI template", ASI repo).
 *
 *   - The JSI close-out (the day before) stages a PREPARED batch: a draft to operations@ with subject
 *     "JSI-PREPARED v1 <send date> <sha256>", body gzip+base64 JSON (ops/routines/tools/prepare_batch.py in the
 *     Jobsite repo). It lists the day's Gmail draft IDs with their approved text hashes and, per S1, the TCEQ hook.
 *   - jsiPublishManifest() (6:10, 6:30, 6:50, 7:10 AM Central, weekdays) re-checks every entry (checkEntry_ as the
 *     sender does, plus the NOI hook on the live Central Registry) and publishes ONE same-day
 *     "ASI-MANIFEST v1" draft with business "Jobsite Intelligence", which runSender then sends from sites@.
 *     It never replaces a valid Jobsite manifest or one that has started sending.
 *   - jsiWatchdog() (7:50 AM) and jsiConfirmSends() (5:15 PM) email the owner only when action is needed.
 * Nothing here sends to prospects. Code is owned by the Jobsite repo (ops/sender/JsiPublisher.gs); the user pastes
 * it into the Apps Script project as a new file named JsiPublisher.
 */

var JPUB = {
  PREPARED_RE: /^JSI-PREPARED v1 (\d{4}-\d{2}-\d{2}) ([0-9a-f]{64})$/,
  PREPARED_PREFIX: 'JSI-PREPARED v1',
  BUSINESS: 'Jobsite Intelligence',
  ID_PREFIX: 'JI-',
  LOG_MODE: 'JSI-PUBLISH',        // Sender Log mode column for this publisher's rows (ASI's publisher writes PUBLISH)
  PREPARED_MAX_AGE_D: 6,          // staged up to 6 days ahead (Tue Nov 25 for Mon Nov 30 over Thanksgiving)
  SITE_WINDOW_D: 45,              // tracker, Nov 6: hook site at most 45 days from its TCEQ record date
  // Ten minutes after each ASI run so the two rarely wait on the shared script lock; each run resumes the last.
  PUBLISH_AT: [[6, 10], [6, 30], [6, 50], [7, 10]],
  WATCHDOG_AT: [7, 50],
  CONFIRM_AT: [17, 15],
  JITTER_MIN: 15,
  RUN_LIMIT_MIN: 6,
  TIME_BUDGET_MS: 270000,
  TCEQ_FILES: ['msah-s2rv', '5eqq-7nad', 't34q-qzi3', 'tzyg-j7q4', '9iad-hrn8'],
  HOLIDAYS: ['2026-11-26', '2026-11-27', '2026-12-24', '2026-12-25', '2027-01-01', '2027-01-18', '2027-02-15',
    '2027-05-31', '2027-07-05', '2027-09-06', '2027-11-25', '2027-11-26', '2027-12-24'],
  HANDLERS: ['jsiPublishManifest', 'jsiWatchdog', 'jsiConfirmSends']
};

// ---------------------------------------------------------------- pure helpers (unit-tested)

function jsiIsSendDay_(dateStr, dow) {
  return dow >= 1 && dow <= 5 && JPUB.HOLIDAYS.indexOf(dateStr) < 0;
}

/** Validate and decode a JSI prepared batch. Throws on any problem. */
function jsiDecodePrepared_(subject, body, today, nowMs, sha256Hex, b64Decode, utf8, gunzip) {
  var m = JPUB.PREPARED_RE.exec(String(subject || '').trim());
  if (!m) throw new Error('not a JSI prepared-batch subject');
  var bytes;
  try { bytes = gunzip(b64Decode(String(body || '').replace(/[^A-Za-z0-9+/=]/g, ''))); }
  catch (err) { throw new Error('prepared batch damaged: ' + err); }
  if (sha256Hex(bytes) !== m[2]) throw new Error('prepared batch checksum mismatch');
  var p = JSON.parse(utf8(bytes));
  if (p.version !== 1 || p.kind !== 'prepared') throw new Error('unknown prepared-batch format');
  if (p.business !== JPUB.BUSINESS) throw new Error('prepared batch is for ' + p.business + ', not ' + JPUB.BUSINESS);
  if (p.send_date !== m[1] || p.send_date !== today) throw new Error('prepared batch is for ' + p.send_date + ', not ' + today);
  var ageD = (nowMs - Date.parse(p.prepared_at)) / 86400000;
  if (!(ageD >= -0.05 && ageD <= JPUB.PREPARED_MAX_AGE_D)) throw new Error('prepared batch is too old');
  if (!Array.isArray(p.entries) || !p.entries.length) throw new Error('prepared batch has no entries');
  var bad = p.entries.filter(function (e) { return String(e.outreach_id || '').indexOf(JPUB.ID_PREFIX) !== 0; });
  if (bad.length) throw new Error('prepared batch has non-Jobsite entries: ' + bad[0].outreach_id);
  p.sha = m[2];
  return p;
}

/** Central Registry rows (any of the five regional files) -> {rows: [{status, date}]}. null result = unavailable. */
function jsiNoiFact_(results) {
  var rows = [], failed = 0;
  (results || []).forEach(function (r) {
    if (r === null) { failed++; return; }
    r.forEach(function (x) { rows.push({ status: String(x.additional_id_status || ''), date: String(x.affil_begin_dt || '').slice(0, 10) }); });
  });
  if (!rows.length && failed) return { unavailable: true };
  return { rows: rows };
}

/**
 * Why this entry's hook is no longer fit to send today, or '' if it is.
 * hook = {kind: NOI|NONE, id: TXR15...., cited: YYYY-MM-DD (the record date the copy cites)}
 * fact = {rows: [{status, date}]} from the live Central Registry, or {unavailable: true}.
 * Mirrored in ops/routines/tools/jsi_common.py noi_problem (tests keep them equal).
 */
function noiProblem_(hook, fact, today) {
  if (!hook || hook.kind === 'NONE') return '';
  if (hook.kind !== 'NOI') return 'unknown hook kind ' + hook.kind;
  if (!fact || fact.unavailable) return 'TCEQ Central Registry unavailable';
  var rows = fact.rows || [];
  if (!rows.length) return 'authorization ' + hook.id + ' not found on the Central Registry';
  var active = rows.filter(function (r) { return String(r.status || '').toUpperCase() === 'ACTIVE'; });
  if (!active.length) return 'authorization ' + hook.id + ' is ' + (rows[0].status || 'not ACTIVE');
  var dates = {};
  active.forEach(function (r) { dates[String(r.date || '').slice(0, 10)] = 1; });
  var list = Object.keys(dates).sort();
  if (hook.cited && !dates[hook.cited]) return 'cited record date ' + hook.cited + ' is not on the live record (' + list.join(', ') + ')';
  var age = Math.round((Date.parse(today) - Date.parse(hook.cited)) / 86400000);
  if (age > JPUB.SITE_WINDOW_D) return 'record date ' + hook.cited + ' is ' + age + ' days before ' + today + ' (over ' + JPUB.SITE_WINDOW_D + ')';
  return '';
}

/**
 * What the JSI publisher should do today.
 * s = {sendDay, manifestsToday: [decoded manifests for today, both businesses], liveRowsToday: LIVE Sender Log rows
 *      for JI- entries today, prepared, preparedError}
 */
function jsiPublishDecision_(s) {
  if (!s.sendDay) return { action: 'NONE', why: 'not a send day' };
  if (s.liveRowsToday > 0) return { action: 'SENDING', why: 'the sender already worked on Jobsite rows today (' + s.liveRowsToday + '); never republish' };
  var valid = (s.manifestsToday || []).filter(function (m) { return m.business === JPUB.BUSINESS && m.entries.length && m.dry_run_only === false; });
  if (valid.length) return { action: 'KEEP', why: 'a valid Jobsite manifest for today exists (' + valid[0].entries.length + ' entries)' };
  if (!s.prepared) return { action: 'MISSING', why: s.preparedError || 'no JSI prepared batch for today' };
  return { action: 'PUBLISH', why: 'no valid Jobsite manifest yet' };
}

/** The manifest object (the shape ji_ops.build_manifest writes) for the entries that passed today. */
function jsiBuildManifest_(prepared, entries, nowIso) {
  return {
    version: 1, send_date: prepared.send_date, created_at: nowIso, business: prepared.business,
    dry_run_only: false, max_total: prepared.max_total, max_s1: prepared.max_s1, share: prepared.share,
    aliases: prepared.aliases, dnc_emails: prepared.dnc_emails, dnc_domains: prepared.dnc_domains,
    entries: entries.map(function (e) {
      var o = {}; Object.keys(e).forEach(function (k) { if (k !== 'hook') o[k] = e[k]; }); return o;
    })
  };
}

/** Owner alert text, or null when nothing needs the user. */
function jsiWatchdogReport_(w) {
  var failed = [], action = [];
  if (!w.sendDay) return null;
  if (!w.manifestOk) {
    failed.push('No valid Jobsite manifest for ' + w.today + ' by ' + w.at + ' Central (' + (w.manifestWhy || 'not found') + ').');
    action.push(w.preparedOk ? 'Open Apps Script (ASI Sender) and run jsiPublishManifest once; check the Sender Log for JSI-PUBLISH rows.'
      : 'No JSI prepared batch was staged for today: the JSI close-out did not finish. Open Claude and run the JSI close-out, or accept no Jobsite sends today.');
  }
  if (w.mode !== 'LIVE') { failed.push('Sender MODE is ' + w.mode + '.'); action.push('Apps Script > Project Settings > Script properties: set MODE to LIVE (if sending should resume).'); }
  if (!w.senderTrigger) { failed.push('runSender trigger is missing.'); action.push('Apps Script: run installTrigger once.'); }
  if (!w.publisherTrigger) { failed.push('jsiPublishManifest triggers are missing.'); action.push('Apps Script: run installJsiPublisher once.'); }
  if (!failed.length) return null;
  return { subject: 'ACTION NEEDED: JSI pre-send ' + w.today,
    body: 'What failed:\n- ' + failed.join('\n- ') + '\n\nWhat was retried:\n- ' + ((w.retries || []).join('\n- ') || 'nothing') +
      '\n\nWhat to do:\n- ' + action.join('\n- ') + '\n\n(JSI watchdog in the ASI Sender Apps Script; runs in Google, not on the PC.)' };
}

/** After the window: Jobsite entries neither sent nor skipped. Null when all is accounted for. */
function jsiConfirmReport_(today, man, state) {
  if (!man) return null;
  var pending = man.entries.filter(function (e) { var s = state[e.outreach_id]; return s !== 'sent' && s !== 'skipped'; });
  if (!pending.length) return null;
  return { subject: 'ACTION NEEDED: JSI sends not confirmed ' + today,
    body: 'What failed:\n- ' + pending.length + ' of ' + man.entries.length + ' Jobsite manifest entries were not sent or skipped by 5 PM: ' +
      pending.slice(0, 15).map(function (e) { return e.outreach_id + ' ' + e.to + ' (' + (state[e.outreach_id] || 'not reached') + ')'; }).join(', ') +
      '\n\nWhat was retried:\n- runSender retries every 10 minutes during the window; entries marked "sending" or "error" are never retried automatically.' +
      '\n\nWhat to do:\n- Check the Sender Log and Gmail Sent (from sites@) for these recipients before anything is re-planned. ' +
      'The next JSI close-out reconciles and re-plans unsent drafts once.' };
}

/** Minutes after midnight: when the last JSI publish run can still be working vs. the earliest JSI watchdog. */
function jsiScheduleMargins_() {
  var last = JPUB.PUBLISH_AT[JPUB.PUBLISH_AT.length - 1];
  return { lastPublishDone: last[0] * 60 + last[1] + JPUB.JITTER_MIN + JPUB.RUN_LIMIT_MIN,
    watchdogEarliest: JPUB.WATCHDOG_AT[0] * 60 + JPUB.WATCHDOG_AT[1] - JPUB.JITTER_MIN, sendStart: CFG.HOURS[0] * 60 };
}

// ---------------------------------------------------------------- Apps Script glue

/** Safe to rerun: removes only the JSI publisher's own triggers, then creates them once. Nothing of ASI's is touched. */
function installJsiPublisher() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (JPUB.HANDLERS.indexOf(t.getHandlerFunction()) >= 0) ScriptApp.deleteTrigger(t);
  });
  JPUB.PUBLISH_AT.map(function (x) { return [x[0], x[1], 'jsiPublishManifest']; })
    .concat([[JPUB.WATCHDOG_AT[0], JPUB.WATCHDOG_AT[1], 'jsiWatchdog'], [JPUB.CONFIRM_AT[0], JPUB.CONFIRM_AT[1], 'jsiConfirmSends']])
    .forEach(function (x) {
      ScriptApp.newTrigger(x[2]).timeBased().atHour(x[0]).nearMinute(x[1]).everyDays(1).inTimezone(CFG.TZ).create();
    });
  var names = ScriptApp.getProjectTriggers().map(function (t) { return t.getHandlerFunction(); });
  Logger.log('Triggers now: ' + JSON.stringify(names.reduce(function (o, n) { o[n] = (o[n] || 0) + 1; return o; }, {})));
}

/** Rollback: removes the JSI publisher's triggers only. ASI's publisher and runSender are untouched. */
function removeJsiPublisher() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (JPUB.HANDLERS.indexOf(t.getHandlerFunction()) >= 0) ScriptApp.deleteTrigger(t);
  });
  Logger.log('JSI publisher triggers removed; ASI publisher and runSender untouched.');
}

function jsiTodayInfo_() {
  var now = new Date();
  return { now: now, today: Utilities.formatDate(now, CFG.TZ, 'yyyy-MM-dd'), dow: Number(Utilities.formatDate(now, CFG.TZ, 'u')) };
}

function jsiLiveRowsToday_(today) {
  var sid = PropertiesService.getScriptProperties().getProperty('LOG_SHEET_ID');
  if (!sid) return 0;
  var rows = SpreadsheetApp.openById(sid).getSheets()[0].getDataRange().getValues();
  return rows.filter(function (r) {
    return String(r[0]).indexOf(today) === 0 && r[1] === 'LIVE' && String(r[3]).indexOf(JPUB.ID_PREFIX) === 0;
  }).length;
}

function jsiPreparedForToday_(today, nowMs) {
  var best = null, err = '';
  var resp = Gmail.Users.Drafts.list('me', { q: 'subject:"' + JPUB.PREPARED_PREFIX + ' ' + today + '"', maxResults: 20 });
  (resp.drafts || []).forEach(function (d) {
    var m = GmailApp.getDraft(d.id).getMessage();
    if (parseAddresses_(m.getTo()).join(',') !== CFG.OWNER) return;
    try {
      var p = jsiDecodePrepared_(m.getSubject(), m.getPlainBody(), today, nowMs, sha256Hex_,
        function (s) { return Utilities.base64Decode(s); },
        function (b) { return Utilities.newBlob(b).getDataAsString('UTF-8'); },
        function (b) { return Utilities.ungzip(Utilities.newBlob(b, 'application/x-gzip')).getBytes(); });
      if (!best || p.prepared_at > best.prepared_at) best = p;
    } catch (e) { err = String(e); }
  });
  return { prepared: best, error: err };
}

function jsiFetchJson_(url) {
  for (var i = 0; i < 3; i++) {
    try {
      var r = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
      if (r.getResponseCode() === 200) return JSON.parse(r.getContentText());
    } catch (e) { /* retry */ }
    Utilities.sleep(2000 * (i + 1));
  }
  return null;
}

/** Live Central Registry rows for one authorization (all five regional files). */
function jsiFetchHookFact_(h) {
  if (!h || h.kind !== 'NOI') return {};
  var where = encodeURIComponent("program_code='STORM' AND additional_id_text='" + String(h.id).replace(/[^A-Z0-9]/g, '') + "'");
  return jsiNoiFact_(JPUB.TCEQ_FILES.map(function (ds) {
    return jsiFetchJson_('https://data.texas.gov/resource/' + ds + '.json?$select=additional_id_status,affil_begin_dt&$limit=50&$where=' + where);
  }));
}

function jsiPublishManifest() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) return;            // ASI's publisher holds it; the next JSI run continues
  try {
    var t = jsiTodayInfo_(), props = PropertiesService.getScriptProperties(), key = 'jsipublish:' + t.today;
    var history = JSON.parse(props.getProperty(key) || '[]');
    var prep = jsiPreparedForToday_(t.today, t.now.getTime());
    var d = jsiPublishDecision_({ sendDay: jsiIsSendDay_(t.today, t.dow), manifestsToday: loadManifests_(t.today, t.now.getTime()),
      liveRowsToday: jsiLiveRowsToday_(t.today), prepared: prep.prepared, preparedError: prep.error });
    history.push(Utilities.formatDate(t.now, CFG.TZ, 'HH:mm') + ' ' + d.action + ': ' + d.why);
    if (d.action !== 'PUBLISH') { props.setProperty(key, JSON.stringify(history)); jsiLog_(d.action, d.why); return; }

    var p = prep.prepared, kept = [], dropped = [], started = Date.now();
    var man0 = { aliases: p.aliases, dnc_emails: p.dnc_emails, dnc_domains: p.dnc_domains };
    var ckey = 'jsipubcheck:' + t.today + ':' + p.sha, checked = JSON.parse(props.getProperty(ckey) || '{}');
    for (var i = 0; i < p.entries.length; i++) {
      var e = p.entries[i];
      if (checked[e.outreach_id] === undefined) {
        if (Date.now() - started > JPUB.TIME_BUDGET_MS) {
          props.setProperty(ckey, JSON.stringify(checked));
          history.push('checked ' + Object.keys(checked).length + ' of ' + p.entries.length + '; continuing on the next run');
          props.setProperty(key, JSON.stringify(history)); jsiLog_('PARTIAL', 'checked ' + Object.keys(checked).length + ' of ' + p.entries.length);
          return;
        }
        var why = [];
        try { why = checkEntry_(e, gatherFacts_(e), man0, sha256Utf8_); } catch (err) { why = ['check error: ' + err]; }
        if (!why.length) { var hp = noiProblem_(e.hook, jsiFetchHookFact_(e.hook || {}), t.today); if (hp) why.push(hp); }
        checked[e.outreach_id] = why.join('; ');
        props.setProperty(ckey, JSON.stringify(checked));
        if (why.length) jsiLog_('DROPPED', why.join('; '), e);
      }
      if (checked[e.outreach_id]) dropped.push(e.outreach_id + ': ' + checked[e.outreach_id]); else kept.push(e);
    }
    if (!kept.length) {
      history.push('nothing passed the re-check (' + dropped.length + ' dropped)');
      props.setProperty(key, JSON.stringify(history)); jsiLog_('NOTHING', 'all ' + dropped.length + ' entries dropped'); return;
    }
    var man = jsiBuildManifest_(p, kept, new Date().toISOString().replace(/\.\d{3}Z$/, '+00:00'));
    var bytes = Utilities.newBlob(JSON.stringify(man), 'application/json').getBytes();
    var gz = Utilities.gzip(Utilities.newBlob(bytes, 'application/json')).getBytes();
    var subject = 'ASI-MANIFEST v1 ' + t.today + ' ' + sha256Hex_(bytes);   // the shared sender's manifest format
    GmailApp.createDraft(CFG.OWNER, subject, Utilities.base64Encode(gz).replace(/(.{76})/g, '$1\n'));
    var check = loadManifests_(t.today, Date.now()).filter(function (m) { return m.sha === subject.split(' ').pop(); });
    history.push('PUBLISHED ' + kept.length + ' of ' + p.entries.length + (dropped.length ? ' (dropped: ' + dropped.join(' | ') + ')' : '') +
      (check.length ? '; read back OK' : '; READ-BACK FAILED'));
    props.setProperty(key, JSON.stringify(history));
    jsiLog_(check.length ? 'PUBLISHED' : 'ERROR', kept.length + ' of ' + p.entries.length + ' entries; ' + subject);
  } finally { lock.releaseLock(); }
}

function jsiWatchdog() {
  var t = jsiTodayInfo_(), props = PropertiesService.getScriptProperties();
  var mans = loadManifests_(t.today, t.now.getTime()).filter(function (m) { return m.business === JPUB.BUSINESS && m.entries.length && m.dry_run_only === false; });
  var trig = ScriptApp.getProjectTriggers().map(function (x) { return x.getHandlerFunction(); });
  var prep = jsiPreparedForToday_(t.today, t.now.getTime());
  var rep = jsiWatchdogReport_({ sendDay: jsiIsSendDay_(t.today, t.dow), today: t.today, at: '7:50 AM', manifestOk: mans.length > 0,
    manifestWhy: prep.error, preparedOk: !!prep.prepared, mode: props.getProperty('MODE') || 'DRY_RUN',
    senderTrigger: trig.indexOf('runSender') >= 0, publisherTrigger: trig.indexOf('jsiPublishManifest') >= 0,
    retries: JSON.parse(props.getProperty('jsipublish:' + t.today) || '[]') });
  if (rep) { GmailApp.sendEmail(CFG.OWNER, rep.subject, rep.body); jsiLog_('ALERT', rep.subject); }
  else jsiLog_('WATCHDOG OK', 'Jobsite manifest, MODE and triggers in place');
}

function jsiConfirmSends() {
  var t = jsiTodayInfo_();
  if (!jsiIsSendDay_(t.today, t.dow)) return;
  var props = PropertiesService.getScriptProperties();
  var man = loadManifests_(t.today, t.now.getTime()).filter(function (m) { return m.business === JPUB.BUSINESS && m.dry_run_only === false; })[0];
  if (!man) {
    var hist = JSON.parse(props.getProperty('jsipublish:' + t.today) || '[]');
    GmailApp.sendEmail(CFG.OWNER, 'ACTION NEEDED: no Jobsite manifest ran ' + t.today,
      'What failed:\n- No valid Jobsite manifest was found for today, so no Jobsite email was sent.\n\nWhat was retried:\n- ' +
      (hist.join('\n- ') || 'nothing') + '\n\nWhat to do:\n- Run the JSI close-out in Claude so a prepared batch exists for the next send day.');
    return;
  }
  var rep = jsiConfirmReport_(t.today, man, JSON.parse(props.getProperty('state:LIVE:' + man.sha) || '{}'));
  if (rep) { GmailApp.sendEmail(CFG.OWNER, rep.subject, rep.body); jsiLog_('ALERT', rep.subject); }
  else jsiLog_('CONFIRMED', man.entries.length + ' Jobsite entries sent or skipped');
}

/** Run once by hand after pasting the file: proves the JSI alert route (an email to operations@ from Google). */
function jsiTestAlert() {
  var t = jsiTodayInfo_();
  GmailApp.sendEmail(CFG.OWNER, 'TEST ALERT (no action needed): JSI watchdog route ' + t.today,
    'This is a test of the Jobsite off-PC alert route. Real alerts start with "ACTION NEEDED" and say what failed, what was retried and what to do.');
  jsiLog_('TEST ALERT', 'sent to ' + CFG.OWNER);
}

function jsiLog_(result, detail, e) {
  log_(JPUB.LOG_MODE, result, e || { outreach_id: '', stage: '', to: '', from_alias: '' }, detail, '');
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { JPUB: JPUB, jsiIsSendDay_: jsiIsSendDay_, jsiDecodePrepared_: jsiDecodePrepared_, jsiNoiFact_: jsiNoiFact_,
    noiProblem_: noiProblem_, jsiPublishDecision_: jsiPublishDecision_, jsiBuildManifest_: jsiBuildManifest_,
    jsiWatchdogReport_: jsiWatchdogReport_, jsiConfirmReport_: jsiConfirmReport_, jsiScheduleMargins_: jsiScheduleMargins_,
    installJsiPublisher: installJsiPublisher, removeJsiPublisher: removeJsiPublisher };
}
