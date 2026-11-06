# DFW3: S1 copy (DFW)

Written Nov 6, 2026 from `docs/Outreach_Copy_v2.md` (S1, Tier B) in the structure of the approved `outreach/DFW1_S1_Copy.md`, from `data/packet_DFW3.csv` (PR #21, not merged yet). Signature `DFW Jobsite Intelligence` / `Asterfield Group` / `dfwjobsite@asterfieldgroup.com` (operations, Nov 6); `ops/rules.json` has no DFW sender yet, so `check_copy.py --metro DFW` and `validate` can't pass until operations adds it. Filed facts (authorization, record date, site, location, county, operator) are from the TCEQ record in the packet, recased for reading; all five sites are new to the copy files and appear once. Job type and fit are our read. No published yards and no distances, so each fit line places the site against the areas the hauler publishes, as approved for DFW1, and the close says "in your service area". Every subject is arm A. Section numbers follow the packet rows.

Dropped (MillionVerifier, `data/verified_2026-11-06_millionverifier.csv`, per operations Nov 6: copy only for "ok" rows): #1 Trash Daddy, #2 Texas Rubbish, #3 JOTS Rentals, #7 The Dump-Sirs, #8 Rapid Removal DFW (catch_all) and #11 Metro Bin (invalid), so there are no sections 1, 2, 3, 7, 8 or 11. Checked Nov 6: none of the five is on `data/do_not_contact.csv` or in `data/send_ledger.csv`, and all five are `Not contacted` in `data/hauler_list_dfw.csv` (PR #21 branch).

**For review, not dropped:** #5's hauler name includes a first name (Benita's Roll Off Dumpsters); it is the business name on its own site, used in the greeting as with any business. #10's site, Montessori School of Excellence, uses the name of the Montessori teaching method; it is the school's filed name, not a reference to a person, but flag it if you read it otherwise. Operators Piazza Construction LLC, Jackson Construction Ltd and Andres Construction Services LLC are business names that may be built on surnames (as with the approved Randy Roan Construction Inc). #5's site name is its address and is filed as "Dr" while the street address says "Rd"; both are given as filed (as with DFW1 #6). #5 and #9 say "construction job" because neither filed name shows the job type. Three sites have no street number on file, so the copy gives the filed location in short form. The packet's dates are TCEQ affiliation-begin dates, given as the record date. #10's address begins with a name (hill@), shown only in the To line. Pending the user's approval.

## 4. DFW3: Freedom Dumpsters
- To: info@freedomdumpsterstx.com (A)
- Subject: Melissa Athletic Center
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112548292&program_code=STORM
- Hauler publishes: 15- and 20-yard roll-off dumpsters; construction and commercial

```
Hi Freedom Dumpsters team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1503ZT) with a record date of October 15 for Melissa Athletic Center, north of Champions Way and west of W FM 545, Melissa in Collin County. The operator on file is Piazza Construction LLC.

It's in Melissa, one of the areas you serve, and an athletic center job like this is the kind your 15- and 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. DFW3: Benita's Roll Off Dumpsters
- To: info@benitasrolloffdumpsters.com (A)
- Subject: 12003 E Rocky Creek Dr, Crowley
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112547070&program_code=STORM
- Hauler publishes: 14- to 20-yard roll-off dumpsters; construction and commercial

```
Hi Benita's Roll Off Dumpsters team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1544ZS) with a record date of October 13 for 12003 E Rocky Creek Dr at 12003 E Rocky Creek Rd, Crowley in Tarrant County. The operator on file is Jackson Construction Ltd.

It's in Crowley, one of the areas you serve, and a construction job like this is the kind your 14- to 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 6. DFW3: Aspen Site Rentals
- To: rental@aspensiterentals.com (A)
- Subject: Valley Creek Church
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112547534&program_code=STORM
- Hauler publishes: portable restrooms, fencing, power and site rentals for construction

```
Hi Aspen Site Rentals team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1572ZS) with a record date of October 14 for Valley Creek Church, at the southwest corner of FM 407 and Gateway Dr in Denton County. The operator on file is The Ridgemont Company.

It's in Denton County, one of the counties you serve, and a church job like this is the kind your portable restrooms and site rentals serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 9. DFW3: Dumpster Hire
- To: support@dumpsterhire.com (A)
- Subject: Emerald Lake II
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN112544416&program_code=STORM
- Hauler publishes: 11-, 15- and 20-yard roll-off containers

```
Hi Dumpster Hire team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1531ZR) with a record date of October 7 for Emerald Lake II, southwest of S Hardin Blvd and Tottenham Ct, McKinney in Collin County. The operator on file is Andres Construction Services LLC.

It's in McKinney, one of the areas you serve, and a construction job like this is the kind your 11- to 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 10. DFW3: Bluebonnet Roll Offs
- To: hill@bluebonnetrolloffs.com (A)
- Subject: Montessori School of Excellence
- Subject arm: A
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?ref_num_txt=RN111927695&program_code=STORM
- Hauler publishes: 15- and 20-yard roll-off dumpsters, rock hauling

```
Hi Bluebonnet Roll Offs team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1557ZU) with a record date of October 20 for Montessori School of Excellence, southeast of County Rd 943 and Aberavon St, McKinney in Collin County. The operator on file is Alsal Construction Inc.

It's in McKinney, one of the areas you serve, and a school job like this is the kind your 15- and 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this in your service area, free?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```
