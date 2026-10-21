/**
 * ASI Sender (Google Apps Script, runs inside the operations@asterfieldgroup.com account).
 *
 * Sends the day's approved cold emails (S1-S5) from the right city alias. It sends nothing
 * that is not on the day's manifest, and only after every check below passes. Setup and
 * daily use: ops/sender/README.md.
 *
 * How a send is authorized:
 *   1. Operations validates each email (scripts/asi_ops.py) and creates it as a Gmail draft.
 *   2. Operations creates one manifest draft (subject "ASI-MANIFEST v1 <date> <sha256>") that
 *      lists those drafts: recipient, subject, approved text, alias, thread.
 *   3. This script re-checks every listed draft against the manifest and Gmail before sending,
 *      then sends the draft itself (Gmail deletes a draft once it is sent, so nothing can be
 *      sent twice). Any failed check skips that email and logs why; it is never "fixed".
 *
 * Script property MODE (Project Settings > Script properties):
 *   DRY_RUN (default)  check everything, log what would be sent, send nothing
 *   TEST               send up to TEST_LIMIT copies to TEST_TO (an @asterfieldgroup.com
 *                      address) instead of the prospect; drafts are left untouched
 *   LIVE               send to prospects, a few per run, only on weekdays 8am-5pm Central
 *   PAUSED             do nothing (set automatically on too many bounces)
 */

var CFG = {
  DOMAIN: 'asterfieldgroup.com',
  OWNER: 'operations@asterfieldgroup.com',
  MANIFEST_RE: /^ASI-MANIFEST v1 (\d{4}-\d{2}-\d{2}) ([0-9a-f]{64})$/,
  STAGES: ['S1', 'S2', 'S3', 'S4', 'S5'],
  PER_RUN: 4,            // sends per trigger run (runs every 10 minutes)
  GAP_MS: [40000, 70000],
  TZ: 'America/Chicago',
  HOURS: [8, 17],        // LIVE sends only from 8:00 to 16:59 Central, Monday to Friday
  BOUNCE_PAUSE: 3,       // bounces in the last 24 hours that pause all sending
  MANIFEST_MAX_AGE_H: 36,
  TEST_LIMIT: 4,
  EMAIL_RE: /[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g,
  // Personal-mail domains: many unrelated people share them, so the one-company domain check skips them.
  FREE: ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'live.com', 'msn.com',
    'sbcglobal.net', 'att.net', 'comcast.net', 'me.com', 'ymail.com', 'protonmail.com', 'mail.com']
};

// ---------------------------------------------------------------- pure helpers (unit-tested)

function collapse_(s) {
  return String(s || '').replace(/\s+/g, ' ').trim();
}

function parseAddresses_(header) {
  var out = [];
  (String(header || '').match(CFG.EMAIL_RE) || []).forEach(function (e) {
    e = e.toLowerCase();
    if (out.indexOf(e) < 0) out.push(e);
  });
  return out;
}

function domainOf_(email) {
  return String(email).split('@').pop().toLowerCase();
}

