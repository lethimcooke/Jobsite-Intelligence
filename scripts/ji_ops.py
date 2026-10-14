#!/usr/bin/env python3
"""Jobsite Intelligence outreach operations (copy of Austin-Signage scripts/asi_ops.py at 01d7453; the ASI repo owns the code, resync from there, change only via the user).

Outreach operations: approved copy -> validated draft queue -> Gmail drafts -> evidence-backed logging.

Adapted from the ASI operations starter kit (ops/starter-kit/, Node). Rules live in
ops/rules.json; the tracker wins over that file. This tool never sends mail and never calls
Gmail itself: the operator (Claude) makes the Gmail MCP calls and feeds the results back in.

Commands (run from the repo root):
  convert SOURCE.md --batch B --city C --stage S [--packet PACKET.md] --out ops/queue/B.json
        Copy an approved copy file into a queue, verbatim and in file order.
  validate QUEUE [--send-date YYYY-MM-DD]
  plan QUEUE... --send-date YYYY-MM-DD [--apply]   (first touches first, then oldest follow-ups, within caps)
        Rules, do-not-contact, list status, daily S1 cap, and scripts/check_duplicates.py on the packet.
  next QUEUE            Print create_draft payloads for records that have no draft yet.
  record-draft QUEUE ID --draft-id D --message-id M --thread-id T
        Persist a created draft. Refuses a second draft for the same record and payload.
  reconcile-drafts QUEUE DRAFTS.json
        Compare saved draft IDs with a list_drafts result; flag drafts that vanished (sent or deleted).
  evidence QUEUE THREADS.json --out EVIDENCE.json
        Build delivery evidence from a search_threads result (Sent messages only).
  log QUEUE EVIDENCE.json [--apply]
        Dry run by default. --apply backs up the CSVs, then writes the ledger, list status and results.
  status QUEUE          One line per record.
  manifest QUEUE... --send-date D --out ops/manifests/D.json
        List the day's drafted S1-S5 emails (re-validated) for the Gmail sender (ops/sender/);
        prints the subject and base64 body of the manifest draft to create in Gmail.
"""
import argparse
import base64
import csv
import datetime as dt
import glob
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGES = ("S1", "S2", "S3", "S4", "S5", "E1", "E2", "E3")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
FREE = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "live.com", "msn.com",
        "sbcglobal.net", "att.net", "comcast.net", "me.com", "ymail.com", "protonmail.com", "mail.com"}

LEDGER = "send_ledger.csv"
LEDGER_FIELDS = ["logged_at", "outreach_id", "batch", "stage", "city", "company", "kind", "evidence_id",
                 "sent_message_id", "thread_id", "sent_at", "from", "to", "form_url", "confirmation_ref", "note"]
RESULTS = "outreach_results.csv"
RESULTS_FIELDS = ["company", "batch", "s1_date", "hook", "hook_type", "company_type", "base", "outcome",
                  "outcome_date", "notes"]
LIST_FILES = ["master_prospect_list.csv", "adjacent_trades_list.csv"]
# Prospect-list layout. ASI's is the default; another business (Jobsite Intelligence) states its own
# in its rules.json under "lists", e.g. {"files": ["hauler_list_houston.csv"], "glob": "",
# "primary": "email", "alternates": ["site_emails"], "city": "metro"}.
DEFAULT_LISTS = {"files": LIST_FILES, "glob": "*_prospect_list.csv", "primary": "email_primary",
                 "alternates": ["email_alternates"], "city": "city"}
DNC_FIELDS = ["company", "email", "domain", "phone", "address", "reason", "date", "source"]


class OpsError(Exception):
    pass


# ---------- io ----------

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.loads(f.read().lstrip("﻿"))


def write_json_atomic(path, data):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def read_csv(path, required=None, exact=None):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fields = r.fieldnames or []
        rows = list(r)
    name = os.path.basename(path)
    if exact is not None and fields != exact:
        raise OpsError(f"schema drift in {name}: expected {exact}, found {fields}")
    if required and not required.issubset(fields):
        raise OpsError(f"schema drift in {name}: missing {sorted(required - set(fields))}")
    return fields, rows


def line_ending(path):
    """Keep each file's own line ending (the master list is CRLF, the results CSV is LF)."""
    if not os.path.exists(path):
        return "\n"
    with open(path, "rb") as f:
        first = f.readline()
    return "\r\n" if first.endswith(b"\r\n") else "\n"


def write_csv_tmp(path, fields, rows):
    d = os.path.dirname(os.path.abspath(path))
    term = line_ending(path)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator=term)
        w.writeheader()
        w.writerows(rows)
    return tmp


def now_iso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


# ---------- rules and lists ----------

def load_rules(path):
    rules = read_json(path)
    if rules.get("reviewed") is not True:
        raise OpsError(f"{path}: rules must be reviewed against the tracker and marked reviewed: true")
    # Attachments and other repo paths resolve against the repo that owns these rules.
    rules["_root"] = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    return rules


def list_config(rules=None):
    cfg = dict(DEFAULT_LISTS)
    cfg.update((rules or {}).get("lists") or {})
    return cfg


def list_required(cfg):
    return {"company", "outreach_status", cfg["primary"], *cfg["alternates"]} | ({cfg["city"]} if cfg.get("city") else set())


def row_emails(row, cfg):
    text = " ".join(row.get(k) or "" for k in [cfg["primary"], *cfg["alternates"]])
    return [e.lower() for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)]


def signature(rules, city):
    s = rules["senders"][city]
    return rules["signature_template"].format(display=s["display"], **{"from": s["from"]})


def norm_name(n):
    n = (n or "").lower().replace("&", " and ")
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    n = re.sub(r"\b(llc|inc|co|corp|company|ltd|the|and)\b", " ", n)
    return "".join(n.split())


def domain(email):
    return email.split("@", 1)[1].lower() if "@" in email else ""


