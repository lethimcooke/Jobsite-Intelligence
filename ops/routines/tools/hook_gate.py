"""Gate Jobsite first touches on a fresh TCEQ hook check before `plan` picks them (close-out, before plan).

python -I hook_gate.py --repo . --send-date YYYY-MM-DD --out <gate.json> [--evidence <glob> ...] [--facts <recheck.json>]

Checks every ready S1 (status queued/deferred, no planned_for) and every row held for a Central Registry outage with
the JSI publisher's own rule (JsiPublisher.gs noiProblem_, run through ops/sender/hook_facts.cjs) as of the send date:
the authorization is ACTIVE on the live Central Registry, the record date the copy cites is on the live record, and
it is at most 45 days before the send date. --facts replays a saved hook_recheck.js output instead of the network.
Writes <gate.json> (every result), <gate>.stale.json ({id: reason} of failing rows, for
`hold_stale.py --stale <it> --apply`) and <gate>.release.txt (outage-held rows that now pass, for
`hold_stale.py --release <ids> --apply`). Rows whose copy has no authorization or cited date fail (they cannot be
re-checked). Read-only on the queues.
"""
import argparse, glob, json, os, subprocess, sys, tempfile
from datetime import date, datetime, timezone
p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--send-date", required=True); p.add_argument("--out", required=True)
p.add_argument("--evidence", action="append", default=[]); p.add_argument("--facts")
a = p.parse_args()
TOOLS = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.abspath(a.out)
FACTS = os.path.abspath(a.facts) if a.facts else None
sys.path.insert(0, TOOLS)
import jsi_common as jc
os.chdir(a.repo)
checked = jc.load_checked(a.evidence)
ref = date.fromisoformat(a.send_date)
items, meta, bad = [], {}, {}
for f in sorted(glob.glob("ops/queue/*.json")):
    with open(f, encoding="utf-8") as fh: q = json.load(fh)
    for r in q["records"]:
        if r.get("stage") != "S1": continue
        ready = r.get("status") in ("queued", "deferred") and not r.get("planned_for")
        outage_held = r.get("status") == "held_stale" and "TCEQ outage" in str(r.get("hold_note", ""))
        if not (ready or outage_held): continue
        try:
            hook = jc.hook_for(r["body"], jc.packet_row(q.get("packet"), r["to"]), checked, ref)
        except ValueError as ex:
            bad[r["id"]] = str(ex); continue
        items.append({"id": r["id"], "hook": hook})
        meta[r["id"]] = {"queue": os.path.basename(f)[:-5], "held": outage_held, "city": r.get("city", "")}
tmp = os.path.join(tempfile.gettempdir(), f"jsi_hook_gate_{os.getpid()}.json")
with open(tmp, "w", encoding="utf-8") as fh: json.dump(items, fh)
cmd = ["node", os.path.join("ops", "sender", "hook_facts.cjs"), tmp, a.send_date] + (["--facts", FACTS] if FACTS else [])
node = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
os.remove(tmp)
if node.returncode: sys.exit("hook_facts.cjs failed: " + node.stderr[-400:])
res = json.loads(node.stdout)
stale, release, counts = {}, [], {}
for x in res["results"]:
    m = meta[x["id"]]; prob = x["problem"]
    if prob and (x.get("fact") or {}).get("unavailable"): prob = "TCEQ outage: " + prob
    x.update(m, problem=prob)
    key = ("held " if m["held"] else "") + x["kind"] + (" fail" if prob else " pass")
    counts[key] = counts.get(key, 0) + 1
    if prob and not m["held"]: stale[x["id"]] = prob
    if not prob and m["held"]: release.append(x["id"])
for k, why in bad.items(): stale[k] = "cannot re-check its hook: " + why
report = {"send_date": a.send_date, "checked_at": datetime.now(timezone.utc).isoformat(), "tceq_available": res["tceq_available"],
          "counts": counts, "fail": len(stale), "release": release, "results": res["results"], "unclassifiable": bad}
base = OUT[:-5] if OUT.endswith(".json") else OUT
with open(OUT, "w", encoding="utf-8", newline="\n") as fh: json.dump(report, fh, indent=1)
with open(base + ".stale.json", "w", encoding="utf-8", newline="\n") as fh: json.dump(stale, fh, indent=1)
with open(base + ".release.txt", "w", encoding="utf-8", newline="\n") as fh: fh.write(",".join(release))
print(json.dumps({k: report[k] for k in ("send_date", "tceq_available", "counts", "fail", "release")}, indent=1))
