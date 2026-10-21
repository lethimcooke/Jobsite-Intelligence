# Hook packet: batch H10

Houston-area public research, October 20, 2026 (America/New_York). Prospecting only. Raw fetch timestamps use UTC, including early October 21.

**Partial batch:** 3/15 target rows. Across H7-H10: 14 packet rows, not 60. There are 24 verified contact records in total; 10 reserves have no packet hook. Do not treat reserve rows as ready for copy. No copy, Gmail, queue, tracker or existing-status changes.

Site facts come from fresh `pull_noi_sites.py --metro Houston --days 30` output and exact live TCEQ RN/authorization rechecks. Every selected authorization was ACTIVE at recheck, with a business affiliation-begin date within September 20 through October 20. **That date is the public record affiliation date, not independently verified original authorization issuance or construction start.** All sites are priority 1-2 after documented review. Some street addresses are explicit TCEQ location descriptions or supplemental TABS/facility addresses; those are identified per row, never represented as a filled TCEQ street field.

**Distance is from the labelled service-city reference, not a verified operating yard.** Matching is manual against published metro/service coverage. Numeric values are rounded straight-line miles, our read, using public ArcGIS reference points and the repo distance helper. Three site street geocodes were not strong enough; mileage is left blank on those rows. No nearest-site, driving-distance or delivery-quote claim. Exact delivery territory remains unverified.

**Email review:** 1 business-domain and 2 free-mail addresses. All are grade A, directly fetched on the own website in this session, with Cloudflare-protected addresses decoded where present and an actual non-null MX response. A business-domain contact is used when published alongside free mail. Free-mail rows retain `needs email pass`. Publication and MX do not verify individual mailbox acceptance, ownership, deliverability or consent.

**No reuse:** companies, legal aliases available from public matches, all email columns and website/email domains were screened against the master, DNC and H1-H6. Published phones were additionally screened. A bounced domain is suppressed in full. Selected sites and authorizations appear once across H7-H10 and were not used in H1-H6. Business/site names only; no individual names used as hooks.

No claim that work started, a vendor is unselected, or work is open for bid. Current carrier status, private ownership links, fleet counts, project stage and delivery coverage need review before any later operations.

| # | Batch | Hauler | Email (grade) | Yard / service reference | Publishes | Site | TCEQ auth / record date / RN | Operator on file | Miles (city reference) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H10 | H J Services LLC | hjservices@sbcglobal.net (A; needs email pass) | Cypress (service reference) | 11- to 15-yard roll-offs | NW99 DC III, 20400 CLAY INDUSTRIAL RD, TOMBALL, TX | TXR1568ZN / 2026-09-24 / RN112535935 | CLAY DEVELOPMENT & CONSTRUCTION INC | Not verified |
| 2 | H10 | Goldmine Dumpsters LLC | goldminedumps@gmail.com (A; needs email pass) | Houston (service reference) | roll-off containers | ELLA 45 PHASE II, 14250 ELLA BLVD, HOUSTON, TX | TXR1507ZR / 2026-10-06 / RN112543616 | HANOVER RS CONSTRUCTION LLC | 15 |
| 3 | H10 | All Pro Waste Services | info@allprowasteservices.com (A) | Magnolia (service reference) | roll-off containers | TC JESTER INDUSTRIAL, 2929 W MOUNT HOUSTON RD, HOUSTON, TX | TXR1520ZN / 2026-09-23 / RN112534748 | FCL BUILDERS TEXAS LLC | 28 |

## Sources and verification

