# Houston H7-H10 research handoff

Prepared October 20, 2026, America/New_York. Prospecting only.

**Partial delivery: 14 packet rows, not the requested 60.** H7 4, H8 4, H9 3, H10 3. There are **24 verified contacts: 17 business-domain and 7 free-mail**, including **10 reserves without a packet hook**. The contact shortfall is 36; packet shortfall is 46. Do not treat the reserves as ready for copy.

All 325 existing master rows remain byte-for-byte unchanged. Twenty-four new rows were appended as Not contacted, with original column headers. No copy, Gmail, queues, tracker, results, ledger or existing-status changes.

The 30-day site window was retained. No response authorizing a longer window was received while working. A wider window would need explicit authorization and would not solve the separate 60-contact shortfall by itself.

## Validation

| Packet | Rows | Business-domain | Free-mail | Checker |
|---|---:|---:|---:|---|
| H7 | 4 | 4 | 0 | 0 flags (4 rows checked) |
| H8 | 4 | 4 | 0 | 0 flags (4 rows checked) |
| H9 | 3 | 2 | 1 | 0 flags (3 rows checked) |
| H10 | 3 | 1 | 2 | 0 flags (3 rows checked) |

Reserve CSV: 0 flags (10 rows checked). Unit tests: 31 passed. Extra assertions cover all email columns, legal/DBA names from available matches, website/email domains, published phones, prior packet identities, DNC and cross-packet uniqueness. Fourteen distinct RN/site and authorization IDs, no H1-H6 reuse.

## Sources and outcomes

Counts overlap. Website leads include unrelated businesses, directories, wrong-state providers and failed website hypotheses; they are not 552 confirmed Houston haulers.

| Source | Tried/results | Outcome |
|---|---|---|
| YellowPages | 128 queries, 2392 result listings; 125 HTTP 200, one 404, two 503 | Suburban category pages, later pages and exact registry-name lookups. Discovery only; no directory email accepted. |
| BBB | 187 category/profile pages, including 163 profile fetches | Own-domain leads; many were outside the five counties or already used. |
| Houston city operator list | Six-page public PDF, updated June 12, 2020 | Historical discovery/alias screen, not current licensing. It confirms Conroe Chem Can dba Tanks A Lot; the phone matches an existing account, so skipped. |
| Comptroller | 307 five-county NAICS 562111/562119/562991 outlet records | Identity/domain discovery only; no registry-only email accepted. |
| FMCSA | 2626 wider name-query records, filtered to 22 relevant new name/size leads; additional phone batches | Domain, legal/DBA and fleet crosschecks. A broad PORTA substring also matched transportation names; those irrelevant records were filtered, not counted as hauler prospects. Century confirmed by exact own office address and filed business domain; its chosen email is the current own-site address, not the different filed address. |
| Exa | 32 successful queries, 525 results, then one free-tier rate-limit response | Continued with directories, registry domain leads, website hypotheses, canonical addresses and direct own reads; the rate limit was not the stopping rule. |
| PSAI directory | Public find-a-member URL returned 403 | No bypass or member-only access; no contacts accepted from it. Public PSAI guide was not an operator directory. |
| Direct websites | 552 domain leads, 1451 page attempts including redirects/retries | 24 contacts passed the combined own-page/MX/account screen. Cloudflare email addresses decoded. Canonical HTTPS/www and published HTTP fallbacks were tried on transport failures. |
| Other public search / reader / render checks | Google returned a JS shell, reader returned CAPTCHA; Bing RSS was irrelevant; isolated Chromium own-page rendering failed | No CAPTCHA bypass, cookies or login. None accepted as email proof; direct own-page evidence remains mandatory. |
| TCEQ | Five-region pull, 147 rows since September 20; 18 manually reviewed source/address candidates | Four had no recent ACTIVE authorization at exact recheck and were dropped. Fourteen selected, with street/address provenance and scope review. Other records were used already, non-priority construction types, lacked a reliable street address, or had ambiguous scope/name. |
| Supplemental project addresses | Public TABS project-name/address searches plus HCA own facility page | Added/corroborated specific addresses and corrected automated industrial classifications. No unsupported house numbers, no intersection geocodes presented as street-level points. |

## Why rows were held

One otherwise-fit company, Arcann Waste, failed the actual non-null MX check. Conroe Chem Can and MGM Waste matched published phones of existing accounts. These were excluded before append. The wider website audit has **260 no-live-email domain leads**; that is not a claim of 260 operating haulers. Forms, blocked or unavailable pages, agency contacts, template/demo sites and registry-only addresses were not promoted into packets. All unsuccessful domain leads and exact available URLs/statuses are in the holds CSV.

| Website-lead disposition | Count |
|---|---:|
| coverage_unverified | 38 |
| directory_or_nonprovider | 32 |
| failed_mx | 1 |
| linked_existing | 6 |
| national_franchise_or_broker | 48 |
| no_live_email | 260 |
| operator_or_identity_unverified | 42 |
| packet | 14 |
| research_hold | 25 |
| scope_or_wrong_identity | 76 |
| verified_reserve | 10 |

Positive linked-account exclusions also include RMI becoming Moffitt, and Gainsborough/Texas Outhouse/Luxury Event Trailers publishing existing GTX Waste contacts. Heritage/First Class published Doodie Calls contact links and were held rather than treated as separate independent accounts. VETS franchise, nationwide partner networks, wrong-state lookalikes and junk/septic-only scopes were skipped. No business-domain email was replaced with a published free-mail alternative.

## Unverified or limited

- MX plus own-site publication does not establish individual mailbox acceptance or delivery. No SMTP probe, email or form was sent. Free-mail retains needs email pass.
- Private beneficial ownership, unpublished partner links and current total fleet size are not comprehensively verifiable. Specific active filed carrier counts are quoted as filings, not a fleet audit.
- The TCEQ source and pull script expose affiliation-begin dates. Original authorization issue dates were not independently established. Every selected exact authorization was ACTIVE, with a recent business affiliation; no construction-start or opening claim.
- Some TCEQ street fields are blank. Explicit location descriptions and matched supplemental property/facility addresses are labelled, not silently made into filed TCEQ addresses. Hightower has a county discrepancy: TCEQ Harris versus geocoder Fort Bend. It is assigned only to a hauler advertising both counties; exact boundary remains unverified.
- NW99 DC III and Timbers Edge lack a strong street geocode; Pine Forest returned a street-name-level point. All three city-reference mileages stay blank. No driving distance, verified yard distance, nearest-site or delivery quote is claimed.
- Exact site footprint and actual delivery coverage need confirmation. Some hook facts describe civil/site work; no claim of available work, an unselected hauler or open bids.

## Files

- data/packet_H7.csv through data/packet_H10.csv and outreach/H7_Hook_Packet.md through H10_Hook_Packet.md.
- data/new_haulers_H7-H10_2026-10-20.csv: the 24 appended rows.
- data/verified_reserve_H7-H10_2026-10-20.csv: 10 contact records without hooks, not queued.
- data/research_holds_H7-H10_2026-10-20.csv: unsuccessful domain leads, including form URLs where verified.
- data/sites_H7-H10_2026-10-20.csv: 14 reviewed active source records with original/supplemental address provenance.
- data/hauler_verification_H7-H10_2026-10-20.json and validation JSON: exact evidence, query provenance, DNS responses and preservation checks.
