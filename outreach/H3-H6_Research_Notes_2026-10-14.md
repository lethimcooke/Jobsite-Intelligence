# Houston hauler research: H3 to H6

Research started October 14, 2026. Prospecting only. The live repository at f693a68 and its
AGENTS.md governed the work. README_FIRST.md and AGENTS.md from the attached v2 prospector
kit were read. The live checkout has no README_FIRST.md; its README.md and CLAUDE.md were
also consulted, with current AGENTS.md taking priority over older launch notes.

## Delivery

| Packet | Prospects | CSV checker | Markdown checker |
|---|---:|---|---|
| H3 | 15 | 0 flags | 0 flags |
| H4 | 15 | 0 flags | 0 flags |
| H5 | 15 | 0 flags | 0 flags |
| H6 | 15 | 0 flags | 0 flags |

There are 60 distinct prospects: **52 newly added companies and 8 requalified existing
Not contacted rows**. All eight were previously fit False, not previously qualified fits.
The master list grows from 273 to 325 rows. Existing outreach_status values are unchanged;
all 52 additions are Not contacted. No H1/H2 account is reused.

- 33 addresses are business-domain emails published on the hauler's own website.
- 27 addresses are free-mail addresses published on the hauler's own website. They carry
  the mandatory **needs email pass** flag in the packet and list notes. Source grade A means
  own-site publication only; it does not remove that flag or establish delivery readiness.
- Every packet row has an own-site email citation, service evidence, a TCEQ RN and TXR15
  authorization, record URL and verification notes. No email was guessed.
- The eight requalified rows are PARADA WASTE LLC, TOP WASTE SOLUTIONS, NATION WASTE INC,
  BEST DUMPSTER SERVICE, Q-LINE SITE SERVICES LLC, TEXAS ROLL OFF,
  YOUR DUMPSTER BUDDY RENTALS LLC and TAKE1 DUMPSTER RENTAL LLC.

## Sources and screening

Discovery used the City of Houston commercial solid-waste operator list, chamber/BBB
search results and suburb-specific public web search. The city's published list is dated
June 12, 2020, so it is a discovery source only:
https://www.houstontx.gov/ara/franchise/solid_waste_hauler_operators.pdf

Services and contact addresses were checked on public own-site pages, read through Jina
Reader and/or direct public HTML. Alternate domains with the same email were treated as
one account, including DW Companies/DWC Dumpsters, A&W's two domains and Humpty's two sites.
The underlying site's public Cloudflare email display, when present, was decoded as public
contact information. No logins, cookies, contact-form submissions or mailbox calls were used.

Code compared candidate company/legal names, emails, website domains, available published
phones and identified USDOT numbers with the existing list and H1/H2 identities. It also
checked do-not-contact and exclusions, and the available ASI master/trade/exclusion/DNC
snapshots. No matches to those ASI snapshots were found. These are snapshot checks, not a
claim of access to current Gmail engagement or every possible owner/partner relationship.

Current FMCSA records were queried through the public Company Census dataset:
https://data.transportation.gov/resource/az4n-8mr2.json

Matched fleet numbers are as filed, sometimes from older updates, not an independent
current fleet audit. Unknown fleet size is left unknown, never converted into zero.
Known national/franchise operators and brokers were not used to fill the target. Additional
rejected and contact-only candidates are in research_holds_H3-H6_2026-10-14.csv.

## Project pool and matching

The repo pull returned 96 Houston-area sites over 21 days. A 30-day pull returned 137.
The final pool has **20 sites with an ACTIVE matching TXR15 authorization, a usable street
address and a geocoded point**, each record re-opened during research. This is a screened
pool, not a claim to cover every construction site in the metro.

The reported date comes from **affil_begin_dt**, the record's affiliation date. It is not
an independently verified authorization issue date, filed construction start, actual start
or proof that a hauling contract is available. The data source does not establish those.

