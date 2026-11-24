"""Jobsite daily status (read-only). Reads the checkout given by --repo and writes one Markdown report.

python -I daily_status.py --repo D:\\Workspace\\jobsite-intelligence-repo --out <status.md>
       [--today YYYY-MM-DD] [--now HH:MM (ET)] [--gmail-prepared found|missing|unchecked]
       [--gmail-manifest found|missing|unchecked] [--stale-out stale.json]

Checks, in order: send confirmation for the last 21 days of manifests and prepared batches; the next send day's
batch (before the JSI publish window ends, 8:35 AM ET: drafted rows plus the staged JSI-PREPARED draft or a repo
manifest; after it: a live Jobsite manifest); first-touch inventory (ready count in cities with a sender alias,
coverage in business days at 5 a day, reserve under 50); follow-ups due and the one-day copy buffer; verification
backlog (pending count and age; alert after 3 business days). --stale-out writes {id: reason} for first touches
whose hook is past the 45-day window on the next send day or cannot be read (for hold_stale.py). Nothing is
written in the repo.
"""
import argparse, collections, csv, glob, json, os, subprocess, sys
from datetime import date, datetime, timedelta, timezone

p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--out", required=True)
p.add_argument("--today"); p.add_argument("--now", help="HH:MM Eastern (default: the clock)")
p.add_argument("--gmail-manifest", default="unchecked"); p.add_argument("--gmail-prepared", default="unchecked")
p.add_argument("--stale-out")
a = p.parse_args()
TOOLS = os.path.dirname(os.path.abspath(__file__))
os.chdir(a.repo); sys.path.insert(0, "scripts"); sys.path.insert(0, TOOLS)
import ji_ops as ops
import jsi_common as jc
import mv_bulk

def eastern_now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/New_York"))
    except Exception:
        return datetime.now(timezone.utc) - timedelta(hours=5)
TODAY = date.fromisoformat(a.today) if a.today else eastern_now().date()
NOW = a.now or eastern_now().strftime("%H:%M")
PUBLISH_DONE, SEND_END, STALL_BD = "08:35", "18:00", 3          # ET: last JSI publish run done; sender window ends
HOL = jc.holidays(".")
rules = ops.load_rules("ops/rules.json")
PER_DAY = min(rules["max_s1_per_day"], ops.daily_share(rules))
SHARE = ops.daily_share(rules)
RESERVE, TARGET, FU_BUFFER = 10 * PER_DAY, 15 * PER_DAY, SHARE - PER_DAY
CITIES = jc.sending_cities(rules)

with open("data/send_ledger.csv", encoding="utf-8") as fh: ledger = list(csv.DictReader(fh))
logged = {r["outreach_id"] for r in ledger}
queues = []
for f in sorted(glob.glob("ops/queue/*.json")):
    with open(f, encoding="utf-8") as fh: queues.append((f, json.load(fh)))
recs = [r for _, q in queues for r in q["records"] if "stage" in r and "to" in r]
qstatus = {r["id"]: r.get("status") for r in recs}
alerts, L = [], []

# 1. Send confirmation
L.append("## 1. Send confirmation (last 21 days)\n")
for f in sorted(glob.glob("ops/manifests/*.json") + glob.glob("ops/prepared/*.json")):
    with open(f, encoding="utf-8") as fh: raw = json.load(fh)
    m = raw.get("manifest") or raw.get("prepared") or raw
    sd = date.fromisoformat(m["send_date"])
    if sd >= TODAY or sd < TODAY - timedelta(days=21): continue
    # accounted for: in the ledger, or the queue moved on (skipped, held, re-planned) so it is no longer this day's draft
    missing = [e["outreach_id"] for e in m["entries"] if e["outreach_id"] not in logged and qstatus.get(e["outreach_id"]) == "drafted"]
    kind = "prepared" if "prepared" in raw else "manifest"
    L.append(f"- {sd} ({kind}): {len(m['entries']) - len(missing)}/{len(m['entries'])} accounted for"
             + (f"; **UNCONFIRMED: {len(missing)}** ({', '.join(missing[:6])}{'...' if len(missing) > 6 else ''})" if missing else ""))
    if missing:
        alerts.append(f"MISSING SEND CONFIRMATION: {kind} {sd} has {len(missing)} entries still drafted with no ledger row. "
                      "Export the Sender Log and reconcile (JSI_CloseOut.md section A) before planning.")

