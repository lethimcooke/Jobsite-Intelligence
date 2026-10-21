# Houston recheck and public research: October 21, 2026

Prospecting only. No copy, Gmail, sending, queues or tracker edits. All 349 existing Houston master rows, including their statuses, are preserved byte for byte. H5/H6 packets, DNC, ledger and results are unchanged. Four new Houston rows were appended as Not contacted. Seven DFW research-only rows were added as Not contacted; no DFW packets.

## Recheck

- H5: 14/15 exact addresses still published; 15/15 domains passed MX.
- H6: 14/15 exact addresses still published; 15/15 domains passed MX.
- Unconfirmed publication: Precision Dumpsters LLC, inquiry@precisiondumpstersllc.com; Big Orange Bins, binsdumps77@gmail.com. Live root/contact pages loaded, but the exact email was not found after link, markup and Cloudflare decoding checks. No different published address confirmed. This does not establish closure or a bounce.
- Normal public WWW/HTTP retries resolved four initially inaccessible sites. All checks were read-only. No forms submitted or test messages sent.

## Packets and reserves

| Packet | Rows | Business-domain | Free-mail | Checker |
|---|---:|---:|---:|---|
| H11 | 9 | 5 | 4 | 0 flags, CSV and Markdown |
| H12 | 4 | 4 | 0 | 0 flags, CSV and Markdown |

All 10 reserves passed current own-site publication and actual MX checks. Nine have matches in H11. Aqua-Zyme remains unmatched: no eligible unused recent ACTIVE Brazoria site with a usable location was verified within its published local hauling/sanitation coverage. Its national equipment-shipping business was not treated as local hauling coverage. It remains in the master unchanged.

Throne Ranger's H11 row is **exploratory**: it publishes restroom-trailer rental/delivery, but construction service is not established. Its multifamily site also has a TCEQ/TABS address discrepancy. Review those limits before later operations; this packet grants no approval to send. No H13 is manufactured from unqualified leads.

H12 is short of the roughly 15-row target. It contains three sanitation operators and one roll-off operator with a Waller County outlet corroborated by public records. K & H is based in Brenham and included for its published Waller sanitation service. New roll-off operator: Waste Solutions USA, Hempstead/Waller. Tru-Tex passed publication/MX but was held because the same-name Anahuac carrier has a different phone/email and its exact identity/base is not established. Every accepted address was fetched on its own live site today and has a recorded non-null MX result.

## Sources and funnel

- Yellow Pages public city/category searches: 34 queries, 967 result rows with substantial overlap. Cities include Waller, Hempstead, Brookshire, Hockley, Prairie View, Liberty, Dayton, Cleveland, Mont Belvieu, Anahuac, Winnie, Wallisville, Baytown, Crosby and core-county sanitation searches.
- Comptroller: 15 ring-county NAICS 562111/562119/562991 records; 37 core-county NAICS 562991 records. Registry contacts were discovery leads only, never accepted as email evidence.
- FMCSA: 101 active ring-county refuse/sanitation discovery records, plus exact carrier/phone/domain queries. Known over-60 fleets, national groups and franchises were excluded. A phone-linked trucking record is not presented as proof of Shep Boys' sanitation fleet size.
- Exa public web search: 38 queries including site/address corroboration and the initial broader search. Search snippets were discovery only; accepted emails required direct own-page fetches.
- Direct research: 156 candidate domain spellings fetched, including WWW aliases and hypotheses from public registry identities. These are not 156 distinct operators. Of them, 96 had no valid email on a successful direct HTTP 200 page. Others were existing accounts, national/franchise/broker sites, unrelated or changed domains, septic-only businesses, or roll-off operators without a verified requested county base. The holds CSV gives domain-level observations and reasons.
- Actual MX: 40 domains queried across rechecks, reserves and new research. One failed: houstonportapottyrentals.com returned NOERROR with no MX answer and was dropped. No accepted address failed MX. Do not confuse valid MX with an individual mailbox delivery test.
- DFW optional: the prescribed enrich command identified 215 registry candidates, scanned 66 business domains and auto-marked 16 fits. Seven independently reviewed rows met the stronger own-live-site plus MX standard. Corporate/franchise, registry-only, inaccessible and insufficient-scope candidates were excluded. The command initially crashed on a malformed registry email; a scratch-only guard allowed completion. Repository scripts are unchanged.
- TCEQ: the prescribed fresh 30-day pull initially hit 503. Per-dataset retries recovered all five datasets for both core and ring counties: 153 core sites, 25 ring sites after the script's individual-operator filtering. Exact live RN/TXR15 rechecks and manual priority/address review selected 13 unique sites. No selected RN or authorization appears in prior H1-H10 CSV or outreach records.

Counts overlap across discovery sources. The source-summary JSON records query URLs, fetch times and response counts; the holds CSV records unsuccessful leads. DNS responses and own-page verification evidence are included separately.

## Limits

- TCEQ dates are business affiliation-begin dates on ACTIVE authorizations. Original authorization issue dates were not independently verified, so the strict claim that each authorization was first issued in the last 30 days cannot be made. No construction-start or procurement-stage claim.
- Sam's Club 9753 uses a supplemental filed street-intersection Location Address; Creekland amenity uses its explicit TCEQ street intersection. These are not numbered postal addresses or verified entrances. The TABS suite address for Creekland was not substituted as the physical jobsite.
- The Vic at Sunterra: TCEQ 7229 Bartlett St versus TABS 245 Bartlett Road; exact entrance, original phase and present construction stage unresolved.
- Prestige publishes info@pprestrooms.com on its own different-domain website. Its MX is Mailgun; inbound routing/mailbox acceptance and Katy dispatch coverage remain unverified.
- No verified yard coordinates or numeric mileage; service_area_city and miles_from_service_city_our_read columns retained, distances blank. Published metro/service-area matches are our read, not a delivery commitment.
- Private beneficial ownership, undisclosed account links and current aggregate fleet totals cannot be fully established from these public sources. Filed power units are dated carrier filings, not current fleet audits.
- JavaScript/browser-only contact sites that could not be rendered were held. No cached search email was substituted for a live own-page fetch.

## Validation

H11 CSV: 0 flags (9 rows checked). H12 CSV: 0 flags (4 rows checked). Matching Markdown packets also print 0 flags. All 31 unit tests pass. Existing-row and protected-file preservation checks pass. Full outputs are in data/validation_H11-H12_2026-10-21.json.