## 1. H10: H J Services LLC
- To: hjservices@sbcglobal.net
- Email grade: A, own-site publication; needs email pass (free-mail only).
- Website: https://hjservicestx.com/
- Email evidence: https://hjservicestx.com/; HTTP 200 fetched 2026-10-21T00:55:48.950452+00:00.
- MX evidence: https://dns.google/resolve?name=sbcglobal.net&type=MX; checked 2026-10-21T01:01:12.955639+00:00; 10 mx-att.mail.am0.yahoodns.net.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial, 11-yd, 15-yd; Cypress is a service-city reference, not a verified operating yard.
- Published coverage: Conroe, Cypress, Hempstead, Hockley, Houston, Katy, Magnolia, Montgomery, Spring, Tomball.
- Hauler sources: https://hjservicestx.com/
- Hook: NW99 DC III, 20400 CLAY INDUSTRIAL RD, TOMBALL, TX; RN112535935, TXR1568ZN; affiliation record date 2026-09-24.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112535935%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:55.256752+00:00.
- Site/address review: Retain filed TCEQ street address and project classification. Site field describes a business, industrial facility or business location, not an individual.
- Verification: needs email pass (free-mail only); own page HTTP 200 fetched 2026-10-21T00:55:48.950452+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 10 mx-att.mail.am0.yahoodns.net.. Retain filed TCEQ street address and project classification. Site field describes a business, industrial facility or business location, not an individual.
- Additional flags: Street-level site geocode unavailable; city-reference mileage blank, not guessed; needs email pass; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 2. H10: Goldmine Dumpsters LLC
- To: goldminedumps@gmail.com
- Email grade: A, own-site publication; needs email pass (free-mail only).
- Website: https://goldminedumpsters.com/
- Email evidence: https://goldminedumpsters.com/contact/; HTTP 200 fetched 2026-10-21T01:05:24.678900+00:00.
- MX evidence: https://dns.google/resolve?name=gmail.com&type=MX; checked 2026-10-21T01:01:11.852495+00:00; 5 gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com.; 10 alt1.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Houston is a service-city reference, not a verified operating yard.
- Published coverage: Houston.
- Hauler sources: https://goldminedumpsters.com/contact/
- Hook: ELLA 45 PHASE II, 14250 ELLA BLVD, HOUSTON, TX; RN112543616, TXR1507ZR; affiliation record date 2026-10-06.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112543616%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:55.935099+00:00.
- Site/address review: Priority reviewed as industrial: TABS exact 14250 Ella Blvd describes a 90,763 sq ft warehouse, not housing.
- Verification: needs email pass (free-mail only); own page HTTP 200 fetched 2026-10-21T01:05:24.678900+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 5 gmail-smtp-in.l.google.com.; 20 alt2.gmail-smtp-in.l.google.com.; 40 alt4.gmail-smtp-in.l.google.com.; 10 alt1.gmail-smtp-in.l.google.com.; 30 alt3.gmail-smtp-in.l.google.com.. Priority reviewed as industrial: TABS exact 14250 Ella Blvd describes a 90,763 sq ft warehouse, not housing.
- Additional flags: Supplemental project/address source: https://www.tdlr.texas.gov/TABS/Search/Print/TABS2027003331; Priority manually reviewed as industrial; original automated priority 3; needs email pass; Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## 3. H10: All Pro Waste Services
- To: info@allprowasteservices.com
- Email grade: A, own-site publication; own-site business email; non-null MX checked.
- Website: https://allprowasteservices.com/
- Email evidence: https://www.allprowasteservices.com/contact_us/; HTTP 200 fetched 2026-10-21T00:55:33.905611+00:00.
- MX evidence: https://dns.google/resolve?name=allprowasteservices.com&type=MX; checked 2026-10-21T01:01:11.216326+00:00; 0 allprowasteservices-com.mail.protection.outlook.com.. No mailbox-delivery test.
- Fit: roll-off, construction, commercial; Magnolia is a service-city reference, not a verified operating yard.
- Published coverage: Magnolia and Greater Houston.
- Hauler sources: https://www.allprowasteservices.com/contact_us/
- Hook: TC JESTER INDUSTRIAL, 2929 W MOUNT HOUSTON RD, HOUSTON, TX; RN112534748, TXR1520ZN; affiliation record date 2026-09-23.
- Filing: https://data.texas.gov/resource/tzyg-j7q4.json?%24where=ref_num_txt%3D%27RN112534748%27+AND+program_code%3D%27STORM%27+AND+starts_with%28additional_id_text%2C%27TXR15%27%29&%24limit=1000; exact live recheck 2026-10-21T01:31:55.151104+00:00.
- Site/address review: Retain filed TCEQ street address and project classification. Site field describes a business, industrial facility or business location, not an individual.
- Verification: own-site business email; non-null MX checked; own page HTTP 200 fetched 2026-10-21T00:55:33.905611+00:00; Fleet size not independently verified; no claim of zero vehicles or a confirmed fleet below 60. Own-site local operator presentation and published services; private beneficial ownership and equipment ownership not independently audited. No positive franchise/national/operator-account link found in checked sources. Mailbox acceptance and delivery are untested. No verified operating-yard coordinate; city reference only. MX: 0 allprowasteservices-com.mail.protection.outlook.com.. Retain filed TCEQ street address and project classification. Site field describes a business, industrial facility or business location, not an individual.
- Additional flags: Date is TCEQ affiliation-begin date; original authorization issue date not independently established.

## Batch validation

`python3 scripts/check_packet.py data/packet_H10.csv`: **0 flags (3 rows checked)**. `python3 -m unittest discover -s tests`: **31 tests passed**. Field-preservation assertions passed; results are in the PR and validation JSON.

See `data/hauler_verification_H7-H10_2026-10-20.json`, `data/research_holds_H7-H10_2026-10-20.csv` and the reserve CSV for limits and unsuccessful leads.
