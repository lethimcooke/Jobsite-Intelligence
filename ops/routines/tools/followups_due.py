"""List Jobsite follow-ups due on or before a send date (read-only).

python -I followups_due.py --repo . --date YYYY-MM-DD [--out due.json]

Rules (tracker cadence + ops/rules.json short_sequence): every Jobsite batch runs S1, S2, S5. S2 = S1 + 2 business days,
S5 = S1 + 13, never sooner than the minimum gap after the latest actual send (S2 2, S5 4). Business days skip weekends
and ops/routines/holidays.txt. Excluded: bounced, any E-stage (engaged), do-not-contact (address or company domain),
list status replied/declined/closed/bounced/opt-out/hold, and recipients whose next stage already has a sent or skipped
record. Output: one record per recipient with next stage, due date, S1 date, batch, city, company, the S1 actually sent's
subject, the latest sent message id (reply_to) and thread id, copy_ready_id (a validated S2/S5 record not yet sent) and
planned_for (the day that copy is planned or drafted for, else ""). Oldest S1 first.
"""
import argparse, collections, csv, glob, json, os, sys
from datetime import date
p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--date", required=True); p.add_argument("--out")
a = p.parse_args()
TOOLS = os.path.dirname(os.path.abspath(__file__))
os.chdir(a.repo); sys.path.insert(0, "scripts"); sys.path.insert(0, TOOLS)
import ji_ops as ops
import jsi_common as jc
HOL = jc.holidays(".")
D = date.fromisoformat(a.date)
rules = ops.load_rules("ops/rules.json"); lists = ops.load_lists("data", rules); dnc = ops.load_dnc("data")
short_from = rules.get("short_sequence", {}).get("from_s1_date", "2026-10-14")
OFF = {"S2": 2, "S3": 5, "S4": 9, "S5": 13}; GAP = {"S2": 2, "S3": 3, "S4": 4, "S5": 4}
with open("data/send_ledger.csv", encoding="utf-8") as fh: led = list(csv.DictReader(fh))
by = collections.defaultdict(list)
for r in led: by[r["to"].strip().lower()].append(r)
existing = collections.defaultdict(set)
ready_copy = collections.defaultdict(dict)
planned = collections.defaultdict(dict)
subj = {}
for f in glob.glob("ops/queue/*.json"):
    with open(f, encoding="utf-8") as fh: q = json.load(fh)
    for r in q["records"]:
        if "stage" not in r or "to" not in r: continue
        to = r["to"].strip().lower()
        if r.get("status") in ("sent_confirmed", "skipped"): existing[to].add(r["stage"])
        elif r.get("status") in ("queued", "drafted", "deferred") and r["stage"] != "S1":
            ready_copy[to][r["stage"]] = r["id"]
            if r.get("status") in ("queued", "drafted") and r.get("planned_for"): planned[to][r["stage"]] = r["planned_for"]
        # The S1 actually sent wins over a skipped or unsent S1 to the same address (ASI fix, Nov 23).
        if r["stage"] == "S1" and (to not in subj or r.get("status") == "sent_confirmed" and not subj[to][1]):
            subj[to] = (r.get("subject", ""), r.get("status") == "sent_confirmed")
out, excl = [], collections.Counter()
for to, rows in by.items():
    sent = [r for r in rows if r["kind"] == "gmail_sent"]
    if any(r["kind"] == "gmail_bounce" for r in rows): excl["bounced"] += 1; continue
    if any(r["stage"].startswith("E") for r in rows): excl["engaged"] += 1; continue
    dom = to.split("@")[-1]
    if to in dnc[0] or (dom not in ops.FREE and dom in dnc[1]): excl["do-not-contact"] += 1; continue
    st = (lists.get(to) or (None, {"outreach_status": ""}))[1].get("outreach_status", "").lower()
    if any(s in st for s in ("replied", "declined", "closed", "bounced", "opt", "do not", "hold")): excl["list status"] += 1; continue
    s1 = [r for r in sent if r["stage"] == "S1"]
    if not s1: continue
    s1d = min(date.fromisoformat(r["sent_at"][:10]) for r in s1)
    seq = ["S1", "S2", "S5"] if s1d.isoformat() >= short_from else ["S1", "S2", "S3", "S4", "S5"]
    done = [s for s in seq if s in {r["stage"] for r in sent}]
    if done[-1] == "S5": continue
    nxt = seq[seq.index(done[-1]) + 1]
    if nxt in existing[to]: excl[f"{nxt} already sent or skipped"] += 1; continue
    last = max(sent, key=lambda r: r["sent_at"])
    due = max(jc.bd_add(s1d, OFF[nxt], HOL), jc.bd_add(date.fromisoformat(last["sent_at"][:10]), GAP[nxt], HOL))
    if due > D: continue
    out.append({"to": to, "next": nxt, "due": due.isoformat(), "s1_date": s1d.isoformat(), "batch": s1[0]["batch"],
                "city": s1[0]["city"], "company": s1[0]["company"], "s1_subject": subj.get(to, ("",))[0],
                "reply_to_message_id": last.get("evidence_id") or last.get("sent_message_id"), "thread_id": last.get("thread_id"),
                "last_stage": last["stage"], "last_sent": last["sent_at"][:10],
                "copy_ready_id": ready_copy[to].get(nxt), "planned_for": planned[to].get(nxt, "")})
out.sort(key=lambda x: (x["s1_date"], x["batch"], x["to"]))
summary = {"date": a.date, "due": len(out), "copy_ready": sum(1 for x in out if x["copy_ready_id"]),
           "already_planned": sum(1 for x in out if x["planned_for"]),
           "by_stage": dict(collections.Counter(x["next"] for x in out)),
           "by_batch": dict(collections.Counter(x["batch"] for x in out)), "excluded": dict(excl)}
if a.out:
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh: json.dump({"summary": summary, "due": out}, fh, indent=1)
print(json.dumps(summary, indent=1))
