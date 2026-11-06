# DFW2: S1 copy (DFW)

Written Nov 6, 2026 from `docs/Outreach_Copy_v2.md` (S1, Tier B) in the structure of the approved `outreach/DFW1_S1_Copy.md`, from `data/packet_DFW2.csv` (Codex, PR #19, not merged yet). Signature `DFW Jobsite Intelligence` / `Asterfield Group` / `dfwjobsite@asterfieldgroup.com` (operations, Nov 6); `ops/rules.json` has no DFW sender yet, so `check_copy.py --metro DFW` and `validate` can't pass until operations adds it. Filed facts (authorization, record date, site, address, county, operator) are from the TCEQ record in the packet, recased for reading (the same recasing as DFW1 for shared sites). Job type and fit are our read. No published yards and no distances, so each fit line places the site against the areas the hauler publishes, as approved for DFW1, and the close says "in your service area". Every subject is arm A. Section numbers follow the packet rows.

Dropped (MillionVerifier, `data/verified_2026-11-06_millionverifier.csv`, per operations Nov 6: copy only for "ok" rows): #3 ABCDump, #4 Iron Eagle, #8 Cowtown, #9 Bosman, #15 U Dump It I Take It (catch_all), #6 MCK, #10 Ranger Waste (invalid) and #12 Open Top Waste (unknown), so there are no sections 3, 4, 6, 8, 9, 10, 12 or 15. Checked Nov 6: none of the seven is on `data/do_not_contact.csv` or in `data/send_ledger.csv`, and all seven are `Not contacted` in `data/hauler_list_dfw.csv` (PR #19 branch).

**For review, not dropped:** five of the seven sites are also DFW1 sites. Each appears once in this batch, and the H3-H6 batches already shared sites across batches. Three of those DFW1 haulers are still kept, so the same site would reach two haulers: #2 Parker (EQT Airparq 820, also DFW1 #15 One Stop Porta Shop, a toilet company), #5 Dumpster Quest (Prosper Flex Park, also DFW1 #11 Texas Elite, roll-offs and toilets in the same area) and #7 D&A (EQT Southport, also DFW1 #1 Fusion, roll-offs in the same area). The approved "same sites to competitors" reply covers this; swap #5 and #7 if you'd rather not send the same roll-off site twice. #13 and #14's sites were DFW1's #3 and #4, both now SKIP, so no overlap is sent. #11's site name is its street address and the operator is a utility and infrastructure contractor (MasTec), so "commercial job" is our loosest read here. The packet's dates are TCEQ affiliation-begin dates, given as the record date. Named mailboxes (#5 jonathan@, #13 david@) appear only in the To line; greetings use the business. #13 DFW Toilets bills through Texas Johns per its own pages (packet note); treated as one prospect. #2's email domain (parkerwaste.com) differs from its website (parkerwasteservices.com); the address is published on its own site. **HOLD #1 Greenmark Waste Solutions:** its only packet site, Collins Office Condos, may be named after a person (Collins is a common surname), and the brief says to flag such a site and not use it. Its copy is written in full so it can go if the user confirms the name is not a person's, or swapped for another site from the prospector; until then don't queue it. Six emails are ready per stage. Pending the user's approval.

## 1. DFW2: Greenmark Waste Solutions (HOLD: site name may be a person's surname; needs the user's OK or another site)
- To: customerservice@greenmarkwaste.com (A)
- Subject: Collins Office Condos
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-19%27&%24limit=10000
- Hauler publishes: 15- to 40-yard roll-offs and portable restrooms

```
Hi Greenmark Waste Solutions team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1568ZP) with a record date of October 1 for Collins Office Condos at 110 and 112 Clay Road, Sunnyvale in Dallas County. The operator on file is BQ Construction Inc.

It's in Sunnyvale, in the DFW metroplex you serve, and an office job like this is the kind your 15- to 40-yard roll-offs and portable restrooms serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 2. DFW2: Parker Waste Services
- To: info@parkerwaste.com (A)
- Subject: EQT Airparq 820, Fort Worth
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112542105&program_code=STORM
- Hauler publishes: roll-off dumpster rentals

```
Hi Parker Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1548ZQ) with a record date of October 5 for EQT Airparq 820 at 3950 Angle Ave, Fort Worth in Tarrant County. The operator on file is Arco Design Build Southwest.

It's in Fort Worth, in Tarrant County, one of the counties you serve, and an industrial job like this is the kind your roll-off dumpsters serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. DFW2: Dumpster Quest DFW
- To: jonathan@dumpsterquestdfw.com (A)
- Subject: Prosper Flex Park
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112549498&program_code=STORM
- Hauler publishes: 20-yard roll-off dumpster rentals

```
Hi Dumpster Quest DFW team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1548ZT) with a record date of October 16 for Prosper Flex Park - Building 1 at 621 West Prosper Trail, Prosper in Collin County. The operator on file is HBA Design Build LLC.

It's in Prosper, one of the areas you serve, and a commercial job like this is the kind your 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 7. DFW2: D&A Waste Services
- To: info@dandawaste.com (A)
- Subject: EQT Southport, Wilmer
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112543889&program_code=STORM
- Hauler publishes: 10-, 20-, 30-, 35- and 40-yard roll-off dumpsters

```
Hi D&A Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1512ZR) with a record date of October 7 for EQT Southport Bldg 3 and Bldg 4 at 1600 Southport Road, Wilmer in Dallas County. The operator on file is Arco Design Build Southwest.

It's in Wilmer, in Dallas County, one of the areas you serve, and an industrial job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

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
