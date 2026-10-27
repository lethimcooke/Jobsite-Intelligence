# DFW1: S1 copy (DFW)

Written Oct 27, 2026 from `docs/Outreach_Copy_v2.md` (S1, Tier B) in the structure of the approved `outreach/H5_S1_Copy.md`, from `data/packet_DFW1.csv` and `outreach/DFW1_Hook_Packet.md` (15 haulers). Sender display name `DFW Jobsite Intelligence` (user, Oct 26), from sites@asterfieldgroup.com; `ops/rules.json` has no DFW sender yet, so `check_copy.py --metro DFW` can't check the signature. Filed facts (authorization, record date, site, address, county, operator) are from the TCEQ record, recased for reading; every site appears once. Job type and fit are our read. No published yards, so the close says "in your service area". Every subject is arm A.

**One wording change for the user to approve:** the DFW1 packet gives no distance for any row (no verified yard; "no distance estimate"). Instead of "It's about N miles from [city]", each fit line places the site against the areas the hauler publishes, for example "It's in Celina, one of the areas you serve" or "It's in Coppell, in the DFW metroplex you serve". The rest of the line is unchanged.

Dropped (checked Oct 27): nobody. None of the 15 is on `data/do_not_contact.csv`, logged as bounced in `data/send_ledger.csv`, or listed with a status other than `Not contacted` in `data/hauler_list_dfw.csv`. For review, not dropped: #6's site is filed as "4955 Rochelle" with the street address 4995 W Rochelle Rd; both are given as filed. Several To addresses begin with a first name or initial (#4 g.mccurry@, #10 andrew@, #11 tabatha@, #15 nathan@); names appear only in the To line, never in the copy. #15 One Stop Porta Shop has no matched public fleet count (packet flag). #13 Sunbelt and #10 Sundance also advertise brokerage or nationwide services; the match is to their local operations. Approved by the user Oct 27 ("approved all").

## 1. DFW1: FUSION WASTE & RECYCLING
- To: service@fusionwaste.com (A)
- Subject: EQT Southport, Wilmer
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, demolition, compactors, residential, 10-yd, 20-yd, 30-yd, 40-yd

```
Hi Fusion Waste & Recycling team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1512ZR) with a record date of October 7 for EQT Southport Bldg 3 and Bldg 4 at 1600 Southport Road, Wilmer in Dallas County. The operator on file is Arco Design Build Southwest.

It's in Wilmer, in the Dallas area you serve, and an industrial job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 2. DFW1: RED RIVER ROLL OFFS
- To: admin@redriverrolloffs.com (A)
- Subject: 7-Eleven, 1215 E Frontier Pkwy
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, demolition, residential

```
Hi Red River Roll Offs team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1577ZP) with a record date of October 1 for 7-Eleven 42828 at 1215 E Frontier Pkwy, Celina in Collin County. The operator on file is Schaffer Construction LLC.

It's in Celina, one of the areas you serve, and a commercial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 3. DFW1: DISCOUNT DUMPSTERS
- To: office@discountdumpstersdfw.com (A)
- Subject: Agape Baptist Church, Sachse
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, demolition, 40-yd

```
Hi Discount Dumpsters team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1506ZR) with a record date of October 6 for Agape Baptist Church at 1540 Blackburn Rd, Sachse in Dallas County. The operator on file is Fort Construction LP.

It's in Sachse, in the DFW metroplex you serve, and a church job like this is the kind your 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 4. DFW1: WEONIT WASTE & RECYCLE LLC
- To: g.mccurry@weonit.net (A)
- Subject: Presbyterian Village North
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 10-yd, 20-yd, 30-yd, 40-yd

```
Hi WeOnIt Waste & Recycle team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1541ZT) with a record date of October 15 for Presbyterian Village North at 8600 Skyline Dr, Dallas in Dallas County. The operator on file is PARIC LLC.

It's in Dallas, one of the areas you serve, and a senior-living job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. DFW1: HART WASTE REMOVAL
- To: info@hartwasteremoval.com (A)
- Subject: Self-storage facility, Mesquite
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, residential, 10-yd, 15-yd, 20-yd, 30-yd

```
Hi Hart Waste Removal team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1549ZO) with a record date of September 28 for Proposed Self-Storage Facility at 5201 Northwest Drive, Mesquite in Dallas County. The operator on file is Reliable Paving Inc.

It's in Mesquite, in the Dallas area you serve, and a self-storage job like this is the kind your 10- to 30-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 6. DFW1: BLUE STAR DUMPSTERS LLC
- To: info@bluestardumpsters.com (A)
- Subject: 4955 Rochelle, Irving
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, residential, 20-yd, 30-yd

```
Hi Blue Star Dumpsters team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1558ZP) with a record date of October 1 for 4955 Rochelle at 4995 W Rochelle Rd, Irving in Dallas County. The operator on file is Alliance Industrial Builders LP.

