# Hook packet: batch H9

Houston-area public research, October 20, 2026 (America/New_York). Prospecting only. Raw fetch timestamps use UTC, including early October 21.

**Partial batch:** 3/15 target rows. Across H7-H10: 14 packet rows, not 60. There are 24 verified contact records in total; 10 reserves have no packet hook. Do not treat reserve rows as ready for copy. No copy, Gmail, queue, tracker or existing-status changes.

Site facts come from fresh `pull_noi_sites.py --metro Houston --days 30` output and exact live TCEQ RN/authorization rechecks. Every selected authorization was ACTIVE at recheck, with a business affiliation-begin date within September 20 through October 20. **That date is the public record affiliation date, not independently verified original authorization issuance or construction start.** All sites are priority 1-2 after documented review. Some street addresses are explicit TCEQ location descriptions or supplemental TABS/facility addresses; those are identified per row, never represented as a filled TCEQ street field.

**Distance is from the labelled service-city reference, not a verified operating yard.** Matching is manual against published metro/service coverage. Numeric values are rounded straight-line miles, our read, using public ArcGIS reference points and the repo distance helper. Three site street geocodes were not strong enough; mileage is left blank on those rows. No nearest-site, driving-distance or delivery-quote claim. Exact delivery territory remains unverified.

**Email review:** 2 business-domain and 1 free-mail addresses. All are grade A, directly fetched on the own website in this session, with Cloudflare-protected addresses decoded where present and an actual non-null MX response. A business-domain contact is used when published alongside free mail. Free-mail rows retain `needs email pass`. Publication and MX do not verify individual mailbox acceptance, ownership, deliverability or consent.

**No reuse:** companies, legal aliases available from public matches, all email columns and website/email domains were screened against the master, DNC and H1-H6. Published phones were additionally screened. A bounced domain is suppressed in full. Selected sites and authorizations appear once across H7-H10 and were not used in H1-H6. Business/site names only; no individual names used as hooks.

No claim that work started, a vendor is unselected, or work is open for bid. Current carrier status, private ownership links, fleet counts, project stage and delivery coverage need review before any later operations.

| # | Batch | Hauler | Email (grade) | Yard / service reference | Publishes | Site | TCEQ auth / record date / RN | Operator on file | Miles (city reference) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H9 | Katy Dumpster Rental Group | info@katydumpsterrentalgroup.com (A) | Katy (service reference) | roll-off containers | PINE FOREST COMMERCE CENTER, 4117 Queenston Blvd, Houston, TX | TXR1573ZM / 2026-09-22 / RN112533765 | RENDON AND ASSOCIATES LLC | Not verified |
| 2 | H9 | Trash Monkey Dumpster Rentals | trashmonkey2019@gmail.com (A; needs email pass) | Conroe (service reference) | roll-off containers | TOMBALL PINES BUSINESS PARK, 1514 S PERSIMMON ST, TOMBALL, TX | TXR1582ZR / 2026-10-09 / RN112545553 | CENTURY CONCRETE CONSTRUCTION INC | 18 |
| 3 | H9 | Old Glory Rolloff Dumpsters | shelley@oldgloryrolloffdumpsters.com (A) | Spring (service reference) | roll-off containers | TIMBERS EDGE RECREATIONAL CENTER, 21965 Woodward Blvd, Splendora, TX | TXR1517ZP / 2026-09-30 / RN112539168 | STONE CASTLE CONSTRUCTORS LLC | Not verified |

## Sources and verification