def load_lists(data_dir, rules=None):
    """email (lower) -> (file, row) across every prospect list."""
    cfg = list_config(rules)
    index = {}
    files = [os.path.join(data_dir, f) for f in cfg["files"]]
    if cfg.get("glob"):
        files += sorted(glob.glob(os.path.join(data_dir, cfg["glob"])))
    seen = set()
    for path in files:
        if path in seen or not os.path.exists(path):
            continue
        seen.add(path)
        _, rows = read_csv(path, required=list_required(cfg))
        for row in rows:
            for e in row_emails(row, cfg):
                index.setdefault(e, (os.path.basename(path), row))
    if not index:
        raise OpsError(f"no prospect list found in {data_dir} (lists: {cfg['files']})")
    return index


def load_dnc(data_dir):
    _, rows = read_csv(os.path.join(data_dir, "do_not_contact.csv"), exact=DNC_FIELDS)
    emails = {r["email"].strip().lower() for r in rows if r["email"].strip()}
    domains = {r["domain"].strip().lower() for r in rows if r["domain"].strip()} - FREE
    names = {norm_name(r["company"].split("(")[0]) for r in rows if r["company"].strip()}
    return emails, domains, names - {""}


def load_other(rules_path, data_dir, fallback_lists=None):
    """The other business that shares this mailbox: its lists, do-not-contact and ledger.
    One company, one business: nobody on its lists or its do-not-contact may get our email."""
    rules = read_json(rules_path)          # only its list layout is used here, not its copy rules
    if not rules.get("lists") and fallback_lists:
        rules["lists"] = fallback_lists    # until its own rules.json states its layout
    lists = load_lists(data_dir, rules)
    names = {norm_name(row["company"]) for _, row in lists.values()} - {""}
    domains = {domain(e) for e in lists} - FREE
    ledger = ledger_rows(data_dir)
    dnc_path = os.path.join(data_dir, "do_not_contact.csv")
    if os.path.exists(dnc_path):
        dnc_rows = read_csv(dnc_path, exact=DNC_FIELDS)[1]
    elif ledger:
        raise OpsError(f"{dnc_path} is missing, but that business has sent email")
    else:
        dnc_rows = []                      # it has never sent, so nobody has opted out yet
    dnc = ({r["email"].strip().lower() for r in dnc_rows if r["email"].strip()},
           {r["domain"].strip().lower() for r in dnc_rows if r["domain"].strip()} - FREE,
           {norm_name(r["company"].split("(")[0]) for r in dnc_rows if r["company"].strip()} - {""})
    return {"business": rules.get("business", rules_path), "lists": lists, "names": names, "domains": domains,
            "dnc": dnc, "dnc_rows": dnc_rows, "ledger": ledger}


def resolve_other(rules, other_rules=None, other_data_dir=None):
    """Load the other business from CLI paths or the rules' cross_business defaults (paths relative to
    this repo's root). Required when the rules say so."""
    cb = rules.get("cross_business") or {}
    r = other_rules or (cb.get("rules") and os.path.join(ROOT, cb["rules"]))
    d = other_data_dir or (cb.get("data_dir") and os.path.join(ROOT, cb["data_dir"]))
    if not (r and d):
        if cb.get("required"):
            raise OpsError("cross-business check is required: pass --other-rules and --other-data-dir")
        return None
    if not (os.path.exists(r) and os.path.isdir(d)):
        raise OpsError(f"cross-business check: {r} or {d} not found ({cb.get('missing_hint', 'clone the other repo')})")
    return load_other(r, d, cb.get("lists_if_unstated"))


def cross_business_errors(rec, other):
    if not other:
        return []
    to, name = rec["to"].strip().lower(), norm_name(rec.get("company", ""))
    who, errs = other["business"], []
    hit = other["lists"].get(to)
    if hit:
        errs.append(f"recipient is on {who}'s list ({hit[0]}: {hit[1]['company']}); one company, one business")
    elif domain(to) not in FREE and domain(to) in other["domains"]:
        errs.append(f"recipient's domain {domain(to)} is on {who}'s list; one company, one business")
    if name and name in other["names"]:
        errs.append(f"company name matches one on {who}'s list; one company, one business")
    emails, domains, names = other["dnc"]
    if to in emails or (domain(to) not in FREE and domain(to) in domains) or (name and name in names):
        errs.append(f"on {who}'s do-not-contact list")
    return errs


def refund_allowed(rules, rec):
    ra = rules.get("refund_allowed", {})
    to = rec["to"].lower()
    if to in {e.lower() for e in ra.get("emails", [])} or domain(to) in {d.lower() for d in ra.get("domains", [])}:
        return True
    return any(norm_name(c) and norm_name(c) in norm_name(rec.get("company", "")) for c in ra.get("companies", []))


# ---------- validation ----------

def footer_text(rules, stage):
    f = rules.get("footer") or {}
    if stage not in f.get("stages", []):
        return ""
    return "\n".join(x for x in (f.get("text", ""), f.get("address", "")) if x)


