# Copywriter brief: all outstanding Jobsite Intelligence copy (Oct 27, 2026)

You are the copywriter for Jobsite Intelligence (repo lethimcooke/Jobsite-Intelligence). Read
`CLAUDE.md`, `docs/Outreach_Copy_v2.md` (the formulas), `ops/rules.json` (what the validator
enforces) and the approved examples below before writing anything. You write copy files only: no
Gmail, no queues, no tracker, no ledger, no list statuses, nothing that sends.

## Deliver in this order (the operator needs each by the date shown, 1 PM CT)

| # | File to write | Haulers | Stage | Needed by | Source |
|---|---|---|---|---|---|
| 1 | `outreach/JI-H5_S2_Copy.md` | H5 #1, 3-15 (14; #2 Precision is SKIP) | S2 | **Wed Oct 28** | `outreach/H5_S1_Copy.md` (each S1's subject, site, operator) |
| 2 | `outreach/H6_S1_Copy.md` | H6 (15) | S1 | **Thu Oct 29** | `data/packet_H6.csv`, `outreach/H6_Hook_Packet.md` |
| 3 | `outreach/JI-H6_S2_Copy.md` | H6 (15) | S2 | Mon Nov 2 | your H6 S1 |
| 4 | `outreach/JI-H3_S5_Copy.md` | H3 #1-5, 7-15 (14; #6 bounced) | S5 | Mon Nov 2 | `outreach/H3_S1_Copy.md`, `outreach/JI-H3_S2_Copy.md`, `outreach/JI-H3_S2_Copy_15.md` |
| 5 | `outreach/H7-H10_S1_Copy.md` and `outreach/JI-H7-H10_S2_Copy.md` | H7, H8, H9, H10 (14) | S1, S2 | Tue Nov 3 | `data/packet_H7.csv` ... `H10.csv` and their hook packets |
| 6 | `outreach/H11_S1_Copy.md`, `outreach/H12_S1_Copy.md` and their S2 files | H11 (8; Throne Ranger stays out), H12 (4) | S1, S2 | Thu Nov 5 | `data/packet_H11.csv`, `data/packet_H12.csv` |
| 7 | `outreach/JI-H4_S5_Copy.md` | H4 #1-7, 9-12, 14, 15 (13; #8 PEM skipped, #13 Quickwaste bounced) | S5 | Fri Nov 6 | `outreach/H4_S1_Copy.md`, `outreach/JI-H4_S2_Copy.md` |
| 8 | `outreach/DFW1_S1_Copy.md` and `outreach/JI-DFW1_S2_Copy.md` | DFW1 (15) | S1, S2 | Fri Nov 6 | `data/packet_DFW1.csv`, `outreach/DFW1_Hook_Packet.md` |
| 9 | `outreach/JI-H5_S5_Copy.md`, then S5 for H6 onward | | S5 | Nov 10 onward | |

Before writing each row, drop any hauler that is now on `data/do_not_contact.csv`, has a status
other than `Not contacted` in its list (for S1), or is in `data/send_ledger.csv` as bounced.
Say in the file's header who you dropped and why.

## Formulas (copy exactly; only the bracketed parts change)

Copy the structure of these approved files, which already passed review:
- S1: `outreach/H5_S1_Copy.md` (no published yard: "It's about N miles from [service-area city],
  one of the areas you serve, and a [job type] job like this is the kind your [their published
  equipment] serve; that's our read, not the filing."; close "Want five sites like this in your
  service area, free?"). If the packet gives a real published yard, use the H1-H2 "near your yard"
  wording from `docs/Outreach_Copy_v2.md` instead.
- S2: `outreach/JI-H4_S2_Copy.md` ("One more on [site]: the operator on file is [operator], so its
  main office line is the place to ask who arranges site services there; that's our read, not the
  filing. Each site in the sample lists that line and the TCEQ record link, so you can check it
  yourself." then "Want the five sites in your service area?"). Subject: "Re: " + the exact S1
  subject.
- S5: `outreach/JI-H1_S5_Copy.md` ("Last note from me on this. If new job sites [near your <city>
  yard / in your service area] are ever useful, reply "send it" and the five-site sample will be in
  your inbox the same day." then "Should I check back in a few months?"). Subject: "Re: " + the
  exact S1 subject.

Every body ends with the three-line signature, a blank line, then the opt-out line:

```
Houston Jobsite Intelligence
Asterfield Group
sites@asterfieldgroup.com

If this isn't useful, reply "no thanks" and I won't email again.
```

DFW1 only: the first signature line is `DFW Jobsite Intelligence` (user, Oct 26). The validator
does not know that name yet, so `check_copy.py --metro DFW` will flag the signature; note that in
the PR and change nothing else to make it pass.

S1 price line, word for word (en dash between 15 and 20):
`The sample costs nothing; after it, our 30-day pilot is a one-time $500 for 15–20 verified projects, with no subscription.`

## Hard rules

- No em dashes anywhere. No calls offered or mentioned.
- Business names only. Never a person's name, in a greeting, a site name or anywhere else. Greet
  "Hi [Company] team,". A site named after a person: flag it, don't use it.
- Every fact (authorization ID, record date, site, address, county, operator) comes from the TCEQ
  record in the packet, recased for reading. Job type, fit and distance are labeled as our read.
- Never say or imply that work has started, that a vendor is unselected, or that work is open for
  bid. None of the phrases in `ops/rules.json` `banned_phrases`.
- Use the record date as "a record date of [Month D]"; never call it an issue or approval date.
- One site per hauler per batch; don't reuse a site already used for another hauler in the same
  batch.
- Never use team@claimcascade.com.

## File format (the operator converts these mechanically, so keep it exact)

One header paragraph (what it is, source files, who was dropped and why, "Pending the user's
approval."), then per hauler:

````
## N. H6: Company Name
- To: email@example.com
- Subject: Site Name, Street

```
Hi Company team,
...body, signature, blank line, opt-out line...
```
````

S1 entries also carry the `- Subject arm: A`, `- Site record:` and `- Hauler publishes:` lines,
as in `outreach/H5_S1_Copy.md`.

## Check, then deliver

- `python3 scripts/check_copy.py --metro Houston --stage S1 outreach/H6_S1_Copy.md` (use the right
  stage per file) must print PASS for every Houston file.
- `python3 -m unittest discover -s tests` must still pass.
- Work on a branch `copy/<short-topic>` and open one PR to `main` per row above (rows 5 and 6 can
  share a PR). Don't push to main. The PR lists each file, the hauler count, anyone dropped and
  why, and the check output. The user approves the copy; the operator merges and queues it.