scripts/build_packet.py produced the pairs from scratch inputs. The original script was
not modified. Its batch labels were changed from its default H1 to the required H3-H6 in
the delivery files. Geography used Census address matching, an ArcGIS address fallback for
high-confidence street/point matches, and public service-city reference points. Person-like
business/site flags were reviewed; obvious business/facility names were distinguished from
individuals. Sites naming individuals were excluded.

**Operating yards were not confirmed.** The matching reference is a city within the
advertised metro/county coverage, sometimes broader than an individually named service
city. Mileage is straight-line from that reference, not yard mileage or a route estimate.
The original yard-mileage CSV field is blank. The added service-city mileage field and each
packet's column heading state what was calculated. The matching audit records the points.

Each pair is the nearest still-unused eligible site for its batch's reference and screened
coverage. Earlier rows can consume a closer site. Published narrow coverage was respected:
Montgomery specialists receive the Montgomery record; Texas Roll Off receives an Alvin
record; Texas Rolloff Dumpster Rentals receives a Spring record; Rollin Dirty is not given
Houston city; Toss and Haul receives an eastern-metro record. Exact service to every street,
delivery radius, current capacity and pricing are not verified.

Each batch has 15 distinct RNs. Records may repeat across different batches, as AGENTS.md
permits. This is not exclusivity. Ridgelake Cove is filed as clearing/grubbing; its final
end use is unverified and is flagged, rather than represented as a verified vertical build.

## Specific review flags

| Account | Unresolved item |
|---|---|
| PEM Dumpster Rentals | Matching historical carrier record is inactive; current carrier unverified. Site also publishes singular/plural mailbox variants; needs email pass. |
| Buck Waste | Matching carrier record is inactive; current operating carrier unverified. |
| Instant Solutions | Published mailbox matches an inactive historical carrier record; current operating carrier unverified; needs email pass. |
| Union Dumpster & Rentals | Phone-only inactive registry match was not accepted as identity proof; operating carrier remains unverified; needs email pass. |
| In-Laws Dumpsters | Own-site phone occurs in multiple unrelated carrier records; those were not treated as its fleet or identity; needs email pass. |
| AJ Foyt Roll Offs | Own site names Mid-Tex Environmental as current operator, while multiple active carrier records use the brand; verify current operating entity. One account only. |
| Dolly's Dumpsters of Houston | Published local services/address/email found; independent ownership and container ownership not independently confirmed. Review before copy. |
| Precision Dumpsters LLC | Own-site local rental services and email found; independent ownership and fleet not independently confirmed. Review before copy. |
| Mr. Niceday's / Houston Rolling Restrooms | Narrower fit: construction restroom trailers, not a claim they rent standalone porta potties. |

Independent ownership elsewhere is based on public business/site evidence, including
self-reported local/family operation where stated; no complete corporate ownership audit
was done. Source grade A and a zero-flag duplicate check do not resolve these limitations.

## Legacy-record warning found during research

These older-source records were **not used** in the new packets:

| Record | Authorization | Status returned by the public source |
|---|---|---|
| RN102271178, Central Office Annex | TXR154490 | CANCELLED |
| RN106116676, BMC | TXR15RS92 | EXPIRED |
| RN112328034, Echo Park Spring | TXR1555WO | CANCELLED |

The operations reviewer should re-open the source before relying on an older hook.
No existing packet, copy, queue, tracker or send record was edited to act on this finding.

## Validation and boundaries

- check_packet.py: 0 flags on all four CSVs and all four Markdown packets; 60 rows also
  pass the combined identity check.
- Python suite: 31 tests passed.
- Code assertions: 15 distinct projects per batch, all selected authorization/date pairs
  match ACTIVE public source rows, no new-row identity conflicts, and unchanged existing statuses.
- Protected-file hashes and tracked-file checks: operations, copy, samples, tracker, DNC, results and ledger unchanged.
- CSV headers match the master list exactly for new and requalified row exports. Existing
  CSV CRLF line endings were retained; whitespace check used cr-at-eol.
- No outreach copy, sample report, draft, form submission, manifest or send was produced.

Validation details: data/validation_H3-H6_2026-10-14.json.
Source-level notes: data/hauler_verification_H3-H6_2026-10-14.csv.
