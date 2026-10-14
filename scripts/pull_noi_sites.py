#!/usr/bin/env python3
"""Pull new construction stormwater sites (TCEQ TXR15 authorizations) for one metro.

Source: TCEQ Central Registry files on data.texas.gov (free, updated daily). One row per
site (regulated entity, RN), with every TXR15 authorization and operator on it.

Usage:
    python3 pull_noi_sites.py --metro Austin --days 14 --out sites_austin.csv

Rules carried over from ASI:
- Business names only. Operators listed as sole proprietorships or individuals are dropped;
  a site with no business operator left is dropped. Site names that look like a person's
  name are flagged for review, never sent unreviewed.
- The CSV holds facts from the record plus our read (`project_type`, `priority`), labeled.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request

from metros import METROS, TCEQ_FILES

BASE = "https://data.texas.gov/resource/{id}.json"
INDIVIDUAL_TYPES = {"SOLE PROPRIETORSHIP", "INDIVIDUAL OWNER TYPE"}
GOVERNMENT_TYPES = {"COUNTY GOVERNMENT", "CITY GOVERNMENT", "STATE GOVERNMENT", "FEDERAL GOVERNMENT", "OTHER GOVERNMENT"}

NATIONAL_BUILDERS = re.compile(
    r"LENNAR|PULTE|MERITAGE|TAYLOR MORRISON|HORTON|PERRY HOMES|HIGHLAND HOMES|CENTURY|KB HOME|"
    r"ASHTON|WEEKLEY|CLAYTON|TRI POINTE|M/I HOMES|TOLL|SHEA|MATTAMY|DREAM FINDERS|DFH|"
    r"CONTINENTAL HOMES|FORESTAR|BLOOMFIELD|CHESMAR|GEHAN|HISTORYMAKER|STARLIGHT|BRIGHTLAND|CASTLEROCK",
    re.I,
)
UTILITY = re.compile(
    r"\b(WATER|WASTEWATER|SEWER|LIFT STATION|GAS|PIPELINE|ELECTRIC|SUBSTATION|TRANSMISSION|FIBER|"
    r"DRAINAGE|LINE|MAIN|OFFSITE|POND|CHANNEL|DETENTION)\b"
)
UTILITY_OPS = re.compile(r"ATMOS|ONCOR|CENTERPOINT|ENTERGY|PEDERNALES|BLUEBONNET|AUSTIN ENERGY|CPS ENERGY", re.I)
ROAD = re.compile(r"\b(ROAD|RD|BLVD|PKWY|HWY|SH|FM|IH|US|WIDENING|STREET|STREETS|BRIDGE|TXDOT|IMPROVEMENTS|PAVING|SIDEWALK)\b")
SUBDIVISION = re.compile(r"\b(PHASE|PHS|PH|UNIT|SECTION|SEC|SUBDIVISION|ESTATES|LOTS|HOMEBUILDING|TRACT)\b")
MULTIFAMILY = re.compile(r"APARTMENT|MULTIFAMILY|TOWNHOME|LOFTS|RESIDENCES|SENIOR LIVING|BTR|BUILD TO RENT")
ENERGY = re.compile(r"SOLAR|BESS|BATTERY STORAGE|WIND|POWER PLANT|DATA CENTER")
AMENITY = re.compile(r"AMENITY|CLUBHOUSE|RECREATION|AQUATIC|(?<!OFFICE )(?<!BUSINESS )(?<!INDUSTRIAL )(?<!TECHNOLOGY )PARK\b")
RESIDENTIAL_OPS = re.compile(r"RESIDENTIAL|HOMEOWNERS|HOA\b", re.I)
UTILITY_INDUSTRY = re.compile(r"Electric|Water Supply|Sewage|Pipeline|Natural Gas Distribution", re.I)
# Common words that mean a two-word site name is not a person's name.
NOT_PERSON = re.compile(
    r"\b(PARK|PLAZA|CENTER|CENTRE|RANCH|FARMS?|CREEK|HILLS?|OAKS?|VILLAGE|POINTE?|CROSSING|COMMONS|"
    r"STORAGE|SCHOOL|CHURCH|ADDITION|DEVELOPMENT|INDUSTRIAL|BUSINESS|OFFICE|RETAIL|MEDICAL|CAMPUS|"
    r"PROJECT|SITE|YARD|PLANT|TERMINAL|WAREHOUSE|LOGISTICS|SPRINGS|LAKE|TRAILS?|RESERVE|LANDING|HEIGHTS)\b"
)


def get(dataset, params):
    url = BASE.format(id=dataset) + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as resp:
        return json.load(resp)


def project_type(site_name, operators, industry=""):
    """Our read of the project type from the site name and operators (not a filed fact)."""
    ops = " ".join(operators)
    if ENERGY.search(site_name):
        return "energy", 4
    if UTILITY.search(site_name) or UTILITY_OPS.search(ops) or UTILITY_INDUSTRY.search(industry):
        return "utility / drainage", 4
    if ROAD.search(site_name) and not AMENITY.search(site_name):
        return "road / street", 4
    if MULTIFAMILY.search(site_name):
        return "multifamily", 2
    if AMENITY.search(site_name):
        return "amenity / recreation", 1
    if SUBDIVISION.search(site_name) or NATIONAL_BUILDERS.search(ops) or RESIDENTIAL_OPS.search(ops):
        return "subdivision / homebuilding", 3
    return "commercial / industrial / institutional", 1


def looks_like_person(site_name):
    words = site_name.split()
    if len(words) in (2, 3) and not re.search(r"\d", site_name) and not NOT_PERSON.search(site_name):
        if not (SUBDIVISION.search(site_name) or ROAD.search(site_name) or UTILITY.search(site_name)):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--metro", required=True, choices=sorted(METROS))
    ap.add_argument("--days", type=int, default=14, help="look back this many days (default 14)")
    ap.add_argument("--out", required=True, help="output CSV path")
    args = ap.parse_args()

    counties = list(METROS[args.metro]["counties"])
    since = (dt.date.today() - dt.timedelta(days=args.days)).isoformat()
    county_list = ",".join("'%s'" % c for c in counties)
    where = (
        "program_code='STORM' AND starts_with(additional_id_text,'TXR15') "
        f"AND affil_begin_dt >= '{since}' AND re_phys_loc_addr_county in({county_list})"
    )
    cols = (
        "ref_num_txt,reg_ent_name,re_phys_loc_addr_line_1,re_phys_loc_city,re_phys_loc_addr_county,"
        "re_phys_loc_desc,indus_typ_name,princ_name,name_txt,additional_id_text,additional_id_status,affil_begin_dt"
    )

    rows = []
    for dataset in TCEQ_FILES:
        batch = get(dataset, {"$select": cols, "$where": where, "$limit": 50000})
        for r in batch:
            r["_dataset"] = dataset
        rows.extend(batch)

    sites = {}
    for r in rows:
        rn = r["ref_num_txt"]
        s = sites.setdefault(rn, {
            "rn": rn,
            "site_name": (r.get("reg_ent_name") or "").strip(),
            "street_address": (r.get("re_phys_loc_addr_line_1") or "").strip(),
            "city": (r.get("re_phys_loc_city") or "").strip(),
            "county": r.get("re_phys_loc_addr_county", ""),
            "location_description": (r.get("re_phys_loc_desc") or "").strip(),
            "industry_filed": r.get("indus_typ_name") or "",
            "authorizations": set(),
            "first_date": r["affil_begin_dt"][:10],
            "operators": {},
            "dataset": r["_dataset"],
        })
        s["authorizations"].add(r.get("additional_id_text", ""))
        s["first_date"] = min(s["first_date"], r["affil_begin_dt"][:10])
        if r.get("princ_name"):
            s["operators"][r["princ_name"].strip()] = r.get("name_txt", "")

    out_rows = []
    dropped_individual = 0
    for s in sites.values():
        business_ops = {n: t for n, t in s["operators"].items() if t not in INDIVIDUAL_TYPES}
        if not business_ops:
            dropped_individual += 1
            continue
        ptype, priority = project_type(s["site_name"], list(business_ops), s["industry_filed"])
        flags = []
        if looks_like_person(s["site_name"]):
            flags.append("site name may be a person's name: review before use")
        if NATIONAL_BUILDERS.search(" ".join(business_ops)):
            flags.append("national homebuilder on site")
            priority = max(priority, 3)
        if any(t in GOVERNMENT_TYPES for t in business_ops.values()):
            flags.append("government operator")
            priority = max(priority, 3)
        out_rows.append({
            "priority": priority,
            "project_type_our_read": ptype,
            "date_on_file": s["first_date"],
            "site_name": s["site_name"],
            "street_address": s["street_address"],
            "city": s["city"],
            "county": s["county"],
            "location_description": s["location_description"],
            "tceq_authorizations": " ".join(sorted(a for a in s["authorizations"] if a)),
            "regulated_entity_rn": s["rn"],
            "operators_on_file": "; ".join(sorted(business_ops)),
            "operator_types": "; ".join(sorted(set(business_ops.values()))),
            "industry_filed": s["industry_filed"],
            "flags": "; ".join(flags),
            "source_url": f"https://data.texas.gov/resource/{s['dataset']}.json?ref_num_txt={s['rn']}&program_code=STORM",
            "checked_on": dt.date.today().isoformat(),
        })

    # Best first: lowest priority number, then newest record.
    out_rows.sort(key=lambda r: r["date_on_file"], reverse=True)
    out_rows.sort(key=lambda r: r["priority"])
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]) if out_rows else ["priority"])
        w.writeheader()
        w.writerows(out_rows)

    by_type = {}
    for r in out_rows:
        by_type[r["project_type_our_read"]] = by_type.get(r["project_type_our_read"], 0) + 1
    print(f"{args.metro}: {len(out_rows)} sites since {since} "
          f"({dropped_individual} dropped as individual-owned) -> {args.out}", file=sys.stderr)
    for k, v in sorted(by_type.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}", file=sys.stderr)


if __name__ == "__main__":
    main()