def check_record(rec, rules, lists, dnc, s1_dates=None, other=None):
    errs = []
    for k in ("id", "batch", "company", "city", "stage", "from", "to", "subject", "body"):
        if not isinstance(rec.get(k), str) or not rec[k].strip():
            errs.append(f"missing {k}")
    if errs:
        return errs
    stage, city, to = rec["stage"], rec["city"], rec["to"].strip().lower()
    if stage not in STAGES:
        errs.append(f"invalid stage {stage}")
    if city not in rules["senders"]:
        errs.append(f"no configured sender for city {city}")
    elif rec["from"].lower() != rules["senders"][city]["from"]:
        errs.append(f"wrong sender for {city}: {rec['from']} (needs {rules['senders'][city]['from']})")
    if not EMAIL_RE.match(to):
        errs.append(f"invalid recipient {rec['to']}")
    if any(re.search(r"[\r\n]", rec[k]) for k in ("subject", "from", "to")):
        errs.append("header contains a newline")
    copy = rec["subject"] + "\n" + rec["body"]
    low = copy.lower()
    for a in rules.get("banned_addresses", []):
        if a.lower() in low or a.lower() == to:
            errs.append(f"banned address {a}")
    if "—" in copy:
        errs.append("em dash")
    for p in rules.get("banned_phrases", []):
        if p.lower() in low:
            errs.append(f"banned phrase: {p}")
    if rules.get("refund_word", "refund") in low and not refund_allowed(rules, rec):
        errs.append("refund wording (only the grandfathered five may see it)")
    if city in rules["senders"] and not rec["body"].rstrip().endswith(signature(rules, city)):
        errs.append("body does not end with the full three-line signature for " + city)
    pr = rules.get("price_rules", {}).get(stage)
    if pr:
        if "exact" in pr:
            line = rules[pr["exact"]]
            n = rec["body"].count(line)
            if n != 1:
                errs.append(f"standard price line must appear exactly once (found {n})")
        for p in pr.get("all_of", []):
            if p not in rec["body"]:
                errs.append(f"price wording missing: {p}")
    want = footer_text(rules, stage)
    if want and rec.get("footer") != want:
        errs.append("opt-out footer missing or out of date (re-convert the queue)")
    if "—" in (rec.get("footer") or ""):
        errs.append("em dash in footer")
    seq = rules.get("short_sequence") or {}
    s1 = (s1_dates or {}).get(to)
    if seq and s1 and s1 >= seq.get("from_s1_date", "9999") and stage.startswith("S") and stage not in seq.get("stages", []):
        errs.append(f"{stage} is dropped for batches first sent on/after {seq['from_s1_date']} (sequence is {', '.join(seq['stages'])})")
    if stage in rules.get("thread_required_stages", []) and not rec.get("reply_to_message_id"):
        errs.append("follow-up needs reply_to_message_id (latest message in the thread)")
    atts = rec.get("attachments") or []
    if not isinstance(atts, list) or any(not isinstance(a, str) for a in atts):
        errs.append("attachments must be a list of repo paths")
    else:
        if stage in rules.get("attachment_required_stages", []) and not atts:
            errs.append(f"{stage} needs the sample PDF attached")
        for a in atts:
            if not os.path.exists(os.path.join(rules.get("_root", ROOT), a)):
                errs.append(f"attachment not found: {a}")
    emails, domains, names = dnc
    if to in emails or (domain(to) not in FREE and domain(to) in domains) or norm_name(rec["company"]) in names:
        errs.append("do-not-contact match")
    hit = lists.get(to)
    if not hit:
        errs.append("recipient is not in any prospect list (add it there first)")
    else:
        status = hit[1]["outreach_status"].strip()
        allowed = rules.get("status_rules", {}).get(stage, [])
        if not any(status.startswith(a) for a in allowed):
            errs.append(f"list status '{status}' ({hit[0]}) does not allow {stage}")
    errs += cross_business_errors(rec, other)
    return errs


def s1_dates_from_ledger(data_dir):
    out = {}
    for r in ledger_rows(data_dir):
        if r["stage"] == "S1" and r["kind"] == "gmail_sent":
            to = r["to"].strip().lower()
            out[to] = min(out.get(to, r["sent_at"][:10]), r["sent_at"][:10])
    return out


def daily_share(rules):
    """This business's share of the shared mailbox's daily total (user, Oct 14: ASI 45, Jobsite 15)."""
    total = rules.get("max_total_per_day", 10**6)
    return min(rules.get("daily_share", total), total)


def sent_on(data_dir, send_date, other=None):
    """Emails sent from the shared mailbox on send_date, both businesses' ledgers."""
    rows = ledger_rows(data_dir) + ((other or {}).get("ledger") or [])
    return [r for r in rows if r["kind"] == "gmail_sent" and r["sent_at"][:10] == send_date]


def plan_day(queues, rules, data_dir, send_date, other=None):
    """Pick today's sends across queues: first touches first (up to max_s1_per_day), then
    follow-ups oldest S1 first, all within max_total_per_day. The rest become 'deferred'.
    The mailbox's daily total is shared with the other business, so its sends count too; pass its
    queues for the day too (planned jointly, same order: first touches of both businesses first)."""
    sent, mine = sent_on(data_dir, send_date, other), sent_on(data_dir, send_date)
    budget = min(rules.get("max_total_per_day", 10**6) - len(sent), daily_share(rules) - len(mine))
    s1_budget = min(rules["max_s1_per_day"], daily_share(rules)) - sum(1 for r in mine if r["stage"] == "S1")
    s1_dates = s1_dates_from_ledger(data_dir)
    for r in (other or {}).get("ledger") or []:
        if r["stage"] == "S1" and r["kind"] == "gmail_sent":
            to = r["to"].strip().lower()
            s1_dates[to] = min(s1_dates.get(to, r["sent_at"][:10]), r["sent_at"][:10])
    cands = []
    for qi, (path, q) in enumerate(queues):
        for r in q["records"]:
            if r.get("status") in ("queued", "deferred") and not r.get("draft"):
                first = r["stage"] == "S1"
                # No S1 in the ledger means the S1 predates the ledger (before Oct 7), so it is oldest.
                age = s1_dates.get(r["to"].lower(), "0000") if not first else ""
                # Engaged emails (E1-E3) always go first: the tracker puts replies ahead of everything.
                tier = -1 if r["stage"].startswith("E") else (0 if first else 1)
                cands.append(((tier, age, qi, r["seq"]), r))
    picked, deferred = [], []
    for _, r in sorted(cands, key=lambda x: x[0]):
        if r["stage"] == "S1":
            ok = s1_budget > 0 and budget > 0
            s1_budget -= ok
        else:
            ok = budget > 0
        budget -= ok
        r["status"] = "queued" if ok else "deferred"
        (picked if ok else deferred).append(r)
    return picked, deferred


