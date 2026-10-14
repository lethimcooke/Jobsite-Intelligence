#!/usr/bin/env python3
"""Pair each hauler with its nearest usable construction site and write a hook packet.

Inputs are the outputs of pull_noi_sites.py and enrich_haulers.py. Sites need a street
address (the US Census geocoder places it); haulers need a yard address. Distances are
straight-line miles, our read, rounded.

Rules (from the ASI tracker, carried over):
- Only sites with priority 1-2 (commercial, industrial, institutional, amenity, multifamily).
- Sites flagged for a possible person's name are left out unless their RN is passed with
  --allow-rn after a human review.
- A site is used at most once per batch (--batch-size, default 10).
- Only haulers with `fit` true and an A or B-dir email.

Usage:
    python3 build_packet.py --sites sites.csv --haulers haulers.csv --batch-prefix H \
        --count 20 --out-csv packet.csv --out-md packet.md [--allow-rn RN1 RN2 ...] [--skip-rn RN ...]
"""
import argparse
import csv
import json
import math
import sys
import time
import urllib.parse
import urllib.request

GEOCODER = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"


def geocode(address, cache):
    if address in cache:
        return cache[address]
    params = {"address": address, "benchmark": "Public_AR_Current", "format": "json"}
    point = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(GEOCODER + "?" + urllib.parse.urlencode(params), timeout=60) as r:
                matches = json.load(r)["result"]["addressMatches"]
            if matches:
                c = matches[0]["coordinates"]
                point = (c["y"], c["x"])
            break
        except Exception:
            time.sleep(2 * (attempt + 1))
    cache[address] = point
    return point


def miles(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))


def services_phrase(svc):
    """Plain-words description of what the hauler publishes, for the S1 fit line."""
    s = [x.strip() for x in svc.split(",") if x.strip()]
    sizes = [x.replace("-yd", "") for x in s if x.endswith("-yd")]
    parts = []
    if "roll-off" in s:
        if len(sizes) >= 2:
            parts.append(f"{sizes[0]}- to {sizes[-1]}-yard roll-offs")
        elif sizes:
            parts.append(f"{sizes[0]}-yard roll-offs")
        else:
            parts.append("roll-off containers")
    if "portable toilets" in s:
        parts.append("portable toilets")
    if "restroom trailers" in s and "portable toilets" not in s:
        parts.append("restroom trailers")
    return " and ".join(parts) if parts else "site services"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sites", required=True)
    ap.add_argument("--haulers", required=True)
    ap.add_argument("--batch-prefix", required=True, help="e.g. H for Houston: batches H1, H2, ...")
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--allow-rn", nargs="*", default=[], help="flagged sites cleared by human review")
    ap.add_argument("--skip-rn", nargs="*", default=[], help="sites to leave out (conflicts, poor fit)")
    ap.add_argument("--skip-company", nargs="*", default=[], help="haulers to leave out (conflicts, do-not-contact)")
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    cache = {}
    sites = []
    for s in csv.DictReader(open(args.sites)):
        if s["priority"] not in ("1", "2") or not s["street_address"]:
            continue
        if s["regulated_entity_rn"] in args.skip_rn:
            continue
        if "person" in s["flags"] and s["regulated_entity_rn"] not in args.allow_rn:
            continue
        pt = geocode(f"{s['street_address']}, {s['city'] or s['county'] + ' County'}, TX", cache)
        if pt:
            s["_pt"] = pt
            sites.append(s)

    haulers = []
    for h in csv.DictReader(open(args.haulers)):
        if h["fit"] != "True" or h["email_confidence"] not in ("A", "B-dir") or h["outreach_status"] != "Not contacted":
            continue
        if h["company"] in args.skip_company:
            continue
        pt = geocode(h["yard_address"], cache)
        if pt:
            h["_pt"] = pt
            haulers.append(h)
    haulers = haulers[: args.count]

    rows = []
    for i, h in enumerate(haulers):
        batch = f"{args.batch_prefix}{i // args.batch_size + 1}"
        used = {r["site_rn"] for r in rows if r["batch"] == batch}
        options = sorted((miles(h["_pt"], s["_pt"]), s) for s in sites if s["regulated_entity_rn"] not in used)
        if not options:
            continue
        d, s = options[0]
        rows.append({
            "batch": batch,
            "company": h["company"],
            "email": h["email"],
            "email_confidence": h["email_confidence"],
            "yard_address": h["yard_address"],
            "yard_city": h["yard_address"].split(",")[-2].strip().title() if h["yard_address"].count(",") >= 2 else "",
            "services_published": h["services_published"],
            "fit_phrase_our_read": services_phrase(h["services_published"]),
            "areas_published": h["areas_published"],
            "site_name": s["site_name"].title(),
            "site_address": f"{s['street_address'].title()}, {(s['city'] or '').title()}".strip(", "),
            "county": s["county"].title(),
            "tceq_authorization": s["tceq_authorizations"].split()[0],
            "date_on_file": s["date_on_file"],
            "operator_on_file": s["operators_on_file"],
            "project_type_our_read": s["project_type_our_read"],
            "miles_from_yard_our_read": round(d),
            "site_rn": s["regulated_entity_rn"],
            "site_source_url": s["source_url"],
            "usdot": h["usdot"],
            "flags": s["flags"],
        })

    with open(args.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    with open(args.out_md, "w") as f:
        f.write(f"# Hook packet: batches {args.batch_prefix}1 to {rows[-1]['batch']}\n\n")
        f.write("Facts come from the TCEQ Central Registry (site) and FMCSA plus the hauler's own website "
                "(hauler). Distance and fit are our read. Every row still needs the ops checks before copy: "
                "record re-opened, ASI conflict check, do-not-contact, no person's name.\n\n")
        f.write("| # | Batch | Hauler | Email (grade) | Yard | Publishes | Site | TCEQ auth / date | Operator on file | Miles |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for n, r in enumerate(rows, 1):
            f.write(f"| {n} | {r['batch']} | {r['company']} | {r['email']} ({r['email_confidence']}) | {r['yard_city']} | "
                    f"{r['fit_phrase_our_read']} | {r['site_name']}, {r['site_address']} | {r['tceq_authorization']} / "
                    f"{r['date_on_file']} | {r['operator_on_file'].title()} | {r['miles_from_yard_our_read']} |\n")
    print(f"{len(rows)} hauler-site pairs from {len(haulers)} haulers and {len(sites)} geocoded sites -> "
          f"{args.out_csv}, {args.out_md}", file=sys.stderr)


if __name__ == "__main__":
    main()