## 1. H9: Katy Dumpster Rental Group
- To: info@katydumpsterrentalgroup.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://katydumpsterrentalgroup.com/
- Email evidence: https://katydumpsterrentalgroup.com/contact.html; HTTP 200 fetched 2026-10-21T00:58:08.909044+00:00.
- MX evidence: https://dns.google/resolve?name=katydumpsterrentalgroup.com&type=MX; checked 2026-10-21T01:01:12.337672+00:00; 5 mx1.hostinger.com.; 10 mx2.hostinger.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Katy is a service-city reference, not a verified operating yard.
- Published coverage: Katy, Harris, Fort Bend and Waller counties.
- Hauler sources: https://katydumpsterrentalgroup.com/contact.html
- Hook: PINE FOREST COMMERCE CENTER, 4117 Queenston Blvd, Houston, TX; RN112533765, TXR1573ZM; affiliation record date 2026-09-22.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112533765%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:58.364091+00:00.
- Site/address review: TABS same commerce center Building 7 provides a building reference on the park at Queenston/Clay. Reference is within the named park, not a surveyed whole-site centroid; filed ZIP is not used to geocode.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:58:08.909044+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own site claims locally owned operation and calls 800 Avenue D, Katy a working yard. That yard and ownership claim were not independently reconciled; output distances deliberately use Katy city reference, not that claimed yard. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 5 mx1.hostinger.com.; 10 mx2.hostinger.com.. TABS same commerce center Building 7 provides a building reference on the park at Queenston/Clay. Reference is within the named park, not a surveyed whole-site centroid; filed ZIP is not used to geocode.
- Additional flags: Street-level site geocode unavailable; city-reference mileage blank, not guessed; Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2027002756; TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 2. H9: Trash Monkey Dumpster Rentals
- To: trashmonkey2019@gmail.com
- Email grade: A, own-site publication; needs email pass (free-mail only).
- Website: https://trashmonkey.net/
- Email evidence: http://trashmonkey.net/about-us-contact-us/; HTTP 200 fetched 2026-10-21T00:55:12.849401+00:00.
- MX evidence: https://dns.google/resolve?name=gmail.com&type=MX; checked 2026-10-21T01:01:11.852495+00:00; 5 gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com.; 10 alt1.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Conroe is a service-city reference, not a verified operating yard.
- Published coverage: Houston, Magnolia, Tomball, Spring, Cypress, The Woodlands, Montgomery, Conroe, Pinehurst, Katy, Fulshear and Cinco Ranch.
- Hauler sources: http://trashmonkey.net/about-us-contact-us/; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Montgomery%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=The+Woodlands%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Kingwood%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Magnolia%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Tomball%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Cypress%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Spring%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Humble%2C+TX; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Conroe%2C+TX
- Hook: TOMBALL PINES BUSINESS PARK, 1514 S PERSIMMON ST, TOMBALL, TX; RN112545553, TXR1582ZR; affiliation record date 2026-10-09.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112545553%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:56.033226+00:00.
- Site/address review: Priority reviewed as industrial: exact same address/name in TABS describes light-industrial business park; script phase/builder keywords incorrectly downgraded it.
- Verification: needs email pass (free-mail only); own page HTTP 200 fetched 2026-10-21T00:55:12.849401+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 5 gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com.; 10 alt1.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com.. Priority reviewed as industrial: exact same address/name in TABS describes light-industrial business park; script phase/builder keywords incorrectly downgraded it.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2026022493; Priority manually reviewed as industrial; original automated priority 3; needs email pass; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 3. H9: Old Glory Rolloff Dumpsters
- To: shelley@oldgloryrolloffdumpsters.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://oldgloryrolloffdumpsters.com/
- Email evidence: https://oldgloryrolloffdumpsters.com/contact/; HTTP 200 fetched 2026-10-21T00:57:55.130712+00:00.
- MX evidence: https://dns.google/resolve?name=oldgloryrolloffdumpsters.com&type=MX; checked 2026-10-21T01:01:12.510838+00:00; 0 oldgloryrolloffdumpsters-com.mail.protection.outlook.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Spring is a service-city reference, not a verified operating yard.
- Published coverage: Conroe, Magnolia, Montgomery, New Caney, Shenandoah, Spring, The Woodlands, Tomball and Willis.
- Hauler sources: https://oldgloryrolloffdumpsters.com/contact/
- Hook: TIMBERS EDGE RECREATIONAL CENTER, 21965 Woodward Blvd, Splendora, TX; RN112539168, TXR1517ZP; affiliation record date 2026-09-30.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112539168%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:57.724693+00:00.
- Site/address review: Exact community amenity center in TABS, same Woodward Blvd/Canopies Pkwy location described by TCEQ. Supplemental address, not a filled-in TCEQ street fact.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:57:55.130712+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 0 oldgloryrolloffdumpsters-com.mail.protection.outlook.com.. Exact community amenity center in TABS, same Woodward Blvd/Canopies Pkwy location described by TCEQ. Supplemental address, not a filled-in TCEQ street fact.
- Additional flags: Street-level site geocode unavailable; city-reference mileage blank, not guessed; Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2025020442; TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## Batch validation

`python3 scripts/check_packet.py data/packet_H9.csv`: **0 flags (3 rows checked)**. `python3 -m unittest discover -s tests`: **31 tests passed**. Field-preservation assertions passed; results are in the PR and validation JSON.

See `data/hauler_verification_H7-H10_2026-10-20.json`, `data/research_holds_H7-H10_2026-10-20.csv` and the reserve CSV for limits and unsuccessful leads.
