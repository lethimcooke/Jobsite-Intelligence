"""Hold Jobsite first touches whose hook went stale (same tool as ASI's), so `plan` never picks them (plan only takes queued/deferred).

python -I hold_stale.py --repo <checkout> --stale <stale.json from daily_status.py --stale-out or hook_gate.py> [--apply]
           [--release <ID,ID,...>]

--apply sets each listed queued/deferred/drafted S1 to status 'held_stale' (a drafted row loses its planned_for) with a dated note; without it, prints
what it would do. --release puts held rows back to 'deferred' (use after a re-hook or a fresh re-check).
Files are written with LF endings.
"""
import argparse, glob, json, os
from datetime import date
p = argparse.ArgumentParser()
p.add_argument("--repo", required=True); p.add_argument("--stale"); p.add_argument("--apply", action="store_true")
p.add_argument("--release", default="")
a = p.parse_args()
stale = {}
if a.stale:
    with open(a.stale, encoding="utf-8") as fh: stale = json.load(fh)
release = {x for x in a.release.split(",") if x}
changed = []
for f in sorted(glob.glob(os.path.join(a.repo, "ops", "queue", "*.json"))):
    with open(f, encoding="utf-8") as fh: q = json.load(fh)
    hit = False
    for r in q["records"]:
        if r.get("stage", q.get("stage")) != "S1": continue
        if r["id"] in stale and r.get("status") in ("queued", "deferred", "drafted"):
            changed.append((r["id"], r["status"], "held_stale", stale[r["id"]]))
            if a.apply:
                # A drafted row leaves its send day; its Gmail draft and draft record stay untouched for a later release.
                if r.get("planned_for"): r["held_from"] = r.pop("planned_for")
                r["status"] = "held_stale"; r["hold_note"] = f"{date.today()}: stale hook ({stale[r['id']]}); needs a re-hook"; hit = True
        elif r["id"] in release and r.get("status") == "held_stale":
            changed.append((r["id"], "held_stale", "deferred", "released"))
            if a.apply:
                r["status"] = "deferred"; r["hold_note"] = f"{date.today()}: released"; hit = True
    if hit:
        with open(f, "w", encoding="utf-8", newline="\n") as fh: json.dump(q, fh, indent=2, ensure_ascii=False); fh.write("\n")
for c in changed: print(("APPLIED " if a.apply else "WOULD   ") + " ".join(map(str, c)))
print(f"{len(changed)} change(s){'' if a.apply else ' (dry run)'}")
