# Hook packet: batch H8

Houston-area public research, October 20, 2026 (America/New_York). Prospecting only. Raw fetch timestamps use UTC, including early October 21.

**Partial batch:** 4/15 target rows. Across H7-H10: 14 packet rows, not 60. There are 24 verified contact records in total; 10 reserves have no packet hook. Do not treat reserve rows as ready for copy. No copy, Gmail, queue, tracker or existing-status changes.

Site facts come from fresh `pull_noi_sites.py --metro Houston --days 30` output and exact live TCEQ RN/authorization rechecks. Every selected authorization was ACTIVE at recheck, with a business affiliation-begin date within September 20 through October 20. **That date is the public record affiliation date, not independently verified original authorization issuance or construction start.** All sites are priority 1-2 after documented review. Some street addresses are explicit TCEQ location descriptions or supplemental TABS/facility addresses; those are identified per row, never represented as a filled TCEQ street field.

**Distance is from the labelled service-city reference, not a verified operating yard.** Matching is manual against published metro/service coverage. Numeric values are rounded straight-line miles, our read, using public ArcGIS reference points and the repo distance helper. Three site street geocodes were not strong enough; mileage is left blank on those rows. No nearest-site, driving-distance or delivery-quote claim. Exact delivery territory remains unverified.

**Email review:** 4 business-domain and 0 free-mail addresses. All are grade A, directly fetched on the own website in this session, with Cloudflare-protected addresses decoded where present and an actual non-null MX response. A business-domain contact is used when published alongside free mail. Free-mail rows retain `needs email pass`. Publication and MX do not verify individual mailbox acceptance, ownership, deliverability or consent.

**No reuse:** companies, legal aliases available from public matches, all email columns and website/email domains were screened against the master, DNC and H1-H6. Published phones were additionally screened. A bounced domain is suppressed in full. Selected sites and authorizations appear once across H7-H10 and were not used in H1-H6. Business/site names only; no individual names used as hooks.

No claim that work started, a vendor is unselected, or work is open for bid. Current carrier status, private ownership links, fleet counts, project stage and delivery coverage need review before any later operations.

| # | Batch | Hauler | Email (grade) | Yard / service reference | Publishes | Site | TCEQ auth / record date / RN | Operator on file | Miles (city reference) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H8 | Supreme Site Services LLC | case@supremesiteservicesco.com (A) | Spring (service reference) | portable toilets | HCA KINGWOOD TOWER EXPANSION, 22999 Highway 59 N, Kingwood, TX | TXR1544ZP / 2026-09-30 / RN112539697 | R CONSTRUCTION COMPANY | 10 |
| 2 | H8 | SolidSite | erik@gosolidsite.com (A) | Richmond (service reference) | portable toilets | HILLCROFT LOGISTICS, 13830 HILLCROFT AVENUE, HOUSTON, TX | TXR1599ZT / 2026-10-19 / RN112550728 | BURTON CONSTRUCTION CO | 17 |
| 3 | H8 | Action Trucking Company | info@actiontrucking.com (A) | Houston (service reference) | roll-off containers | CARSON FAIRMONT, 7501 Fairmont Parkway, Pasadena, TX | TXR1580ZN / 2026-09-24 / RN112536255 | BURTON CONSTRUCTION CO | 17 |
| 4 | H8 | Century Sanitation LLC | chad@centurysanitation.com (A) | Houston (service reference) | portable toilets | BELTWAY PINES BUSINESS PARK, 9202 E Sam Houston Pkwy N, Houston, TX | TXR1588ZM / 2026-09-22 / RN112534185 | BURTON CONSTRUCTION CO | 13 |

## Sources and verification