/** Plain text of a Gmail HTML body (line breaks, tags, entities), for drafts that have no text part. */
function htmlToText_(html) {
  return String(html || '')
    .replace(/<br\s*\/?>/gi, '\n').replace(/<\/(div|p|blockquote)>/gi, '\n')
    .replace(/<[^>]*>/g, '')
    .replace(/&#(\d+);/g, function (_, n) { return String.fromCharCode(Number(n)); })
    .replace(/&#x([0-9a-f]+);/gi, function (_, n) { return String.fromCharCode(parseInt(n, 16)); })
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
}

/** The alias whose address appears last in the text (the signature line). */
function aliasInSignature_(text, aliases) {
  var low = String(text).toLowerCase(), best = '', at = -1;
  aliases.forEach(function (a) {
    var i = low.lastIndexOf(a.toLowerCase());
    if (i > at) { at = i; best = a.toLowerCase(); }
  });
  return best;
}

/** Validate and decode a manifest draft. Throws on any problem. */
function decodeManifest_(subject, body, today, nowMs, sha256Hex, b64Decode, utf8, gunzip) {
  var m = CFG.MANIFEST_RE.exec(String(subject || '').trim());
  if (!m) throw new Error('not a manifest subject');
  var bytes;
  try { bytes = gunzip(b64Decode(String(body || '').replace(/[^A-Za-z0-9+/=]/g, ''))); }
  catch (err) { throw new Error('manifest checksum mismatch (damaged or edited): ' + err); }
  if (sha256Hex(bytes) !== m[2]) throw new Error('manifest checksum mismatch (damaged or edited)');
  var man = JSON.parse(utf8(bytes));
  if (man.version !== 1) throw new Error('unknown manifest version');
  if (man.send_date !== m[1]) throw new Error('manifest date does not match its subject');
  if (man.send_date !== today) throw new Error('manifest is for ' + man.send_date + ', not today');
  var age = (nowMs - Date.parse(man.created_at)) / 3600000;
  if (!(age >= -1 && age <= CFG.MANIFEST_MAX_AGE_H)) throw new Error('manifest is too old');
  if (!Array.isArray(man.entries)) throw new Error('manifest has no entries');
  man.sha = m[2];
  return man;
}

/**
 * Every reason this entry must NOT be sent. Empty array = safe to send.
 * f = facts read from Gmail (see gatherFacts_); man = the manifest;
 * sha256Utf8(text) = hex SHA-256 of the text's UTF-8 bytes.
 */
function checkEntry_(e, f, man, sha256Utf8) {
  var r = [];
  var aliases = Object.keys(man.aliases || {}).map(function (a) { return a.toLowerCase(); });
  var to = String(e.to || '').toLowerCase();
  if (CFG.STAGES.indexOf(e.stage) < 0) r.push('stage ' + e.stage + ' is not a cold-email stage');
  if (!to || parseAddresses_(to).length !== 1 || parseAddresses_(to)[0] !== to) r.push('bad recipient in manifest');
  if (domainOf_(to) === CFG.DOMAIN) r.push('recipient is our own domain');
  if ((e.stage === 'S1') === Boolean(e.is_reply)) r.push('S1 must be a new thread and S2-S5 must be replies');
  if (!f.draftFound) { r.push('draft not found (already sent or deleted)'); return r; }

  // Recipient: exactly the approved address, nobody else.
  if (f.draftTo.length !== 1 || f.draftTo[0] !== to) r.push('draft To is ' + f.draftTo.join(',') + ', approved ' + to);
  if (f.draftCc.length || f.draftBcc.length) r.push('draft has Cc/Bcc');

  // Content: subject exact; the draft text is exactly the approved text (a follow-up may carry
  // Gmail's quoted history after it; a first email may not have anything after it).
  if (String(f.draftSubject).trim() !== String(e.subject).trim()) r.push('subject differs from the approved subject');
  // Gmail may hold the draft as text or as HTML only; either reading must match exactly.
  var n = Number(e.body_len) || 0, approved = '';
  var textOk = n > 0 && /^[0-9a-f]{64}$/.test(String(e.body_sha256)) &&
    [f.draftBody, htmlToText_(f.draftHtml)].some(function (raw) {
      var body = collapse_(raw);
      var ok = body.length >= n && sha256Utf8(body.slice(0, n)) === e.body_sha256 && (e.is_reply || body.length === n);
      if (ok) approved = body.slice(0, n);
      return ok;
    });
  if (!textOk) r.push('body differs from the approved text (edited after approval?)');

  // Sender: the signature's alias, the manifest's alias and a verified Gmail alias must agree.
  var alias = String(e.from_alias || '').toLowerCase();
  if (aliases.indexOf(alias) < 0) r.push('alias ' + alias + ' is not one of the city aliases');
  if (aliasInSignature_(approved, aliases) !== alias) r.push('signature alias does not match ' + alias);
  if ((man.aliases || {})[e.from_alias] !== e.display_name) r.push('display name does not match the alias');
  if (f.aliasesAvailable.indexOf(alias) < 0) r.push(alias + ' is not a verified Send-mail-as alias');

  // Do not contact, replies, bounces.
  if ((man.dnc_emails || []).indexOf(to) >= 0 || (man.dnc_domains || []).indexOf(domainOf_(to)) >= 0) r.push('do-not-contact');
  if (f.recipientWroteUs) r.push('recipient has written to us; handle by hand');
  if (f.bounced) r.push('an earlier email to this address bounced');

  // Thread: the draft is where it was approved, and nothing new has happened in it.
  if (f.draftThreadId !== e.thread_id) r.push('draft moved to a different thread');
  var msgs = f.threadMessages;
  if (e.is_reply) {
    if (!/^re:/i.test(String(e.subject))) r.push('reply subject must start with Re:');
    if (!msgs.length) r.push('reply thread has no earlier message');
    msgs.forEach(function (m) {
      if (domainOf_(m.from) !== CFG.DOMAIN) r.push('thread has a message from ' + m.from);
      if (m.to.indexOf(to) < 0) r.push('thread has a message not addressed to ' + to);
    });
    if (msgs.length && msgs[msgs.length - 1].id !== e.reply_to_message_id) r.push('thread changed since approval (new message)');
  } else {
    if (msgs.length) r.push('first email draft is inside an existing thread');
    if (f.sentToBefore > 0) r.push('we have already emailed this address');
    // One company, one business: nobody at this company has written to us or heard from any alias.
    if (CFG.FREE.indexOf(domainOf_(to)) < 0 && f.domainSeen > 0) {
      r.push('someone at ' + domainOf_(to) + ' already has email with us (either business); handle by hand');
    }
  }
  return r;
}

/** Split raw MIME bytes into an ASCII header string, the blank-line separator and body bytes. */
function splitMime_(bytes) {
  var b = bytes.map(function (x) { return x & 0xff; });
  for (var i = 0; i < b.length - 1; i++) {
    var crlf = b[i] === 13 && b[i + 1] === 10 && b[i + 2] === 13 && b[i + 3] === 10;
    var lf = b[i] === 10 && b[i + 1] === 10;
    if (crlf || lf) {
      var end = crlf ? i + 2 : i + 1, sepLen = crlf ? 2 : 1;   // header keeps its own last line break
      var head = '';
      for (var j = 0; j < end; j++) {
        if (b[j] > 127) throw new Error('non-ASCII byte in headers');
        head += String.fromCharCode(b[j]);
      }
      return { header: head, sep: crlf ? '\r\n' : '\n', body: bytes.slice(end + sepLen) };
    }
  }
  throw new Error('no header/body separator');
}

/**
 * The bytes of a Gmail API `raw` field. Apps Script's Gmail service returns it already
 * decoded (a byte array); the REST API returns base64url text. Accept either.
 */
function rawBytes_(raw, b64Decode) {
  if (Array.isArray(raw)) return raw;
  if (raw && typeof raw === 'object' && typeof raw.length === 'number') return Array.prototype.slice.call(raw);
  var s = String(raw || '').replace(/-/g, '+').replace(/_/g, '/').replace(/\s+/g, '');
  while (s.length % 4) s += '=';
  return b64Decode(s);
}

function asciiBytes_(s) {
  var out = [];
  for (var i = 0; i < s.length; i++) {
    var c = s.charCodeAt(i);
    if (c > 127) throw new Error('non-ASCII header text');
    out.push(c);
  }
  return out;
}

/** Logical header lines (folded continuations joined to their header). */
function headerBlocks_(header) {
  var nl = header.indexOf('\r\n') >= 0 ? '\r\n' : '\n';
  var lines = header.split(nl);
  if (lines[lines.length - 1] === '') lines.pop();
  var blocks = [];
  lines.forEach(function (ln) {
    if (/^[ \t]/.test(ln) && blocks.length) blocks[blocks.length - 1].push(ln);
    else blocks.push([ln]);
  });
  return { nl: nl, blocks: blocks };
}

function headerName_(block) {
  return block[0].split(':')[0].trim().toLowerCase();
}

function getHeader_(header, name) {
  var hb = headerBlocks_(header);
  for (var i = 0; i < hb.blocks.length; i++) {
    if (headerName_(hb.blocks[i]) === name.toLowerCase()) {
      return hb.blocks[i].join(' ').replace(/^[^:]*:\s*/, '');
    }
  }
  return '';
}

/** Replace the one From header. Refuses if there is not exactly one. */
function replaceFromHeader_(header, display, alias) {
  if (!/^[A-Za-z0-9 .&,'-]+$/.test(display)) throw new Error('unsafe display name');
  if (!/^[a-z0-9._-]+@[a-z0-9.-]+$/.test(alias)) throw new Error('unsafe alias');
  var hb = headerBlocks_(header), hits = 0;
  hb.blocks = hb.blocks.map(function (bl) {
    if (headerName_(bl) !== 'from') return bl;
    hits++;
    return ['From: "' + display + '" <' + alias + '>'];
  });
  if (hits !== 1) throw new Error('expected exactly one From header, found ' + hits);
  return hb.blocks.map(function (bl) { return bl.join(hb.nl); }).join(hb.nl) + hb.nl;
}

/** TEST mode: same message, but to testTo only, out of the prospect's thread, subject marked. */
function rewriteForTest_(header, testTo) {
  if (domainOf_(testTo) !== CFG.DOMAIN) throw new Error('TEST_TO must be an @' + CFG.DOMAIN + ' address');
  var hb = headerBlocks_(header), drop = ['cc', 'bcc', 'in-reply-to', 'references'];
  var out = [];
  hb.blocks.forEach(function (bl) {
    var n = headerName_(bl);
    if (drop.indexOf(n) >= 0) return;
    if (n === 'to') { out.push(['To: <' + testTo + '>']); return; }
    if (n === 'subject') { out.push([bl[0].replace(/^(subject:\s*)/i, '$1[TEST] ')].concat(bl.slice(1))); return; }
    out.push(bl);
  });
  return out.map(function (bl) { return bl.join(hb.nl); }).join(hb.nl) + hb.nl;
}

/**
 * The day's sending order across every manifest (ASI's and Jobsite's share one mailbox):
 * all first emails (S1) before any follow-up; within each, the manifests take turns and each
 * keeps its own order. Returns [{man, e}].
 */
function orderEntries_(manifests) {
  var out = [];
  [true, false].forEach(function (firstTier) {
    var lists = manifests.map(function (man) {
      return man.entries.filter(function (e) { return (e.stage === 'S1') === firstTier; })
        .map(function (e) { return { man: man, e: e }; });
    });
    for (var i = 0; lists.some(function (l) { return i < l.length; }); i++) {
      lists.forEach(function (l) { if (i < l.length) out.push(l[i]); });
    }
  });
  return out;
}

/**
 * The mailbox's daily caps: the strictest of the day's manifests (60 total; S1 counts toward it),
 * plus each business's share of that total (ASI 45, Jobsite 15; a manifest without one may use it all).
 */
function sharedCaps_(manifests) {
  // The total is the mailbox's and the strictest manifest wins. Each business keeps its own share and its own
  // first-email cap (Oct 21: Jobsite's 5 had capped ASI's first emails at 5, counted across both businesses).
  var total = Infinity, s1 = Infinity, share = {}, s1By = {};
  manifests.forEach(function (m) {
    total = Math.min(total, Number(m.max_total) || 0);
    s1 = Math.min(s1, Number(m.max_s1) || 0);
    var b = m.business || '', mine = m.share === undefined ? Infinity : (Number(m.share) || 0);
    share[b] = Math.min(share[b] === undefined ? Infinity : share[b], mine);
    s1By[b] = Math.min(s1By[b] === undefined ? Infinity : s1By[b], Number(m.max_s1) || 0);
  });
  return { total: total, s1: s1, share: share, s1By: s1By };
}

/** Every manifest's do-not-contact applies to every email of the day, whichever business sends it. */
function unionDnc_(manifests) {
  var emails = [], domains = [];
  manifests.forEach(function (m) {
    (m.dnc_emails || []).forEach(function (x) { if (emails.indexOf(x) < 0) emails.push(x); });
    (m.dnc_domains || []).forEach(function (x) { if (domains.indexOf(x) < 0) domains.push(x); });
  });
  return { dnc_emails: emails, dnc_domains: domains };
}

/** True when this run may only check and log the manifest's emails: DRY_RUN, or a test manifest. */
function checkOnly_(mode, man) {
  return mode === 'DRY_RUN' || man.dry_run_only !== false;
}

function inWindow_(date, tz, fmt) {
  var dow = Number(fmt(date, tz, 'u'));          // 1 = Monday ... 7 = Sunday
  var hour = Number(fmt(date, tz, 'H'));
  return dow >= 1 && dow <= 5 && hour >= CFG.HOURS[0] && hour < CFG.HOURS[1];
}

// ---------------------------------------------------------------- Apps Script glue

function setup() {
  var props = PropertiesService.getScriptProperties();
  if (!props.getProperty('MODE')) props.setProperty('MODE', 'DRY_RUN');
  if (!props.getProperty('TEST_TO')) props.setProperty('TEST_TO', CFG.OWNER);
  if (!props.getProperty('LOG_SHEET_ID')) {
    var ss = SpreadsheetApp.create('ASI Sender Log');
    ss.getSheets()[0].appendRow(['time (Central)', 'mode', 'result', 'outreach_id', 'stage', 'to', 'from', 'detail', 'message_id']);
    props.setProperty('LOG_SHEET_ID', ss.getId());
  }
  Logger.log('Mode: ' + props.getProperty('MODE') + '. Aliases Gmail can send as: ' + GmailApp.getAliases().join(', '));
  Logger.log('Log sheet: https://docs.google.com/spreadsheets/d/' + props.getProperty('LOG_SHEET_ID'));
}

function installTrigger() {
  removeTriggers();
  ScriptApp.newTrigger('runSender').timeBased().everyMinutes(10).create();
  Logger.log('runSender will run every 10 minutes.');
}

function removeTriggers() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'runSender') ScriptApp.deleteTrigger(t);
  });
}

