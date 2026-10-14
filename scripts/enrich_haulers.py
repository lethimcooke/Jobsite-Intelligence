#!/usr/bin/env python3
"""Find and grade roll-off and portable toilet haulers for one metro.

1. FMCSA Company Census (data.transportation.gov az4n-8mr2): active carriers in the metro's
   counties that haul garbage/refuse (`crgo_garbage = X`), with a hauler-like name. This
   gives the legal name, yard address, fleet size (power units) and the email the carrier
   filed with FMCSA.
2. The hauler's own website (the domain of its FMCSA email, when it isn't a free-mail
   address): published services (roll-off, portable toilets, construction, commercial,
   container sizes), service areas and published emails.

National haulers, franchises and fleets over 60 power units are skipped: the buyer is the
independent, owner-run hauler.

Email grades (same as ASI): A = published on the hauler's own site; B-dir = filed with FMCSA
on the hauler's own business domain. Free-mail-only carriers are kept but marked
`needs email pass`.

Usage:
    python3 enrich_haulers.py --metro Houston --out haulers_houston_enriched.csv
"""
import argparse
import concurrent.futures as cf
import csv
import html
import json
import re
import sys
import urllib.parse
import urllib.request

from metros import METROS

FMCSA = "https://data.transportation.gov/resource/az4n-8mr2.json"
FREE_MAIL = re.compile(r"@(gmail|yahoo|ymail|hotmail|outlook|aol|att|comcast|icloud|live|msn|sbcglobal)\.", re.I)
FIT = re.compile(r"ROLL ?-?OFF|DUMPSTER|DISPOSAL|WASTE|PORTABLE|PORTA|SANITATION|RESTROOM|CONTAINER|SITE SERVICE", re.I)
NATIONAL_NAMES = re.compile(
    r"WASTE MANAGEMENT|REPUBLIC|WASTE CONNECTIONS|GFL|\bBFI\b|FRONTIER|WASTE PRO|ALLIED|"
    r"FCC ENVIRONMENTAL|BIN THERE|BUDGET DUMPSTER|UNITED SITE|REDBOX|JUNK KING|GOT[- ]JUNK",
    re.I,
)
NATIONAL_DOMAINS = re.compile(
    r"wasteconnections|fccenvironmental|republicservices|wm\.com|gflenv|bintheredumpthat|redboxplus|arcosa|enais",
    re.I,
)
MAX_POWER_UNITS = 60
SERVICES = {
    "roll-off": r"roll[- ]?off|dumpster",
    "construction": r"construction",
    "commercial": r"commercial",
    "portable toilets": r"portable (toilet|restroom)|porta[- ]?(potty|john)",
    "restroom trailers": r"restroom trailer",
    "hand-wash": r"hand[- ]?wash",
    "washout": r"washout",
    "demolition": r"demolition",
    "compactors": r"compactor",
    "residential": r"residential",
    "10-yd": r"\b10[- ]?(yd|yard)",
    "15-yd": r"\b15[- ]?(yd|yard)",
    "20-yd": r"\b20[- ]?(yd|yard)",
    "30-yd": r"\b30[- ]?(yd|yard)",
    "40-yd": r"\b40[- ]?(yd|yard)",
}
AREAS = [
    "houston", "katy", "cypress", "spring", "tomball", "humble", "kingwood", "pasadena", "pearland",
    "sugar land", "richmond", "rosenberg", "conroe", "the woodlands", "baytown", "league city",
    "friendswood", "missouri city", "fulshear", "magnolia", "alvin", "galveston", "montgomery",
    "porter", "crosby", "la porte", "channelview", "webster", "stafford", "jersey village", "waller",
    "hockley", "brookshire", "fort bend", "harris county", "montgomery county", "brazoria",
    "deer park", "dickinson", "texas city", "austin", "round rock", "georgetown", "cedar park",
    "pflugerville", "san marcos", "kyle", "buda", "dallas", "fort worth", "plano", "arlington",
    "san antonio", "new braunfels",
]
SKIP_EMAIL = re.compile(r"\.(png|jpe?g|gif|webp|svg|js)$|sentry|wixpress|example|godaddy|preact", re.I)


def page_text(url, reader=False):
    """Visible text of a page. With reader=True, uses the r.jina.ai reader for script-built sites."""
    try:
        target = ("https://r.jina.ai/" + url) if reader else url
        req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=45).read(600000).decode("utf-8", "ignore")
    except Exception:
        return ""
    if not reader:
        raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
        raw = re.sub(r"<[^>]+>", " ", raw)
    return " ".join(html.unescape(raw).split())