## 1. H8: Supreme Site Services LLC
- To: case@supremesiteservicesco.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://supremesiteservicesco.com/
- Email evidence: https://supremesiteservicesco.com/contact-us/; HTTP 200 fetched 2026-10-21T00:55:55.873707+00:00.
- MX evidence: https://dns.google/resolve?name=supremesiteservicesco.com&type=MX; checked 2026-10-21T01:01:13.205220+00:00; 1 smtp.google.com.. No mailbox-delivery test.
- Fit: portable toilets, restroom trailers, construction, commercial; Spring is a service-city reference, not a verified operating yard.
- Published coverage: Conroe, Cypress, Hockley, Houston, Humble, Magnolia, Montgomery, New Caney, Porter, Spring, The Woodlands, Tomball, Waller, Willis.
- Hauler sources: https://supremesiteservicesco.com/contact-us/
- Hook: HCA KINGWOOD TOWER EXPANSION, 22999 Highway 59 N, Kingwood, TX; RN112539697, TXR1544ZP; affiliation record date 2026-09-30.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112539697%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:56.981835+00:00.
- Site/address review: TCEQ identifies the north-side parking lot of HCA Houston Healthcare Kingwood. HCA own location page and exact-name TABS corroborate the hospital campus address; supplemental address, not filed TCEQ street field.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:55:55.873707+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 1 smtp.google.com.. TCEQ identifies the north-side parking lot of HCA Houston Healthcare Kingwood. HCA own location page and exact-name TABS corroborate the hospital campus address; supplemental address, not filed TCEQ street field.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2026016305; TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 2. H8: SolidSite
- To: erik@gosolidsite.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://gosolidsite.com/
- Email evidence: https://gosolidsite.com/about; HTTP 200 fetched 2026-10-21T00:55:43.441194+00:00.
- MX evidence: https://dns.google/resolve?name=gosolidsite.com&type=MX; checked 2026-10-21T01:01:11.935167+00:00; 0 gosolidsite-com.mail.protection.outlook.com.. No mailbox-delivery test.
- Fit: portable toilets, construction, commercial; Richmond is a service-city reference, not a verified operating yard.
- Published coverage: Greater Houston, Fort Bend and Rio Grande Valley.
- Hauler sources: https://gosolidsite.com/about
- Hook: HILLCROFT LOGISTICS, 13830 HILLCROFT AVENUE, HOUSTON, TX; RN112550728, TXR1599ZT; affiliation record date 2026-10-19.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112550728%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:54.918075+00:00.
- Site/address review: Retain filed TCEQ street address and project classification. Site field describes a business, industrial facility or business location, not an individual.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:55:43.441194+00:00; Public active carrier record(s) tied by phone or exact business email domain: USDOT 7993817, 1 power units as filed , USDOT 4534767, 1 power units as filed 20260217. Filed counts are not a current fleet audit. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 0 gosolidsite-com.mail.protection.outlook.com.. Retain filed TCEQ street address and project classification. Site field describes a business, industrial facility or business location, not an individual.
- Additional flags: Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 3. H8: Action Trucking Company
- To: info@actiontrucking.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://actiontrucking.com/
- Email evidence: https://www.actiontrucking.com/; HTTP 200 fetched 2026-10-21T00:55:25.184056+00:00.
- MX evidence: https://dns.google/resolve?name=actiontrucking.com&type=MX; checked 2026-10-21T01:01:11.302475+00:00; 10 actiontrucking-com.mail.protection.outlook.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Houston is a service-city reference, not a verified operating yard.
- Published coverage: Greater Houston.
- Hauler sources: https://www.actiontrucking.com/; https://www.yellowpages.com/search?search_terms=roll+off+dumpster+rental&geo_location_terms=Sugar+Land%2C+TX
- Hook: CARSON FAIRMONT, 7501 Fairmont Parkway, Pasadena, TX; RN112536255, TXR1580ZN; affiliation record date 2026-09-24.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112536255%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:57.579077+00:00.
- Site/address review: Exact-name commercial-property filing in TABS provides address consistent with TCEQ Fairmont/Red Bluff corner. Business/property name, not a named individual.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:55:25.184056+00:00; Public active carrier record(s) tied by phone or exact business email domain: USDOT 1948543, 27 power units as filed 20260303. Filed counts are not a current fleet audit. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 10 actiontrucking-com.mail.protection.outlook.com.. Exact-name commercial-property filing in TABS provides address consistent with TCEQ Fairmont/Red Bluff corner. Business/property name, not a named individual.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2026017481; TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 4. H8: Century Sanitation LLC
- To: chad@centurysanitation.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://centurysanitation.com/
- Email evidence: https://www.centurysanitation.com/contact-us; HTTP 200 fetched 2026-10-21T01:14:12.463420+00:00.
- MX evidence: https://dns.google/resolve?name=centurysanitation.com&type=MX; checked 2026-10-21T01:22:38.626735+00:00; 1 aspmx.l.google.com.; 10 alt3.aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.. No mailbox-delivery test.
- Fit: portable toilets, construction, commercial; Houston is a service-city reference, not a verified operating yard.
- Published coverage: Houston office and construction/oilfield sanitation locations in Texas.
- Hauler sources: https://www.centurysanitation.com/contact-us
- Hook: BELTWAY PINES BUSINESS PARK, 9202 E Sam Houston Pkwy N, Houston, TX; RN112534185, TXR1588ZM; affiliation record date 2026-09-22.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112534185%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:58.384625+00:00.
- Site/address review: TABS exact park name and matching East Beltway location describe a one-story tiltwall shell; supplemental address.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T01:14:12.463420+00:00; Public active carrier record(s) tied by phone or exact business email domain: USDOT 4013595, 30 power units as filed 20250520. Filed counts are not a current fleet audit. Exact own Houston office address 2096 Genoa Red Bluff Rd and own email domain match active Century Sanitation LLC, USDOT 4013595. Own site publishes construction sanitation and Houston office; current route availability is unverified. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 1 aspmx.l.google.com.; 10 alt3.aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.. TABS exact park name and matching East Beltway location describe a one-story tiltwall shell; supplemental address.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2027001573; TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## Batch validation

`python3 scripts/check_packet.py data/packet_H8.csv`: **0 flags (4 rows checked)**. `python3 -m unittest discover -s tests`: **31 tests passed**. Field-preservation assertions passed; results are in the PR and validation JSON.

See `data/hauler_verification_H7-H10_2026-10-20.json`, `data/research_holds_H7-H10_2026-10-20.csv` and the reserve CSV for limits and unsuccessful leads.
