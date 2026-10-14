# Jobsite Intelligence: daily operations

`scripts/ji_ops.py` (a copy of ASI's `scripts/asi_ops.py`) does the queueing, validating, drafting
records, manifest, evidence and logging. Rules: `ops/rules.json` (**the tracker wins**; change both in
the same commit). Tests: `python3 -m unittest discover -s tests`. Don't write one-off parsers or
logging snippets; if the tool lacks something, tell the user (the ASI repo owns the code).

The tool never sends mail and never calls Gmail. Claude makes the Gmail MCP calls and passes the
results to the tool. Nothing is "sent" without a Sent-folder message ID.

## The shared mailbox (read this first)

Jobsite and ASI (Austin Signage Intelligence) are separate businesses with separate repos and
sessions. They share one Gmail mailbox (operations@asterfieldgroup.com) and one sender script.

- **Our lane:** only `sites@asterfieldgroup.com` threads, only drafts recorded in our queues, only our
  manifest draft, only `JI/...` labels. Never open, edit, label or delete ASI's drafts, manifests,
  threads (fieldwork@, houston@, dfw@, sanantonio@) or `ASI/...` labels.
- **Daily total:** the mailbox sends at most 60 a day. Jobsite plans to **15** (`daily_share`), ASI to 45.
  The ASI Sender enforces the 60 and each share; first emails go before follow-ups.
- **One company, one business:** the sender refuses a first email if anyone at that domain (not
  personal mail) has ever written to us or been emailed from any alias, and every manifest's
  do-not-contact applies to every email. A sender SKIP for that reason means the company belongs to
  ASI: mark it in our list notes and drop it.
- **The ASI Sender** (Google Apps Script in the user's Gmail) sends approved S1, S2 and S5 drafts listed
  in a validated manifest, from `sites@` as "Houston Jobsite Intelligence". Its code is owned by the
  ASI repo; `ops/sender/Code.gs` here is a reference copy only. Its log is the "ASI Sender Log" sheet
  (our rows start `JI-`).

## Daily loop

Short prompt to start a day: **"Run the ops/README.md daily loop for <batch files>."**

1. **Check the mailbox (our lane only).**
   - Replies: `search_threads` with `to:sites@asterfieldgroup.com -from:asterfieldgroup.com newer_than:3d`,
     then `get_thread` on each hit (search previews omit newer messages).
   - Bounces: `from:(mailer-daemon OR postmaster) newer_than:3d`; act only on bounces for addresses in
     our ledger or queues.
   - Record every reply, opt-out ("no thanks", "remove", "stop") and bounce in the tracker and list
     before anything else. A reply sets list status `Replied <date> (...)`, which blocks cold follow-ups.
     An opt-out also goes in `data/do_not_contact.csv`. Engaged replies (E1-E3) are drafted for the user,
     labeled `JI/Send manually`; the user sets the From alias to sites@ and sends them. **E1 (sample):**
     build that hauler's own sample the same day in `jobsite-report/` (5 TCEQ sites in its service area,
     picked for its services; its S1 site can be #1; follow `jobsite-report/README.md`), export the PDF,
     draft the E1 in the hauler's thread, and tell the user to attach the PDF and set From to sites@.
     Every hand-off says this (Oct 14: an ASI engaged email went out from operations@).
   - List due follow-ups from `data/send_ledger.csv` (S2 at S1 + 2 business days, S5 at S1 + 13).
2. **Queue.** For each approved copy file due today:
   `python3 scripts/ji_ops.py convert outreach/<file>.md --batch JI-<B> --city Houston --stage <S1|S2|S5> --title-prefix <B> --out ops/queue/JI-<B>-<stage>.json`
   Bodies are copied verbatim, in file order; an opt-out line at the end of a body becomes the footer
   (appears once). Batch IDs always start `JI-`. Follow-ups (S2, S5): right after convert, run
   `python3 scripts/ji_ops.py link-threads ops/queue/<Q>.json`, which fills each record's
   `reply_to_message_id` from the ledger (the latest send to that recipient). Fill each record's
   `hook_type` with the site type (industrial, commercial, construction) so `scripts/outreach_stats.py`
   can group results by it.
3. **Plan.** `python3 scripts/ji_ops.py plan ops/queue/<today's queues>.json --send-date YYYY-MM-DD --apply`
   picks today's 15: first emails first, then follow-ups oldest first. The rest are `deferred`.
4. **Validate.** `python3 scripts/ji_ops.py validate ops/queue/<Q>.json --send-date YYYY-MM-DD` must print
   PASS (sender and signature, price line once, em dashes, banned claims and call offers, refund wording,
   do-not-contact, list status per stage, S1-S2-S5 sequence, threading, caps).
5. **Draft.** `python3 scripts/ji_ops.py next ops/queue/<Q>.json` prints the payloads. For each: `create_draft`
   (with `replyToMessageId` for follow-ups), then right away
   `python3 scripts/ji_ops.py record-draft ops/queue/<Q>.json <id> --draft-id .. --message-id .. --thread-id ..`.
   After an interruption: `list_drafts`, save as JSON, `reconcile-drafts`, then `next`. Gmail drafts are
   always From operations@; the sender switches them to sites@ when it sends.
6. **Manifest.** Once today's drafts are made:
   `python3 scripts/ji_ops.py manifest <today's queues> --send-date YYYY-MM-DD --out ops/manifests/<date>.json`
   (re-validates everything; refuses the whole list on any error), then `create_draft` to
   operations@asterfieldgroup.com with the printed SUBJECT and BODY exactly. Record its draft ID in the
   tracker; it is the only manifest we may ever delete. Label it `JI/Do not send`.
7. **Evidence.** After the sender has run: `search_threads` with `in:sent from:sites@asterfieldgroup.com newer_than:1d`
   (save as JSON), then `python3 scripts/ji_ops.py evidence ops/queue/<Q>.json <threads.json> --out ops/evidence/<date>_<Q>.json`.
   Check it against the sender log's JI- rows. Add bounces by hand (`kind: gmail_bounce`).
8. **Log.** `python3 scripts/ji_ops.py log ops/queue/<Q>.json ops/evidence/<date>_<Q>.json` (dry run), then with
   `--apply`. It backs up to `data/backups/` (gitignored), appends the ledger, sets S1 list status,
   appends `outreach_results.csv`, and marks records `sent_confirmed`.
9. **Tracker and push.** Update the tracker's send table and engaged rows, commit, push to `main`.

## Hard limits

- Claude never sends email; Gmail send, reply, forward and trash are denied in `.claude/settings.json`.
- Only the ASI Sender sends, and only manifest-listed, validated S1, S2 and S5 drafts. Engaged emails
  stay with the user.
- No em dashes. Full three-line signature. Never team@claimcascade.com. Never name individuals in copy.
  Never say construction started, a vendor or hauler is unselected, or work is open for bid. No calls offered.
- Nothing is marked sent without Sent-folder evidence.