function runSender() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;
  try {
    var props = PropertiesService.getScriptProperties();
    var mode = props.getProperty('MODE') || 'DRY_RUN';
    if (['DRY_RUN', 'TEST', 'LIVE'].indexOf(mode) < 0) return;
    var now = new Date();
    if (mode === 'LIVE' && !inWindow_(now, CFG.TZ, Utilities.formatDate)) return;
    var bounces = GmailApp.search('from:(mailer-daemon OR postmaster) newer_than:1d').length;
    if (bounces >= CFG.BOUNCE_PAUSE) { pause_(bounces + ' bounces in the last 24 hours'); return; }

    var today = Utilities.formatDate(now, CFG.TZ, 'yyyy-MM-dd');
    var manifests = loadManifests_(today, now.getTime());
    if (!manifests.length) return;
    // One mailbox, one set of daily caps, whichever business a manifest belongs to.
    var caps = sharedCaps_(manifests), dnc = unionDnc_(manifests);
    var states = {}, sends = 0, sentToday = 0, tests = 0, byBiz = {}, s1ByBiz = {};
    manifests.forEach(function (mf) {
      var live = JSON.parse(props.getProperty('state:LIVE:' + mf.sha) || '{}');
      sentToday += countValues_(live, 'sent');
      byBiz[mf.business || ''] = (byBiz[mf.business || ''] || 0) + countValues_(live, 'sent');
      s1ByBiz[mf.business || ''] = (s1ByBiz[mf.business || ''] || 0) + countStage_(mf, live, 'S1');
      states[mf.sha] = JSON.parse(props.getProperty('state:' + mode + ':' + mf.sha) || '{}');
      tests += countValues_(states[mf.sha], 'test');
    });
    var testLimit = Number(props.getProperty('TEST_LIMIT') || CFG.TEST_LIMIT);
    var queue = orderEntries_(manifests);              // first emails of every manifest before any follow-up
    for (var j = 0; j < queue.length; j++) {
      var man = queue[j].man, e = queue[j].e;
      var key = 'state:' + mode + ':' + man.sha, state = states[man.sha];
      if (state[e.outreach_id]) continue;
      if (mode === 'TEST' && tests >= testLimit) return;
      if (mode !== 'DRY_RUN' && sends >= CFG.PER_RUN) return;
      var biz = man.business || '';
      if (mode === 'LIVE' && (sentToday >= caps.total || (byBiz[biz] || 0) >= caps.share[biz] ||
          (e.stage === 'S1' && (s1ByBiz[biz] || 0) >= caps.s1By[biz]))) {
        log_(mode, 'CAP', e, 'daily cap reached; left as a draft', ''); continue;
      }
      var reasons;
      try { reasons = checkEntry_(e, gatherFacts_(e), Object.assign({}, man, dnc), sha256Utf8_); } catch (err) { reasons = ['check error: ' + err]; }
      if (reasons.length) {
        if (mode !== 'DRY_RUN') { state[e.outreach_id] = 'skipped'; props.setProperty(key, JSON.stringify(state)); }
        log_(mode, 'SKIP', e, reasons.join('; '), '');
        continue;
      }
      // A manifest sends only if it says dry_run_only: false; a test manifest never sends, whatever MODE
      // says (Oct 14: a LIVE run sent the City Waste test email).
      if (checkOnly_(mode, man)) {
        log_(mode, 'WOULD SEND', e, mode === 'DRY_RUN' ? '' : 'test manifest (not marked dry_run_only: false); not sent', '');
        if (mode !== 'DRY_RUN') { state[e.outreach_id] = 'dry_run_only'; props.setProperty(key, JSON.stringify(state)); }
        continue;
      }
      if ((props.getProperty('MODE') || '') !== mode) return;          // kill switch flipped mid-run
      if (sends > 0) Utilities.sleep(CFG.GAP_MS[0] + Math.floor(Math.random() * (CFG.GAP_MS[1] - CFG.GAP_MS[0])));
      state[e.outreach_id] = 'sending';                                   // never retried blindly
      props.setProperty(key, JSON.stringify(state));
      try {
        var id = mode === 'LIVE' ? sendLive_(e) : sendTest_(e, props.getProperty('TEST_TO'));
        state[e.outreach_id] = mode === 'LIVE' ? 'sent' : 'test';
        log_(mode, mode === 'LIVE' ? 'SENT' : 'TEST SENT', e, '', id);
      } catch (err) {
        state[e.outreach_id] = 'error';
        log_(mode, 'ERROR', e, String(err), '');
        pause_('send error on ' + e.outreach_id + ': ' + err);
        props.setProperty(key, JSON.stringify(state));
        return;
      }
      props.setProperty(key, JSON.stringify(state));
      sends++;
      if (mode === 'TEST') tests++;
      if (mode === 'LIVE') { sentToday++; byBiz[biz] = (byBiz[biz] || 0) + 1; if (e.stage === 'S1') s1ByBiz[biz] = (s1ByBiz[biz] || 0) + 1; }
    }
  } finally {
    lock.releaseLock();
  }
}

