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
from urllib.parse import urlsplit

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
            rows.append({**r, "email": (r.get("email") or "").strip().lower()})
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


def identities(row):
    keys = set()
    for field in ("company", "legal_name"):
        if norm(row.get(field, "")):
            keys.add(("company", norm(row[field])))
    for field in ("email", "site_emails"):
        for email in re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", row.get(field, "").lower()):
            keys.add(("email", email))
            host = domain(email)
            if host and not FREE_MAIL.match(host):
                keys.add(("domain", host.removeprefix("www.")))
    for field in ("domain", "website", "website_url"):
        value = row.get(field, "").strip().lower()
        if value:
            host = urlsplit(value if "://" in value else "https://" + value).hostname
            if host:
                keys.add(("domain", host.removeprefix("www.")))
    return keys


def csv_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def check(packet, root=ROOT):
    with open(os.path.join(root, "ops", "rules.json"), encoding="utf-8") as handle:
        rules = json.load(handle)
    blocked = {}
    for row in csv_rows(os.path.join(root, "data", "do_not_contact.csv")):
        for key in identities(row):
            blocked[key] = "on do_not_contact.csv"
    for filename in rules.get("lists", {}).get("files", []):
        for row in csv_rows(os.path.join(root, "data", filename)):
            status = row.get("outreach_status", "").strip()
            if status != "Not contacted":
                for key in identities(row):
                    blocked.setdefault(key, f"list status is '{status or 'missing'}'")
    tracker = os.path.join(root, "Jobsite_Intelligence_Outreach_Tracker.md")
    if os.path.exists(tracker):
        with open(tracker, encoding="utf-8") as handle:
            section = handle.read().split("## Excluded", 1)
        if len(section) == 2:
            section = re.split(r"(?m)^## ", section[1])[0]
            for match in re.finditer(r"(?m)^- (.+?)(?: \(|:|$)", section):
                blocked[("company", norm(match.group(1)))] = "on the tracker's Excluded list"
    for filename in ("master_prospect_exclusions.csv", "prospect_exclusions.csv", "excluded.csv"):
        for row in csv_rows(os.path.join(root, "data", filename)):
            for key in identities(row):
                blocked[key] = "on the excluded list"
    # Carry company exclusions through known aliases and domains from the lists.
    for filename in rules.get("lists", {}).get("files", []):
        for row in csv_rows(os.path.join(root, "data", filename)):
            keys = identities(row)
            if any("Excluded" in blocked.get(key, "") or "excluded" in blocked.get(key, "") for key in keys):
                for key in keys:
                    blocked[key] = "on the excluded list"
    flags, seen_domains = [], {}
    if not packet:
        return ["No prospect rows parsed; packet was not checked"]
    for index, row in enumerate(packet, 1):
        label = f"#{index} {row.get('company', '')} <{row.get('email', '')}>"
        keys = identities(row)
        if not norm(row.get("company", "")):
            flags.append(f"{label}: missing company")
        for reason in sorted({blocked[key] for key in keys if key in blocked}):
            flags.append(f"{label}: {reason}")
        for host in sorted(value for kind, value in keys if kind == "domain"):
            if host in seen_domains:
                flags.append(f"{label}: same domain as #{seen_domains[host]}")
            else:
                seen_domains[host] = index
    return flags


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    packet = read_packet(sys.argv[1])
    flags = check(packet)
    for flag in flags:
        print(flag)
    print(f"{len(flags)} flags ({len(packet)} rows checked)")
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
