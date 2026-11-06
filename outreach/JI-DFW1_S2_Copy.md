# JI-DFW1 S2 copy (DFW)

Written Oct 27 from `docs/Outreach_Copy_v2.md` (S2, business day +2, same thread) for DFW1, from `outreach/DFW1_S1_Copy.md` (same PR: each S1's subject, site and operator, unchanged). Same wording as the approved H4 S2s ("in your service area": no published yards). Signature first line `DFW Jobsite Intelligence` (user, Oct 26). Dropped: nobody (checked Oct 27 against `data/do_not_contact.csv` and `data/send_ledger.csv`). Section numbers match the S1 file. Each S2 sends only after its S1 is confirmed sent and only if the hauler hasn't replied or bounced. Approved by the user Oct 27 ("approved all").

**Nov 6 changes (operations):** DFW sends from **dfwjobsite@asterfieldgroup.com**, not sites@ (ASI confirmed the sender refuses a sites@ or dfwsites@ signature for DFW), so the third signature line of every body is now dfwjobsite@asterfieldgroup.com; nothing else in the bodies changed. MillionVerifier (`data/verified_2026-11-06_millionverifier.csv`) rated 6 rows "ok"; the other 9 are marked SKIP and must not be queued: #3 Discount Dumpsters, #4 Weonit, #6 Blue Star, #8 EnviroHauling, #9 HD Waste, #10 Sundance, #12 Sweet Dumps, #13 Sunbelt (catch_all) and #5 Hart Waste Removal (invalid). Kept: #1 Fusion, #2 Red River, #7 Delta, #11 Texas Elite, #14 Waste Advantage, #15 One Stop Porta Shop. `check_copy.py` and `validate` will flag the DFW signature until operations adds the DFW sender to `ops/rules.json`. Signature change and SKIPs pending the user's approval.

## 1. DFW1: FUSION WASTE & RECYCLING
- To: service@fusionwaste.com
- Subject: Re: EQT Southport, Wilmer

```
Hi Fusion Waste & Recycling team,

One more on EQT Southport Bldg 3 and Bldg 4: the operator on file is Arco Design Build Southwest, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 2. DFW1: RED RIVER ROLL OFFS
- To: admin@redriverrolloffs.com
- Subject: Re: 7-Eleven, 1215 E Frontier Pkwy

```
Hi Red River Roll Offs team,

One more on 7-Eleven 42828: the operator on file is Schaffer Construction LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 3. DFW1: DISCOUNT DUMPSTERS (SKIP: MillionVerifier catch_all, Nov 6)
- To: office@discountdumpstersdfw.com
- Subject: Re: Agape Baptist Church, Sachse

```
Hi Discount Dumpsters team,

One more on Agape Baptist Church: the operator on file is Fort Construction LP, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 4. DFW1: WEONIT WASTE & RECYCLE LLC (SKIP: MillionVerifier catch_all, Nov 6)
- To: g.mccurry@weonit.net
- Subject: Re: Presbyterian Village North

```
Hi WeOnIt Waste & Recycle team,

One more on Presbyterian Village North: the operator on file is PARIC LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 5. DFW1: HART WASTE REMOVAL (SKIP: MillionVerifier invalid, Nov 6)
- To: info@hartwasteremoval.com
- Subject: Re: Self-storage facility, Mesquite

```
Hi Hart Waste Removal team,

One more on Proposed Self-Storage Facility: the operator on file is Reliable Paving Inc, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 6. DFW1: BLUE STAR DUMPSTERS LLC (SKIP: MillionVerifier catch_all, Nov 6)
- To: info@bluestardumpsters.com
- Subject: Re: 4955 Rochelle, Irving

```
Hi Blue Star Dumpsters team,

One more on 4955 Rochelle: the operator on file is Alliance Industrial Builders LP, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 7. DFW1: Delta Solid Waste Management LLC
- To: info@deltawasteservices.com
- Subject: Re: Anna Buzz Center

```
Hi Delta Solid Waste Management team,

One more on Anna Buzz Center: the operator on file is PVB Contracting LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 8. DFW1: EnviroHauling Services (SKIP: MillionVerifier catch_all, Nov 6)
- To: info@envirohauling.com
- Subject: Re: Chilis Grill & Bar, Little Elm

```
Hi EnviroHauling Services team,

One more on Chilis Grill & Bar - Little Elm 1698: the operator on file is Venture Construction Company, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 9. DFW1: HD Waste & Recycling (SKIP: MillionVerifier catch_all, Nov 6)
- To: service@hdwastetx.com
- Subject: Re: Naterra World HQ, Coppell

```
Hi HD Waste & Recycling team,

One more on Naterra World HQ - Commercial: the operator on file is Crossland Construction Company Inc, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 10. DFW1: Sundance Disposal (SKIP: MillionVerifier catch_all, Nov 6)
- To: andrew@sundancedisposal.com
- Subject: Re: Arbrook Apartments

```
Hi Sundance Disposal team,

One more on Arbrook Apartments: the operator on file is Roers General Contracting LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 11. DFW1: Texas Elite Disposal
- To: tabatha@texaselitedisposal.com
- Subject: Re: Prosper Flex Park

```
Hi Texas Elite Disposal team,

One more on Prosper Flex Park - Building 1: the operator on file is HBA Design Build LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 12. DFW1: Sweet Dumps (SKIP: MillionVerifier catch_all, Nov 6)
- To: inbox@sweetdumps.com
- Subject: Re: McKeever Grocer and Retail, Fort Worth

```
Hi Sweet Dumps team,

One more on N FTW McKeever Grocer and Retail: the operator on file is Reliable Paving Inc, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 13. DFW1: Sunbelt Disposal & Recycling (SKIP: MillionVerifier catch_all, Nov 6)
- To: sales@sunbeltdisposal.com
- Subject: Re: The Edifice at Anna

```
Hi Sunbelt Disposal & Recycling team,

One more on The Edifice at Anna: the operator on file is PVB Contracting LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 14. DFW1: Waste Advantage
- To: dispatch@wasteadvantagetx.com
- Subject: Re: 7Brew Coffee McKinney

```
Hi Waste Advantage team,

One more on 7Brew Coffee McKinney: the operator on file is Schaffer Construction LLC, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## 15. DFW1: One Stop Porta Shop
- To: nathan@onestopportashop.com
- Subject: Re: EQT Airparq 820, Fort Worth

```
Hi One Stop Porta Shop team,

One more on EQT Airparq 820: the operator on file is Arco Design Build Southwest, so its main office line is the place to ask who arranges site services there; that's our read, not the filing. Each site in the sample lists that line and the TCEQ record link, so you can check it yourself.

Want the five sites in your service area?

DFW Jobsite Intelligence
Asterfield Group
dfwjobsite@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```
