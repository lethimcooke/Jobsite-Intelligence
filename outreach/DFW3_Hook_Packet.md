# Hook packet: batch DFW3

**Prepared:** November 6, 2026, by Claude (prospector role, same rules as AGENTS.md). Prospecting only. **11 first-touch haulers, all new, all Not contacted.** No copy, Gmail, queues, ledger, tracker, samples or sending actions. Target was about 15; 11 met the stricter bar (see Shortfall).

**Email (stricter bar after the Nov 4 bounces):** all 11 grade A, each exact address re-fetched on the hauler's own live page on November 6 (direct HTTP fetch, no proxy reader); page URL and timestamp recorded per row. MX looked up for every domain the same run (Google DNS-over-HTTPS) and written in `verification_notes`. Publication and MX do not prove delivery: every address is in `data/to_verify_DFW3.csv` for MillionVerifier before any first email.

**MX flags:** 1 forwarder MX: **#4 Freedom Dumpsters (Hostinger)**. 2 for review, not on the forwarder list: **#5 Benita's (Namecheap Private Email, registrar-hosted mailbox)** and **#11 Metro Bin (self-hosted MX on its own host)**. The other 8 are Google Workspace or Microsoft 365.

**Needs recheck (not counted):** Waste Warriors Inc (admin@wastewarriorsinc.com on its live page, but no published services or area; held in `data/research_holds_DFW3_2026-11-06.csv`).

**Duplicates screened:** `hauler_list_dfw.csv`, `hauler_list_houston.csv`, every `data/packet_*.csv` including codex/dfw2's `packet_DFW2.csv`, its DFW2 hauler rows and holds, `send_ledger.csv`, `do_not_contact.csv` (email and domain), `verified_*.csv`, `to_verify*.csv`, Houston research holds, and the tracker's Excluded list. Matched by company, email, domain and USDOT. No sign companies. Brokers, franchises, national haulers and out-of-area sites skipped (holds file lists 24 leads and why).

**Site facts:** `pull_noi_sites.py --metro DFW --days 30` ran unchanged on November 6 (63 sites since Oct 7, saved as `data/sites_DFW3_2026-11-06.csv`). Each selected RN was then re-fetched individually from the live data.texas.gov DFW file (19:00 to 19:01 UTC): all 11 ACTIVE (one candidate, GOOGLE DFW 1.0, came back SUSPENDED and was dropped). Priority 1, last 30 days, business operators, no person-named sites (ALLSUPS dropped as named for a founder; LANCASTER MILLS cleared, Lancaster is the city), no RN used in DFW1, DFW2 or H1-H12. Most new DFW records carry cross streets, not a street number; those are given as filed and the city is our read where the record doesn't state it.

**Dates and limits:** date on file is the TCEQ affiliation-begin date (Oct 7 to Oct 20). No claim that work has started, a vendor is unselected, or work is open for bid. Service-area matches are our read of each hauler's published list; dispatch acceptance and distance are unverified.

**Tools note:** `agent-reach` and `mcporter` are not installed in this session (setup script did not run); web reading used direct fetches and Chromium. `scripts/enrich_haulers.py` crashed on an FMCSA email with no `@`; a scratch copy with a one-line guard was used, repo script unchanged.

