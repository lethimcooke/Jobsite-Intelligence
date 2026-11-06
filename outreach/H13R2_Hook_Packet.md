# Hook packet: batch H13R2 (Houston reserves, 45-day sites)

**Prepared:** November 6, 2026, by Claude (prospector role) at operations' request, after the user approved a 45-day site window (relayed by operations, Nov 6). It pairs four of the H13R haulers that were waiting for a site (PR #27 adds their rows to `data/hauler_list_houston.csv`). The addresses are already verified (MillionVerifier ok) and were rechecked on each hauler's own live page on Nov 6, so no verification CSV is needed. Prospecting only.

**Sites:** taken from `pull_noi_sites.py --metro Houston --days 45` (Nov 6) and re-fetched live at 20:28 UTC. All four are ACTIVE, priority 1, and not in any packet. KAJIMA CONSTRUCTION YOKOGAWA PARK was dropped because its TXR15 is CANCELLED, so FULSHEAR LAKES LAKESIDE PARK SECTION 6 replaces it for K&K. Tru-Tex Sanitation stays unpaired until a site appears in its Baytown-east area. Area matches are our read. No claim that work has started, a vendor is unselected, or work is open for bid.

| # | Batch | Hauler | Email (grade) | Service reference | Publishes | Site | TCEQ auth / date on file / RN | Business affiliation on file | Miles |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H13R2 | K&K Dumpster Rentals | 002kevinrodriguez@gmail.com (A) | Fulshear (service reference) | 10-, 15-, 20-, 25-, 30- and 40-yard dumpster rentals | FULSHEAR LAKES LAKESIDE PARK SECTION 6, APPROX. 200 YDS W OF RIVER BLUET PL & BLUE DASHER PK PL, FULSHEAR, TX | TXR1532ZN / 2026-09-23 / RN112535117 | BEYER CONSTRUCTION LLC | unverified |
| 2 | H13R2 | Texas Lux Restroom Trailers | contact@texasluxrestroomtrailers.com (A) | Houston (service reference) | restroom trailers | CALLISTO II ENERGY CENTER, 12302 HIRAM CLARKE RD, HOUSTON, TX | TXR1582XB / 2026-09-28 / RN112358486 | CALLISTO II ENERGY CENTER LLC | unverified |
| 3 | H13R2 | Trailer Ready Rentals LLC | trailerreadyrentals@gmail.com (A) | Houston (service reference) | restroom trailers | IAH COMMERCE PARK, APPROX. 0.30 MI E OF FM 1960 RD & FOXWOOD FOREST BLVD, HARRIS COUNTY, TX | TXR1553ZO / 2026-09-28 / RN112537824 | ROACH & PADUA REALTY 1960 JV LLC | unverified |
| 4 | H13R2 | Container Source Inc. | office@containersourceinc.com (A) | Waller (service reference) | roll-off dumpster rentals | KATY PARK NWC, W SIDE OF KATY HOCKLEY CUT OFF RD, N OF MORTON RD, HARRIS COUNTY, TX | TXR1558ZN / 2026-09-24 / RN112535778 | JOERIS GENERAL CONTRACTORS LLC | unverified |

## Sources and verification

