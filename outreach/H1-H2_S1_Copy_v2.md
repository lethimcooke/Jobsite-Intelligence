# H1 to H2: S1 copy v2 (Houston)
Written October 14, 2026 from `docs/Outreach_Copy_v2.md` (S1, Tier B). Same 19 haulers and sites as `outreach/H1-H2_S1_Copy.md`; every filed fact (authorization, date, site, address, county, operator) is unchanged from `data/packet_H1-H2.csv`, recased for reading. Distance, job type and fit are our read. Sender: Houston Jobsite Intelligence <sites@asterfieldgroup.com>.

**Subject A/B test:** rows alternate A (`[Site name]`, plus the street when the name is under 10 characters) and B (`Job site [N] miles from your yard`), skipping HOLD rows, so each send day carries both arms. Log the arm with the send.

**Not ready to send:** the `[MAILING ADDRESS]` footer line is still pending from the user and must be added under the opt-out line in every body before drafting. Two rows are on HOLD (see the row notes). Before drafting: re-open each site's source URL, confirm the hauler's site still lists the services named, run the ASI conflict check, and run `check_copy.py`.

## 1. H1: City Waste LP
- To: sales@city-waste.com (A)
- Subject (A): Central Office Annex
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN102271178&program_code=STORM
- Hauler publishes: roll-off, commercial, compactors

```
Hi City Waste team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR154490) dated September 24 for Central Office Annex at 1617 Lauder Rd, Houston in Harris County. The operator on file is Nupi Americas Inc.

It's about 7 miles from your Houston yard, and an industrial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 2. H1: Rapid Waste Solutions of Texas LLC
- To: info@rapidwastesolutions.com (A)
- Subject (B): Job site 11 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN100705680&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, portable toilets, restroom trailers, hand-wash, demolition, compactors, residential, 20-yd, 30-yd, 40-yd

```
Hi Rapid Waste Solutions of Texas team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1573ZR) dated October 8 for BJ Services Tomball at 11211 FM 2920 Rd, Tomball in Harris County. The operator on file is ICI Construction Inc.

It's about 11 miles from your Hockley yard, and an industrial job like this is the kind your 20- to 40-yard roll-offs and portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 3. H1: Buiza Waste
- To: customerservice@buizawaste.com (A)
- Subject (A): Fifth Third Bank Shops at Katy
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112540703&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential

```
Hi Buiza Waste team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1591ZP) dated October 2 for Fifth Third Bank Shops at Katy at 1720 Spring Green Blvd, Katy in Fort Bend County. The operator on file is The Fifth Third Bank.

It's about 10 miles from your Richmond yard, and a commercial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 4. H1: Texan Waste Services Inc
- To: sales@texanwasteservices.com (A)
- Subject (B): Job site 4 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112538277&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, compactors, 20-yd, 30-yd, 40-yd

```
Hi Texan Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1577ZO) dated September 29 for Rockefeller Axis 290 at 6995 Brittmoore Rd, Houston in Harris County. The operator on file is Burton Construction Co.

It's about 4 miles from your Houston yard, and an industrial job like this is the kind your 20- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. H1: Waste Shrink LLC
- To: info@wasteshrink.com (A)
- Subject (A): BMC, 7355 West Rd
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN106116676&program_code=STORM
- Hauler publishes: roll-off, construction, commercial

```
Hi Waste Shrink team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR15RS92) dated October 2 for BMC at 7355 West Rd, Houston in Harris County. The operator on file is BFS Group LLC.

It's about 6 miles from your Houston yard, and an industrial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 6. H1: Red Dog Dumpsters LLC (HOLD)
- To: info@reddogdumpsters.com (A)
- Subject (none): Project Wildcat
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112539986&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 10-yd, 15-yd, 20-yd
- HOLD: reddogdumpsters.com is a Nashville, Tennessee company; FMCSA puts this yard at 1100 Brittmoore Rd, Houston (record updated 2019). The fit line came from the Nashville site. Confirm it's the same business and what it publishes before sending.

```
Hi Red Dog Dumpsters team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1563ZP) dated October 1 for Project Wildcat at 222 Holmes Rd, Houston in Harris County. The operator on file is FCL Builders Texas LLC.