def scan_site(c):
    text = ""
    for path in ["", "/contact", "/contact-us", "/services", "/service-area", "/about", "/about-us"]:
        text += " " + (page_text(f"https://{c['domain']}{path}") or page_text(f"http://{c['domain']}{path}"))
    if len(text.strip()) < 1500:
        text += " " + page_text(f"https://{c['domain']}", reader=True)
    low = text.lower()
    emails = sorted({m.lower() for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", text)
                     if not SKIP_EMAIL.search(m) and m.lower().endswith("@" + c["domain"])})
    c["site_text_chars"] = len(text.strip())
    c["services_published"] = ", ".join(k for k, v in SERVICES.items() if re.search(v, low))
    c["areas_published"] = ", ".join(a for a in AREAS if a in low)
    c["site_emails"] = ", ".join(emails)
    return c


def grade(c):
    generic = [e for e in c["site_emails"].split(", ") if e and re.match(r"(info|sales|service|services|office|dispatch|contact|admin|customerservice|support)@", e)]
    if generic:
        c["email"], c["email_confidence"] = generic[0], "A"
    elif c["site_emails"]:
        c["email"], c["email_confidence"] = c["site_emails"].split(", ")[0], "A"
    elif c["domain"] and c["fmcsa_email"]:
        c["email"], c["email_confidence"] = c["fmcsa_email"].lower(), "B-dir"
    else:
        c["email"], c["email_confidence"] = "", "needs email pass"
    svc = c["services_published"]
    c["fit"] = ("roll-off" in svc or "portable toilets" in svc) and ("construction" in svc or "commercial" in svc)
    return c


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--metro", required=True, choices=sorted(METROS))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    fips = ",".join("'%s'" % f for f in METROS[args.metro]["fips"])
    params = {
        "$select": "dot_number,legal_name,dba_name,phy_street,phy_city,phy_zip,phone,email_address,power_units,mcs150_date",
        "$where": f"phy_state='TX' AND status_code='A' AND crgo_garbage='X' AND phy_cnty in({fips})",
        "$limit": 20000,
    }
    with urllib.request.urlopen(FMCSA + "?" + urllib.parse.urlencode(params), timeout=180) as resp:
        carriers = json.load(resp)

    cands = {}
    for r in carriers:
        name = f"{r.get('legal_name') or ''} {r.get('dba_name') or ''}"
        email = (r.get("email_address") or "").strip()
        units = int(r.get("power_units") or 0)
        if not FIT.search(name) or NATIONAL_NAMES.search(name) or NATIONAL_DOMAINS.search(email) or units > MAX_POWER_UNITS:
            continue
        domain = "" if (not email or FREE_MAIL.search(email)) else email.split("@")[1].lower()
        key = domain or name
        if key in cands:
            continue
        cands[key] = {
            "company": (r.get("dba_name") or r.get("legal_name") or "").strip(),
            "legal_name": r.get("legal_name", ""),
            "usdot": r["dot_number"],
            "power_units": units,
            "yard_address": f"{r.get('phy_street', '').strip()}, {r.get('phy_city', '').strip()}, TX {r.get('phy_zip', '')[:5]}",
            "phone": r.get("phone", ""),
            "fmcsa_email": email,
            "domain": domain,
            "fmcsa_updated": (r.get("mcs150_date") or "")[:10],
            "metro": args.metro,
        }

    with_site = [c for c in cands.values() if c["domain"]]
    with cf.ThreadPoolExecutor(12) as ex:
        scanned = list(ex.map(scan_site, with_site))
    for c in cands.values():
        if not c["domain"]:
            c.update(site_text_chars=0, services_published="", areas_published="", site_emails="")
    rows = [grade(c) for c in scanned + [c for c in cands.values() if not c["domain"]]]
    rows.sort(key=lambda c: (not c["fit"], c["email_confidence"] != "A", -c["power_units"]))
    for c in rows:
        c.update(outreach_status="Not contacted", notes="")

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    fit = sum(1 for c in rows if c["fit"])
    print(f"{args.metro}: {len(carriers)} FMCSA refuse carriers, {len(rows)} hauler candidates, "
          f"{len(with_site)} with a business website, {fit} publishing roll-off or toilets plus "
          f"construction or commercial work -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
