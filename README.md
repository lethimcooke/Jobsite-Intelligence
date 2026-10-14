# Jobsite Intelligence: launch framework

Working name for Asterfield's second business: new construction sites from TCEQ stormwater
records, sold as research to independent roll-off and portable toilet haulers. Free five-site
sample, then a one-time $500 30-day pilot for 15–20 verified projects. Same engine, agent
roles, guardrails and deliverability rules as Austin Signage Intelligence (ASI).

Why this idea: `docs/Business_Selection_Research.md`
(Addendum 2 has the final ranking).

## What's in this folder

| File | What it is | State |
|---|---|---|
| `scripts/pull_noi_sites.py` | Pulls new TXR15 construction sites for a metro from TCEQ's Central Registry (daily, free), one row per site, drops individual-owned operators, flags person-like site names, ranks by project type (our read) | Tested live Oct 14: Austin 37 sites / 14 days, Houston 57 |
| `scripts/pull_haulers.py` | Starting hauler list from Comptroller sales-tax permits (NAICS 562111, 562119, 562991), skipping governments, individuals and nationals | Tested live Oct 14: Austin 134 candidates, 40 with fitting names |
| `scripts/metros.py` | County lists, Comptroller county codes and FMCSA county FIPS for Austin, Houston, DFW, San Antonio | Codes checked against live rows |
| `scripts/enrich_haulers.py` | FMCSA refuse carriers in the metro, joined to each hauler's own website: services, areas, published emails, grade | Tested live Oct 14: Houston 273 candidates, 22 fits |
| `scripts/build_packet.py` | Geocodes sites and yards (US Census), pairs each hauler with the nearest usable site, one site per batch | Tested live Oct 14 |
| `scripts/write_s1.py`, `scripts/check_copy.py` | S1 drafts from a packet; pre-check against `ops/rules.json` | Tested Oct 14: 19 bodies PASS |
| `ops/rules.json` | Validator rules in ASI's schema: senders, signature, exact price line, footer, banned claims for this market | Sender set to `sites@` |
| `docs/Outreach_Copy_v1.md` | S1, S2, S5, E1, E3 adapted from ASI's copy v2 | Draft; passes its own banned-phrase check |

