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
| 2026-10-16 08:02-08:32 CT | JI-H2 (1), JI-H3 (11 logged) | S1 | 12 of 15 logged (Essential Waste; H3 #1-11); Dump Today sent 08:32, Mr. Niceday's and RNC Developers still sending | `ops/evidence/2026-10-16_JI-H2-S1_a.json`, `ops/evidence/2026-10-16_JI-H3-S1_a.json` (Dump Today logged in the next pass) | No bounces or replies. Friday gate report: 31 sent Oct 14-16, 0 hard bounces, 0 complaints or blocks, no sender pause. |

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
| 2026-10-16 | r8637948838471712868 (message 1a140ec80a072bdb, labeled JI/Do not send) | ASI-MANIFEST v1 2026-10-16 8885a25f89db96723edd19ca568f5473fb481175ba801d6fcc94ebe48356fce3 (15 S1s: Essential Waste + H3 #1-14, dry_run_only false; user approved Oct 15) |

- **Oct 15 cap note:** `validate` on the Oct 16 queues now reports the new 5-first-email cap; the Oct 16 manifest was built and approved before the cap and sends unchanged (ASI ops, item 2). Don't rebuild it.

## Excluded

- Red Dog Dumpsters LLC (Oct 14): email domain is a Nashville, TN company; doesn't match the Houston FMCSA yard.
- Waste Falcon LLC (Oct 14): serves Bryan-College Station; Cypress address is a mailbox suite.
