"""Reply rates from data/outreach_results.csv.

Usage: python3 scripts/outreach_stats.py

Update the CSV whenever an outcome changes (replied, bounced, declined, paid).
Outcomes: no reply | replied | declined | bounced | paid. "Engaged" counts
replied, declined and paid, since each of those answered us.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "data" / "outreach_results.csv"
ENGAGED = {"replied", "declined", "paid"}


def table(rows, key, title):
    groups = defaultdict(list)
    for r in rows:
        groups[r[key]].append(r)
    print(f"\n{title}")
    print(f"  {'group':32} {'sent':>4} {'replied':>7} {'rate':>6} {'bounced':>7}")
    for g, rs in sorted(groups.items(), key=lambda kv: (-sum(x['outcome'] in ENGAGED for x in kv[1]), -len(kv[1]))):
        delivered = [x for x in rs if x["outcome"] != "bounced"]
        eng = sum(x["outcome"] in ENGAGED for x in rs)
        rate = f"{eng / len(delivered):.0%}" if delivered else "-"
        print(f"  {g[:32]:32} {len(rs):>4} {eng:>7} {rate:>6} {len(rs) - len(delivered):>7}")


def main():
    rows = list(csv.DictReader(open(PATH, newline="")))
    # Historical records kept subject-arm or copy-version notes in this field.
    # Group by site type while preserving the evidence CSV unchanged.
    for row in rows:
        row["hook_type"] = row.get("hook_type", "").split(";", 1)[0].strip() or "unknown"
    delivered = [r for r in rows if r["outcome"] != "bounced"]
    eng = [r for r in rows if r["outcome"] in ENGAGED]
    paid = [r for r in rows if r["outcome"] == "paid"]
    print(f"Contacted {len(rows)} | delivered {len(delivered)} | replied {len(eng)} ({len(eng) / max(len(delivered), 1):.0%}) | paid {len(paid)}")
    table(rows, "hook_type", "By project type")
    table(rows, "company_type", "By company type")
    table(rows, "batch", "By batch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