It's about 12 miles from your Houston yard, and a construction job like this is the kind your 10- to 20-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 7. H1: Baker Waste Services LLC
- To: dbaker@bwsdumpsters.com (A)
- Subject (B): Job site 6 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN110638913&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, residential, 30-yd, 40-yd

```
Hi Baker Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1523XC) dated September 24 for Hoelscher Weatherstrip Manufacturing at 2400 S Persimmon St, Tomball in Harris County. The operator on file is Hoelscher Weatherstrip Manufacturing Co Inc.

It's about 6 miles from your Spring yard, and an industrial job like this is the kind your 30- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 8. H1: Texas Modern Waste LLC
- To: robby@texasmodernwaste.com (A)
- Subject (A): Teadit North America Inc-Manufacturing Facility
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN106881923&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 20-yd, 30-yd, 40-yd

```
Hi Texas Modern Waste team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1518ZN) dated September 23 for Teadit North America Inc-Manufacturing Facility at 10545 Red Bluff Rd, Pasadena in Harris County. The operator on file is FCL Builders Texas LLC.

It's about 19 miles from your Baytown yard, and an industrial job like this is the kind your 20- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 9. H1: Security Waste LLC
- To: admin@ofssolidwaste.com (A)
- Subject (B): Job site 18 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112546411&program_code=STORM
- Hauler publishes: roll-off, commercial, residential, 20-yd, 30-yd, 40-yd

```
Hi Security Waste team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1515ZS) dated October 12 for HLSR 288 at 9950 South Fwy, Houston in Harris County. The operator on file is Clay Development & Construction Inc.

It's about 18 miles from your Channelview yard, and a construction job like this is the kind your 20- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 10. H1: EZ Waste Inc
- To: bgonzalez@ezwasteinc.com (B-dir)
- Subject (A): Infrastructure Services
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN101903235&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 10-yd, 20-yd, 30-yd, 40-yd

```
Hi EZ Waste team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1512ZQ) dated October 5 for Infrastructure Services at 711 Rankin Rd, Houston in Harris County. The operator on file is Cannon Construction Company Inc.

It's about 15 miles from your Houston yard, and a construction job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 11. H2: Astro Waste Inc
- To: info@astrowaste.com (B-dir)
- Subject (B): Job site a mile from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112538277&program_code=STORM
- Hauler publishes: roll-off, construction, commercial

```
Hi Astro Waste team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1577ZO) dated September 29 for Rockefeller Axis 290 at 6995 Brittmoore Rd, Houston in Harris County. The operator on file is Burton Construction Co.

It's about a mile from your Houston yard, and an industrial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 12. H2: Moffitt Site Services LLC
- To: carlk@moffittservices.com (B-dir)
- Subject (A): Hoelscher Weatherstrip Manufacturing
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN110638913&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, portable toilets, hand-wash, demolition, residential

```
Hi Moffitt Site Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1523XC) dated September 24 for Hoelscher Weatherstrip Manufacturing at 2400 S Persimmon St, Tomball in Harris County. The operator on file is Hoelscher Weatherstrip Manufacturing Co Inc.

It's about 11 miles from your Cypress yard, and an industrial job like this is the kind your roll-off containers and portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 13. H2: OP Enterprises Waste Services
- To: services@opewasteservices.com (B-dir)
- Subject (B): Job site 4 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112546411&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, portable toilets, restroom trailers, hand-wash, residential
- Recheck by hand: the hauler's website blocked our reader on Oct 14, so its services weren't reconfirmed.

