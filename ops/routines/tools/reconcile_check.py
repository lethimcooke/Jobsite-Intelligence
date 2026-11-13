"""Reconcile one manifest against the Sender Log export and Gmail Sent (read-only).

python -I reconcile_check.py --manifest ops/manifests/D.json --sender-log <csv> --sent <search_threads json> --out <report.json>

Per entry:
  SENT       Sender Log LIVE SENT row whose message_id is a Sent message to that recipient from the manifest alias
  SKIPPED    Sender Log SKIP/ERROR row (detail kept); the queue's own skip handling applies
  PENDING    no Sender Log row and no Sent message: the sender has not reached it (or did not run)
  UNCERTAIN  the log and Sent disagree (sent without a log row, a log row without Sent, wrong alias or
             recipient). Never retry an UNCERTAIN entry: check its draft (list_drafts) and Sent first.
Also writes <out>.sent_threads.json: Sent messages for SENT entries only, in search_threads shape, for
`asi_ops.py evidence` / `ji_ops.py evidence`.
"""
import argparse, csv, json, collections
p = argparse.ArgumentParser()
p.add_argument("--manifest", required=True); p.add_argument("--sender-log", required=True)
p.add_argument("--sent", required=True); p.add_argument("--out", required=True)
a = p.parse_args()
with open(a.manifest, encoding="utf-8") as fh: raw = json.load(fh)
man = raw.get("manifest", raw); d = man["send_date"]
logrows = collections.defaultdict(list)
with open(a.sender_log, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r.get("time (Central)", "").startswith(d) and r.get("mode") in ("LIVE",):
            logrows[r.get("outreach_id", "")].append(r)
with open(a.sent, encoding="utf-8") as fh: sent = json.load(fh)
msgs = {}
for t in sent.get("threads", []):
    for m in t.get("messages", []):
        if "SENT" in (m.get("labelIds") or []): msgs[m["id"]] = m
by_to = collections.defaultdict(list)
for m in msgs.values():
    for to in m.get("toRecipients") or []: by_to[to.lower()].append(m)
res, keep_threads = [], []
for e in man["entries"]:
    rid, to, alias = e["outreach_id"], e["to"].lower(), e["from_alias"].lower()
    rows = logrows.get(rid, [])
    sent_rows = [r for r in rows if r.get("result") == "SENT" and r.get("message_id")]
    skip_rows = [r for r in rows if r.get("result") in ("SKIP", "ERROR")]
    cand = [m for m in by_to.get(to, []) if m.get("date", "")[:10] >= d[:10]]
    if sent_rows:
        mid = sent_rows[-1]["message_id"]; m = msgs.get(mid)
        if m and to in [x.lower() for x in m.get("toRecipients") or []] and (m.get("sender") or "").lower() == alias:
            st, why = "SENT", f"log SENT {sent_rows[-1]['time (Central)']} CT, message {mid}"
            keep_threads.append({"id": m.get("threadId"), "messages": [m]})
        else:
            st, why = "UNCERTAIN", f"log SENT message {mid} not found in Sent to {to} from {alias}"
    elif skip_rows:
        st, why = "SKIPPED", f"{skip_rows[-1]['result']}: {skip_rows[-1].get('detail', '')[:120]}"
    elif cand:
        st, why = "UNCERTAIN", f"Sent has {len(cand)} message(s) to {to} today but the Sender Log has no row"
    else:
        st, why = "PENDING", "no Sender Log row and nothing in Sent"
    res.append({"outreach_id": rid, "stage": e["stage"], "to": to, "from_alias": alias, "status": st, "why": why})
count = collections.Counter(r["status"] for r in res)
report = {"send_date": d, "entries": len(res), "counts": dict(count), "results": res}
with open(a.out, "w", encoding="utf-8", newline="\n") as fh: json.dump(report, fh, indent=1)
with open(a.out.replace(".json", "") + ".sent_threads.json", "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"threads": keep_threads}, fh, indent=1)
print(json.dumps({"send_date": d, "entries": len(res), "counts": dict(count)}, indent=1))
for r in res:
    if r["status"] != "SENT": print(f"  {r['status']:9} {r['outreach_id']:14} {r['to']:34} {r['why']}")
