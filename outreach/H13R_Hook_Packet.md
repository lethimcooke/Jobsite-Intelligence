# Hook packet: batch H13R (Houston reserves)

**Prepared:** November 6, 2026, by Claude (prospector role) at operations' request. Source: Codex's 13 Houston refresh reserves (`data/houston_refresh_reserves_2026-11-06.csv` on codex/houston-h13, PR #20). Operations sent the 9 that MillionVerifier returned `ok`. Prospecting only. No copy, Gmail, ledger or tracker changes.

**Result:** 3 rows paired now. 5 are fit-checked and added to `data/hauler_list_houston.csv` as Not contacted, but no compliant site in their area was available (see Waiting for a site). 1 is held for recheck.

**Email:** each address was rechecked on the hauler's own live page on Nov 6 (direct fetch, or Chromium for JS-only sites) and MX was looked up the same run. Own-site free-mail is graded A, as in H3 to H13. All 9 already passed MillionVerifier, so no new verification CSV is needed. Forwarder MX: none (Microsoft 365, Google Workspace, Gmail and iCloud only).

**Sites:** `pull_noi_sites.py --metro Houston --days 30` (Nov 6, 82 sites since Oct 7), then each RN was fetched live. Excluded from the 24 unused priority 1-2 candidates:
- Master-planned residential communities: 7 SEKISUI HOUSE COMMUNITIES records plus WESTRIDGE COVE.
- Road, flood-control, waterline, dredging and WWTP utility work: WWTP FOR MC MUD NO 173 is a wastewater plant.
- Person-named sites: JOHN SHARP DRIVE, FRANKYS SAND PIT, KINGHAM DALTON AKER KVAERNER, ROSA ALLEN, and RIVER PARK RANCH (an individual operator).
- TEXAS PETROLEUM GROUP: the record address is an office suite.
- QSL TEXAS TERMINALS: its TXR15 authorization is CANCELLED on the live record.

No RN is in any `data/packet_*.csv` or on the H13 branch.

**Limits:** date on file is the affiliation-begin date. No claim that work has started, a vendor is unselected, or work is open for bid. Area matches are our read; distance and dispatch acceptance are unverified.

| # | Batch | Hauler | Email (grade) | Service reference | Publishes | Site | TCEQ auth / date on file / RN | Business affiliation on file | Miles |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H13R | Mid-Tex Environmental Services LLC | midtexenvironmental@gmail.com (A) | Cypress (service reference) | roll-off dumpsters | CYPRESS FIELDS BUSINESS PARK, 15101 CYPRESS FIELDS AVE, CYPRESS, TX | TXR1594ZB / 2026-11-05 / RN112504477 | CYPRESS FIELDS BUSINESS PARK LLC | unverified |
| 2 | H13R | La Dompe LLC | selvin.turcios@ladompellc.com (A) | North Houston (service reference) | roll-off dumpsters | NORTH HOUSTON COMMERCE PARK, E SIDE OF ALDINE WESTFIELD RD, BETWEEN WOODCREEK LN & W W THORNE DR, HOUSTON, TX | TXR1549ZS / 2026-10-13 / RN112547120 | SLATE CONSTRUCTION LLC | unverified |
| 3 | H13R | Frontier Site Services | sales@frontiersiteservices.com (A) | Houston (service reference) | porta potties | 608 W DONOVAN, 608 W DONOVAN ST, HOUSTON, TX | TXR1599ZS / 2026-10-14 / RN112092143 | RIVERWAY BUILDERS LLC | unverified |

## Sources and verification

## 1. H13R: Mid-Tex Environmental Services LLC
- To: midtexenvironmental@gmail.com
- Email grade: A, exact address on own live page.
- Website: https://midtexenvironmental.com/
- Email evidence: https://midtexenvironmental.com/contact-us/; HTTP 200 fetched 2026-11-06T20:12:10.688006+00:00 (direct fetch).
- MX: 10 alt1.gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 5 gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com..
- Fit: roll-off dumpsters; front-load dumpsters; commercial and industrial disposal. Published area: Tomball, Houston, Cypress, Magnolia, Montgomery, Waller, Prairie View, Hempstead, Spring, The Woodlands.
- Site: CYPRESS FIELDS BUSINESS PARK, 15101 CYPRESS FIELDS AVE, CYPRESS, TX, HARRIS County.
- TCEQ: TXR1594ZB; RN112504477; ACTIVE; affiliation date 2026-11-05; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112504477&program_code=STORM; fetched 2026-11-06T20:14Z.
- Notes: Site record ACTIVE on live data.texas.gov RN lookup fetched 2026-11-06T20:14Z; not in any data/packet_*.csv or the H13 branch. Published list includes Cypress; site in CYPRESS, HARRIS County. THETA GROUP CONSTRUCTION LLC also on file since 2026-08-07; the Nov 5 date is the newer business affiliation.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 2. H13R: La Dompe LLC
- To: selvin.turcios@ladompellc.com
- Email grade: A, exact address on own live page.
- Website: https://ladompellc.com/
- Email evidence: https://www.ladompellc.com/contact; HTTP 200 fetched 2026-11-06T20:11:51.740589+00:00 (direct fetch).
- MX: 0 ladompellc-com.mail.protection.outlook.com..
- Fit: roll-off dumpsters; dumpster trailers; construction debris removal. Published area: North Houston and Humble.
- Site: NORTH HOUSTON COMMERCE PARK, E SIDE OF ALDINE WESTFIELD RD, BETWEEN WOODCREEK LN & W W THORNE DR, HOUSTON, TX, HARRIS County.
- TCEQ: TXR1549ZS; RN112547120; ACTIVE; affiliation date 2026-10-13; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112547120&program_code=STORM; fetched 2026-11-06T20:14Z.
- Notes: Site record ACTIVE on live data.texas.gov RN lookup fetched 2026-11-06T20:14Z; not in any data/packet_*.csv or the H13 branch. Published North Houston and Humble; site on Aldine Westfield Rd in north Harris County (Houston, our read). Script typed it amenity; the name and operator read as commercial.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 3. H13R: Frontier Site Services
- To: sales@frontiersiteservices.com
- Email grade: A, exact address on own live page.
- Website: https://frontiersiteservices.com/
- Email evidence: https://frontiersiteservices.com/contact-us/; HTTP 200 fetched 2026-11-06T20:12:32.416080+00:00 (direct fetch).
- MX: 0 frontiersiteservices-com.mail.protection.outlook.com..
- Fit: porta potties; restroom trailers; temporary site infrastructure; construction and industrial rentals. Published area: Houston Texas location and Tulsa Oklahoma location.
- Site: 608 W DONOVAN, 608 W DONOVAN ST, HOUSTON, TX, HARRIS County.
- TCEQ: TXR1599ZS; RN112092143; ACTIVE; affiliation date 2026-10-14; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112092143&program_code=STORM; fetched 2026-11-06T20:14Z.
- Notes: Site record ACTIVE on live data.texas.gov RN lookup fetched 2026-11-06T20:14Z; not in any data/packet_*.csv or the H13 branch. Published Houston location; site in HOUSTON, HARRIS County. Also TXR1509SX on the same RN. Site name is the street address; W DONOVAN, LLC is also on file (listed by TCEQ as individual owner type), so only the business operator is named.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## Waiting for a site (fit confirmed, address rechecked, added to the Houston list)

- Container Source Inc., office@containersourceinc.com (https://containersourceinc.com/contact/). Roll-offs plus shipping containers. Based in Brenham; Tomball is on its list. No 30-day site near Tomball.
- Tru-Tex Sanitation, caseyestes1684@icloud.com (https://trutexsanitation.com/contact/). 20- to 40-yard roll-offs; Baytown and east (Chambers, Liberty). No 30-day site in that area.
- K&K Dumpster Rentals, 002kevinrodriguez@gmail.com (https://www.kkdumpsters.com/, Chromium render). 10- to 40-yard, commercial and construction, Houston area.
- Texas Lux Restroom Trailers, contact@texasluxrestroomtrailers.com (https://texasluxrestrooms.com/contact/). Restroom trailers for construction and industrial turnarounds.
- Trailer Ready Rentals LLC, trailerreadyrentals@gmail.com (https://trailerreadyrentals.com/, Chromium render). Restroom trailers, construction sites included.

If the date window is widened to 45 days, unused business sites exist. KAJIMA CONSTRUCTION YOKOGAWA PARK (Sugar Land), IAH COMMERCE PARK (FM 1960), CALLISTO II ENERGY CENTER (Hiram Clarke Rd) and KATY PARK NWC (Katy Hockley Cut Off Rd) would cover K&K, Texas Lux, Trailer Ready and Container Source. Nothing comes close for Tru-Tex.

## Held for recheck

- Father & Son Dirt Works LLC, fathersondirtworks2@gmail.com. The address is on its own contact page (https://landclearinghoustontxcom.com/contact-us, HTTP 200 on Nov 6 after resets). Its homepage now describes land clearing, dirt leveling and brush hogging, and the roll-off page reset the connection on every try. Roll-off rental can't be confirmed today, so it isn't added.
