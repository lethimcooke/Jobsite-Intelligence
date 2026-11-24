#!/usr/bin/env python3
"""Write S1 drafts from a hook packet CSV (build_packet.py output), one per hauler.

Follows docs/Outreach_Copy_v2.md (S1, Tier B) and ops/rules.json (exact price line,
signature, opt-out footer). Site names and operators are re-cased for reading; review the
names table at the top of the output file, and any site type marked "construction".

Usage:
    python3 write_s1.py --packet packet.csv --metro Houston --out outreach/H1-H2_S1_Copy.md \
        [--site-type RN=industrial RN=commercial ...] [--name "Bj Services=BJ Services" ...]
"""
import argparse
import csv
import datetime as dt
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = json.load(open(os.path.join(HERE, "..", "ops", "rules.json"), encoding="utf-8"))
SMALL = {"Of", "And", "At", "The", "To"}
UPPER = {"LLC", "LP", "LLP", "II", "III", "FM", "SH", "US", "IH", "ISD", "HCA", "NW", "NE", "SW", "SE", "DC", "CR"}


def recase(text):
    words = []
    for i, w in enumerate(text.split()):
        core = re.sub(r"[^A-Za-z]", "", w).upper()
        if core in UPPER:
            words.append(w.upper())
        elif core == "INC":
            words.append(w.capitalize())
        elif i and w.title() in SMALL:
            words.append(w.lower())
        else:
            words.append(w.capitalize() if not re.match(r"^\d", w) else w.lower())
    return " ".join(words)


def distance(miles):
    m = int(float(miles))
    return "a mile" if m <= 1 else f"{m} miles"


def month_day(iso):
    """'2026-11-09' -> 'November 9' (portable: Windows strftime rejects %-d)."""
    d = dt.date.fromisoformat(iso)
    return f"{d:%B} {d.day}"


def fit_lines(r, kind, fit):
    """v2 fit line and close. With a yard distance, the yard variant; without one (no published yard),
    the site is placed against the hauler's published areas, as approved from H11 on."""
    article = "an" if kind[0] in "aeiou" else "a"
    miles = (r.get("miles_from_yard_our_read") or "").strip()
    if miles:
        yard = recase(r.get("yard_city") or "") or "nearby"
        return (f"It's about {distance(miles)} from your {yard} yard, and {article} {kind} job like this is the "
                f"kind your {fit} serve; that's our read, not the filing.",
                "Want five sites like this near your yard, free?")
    area = (r.get("service_area_city") or "").strip()
    if not area and "," in r["site_address"]:
        area = recase(r["site_address"].split(",")[1].strip())
    return (f"It's in {area or 'your area'}, one of the areas you serve, and {article} {kind} job like this is "
            f"the kind your {fit} serve; that's our read, not the filing.",
            "Want five sites like this in your service area, free?")


def greeting_name(company):
    """Company name without its legal suffix, for 'Hi [Company] team'."""
    return re.sub(r",?\s+(LLC|L\.L\.C\.|LP|LLP|Inc\.?|Ltd\.?|Co\.?|Corp\.?)$", "", company).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--packet", required=True)
    ap.add_argument("--metro", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--site-type", nargs="*", default=[], help="RN=industrial|commercial|school|construction")
    ap.add_argument("--name", nargs="*", default=[], help='"Recased=Correct" overrides for names')
    args = ap.parse_args()

    sender = RULES["senders"][args.metro]
    signature = RULES["signature_template"].format(**sender)
    price = RULES["standard_price_line"]
    footer = RULES["footer"]["text"]
    types = dict(x.split("=", 1) for x in args.site_type)
    fixes = dict(x.split("=", 1) for x in args.name)

    def fix(s):
        for a, b in fixes.items():
            s = s.replace(a, b)
        return s

    rows = list(csv.DictReader(open(args.packet, encoding="utf-8")))
    out = [f"# {rows[0]['batch']} to {rows[-1]['batch']}: S1 copy ({args.metro})\n",
           f"Generated {dt.date.today().isoformat()} from the hook packet. Tier B (no public record names a "
           f"hauler at a job site). Sender: {sender['display']} <{sender['from']}>. Every fact is from the "
           "TCEQ Central Registry record cited in the row; distance and fit are labeled as our read.\n",
           "Before drafting: re-open each site's source URL, confirm the hauler's site still lists the services "
           "named, and run the validator.\n"]
    for n, r in enumerate(rows, 1):
        site = fix(recase(r["site_name"]))
        street = fix(recase(r["site_address"].split(",")[0]))
        city = recase(r["site_address"].split(",")[1]) if "," in r["site_address"] else ""
        operator = fix(recase(r["operator_on_file"].split(";")[0]))
        company = fix(recase(r["company"]))
        date = month_day(r["date_on_file"])
        kind = types.get(r["site_rn"], "construction")
        fit_line, close = fit_lines(r, kind, r["fit_phrase_our_read"])
        body = (
            f"Hi {greeting_name(company)} team,\n\n"
            f"TCEQ's Central Registry lists a construction stormwater authorization ({r['tceq_authorization']}) "
            f"with a record date of {date} for {site} at {street}{', ' + city if city else ''} in "
            f"{recase(r['county'])} County. The operator on file is {operator}.\n\n"
            f"{fit_line}\n\n"
            f"We're a research service with no tie to the project. {price}\n\n"
            f"{close}\n\n"
            f"{signature}\n\n{footer}"
        )
        subject = site if len(site) >= 10 else f"{site}, {street}"
        out.append(f"\n## {n}. {r['batch']}: {company}\n")
        out.append(f"- To: {r['email']} ({r['email_confidence']})\n- Subject: {subject}\n- Subject arm: A\n"
                   f"- Site record: {r['site_source_url']}\n- Hauler publishes: {r['services_published']}\n")
        out.append("\n```\n" + body + "\n```\n")
    text = "".join(out)
    if "—" in text:
        raise SystemExit("em dash found; fix before writing")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    print(f"{len(rows)} S1 drafts -> {args.out}")


if __name__ == "__main__":
    main()
