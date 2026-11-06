# DFW2 site repair (Nov 6, 2026)

Prospecting only. Four DFW2 haulers get new sites; every hauler field is unchanged. Rows are in `data/packet_DFW2_repair.csv` (same columns as `packet_DFW2.csv`). The copywriter updates PR #24 from these.

| DFW2 hauler | Old site (why replaced) | New site | TCEQ auth / date on file / RN | Business affiliation on file |
|---|---|---|---|---|
| Greenmark Waste Solutions | COLLINS OFFICE CONDOS, RN112540109 (may be named for a person) | ASTER PARK 3A, NW of Aster Park Trl & Coughlin Pkwy, McKinney (our read), Collin County | TXR1578ZS / 2026-10-14 / RN112547658 | PCI UTILITIES LLC |
| Parker Waste Services | EQT AIRPARQ 820, RN112542105 (also DFW1 One Stop Porta Shop) | SAGE ALEMEDA, east side of Alemeda St 0.5 mi north of Camp Bowie W Blvd, Fort Worth (our read), Tarrant County | TXR1553ZS / 2026-10-13 / RN112547245 | SAGE ALEMEDA LLC |
| Dumpster Quest DFW | PROSPER FLEX PARK - BUILDING 1, RN112549498 (also DFW1 Texas Elite Disposal) | RESTAURANT AND RETAIL BUILDING, SWC of Washington Dr and Harrison St, Melissa (our read), Collin County | TXR1557ZR / 2026-10-08 / RN112544895 | TEXAS SPARKS CONSTRUCTIONS LLC |
| D&A Waste Services | EQT SOUTHPORT BLDG 3 AND BLDG 4, RN112543889 (also DFW1 Fusion Waste & Recycling) | BROOKVIEW - MULTIFAMILY, Stonecrest Rd and Skyview Ln, Denton County (city not on record) | TXR1585ZR / 2026-10-09 / RN112545611 | CB JENI 2020 LLC |

**Checks:** all four records re-fetched from the live data.texas.gov DFW file on Nov 6 (20:05 UTC): authorization and regulated entity ACTIVE. Affiliation dates Oct 8 to Oct 14 (last 30 days). Priority 1, except Aster Park 3A, which is priority 2 (amenity, our read). None appears in any `data/packet_*.csv` (DFW1, DFW2, DFW3, H1-H13), and no two of them share a site. `python3 scripts/check_packet.py data/packet_DFW2_repair.csv` prints 0 flags.

**Names:** SAGE ALEMEDA and BROOKVIEW tripped the script's person-name flag. Both were cleared by hand. Sage is the operator's business name (SAGE ALEMEDA LLC) and Alemeda is the street. Brookview is a place name. Skipped as possible person names: RAINWATER - MULTIFAMILY, 26012 RICHARDSON RIDGE, EWING GMC, ALLSUPS, THE FERRARA RESIDENCE.

**Area matches (our read):** each hauler's own published list. Parker publishes Tarrant County (Benbrook, White Settlement, and others) plus a Fort Worth city hauler listing. Dumpster Quest lists Melissa. D&A lists Denton County and Flower Mound. Greenmark covers the DFW metroplex. Cities that the records don't give come from OpenStreetMap street lookups. Dispatch acceptance and distance are unverified. The pool is thin: only 16 recent unused priority 1-2 DFW records were left. Next pull will include records filed after Oct 30.
