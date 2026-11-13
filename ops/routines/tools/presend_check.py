"""Pre-send decision for one business and one send date (read-only). Works for ASI and Jobsite: both
use the same manifest format and sender.

python -I presend_check.py --repo <checkout> --date YYYY-MM-DD --prefix <ASI-MANIFEST|...> \
       [--gmail-drafts <list_drafts json>] [--sender-log <csv>] [--id-prefix JI-] [--out decision.json]

Decision (printed as JSON, also written to --out):
  KEEP      today's manifest exists in the repo and in Gmail, hashes agree, it has entries and is fresh
  SENDING   the Sender Log already has rows for today's manifest: never rebuild or republish
  BUILD     no usable manifest, and drafted records planned for today exist: build and publish one
  NOTHING   no usable manifest and nothing drafted for today: record the reason, retry next business day
Every reason is listed. A KEEP or SENDING manifest is never replaced.
"""
import argparse, csv, glob, hashlib, json, os, re, sys
from datetime import datetime, timedelta, timezone

p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--date", required=True)
p.add_argument("--prefix", default="ASI-MANIFEST"); p.add_argument("--gmail-drafts")
p.add_argument("--sender-log"); p.add_argument("--id-prefix", default="")
p.add_argument("--out")
a = p.parse_args()
reasons, d = [], a.date
mf_path = os.path.join(a.repo, "ops", "manifests", f"{d}.json")
man = sub = None
if os.path.exists(mf_path):
    with open(mf_path, encoding="utf-8") as fh: raw = json.load(fh)
    man = raw.get("manifest", raw); sub = raw.get("subject")
    reasons.append(f"repo manifest {d}.json: {len(man.get('entries', []))} entries, created {man.get('created_at')}, dry_run_only={man.get('dry_run_only')}")
else:
    reasons.append(f"no repo manifest for {d}")

gmail = []
if a.gmail_drafts and os.path.exists(a.gmail_drafts):
    with open(a.gmail_drafts, encoding="utf-8") as fh: g = json.load(fh)
    for x in g.get("drafts", []):
        s = x.get("subject") or ""
        if s.startswith(f"{a.prefix} v1 {d} "): gmail.append(x)
    reasons.append(f"Gmail {a.prefix} drafts for {d}: {len(gmail)}")
else:
    reasons.append("Gmail drafts not supplied: cannot confirm the published manifest")

sending = 0
ids = {e["outreach_id"] for e in (man or {}).get("entries", [])}
if a.sender_log and os.path.exists(a.sender_log):
    with open(a.sender_log, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r.get("time (Central)", "").startswith(d) and r.get("mode") == "LIVE" and (
                    r.get("outreach_id") in ids or (a.id_prefix and r.get("outreach_id", "").startswith(a.id_prefix))):
                sending += 1
    reasons.append(f"Sender Log LIVE rows today for this business: {sending}")

drafted_today = []
for f in glob.glob(os.path.join(a.repo, "ops", "queue", "*.json")):
    with open(f, encoding="utf-8") as fh: q = json.load(fh)
    for r in q["records"]:
        if r.get("status") == "drafted" and r.get("planned_for") == d and r["stage"] in ("S1", "S2", "S3", "S4", "S5"):
            drafted_today.append((os.path.relpath(f, a.repo).replace("\\", "/"), r["id"]))
reasons.append(f"drafted records planned for {d}: {len(drafted_today)}")

def fresh(m):
    try:
        created = datetime.fromisoformat(m["created_at"])
        eight_am = datetime.fromisoformat(f"{d}T08:00:00-06:00")
        return timedelta(hours=-1) <= eight_am - created <= timedelta(hours=36)
    except Exception: return False

hash_ok = bool(man and sub and any(x.get("subject") == sub for x in gmail))
if sending:
    decision = "SENDING"
elif man and man.get("entries") and hash_ok and fresh(man) and man.get("dry_run_only") is False:
    decision = "KEEP"
else:
    if man and not man.get("entries"): reasons.append("repo manifest is EMPTY")
    if man and not fresh(man): reasons.append("repo manifest is outside the 36-hour window at 8 AM")
    if man and not hash_ok: reasons.append("published Gmail manifest missing or its subject differs from the repo manifest")
    if man and man.get("dry_run_only") is not False: reasons.append("repo manifest is a dry-run manifest")
    decision = "BUILD" if drafted_today else "NOTHING"
queues = sorted({q for q, _ in drafted_today})
out = {"date": d, "decision": decision, "reasons": reasons, "queues": queues, "drafted_ids": sorted(i for _, i in drafted_today),
       "existing_gmail_manifest_ids": [x.get("id") for x in gmail]}
if a.out:
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh: json.dump(out, fh, indent=1)
print(json.dumps(out, indent=1))