# 2. Next send day's batch
nsd = TODAY if jc.is_bd(TODAY, HOL) and NOW < SEND_END else jc.next_bd(TODAY, HOL)
after = nsd == TODAY and NOW >= PUBLISH_DONE
mf, pf = f"ops/manifests/{nsd}.json", f"ops/prepared/{nsd}.json"
drafted = sum(1 for r in recs if r.get("planned_for") == str(nsd) and r.get("status") == "drafted")
undrafted = sum(1 for r in recs if r.get("planned_for") == str(nsd) and r.get("status") == "queued")
L.append(f"\n## 2. Batch for {nsd:%a %b %d} ({'after' if after else 'before'} the {PUBLISH_DONE} ET publish window, now {NOW} ET)\n")
L.append(f"- Drafted: {drafted}; planned but not drafted: {undrafted}; repo prepared batch: {'present' if os.path.exists(pf) else 'missing'}; "
         f"JSI-PREPARED draft: {a.gmail_prepared}; repo manifest: {'present' if os.path.exists(mf) else 'missing'}; Gmail Jobsite manifest: {a.gmail_manifest}")
if not after:
    if not drafted:
        alerts.append(f"MISSING BATCH for {nsd}: nothing drafted for that day. Run the JSI close-out (plan, drafts, prepare_batch).")
    elif a.gmail_prepared == "missing" and not os.path.exists(mf):
        alerts.append(f"MISSING PREPARED BATCH for {nsd}: {drafted} drafted, but no JSI-PREPARED draft and no repo manifest. Stage it (JSI_CloseOut.md C5b).")
else:
    if a.gmail_manifest == "missing" or (a.gmail_manifest == "unchecked" and not os.path.exists(mf) and not os.path.exists(pf)):
        alerts.append(f"MISSING MANIFEST for {nsd}: the publish window has passed and no Jobsite manifest is confirmed. "
                      "Check the Sender Log JSI-PUBLISH rows and the JSI watchdog email; JSI_PreSend.md builds one.")
if undrafted and drafted:
    alerts.append(f"PLANNED NOT DRAFTED: {undrafted} records planned for {nsd} have no draft, so the batch leaves them out.")

# 3. First-touch inventory
lists, dnc = ops.load_lists("data", rules), ops.load_dnc("data")
s1_dates = ops.s1_dates_from_ledger("data")
sent_to = {r["to"].strip().lower() for r in ledger}
sent_dom = {r["to"].split("@")[-1].strip().lower() for r in ledger} - ops.FREE
seen, inv, stale_ids = set(), collections.Counter(), {}
for r in recs:
    if r["stage"] != "S1" or r.get("status") in ("sent_confirmed", "skipped"): continue
    to = r["to"].strip().lower(); dom = to.split("@")[-1]; key = to if dom in ops.FREE else dom
    if key in seen: inv["duplicate firm"] += 1; continue
    seen.add(key)
    why = ""
    try:
        hook = jc.hook_for(r["body"], "", None, nsd)
        why = jc.window_problem(date.fromisoformat(hook["cited"]), nsd)
    except ValueError as ex:
        why = "cannot re-check its hook: " + str(ex)
    if why and r.get("status") in ("queued", "deferred"): stale_ids[r["id"]] = why
    if r.get("status") == "held_stale": b = "held (stale hook)"
    elif r.get("status") == "drafted": b = "drafted"
    elif to in sent_to or (dom not in ops.FREE and dom in sent_dom): b = "already contacted"
    elif r.get("city") not in CITIES: b = f"waits for a sender alias ({r.get('city')})"
    elif [e for e in ops.check_record(r, rules, lists, dnc, s1_dates) if "reply_to" not in e]: b = "needs copy fix"
    elif why: b = "hook past the 45-day window"
    else: b = "ready"
    inv[b] += 1
