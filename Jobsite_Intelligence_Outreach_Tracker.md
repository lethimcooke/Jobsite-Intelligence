# Jobsite Intelligence: Outreach Tracker

Started October 14, 2026. The source of truth for standing rules, sends and engaged prospects.
`ops/rules.json` follows this file (change both in the same commit). Daily loop: `ops/README.md`.

## Standing rules (user decisions)

- **Offer:** free five-site sample, then a one-time $500 30-day pilot for 15-20 verified projects,
  no subscription, no auto-renew, no refund. The price goes in every S1 with the standard line.
- **Sender (Oct 14):** `sites@asterfieldgroup.com`, display "[City] Jobsite Intelligence". Houston only
  for now. Full three-line signature on every email:
  `Houston Jobsite Intelligence` / `Asterfield Group` / `sites@asterfieldgroup.com`.
- **Sending (Oct 14):** the ASI Sender (Apps Script in the user's Gmail, owned by the Austin-Signage repo)
  sends only S1, S2 and S5 drafts listed in that day's validated manifest. Engaged replies (E1-E3) are
  drafted for the user, labeled `JI/Send manually`, and sent by the user from sites@.
- **Pace (user, Oct 15; replaces Oct 14's "no separate first-email cap"):** the operations@ mailbox sends at
  most 60 a day across both businesses; Jobsite's share is 15, ASI's 45. Each first email brings two
  follow-ups, so Jobsite adds at most **5 new first emails a day** (ASI 15). First emails still go first;
  follow-ups fill the rest, oldest first; the rest wait a day. Oct 16 is unchanged (15 first emails already on
  the manifest); the cap starts Mon Oct 19, which is follow-ups only. From Tue Oct 20: 5 first emails, then
  follow-ups.
- **Ramp (user, Oct 15, option 1):** the shared total rises about 10 a week, only if the previous 5 sending
  days had hard bounces under 2% of sends, no spam complaint or block notice, and no sender auto-pause:

  | From | Mailbox total | Jobsite share | Jobsite first emails |
  |---|---|---|---|
  | Oct 19 | 60 | 15 | 5 |
  | Oct 26 | 70 | 18 | 6 |
  | Nov 2 | 80 | 20 | 6 |
  | Nov 9 | 90 | 23 | 7 |
  | Nov 16 | 100 | 25 | 8 |

  On each step day change `max_total_per_day`, `daily_share` and `max_s1_per_day` in `ops/rules.json`
  together, and only after the user confirms the gate held. ASI changes its total the same day (the sender
  uses the lowest total across the day's manifests; if the two disagree, the lower wins). Jobsite reports its
  bounce count every Friday.
- **Sequence:** S1, S2 (+2 business days), S5 (+13). Any reply freezes the cold sequence.
- **One company, one business:** a company emailed by ASI is never cold-emailed by Jobsite, and the reverse.
  The sender enforces it at send time; a skip for that reason means drop the company here.
- **Copy:** `docs/Outreach_Copy_v2.md`. No em dashes, no individuals named, no calls offered, every claim
  cites the TCEQ record, our read is labeled. Never say construction started, a hauler or vendor is
  unselected, or work is open for bid.
- **Payment:** Stripe Payment Link by default; Stripe invoice if the buyer asks; first list within a week of
  payment. Product "Jobsite Intelligence 30-day pilot, $500" in the same Asterfield Stripe account as ASI,
  kept separate so revenue splits by business. **Link: PENDING; the user creates it when either business (ASI or Jobsite) secures its first pilot payment (user, Oct 14).** Send it only after a
  hauler says yes to the E3, never in S1 or E1.
- **Prospecting (user, Oct 14):** Codex prospects (see `AGENTS.md`) to save Claude Code usage; Claude reviews its PRs with `check_packet.py` before merging.
- **Sample report:** `jobsite-report/`, one per hauler, built the same day as a "send it" reply.
- **Opt-out footer** on every cold email; opt-outs honored the same day and added to `data/do_not_contact.csv`.
- **Mailing address (user, Oct 14): skipped.** The user decided to send without a postal address line in the
  footer (CAN-SPAM requires one in commercial email; risk accepted by the user). `ops/rules.json`
  `footer.address` stays empty until the user gives an address.

## Gmail lane

Shared mailbox with ASI. Jobsite touches only sites@ threads, drafts in its own queues, its own manifest
draft and `JI/` labels. Labels (created Oct 14): `JI/Send manually` (Label_6), `JI/Do not send` (Label_7).

## Batches

| Batch | Metro | Copy file | Rows | Status |
|---|---|---|---|---|
| JI-H1 | Houston | outreach/H1-H2_S1_Copy_v2.md (H1) | 10: City Waste sent Oct 14 (v1 text), Red Dog SKIP, 8 queued | Validate PASS for 2026-10-15; planned Oct 15: all 8. 8 drafted Oct 14, listed in the Oct 15 manifest |
| JI-H2 | Houston | outreach/H1-H2_S1_Copy_v2.md (H2) | 9: Waste Falcon SKIP, 8 queued | Validate PASS for 2026-10-15; planned Oct 15: 7; 7 drafted Oct 14, listed in the Oct 15 manifest; deferred to Oct 16: Essential Waste Solutions |
| JI-H3 | Houston | `outreach/H3_S1_Copy.md` (approved by the user Oct 15) | 15 | Validate PASS for 2026-10-16; planned Oct 16: 14 (drafted Oct 15, in the Oct 16 manifest); deferred: Trash Hauling Fast (#15) |
| JI-H11 to JI-H12 | Houston | prospects only: `outreach/H11_Hook_Packet.md`, `H12` (Codex, PR 4, merged Oct 21) | 13 (H11 9, H12 4) | Reviewed: `check_packet.py` 0 flags each; 4 rows appended, no existing row changed. Every email on the hauler's live site with MX. Notes for copy: Throne Ranger (H11) is exploratory, construction fit unverified: hold it; named mailboxes (wendy@, cindy@): greet the business; no city-reference mileage in these rows, so S1s state no distance; The Vic at Sunterra has a TCEQ/TABS address discrepancy. |
| JI-H7 to JI-H10 | Houston | prospects only: `outreach/H7_Hook_Packet.md` to `H10` (Codex, PR 3, merged Oct 20) | 14 (H7 4, H8 4, H9 3, H10 3) plus 10 unverified reserves (`data/verified_reserve_H7-H10_2026-10-20.csv`, not ready for copy) | Reviewed: `check_packet.py` 0 flags each; 24 rows appended to the list, no existing row changed. Every email published on the hauler's live site with an MX record (17 business-domain, 7 free-mail across new rows). Notes for copy: greet EDCA Cleaning Services as All Dumpsters Rental (its site and domain); four addresses are named mailboxes (case@, erik@, chad@, shelley@): greet the business, never the person; three rows have no mileage (Katy Dumpster Rental Group, Old Glory, H J Services), so their S1 must not state a distance; several site addresses come from TDLR TABS filings, cited as such. Target was 60; Codex found 14 that passed the stricter checks. |
| JI-H3 to JI-H6 | Houston | prospects only: `outreach/H3_Hook_Packet.md` to `H6` (Codex, PR 2, merged Oct 15) | 60 (15 each): 52 new companies, 8 requalified list rows | Reviewed: `check_packet.py` 0 flags each. S1 copy not written yet. Notes for copy: no yard addresses, so distances are from a service city (never "from your yard", so subject arm B can't be used as written); 20 sites shared across the 60 (each once per batch); 27 free-mail addresses published on the hauler's own site; Instant Solutions marked review before copy (mailbox matches an inactive carrier record); Dennis Williams & Co: greet as the business (DW Companies), never by a person's name. |

## Plan

- **Oct 15:** 15 S1s (JI-H1 8, JI-H2 7), Jobsite's full daily share. **Oct 16:** Essential Waste Solutions S1 plus City Waste S2 (`outreach/JI-H1_S2_Copy.md`, queue `ops/queue/JI-H1-S2.json`, linked to thread 1a13ba7b4a2819dd; validate PASS for Oct 16). Drafts and the Oct 16 manifest are made on Oct 15 (a manifest goes stale after 36 hours). S2s for confirmed Oct 15 S1s are due Oct 19 (+2 business days; Oct 17 is a Saturday). Essential Waste Solutions, if sent Oct 16, reaches S2 on Oct 20. S5 (+13 business days): Nov 2, 3, 4 for S1s sent Oct 14, 15, 16.
- **Oct 16 (planned Oct 15):** 15 S1s: Essential Waste Solutions (JI-H2) plus H3 #1-14 (unchanged by the Oct 15 cap). **Mon Oct 19: follow-ups only** (user, Oct 15): the 15 S2s for the Oct 15 batch plus City Waste's S2 = 16 due; the oldest 15 go Monday, the last waits for Tuesday. **From Tue Oct 20:** 5 new first emails a day (H3 #15 Trash Hauling Fast first), then follow-ups oldest first.
- **S2 copy (user, Oct 16, "approve"):** `outreach/JI-H1_S2_Copy_b.md` (H1 #2-10) and `outreach/JI-H2_S2_Copy.md` (H2 #11-18); S5 files stay in `outreach/review/`. **Mon Oct 19 drafted Oct 16:** 15 S2s (City Waste plus 14 of the Oct 15 batch), each threaded to its S1; deferred: Hercules (Oct 20), Essential Waste (due Oct 20). Manifest `ops/manifests/2026-10-19.json` built; **its Gmail draft must be created Sun evening or Mon before 8 AM CT** (a manifest goes stale after 36 hours), after a reply check, with the user's OK.
- The A/B subject arm is in the copy file per row; log it with each send in `outreach_results.csv` notes.

## Send log

| Date | Batch | Stage | Sent | Evidence | Notes |
|---|---|---|---|---|---|
| 2026-10-14 13:32 CT | JI-H1 | S1 | 1: City Waste LP (sales@city-waste.com) | Sent 1a13bb05fcc96d4f, thread 1a13ba7b4a2819dd; `ops/evidence/2026-10-14_JI-H1.json`; queue `ops/queue/JI-H1-S1-sent-v1.json` | Sent by mistake: an ASI test manifest made while the sender was LIVE. Approved v1 text, from sites@ as Houston Jobsite Intelligence, without the mailing-address line (still pending). Kit v2 adds `dry_run_only` to every manifest so tests can't send. S2 due Oct 16. |
| 2026-10-15 08:04-09:14 CT | JI-H1 (8), JI-H2 (7) | S1 | 15 (all in the Oct 15 manifest) | `ops/evidence/2026-10-15_JI-H1-S1.json`, `ops/evidence/2026-10-15_JI-H2-S1.json`; ledger and results appended | From sites@; no bounces or replies as of 10:48 CT. S2 due Mon Oct 19 (+2 business days). |
| 2026-10-16 08:02-08:32 CT | JI-H2 (1), JI-H3 (14) | S1 | 15 of 15 logged (Essential Waste; H3 #1-14; last three logged Oct 19 from `ops/evidence/2026-10-16_JI-H3-S1_b.json`) | `ops/evidence/2026-10-16_JI-H2-S1_a.json`, `ops/evidence/2026-10-16_JI-H3-S1_a.json` (Dump Today logged in the next pass) | No bounces or replies. Friday gate report: 31 sent Oct 14-16, 0 hard bounces, 0 complaints or blocks, no sender pause. |
| 2026-10-19 12:55-14:05 CT | JI-H1 (9), JI-H2 (6) | S2 | 15 (City Waste, H1 #2-5, 7-10, H2 #11-16) | `ops/evidence/2026-10-19_JI-H1-S2_a.json`, `..._JI-H1-S2-b_a.json`, `..._JI-H1-S2-b_b.json`, `..._JI-H2-S2_b.json` | Threaded to each S1. No replies. Same day: H3 #6 S1 hard bounce logged. |
| 2026-10-22 08:03-08:35 CT | JI-H3 (1+8), JI-H4 (4), JI-H2 (2) | S1 5, S2 10 | 15 (Trash Hauling Fast, H4 #1-4; S2 Hercules, Essential Waste, H3 #1-5, 7-9) | `ops/evidence/2026-10-22_*.json` | First day after the sender pause. No replies, no bounces (checked 2:30 PM CT). |
| 2026-10-23 08:03-08:45 CT | JI-H4 (5), JI-H3 (5) | S1 5, S2 5 | 10 (Texas Rolloff Dumpster Rentals, Action Roll-Offs, Driveway Dumpster Rental, Come and Take It Dumpsters, Junk It Mobile Dumpsters; S2 H3 #10-14: Tanks A Lot, Grand Slam, Dump Today, Mr. Niceday's, RNC) | `ops/evidence/2026-10-23_*.json` | No replies, no bounces (checked 9:15 AM CT). Running total 71 sends to 41 haulers, 1 hard bounce. H4 S2 #5-10 linked to their S1 threads. |

## Engaged prospects

One row per prospect who replies. Cadence: E1 (sample attached) the same day as the reply; E2 at sample + 2
business days; E3 (pilot offer) after useful feedback or at sample + 5 business days. Any reply freezes the
silent sequence and sets list status to "Replied (...)". Every E-stage hand-off reminds the user: attach the
PDF, set From to sites@ (Oct 14: an ASI engaged email went out from operations@).

| Company | Batch | Latest event (date, time CT, their words) | Status | Required next action |
|---|---|---|---|---|

- **Tests:** any test manifest is made with `ji_ops.py manifest ... --dry-run-only`; the sender only sends from manifests marked `"dry_run_only": false`.

- **Follow-up copy (Oct 14):** H1/H2 S2 and S5 drafts for review are in `outreach/review/` (17 accounts per stage; converted queues in `ops/review/queues/`, outside the live queues). Pending the user's approval; City Waste's live S2 stays `outreach/JI-H1_S2_Copy.md`.

## Manifest drafts (the only ones Jobsite may delete)

| Send date | Draft ID | Subject |
|---|---|---|
| 2026-10-15 | r8605933855582475111 (message 1a13c9cb6e281e74, labeled JI/Do not send) | ASI-MANIFEST v1 2026-10-15 fae0d3b38062bfa462ea73fae93e63c9ab1535ebdfbe029993916ddadbe2162b (15 S1s, dry_run_only false; user approved Oct 14). **Deleted Oct 15 after its sends were logged (spent).** |
| 2026-10-16 | r8637948838471712868 (message 1a140ec80a072bdb, labeled JI/Do not send) | ASI-MANIFEST v1 2026-10-16 8885a25f89db96723edd19ca568f5473fb481175ba801d6fcc94ebe48356fce3 (15 S1s: Essential Waste + H3 #1-14, dry_run_only false; user approved Oct 15). **Deleted Oct 19 after its sends were logged (spent).** |
| 2026-10-19 | r-5077443539634189182 (message 1a1553aba09d33eb, labeled JI/Do not send) | ASI-MANIFEST v1 2026-10-19 e79e7fc66e8ccf34ace513693b046858b038f3e6e61dcd84e4b477b85981f2be (15 S2s, dry_run_only false; user approved Oct 19, created 12:35 CT)  **Deleted Oct 19 after its 15 sends were logged (spent).** |
| 2026-10-20 | r2025179972168776424 (message 1a155fed924a4c7b, labeled JI/Do not send) | ASI-MANIFEST v1 2026-10-20 575277d0b0f0e7380ce59cfb55aebfbf98bd9e9e482b775c3e7556924a770e86 (15: 5 S1 (H3 #15, H4 #1-4) + 10 S2 (Hercules, Essential Waste, H3 #1-5, 7-9); user approved Oct 19 "approve H3 S2 and go ahead"; created 4:08 PM CT) |
| 2026-10-22 | r5412951461588570780 (message 1a1600efa5014dd5; the JI/Do not send label failed: Gmail returned "caller does not have permission"; the user adds it by hand) | ASI-MANIFEST v1 2026-10-22 59e711a725300f22871e7b1b335b03c88f26c441727ac8143a2ed0ce2158b43d (15: 5 S1 (H3 #15, H4 #1-4) + 10 S2; created Oct 21 3:02 PM CT per ASI ops relayed by the user; no replies or bounces; 5 S1 addresses rechecked on live sites)  **Deleted Oct 22 after its 15 sends were logged (spent).** |
| 2026-10-23 | r619740113729683949 (message 1a16519d01df138c; JI/Do not send label failed again: "caller does not have permission") | ASI-MANIFEST v1 2026-10-23 dec1fd6c6011fae4e0edaa2fc521dc5abe091f03e53f4f0dc1560e32f22f55fd (10: 5 S1 (H4 #5-7, 9, 10) + 5 S2 (H3 #10-14); user approved Oct 21 "go ahead for Friday"; created Oct 22 2:31 PM CT)  **Deleted Oct 23 after its 10 sends were logged (spent).** |
| 2026-10-26 | r6063913005521067503 (message 1a178ac17ca07314; JI/Do not send label failed again: "caller does not have permission"; the user adds it by hand) | ASI-MANIFEST v1 2026-10-26 e60fe7c98d888ae5845443647bb1796e13282966fd2181d832ea21b57751d890 (9: 5 S1 (H4 #11-15) + 4 S2 (H4 #1-4); built Mon 9:45 AM CT after the user said "do something today"; no Sunday build because the user had not OK'd one; 5 S1 addresses rechecked on live sites (Quickwaste via Jina, its site blocks direct fetches) and MX checked; draft body verified identical to the manifest) |

- **Oct 15 cap note:** `validate` on the Oct 16 queues now reports the new 5-first-email cap; the Oct 16 manifest was built and approved before the cap and sends unchanged (ASI ops, item 2). Don't rebuild it.

- **Delivery watch (Oct 19):** support@dumpsterintherough.com (H3 #6, sent Oct 16): Gmail delay notices Oct 17 and Oct 18, still retrying; not a hard bounce yet. If it fails, add it to do-not-contact and count it in the Friday gate report.
- **Oct 19 manifest:** none was put in Gmail over the weekend, so nothing sent Monday morning. Rebuilt Oct 19 10:08 CT (`ops/manifests/2026-10-19.json`, 15 S2s, validate PASS); user approved 12:33 CT; Gmail draft created and labeled.

- **Bounce (Oct 19):** support@dumpsterintherough.com (H3 #6) hard-bounced 10:31 CT after two delay notices; logged from `ops/evidence/2026-10-19_JI-H3-S1_bounce.json`, added to `data/do_not_contact.csv`, its S2 skipped. Gate count so far: 1 hard bounce in 46 sends (2.2%, just over the 2% line; report Friday).
- **H4 S1 (user, Oct 19, "approve H4"):** queued; Tue Oct 20 has H3 #15 plus H4 #1-4 (5 first emails) and the Hercules and Essential Waste S2s, all drafted. H4 #5-15 wait in `ops/queue/JI-H4-S1-hold.json` because ji_ops `validate` counts deferred S1s toward the day's cap (ASI-owned code; fix requested from ASI). Each day, move that day's 5 into a live queue before planning.
- **H3 S2 copy:** `outreach/JI-H3_S2_Copy.md` (13 haulers, #6 skipped), pending the user's approval; due Oct 20.

- **Oct 19-21 sender pause (ASI ops, Oct 21):** the shared ASI Sender auto-paused Oct 19 4:22 PM CT after 3 bounces in 24 hours (our Dumpster in the Rough plus two ASI addresses). Nothing sent Oct 20 or Oct 21. The fix (`ops/sender/Code.gs` synced from ASI commit 2a0d85a): each business has its own first-email cap; ours stays 5 of a 15 share. The user pastes it into Apps Script and sets MODE to LIVE before Oct 22.
- **Bounce rule additions (ASI ops review, Oct 21):** log and suppress any bounce the same day (address and domain in `data/do_not_contact.csv`); never send a first email to a domain that has bounced before. ASI checks bounces around midday on send days.
- **ji_ops sync (Oct 21):** `scripts/ji_ops.py` synced from ASI `asi_ops.py` f34e343 (records carry `planned_for`; validate and plan count only the day's records; manifest leaves out drafts planned for another day). The `JI-H4-S1-hold.json` workaround is gone: H4 #5-15 are back in `JI-H4-S1.json` as deferred. Oct 22 plan applied: 15 (5 S1, 10 S2), validate PASS.
- **Bounce rule (ASI ops, Oct 21):** 3 bounces in 24 hours from either business pauses both. Until a mailbox-verification service exists: keep first emails low (5), recheck that each first-email address still appears on the hauler's live site before it goes on a manifest, and drop anything that has bounced. Oct 20 recheck: Trash Hauling Fast, Jon's Junk Removal, Renegade Roll-Offs, Texas Roll Off and Long Boy Rentals all still publish their address (direct page fetch, Cloudflare-decoded).
- **Next send: Thu Oct 22** (a manifest only sends on its own date and goes stale after 36 hours, so it is built Wed Oct 21 afternoon): the same 15 drafted for Oct 20 (5 S1: H3 #15, H4 #1-4; 10 S2), validate PASS for Oct 22. Items planned for Oct 21 (H3 S2 #10-14, H4 #5-9) move to Fri Oct 23.

- **Fri Oct 23 prep (Oct 21):** Friday's first emails are H4 #5-7, 9 and 10 (Texas Rolloff Dumpster Rentals, Action Roll-Offs, Driveway Dumpster Rental, Come and Take It, Junk It Mobile Dumpsters); all five addresses rechecked on the live sites, MX present. PEM Dumpster Rentals (H4 #8) skipped: its page renders empty, so the address can't be confirmed. Follow-ups: H3 S2 #10-14. Friday is planned, drafted and put on a manifest Thursday afternoon after Thursday's sends are logged (planning earlier would carry Thursday's unsent drafts). **User approved Friday's list Oct 21 ("go ahead for Friday").**
- **Pace (user, Oct 21):** from Mon Oct 26, first emails are 15 a day for ASI and 5 for Jobsite (unchanged for us).

- **H5/H6 recheck (Codex, Oct 21):** 28 of 30 addresses still on the haulers' live pages, all 30 with MX. Not confirmed, so skipped when H5/H6 copy is written: Precision Dumpsters LLC (H5) and Big Orange Bins (H6).
- **DFW (research only, Oct 21):** `data/hauler_list_dfw.csv`, 7 rows, no packets. Nothing is sent to DFW without the user's decision on a second city and its sender name.
- **Daily check-in (user, Oct 26):** a scheduled task (trig_01XWLjVVpmaz9CLypRMhXqyE) wakes this session Sun-Thu at 1:37 PM CT to log the day's sends, check replies and bounces, and draft the next send day. The manifest Gmail draft is still created only after the user's OK in chat. No Friday run: a Friday-built manifest would be stale by Monday 8 AM (36 hours), so Sunday's run builds Monday's.
- **H3 S2 #15 (Trash Hauling Fast)** approved by the user Oct 26 ("approve"): `outreach/JI-H3_S2_Copy_15.md`, queued as `ops/queue/JI-H3-S2-15.json` (linked to its Oct 22 S1, validate PASS), for Tue Oct 27.
- **DFW approved as the second city (user, Oct 26: "DFW is fine").** Codex prospects DFW next (`AGENTS.md`, packets DFW1, DFW2...). Before any DFW send: the sender display name and signature for DFW (proposal: "DFW Jobsite Intelligence" from sites@; the alias map in `ops/rules.json` and the ASI Sender take one name per alias, so this needs the user and ASI), and DFW S1 copy approved by the user.

- **Copy status (Oct 21):** H1/H2 S5 approved by the user ("approve"): `outreach/JI-H1_S5_Copy.md`, `outreach/JI-H2_S5_Copy.md`, due Nov 2-3. `outreach/JI-H4_S2_Copy.md` (14, PEM skipped; due from Oct 26) and `outreach/H5_S1_Copy.md` (14; Precision skipped; first H5 sends from Oct 27) approved by the user Oct 22 ("approve H4 S2 and H5"); queued as `ops/queue/JI-H4-S2.json` (link-threads after each H4 S1 is logged) and `ops/queue/JI-H5-S1.json`.

- **Oct 26 workaround:** `plan` again picked H4 S2s whose S1 was unsent (#11-15) and #5 (S1 Oct 23, not due). H4 S2 #1-4 planned by hand for Oct 26; #5-10 deferred (planned Oct 30); #11-15 moved to `ops/queue/JI-H4-S2-hold.json` until their S1s (sent Oct 26) are logged, because `validate` checks every unsent record in a queue. Trash Hauling Fast (H3 #15) S2 copy still to be written and approved.
- **ji_ops plan gap (Oct 22, for ASI):** `plan` picked S2s whose S1 had not been sent yet (H4 #5-15) when `JI-H4-S2.json` was passed for Oct 23; `validate` correctly rejects them (list status, no reply_to), so nothing wrong was drafted. Until fixed, pass a follow-up queue to `plan` only once its S1s are logged and due.

- **Full mailbox audit (Oct 22, 2:40 PM CT, user asked):** every non-Asterfield message in the last 10 days, all folders, read. No hauler has replied to Jobsite. Sent from sites@ to prospects: 61 messages to 36 haulers, exactly matching `data/send_ledger.csv` (Oct 14: 1, Oct 15/16/19/22: 15 each); 1 hard bounce (Dumpster in the Rough), already suppressed. The two recent replies are ASI's: Nautilus Sign (houston@, Oct 22 11:06 AM CT, asks for the free sample) and Stat Signz (dfw@, Oct 22 12:29 PM CT, "No thanks"). One stray send: Oct 21 4:18 PM CT, an ASI sign-shop email (A To Z Sign Company / Thai Tale Eatery) went out **from sites@ to the user's own address**, not to a prospect; it was not on a Jobsite manifest (looks like a sender test). Reported to the user for ASI.

## Excluded

- Red Dog Dumpsters LLC (Oct 14): email domain is a Nashville, TN company; doesn't match the Houston FMCSA yard.
- Waste Falcon LLC (Oct 14): serves Bryan-College Station; Cypress address is a mailbox suite.