```
Hi OP Enterprises Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1515ZS) dated October 12 for HLSR 288 at 9950 South Fwy, Houston in Harris County. The operator on file is Clay Development & Construction Inc.

It's about 4 miles from your Houston yard, and a construction job like this is the kind your roll-off containers and portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 14. H2: Jet Waste Services LP
- To: slencina@jetwaste.com (B-dir)
- Subject (A): BMC, 7355 West Rd
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN106116676&program_code=STORM
- Hauler publishes: roll-off, commercial, residential

```
Hi Jet Waste Services team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR15RS92) dated October 2 for BMC at 7355 West Rd, Houston in Harris County. The operator on file is BFS Group LLC.

It's about 6 miles from your Houston yard, and an industrial job like this is the kind your roll-off containers serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 15. H2: Sustainable Disposal Bins LLC
- To: customersupport@sustainablebins.com (B-dir)
- Subject (B): Job site 15 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112540117&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 10-yd, 20-yd, 30-yd, 40-yd

```
Hi Sustainable Disposal Bins team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1569ZP) dated October 1 for TNMP Alvin Construction Center at 1157 Fox Meadow Dr, Alvin in Brazoria County. The operator on file is Texas-New Mexico Power Company.

It's about 15 miles from your Rosharon yard, and a commercial job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 16. H2: Z Sites
- To: bryan.k@zsites.com (B-dir)
- Subject (A): BJ Services Tomball
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN100705680&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, portable toilets, residential, 40-yd

```
Hi Z Sites team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1573ZR) dated October 8 for BJ Services Tomball at 11211 FM 2920 Rd, Tomball in Harris County. The operator on file is ICI Construction Inc.

It's about 7 miles from your Pinehurst yard, and an industrial job like this is the kind your 40-yard roll-offs and portable toilets serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 17. H2: Hercules Dumpster Rentals LLC
- To: office@herculeswaste.com (B-dir)
- Subject (B): Job site 11 miles from your yard
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN106881923&program_code=STORM
- Hauler publishes: roll-off, construction, demolition, 10-yd, 15-yd, 20-yd, 30-yd, 40-yd
- Recheck by hand: the hauler's website blocked our reader on Oct 14, so its services weren't reconfirmed.

```
Hi Hercules Dumpster Rentals team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1518ZN) dated September 23 for Teadit North America Inc-Manufacturing Facility at 10545 Red Bluff Rd, Pasadena in Harris County. The operator on file is FCL Builders Texas LLC.

It's about 11 miles from your Dickinson yard, and an industrial job like this is the kind your 10- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 18. H2: Essential Waste Solutions LLC
- To: luisg@essential-waste.com (B-dir)
- Subject (A): Fifth Third Bank Shops at Katy
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN112540703&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 20-yd, 30-yd, 40-yd

```
Hi Essential Waste Solutions team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1591ZP) dated October 2 for Fifth Third Bank Shops at Katy at 1720 Spring Green Blvd, Katy in Fort Bend County. The operator on file is The Fifth Third Bank.

It's about 8 miles from your Houston yard, and a commercial job like this is the kind your 20- to 40-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 19. H2: Waste Falcon LLC (HOLD)
- To: nick@wastefalcon.com (B-dir)
- Subject (none): Infrastructure Services
- Site record: https://data.texas.gov/resource/tzyg-j7q4.json?ref_num_txt=RN101903235&program_code=STORM
- Hauler publishes: roll-off, construction, commercial, demolition, residential, 10-yd, 15-yd, 20-yd, 30-yd
- HOLD: wastefalcon.com lists College Station, Bryan and Navasota as its service area; FMCSA puts the yard in Cypress. Confirm it serves Houston before sending.

```
Hi Waste Falcon team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1512ZQ) dated October 5 for Infrastructure Services at 711 Rankin Rd, Houston in Harris County. The operator on file is Cannon Construction Company Inc.

It's about 13 miles from your Cypress yard, and a construction job like this is the kind your 10- to 30-yard roll-offs serve; that's our read, not the filing.

We're a research service with no tie to the project. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want five sites like this near your yard, free?

Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```
