# Operations handoff (Nov 4, 2026, 2:00 PM CT)

Start here in a new session. The tracker (`Jobsite_Intelligence_Outreach_Tracker.md`) is the full record; this is the short version.

## State
- 150 cold sends to 76 Houston haulers since Oct 14. 1 reply (Renegade Roll-Offs). 5 hard bounces (3.3%, over the 2% gate): Dumpster in the Rough, Quickwaste, Dolly's Dumpsters, Missouri City Porta Potty and Dumpster Conroe (the last two Nov 4, "554 Relay access denied", addresses that passed the live-site and MX recheck), all on `data/do_not_contact.csv`.
- Nov 4's 15 logged; its manifest draft deleted.
- **Thu Nov 5 manifest built, not in Gmail yet** (`ops/manifests/2026-11-05.json`, 15 follow-ups: H3 S5 #4, 5, 7-14; H5 S2 #13-15; H6 S2 #1-2; drafts created and verified). Create the Gmail draft only after the user's OK, before 8 AM CT Thursday. No first emails planned: the user decides whether to resume them (verify addresses first).
- Queues in `ops/queue/`; held: `JI-H5-S2-hold.json` (#12 Nation Waste, held for the user), `JI-H3-S5-hold.json` (#15 Trash Hauling Fast, due Nov 10), `JI-H7-H10-S1.json` #5-14 (first emails, deferred). H7-H10 S2 copy, when converted, must skip #1 and #4 (bounced). LJP Hauling (H6 #14) skipped.
## Engaged
- **Renegade Roll-Offs (Erin):** sample sent Oct 30 (from operations@ by mistake). E2 check-in sent by the user Nov 4, 7:04 AM CT from sites@ (Sent 1a1a6a969e4310cb); no reply from her since Oct 29. E3 (pilot offer) due Nov 6 if no answer; needs a Stripe payment link first (not made yet).

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
