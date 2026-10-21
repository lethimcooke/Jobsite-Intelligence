# Hook packet: batch H7

Houston-area public research, October 20, 2026 (America/New_York). Prospecting only. Raw fetch timestamps use UTC, including early October 21.

**Partial batch:** 4/15 target rows. Across H7-H10: 14 packet rows, not 60. There are 24 verified contact records in total; 10 reserves have no packet hook. Do not treat reserve rows as ready for copy. No copy, Gmail, queue, tracker or existing-status changes.

Site facts come from fresh `pull_noi_sites.py --metro Houston --days 30` output and exact live TCEQ RN/authorization rechecks. Every selected authorization was ACTIVE at recheck, with a business affiliation-begin date within September 20 through October 20. **That date is the public record affiliation date, not independently verified original authorization issuance or construction start.** All sites are priority 1-2 after documented review. Some street addresses are explicit TCEQ location descriptions or supplemental TABS/facility addresses; those are identified per row, never represented as a filled TCEQ street field.

**Distance is from the labelled service-city reference, not a verified operating yard.** Matching is manual against published metro/service coverage. Numeric values are rounded straight-line miles, our read, using public ArcGIS reference points and the repo distance helper. Three site street geocodes were not strong enough; mileage is left blank on those rows. No nearest-site, driving-distance or delivery-quote claim. Exact delivery territory remains unverified.

**Email review:** 4 business-domain and 0 free-mail addresses. All are grade A, directly fetched on the own website in this session, with Cloudflare-protected addresses decoded where present and an actual non-null MX response. A business-domain contact is used when published alongside free mail. Free-mail rows retain `needs email pass`. Publication and MX do not verify individual mailbox acceptance, ownership, deliverability or consent.

**No reuse:** companies, legal aliases available from public matches, all email columns and website/email domains were screened against the master, DNC and H1-H6. Published phones were additionally screened. A bounced domain is suppressed in full. Selected sites and authorizations appear once across H7-H10 and were not used in H1-H6. Business/site names only; no individual names used as hooks.

No claim that work started, a vendor is unselected, or work is open for bid. Current carrier status, private ownership links, fleet counts, project stage and delivery coverage need review before any later operations.

| # | Batch | Hauler | Email (grade) | Yard / service reference | Publishes | Site | TCEQ auth / record date / RN | Operator on file | Miles (city reference) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H7 | Missouri City Porta Potty | contact@missouricityportapotty.com (A) | Missouri City (service reference) | portable toilets | CHAIR KING, 25402 Katy Fwy, Katy, TX | TXR1591ZT / 2026-10-19 / RN112550371 | UNITED CONSTRUCTORS OF TEXAS INC | 21 |
| 2 | H7 | EDCA Cleaning Services LLC | info@alldumpstersrental.com (A) | Alvin (service reference) | 15- to 25-yard roll-offs | HIGHTOWER BUSINESS PARK - PHASE 2, 5616 MCHARD RD, HOUSTON, TX | TXR1568ZM / 2026-09-22 / RN112533690 | SLATE CONSTRUCTION LLC | 18 |
| 3 | H7 | SwellTex Services | info@swelltex.com (A) | Montgomery (service reference) | roll-off containers | LAKE CREEK APARTMENTS, 20970 FM 2854, Montgomery, TX | TXR1530ZS / 2026-10-12 / RN112546734 | BLAZER BUILDING SOUTHWEST LLC | 3 |
| 4 | H7 | Dumpster Conroe | info@dumpsterconroe.com (A) | Conroe (service reference) | roll-off containers | 8513 & 8517 PRINE LN BUSINESS CENTER, 8513 Prine Lane, MONTGOMERY County, TX | TXR1590ZS / 2026-10-14 / RN112547906 | CONNOR DAVIS CONSTRUCTION | 12 |

## Sources and verification

