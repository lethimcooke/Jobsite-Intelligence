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
| `scripts/metros.py` | County lists and Comptroller county codes for Austin, Houston, DFW, San Antonio | Codes checked against outlet cities |
| `ops/rules.json` | Validator rules in ASI's schema: senders, signature, exact price line, footer, banned claims for this market | Draft; aliases are placeholders |
| `docs/Outreach_Copy_v1.md` | S1, S2, S5, E1, E3 adapted from ASI's copy v2 | Draft; passes its own banned-phrase check |

Run from this folder (Python 3, standard library only):
```
python3 scripts/pull_noi_sites.py --metro Austin --days 14 --out sites_austin.csv
python3 scripts/pull_haulers.py  --metro Austin --out haulers_austin.csv
```
Write outputs to the session scratchpad or `data/`, not next to the scripts.

## Phase 0: decisions only you can make (before anything is sent)

1. **Go or wait.** The tracker's checkpoint says revisit ASI's offer if its first 10 samples
   bring no sale. Decide whether this test runs now or after ASI's first payment.
2. **Name and sender.** Brand name (working: "[Metro] Jobsite Intelligence") and alias
   (placeholder `sites@asterfieldgroup.com`). It needs to be added as an alias in Google
   Workspace like `fieldwork@`.
3. **Volume.** The test shares ASI's mailbox cap (60 a day total, 20 first emails), unless you
   lift the "no new sending domains until the first paying client" rule. Recommended: share the
   cap, 20 test S1s in total.
4. **Metro.** Austin first (same alias pattern, same city-match rule). Houston has more
   commercial sites (28 of 57 in the last two weeks vs Austin's 10 of 37), so it's the
   alternative if Austin's hauler list runs thin.
5. **Mailing address** for the footer, the same open item as ASI.

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
