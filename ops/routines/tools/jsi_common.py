"""Shared helpers for the Jobsite routine tools (business days, the TCEQ NOI hook, saved re-checks).

The hook of every Jobsite first touch is one TCEQ construction stormwater authorization (TXR15....) on the
Central Registry, cited in the S1's first paragraph as "authorization (TXR1594ZB) with a record date of November 5"
(older copy: "... (TXR1573ZR) dated October 8"). The rules for when a hook is fit to send live in one place,
ops/sender/JsiPublisher.gs `noiProblem_` (run from the PC through ops/sender/hook_facts.cjs); `noi_problem` below
mirrors it for read-only previews (daily_status, calendar) and is kept equal by tests.
"""
import glob, json, os, re
from datetime import date, datetime, timedelta, timezone

SITE_WINDOW_D = 45          # tracker, Nov 6: hook sites up to 45 days from their TCEQ record date
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}
AUTH_RE = re.compile(r"\bTXR15[0-9A-Z]{4}\b")
DATE_RE = re.compile(r"(?:record date of|dated) (" + "|".join(MONTHS) + r") (\d{1,2})(?:, (\d{4}))?")


def holidays(repo="."):
    out = set()
    p = os.path.join(repo, "ops", "routines", "holidays.txt")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if re.match(r"\d{4}-\d{2}-\d{2}$", line): out.add(date.fromisoformat(line))
    return out


def is_bd(d, hol): return d.weekday() < 5 and d not in hol


def next_bd(d, hol):
    d += timedelta(1)
    while not is_bd(d, hol): d += timedelta(1)
    return d


def bd_add(d, n, hol):
    while n:
        d += timedelta(1)
        if is_bd(d, hol): n -= 1
    return d


def bdays_from(d, n, hol):
    out = []
    while len(out) < n:
        if is_bd(d, hol): out.append(d)
        d += timedelta(1)
    return out


def first_para(body):
    parts = (body or "").split("\n\n")
    return parts[1] if len(parts) > 1 else (body or "")


def cited_date(text, ref):
    """The record date the copy cites, as a date. A date with no year is the latest one on or before ref + 7 days
    (record dates are in the past when the copy is written)."""
    m = DATE_RE.search(text or "")
    if not m: return None
    mo, dd = MONTHS[m.group(1)], int(m.group(2))
    if m.group(3): return date(int(m.group(3)), mo, dd)
    y = ref.year
    while date(y, mo, dd) > ref + timedelta(7): y -= 1
    return date(y, mo, dd)


def packet_row(packet, to):
    """The packet line (CSV or Markdown) that names this recipient, else ''."""
    try:
        with open(packet, encoding="utf-8") as fh:
            return next((line for line in fh if to.lower() in line.lower()), "")
    except (OSError, TypeError):
        return ""


def hook_for(body, packet_line="", checked=None, ref=None):
    """{kind: NOI, id: TXR15...., cited: YYYY-MM-DD, checked_at} for a first touch; raises ValueError when the
    authorization or its cited date is missing (the row cannot be re-checked, so it is held, never sent blind)."""
    ref = ref or date.today()
    first = first_para(body)
    ids = AUTH_RE.findall(first) or AUTH_RE.findall(packet_line or "")
    if not ids: raise ValueError("no TXR15 authorization in its first paragraph or packet line")
    c = cited_date(first, ref)
    if not c: raise ValueError(f"{ids[0]}: no cited record date ('record date of <Month> <day>') in its first paragraph")
    return {"kind": "NOI", "id": ids[0], "cited": c.isoformat(), "checked_at": (checked or {}).get(ids[0], "")[:10]}


def noi_problem(hook, fact, send_date):
    """Python mirror of JsiPublisher.gs noiProblem_ (tests keep the two equal). fact = hook_recheck.js record:
    {rows: [{status, date}], ...} or {unavailable: true}."""
    if not hook or hook.get("kind") == "NONE": return ""
    if hook.get("kind") != "NOI": return "unknown hook kind " + str(hook.get("kind"))
    if not fact or fact.get("unavailable"): return "TCEQ Central Registry unavailable"
    rows = fact.get("rows") or []
    if not rows: return "authorization " + hook["id"] + " not found on the Central Registry"
    active = [r for r in rows if str(r.get("status", "")).upper() == "ACTIVE"]
    if not active: return "authorization " + hook["id"] + " is " + (rows[0].get("status") or "not ACTIVE")
    dates = sorted({str(r.get("date", ""))[:10] for r in active})
    if hook.get("cited") and hook["cited"] not in dates:
        return "cited record date " + hook["cited"] + " is not on the live record (" + ", ".join(dates) + ")"
    age = (date.fromisoformat(send_date) - date.fromisoformat(hook["cited"])).days
    if age > SITE_WINDOW_D:
        return "record date " + hook["cited"] + " is " + str(age) + " days before " + send_date + " (over " + str(SITE_WINDOW_D) + ")"
    return ""


def window_problem(cited, send_date):
    """The part of the rule that needs no network: the 45-day site window."""
    if not cited: return ""
    age = (send_date - cited).days
    return f"record date {cited} is {age} days before {send_date} (over {SITE_WINDOW_D})" if age > SITE_WINDOW_D else ""


def load_checked(paths):
    """Latest successful re-check per authorization from hook_recheck.js output files (glob patterns)."""
    checked = {}
    for pat in paths:
        for g in glob.glob(pat):
            try:
                with open(g, encoding="utf-8") as fh: d = json.load(fh)
            except (OSError, ValueError): continue
            if not isinstance(d, dict) or not isinstance(d.get("records"), dict): continue
            when = d.get("checked_at") or datetime.fromtimestamp(os.path.getmtime(g), timezone.utc).isoformat()
            for k, v in d["records"].items():
                if k.startswith("TXR15") and isinstance(v, dict) and not v.get("unavailable") and v.get("rows"):
                    if when > checked.get(k, ""): checked[k] = when
    return checked


def sending_cities(rules):
    """Cities with a sender alias in rules.json (Houston only until dfwjobsite@ exists). Rows elsewhere wait."""
    return set(rules.get("senders", {}))