## 1. H7: Missouri City Porta Potty
- To: contact@missouricityportapotty.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://missouricityportapotty.com/
- Email evidence: https://missouricityportapotty.com/contact.html; HTTP 200 fetched 2026-10-21T00:55:45.227703+00:00.
- MX evidence: https://dns.google/resolve?name=missouricityportapotty.com&type=MX; checked 2026-10-21T01:01:12.208007+00:00; 20 eforward5.registrar-servers.com.; 10 eforward1.registrar-servers.com.; 10 eforward2.registrar-servers.com.; 15 eforward4.registrar-servers.com.; 10 eforward3.registrar-servers.com.. No mailbox-delivery test.
- Fit: portable toilets, construction, commercial; Missouri City is a service-city reference, not a verified operating yard.
- Published coverage: Missouri City and Fort Bend County.
- Hauler sources: https://missouricityportapotty.com/contact.html
- Hook: CHAIR KING, 25402 Katy Fwy, Katy, TX; RN112550371, TXR1591ZT; affiliation record date 2026-10-19.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112550371%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:57.356591+00:00.
- Site/address review: Chair King is a retailer, not a person. Exact-name Katy TABS new retail building gives this supplemental address; matches TCEQ northwest I-10/Katy Village Parkway location.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:55:45.227703+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 20 eforward5.registrar-servers.com.; 10 eforward1.registrar-servers.com.; 10 eforward2.registrar-servers.com.; 15 eforward4.registrar-servers.com.; 10 eforward3.registrar-servers.com.. Chair King is a retailer, not a person. Exact-name Katy TABS new retail building gives this supplemental address; matches TCEQ northwest I-10/Katy Village Parkway location.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2026020213; TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 2. H7: EDCA Cleaning Services LLC
- To: info@alldumpstersrental.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://alldumpstersrental.com/
- Email evidence: https://alldumpstersrental.com/contact-us/; HTTP 200 fetched 2026-10-21T00:55:54.062071+00:00.
- MX evidence: https://dns.google/resolve?name=alldumpstersrental.com&type=MX; checked 2026-10-21T01:01:11.248855+00:00; 0 alldumpstersrental.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial, 15-yd, 20-yd, 25-yd; Alvin is a service-city reference, not a verified operating yard.
- Published coverage: Brazoria, Fort Bend, Galveston and Harris counties.
- Hauler sources: https://alldumpstersrental.com/contact-us/
- Hook: HIGHTOWER BUSINESS PARK - PHASE 2, 5616 MCHARD RD, HOUSTON, TX; RN112533690, TXR1568ZM; affiliation record date 2026-09-22.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112533690%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:56.165957+00:00.
- Site/address review: Priority reviewed as industrial business park, not a subdivision. TCEQ filed 5616 McHard Rd retained. TABS same park Building 05 describes a warehouse; different building address is not substituted.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:55:54.062071+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 0 alldumpstersrental.com.. Priority reviewed as industrial business park, not a subdivision. TCEQ filed 5616 McHard Rd retained. TABS same park Building 05 describes a warehouse; different building address is not substituted.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2027001125; Priority manually reviewed as industrial; original automated priority 3; County discrepancy: TCEQ Harris, mapped street point Fort Bend; both within advertised coverage and requested metro; exact boundary unverified; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 3. H7: SwellTex Services
- To: info@swelltex.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://swelltex.com/
- Email evidence: https://www.swelltex.com/contact; HTTP 200 fetched 2026-10-21T00:58:01.701252+00:00.
- MX evidence: https://dns.google/resolve?name=swelltex.com&type=MX; checked 2026-10-21T01:01:13.228986+00:00; 10 alt3.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; 1 aspmx.l.google.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Montgomery is a service-city reference, not a verified operating yard.
- Published coverage: Montgomery County and surrounding counties.
- Hauler sources: https://www.swelltex.com/contact
- Hook: LAKE CREEK APARTMENTS, 20970 FM 2854, Montgomery, TX; RN112546734, TXR1530ZS; affiliation record date 2026-10-12.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112546734%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:55.699221+00:00.
- Site/address review: TCEQ location description explicitly gives 20970 FM 2854.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:58:01.701252+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 10 alt3.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; 1 aspmx.l.google.com.. TCEQ location description explicitly gives 20970 FM 2854.
- Additional flags: TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 4. H7: Dumpster Conroe
- To: info@dumpsterconroe.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://dumpsterconroe.com/
- Email evidence: https://dumpsterconroe.com/contact-us/; HTTP 200 fetched 2026-10-21T01:05:13.365848+00:00.
- MX evidence: https://dns.google/resolve?name=dumpsterconroe.com&type=MX; checked 2026-10-21T01:22:38.040768+00:00; 5 mx1.hostinger.pk.; 10 mx2.hostinger.pk.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Conroe is a service-city reference, not a verified operating yard.
- Published coverage: Conroe, Magnolia, Spring and Montgomery County.
- Hauler sources: https://dumpsterconroe.com/contact-us/
- Hook: 8513 & 8517 PRINE LN BUSINESS CENTER, 8513 Prine Lane, MONTGOMERY County, TX; RN112547906, TXR1590ZS; affiliation record date 2026-10-14.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112547906%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:55.426966+00:00.
- Site/address review: TCEQ location description explicitly gives 8513 & 8517 Prine Lane; 8513 is the geocoding reference.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T01:05:13.365848+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 5 mx1.hostinger.pk.; 10 mx2.hostinger.pk.. TCEQ location description explicitly gives 8513 & 8517 Prine Lane; 8513 is the geocoding reference.
- Additional flags: TCEQ street field blank; reference address from location description or explicitly linked supplemental source; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## Batch validation

`python3 scripts/check_packet.py data/packet_H7.csv`: **0 flags (4 rows checked)**. `python3 -m unittest discover -s tests`: **31 tests passed**. Field-preservation assertions passed; results are in the PR and validation JSON.

See `data/hauler_verification_H7-H10_2026-10-20.json`, `data/research_holds_H7-H10_2026-10-20.csv` and the reserve CSV for limits and unsuccessful leads.