function loadManifests_(today, nowMs) {
  var out = [];
  GmailApp.getDrafts().forEach(function (d) {
    var m = d.getMessage();
    if (!CFG.MANIFEST_RE.test(m.getSubject())) return;
    if (parseAddresses_(m.getTo()).join(',') !== CFG.OWNER) return;
    try {
      var man = decodeManifest_(m.getSubject(), m.getPlainBody(), today, nowMs, sha256Hex_,
        function (s) { return Utilities.base64Decode(s); },
        function (b) { return Utilities.newBlob(b).getDataAsString('UTF-8'); },
        function (b) { return Utilities.ungzip(Utilities.newBlob(b, 'application/x-gzip')).getBytes(); });
      // The same manifest saved twice is one manifest (ASI's and Jobsite's differ by checksum).
      if (!out.some(function (x) { return x.sha === man.sha; })) out.push(man);
    } catch (err) {
      if (String(err).indexOf('not today') < 0) Logger.log('Ignored manifest "' + m.getSubject() + '": ' + err);
    }
  });
  return out;
}

function sha256Hex_(bytes) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, bytes).map(function (b) {
    return ('0' + (b & 0xff).toString(16)).slice(-2);
  }).join('');
}

function sha256Utf8_(text) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, text, Utilities.Charset.UTF_8).map(function (b) {
    return ('0' + (b & 0xff).toString(16)).slice(-2);
  }).join('');
}

