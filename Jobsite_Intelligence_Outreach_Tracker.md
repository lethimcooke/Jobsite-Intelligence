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
- **Pace (Oct 14):** the operations@ mailbox sends at most 60 a day across both businesses; Jobsite's share
  is 15, ASI's 45. First emails always go before follow-ups; follow-ups wait a day when the share is full.
  No separate first-email cap.
- **Sequence:** S1, S2 (+2 business days), S5 (+13). Any reply freezes the cold sequence.
- **One company, one business:** a company emailed by ASI is never cold-emailed by Jobsite, and the reverse.
  The sender enforces it at send time; a skip for that reason means drop the company here.
- **Copy:** `docs/Outreach_Copy_v2.md`. No em dashes, no individuals named, no calls offered, every claim
  cites the TCEQ record, our read is labeled. Never say construction started, a hauler or vendor is
  unselected, or work is open for bid.
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

## Plan

- **Oct 15:** 15 S1s (JI-H1 8, JI-H2 7), Jobsite's full daily share. **Oct 16:** Essential Waste Solutions S1, plus City Waste S2 (copy still to be written; threaded on its Oct 14 S1). S2s for Oct 15 S1s are due Oct 17.
- The A/B subject arm is in the copy file per row; log it with each send in `outreach_results.csv` notes.

## Send log

| Date | Batch | Stage | Sent | Evidence | Notes |
|---|---|---|---|---|---|
| 2026-10-14 13:32 CT | JI-H1 | S1 | 1: City Waste LP (sales@city-waste.com) | Sent 1a13bb05fcc96d4f, thread 1a13ba7b4a2819dd; `ops/evidence/2026-10-14_JI-H1.json`; queue `ops/queue/JI-H1-S1-sent-v1.json` | Sent by mistake: an ASI test manifest made while the sender was LIVE. Approved v1 text, from sites@ as Houston Jobsite Intelligence, without the mailing-address line (still pending). Kit v2 adds `dry_run_only` to every manifest so tests can't send. S2 due Oct 16. |

## Engaged prospects

| Company | First reply | Last touch | Next touch | Notes |
|---|---|---|---|---|

- **Tests:** any test manifest is made with `ji_ops.py manifest ... --dry-run-only`; the sender only sends from manifests marked `"dry_run_only": false`.

## Manifest drafts (the only ones Jobsite may delete)

| Send date | Draft ID | Subject |
|---|---|---|
| 2026-10-15 | r8605933855582475111 (message 1a13c9cb6e281e74, labeled JI/Do not send) | ASI-MANIFEST v1 2026-10-15 fae0d3b38062bfa462ea73fae93e63c9ab1535ebdfbe029993916ddadbe2162b (15 S1s, dry_run_only false; user approved Oct 14) |

## Excluded

- Red Dog Dumpsters LLC (Oct 14): email domain is a Nashville, TN company; doesn't match the Houston FMCSA yard.
- Waste Falcon LLC (Oct 14): serves Bryan-College Station; Cypress address is a mailbox suite.
