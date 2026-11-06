# JI-DFW1 S5 copy (DFW)

Written Oct 27 from `docs/Outreach_Copy_v2.md` (S5, business day +13, same thread) in the structure of the approved `outreach/JI-H1_S5_Copy.md`, for DFW1, from the approved `outreach/DFW1_S1_Copy.md`. Subjects are "Re: " plus the exact S1 subject (the same subjects as the approved S2 file). These haulers have no published yard, so the wording is "in your service area". Signature first line `DFW Jobsite Intelligence` (user, Oct 26), as in the approved DFW1 S1 and S2. Dropped: nobody. Checked Oct 27: none is on `data/do_not_contact.csv`, logged as bounced in `data/send_ledger.csv`, or marked as replied in `data/outreach_results.csv`. Section numbers match the S1 file. Due S1 + 13 business days from each hauler's S1 send date. Each S5 sends only if the hauler hasn't replied, bounced or opted out by then; re-check before queueing. Approved by the user Oct 28 ("Approved").

**Nov 6 changes (operations):** DFW sends from **dfwjobsite@asterfieldgroup.com**, not sites@ (ASI confirmed the sender refuses a sites@ or dfwsites@ signature for DFW), so the third signature line of every body is now dfwjobsite@asterfieldgroup.com; nothing else in the bodies changed. MillionVerifier (`data/verified_2026-11-06_millionverifier.csv`) rated 6 rows "ok"; the other 9 are marked SKIP and must not be queued: #3 Discount Dumpsters, #4 Weonit, #6 Blue Star, #8 EnviroHauling, #9 HD Waste, #10 Sundance, #12 Sweet Dumps, #13 Sunbelt (catch_all) and #5 Hart Waste Removal (invalid). Kept: #1 Fusion, #2 Red River, #7 Delta, #11 Texas Elite, #14 Waste Advantage, #15 One Stop Porta Shop. `check_copy.py` and `validate` will flag the DFW signature until operations adds the DFW sender to `ops/rules.json`. Signature change and SKIPs pending the user's approval.

## 1. DFW1: FUSION WASTE & RECYCLING
- To: service@fusionwaste.com
- Subject: Re: EQT Southport, Wilmer
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Fusion Waste & Recycling team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 2. DFW1: RED RIVER ROLL OFFS
- To: admin@redriverrolloffs.com
- Subject: Re: 7-Eleven, 1215 E Frontier Pkwy
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Red River Roll Offs team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 3. DFW1: DISCOUNT DUMPSTERS (SKIP: MillionVerifier catch_all, Nov 6)
- To: office@discountdumpstersdfw.com
- Subject: Re: Agape Baptist Church, Sachse
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Discount Dumpsters team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 4. DFW1: WEONIT WASTE & RECYCLE LLC (SKIP: MillionVerifier catch_all, Nov 6)
- To: g.mccurry@weonit.net
- Subject: Re: Presbyterian Village North
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi WeOnIt Waste & Recycle team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. DFW1: HART WASTE REMOVAL (SKIP: MillionVerifier invalid, Nov 6)
- To: info@hartwasteremoval.com
- Subject: Re: Self-storage facility, Mesquite
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Hart Waste Removal team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 6. DFW1: BLUE STAR DUMPSTERS LLC (SKIP: MillionVerifier catch_all, Nov 6)
- To: info@bluestardumpsters.com
- Subject: Re: 4955 Rochelle, Irving
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Blue Star Dumpsters team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 7. DFW1: Delta Solid Waste Management LLC
- To: info@deltawasteservices.com
- Subject: Re: Anna Buzz Center
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Delta Solid Waste Management team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 8. DFW1: EnviroHauling Services (SKIP: MillionVerifier catch_all, Nov 6)
- To: info@envirohauling.com
- Subject: Re: Chilis Grill & Bar, Little Elm
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi EnviroHauling Services team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 9. DFW1: HD Waste & Recycling (SKIP: MillionVerifier catch_all, Nov 6)
- To: service@hdwastetx.com
- Subject: Re: Naterra World HQ, Coppell
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi HD Waste & Recycling team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 10. DFW1: Sundance Disposal (SKIP: MillionVerifier catch_all, Nov 6)
- To: andrew@sundancedisposal.com
- Subject: Re: Arbrook Apartments
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Sundance Disposal team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 11. DFW1: Texas Elite Disposal
- To: tabatha@texaselitedisposal.com
- Subject: Re: Prosper Flex Park
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Texas Elite Disposal team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 12. DFW1: Sweet Dumps (SKIP: MillionVerifier catch_all, Nov 6)
- To: inbox@sweetdumps.com
- Subject: Re: McKeever Grocer and Retail, Fort Worth
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Sweet Dumps team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 13. DFW1: Sunbelt Disposal & Recycling (SKIP: MillionVerifier catch_all, Nov 6)
- To: sales@sunbeltdisposal.com
- Subject: Re: The Edifice at Anna
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Sunbelt Disposal & Recycling team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 14. DFW1: Waste Advantage
- To: dispatch@wasteadvantagetx.com
- Subject: Re: 7Brew Coffee McKinney
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi Waste Advantage team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 15. DFW1: One Stop Porta Shop
- To: nathan@onestopportashop.com
- Subject: Re: EQT Airparq 820, Fort Worth
- Site record: https://data.texas.gov/resource/t34q-qzi3.json?%24where=program_code%3D%27STORM%27+AND+affil_begin_dt+%3E%3D+%272026-09-26%27&%24limit=10000

```
Hi One Stop Porta Shop team,

Last note from me on this. If new job sites in your service area are ever useful, reply "send it" and the five-site sample will be in your inbox the same day.

Should I check back in a few months?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```
