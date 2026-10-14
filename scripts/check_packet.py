#!/usr/bin/env python3
"""Check a new prospect packet before any copy is written (Jobsite's check_duplicates.py).

Reads either a packet CSV (columns `company` and `email`, e.g. build_packet.py output) or a copy /
hook-packet markdown file (`## N. ...: Company` sections with a `- To:` line). Flags any row whose
company, email or domain:
  - is on data/do_not_contact.csv;
  - has a list status other than "Not contacted" in the hauler lists named in ops/rules.json;
  - repeats another row's domain within the packet;
  - is on the tracker's Excluded list.
Prints one line per flag and "N flags". Exit code 1 when anything is flagged.

Usage:
    python3 scripts/check_packet.py data/packet_H3.csv
    python3 scripts/check_packet.py outreach/H3_S1_Copy.md
"""
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FREE_MAIL = re.compile(r"^(gmail|yahoo|ymail|hotmail|outlook|aol|att|comcast|icloud|live|msn|sbcglobal)\.", re.I)
LEGAL = re.compile(r"\b(LLC|L L C|INC|LTD|LP|LLP|CO|CORP|COMPANY|THE)\b")


def norm(name):
    name = re.sub(r"\(.*?\)", " ", (name or "").upper())
    name = re.sub(r"[^A-Z0-9 ]", " ", name)
    return " ".join(LEGAL.sub(" ", name).split())


def domain(email):
    return email.split("@", 1)[1].lower() if "@" in (email or "") else ""


def read_packet(path):
    rows = []
    if path.endswith(".csv"):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            rows.append({"company": r.get("company", ""), "email": (r.get("email") or "").strip().lower()})
        return rows
    text = open(path, encoding="utf-8").read()
    for sec in re.split(r"(?m)^## ", text)[1:]:
        head = sec.splitlines()[0]
        if "SKIP" in head.upper():
            continue
        title = re.sub(r"^\d+\.\s*", "", head)
        title = re.sub(r"^[A-Z0-9]+:\s*", "", title)
        to = re.search(r"(?m)^- To:\s*([^\s(]+)", sec)
        if to:
            rows.append({"company": title.strip(), "email": to.group(1).lower()})
    return rows


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rules = json.load(open(os.path.join(ROOT, "ops", "rules.json")))
    packet = read_packet(sys.argv[1])

    dnc_text = ""
    dnc_path = os.path.join(ROOT, "data", "do_not_contact.csv")
    if os.path.exists(dnc_path):
        dnc_text = open(dnc_path, encoding="utf-8").read().lower()

    status = {}
    for f in rules.get("lists", {}).get("files", []):
        p = os.path.join(ROOT, "data", f)
        if not os.path.exists(p):
            continue
        for r in csv.DictReader(open(p, encoding="utf-8")):
            st = (r.get("outreach_status") or "").strip()
            for key in (r.get("email", "").lower(), norm(r.get("company", "")), norm(r.get("legal_name", ""))):
                if key:
                    status[key] = st

    excluded = set()
    tracker = os.path.join(ROOT, "Jobsite_Intelligence_Outreach_Tracker.md")
    if os.path.exists(tracker):
        part = open(tracker, encoding="utf-8").read().split("## Excluded", 1)
        if len(part) == 2:
            for m in re.finditer(r"(?m)^- (.+?) \(", part[1]):
                excluded.add(norm(m.group(1)))

    flags = []
    seen_domains = {}
    for i, r in enumerate(packet, 1):
        label = f"#{i} {r['company']} <{r['email']}>"
        dom = domain(r["email"])
        if r["email"] and r["email"] in dnc_text:
            flags.append(f"{label}: email is on do_not_contact.csv")
        elif dom and not FREE_MAIL.match(dom) and dom in dnc_text:
            flags.append(f"{label}: domain {dom} is on do_not_contact.csv")
        if norm(r["company"]) and norm(r["company"]).lower() in dnc_text:
            flags.append(f"{label}: company is on do_not_contact.csv")
        st = status.get(r["email"]) or status.get(norm(r["company"]))
        if st and st != "Not contacted":
            flags.append(f"{label}: list status is '{st}'")
        if dom and not FREE_MAIL.match(dom):
            if dom in seen_domains:
                flags.append(f"{label}: same domain as #{seen_domains[dom]}")
            else:
                seen_domains[dom] = i
        if norm(r["company"]) in excluded:
            flags.append(f"{label}: on the tracker's Excluded list")

    for f in flags:
        print(f)
    print(f"{len(flags)} flags ({len(packet)} rows checked)")
    sys.exit(1 if flags else 0)


if __name__ == "__main__":
    main()
