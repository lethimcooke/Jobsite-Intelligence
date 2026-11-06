# Operations handoff (Nov 5, 2026, 2:15 PM CT)

Start here in a new session. The tracker (`Jobsite_Intelligence_Outreach_Tracker.md`) is the full record; this is the short version.

## State
- 165 cold sends to 76 Houston haulers since Oct 14. 1 reply (Renegade Roll-Offs). 5 hard bounces (3.0%, over the 2% gate): Dumpster in the Rough, Quickwaste, Dolly's Dumpsters, Missouri City Porta Potty, Dumpster Conroe, all on `data/do_not_contact.csv`.
- Nov 5's 15 logged; its manifest draft deleted.
- **Fri Nov 6 manifest is in Gmail** (draft r4547905190791005644, user OK Nov 5; `ops/manifests/2026-11-06.json`, 15 = 5 S1 (Old Glory, Goldmine, Houston Luxury Restrooms, Smooth Move, Texas Gulf Recycling) + 10 S2 (H6 #3-6, 8, 10-13, 15); drafts created).
- **First emails resume Fri Nov 6, verified only** (MillionVerifier, Nov 4: `data/verified_2026-11-04_millionverifier.csv`). Of the 11 ok: 5 planned for Fri Nov 6; Trash Monkey (H7-H10 #10) and J.A.C. (H11 #2) skipped Nov 5 (address gone from their sites); left: Turbo Rolloff (H11 #8, address not on its homepage at the Nov 5 check: recheck its contact page), 786 Dumpsters (H11 #9, on its site Nov 5), K & H (H12 #2), Waste Solutions USA (H12 #4). 12 skipped (2 invalid: Action Trucking, Katy Dumpster Rental Group; 10 catch_all, including Nation Waste, now dropped). Any new first-email address gets verified first; only `ok` is sent. These run out Mon Nov 9: Codex's Houston refresh (verified) is needed.
- Held: `JI-H3-S5-hold.json` (#15 Trash Hauling Fast, due Nov 10). H7-H10 S2 copy, when converted, must skip every S1 that wasn't sent (#1 and #4 bounced; #5-9, 12, 14 skipped). LJP Hauling (H6 #14) skipped.
## Prospect surplus plan (user, Nov 6)
- Goal: a two-week buffer of verified first emails so every weekday has 5 first emails plus follow-ups. Cap stays 5 a day while bounces are over 2%.
- **One combined verification upload (user, Nov 6):** hold `to_verify_2026-11-06_DFW.csv` (30) and `to_verify_2026-11-06_Houston.csv` (21, H13 PR #20 + reserves); when the prospector's DFW3 PR lands (due Sun Nov 8), review it and send the user ONE CSV with all of them plus DFW3 and any Codex H14. If DFW3 is late, send it Sunday evening without DFW3. Results are needed by Mon noon so Monday's check-in can plan Tuesday's first emails.
- Verification stays manual: operations sends the user a CSV per batch, the user runs MillionVerifier and sends back the report; only `ok` is queued, and each address is rechecked on the live site at planning.
- DFW starts as soon as its sender exists: ASI confirmed Nov 6: alias **dfwjobsite@asterfieldgroup.com** ("DFW Jobsite Intelligence"; dfwsites@ would collide with sites@), no sender code change; added to `ops/rules.json` (and the manifest test) once the alias exists. Waiting on: the user creates and verifies the alias in Gmail; the copywriter changes DFW signatures to it and writes DFW2 copy; then a dry-run test manifest. DFW1 + DFW2 (PR #19, reviewed: 0 flags, tests pass, no overlaps; waits for the user's OK to merge) sent to the user for verification: `data/to_verify_2026-11-06_DFW.csv` (30).
- Prospecting: Codex owns Houston (H13-H16, 60 haulers, H13 by Sun Nov 8). +JSI PROSPECTOR (session_01YEUMDsoi5W5ZHL7V6QZ2MB, created Nov 6) owns DFW (DFW3 by Nov 8, DFW4 by Nov 11). Both deliver a to_verify CSV per packet.

## Engaged
- **Renegade Roll-Offs (Erin):** sample sent Oct 30 (from operations@ by mistake). E2 check-in sent by the user Nov 4, 7:04 AM CT from sites@ (Sent 1a1a6a969e4310cb); no reply from her since Oct 29. E3 (pilot offer) drafted in her thread (r5801946320233686263); the user sends it Fri Nov 6 from sites@ if she hasn't replied. Payment link only after a yes (user, Nov 4).

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
- Stripe payment link: only once a hauler says yes (user, Nov 4).
- Codex: DFW2 and DFW3 packets, plus a Houston refresh. Houston first emails run out about Nov 11.
- DFW sender ("DFW Jobsite Intelligence") with ASI by about Nov 10.
