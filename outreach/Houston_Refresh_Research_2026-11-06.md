# Houston refresh research: November 6, 2026

H13 delivers 8 new matched haulers, not the requested 40. H14 and H15 are not complete. The strict 30-day, unused-RN and priority 1-2 site conditions leave eight confirmed matches from the pulls below. Contacts without a compliant unused site are held separately and are not counted as packet stock. No broader date window has been authorized.

## Source coverage and actual yield

| Source | Retrieved or checked | Result and limits |
|---|---|---|
| Comptroller active sales-tax outlets, NAICS 562111, 562119, 562991, all eight requested counties | 327 outlet rows; 234 remained after initial name/alias suppression | Discovery only. Multiple outlets may represent one company. Own-site checks, not registry emails, determine inclusion. Many records are septic-only, residential collection, junk-only, government or existing aliases. |
| FMCSA active garbage/refuse carriers, eight counties | 2,053 registry rows; 382 additional unseen business-domain roots screened after broadening the name filter | 86 HTTP 200 roots, 199 HTTP 503, 82 connection failures, 8 HTTP 406, 6 HTTP 404, 1 HTTP 403. These are URL attempts, not 382 qualified haulers. Most successful pages are unrelated trucking, moving or industrial services. Arcann Waste was a useful additional lead. Registry mailboxes alone were not accepted. |
| Existing Houston fit False rows | 243 of 353 baseline master rows | Rechecked as discovery/identity references. Every existing company remains excluded under the user's any-status rule, even if its current website shows newly suitable services. No existing row changed. |
| PSAI public operator directory | 46 Texas members, all four pages; extra Houston, Conroe, Katy and Baytown filters | Texas Outhouse is an existing Gainsborough/GTX account. United Site Services and FusionSite are corporate exclusions. Rest Stop is an existing account. HAT Services is a new own-site lead; directory page alone is not email evidence. No login or contact endpoint used. |
| Requested suburb searches | All 31 named suburbs queried with Exa; 12 results requested per suburb | Initial Brave discovery hit HTTP 429; switched sources. Search results are discovery only. Each retained contact requires its own direct website fetch. Candidate URLs include national doorways and unrelated areas, which are excluded. |
| BBB and chamber listings | Discovered through targeted company/suburb searches | Used as discovery and identity references, never sole email evidence. These sources have not been exhaustively enumerated. |
| Standard Houston TCEQ script | Initial call HTTP 503 | Broader regional queries succeeded for all five source datasets. No outage was treated as proof that no sites exist. |
| TCEQ regional construction records | 85 current-window Houston-area sites, October 7 to November 6 | 32 initially classified priority 1-2 and unused. Manual scope review removes single-family homebuilding, utilities, roads, an individual-named property, and uncertain construction locations. OREM RD is promoted because the filed description explicitly says commercial business-park buildings. |
| EPA ICIS construction permits | 68 Houston-area permits with original issue October 7 to November 6 | Six authorizations absent from the affiliation-date pull. Two add qualifying sites: Porter High School phase III and Steel Supply processing center. The others are subdivision, road or flood-control work. EPA status lag is not used for ACTIVE status; each selected authorization is checked live on TCEQ. |

The full site disposition is in `data/houston_refresh_site_screen_2026-11-06.csv`. Five initially eligible unused sites, OREM RD and two EPA-discovered authorizations produce the eight H13 hooks. North Houston Commerce Park is held because original issue date is unverified. Physical emergency staging facilities are distinguished from utility-line work; Sawgrass is filed as an emergency staging yard. The CenterPoint Pine Island record is excluded because its filed scope says detention basin for future development.

## Important exclusions and holds

| Candidate or brand | Disposition |
|---|---|
| EnviroLink | Own site identifies Trash Hauling Fast as a related operating brand, already in the master. One business, not a new prospect. |
| Gainsborough / GTX / Texas Outhouse | Existing account linked by published GTX-domain email. |
| RMI Emergency Services | Own site identifies former Moffitt brand; existing account. |
| Heritage Sanitation | Own contact page routes to Doodie Calls; corporate/acquired network. |
| DWC Dumpsters | Own contact links existing Dennis Williams & Co account. |
| MS Roll Offs | Own coverage is Houston County/Anderson County, not Houston metro. |
| Peninsula Septic | Exact own-site email found, but actual MX lookup returned no MX. Held, not counted. |
| Sima Roll Off, Haul Day Long | Direct site unavailable or hosting placeholder. Needs recheck; no reader-only result counted. |
| Loads2Go, First Response Dumpster Rentals, Eagle Can, 2S Rolloff, Nexus Disposal | Suitable service leads but no qualifying own-site email found on the pages checked; forms were not submitted. |
| American On-Site, Tambo and nationwide city-doorway networks | Broker/national partner-network indicators; excluded. |
| Dump Hero and Qwk Dumps | Dump-trailer rental, not verified roll-off or portable-toilet service. Held rather than broaden the target. |
| LUX Trailer Rental | Restroom-trailer email is published, but checked pages emphasize events and do not establish construction service. Held for fit. |
| Payless Waste Solutions, CBR Industrial | Own-site services are grease/lint/grit traps or industrial contracting, not the requested rental services. |
| K2 Dumpster Rental, Onsite Pro Can, Toss It Dumpsters | Own coverage is outside Houston metro. |
| Generic .site/.store operators | Email/MX alone does not prove independent equipment ownership. Ownership/operator identity needs corroboration before counting. Forwarder MX is flagged when detected, not treated as mailbox verification. |

## Verification and claims limits

- H13: eight direct own-site grade A emails, seven business-domain and one business Gmail. Zero forwarder MX flags and zero needs-recheck emails included. Gmail retains needs email pass.
- The exact page URL, fetch timestamp, SHA256 and actual DNS response are saved in `data/h13_verification_2026-11-06.json`.
- Publication and MX cannot establish acceptance, catch-all behavior or inbox delivery. MillionVerifier is pending. No SMTP probes, test sends or contacts occurred.
- Eight original issue dates are corroborated by the public EPA archive. Live TCEQ RN and authorization status is ACTIVE for every selected site. Exact entrances, dispatch availability, beneficial ownership and unfiled/current fleet totals remain unverified.
- No existing master rows or outreach statuses were changed. No copy, queues, ledger, samples, tracker or sending files were edited.

## Checks

```
python3 scripts/check_packet.py data/packet_H13.csv
0 flags (8 rows checked)

python3 -m unittest discover -s tests
Ran 31 tests
OK
```