function gatherFacts_(e) {
  var f = { draftFound: false };
  var draft;
  try { draft = GmailApp.getDraft(e.draft_id); } catch (err) { draft = null; }
  if (!draft) return f;
  var m = draft.getMessage(), thread = m.getThread();
  f.draftFound = true;
  f.draftTo = parseAddresses_(m.getTo());
  f.draftCc = parseAddresses_(m.getCc());
  f.draftBcc = parseAddresses_(m.getBcc());
  f.draftSubject = m.getSubject();
  f.draftBody = m.getPlainBody();
  f.draftHtml = m.getBody();
  f.draftThreadId = thread.getId();
  f.threadMessages = thread.getMessages().filter(function (x) { return !x.isDraft(); }).map(function (x) {
    return { id: x.getId(), from: parseAddresses_(x.getFrom())[0] || '', to: parseAddresses_(x.getTo() + ',' + x.getCc()) };
  });
  f.aliasesAvailable = GmailApp.getAliases().map(function (a) { return a.toLowerCase(); });
  f.recipientWroteUs = GmailApp.search('from:' + e.to, 0, 1).length > 0;
  f.bounced = GmailApp.search('from:(mailer-daemon OR postmaster) "' + e.to + '"', 0, 1).length > 0;
  f.sentToBefore = GmailApp.search('in:sent to:' + e.to, 0, 1).length;
  var dom = domainOf_(e.to);
  f.domainSeen = CFG.FREE.indexOf(dom) >= 0 ? 0 :
    GmailApp.search('in:anywhere -in:draft {from:@' + dom + ' to:@' + dom + ' cc:@' + dom + '}', 0, 1).length;
  return f;
}