def ledger_rows(data_dir):
    path = os.path.join(data_dir, LEDGER)
    if not os.path.exists(path):
        return []
    return read_csv(path, exact=LEDGER_FIELDS)[1]


def validate_queue(queue, rules, data_dir, send_date=None, run_dup_check=True, other=None):
    errs = []
    lists, dnc = load_lists(data_dir, rules), load_dnc(data_dir)
    s1_dates = s1_dates_from_ledger(data_dir)
    ids, tos = set(), set()
    for rec in queue["records"]:
        if rec.get("status") == "skipped":
            continue
        tag = rec.get("id", "?")
        if tag in ids:
            errs.append(f"{tag}: duplicate outreach id")
        ids.add(tag)
        if rec.get("to", "").lower() in tos:
            errs.append(f"{tag}: recipient appears twice in this queue")
        tos.add(rec.get("to", "").lower())
        if rec.get("status") in ("sent_confirmed",):
            continue
        errs += [f"{tag}: {e}" for e in check_record(rec, rules, lists, dnc, s1_dates, other)]
    if send_date:
        already = sum(1 for r in sent_on(data_dir, send_date) if r["stage"] == "S1")   # this business's share
        planned = sum(1 for r in queue["records"] if r.get("stage") == "S1" and r.get("status") not in ("skipped", "sent_confirmed"))
        s1_cap = min(rules["max_s1_per_day"], daily_share(rules))
        if already + planned > s1_cap:
            errs.append(f"S1 cap: {already} already logged on {send_date} + {planned} planned > {s1_cap}")
        cap = rules.get("max_total_per_day") and daily_share(rules)
        if cap:
            done = len(sent_on(data_dir, send_date))
            todo = sum(1 for r in queue["records"] if r.get("status") not in ("skipped", "sent_confirmed", "deferred"))
            if done + todo > cap:
                errs.append(f"daily cap: {done} already sent on {send_date} + {todo} planned > {cap} (run plan)")
    packet = queue.get("packet")
    if run_dup_check and packet:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "check_duplicates.py"), packet],
                           cwd=ROOT, capture_output=True, text=True)
        if p.returncode != 0:
            errs.append("check_duplicates.py flagged the packet:\n" + (p.stdout + p.stderr).strip())
    return errs


# ---------- convert ----------

SECTION_RE = re.compile(r"^### (\d+)\. (.+)$", re.M)
SECTION2_RE = re.compile(r"^## (\d+)\. (.+)$", re.M)   # Jobsite copy files number their '## ' headings
TO_RE = re.compile(r"(?:\*\*To:\*\*|^- To:)\s*([^\s(]+)", re.M)
SUBJECT_RE = re.compile(r"(?:\*\*Subject:\*\*|^- Subject:)\s*(.+?)\s*$", re.M)


def convert(source, batch, city, stage, rules, packet=None, section=None, title_prefix=None):
    with open(source, encoding="utf-8") as fh:
        text = fh.read()
    full = text
    if section:
        parts = re.split(r"(?m)^## ", text)
        hits = [p for p in parts if p.startswith(section)]
        if len(hits) != 1:
            raise OpsError(f"section '{section}' matched {len(hits)} '## ' headings; it must match exactly one")
        text = "## " + hits[0]
    heads = list(SECTION_RE.finditer(text)) or list(SECTION2_RE.finditer(text))
    if not heads:
        raise OpsError("no '### N. Company' (or '## N. Company') sections found")
    footer = footer_text(rules, stage)
    records = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        sec = text[h.start():end]
        num, title = int(h.group(1)), h.group(2).strip()
        if title_prefix:
            # One file, several batches ("## 3. H1: Buiza Waste"): keep this batch's sections only.
            if not title.startswith(title_prefix + ": "):
                continue
            title = title[len(title_prefix) + 2:].strip()
        rid = f"{batch}-{stage}-{num:02d}"
        if "SKIP" in title.upper():
            records.append({"id": rid, "seq": num, "batch": batch, "company": title, "status": "skipped",
                            "skip_reason": title})
            continue
        to, subj = TO_RE.search(sec), SUBJECT_RE.search(sec)
        body = re.search(r"```\n(.*?)\n```", sec, re.S)
        if not (to and subj and body):
            raise OpsError(f"section {num} ({title}) lacks To, Subject or a fenced body")
        if not EMAIL_RE.match(to.group(1)):
            raise OpsError(f"section {num}: recipient '{to.group(1)}' is not a full address; resolve it in the copy file")
        if body.group(1) not in full:
            raise OpsError("internal: body not verbatim")
        text_body = body.group(1)
        # A copy file that already ends the body with the opt-out line: keep it once, as the footer.
        if footer and text_body.rstrip().endswith("\n\n" + footer):
            text_body = text_body.rstrip()[:-len(footer)].rstrip()
        records.append({
            "id": rid, "seq": num, "batch": batch, "company": title, "city": city, "stage": stage,
            "from": rules["senders"][city]["from"], "to": to.group(1), "subject": subj.group(1),
            "body": text_body, "reply_to_message_id": None, "attachments": [],
            "hook_type": "", "status": "queued", "draft": None, "footer": footer,
        })
    if not records:
        raise OpsError(f"no sections for '{title_prefix}' found")
    return {
        "batch": batch, "city": city, "stage": stage, "source": os.path.relpath(source, ROOT),
        "section": section, "title_prefix": title_prefix, "source_sha256": hashlib.sha256(full.encode()).hexdigest(), "packet": packet,
        "created_at": now_iso(), "records": records,
    }


# ---------- drafts ----------

def payload(rec):
    body = rec["body"] + ("\n\n" + rec["footer"] if rec.get("footer") else "")
    return {"to": [rec["to"]], "subject": rec["subject"], "body": body,
            "replyToMessageId": rec.get("reply_to_message_id") or None, "attachments": rec.get("attachments") or []}


