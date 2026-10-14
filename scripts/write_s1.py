#!/usr/bin/env python3
"""Write S1 drafts from a hook packet CSV (build_packet.py output), one per hauler.

Follows docs/Outreach_Copy_v1.md (S1, Tier B) and ops/rules.json (exact price line,
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
RULES = json.load(open(os.path.join(HERE, "..", "ops", "rules.json")))
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
    m = int(miles)
    return "a mile" if m <= 1 else f"{m} miles"


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

    rows = list(csv.DictReader(open(args.packet)))
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
        date = dt.date.fromisoformat(r["date_on_file"]).strftime("%B %-d")
        kind = types.get(r["site_rn"], "construction")
        yard = recase(r["yard_city"]) or "nearby"
        body = (
            f"Hi {greeting_name(company)} team,\n\n"
            f"TCEQ's Central Registry lists a construction stormwater authorization ({r['tceq_authorization']}) "
            f"dated {date} for {site} at {street}{', ' + city if city else ''} in {r['county']} County. "
            f"The operator on file is {operator}. It's about {distance(r['miles_from_yard_our_read'])} from your "
            f"{yard} yard, and {('an' if kind[0] in 'aeiou' else 'a')} {kind} site like this is the kind of job "
            f"your {r['fit_phrase_our_read']} serve; that's our read, not the filing.\n\n"
            "We're a research service with no connection to the project: each week we pull new construction "
            f"sites from state records and match them to haulers by service area. {price}\n\n"
            "Want the free five-site sample?\n\n"
            f"{signature}\n\n{footer}"
        )
        out.append(f"\n## {n}. {r['batch']}: {company}\n")
        out.append(f"- To: {r['email']} ({r['email_confidence']})\n- Subject: {site}, {street}\n"
                   f"- Site record: {r['site_source_url']}\n- Hauler publishes: {r['services_published']}\n")
        out.append("\n```\n" + body + "\n```\n")
    text = "".join(out)
    if "—" in text:
        raise SystemExit("em dash found; fix before writing")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    open(args.out, "w").write(text)
    print(f"{len(rows)} S1 drafts -> {args.out}")


if __name__ == "__main__":
    main()