/** Send the approved draft itself, with only its From header changed to the city alias. */
function sendLive_(e) {
  var d = Gmail.Users.Drafts.get('me', e.draft_id, { format: 'raw' });
  var parts = splitMime_(rawBytes_(d.message.raw, function (s) { return Utilities.base64Decode(s); }));
  var to = parseAddresses_(getHeader_(parts.header, 'To'));
  if (to.length !== 1 || to[0] !== e.to) throw new Error('raw To header is ' + to.join(','));
  if (getHeader_(parts.header, 'Cc') || getHeader_(parts.header, 'Bcc')) throw new Error('raw draft has Cc/Bcc');
  var header = replaceFromHeader_(parts.header, e.display_name, e.from_alias);
  var raw = Utilities.base64EncodeWebSafe(asciiBytes_(header + parts.sep).concat(parts.body));
  Gmail.Users.Drafts.update({ id: e.draft_id, message: { raw: raw, threadId: d.message.threadId } }, 'me', e.draft_id);
  var sent = Gmail.Users.Drafts.send({ id: e.draft_id }, 'me');
  var msg = GmailApp.getMessageById(sent.id);
  var gotTo = parseAddresses_(msg.getTo()), gotFrom = parseAddresses_(msg.getFrom());
  if (gotTo.length !== 1 || gotTo[0] !== e.to || gotFrom[0] !== e.from_alias) {
    throw new Error('sent message check failed: from ' + gotFrom + ' to ' + gotTo);
  }
  return sent.id;
}