| # | Batch | Hauler | Email (grade) | Service reference | Publishes | Site | TCEQ auth / date on file / RN | Business affiliation on file | Miles |
|---|---|---|---|---|---|---|---|---|---|
| 1 | DFW3 | Trash Daddy Dumpsters | info@trashdaddydumpsters.com (A) | Plano (service reference) | 10- to 40-yard roll-offs | PROJECT EAGLE, LEGACY DR & PARKWOOD BLVD, PLANO, TX | TXR1542ZT / 2026-10-15 / RN112549266 | AT JV | unverified |
| 2 | DFW3 | Texas Rubbish | office@texasrubbish.com (A) | Lancaster (service reference) | 10- to 30-yard roll-offs | LANCASTER MILLS, SE OF W REDBUD LN & W MAIN ST, LANCASTER, TX | TXR1562ZT / 2026-10-16 / RN112549928 | RPM XCONSTRUCTION LLC | unverified |
| 3 | DFW3 | JOTS Rentals | info@jotsrentals.com (A) | Celina (service reference) | portable restrooms and roll-off dumpsters | GREEN MEADOWS MULTI-FAMILY PH2, FM 428, 0.5 MI WEST OF LEGACY DR, CELINA, TX | TXR1561ZR / 2026-10-08 / RN112545082 | SAGE-CELINA LLC | unverified |
| 4 | DFW3 | Freedom Dumpsters | info@freedomdumpsterstx.com (A) | Melissa (service reference) | 15- and 20-yard roll-offs | MELISSA ATHLETIC CENTER, N OF CHAMPIONS WY, W OF W FM 545, MELISSA, TX 75454 | TXR1503ZT / 2026-10-15 / RN112548292 | PIAZZA CONSTRUCTION LLC | unverified |
| 5 | DFW3 | Benita's Roll Off Dumpsters | info@benitasrolloffdumpsters.com (A) | Crowley (service reference) | 14- to 20-yard roll-offs | 12003 E ROCKY CREEK DR, 12003 E ROCKY CREEK RD, CROWLEY, TX 76036 | TXR1544ZS / 2026-10-13 / RN112547070 | JACKSON CONSTRUCTION LTD | unverified |
| 6 | DFW3 | Aspen Site Rentals | rental@aspensiterentals.com (A) | Denton County (service reference) | portable restrooms | VALLEY CREEK CHURCH, SWC OF FM 407 AND GATEWAY DR, DENTON COUNTY, TX | TXR1572ZS / 2026-10-14 / RN112547534 | THE RIDGEMONT COMPANY | unverified |
| 7 | DFW3 | The Dump-Sirs Dumpster Rental | service@thedumpsirs.com (A) | Fort Worth (service reference) | roll-off dumpsters | D2 - WESTPORT, N OF INTERMODAL PKWY & OLD BLUE MOUND RD, FORT WORTH, TX | TXR1593ZT / 2026-10-19 / RN112550413 | GRAY CONSTRUCTION INC | unverified |
| 8 | DFW3 | Rapid Removal DFW | office@rapidremovaldfw.com (A) | Frisco (service reference) | 14- to 40-yard dumpster rentals | POINT EAST INDUSTRIAL, EVERWELL LN, 0.6 MI S OF PGA PKWY, FRISCO, TX | TXR1538ZS / 2026-10-12 / RN112546882 | ARCO MURRAY NATIONAL HOLDINGS INC | unverified |
| 9 | DFW3 | Dumpster Hire | support@dumpsterhire.com (A) | McKinney (service reference) | 11- to 20-yard roll-offs | EMERALD LAKE II, SW OF S HARDIN BLVD & TOTTENHAM CT, MCKINNEY, TX | TXR1531ZR / 2026-10-07 / RN112544416 | ANDRES CONSTRUCTION SERVICES LLC | unverified |
| 10 | DFW3 | Bluebonnet Roll Offs | hill@bluebonnetrolloffs.com (A) | McKinney (service reference) | 15- and 20-yard roll-offs | MONTESSORI SCHOOL OF EXCELLENCE, SE OF COUNTY RD 943 & ABERAVON ST, MCKINNEY, TX 75071 | TXR1557ZU / 2026-10-20 / RN111927695 | ALSAL CONSTRUCTION INC | unverified |
| 11 | DFW3 | Metro Bin | info@metrobindallas.com (A) | Dallas (service reference) | 10- to 40-yard roll-offs | DA12, 1550 W MOCKINGBIRD LN, DALLAS, TX 75235 | TXR1509WB / 2026-10-08 / RN112297049 | EQUINIX LLC | unverified |

## Sources and verification

