# Operations handoff (Nov 3, 2026, 7:20 PM CT)

Start here in a new session. The tracker (`Jobsite_Intelligence_Outreach_Tracker.md`) is the full record; this is the short version.

## State
- 135 cold sends to 71 Houston haulers since Oct 14. 1 reply (Renegade Roll-Offs). 3 hard bounces (2.2%): Dumpster in the Rough, Quickwaste, Dolly's Dumpsters, all on `data/do_not_contact.csv`.
- **Wed Nov 4 manifest is in Gmail** (draft r5790912484525468717, 15 emails: H6 S1 #15, H7-H10 S1 #1-4, S5 to H2 #12-18 and H3 #1-3). It sends Wednesday morning. Log it at Wednesday's check-in.
- Queues in `ops/queue/`; held: `JI-H5-S2-hold.json` (H5 S2 #12-15, release when due), Nation Waste (H5 S1 #12, held for the user), LJP Hauling (H6 S1 #14, skipped: address gone from its site).

## Engaged
- **Renegade Roll-Offs (Erin):** sample sent Oct 30 (from operations@ by mistake). E2 check-in is drafted in her thread (r7286572832928906880); the user sends it Nov 4 from sites@ if she hasn't replied. E3 (pilot offer) due Nov 6 if no answer; needs a Stripe payment link first (not made yet).

## Daily loop (per `ops/README.md`)
1. Check replies and bounces (Gmail, sites@ and operations@).
2. Log the day's sends from the Sent folder (`ji_ops.py evidence`, `log --apply`), delete the spent manifest draft.
3. Plan the next day: up to 5 S1 (recheck each address on the live site + MX), follow-ups oldest first, 15 total. Validate, draft, record-draft, build manifest.
4. Create the manifest Gmail draft only after the user's OK. Verify its body is identical to the manifest.
5. Tracker, commit, push to main (user OK'd pushes Nov 2).

## Rules learned
- Samples: the **report creator builds**, operations reviews (`jobsite-report/Report_Creator_Brief.md`).
- Copy: the copywriter writes (`outreach/Copywriter_Brief_2026-10-27.md`); all current batches have S1, S2, S5 approved.
- Manifests go stale after 36 hours and send only on their date: build the afternoon before, OK before 8 AM CT.
- Two of three bounces were addresses published on the hauler's own site; the user has signed up for verifiers (MillionVerifier, NeverBounce, Emailable). Verify first-email addresses when possible.

## Open for the user
- Stripe payment link (before Renegade's E3).
- Nation Waste: send, drop or verify.
- Codex: DFW2 and DFW3 packets, plus a Houston refresh. Houston first emails run out about Nov 11.
- DFW sender ("DFW Jobsite Intelligence") with ASI by about Nov 10.
