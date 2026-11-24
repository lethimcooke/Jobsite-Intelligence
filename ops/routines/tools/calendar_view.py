"""Rolling three-week Jobsite first-touch calendar from the live queues (read-only).

python -I calendar_view.py --repo . --start YYYY-MM-DD --out ops/routines/CALENDAR.md [--stale stale.json]

Counts first touches already drafted for a day first, then fills each business day (weekends and holidays.txt
skipped) with ready rows, up to max_s1_per_day (5): status queued/deferred, city with a sender alias (Houston), not
stale or held, hook inside the 45-day TCEQ window on that day, not contacted (ledger by address and domain), one per
firm; rows whose window closes soonest go first. Then follow-ups from followups_due.py fill each day's remaining
share (15 minus that day's first touches), oldest S1 first. Drafts whose day passed unsent count on the first day
(the next plan carries them).
"""
import argparse, collections, csv, glob, json, os, subprocess, sys
from datetime import date, timedelta
p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--stale"); p.add_argument("--start", required=True)
p.add_argument("--out", required=True)
a = p.parse_args()
TOOLS = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.abspath(a.out)
os.chdir(a.repo); sys.path.insert(0, "scripts"); sys.path.insert(0, TOOLS)
import ji_ops as ops
import jsi_common as jc
HOL = jc.holidays(".")
rules = ops.load_rules("ops/rules.json")
PER_DAY = min(rules["max_s1_per_day"], ops.daily_share(rules)); SHARE = ops.daily_share(rules); RESERVE = 10 * PER_DAY
CITIES = jc.sending_cities(rules)
days = jc.bdays_from(date.fromisoformat(a.start), 15, HOL)
stale = set()
if a.stale:
    with open(a.stale, encoding="utf-8") as fh: stale = set(json.load(fh))
with open("data/send_ledger.csv", encoding="utf-8") as fh: led = list(csv.DictReader(fh))
sent_to = {r["to"].lower() for r in led}; sent_dom = {r["to"].split("@")[-1].lower() for r in led} - ops.FREE
drafted = collections.defaultdict(list); cands = []; seen = set(); waiting = collections.Counter()
for f in sorted(glob.glob("ops/queue/*.json")):
    with open(f, encoding="utf-8") as fh: q = json.load(fh)
    for r in q["records"]:
        if r.get("stage") != "S1": continue
        to = r["to"].lower(); dom = to.split("@")[-1]; key = to if dom in ops.FREE else dom
        if r.get("status") == "drafted" and r.get("planned_for"):
            # a draft whose day passed unsent is carried into the next plan (ji_ops plan_day), so it counts on day 1
            drafted[max(r["planned_for"], str(days[0]))].append(r); seen.add(key); continue
        if r.get("status") not in ("queued", "deferred") or r["id"] in stale: continue
        if to in sent_to or (dom not in ops.FREE and dom in sent_dom) or key in seen: continue
        if r.get("city") not in CITIES: waiting[r.get("city")] += 1; continue
        try:
            cited = date.fromisoformat(jc.hook_for(r["body"], "", None, days[0])["cited"])
        except ValueError:
            continue
        seen.add(key)
        cands.append((cited + timedelta(jc.SITE_WINDOW_D), r))
cands.sort(key=lambda x: (x[0], x[1]["id"]))
rows, used = [], set()
for d in days:
    pre = [r for r in drafted.get(str(d), [])]
    take = []
    for last_ok, r in cands:
        if len(pre) + len(take) >= PER_DAY: break
        if r["id"] in used or d > last_ok: continue
        take.append(r); used.add(r["id"])
    rows.append((d, len(pre), len(take)))
ready = len(cands); expired = sum(1 for last_ok, r in cands if r["id"] not in used)
filled = sum(p_ + t for _, p_, t in rows); slots = PER_DAY * len(days)
first_short = next((d for d, p_, t in rows if p_ + t < PER_DAY), None)
L = ["# JSI first-touch calendar (rolling, 15 business days)", "",
     f"Generated from the live queues by `tools/calendar_view.py`. Start {days[0]:%a %b %d}. Holidays from `holidays.txt`. "
     f"{PER_DAY} first touches a day; follow-ups fill the rest of the {SHARE}.", "",
     f"- **Ready first touches (not yet drafted): {ready}** (Houston); waiting for a sender alias: {dict(waiting) or 0}",
     f"- Drafted and planned: {sum(len(v) for v in drafted.values())} ({', '.join(f'{k}: {len(v)}' for k, v in sorted(drafted.items())) or 'none'})",
     f"- Coverage: {ready / PER_DAY:.1f} business days at {PER_DAY}/day; {expired} ready rows pass their 45-day window before a free slot",
     f"- First underfilled day: {first_short:%a %b %d}" if first_short else "- First underfilled day: none in 15 business days",
     f"- Three-week target {slots}; filled {filled}; **gap {slots - filled}**",
     f"- Reserve alert (under {RESERVE} ready): {'YES' if ready < RESERVE else 'no'}", "",
     "| Day | Date | Drafted | Planned from reserve | Total | Short by |", "|---|---|---|---|---|---|"]
for n, (d, p_, t) in enumerate(rows, 1):
    L.append(f"| {n} | {d:%a %b %d} | {p_} | {t} | {p_ + t} | {PER_DAY - p_ - t} |")
fu_json = os.path.join(os.path.dirname(OUT), ".jsi_followups_cache.json")
r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "followups_due.py"), "--repo", ".", "--date", str(days[-1]), "--out", fu_json],
                   capture_output=True, text=True, encoding="utf-8")
if r.returncode: sys.exit("followups_due.py failed: " + r.stderr[-300:])
with open(fu_json, encoding="utf-8") as fh: fu = json.load(fh)["due"]
os.remove(fu_json)
planned_fu = collections.Counter(max(x["planned_for"], str(days[0])) for x in fu if x["planned_for"])
backlog = [x for x in fu if not x["planned_for"]]; taken = set()
L += ["", "## Follow-ups", "",
      f"From `tools/followups_due.py`: {len(fu)} due by {days[-1]:%b %d} from sends already logged; {len(fu) - len(backlog)} already planned "
      f"or drafted, {len(backlog)} unplanned ({sum(1 for x in backlog if x['copy_ready_id'])} with validated copy). "
      "S2s and S5s for first touches not yet sent are not projected.", "",
      f"| Date | Planned or drafted | From backlog | of which copy validated | needs copy | Day total / {SHARE} |", "|---|---|---|---|---|---|"]
for d, p_, t in rows:
    room = max(0, SHARE - p_ - t - planned_fu[str(d)])
    take = [x for x in backlog if x["to"] not in taken and x["due"] <= str(d)][:room]
    for x in take: taken.add(x["to"])
    ok = sum(1 for x in take if x["copy_ready_id"])
    pl = min(planned_fu[str(d)], max(0, SHARE - p_ - t))      # plan caps the day at the share; the rest wait a day
    L.append(f"| {d:%a %b %d} | {pl} | {len(take)} | {ok} | {len(take) - ok} | {p_ + t + pl + len(take)} |")
L.append(f"\nFollow-ups still unassigned after {days[-1]:%b %d}: {len([x for x in backlog if x['to'] not in taken])}.")
with open(OUT, "w", encoding="utf-8", newline="\n") as fh: fh.write("\n".join(L) + "\n")
print("\n".join(L[4:10]))