Run from the repo root (Python 3, standard library only). Scratch output goes to the session
scratchpad; lists and packets that are used for sending are committed under `data/` and `outreach/`.
```
python3 scripts/pull_noi_sites.py  --metro Houston --days 21 --out <scratch>/sites.csv
python3 scripts/enrich_haulers.py  --metro Houston --out data/hauler_list_houston.csv
python3 scripts/build_packet.py    --sites <scratch>/sites.csv --haulers data/hauler_list_houston.csv \
    --batch-prefix H --count 20 --out-csv data/packet_H1-H2.csv --out-md outreach/H1-H2_Hook_Packet.md \
    [--allow-rn <reviewed flagged sites>] [--skip-rn <sites>] [--skip-company <haulers>]
python3 scripts/write_s1.py        --packet data/packet_H1-H2.csv --metro Houston --out outreach/H1-H2_S1_Copy.md \
    --site-type RN=industrial ... --name "Recased=Correct" ...
python3 scripts/check_copy.py      outreach/H1-H2_S1_Copy.md --metro Houston --stage S1 --dnc <ASI do_not_contact.csv>
```
`pull_haulers.py` (Comptroller sales-tax list) is kept as a cross-check; `enrich_haulers.py`
(FMCSA refuse carriers plus each hauler's own website) is the main prospect source, because it
gives a fleet size, a yard address and an email.

## Current state (October 14, 2026)

- `outreach/H1-H2_Hook_Packet.md` and `outreach/H1-H2_S1_Copy.md`: **19 Houston haulers**, each
  paired with the nearest commercial or industrial site (1 to 19 miles, our read), split into
  H1 (10) and H2 (9). Copy passes `check_copy.py`; no hauler is in ASI's lists or do-not-contact
  file, and no site is in an ASI packet, sample or named-project file.
- Email grades: 9 A (published on the hauler's own site), 10 B-dir (filed with FMCSA on the
  hauler's own domain).
- Removed by hand: DC Ex Dumpsters (FMCSA email on an unrelated aviation domain), LM Waste
  Solutions (email on a scrap-metal yard's site), Redbox+ (national franchise). Control Waste
  Services is a fit but its yard address didn't geocode; add it by hand if a 20th is wanted.
- Not drafted and not sent. The two open items below come first.

## Phase 0: decisions

**Made (user, October 14, 2026):**
- Pace: no separate first-email cap. First emails always go first; follow-ups wait when the shared
  60-a-day mailbox total is full.
- Name: "[City] Jobsite Intelligence", sent from `sites@asterfieldgroup.com` for every metro.
- First metro: **Houston** (84 new sites and 70 fitting haulers in three weeks, vs Austin's 56 and 40).
- Launch: start slowly with the 20-email test.

**Still open, and they block sending:**
1. **Mailing address for the footer.** CAN-SPAM requires a physical postal address in commercial
   email (a PO box or virtual mailbox works). ASI's footer is missing it too.
2. **The `sites@` alias.** Add it in Google Workspace (Admin console, the user, Alternate email)
   and as a "Send mail as" address in Gmail, like `fieldwork@`.


## Phase 1: build the first test batch (about 2 working days)

| Step | Role | Output |
|---|---|---|
| 1. Pull sites (last 14 days) and haulers for the metro | Prospector | `sites_<metro>.csv`, `haulers_<metro>.csv` |
| 2. Review sites: keep commercial, industrial, institutional and amenity sites with a business operator; reject person-like names; re-check each record's source URL | Prospector | 10–15 usable sites |
| 3. Hauler pass on the "name fits" rows: own website (services, container sizes, construction or commercial work, yard location), then the email (own site, then FMCSA, then Facebook), grade A/B/B-dir as in ASI | Prospector | 20 haulers with an email and a published service line |
| 4. Conflict check: each hauler against ASI's master list, trade list and do-not-contact file; each site's address and RN against ASI's hook packets and samples | Operations | Pass/fail per row |
| 5. Hook packet: one site per hauler, nearest commercial site to its yard, distance computed from the yard address | Prospector | `outreach/JSI_Batch_T1_Hook_Packet.md` |
| 6. S1 copy from `docs/Outreach_Copy_v1.md`, Tier B only | Copywriter | `outreach/JSI_T1_S1_Copy.md` |
| 7. Validate against `ops/rules.json`, draft, the user sends, log | Operations | Same daily loop as ASI (`Daily_Ops_Loop.md`) |
| 8. Build two sample PDFs in advance (Austin north and south) so an E1 can go out within the hour | Report creator | Five-site samples using the columns below |

**Sample columns:** #, site name, TCEQ authorization(s), RN with source link, date on file,
location, operators on file (businesses only), operator type, related city permit if found,
project type (our read), distance from your yard (our read), likely jobsite needs (our read),
first call (operator's main business line, a routing contact, not a confirmed buyer),
suggested next step (our read), checked on.

## Phase 2: the test and the go/no-go rule

Send 20 S1s (one batch of 10 on each of two days), then S2 and S5 on the short sequence.
Measure at S5 (about three weeks):

| Result after 20 contacts | Call |
|---|---|
| 3+ replies (15%+) and at least one sample requested | **Go.** Scale to the 20-a-day pace within the shared cap, then add Houston. |
| 1–2 replies (5–10%) | **Iterate once.** Change one thing (subject line, or site type), send 20 more. |
| 0 replies | **Stop.** The Tier B gap is real for this buyer; don't scale. |

The real test is payment, not replies. If samples go out and nobody buys after E3, that is the
same wall as ASI, and the problem is the offer, not the market. Tell the user before building
more.

## Rules that carry over unchanged

Nothing is sent except by the user. No em dashes. Business names only, never a person. No
calls offered. Every claim cites a public record, and our read is labeled as our read. Each
city sends from its own alias with the full three-line signature. Opt-out footer on every cold
email; opt-outs honored the same day. Pause on more than 3% bounces or any spam complaint. One
company, one sequence across both businesses.

## Known gaps

- The project-type sort is a name-based first pass. It misreads some sites (for example "Kyle
  Park" is a commercial park, not an amenity), so a person reviews every row.
- No hauler appears in any public site-level record, so the S1 is always Tier B. This is the
  main thing the test measures.
- The site-level job value isn't sourced. Haul prices of $285–850 are background only; the E3
  says "a single site covers it many times over" until a range is sourced.
- ASI's `scripts/asi_ops.py` lives in the Austin-Signage repo, not here. To validate these
  drafts, run it there with this folder's `ops/rules.json`, or copy the rules into that repo.