## 1. DFW3: Trash Daddy Dumpsters
- To: info@trashdaddydumpsters.com
- Email grade: A, exact address on own live page.
- Website: https://trashdaddydumpsters.com/
- Email evidence: https://trashdaddydumpsters.com/contact-us/; HTTP 200 fetched 2026-11-06T19:02:48.889302+00:00 (direct fetch).
- MX: 30 alt2.aspmx.l.google.com.; 40 alt3.aspmx.l.google.com.; 10 aspmx.l.google.com.; 20 alt1.aspmx.l.google.com.; 50 alt4.aspmx.l.google.com.; fetched same run.
- Fit: 10- to 40-yard roll-off dumpsters; construction, commercial, demolition and residential. Published area: Dallas, Fort Worth and listed DFW cities incl. Plano, Frisco, McKinney, Allen, Anna.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: PROJECT EAGLE, LEGACY DR & PARKWOOD BLVD, PLANO, TX, COLLIN County.
- TCEQ: TXR1542ZT; RN112549266; ACTIVE; affiliation date 2026-10-15; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112549266&program_code=STORM; fetched 2026-11-06.
- Area match: Published Dallas, Fort Worth and listed DFW cities incl. Plano, Frisco, McKinney, Allen, Anna; site in PLANO, COLLIN County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Plano is our read of the Legacy Dr and Parkwood Blvd intersection; the record gives cross streets only. Site also publishes an 888 number and individual staff addresses; the general info@ address is used. No FMCSA census match found by name; fleet size unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 2. DFW3: Texas Rubbish
- To: office@texasrubbish.com
- Email grade: A, exact address on own live page.
- Website: https://www.texasrubbish.com/
- Email evidence: https://www.texasrubbish.com/contact-us/; HTTP 200 fetched 2026-11-06T19:02:49.502668+00:00 (direct fetch).
- MX: 5 alt1.aspmx.l.google.com.; 10 alt3.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.; 1 aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; fetched same run.
- Fit: 10- to 30-yard roll-off dumpsters; construction and commercial. Published area: Dallas metro list incl. Lancaster, DeSoto, Cedar Hill, Dallas, Forney.
- Fleet: 5 power units as filed; USDOT 4176803.
- Site: LANCASTER MILLS, SE OF W REDBUD LN & W MAIN ST, LANCASTER, TX, DALLAS County.
- TCEQ: TXR1562ZT; RN112549928; ACTIVE; affiliation date 2026-10-16; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112549928&program_code=STORM; fetched 2026-11-06.
- Area match: Published Dallas metro list incl. Lancaster, DeSoto, Cedar Hill, Dallas, Forney; site in LANCASTER, DALLAS County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Script person-name flag on site name manually cleared: Lancaster is the city name. Lancaster city is our read of the cross streets. FMCSA USDOT 4176803 active, Dallas, 5 power units, filed email on the same domain.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 3. DFW3: JOTS Rentals
- To: info@jotsrentals.com
- Email grade: A, exact address on own live page.
- Website: https://jotsrentals.com/
- Email evidence: https://jotsrentals.com/; HTTP 200 fetched 2026-11-06T19:02:49.866090+00:00 (direct fetch).
- MX: 10 alt3.aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.; 1 aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; fetched same run.
- Fit: portable restrooms, holding tanks and 10- to 30-yard roll-off dumpsters; construction and commercial. Published area: Five Texas yards (Longview, Tyler, Kemp, Mt. Pleasant, Whitewright); service-area page lists Celina, McKinney, Prosper, Dallas.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: GREEN MEADOWS MULTI-FAMILY PH2, FM 428, 0.5 MI WEST OF LEGACY DR, CELINA, TX, DENTON County.
- TCEQ: TXR1561ZR; RN112545082; ACTIVE; affiliation date 2026-10-08; priority 1 (multifamily, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112545082&program_code=STORM; fetched 2026-11-06.
- Area match: Published Five Texas yards (Longview, Tyler, Kemp, Mt. Pleasant, Whitewright); service-area page lists Celina, McKinney, Prosper, Dallas; site in CELINA, DENTON County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Yards are outside the four DFW counties; Celina is listed on its service-area page (about 26 miles from its Whitewright yard, as it publishes). Celina is our read of the location description. Only FMCSA name match is an inactive Longview record (USDOT 427164) on a different domain; current fleet unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 4. DFW3: Freedom Dumpsters
- To: info@freedomdumpsterstx.com
- Email grade: A, exact address on own live page.
- Website: https://freedomdumpsterstx.com/
- Email evidence: https://freedomdumpsterstx.com/; HTTP 200 fetched 2026-11-06T19:02:50.763954+00:00 (direct fetch).
- MX: 10 mx2.hostinger.com.; 5 mx1.hostinger.com.; fetched same run.
- Fit: 15- and 20-yard roll-off dumpsters; construction and commercial. Published area: Grayson, Fannin and Collin counties; Melissa, Anna, McKinney, Allen, Plano listed.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: MELISSA ATHLETIC CENTER, N OF CHAMPIONS WY, W OF W FM 545, MELISSA, TX 75454, COLLIN County.
- TCEQ: TXR1503ZT; RN112548292; ACTIVE; affiliation date 2026-10-15; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112548292&program_code=STORM; fetched 2026-11-06.
- Area match: Published Grayson, Fannin and Collin counties; Melissa, Anna, McKinney, Allen, Plano listed; site in MELISSA, COLLIN County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: FORWARDER MX: Hostinger (mx1/mx2.hostinger.com). Verify before any send. No FMCSA census match found by name; fleet size unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 5. DFW3: Benita's Roll Off Dumpsters
- To: info@benitasrolloffdumpsters.com
- Email grade: A, exact address on own live page.
- Website: https://www.benitasrolloffdumpsters.com/
- Email evidence: https://www.benitasrolloffdumpsters.com/; HTTP 200 fetched 2026-11-06T19:02:51.191034+00:00 (direct fetch).
- MX: 10 mx2.privateemail.com.; 10 mx1.privateemail.com.; fetched same run.
- Fit: 14- to 20-yard roll-off dumpsters; construction and commercial. Published area: Cleburne base; listed cities incl. Crowley, Burleson, Fort Worth, Arlington, Mansfield.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: 12003 E ROCKY CREEK DR, 12003 E ROCKY CREEK RD, CROWLEY, TX 76036, TARRANT County.
- TCEQ: TXR1544ZS; RN112547070; ACTIVE; affiliation date 2026-10-13; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112547070&program_code=STORM; fetched 2026-11-06.
- Area match: Published Cleburne base; listed cities incl. Crowley, Burleson, Fort Worth, Arlington, Mansfield; site in CROWLEY, TARRANT County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: MX review: Namecheap Private Email (mx1/mx2.privateemail.com), a registrar-hosted mailbox; not on the forwarder list but registrar-linked, so verify first. Email is Cloudflare-protected on the page and was decoded. Company name is the business name. Site name on file says DR, filed street says RD. Yard in Cleburne (Johnson County), outside the four counties; Crowley is on its published list. No FMCSA match by name.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 6. DFW3: Aspen Site Rentals
- To: rental@aspensiterentals.com
- Email grade: A, exact address on own live page.
- Website: https://www.aspensiterentals.com/
- Email evidence: https://www.aspensiterentals.com/; HTTP 200 fetched 2026-11-06T19:02:51.717308+00:00 (direct fetch).
- MX: 0 aspensiterentals-com.mail.protection.outlook.com.; fetched same run.
- Fit: portable restrooms, fencing, power and site rentals for construction. Published area: 30 North Texas counties listed incl. Collin, Dallas, Denton, Tarrant.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: VALLEY CREEK CHURCH, SWC OF FM 407 AND GATEWAY DR, DENTON COUNTY, TX, DENTON County.
- TCEQ: TXR1572ZS; RN112547534; ACTIVE; affiliation date 2026-10-14; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112547534&program_code=STORM; fetched 2026-11-06.
- Area match: Published 30 North Texas counties listed incl. Collin, Dallas, Denton, Tarrant; site in DENTON County (city not on file). Area/trade match is our read; dispatch acceptance unverified.
- Notes: Record gives cross streets only; city not stated on file and not asserted. Published 18+ years in business; no FMCSA match by name; fleet size unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 7. DFW3: The Dump-Sirs Dumpster Rental
- To: service@thedumpsirs.com
- Email grade: A, exact address on own live page.
- Website: https://www.thedumpsirs.com/
- Email evidence: https://www.thedumpsirs.com/contact; HTTP 200 fetched 2026-11-06T19:02:52.299245+00:00 (direct fetch).
- MX: 0 thedumpsirs-com.mail.protection.outlook.com.; fetched same run.
- Fit: 20-yard roll-off dumpsters. Published area: Fort Worth.
- Fleet: 1 power units as filed; USDOT 4365425.
- Site: D2 - WESTPORT, N OF INTERMODAL PKWY & OLD BLUE MOUND RD, FORT WORTH, TX, DENTON County.
- TCEQ: TXR1593ZT; RN112550413; ACTIVE; affiliation date 2026-10-19; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112550413&program_code=STORM; fetched 2026-11-06.
- Area match: Published Fort Worth; site in FORT WORTH, DENTON County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Small operator: FMCSA USDOT 4365425 active, Fort Worth, 1 power unit (FMCSA filed a free-mail address; the site publishes service@ on its own domain). Thin site; published area is Fort Worth only. Fort Worth city for the site is our read of the cross streets.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 8. DFW3: Rapid Removal DFW
- To: office@rapidremovaldfw.com
- Email grade: A, exact address on own live page.
- Website: https://www.rapidremovaldfw.com/
- Email evidence: https://www.rapidremovaldfw.com/; HTTP 200 fetched 2026-11-06T19:02:52.696372+00:00 (direct fetch).
- MX: 1 aspmx.l.google.com.; 5 alt2.aspmx.l.google.com.; 10 alt4.aspmx.l.google.com.; 5 alt1.aspmx.l.google.com.; 10 alt3.aspmx.l.google.com.; fetched same run.
- Fit: 14- to 40-yard dumpster rentals, demolition, construction debris removal. Published area: Allen, Plano, Richardson, North Dallas, McKinney, Frisco and Collin and Dallas County areas.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: POINT EAST INDUSTRIAL, EVERWELL LN, 0.6 MI S OF PGA PKWY, FRISCO, TX, COLLIN County.
- TCEQ: TXR1538ZS; RN112546882; ACTIVE; affiliation date 2026-10-12; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112546882&program_code=STORM; fetched 2026-11-06.
- Area match: Published Allen, Plano, Richardson, North Dallas, McKinney, Frisco and Collin and Dallas County areas; site in FRISCO, COLLIN County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Also does junk removal and demolition; dumpster rental is published. Frisco is our read of the location description. No FMCSA match by name; fleet size unverified.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 9. DFW3: Dumpster Hire
- To: support@dumpsterhire.com
- Email grade: A, exact address on own live page.
- Website: https://www.dumpsterhire.com/
- Email evidence: https://www.dumpsterhire.com/; HTTP 200 fetched 2026-11-06T19:02:53.311319+00:00 (direct fetch).
- MX: 0 dumpsterhire-com.mail.protection.outlook.com.; fetched same run.
- Fit: 11-, 15- and 20-yard roll-off containers. Published area: Collin, Denton and Grayson counties; McKinney, Frisco, Plano, Celina listed.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: EMERALD LAKE II, SW OF S HARDIN BLVD & TOTTENHAM CT, MCKINNEY, TX, COLLIN County.
- TCEQ: TXR1531ZR; RN112544416; ACTIVE; affiliation date 2026-10-07; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112544416&program_code=STORM; fetched 2026-11-06.
- Area match: Published Collin, Denton and Grayson counties; McKinney, Frisco, Plano, Celina listed; site in MCKINNEY, COLLIN County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Residential-leaning copy (remodels, roofing, cleanouts). McKinney is our read of the cross streets. Affiliation date Oct 7 is the 30-day edge. No FMCSA match by name.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 10. DFW3: Bluebonnet Roll Offs
- To: hill@bluebonnetrolloffs.com
- Email grade: A, exact address on own live page.
- Website: https://www.bluebonnetrolloffs.com/
- Email evidence: https://www.bluebonnetrolloffs.com/contact_us/; HTTP 200 fetched 2026-11-06T19:02:53.947497+00:00 (direct fetch).
- MX: 0 bluebonnetrolloffs-com.mail.protection.outlook.com.; fetched same run.
- Fit: 15- and 20-yard roll-off dumpsters, rock hauling. Published area: Rowlett base; listed cities incl. McKinney, Princeton, Allen, Frisco, Dallas.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: MONTESSORI SCHOOL OF EXCELLENCE, SE OF COUNTY RD 943 & ABERAVON ST, MCKINNEY, TX 75071, COLLIN County.
- TCEQ: TXR1557ZU; RN111927695; ACTIVE; affiliation date 2026-10-20; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN111927695&program_code=STORM; fetched 2026-11-06.
- Area match: Published Rowlett base; listed cities incl. McKinney, Princeton, Allen, Frisco, Dallas; site in MCKINNEY, COLLIN County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: Address on the contact page uses a single name part (hill@); business mailbox on its own domain. ZIP 75071 is on the record; McKinney is our read of the ZIP. Also TXR1596QB on the same RN. No FMCSA match by name.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## 11. DFW3: Metro Bin
- To: info@metrobindallas.com
- Email grade: A, exact address on own live page.
- Website: https://metrobindallas.com/
- Email evidence: https://metrobindallas.com/; HTTP 200 fetched 2026-11-06T19:02:54.762310+00:00 (direct fetch).
- MX: 0 metrobindallas.com.; fetched same run.
- Fit: 10- to 40-yard roll-off containers; construction and commercial. Published area: Dallas and the DFW metroplex; yard in south-west Dallas as published.
- Fleet: no FMCSA census match by name; fleet unverified.
- Site: DA12, 1550 W MOCKINGBIRD LN, DALLAS, TX 75235, DALLAS County.
- TCEQ: TXR1509WB; RN112297049; ACTIVE; affiliation date 2026-10-08; priority 1 (commercial / industrial / institutional, our read).
- Live source: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112297049&program_code=STORM; fetched 2026-11-06.
- Area match: Published Dallas and the DFW metroplex; yard in south-west Dallas as published; site in DALLAS, DALLAS County. Area/trade match is our read; dispatch acceptance unverified.
- Notes: MX review: self-hosted MX (0 metrobindallas.com, the site's own host), not a known mailbox provider; verify first. Authorization TXR1509WB predates the window; the Oct 8 date is the EQUINIX LLC operator affiliation (CLUNE CONSTRUCTION COMPANY LP also on file since 2025-10-06). No FMCSA match by name.
- Limits: No independently verified yard coordinates or numeric mileage. TCEQ date is the affiliation-begin date, not an independently established original authorization issue date. Exact dispatch acceptance and mailbox delivery unverified.

## Shortfall

Most independent DFW roll-off and toilet haulers with a published business email are already in DFW1, DFW2 or the DFW2 holds. Of about 90 new leads checked today (FMCSA census, City of Dallas franchise list, Hometown Dumpster Rental directory, web search by suburb), most had no published email, a free-mail address only, no MX, or were brokers, franchises or out of area. DFW4 will work the free-mail and form-only leads through other public sources and the Dallas franchisees not yet resolved.
