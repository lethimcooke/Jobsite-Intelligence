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
- **Mailing address (OPEN, blocks LIVE):** CAN-SPAM requires a physical postal address in commercial email.
  `ops/rules.json` `footer.address` is empty until the user gives it.

## Gmail lane

Shared mailbox with ASI. Jobsite touches only sites@ threads, drafts in its own queues, its own manifest
draft and `JI/` labels. Labels (created Oct 14): `JI/Send manually` (Label_6), `JI/Do not send` (Label_7).

## Batches

| Batch | Metro | Copy file | Rows | Status |
|---|---|---|---|---|
| JI-H1 | Houston | outreach/H1-H2_S1_Copy_v2.md (H1) | 10 (Red Dog Dumpsters SKIP, 9 queued) | Requeued Oct 14 from copy v2 (user: send v2 through the tool; subjects reformatted to `- Subject:` with the A/B arm on `- Subject arm:`). Planned for Oct 15: all 9. Validate PASS for 2026-10-15. Not drafted: waiting for the DRY_RUN pass, LIVE go-ahead and the mailing address |
| JI-H2 | Houston | outreach/H1-H2_S1_Copy_v2.md (H2) | 9 (Waste Falcon SKIP, 8 queued) | Same. Planned for Oct 15: 6 (Astro, Moffitt, OP Enterprises, Jet, Sustainable Disposal Bins, Z Sites); deferred to Oct 16: Hercules, Essential Waste |

## Plan

- **Oct 15 (first send):** 15 S1s (JI-H1 all 9, JI-H2 first 6), Jobsite's full daily share. **Oct 16:** the 2 deferred S1s, then S2s start Oct 17 (S1 + 2 business days).
- The A/B subject arm is in the copy file per row; log it with each send in `outreach_results.csv` notes.

## Send log

| Date | Batch | Stage | Sent | Evidence | Notes |
|---|---|---|---|---|---|

## Engaged prospects

| Company | First reply | Last touch | Next touch | Notes |
|---|---|---|---|---|

## Manifest drafts (the only ones Jobsite may delete)

| Send date | Draft ID | Subject |
|---|---|---|

## Excluded

- Red Dog Dumpsters LLC (Oct 14): email domain is a Nashville, TN company; doesn't match the Houston FMCSA yard.
- Waste Falcon LLC (Oct 14): serves Bryan-College Station; Cypress address is a mailbox suite.