## 1. H13R2: K&K Dumpster Rentals
- To: 002kevinrodriguez@gmail.com
- Email grade: A, exact address on own live page.
- Website: https://kkdumpsters.com/
- Email evidence and MX: Own page https://www.kkdumpsters.com/ HTTP 200 rechecked 2026-11-06T20:12:09.249367+00:00 (rendered in Chromium (JS page)). MX: 5 gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com.; 10 alt1.gmail-smtp-in.l.google.com..
- Fit: 10-, 15-, 20-, 25-, 30- and 40-yard dumpster rentals; commercial and construction. Published area: Houston and surrounding areas.
- Site: FULSHEAR LAKES LAKESIDE PARK SECTION 6, APPROX. 200 YDS W OF RIVER BLUET PL & BLUE DASHER PK PL, FULSHEAR, TX, FORT BEND County.
- TCEQ: TXR1532ZN; RN112535117; ACTIVE; affiliation date 2026-09-23; priority 1 (amenity / recreation, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112535117&program_code=STORM; fetched 2026-11-06T20:28Z.
- Area match: Published Houston and surrounding areas; site in FORT BEND County (Fulshear, our read from the development name). Park amenity within a master-planned community; 44 days old. Area/trade match is our read; dispatch acceptance unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified. Site is inside the 45-day window approved Nov 6 (relayed by operations).

## 2. H13R2: Texas Lux Restroom Trailers
- To: contact@texasluxrestroomtrailers.com
- Email grade: A, exact address on own live page.
- Website: https://texasluxrestrooms.com/
- Email evidence and MX: Own page https://texasluxrestrooms.com/contact/ HTTP 200 rechecked 2026-11-06T20:12:10.096972+00:00 (direct fetch). MX: 10 alt3.aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.; 1 aspmx.l.google.com..
- Fit: restroom trailers; industrial turnarounds; construction and emergency rentals. Published area: Houston and Gulf Coast.
- Site: CALLISTO II ENERGY CENTER, 12302 HIRAM CLARKE RD, HOUSTON, TX, HARRIS County.
- TCEQ: TXR1582XB; RN112358486; ACTIVE; affiliation date 2026-09-28; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112358486&program_code=STORM; fetched 2026-11-06T20:28Z.
- Area match: Published Houston and Gulf Coast, industrial and construction rentals; site in HOUSTON, HARRIS County. EPC SERVICES COMPANY also on file since 2026-01-22; Sep 28 is the newer business affiliation. Area/trade match is our read; dispatch acceptance unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified. Site is inside the 45-day window approved Nov 6 (relayed by operations).

## 3. H13R2: Trailer Ready Rentals LLC
- To: trailerreadyrentals@gmail.com
- Email grade: A, exact address on own live page.
- Website: https://trailerreadyrentals.com/
- Email evidence and MX: Own page https://trailerreadyrentals.com/ HTTP 200 rechecked 2026-11-06T20:12:03.621533+00:00 (rendered in Chromium (JS page)). MX: 5 gmail-smtp-in.l.google.com.; 10 alt1.gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com..
- Fit: restroom trailers; construction sites; corporate temporary facilities. Published area: Houston; Willis business reference.
- Site: IAH COMMERCE PARK, APPROX. 0.30 MI E OF FM 1960 RD & FOXWOOD FOREST BLVD, HARRIS COUNTY, TX, HARRIS County.
- TCEQ: TXR1553ZO; RN112537824; ACTIVE; affiliation date 2026-09-28; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112537824&program_code=STORM; fetched 2026-11-06T20:28Z.
- Area match: Published Houston, Willis business reference; site in north HARRIS County near IAH (city not on record, not asserted). Script typed it amenity; name reads commercial. Area/trade match is our read; dispatch acceptance unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified. Site is inside the 45-day window approved Nov 6 (relayed by operations).

## 4. H13R2: Container Source Inc.
- To: office@containersourceinc.com
- Email grade: A, exact address on own live page.
- Website: https://containersourceinc.com/
- Email evidence and MX: Own page https://containersourceinc.com/contact/ HTTP 200 rechecked 2026-11-06T20:11:49.560578+00:00 (direct fetch). MX: 0 containersourceinc-com.mail.protection.outlook.com..
- Fit: roll-off dumpster rentals; shipping containers. Published area: Magnolia, Tomball, Hempstead, Waller.
- Site: KATY PARK NWC, W SIDE OF KATY HOCKLEY CUT OFF RD, N OF MORTON RD, HARRIS COUNTY, TX, HARRIS County.
- TCEQ: TXR1558ZN; RN112535778; ACTIVE; affiliation date 2026-09-24; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112535778&program_code=STORM; fetched 2026-11-06T20:28Z.
- Area match: Published areas (per Codex reserve) Magnolia, Tomball, Hempstead, Waller, plus the Houston corridor; site in west HARRIS County near Katy and Waller County (our read; city not on record). Brenham base. Script typed it amenity; name and operator read commercial. Area/trade match is our read; dispatch acceptance unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified. Site is inside the 45-day window approved Nov 6 (relayed by operations).
