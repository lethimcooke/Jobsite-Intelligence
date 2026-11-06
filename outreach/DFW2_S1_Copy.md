# DFW2: S1 copy (DFW)

Written Nov 6, 2026 from `docs/Outreach_Copy_v2.md` (S1, Tier B) in the structure of the approved `outreach/DFW1_S1_Copy.md`, from `data/packet_DFW2.csv` (Codex, PR #19, not merged yet), with #1, #2, #5 and #7 from `data/packet_DFW2_repair.csv` (PR #26). Signature `DFW Jobsite Intelligence` / `Asterfield Group` / `dfwjobsite@asterfieldgroup.com` (operations, Nov 6); `ops/rules.json` has no DFW sender yet, so `check_copy.py --metro DFW` and `validate` can't pass until operations adds it. Filed facts (authorization, record date, site, address, county, operator) are from the TCEQ record in the packet, recased for reading . Job type and fit are our read. No published yards and no distances, so each fit line places the site against the areas the hauler publishes, as approved for DFW1, and the close says "in your service area". Every subject is arm A. Section numbers follow the packet rows.

Dropped (MillionVerifier, `data/verified_2026-11-06_millionverifier.csv`, per operations Nov 6: copy only for "ok" rows): #3 ABCDump, #4 Iron Eagle, #8 Cowtown, #9 Bosman, #15 U Dump It I Take It (catch_all), #6 MCK, #10 Ranger Waste (invalid) and #12 Open Top Waste (unknown), so there are no sections 3, 4, 6, 8, 9, 10, 12 or 15. Checked Nov 6: none of the seven is on `data/do_not_contact.csv` or in `data/send_ledger.csv`, and all seven are `Not contacted` in `data/hauler_list_dfw.csv` (PR #19 branch).

**Site repair (Nov 6, PR #26, `data/packet_DFW2_repair.csv`):** #1, #2, #5 and #7 now use new sites from the prospector, replacing Collins Office Condos (possibly named for a person) and three sites shared with live DFW1 haulers (EQT Airparq 820, Prosper Flex Park, EQT Southport). The four new sites are in no other packet or copy file. None of the four records gives a city, so the fact line gives the filed location and county only; the city in the fit line (McKinney, Fort Worth, Melissa) is our read of the cross streets (prospector, from OpenStreetMap). #7 names no city, only Denton County. #2 and #7 tripped the prospector script's person-name check; cleared by the prospector (Sage Alemeda is the operator's business name and the street; Brookview is a place name). **For review, not dropped:** #7's operator, CB Jeni 2020 LLC, is a business name that may include a first name (as with the approved Randy Roan Construction Inc). #2's job type isn't filed, so it says "construction job". #13 and #14's sites were DFW1's #3 and #4, both now SKIP, so no overlap is sent. #11's site name is its street address and the operator is a utility and infrastructure contractor (MasTec), so "commercial job" is our loosest read here. The packet's dates are TCEQ affiliation-begin dates, given as the record date. Named mailboxes (#5 jonathan@, #13 david@) appear only in the To line; greetings use the business. #13 DFW Toilets bills through Texas Johns per its own pages (packet note); treated as one prospect. #2's email domain (parkerwaste.com) differs from its website (parkerwasteservices.com); the address is published on its own site. Pending the user's approval.

## 1. DFW2: Greenmark Waste Solutions
- To: customerservice@greenmarkwaste.com (A)
- Subject: Aster Park 3A
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112547658&program_code=STORM
- Hauler publishes: 15- to 40-yard roll-offs and portable restrooms

```
Hi Greenmark Waste Solutions team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1578ZS) with a record date of October 14 for Aster Park 3A, northwest of Aster Park Trl and Coughlin Pkwy in Collin County. The operator on file is PCI Utilities LLC.

It's in McKinney, in the DFW metroplex you serve, and an amenity job like this is the kind your 15- to 40-yard roll-offs and portable restrooms serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 2. DFW2: Parker Waste Services
- To: info@parkerwaste.com (A)
- Subject: Sage Alemeda
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112547245&program_code=STORM
- Hauler publishes: roll-off dumpster rentals

```
Hi Parker Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1553ZS) with a record date of October 13 for Sage Alemeda, on the east side of Alemeda St 0.5 miles north of Camp Bowie W Blvd in Tarrant County. The operator on file is Sage Alemeda LLC.

It's in Fort Worth, in Tarrant County, one of the counties you serve, and a construction job like this is the kind your roll-off dumpsters serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. DFW2: Dumpster Quest DFW
- To: jonathan@dumpsterquestdfw.com (A)
- Subject: Restaurant and Retail Building
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112544895&program_code=STORM
- Hauler publishes: 20-yard roll-off dumpster rentals

```
Hi Dumpster Quest DFW team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1557ZR) with a record date of October 8 for a Restaurant and Retail Building at the southwest corner of Washington Dr and Harrison St in Collin County. The operator on file is Texas Sparks Constructions LLC.

It's in Melissa, one of the areas you serve, and a restaurant and retail job like this is the kind your 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 7. DFW2: D&A Waste Services
- To: info@dandawaste.com (A)
- Subject: Brookview - Multifamily
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112545611&program_code=STORM
- Hauler publishes: 10-, 20-, 30-, 35- and 40-yard roll-off dumpsters

```
Hi D&A Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1585ZR) with a record date of October 9 for Brookview - Multifamily, at Stonecrest Rd and Skyview Ln in Denton County. The operator on file is CB Jeni 2020 LLC.

It's in Denton County, one of the areas you serve, and a multifamily job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 11. DFW2: Blue Giant Dumpsters
- To: info@bluegiantdumpsters.com (A)
- Subject: 2050 Forum Parkway, Bedford
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112525647&program_code=STORM
- Hauler publishes: roll-off dumpster rentals for contractors and commercial customers

```
Hi Blue Giant Dumpsters team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1572ZJ) with a record date of October 6 for 2050 Forum Parkway, Bedford in Tarrant County. The operator on file is MasTec North America Inc.

It's in Bedford, one of the areas you serve, and a commercial job like this is the kind your roll-off dumpsters serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 13. DFW2: DFW Toilets
- To: david@dfwtoilets.com (A)
- Subject: Agape Baptist Church, Sachse
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112543590&program_code=STORM
- Hauler publishes: portable toilets, hand-washing stations and restroom trailers

```
Hi DFW Toilets team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1506ZR) with a record date of October 6 for Agape Baptist Church at 1540 Blackburn Rd, Sachse in Dallas County. The operator on file is Fort Construction LP.

It's in Sachse, in the DFW area you serve, and a church job like this is the kind your portable toilets and hand-washing stations serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 14. DFW2: Unique Waste Disposal
- To: info@uniquewastedisposal.com (A)
- Subject: Presbyterian Village North
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=ref_num_txt%3D%27RN102990561%27+AND+program_code%3D%27STORM%27&%24limit=500
- Hauler publishes: 20-, 30- and 40-yard roll-off containers

```
Hi Unique Waste Disposal team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1541ZT) with a record date of October 15 for Presbyterian Village North at 8600 Skyline Dr, Dallas in Dallas County. The operator on file is PARIC LLC.

It's in Dallas, the area you serve, and a senior-living job like this is the kind your 20- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```