def payload_hash(rec):
    return hashlib.sha256(json.dumps(payload(rec), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def find(queue, rid):
    for r in queue["records"]:
        if r["id"] == rid:
            return r
    raise OpsError(f"unknown outreach id {rid}")


def next_drafts(queue):
    out = []
    for r in sorted(queue["records"], key=lambda r: r["seq"]):
        if r.get("status") != "queued" or r.get("draft"):
            continue
        p = payload(r)
        p.update({"outreach_id": r["id"], "set_from_alias_by_hand": r["from"], "payload_sha256": payload_hash(r)})
        out.append(p)
    return out


def record_draft(queue, rid, draft_id, message_id, thread_id, replace=False):
    r = find(queue, rid)
    h = payload_hash(r)
    if r.get("draft") and not replace:
        same = r["draft"]["payload_sha256"] == h
        raise OpsError(f"{rid} already has draft {r['draft']['draft_id']}"
                       + (" for this exact copy; not creating a duplicate" if same else
                          " for OLDER copy; delete it in Gmail, then rerun with --replace"))
    if r.get("status") == "sent_confirmed":
        raise OpsError(f"{rid} is already confirmed sent")
    r["draft"] = {"draft_id": draft_id, "message_id": message_id, "thread_id": thread_id,
                  "payload_sha256": h, "created_at": now_iso()}
    r["status"] = "drafted"
    return r


def reconcile_drafts(queue, drafts_result):
    remote = {d["id"] for d in (drafts_result.get("drafts") or [])}
    report = []
    for r in sorted(queue["records"], key=lambda r: r["seq"]):
        d = r.get("draft")
        if r.get("status") == "drafted" and d:
            if d["draft_id"] not in remote:
                r["status"] = "draft_missing"
                report.append(f"{r['id']}: draft {d['draft_id']} is gone (sent or deleted); check Sent before recreating")
            elif d["payload_sha256"] != payload_hash(r):
                report.append(f"{r['id']}: copy changed since the draft was made; delete draft {d['draft_id']} and redo")
            else:
                report.append(f"{r['id']}: draft present, copy unchanged")
        elif r.get("status") == "queued":
            report.append(f"{r['id']}: no draft yet")
    return report


# ---------- evidence ----------

def evidence_from_threads(queue, threads_result):
    ev = []
    msgs = [m for t in (threads_result.get("threads") or []) for m in t.get("messages", [])]
    for r in sorted(queue["records"], key=lambda r: r["seq"]):
        if r.get("status") not in ("drafted", "draft_missing") or not r.get("draft"):
            continue
        since = r["draft"]["created_at"]
        hits = [m for m in msgs if "SENT" in (m.get("labelIds") or [])
                and r["to"].lower() in [x.lower() for x in m.get("toRecipients") or []]
                and m.get("date", "") >= since[:19]
                and (r["stage"] == "S1" or m.get("threadId") == r["draft"]["thread_id"])]
        if len(hits) == 1:
            m = hits[0]
            ev.append({"outreach_id": r["id"], "kind": "gmail_sent", "evidence_id": m["id"],
                       "thread_id": m.get("threadId"), "sent_at": m["date"].replace("Z", "+00:00"),
                       "from": m.get("sender", ""), "to": r["to"]})
        elif len(hits) > 1:
            raise OpsError(f"{r['id']}: {len(hits)} sent messages match; resolve by hand")
    return ev


# ---------- send manifest (read by ops/sender/Code.gs) ----------

MANIFEST_PREFIX = "ASI-MANIFEST v1"
SEND_STAGES = ("S1", "S2", "S3", "S4", "S5")


def collapse(text):
    """Whitespace-insensitive form the sender uses to compare a draft with its approved text."""
    return re.sub(r"\s+", " ", text or "").strip()


def build_manifest(queues, rules, data_dir, send_date, other=None, dry_run_only=False):
    """List every drafted cold email (S1-S5) the sender may send on send_date. Each record is
    re-validated; any error refuses the whole manifest. Engaged emails (E1-E3) are never listed."""
    lists, dnc = load_lists(data_dir, rules), load_dnc(data_dir)
    s1_dates = s1_dates_from_ledger(data_dir)
    entries, errs, seen = [], [], set()
    for _, q in queues:
        for r in q["records"]:
            if r.get("status") != "drafted" or r["stage"] not in SEND_STAGES:
                continue
            tag = r["id"]
            errs += [f"{tag}: {e}" for e in check_record(r, rules, lists, dnc, s1_dates, other)]
            d = r.get("draft") or {}
            if not d.get("draft_id") or not d.get("thread_id"):
                errs.append(f"{tag}: no recorded draft")
                continue
            if d.get("payload_sha256") != payload_hash(r):
                errs.append(f"{tag}: queue text changed after the draft was made; re-draft it")
            to = r["to"].strip().lower()
            if to in seen:
                errs.append(f"{tag}: recipient appears twice in this manifest")
            seen.add(to)
            sender = rules["senders"][r["city"]]
            text = collapse(payload(r)["body"])
            entries.append({
                "outreach_id": tag, "stage": r["stage"], "company": r["company"],
                "to": to, "from_alias": sender["from"], "display_name": sender["display"],
                "subject": r["subject"],
                # The sender hashes this many leading characters (UTF-16 units, as JavaScript counts)
                # of the draft's collapsed text and must get exactly this SHA-256.
                "body_len": len(text.encode("utf-16-le")) // 2,
                "body_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "is_reply": bool(r.get("reply_to_message_id")),
                "reply_to_message_id": r.get("reply_to_message_id") or "",
                "draft_id": d["draft_id"], "thread_id": d["thread_id"],
            })
    if errs:
        raise OpsError("manifest refused:\n" + "\n".join(errs))
    # Interleave aliases so no address sends a long run in a row.
    by_alias = {}
    for e in entries:
        by_alias.setdefault(e["from_alias"], []).append(e)
    ordered = []
    while any(by_alias.values()):
        for k in sorted(by_alias):
            if by_alias[k]:
                ordered.append(by_alias[k].pop(0))
    _, rows = read_csv(os.path.join(data_dir, "do_not_contact.csv"), exact=DNC_FIELDS)
    rows += (other or {}).get("dnc_rows") or []          # the sender also refuses the other business's opt-outs
    return {
        "version": 1, "send_date": send_date, "created_at": now_iso(),
        "business": rules.get("business", ""),
        # A test manifest: the sender checks and logs it but never sends from it, in any mode.
        "dry_run_only": bool(dry_run_only),
        # max_total is the mailbox's total across both businesses; share is this business's part of it.
        "max_total": rules.get("max_total_per_day", 60), "max_s1": rules["max_s1_per_day"],
        "share": daily_share(rules),
        "aliases": {v["from"]: v["display"] for v in rules["senders"].values()},
        "dnc_emails": sorted({x["email"].strip().lower() for x in rows if x["email"].strip()}),
        "dnc_domains": sorted({x["domain"].strip().lower() for x in rows if x["domain"].strip()} - FREE),
        "entries": ordered,
    }


def manifest_draft(manifest):
    """Subject and body of the manifest draft: gzip + base64 so Gmail cannot rewrap the JSON; the
    subject carries the JSON's SHA-256 so the sender rejects a damaged or edited manifest."""
    raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True).encode("utf-8")
    b64 = base64.b64encode(gzip.compress(raw, mtime=0)).decode("ascii")
    body = "\n".join(b64[i:i + 76] for i in range(0, len(b64), 76))
    return f"{MANIFEST_PREFIX} {manifest['send_date']} {hashlib.sha256(raw).hexdigest()}", body


# ---------- log ----------

TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?.*(Z|[+-]\d{2}:\d{2})$")


def plan_log(queue, evidence, data_dir, accept_alias=(), rules=None):
    """Validate everything and return the planned writes. Writes nothing."""
    if not isinstance(evidence, list):
        raise OpsError("evidence must be a JSON array")
    cfg = list_config(rules)
    ledger = ledger_rows(data_dir)
    lists = {}
    for f in cfg["files"]:
        p = os.path.join(data_dir, f)
        if os.path.exists(p):
            lists[f] = read_csv(p, required=list_required(cfg))
    res_fields, results = read_csv(os.path.join(data_dir, RESULTS), exact=RESULTS_FIELDS)
    by_key = {(r["kind"], r["evidence_id"]): r for r in ledger}
    logged_sent = {r["outreach_id"]: r for r in ledger if r["kind"] in ("gmail_sent", "form_confirmation")}
    new_ledger, status_changes, result_appends, result_updates, skipped = [], [], [], [], []
    for e in evidence:
        rid = e.get("outreach_id")
        r = find(queue, rid)
        kind = e.get("kind")
        if kind not in ("gmail_sent", "form_confirmation", "gmail_bounce"):
            raise OpsError(f"{rid}: unknown evidence kind {kind}")
        if not e.get("evidence_id"):
            raise OpsError(f"{rid}: evidence_id required (Sent message id, bounce message id or form confirmation id)")
        if not TS_RE.match(e.get("sent_at", "")):
            raise OpsError(f"{rid}: sent_at needs an ISO timestamp with timezone")
        if kind == "gmail_sent":
            if r.get("draft") and e["evidence_id"] == r["draft"].get("message_id"):
                raise OpsError(f"{rid}: evidence is the draft's message id, not a Sent message")
            if e.get("to", "").lower() != r["to"].lower():
                raise OpsError(f"{rid}: recipient mismatch ({e.get('to')} vs {r['to']})")
            if e.get("from", "").lower() != r["from"].lower() and rid not in accept_alias:
                raise OpsError(f"{rid}: sent from {e.get('from')} but must be {r['from']}; "
                               "log only with --accept-alias-mismatch after the user decides")
        if kind == "form_confirmation" and not (e.get("form_url") and e.get("confirmation_ref")):
            raise OpsError(f"{rid}: form needs form_url and confirmation_ref (screenshot or confirmation text)")
        if kind == "gmail_bounce" and rid not in logged_sent and not any(
                x["outreach_id"] == rid and x["kind"] != "gmail_bounce" for x in new_ledger):
            raise OpsError(f"{rid}: bounce recorded before any confirmed send")
        prior = by_key.get((kind, e["evidence_id"]))
        if prior:
            if prior["outreach_id"] != rid:
                raise OpsError(f"{rid}: evidence {e['evidence_id']} already logged for {prior['outreach_id']}")
            skipped.append(f"{rid}: already logged ({kind} {e['evidence_id']})")
            continue
        if kind != "gmail_bounce" and rid in logged_sent:
            raise OpsError(f"{rid}: already logged as sent with different evidence {logged_sent[rid]['evidence_id']}")
        row = {k: "" for k in LEDGER_FIELDS}
        row.update({"logged_at": now_iso(), "outreach_id": rid, "batch": r["batch"], "stage": r["stage"],
                    "city": r["city"], "company": r["company"], "kind": kind, "evidence_id": e["evidence_id"],
                    "sent_message_id": e.get("sent_message_id", ""), "thread_id": e.get("thread_id", "") or "",
                    "sent_at": e["sent_at"], "from": e.get("from", ""), "to": r["to"],
                    "form_url": e.get("form_url", ""), "confirmation_ref": e.get("confirmation_ref", ""),
                    "note": "alias mismatch accepted by user" if rid in accept_alias else ""})
        new_ledger.append(row)
        by_key[(kind, e["evidence_id"])] = row
        if r["stage"] != "S1":
            continue
        day = e["sent_at"][:10]
        alias = r["from"].split("@")[0] + "@"
        target = None
        for f, (_, rows) in lists.items():
            for lr in rows:
                if r["to"].lower() in row_emails(lr, cfg):
                    target = (f, lr)
                    break
            if target:
                break
        if not target:
            raise OpsError(f"{rid}: recipient not found in prospect lists")
        f, lr = target
        old = lr["outreach_status"]
        if kind == "gmail_bounce":
            new = old if old.startswith(f"S1 bounced {day}") else f"S1 bounced {day} ({e.get('reason', 'delivery failure')})"
        else:
            new = f"S1 sent {day} ({alias})"
            if old.startswith(f"S1 bounced {day}"):
                new = old  # already logged by hand, and the outcome since then is newer: leave it
            elif not old.startswith("Not contacted") and old != new:
                raise OpsError(f"{rid}: list status is '{old}', expected Not contacted")
        if old != new:
            status_changes.append((f, lr[cfg["primary"]], old, new))
        existing = [x for x in results if x["company"] == r["company"] and x["batch"] == r["batch"]]
        pending = [x for x in result_appends if x["company"] == r["company"] and x["batch"] == r["batch"]]
        if kind == "gmail_bounce":
            if pending:
                pending[0].update({"outcome": "bounced", "outcome_date": day, "notes": e.get("reason", "")})
            elif existing and existing[0]["outcome"] != "bounced":
                result_updates.append((r["company"], r["batch"], "bounced", day, e.get("reason", "")))
        elif not existing:
            result_appends.append({"company": r["company"], "batch": r["batch"], "s1_date": day,
                                   "hook": r["subject"], "hook_type": r.get("hook_type", ""),
                                   "company_type": r.get("company_type", ""),
                                   "base": lr.get(cfg.get("city") or "city", "").replace(", TX", ""), "outcome": "no reply",
                                   "outcome_date": "", "notes": ""})
    return {"primary": cfg["primary"], "ledger": new_ledger, "status": status_changes, "results_add": result_appends,
            "results_update": result_updates, "skipped": skipped, "lists": lists,
            "results": (res_fields, results), "ledger_existing": ledger}


def describe(plan):
    lines = [f"ledger +{len(plan['ledger'])}"]
    lines += [f"  + {r['outreach_id']} {r['kind']} {r['evidence_id']} {r['sent_at']}" for r in plan["ledger"]]
    lines += [f"status {f}: {e}: '{o}' -> '{n}'" for f, e, o, n in plan["status"]]
    lines += [f"results +{a['company']} ({a['batch']}, {a['s1_date']})" for a in plan["results_add"]]
    lines += [f"results ~{c} ({b}) -> {o} {d}" for c, b, o, d, _ in plan["results_update"]]
    lines += ["skip " + s for s in plan["skipped"]]
    return "\n".join(lines)


def apply_log(queue, plan, data_dir, queue_path):
    if not (plan["ledger"] or plan["status"] or plan["results_add"] or plan["results_update"]):
        return None
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    bdir = os.path.join(data_dir, "backups", stamp)
    os.makedirs(bdir, exist_ok=True)
    targets = [LEDGER, RESULTS] + list(plan["lists"])
    for t in targets:
        p = os.path.join(data_dir, t)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(bdir, t))
    if queue_path:
        shutil.copy2(queue_path, os.path.join(bdir, os.path.basename(queue_path)))
    tmps = []
    try:
        if plan["ledger"]:
            tmps.append((write_csv_tmp(os.path.join(data_dir, LEDGER), LEDGER_FIELDS,
                                       plan["ledger_existing"] + plan["ledger"]), os.path.join(data_dir, LEDGER)))
        rf, rows = plan["results"]
        for c, b, o, d, note in plan["results_update"]:
            for x in rows:
                if x["company"] == c and x["batch"] == b:
                    x.update({"outcome": o, "outcome_date": d, "notes": note or x["notes"]})
        if plan["results_add"] or plan["results_update"]:
            tmps.append((write_csv_tmp(os.path.join(data_dir, RESULTS), rf, rows + plan["results_add"]),
                         os.path.join(data_dir, RESULTS)))
        for f, (fields, lrows) in plan["lists"].items():
            changes = {e: n for ff, e, o, n in plan["status"] if ff == f}
            if not changes:
                continue
            for lr in lrows:
                if lr[plan.get("primary", "email_primary")] in changes:
                    lr["outreach_status"] = changes[lr[plan.get("primary", "email_primary")]]
            tmps.append((write_csv_tmp(os.path.join(data_dir, f), fields, lrows), os.path.join(data_dir, f)))
    except Exception:
        for t, _ in tmps:
            os.unlink(t)
        raise
    for t, final in tmps:
        os.replace(t, final)
    sent = {r["outreach_id"] for r in plan["ledger"] if r["kind"] != "gmail_bounce"}
    for r in queue["records"]:
        if r["id"] in sent:
            r["status"] = "sent_confirmed"
    return bdir


