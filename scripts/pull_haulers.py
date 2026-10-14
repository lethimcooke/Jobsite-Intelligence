#!/usr/bin/env python3
"""Build a starting prospect list of roll-off and portable toilet haulers for one metro.

Source: Texas Comptroller active sales-tax permit holders (data.texas.gov jrea-zgmq, weekly),
NAICS 562111 (solid waste collection), 562119 (other waste collection) and 562991 (septic
and portable toilet services). This finds candidates only; every row still needs the
email pass (own website first, then FMCSA, then Facebook) and a fit check on the
hauler's own site before it can be pitched.

Usage:
    python3 pull_haulers.py --metro Austin --out haulers_austin.csv
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request

from metros import METROS

URL = "https://data.texas.gov/resource/jrea-zgmq.json"
NAICS = {"562111": "solid waste collection", "562119": "other waste collection", "562991": "septic / portable toilet"}
# Comptroller organization types to skip: governments and individual sole owners.
SKIP_ORG_TYPES = {"GC", "GP", "GO", "IS"}
NATIONALS = re.compile(
    r"WASTE MANAGEMENT|\bWM\b|REPUBLIC|\bBFI\b|WASTE CONNECTIONS|GFL|UNITED SITE SERVICES|ALLIED WASTE|"
    r"WASTE PRO|FRONTIER WASTE|TEXAS DISPOSAL SYSTEMS|BUDGET DUMPSTER|1-800-GOT-JUNK|JUNK KING|COLLEGE HUNKS",
    re.I,
)
FIT = re.compile(r"DUMPSTER|ROLL[ -]?OFF|DISPOSAL|WASTE|PORTABLE|PORTA|SANITATION|TOILET|POTTY|HAUL|CONTAINER|SITE SERVICE", re.I)
OFF_FIT = re.compile(r"JUNK|CLEANING|COMPOST|RECYCL|SEPTIC|PUMPING|GREASE|MAID|LAWN", re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--metro", required=True, choices=sorted(METROS))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    codes = ",".join("'%s'" % c for c in METROS[args.metro]["counties"].values())
    naics = ",".join("'%s'" % n for n in NAICS)
    params = {
        "$where": f"outlet_county_code in({codes}) AND outlet_naics_code in({naics})",
        "$limit": 50000,
    }
    with urllib.request.urlopen(URL + "?" + urllib.parse.urlencode(params), timeout=120) as resp:
        rows = json.load(resp)

    companies = {}
    skipped = {"government or individual": 0, "national": 0}
    for r in rows:
        if r.get("taxpayer_organization_type") in SKIP_ORG_TYPES:
            skipped["government or individual"] += 1
            continue
        name = r.get("taxpayer_name", "").strip()
        if NATIONALS.search(name) or NATIONALS.search(r.get("outlet_name", "")):
            skipped["national"] += 1
            continue
        c = companies.setdefault(r["taxpayer_number"], {
            "company": name,
            "outlet_names": set(),
            "yard_addresses": set(),
            "naics": set(),
            "first_permit_date": r.get("outlet_permit_issue_date", "")[:10],
        })
        c["outlet_names"].add(r.get("outlet_name", "").strip())
        c["yard_addresses"].add(f"{r.get('outlet_address', '').strip()}, {r.get('outlet_city', '').strip()} {r.get('outlet_zip_code', '')}")
        c["naics"].add(r["outlet_naics_code"])
        c["first_permit_date"] = min(c["first_permit_date"], r.get("outlet_permit_issue_date", "")[:10])

    out = []
    for c in companies.values():
        text = c["company"] + " " + " ".join(c["outlet_names"])
        if FIT.search(text) and not OFF_FIT.search(text):
            fit = "name fits"
        elif OFF_FIT.search(text):
            fit = "likely off-fit (junk removal, cleaning, septic): check site"
        else:
            fit = "unclear from name: check site"
        out.append({
            "company": c["company"],
            "outlet_names": "; ".join(sorted(c["outlet_names"])),
            "yard_addresses": "; ".join(sorted(c["yard_addresses"])),
            "naics": "; ".join(f"{n} {NAICS[n]}" for n in sorted(c["naics"])),
            "first_permit_date": c["first_permit_date"],
            "name_fit": fit,
            "metro": args.metro,
            "website": "",
            "email": "",
            "email_confidence": "",
            "services_published": "",
            "outreach_status": "Not contacted",
            "notes": "",
            "pulled_on": dt.date.today().isoformat(),
        })
    order = {"name fits": 0, "unclear from name: check site": 1}
    out.sort(key=lambda r: (order.get(r["name_fit"], 2), r["company"]))

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]) if out else ["company"])
        w.writeheader()
        w.writerows(out)
    fits = sum(1 for r in out if r["name_fit"] == "name fits")
    print(f"{args.metro}: {len(out)} candidate companies ({fits} with fitting names); "
          f"skipped {skipped} -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
