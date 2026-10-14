# Jobsite Intelligence: outreach copy v1

Draft, October 14, 2026. Built on ASI's `Outreach_Copy_v2.md` formulas, adjusted for haulers.
Fixed terms are the same as ASI: free five-site sample, then a one-time $500 30-day pilot for
15–20 verified projects, with no subscription, no auto-renew and no refund. No calls. No em dashes.
No person's name. The price line goes in every S1, word for word.

**Signature (Austin; other metros swap city and alias):**
```
Austin Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com
```
Every cold email (S1, S2, S5) ends with: `If this isn't useful, reply "no thanks" and I won't email again.`

## What changes from ASI

- **No Tier A.** No public record names a hauler at a job site, so the "your own recent job"
  line doesn't exist. Instead the fit line uses two checkable details from the hauler's own
  website or sales-tax record: **the distance from its yard** and **what it publishes**
  (container sizes, commercial or construction service, toilets, washout). Label it our read.
- **The fact is a TCEQ record, not a project.** Say "TCEQ's Central Registry lists a construction
  stormwater authorization (TXR15xxxx) dated [date] for [site name] at [address or filed
  location]; the operator on file is [business]." Never say work has started.
- **Pick commercial sites.** Commercial, industrial, institutional and amenity sites first.
  Skip national-homebuilder subdivisions, utility lines and roads unless the hauler publishes
  that kind of work.

## S1 (Day 1)

**Template:**
```
Subject: [Site name], [street or area]

Hi [Company] team,

TCEQ's Central Registry lists a construction stormwater authorization ([TXR15 number]) dated [Month Day] for [site name] at [address or filed location] in [County] County. The operator on file is [operator business]. It's about [N] miles from your [city] yard, and a [commercial / industrial] site like this is the kind of job your [published containers or services] serve; that's our read, not the filing.

We're a research service with no connection to the project: each week we pull new construction sites from state records and match them to haulers by service area. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want the free five-site sample?

[Signature]

If this isn't useful, reply "no thanks" and I won't email again.
```

**Filled example (facts from the record pulled Oct 13; re-check and run the conflict check before any real send):**
```
Subject: Westlake Court Business Center, Bee Cave Road

Hi [Company] team,

TCEQ's Central Registry lists a construction stormwater authorization (TXR1526ZS) dated October 12 for Westlake Court Business Center at 910 Beaver Trail and 3663 Bee Cave Road in Travis County. The operator on file is Capital Constructors Group LLC. It's about [9] miles from your [Oak Hill] yard, and a commercial site like this is the kind of job your 20- and 30-yard roll-offs serve; that's our read, not the filing.

We're a research service with no connection to the project: each week we pull new construction sites from state records and match them to haulers by service area. The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.

Want the free five-site sample?

Austin Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

## S2 (Day 3, same thread)

```
Hi [Company] team,

One more detail on [site name]: the same record lists [second operator, or the industry filed, or the filed location]. Sites like this usually run roll-offs from the vertical phase through finish-out; that's our read, not the filing.

We're a research service, not a broker; the sample is five sites like this one near your yard.

Want the free sample?

[Signature]

If this isn't useful, reply "no thanks" and I won't email again.
```

## S5 (Day 14, same thread)

```
Hi [Company] team,

Last note from me on this. If you ever want five current construction sites near your yard, free, reply "send it" and they'll be in your inbox the same day.

Should I check back in a few months?

[Signature]

If this isn't useful, reply "no thanks" and I won't email again.
```

## E1: the sample is attached

```
Hi [first name or Company team],

Thanks for the reply. The sample is attached: five construction sites within [N] miles of your [city] yard, picked for your [published services].

Start with #1, [site name] at [location]. TCEQ lists authorization [TXR15 number] dated [date], with [operator] as the operator on file. Our read is it fits your [container sizes / toilets], and each site lists the filed facts, our read of the jobsite needs and the operator's main line as the first call.

These five are a snapshot. In our 30-day pilot, a fresh list like this arrives every week, 15–20 sites in all, filtered to the areas you cover. It's a one-time $500, with no subscription.

Is #1 a site your team would go after?

[Signature]
```

## E3: the pilot offer

```
Hi [first name or Company team],

Since [#n / the site they named] looked worth a call, here's how to get more like it.

For the next 30 days we send 15–20 verified construction sites in your service area over four weekly lists, filtered to [their containers or services]. Each one comes with the filed facts, our read of the jobsite needs and the first number to call.

It's a one-time $500: no subscription, no renewal, and it ends on its own. A single site that runs roll-offs for a few months covers it many times over.

Reply "yes" and I'll send the payment link; the first list goes out within a week.

Should I send the link?

[Signature]
```
No dollar range for a site until one is sourced (ASI rule). The haul prices found so far
($285–850 a haul) are background, not copy.

## Check before every send

- The validator (`ops/rules.json`) passes: price line exact, signature, footer, banned phrases.
- No person's name anywhere, including the site name (the pull script flags suspect site names).
- The hauler isn't in ASI's lists or do-not-contact file; the site isn't in an ASI packet or sample.
- The distance and services in the fit line come from the hauler's own site or sales-tax record.