# ---------- cli ----------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rules", default=os.path.join(ROOT, "ops", "rules.json"))
    ap.add_argument("--data-dir", default=os.path.join(ROOT, "data"))
    ap.add_argument("--other-rules", help="the other business's rules.json (cross-business check; default from rules)")
    ap.add_argument("--other-data-dir", help="the other business's data dir (lists, do-not-contact, ledger)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("convert"); c.add_argument("source"); c.add_argument("--batch", required=True)
    c.add_argument("--city", required=True); c.add_argument("--stage", required=True)
    c.add_argument("--packet"); c.add_argument("--out", required=True)
    c.add_argument("--section", help="only the '## <section>' block of a file that holds several batches")
    c.add_argument("--title-prefix", help="only sections titled '<prefix>: Company' (e.g. H1), prefix dropped")
    v = sp.add_parser("validate"); v.add_argument("queue"); v.add_argument("--send-date")
    v.add_argument("--no-dup-check", action="store_true")
    n = sp.add_parser("next"); n.add_argument("queue")
    rd = sp.add_parser("record-draft"); rd.add_argument("queue"); rd.add_argument("id")
    rd.add_argument("--draft-id", required=True); rd.add_argument("--message-id", required=True)
    rd.add_argument("--thread-id", required=True); rd.add_argument("--replace", action="store_true")
    rc = sp.add_parser("reconcile-drafts"); rc.add_argument("queue"); rc.add_argument("drafts")
    ev = sp.add_parser("evidence"); ev.add_argument("queue"); ev.add_argument("threads"); ev.add_argument("--out", required=True)
    lg = sp.add_parser("log"); lg.add_argument("queue"); lg.add_argument("evidence")
    lg.add_argument("--apply", action="store_true"); lg.add_argument("--accept-alias-mismatch", nargs="*", default=[])
    st = sp.add_parser("status"); st.add_argument("queue")
    pl = sp.add_parser("plan", help="pick today's sends across queues (first touches first, then oldest follow-ups) within the daily caps")
    pl.add_argument("queues", nargs="+"); pl.add_argument("--send-date", required=True)
    pl.add_argument("--apply", action="store_true", help="write queued/deferred status back to the queue files")
    pl.add_argument("--other-queues", nargs="*", default=[],
                    help="the other business's queues for the same day, planned jointly against the shared caps")
    mf = sp.add_parser("manifest", help="list the day's drafted S1-S5 emails for the Gmail sender")
    mf.add_argument("queues", nargs="+"); mf.add_argument("--send-date", required=True)
    mf.add_argument("--out", required=True)
    mf.add_argument("--dry-run-only", action="store_true",
                    help="test manifest: the sender only checks and logs it, even when MODE is LIVE")
    a = ap.parse_args(argv)
    rules = load_rules(a.rules)
    other = None
    if a.cmd in ("validate", "next", "plan", "manifest"):
        other = resolve_other(rules, a.other_rules, a.other_data_dir)

    if a.cmd == "manifest":
        if os.path.exists(a.out):
            raise OpsError(f"{a.out} exists")
        m = build_manifest([(p, read_json(p)) for p in a.queues], rules, a.data_dir, a.send_date, other,
                           a.dry_run_only)
        subject, body = manifest_draft(m)
        write_json_atomic(a.out, {"subject": subject, "manifest": m})
        counts = {}
        for e in m["entries"]:
            counts[e["from_alias"]] = counts.get(e["from_alias"], 0) + 1
        print(f"wrote {a.out}: {len(m['entries'])} emails; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
        print("SUBJECT: " + subject)
        print("BODY:\n" + body)
        return 0

    if a.cmd == "convert":
        if os.path.exists(a.out):
            raise OpsError(f"{a.out} exists; queues are never overwritten")
        q = convert(a.source, a.batch, a.city, a.stage, rules, a.packet, a.section, a.title_prefix)
        write_json_atomic(a.out, q)
        live = [r for r in q["records"] if r["status"] != "skipped"]
        print(f"wrote {a.out}: {len(live)} records in file order, {len(q['records']) - len(live)} skipped")
        return 0
    if a.cmd == "plan":
        qs = [(path, read_json(path)) for path in a.queues + a.other_queues]
        if a.other_queues and not other:
            raise OpsError("--other-queues needs the cross-business data (--other-rules/--other-data-dir)")
        picked, deferred = plan_day(qs, rules, a.data_dir, a.send_date, other)
        for r in picked:
            print(f"SEND   {r['id']:<26} {r['stage']:<3} {r['from']:<34} {r['to']}")
        for r in deferred:
            print(f"DEFER  {r['id']:<26} {r['stage']:<3} {r['from']:<34} {r['to']}")
        s1 = sum(1 for r in picked if r["stage"] == "S1")
        print(f"{len(picked)} to send ({s1} first touches, {len(picked) - s1} follow-ups), {len(deferred)} deferred"
              + ("" if a.apply else " (dry run; --apply to save)"))
        if a.apply:
            for path, q in qs:
                write_json_atomic(path, q)
        return 0
    q = read_json(a.queue)
    if a.cmd == "validate":
        errs = validate_queue(q, rules, a.data_dir, a.send_date, not a.no_dup_check, other)
        if errs:
            print("FAIL\n" + "\n".join(errs))
            return 1
        print(f"PASS: {sum(1 for r in q['records'] if r.get('status') != 'skipped')} records")
        return 0
    if a.cmd == "next":
        errs = validate_queue(q, rules, a.data_dir, other=other)
        if errs:
            print("FAIL (fix before drafting)\n" + "\n".join(errs))
            return 1
        print(json.dumps(next_drafts(q), indent=2, ensure_ascii=False))
        return 0
    if a.cmd == "record-draft":
        r = record_draft(q, a.id, a.draft_id, a.message_id, a.thread_id, a.replace)
        write_json_atomic(a.queue, q)
        print(f"{r['id']}: saved draft {a.draft_id}")
        return 0
    if a.cmd == "reconcile-drafts":
        print("\n".join(reconcile_drafts(q, read_json(a.drafts))))
        write_json_atomic(a.queue, q)
        return 0
    if a.cmd == "evidence":
        if os.path.exists(a.out):
            raise OpsError(f"{a.out} exists")
        ev = evidence_from_threads(q, read_json(a.threads))
        write_json_atomic(a.out, ev)
        print(f"wrote {len(ev)} evidence entries to {a.out}; review them, then run log (dry run)")
        return 0
    if a.cmd == "log":
        plan = plan_log(q, read_json(a.evidence), a.data_dir, set(a.accept_alias_mismatch), rules)
        print(("APPLY" if a.apply else "DRY RUN") + "\n" + describe(plan))
        if a.apply:
            b = apply_log(q, plan, a.data_dir, a.queue)
            write_json_atomic(a.queue, q)
            print(f"backups: {os.path.relpath(b, ROOT)}" if b else "nothing to write")
        return 0
    if a.cmd == "status":
        for r in sorted(q["records"], key=lambda r: r["seq"]):
            d = (r.get("draft") or {}).get("draft_id", "")
            print(f"{r['seq']:>2} {r['id']:<14} {r.get('status', ''):<15} {r.get('to', ''):<36} {d}")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OpsError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(2)