It's in Irving, in the Dallas area you serve, and an industrial job like this is the kind your 20- to 30-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 7. DFW1: Delta Solid Waste Management LLC
- To: info@deltawasteservices.com (A)
- Subject: Anna Buzz Center
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, 10-yd, 15-yd, 20-yd, 30-yd, 40-yd

```
Hi Delta Solid Waste Management team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1563ZQ) with a record date of October 6 for Anna Buzz Center at 1005 S Powell Pkwy, Anna in Collin County. The operator on file is PVB Contracting LLC.

It's in Anna, in the North Texas area you serve, and a commercial job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 8. DFW1: EnviroHauling Services
- To: info@envirohauling.com (A)
- Subject: Chilis Grill & Bar, Little Elm
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, compactors, 15-yd, 20-yd, 30-yd, 40-yd

```
Hi EnviroHauling Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1515ZU) with a record date of October 19 for Chilis Grill & Bar - Little Elm 1698 at 26580 E University Dr, Little Elm in Denton County. The operator on file is Venture Construction Company.

It's in Little Elm, in the DFW area you serve, and a restaurant job like this is the kind your 15- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 9. DFW1: HD Waste & Recycling
- To: service@hdwastetx.com (A)
- Subject: Naterra World HQ, Coppell
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, compactors

```
Hi HD Waste & Recycling team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1556ZR) with a record date of October 8 for Naterra World HQ - Commercial at 1525 Point West Blvd, Coppell in Dallas County. The operator on file is Crossland Construction Company Inc.

It's in Coppell, in the DFW metroplex you serve, and an office job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 10. DFW1: Sundance Disposal
- To: andrew@sundancedisposal.com (A)
- Subject: Arbrook Apartments
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, 20-yd, 30-yd, 40-yd

```
Hi Sundance Disposal team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1566ZO) with a record date of September 29 for Arbrook Apartments at 1001 E Arbrook Blvd, Arlington in Tarrant County. The operator on file is Roers General Contracting LLC.

It's in Arlington, one of the areas you serve, and an apartment job like this is the kind your 20- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 11. DFW1: Texas Elite Disposal
- To: tabatha@texaselitedisposal.com (A)
- Subject: Prosper Flex Park
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, portable toilets, hand-wash, compactors

```
Hi Texas Elite Disposal team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1548ZT) with a record date of October 16 for Prosper Flex Park - Building 1 at 621 West Prosper Trail, Prosper in Collin County. The operator on file is HBA Design Build LLC.

It's in Prosper, one of the areas you serve, and a commercial job like this is the kind your roll-off containers and portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 12. DFW1: Sweet Dumps
- To: inbox@sweetdumps.com (A)
- Subject: McKeever Grocer and Retail, Fort Worth
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, 10-yd, 20-yd, 30-yd, 40-yd

```
Hi Sweet Dumps team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1555ZR) with a record date of October 8 for N FTW McKeever Grocer and Retail at 9052 North City Dr, Fort Worth in Tarrant County. The operator on file is Reliable Paving Inc.

It's in Fort Worth, one of the areas you serve, and a commercial job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 13. DFW1: Sunbelt Disposal & Recycling
- To: sales@sunbeltdisposal.com (A)
- Subject: The Edifice at Anna
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, portable toilets, hand-wash

```
Hi Sunbelt Disposal & Recycling team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1562ZQ) with a record date of October 6 for The Edifice at Anna at 1105 S Powell Pkwy, Anna in Collin County. The operator on file is PVB Contracting LLC.

It's in Anna, in the DFW metroplex you serve, and a construction job like this is the kind your roll-off containers and portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 14. DFW1: Waste Advantage
- To: dispatch@wasteadvantagetx.com (A)
- Subject: 7Brew Coffee McKinney
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: roll-off, construction, commercial, compactors

```
Hi Waste Advantage team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1530ZQ) with a record date of October 5 for 7Brew Coffee McKinney at 8701 Eldorado Pkwy, McKinney in Collin County. The operator on file is Schaffer Construction LLC.

It's in McKinney, in the DFW metroplex you serve, and a commercial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 15. DFW1: One Stop Porta Shop
- To: nathan@onestopportashop.com (A)
- Subject: EQT Airparq 820, Fort Worth
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000
- Hauler publishes: portable toilets, construction, commercial, restroom trailers, hand-wash

```
Hi One Stop Porta Shop team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1548ZQ) with a record date of October 5 for EQT Airparq 820 at 3950 Angle Ave, Fort Worth in Tarrant County. The operator on file is Arco Design Build Southwest.

It's in Fort Worth, one of the areas you serve, and an industrial job like this is the kind your portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```