ready = inv["ready"]
cover = ready / PER_DAY
d, n = TODAY, ready
while n >= PER_DAY: d = jc.next_bd(d, HOL); n -= PER_DAY
first_short = jc.next_bd(d, HOL)
L.append("\n## 3. First-touch inventory\n")
L.append(f"- Ready: **{ready}**; coverage **{cover:.1f} business days** at {PER_DAY}/day; first day under {PER_DAY}: {first_short:%a %b %d}")
L.append("- Not ready: " + (", ".join(f"{k} {v}" for k, v in inv.items() if k != "ready") or "none"))
L.append(f"- Gap to {TARGET} (three weeks): {max(0, TARGET - ready)}")
if a.stale_out:
    with open(a.stale_out, "w", encoding="utf-8", newline="\n") as fh: json.dump(stale_ids, fh, indent=1)
    L.append(f"- Stale-hook IDs for hold_stale.py: {len(stale_ids)} (`{os.path.basename(a.stale_out)}`)")
if ready < RESERVE:
    alerts.append(f"RESERVE LOW: {ready} ready first touches, under the {RESERVE} reserve ({cover:.1f} business days).")

# 4. Follow-ups due and the copy buffer (user, Nov 19: copy one send day ahead)
def due(day):
    out = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "followups_due.py"), "--repo", ".", "--date", str(day),
                          "--out", os.path.join(os.path.dirname(os.path.abspath(a.out)), f".jsi_due_{day}.json")],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode: sys.exit("followups_due.py failed: " + out.stderr[-300:])
    path = os.path.join(os.path.dirname(os.path.abspath(a.out)), f".jsi_due_{day}.json")
    with open(path, encoding="utf-8") as fh: res = json.load(fh)["due"]
    os.remove(path)
    return res
n1 = jc.next_bd(nsd, HOL)
due_n, due_n1 = due(nsd), due(n1)
unplanned_n1 = [x for x in due_n1 if not x["planned_for"] or x["planned_for"] > str(nsd)]
need = min(FU_BUFFER, len(unplanned_n1)); on_hand = sum(1 for x in unplanned_n1 if x["copy_ready_id"])
L.append("\n## 4. Follow-ups\n")
L.append(f"- Due by {nsd:%a %b %d}: {len(due_n)} ({dict(collections.Counter(x['next'] for x in due_n))}); planned or drafted: {sum(1 for x in due_n if x['planned_for'])}")
L.append(f"- Copy buffer for {n1:%a %b %d}: {on_hand} with validated copy of {need} needed (up to {FU_BUFFER})")
if on_hand < need:
    alerts.append(f"FOLLOW-UP COPY BUFFER LOW: {on_hand} follow-ups have copy for {n1} but {need} are due. "
                  "Write the next send day's S2/S5 copy now (JSI_CloseOut.md C2b).")

# 5. Verification backlog
st = mv_bulk.load_state(".")
pend = mv_bulk.pending(".", st)
waiting = [e for b in st["batches"] if not b.get("imported") for e in b["emails"]]
since = [date.fromisoformat(x["since"]) for x in pend] + [date.fromisoformat(b["collected_at"]) for b in st["batches"] if not b.get("imported")]
L.append("\n## 5. Verification backlog\n")
L.append(f"- Not yet in a batch: {len(pend)}; in the shared outbox waiting for website results: {len(waiting)}")
if since:
    oldest = min(since); age = sum(1 for i in range((TODAY - oldest).days) if jc.is_bd(oldest + timedelta(i + 1), HOL))
    L.append(f"- Oldest waiting since {oldest} ({age} business days)")
    if age > STALL_BD:
        alerts.append(f"VERIFICATION STALLED: {len(pend) + len(waiting)} addresses waiting, oldest since {oldest} ({age} business days). "
                      r"Upload the newest D:\Workspace\austin-signage-repo\verify\outbox\<date>.csv on the MillionVerifier website and save the results in D:\Workspace\austin-signage-repo\verify\inbox\.")

head = [f"# JSI daily status, {TODAY:%a %b %d, %Y} (read-only)\n", "## Alerts\n"]
head += [f"- **{x}**" for x in alerts] or ["- none"]
with open(a.out, "w", encoding="utf-8", newline="\n") as fh: fh.write("\n".join(head + [""] + L) + "\n")
print("\n".join(head))
print(f"ready {ready}, coverage {cover:.1f} bd, follow-ups due {len(due_n)}, copy buffer {on_hand}/{need}, verification waiting {len(pend) + len(waiting)}")
