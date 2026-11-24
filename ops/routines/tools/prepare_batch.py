"""Stage the next send day's Jobsite batch for the Apps Script publisher (ops/sender/JsiPublisher.gs).

python -I prepare_batch.py --repo . --send-date YYYY-MM-DD --out ops/prepared/<date>.json [--evidence <recheck json glob> ...]

Runs the same checks as `ji_ops.py manifest` (ji_ops.build_manifest re-validates every drafted record planned for the
date and refuses the whole list on any error), then adds a hook per entry for the morning re-check:
  NOI   S1: the TCEQ authorization (TXR15....) and the record date its copy cites; checked_at = the latest saved
        hook_recheck.js run that found it (--evidence), else empty (the publisher re-checks live anyway)
  NONE  follow-ups (S2, S5)
Refuses a batch with no drafted rows, a business other than Jobsite Intelligence, a non JI- ID, or an S1 whose hook
cannot be read. --out is kept in the repo (ops/prepared/) so the close-out reconciles against it the next day; the
published manifest itself lives only in Gmail. Prints SUBJECT and BODY for one Gmail draft to operations@
("JSI-PREPARED v1 <date> <sha>").
"""
import argparse, base64, glob, gzip, hashlib, json, os, sys
from datetime import date, datetime, timezone
p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--send-date", required=True); p.add_argument("--out", required=True)
p.add_argument("--evidence", action="append", default=[])
a = p.parse_args()
TOOLS = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.abspath(a.out)
os.chdir(a.repo); sys.path.insert(0, "scripts"); sys.path.insert(0, TOOLS)
import ji_ops as ops
import jsi_common as jc
checked = jc.load_checked(a.evidence)

queues, recs = [], {}
for f in sorted(glob.glob("ops/queue/*.json")):
    with open(f, encoding="utf-8") as fh: q = json.load(fh)
    hit = [r for r in q["records"] if r.get("status") == "drafted" and r.get("planned_for") == a.send_date]
    if hit:
        # only this day's drafts: build_manifest also lists unplanned legacy drafts, which must not ride along
        queues.append((f, dict(q, records=hit)))
        for r in hit: recs[r["id"]] = (r, q.get("packet"))
if not queues:
    sys.exit(f"no drafted records planned for {a.send_date}")
rules = ops.load_rules(os.path.join("ops", "rules.json"))
if rules.get("business") != "Jobsite Intelligence":
    sys.exit(f"ops/rules.json business is {rules.get('business')!r}, not Jobsite Intelligence")
other = ops.resolve_other(rules, None, None)
try:
    man = ops.build_manifest(queues, rules, "data", a.send_date, other)
except ops.OpsError as ex:
    sys.exit(str(ex))
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
ref = date.fromisoformat(a.send_date)
for e in man["entries"]:
    if not e["outreach_id"].startswith("JI-"): sys.exit(f"{e['outreach_id']}: not a Jobsite ID")
    r, packet = recs[e["outreach_id"]]
    hook = {"kind": "NONE", "id": "", "cited": "", "checked_at": ""}
    if e["stage"] == "S1":
        try:
            hook = jc.hook_for(r["body"], jc.packet_row(packet, r["to"]), checked, ref)
        except ValueError as ex:
            sys.exit(f"{e['outreach_id']}: {ex}")
    e["hook"] = hook
prepared = dict(man, kind="prepared", prepared_at=now)
raw = json.dumps(prepared, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
sha = hashlib.sha256(raw).hexdigest()
body = base64.b64encode(gzip.compress(raw, mtime=0)).decode("ascii")
body = "\n".join(body[i:i + 76] for i in range(0, len(body), 76))
subject = f"JSI-PREPARED v1 {a.send_date} {sha}"
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"subject": subject, "prepared": prepared}, fh, indent=1, ensure_ascii=False); fh.write("\n")
kinds = {}
for e in prepared["entries"]: kinds[e["hook"]["kind"]] = kinds.get(e["hook"]["kind"], 0) + 1
stages = {}
for e in prepared["entries"]: stages[e["stage"]] = stages.get(e["stage"], 0) + 1
print(f"prepared {len(prepared['entries'])} entries for {a.send_date}: stages {stages}, hooks {kinds}")
print("SUBJECT: " + subject)
print("BODY:\n" + body)
