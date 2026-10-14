#!/usr/bin/env python3
"""Check a copy file's email bodies against ops/rules.json before anything is drafted.

Checks every fenced body: exact standard price line once (S1), full signature for the metro,
opt-out footer, banned phrases, em dashes, and the do-not-contact file if one is given.
This is a pre-check; ASI's asi_ops.py validator remains the gate before drafts.

Usage:
    python3 check_copy.py outreach/H1-H2_S1_Copy.md --metro Houston --stage S1 [--dnc path/to/do_not_contact.csv]
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("copy_file")
    ap.add_argument("--metro", required=True)
    ap.add_argument("--stage", default="S1")
    ap.add_argument("--dnc", help="do-not-contact CSV (any file of emails/domains/names)")
    args = ap.parse_args()

    rules = json.load(open(os.path.join(HERE, "..", "ops", "rules.json")))
    text = open(args.copy_file).read()
    bodies = re.findall(r"```\n(.*?)```", text, re.S)
    recipients = re.findall(r"^- To: (\S+)", text, re.M)
    signature = rules["signature_template"].format(**rules["senders"][args.metro])
    dnc = open(args.dnc).read().lower() if args.dnc else ""

    problems = []
    for i, body in enumerate(bodies):
        low = body.lower()
        where = f"body {i + 1}" + (f" ({recipients[i]})" if i < len(recipients) else "")
        if args.stage == "S1" and body.count(rules["standard_price_line"]) != 1:
            problems.append(f"{where}: standard price line must appear exactly once")
        if signature not in body:
            problems.append(f"{where}: full signature for {args.metro} missing")
        if args.stage in rules["footer"]["stages"] and rules["footer"]["text"] not in body:
            problems.append(f"{where}: opt-out footer missing")
        for phrase in rules["banned_phrases"]:
            if phrase in low:
                problems.append(f"{where}: banned phrase '{phrase}'")
        if "—" in body:
            problems.append(f"{where}: em dash")
        if i < len(recipients) and dnc:
            email = recipients[i].lower()
            if email in dnc or email.split("@")[1] in dnc:
                problems.append(f"{where}: recipient is on the do-not-contact file")
    if len(recipients) != len(bodies):
        problems.append(f"{len(bodies)} bodies but {len(recipients)} recipients")
    if len(set(recipients)) != len(recipients):
        problems.append("duplicate recipient in file")

    if problems:
        print("FAIL")
        print("\n".join(problems))
        sys.exit(1)
    print(f"PASS: {len(bodies)} bodies checked against ops/rules.json ({args.metro}, {args.stage})")


if __name__ == "__main__":
    main()