/** TEST mode: send a marked copy to our own mailbox; the draft is left untouched. */
function sendTest_(e, testTo) {
  var d = Gmail.Users.Drafts.get('me', e.draft_id, { format: 'raw' });
  var parts = splitMime_(rawBytes_(d.message.raw, function (s) { return Utilities.base64Decode(s); }));
  var header = rewriteForTest_(replaceFromHeader_(parts.header, e.display_name, e.from_alias), testTo);
  var raw = Utilities.base64EncodeWebSafe(asciiBytes_(header + parts.sep).concat(parts.body));
  return Gmail.Users.Messages.send({ raw: raw }, 'me').id;
}

function pause_(why) {
  PropertiesService.getScriptProperties().setProperty('MODE', 'PAUSED');
  log_('PAUSED', 'PAUSED', { outreach_id: '', stage: '', to: '', from_alias: '' }, why, '');
  GmailApp.sendEmail(CFG.OWNER, 'ASI Sender paused', 'The sender paused itself: ' + why +
    '\n\nNothing more will send until MODE is set back to LIVE in the script properties.');
}

function log_(mode, result, e, detail, id) {
  var row = [Utilities.formatDate(new Date(), CFG.TZ, 'yyyy-MM-dd HH:mm:ss'), mode, result,
    e.outreach_id, e.stage, e.to, e.from_alias, detail, id];
  Logger.log(row.join(' | '));
  var sid = PropertiesService.getScriptProperties().getProperty('LOG_SHEET_ID');
  if (sid) SpreadsheetApp.openById(sid).getSheets()[0].appendRow(row);
}

function countValues_(state, v) {
  return Object.keys(state).filter(function (k) { return state[k] === v; }).length;
}

function countStage_(man, state, stage) {
  return man.entries.filter(function (x) { return x.stage === stage && state[x.outreach_id] === 'sent'; }).length;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    CFG: CFG, collapse_: collapse_, parseAddresses_: parseAddresses_, aliasInSignature_: aliasInSignature_, htmlToText_: htmlToText_,
    decodeManifest_: decodeManifest_, checkEntry_: checkEntry_, splitMime_: splitMime_, asciiBytes_: asciiBytes_,
    getHeader_: getHeader_, rawBytes_: rawBytes_, replaceFromHeader_: replaceFromHeader_, rewriteForTest_: rewriteForTest_, inWindow_: inWindow_,
    orderEntries_: orderEntries_, sharedCaps_: sharedCaps_, unionDnc_: unionDnc_, checkOnly_: checkOnly_
  };
}
