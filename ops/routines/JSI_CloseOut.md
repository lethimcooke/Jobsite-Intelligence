# JSI close-out (Mon-Fri 2:54 PM ET)

Goal: log what went out today, handle the mailbox (our lane), then prepare the next business day: drafts, the
prepared batch for the publisher, and the follow-up copy buffer one send day beyond it. No manifest here.
Read `README.md` here, `ops/README.md` and `CLAUDE.md` first. PY = `D:\Workspace\austin-signage-repo\local\tools\asi-venv\Scripts\python.exe`.
Scratch: `D:\Workspace\austin-signage-repo\local\tools\scratch\routines\<today>\jsi\`. Copy rules: `docs/Outreach_Copy_v2.md`.

## 0. Guard
If `ops/routines/done/closeout_<today>.txt` exists, today's close-out already ran (or was done by hand): log
"already done" and stop. Write that file at the end of a successful run. Call `get_usage` now (README, Logging).

## A. Reconcile today (skip on non-send days)
If neither `ops/manifests/<today>.json` nor `ops/prepared/<today>.json` exists, nothing was listed for today (first day
back after the Nov 18 pause, or a missed close-out): log "no Jobsite list for today", alert only if records were drafted
for today, and go to B. Unsent drafts from an earlier day stay `drafted`; the plan in C carries them.

**Before the JSI publisher is installed** (the Sender Log has never had a `JSI-PUBLISH` row): the pre-send builds
`ops/manifests/<date>.json` the old way, so step 2 uses that file and no row is ever DROPPED. Step C5b still stages the
prepared batch: it costs one labeled draft, proves the batch builds, and is what the publisher will read once installed.
1. Export the Sender Log (as in `JSI_PreSend.md` step 1) and save Gmail Sent:
   `search_threads` `in:sent from:sites@asterfieldgroup.com after:<today> before:<tomorrow>` (METADATA_ONLY, pageSize 50,
   page until done) to `sent_<today>.json` in search_threads shape.
2. The day's list is `ops/manifests/<today>.json` when the pre-send built it, else `ops/prepared/<today>.json` (what the
   publisher published from):
   `PY -I ops/routines/tools/reconcile_check.py --manifest <that file> --sender-log ... --sent ... --out <scratch>\reconcile_<today>.json`
3. SENT entries, per queue: `ji_ops.py evidence <queue> <scratch>\reconcile_<today>.sent_threads.json --out ops/evidence/<today>_<Q>.json`,
   `ji_ops.py log <queue> <evidence>` (dry run), then `--apply`. SKIPPED: mark skipped with the sender's reason (a
   "one company, one business" skip means the company belongs to ASI: note it in the list and drop it). DROPPED (the
   publisher left it out): a hook reason -> `hold_stale.py` with that reason; any other reason -> leave it `drafted` for
   the next plan and say why in the log. UNCERTAIN: check the draft (`list_drafts`) and Sent for the recipient; if a Sent
   message exists, log it from that message; if the draft still exists and nothing was sent, leave it PENDING for the late
   reconcile. Never re-create or resend. PENDING before 6 PM ET is normal while the sender works.
4. No Sender Log rows at all for today's Jobsite list: the sender or publisher did not run: alert (MODE, triggers, JSI-PUBLISH rows).

## B. Mailbox (our lane only)
Replies, bounces and opt-outs since the last close-out on `sites@` threads only, per ops/README.md step 1:
`to:sites@asterfieldgroup.com -from:asterfieldgroup.com newer_than:3d` (then `get_thread` on each hit) and
`from:(mailer-daemon OR postmaster) newer_than:3d` (act only on addresses in our ledger or queues). Record each in the
tracker and the list; a reply sets `Replied <date> (...)`; opt-outs go to `data/do_not_contact.csv`. Engaged replies are
not drafted unattended: alert with the business name and thread link. A hot reply (asks for the sample or the pilot,
says interested) leads the alert with "HOT: <business>". Business names only, never a person's name.

## C. Plan the next business day (N = next weekday not in holidays.txt; Wed Nov 25, 2026 plans Mon Nov 30)
1. Inventory: `PY -I ops/routines/tools/daily_status.py --repo . --out <scratch>\status.md --stale-out <scratch>\stale.json --gmail-prepared <found|missing from list_drafts subject:"JSI-PREPARED v1 <N>">`
   then `PY -I ops/routines/tools/hold_stale.py --repo . --stale <scratch>\stale.json --apply`.
2. Follow-ups due on N: `PY -I ops/routines/tools/followups_due.py --repo . --date <N> --out <scratch>\due_<N>.json`.
   Rows with `copy_ready_id` already have validated copy (yesterday's buffer): re-check each S2/S5 fact against the live
   record (`hook_recheck.js`), restate relative dates ("this week") for N, drop anyone who replied, bounced or opted out.
   Rows without copy: write it per `docs/Outreach_Copy_v2.md` "S2" / "S5" and the latest `outreach/JI-*_S2_Copy*.md` /
   `JI-*_S5_Copy*.md` as examples, one file per batch: `outreach/JI-<B>_<S2|S5>_Copy_<N>.md` (subject `Re: <s1_subject>`),
   `check_copy.py`, then `ji_ops.py convert ... --batch JI-<B> --stage <S2|S5> --out ops/queue/JI-<B>-<S2|S5>-<MMDD>.json`,
   `link-threads`, fill `hook_type`, `validate`.
2b. **Copy buffer, one send day ahead** (user, Nov 19, as ASI): after N's copy exists, write the S2/S5 copy for the
   follow-ups due on N+1 (the next weekday after N not in holidays.txt), up to 10, oldest S1 first, excluding anything
   planned for N; same files and checks as step 2, ending at `validate`. Do not plan or draft them. The next close-out
   reuses them in its step 2. `daily_status.py` alerts FOLLOW-UP COPY BUFFER LOW when the buffer is short.
2c. **Hook gate** (every close-out, before plan): `PY -I ops/routines/tools/hook_gate.py --repo . --send-date <N> --out <scratch>\gate_<N>.json`,
   then `hold_stale.py --repo . --stale <scratch>\gate_<N>.stale.json --apply` and, if `<scratch>\gate_<N>.release.txt`
   lists IDs, `hold_stale.py --repo . --release <those IDs> --apply` (Central Registry back up and their hooks pass). Log the counts.
3. Plan: `PY scripts/ji_ops.py plan <S1 queues, oldest batch first> <today's and buffered follow-up queues> --send-date <N> --apply`.
   It takes up to 5 first touches, then follow-ups oldest S1 first, within 15, and carries drafts whose day passed.
4. For each record planned for N: re-check the hooks of every S1 now planned for N, carried drafts included
   (`hook_gate.py --repo . --send-date <N> --include-drafted --out <scratch>\gate2_<N>.json`, then `hold_stale.py --stale
   <scratch>\gate2_<N>.stale.json --apply`); search Gmail for the address and domain (a hit on an ASI alias means the company
   belongs to ASI: drop it and note it in the list; never open ASI's threads beyond the search result), check the ledger and
   do-not-contact by address and domain. Hold each failure (stale hook -> `hold_stale.py`; reply, bounce, opt-out ->
   ops/README.md step 1). Re-run plan once to backfill.
5. Draft: `ji_ops.py next <queue>`; `create_draft` exactly (with `replyToMessageId` for follow-ups); immediately
   `record-draft` with the real IDs. Read the drafts back (`list_drafts` DRAFT_VIEW_FULL, saved to a file) and compare each
   with the queue payload after whitespace collapse; fix mismatches before going on. Never draft a record already `drafted`.
5b. **Stage the prepared batch** for the JSI publisher:
   `PY -I ops/routines/tools/prepare_batch.py --repo . --send-date <N> --out ops/prepared/<N>.json > <scratch>\prepared_<N>.out.txt`,
   then `create_draft` to operations@asterfieldgroup.com with the printed SUBJECT and BODY exactly, label it
   `JI/Do not send`, and record the draft ID in the run log. Optional check from the PC:
   `node ops/sender/dry_publish.cjs <scratch>\prepared_<N>.out.txt` (live re-check, publishes nothing). Re-staging is safe:
   the publisher uses the newest valid JSI-PREPARED draft for the date. Until the publisher is installed the pre-send
   builds the manifest from the same drafts, so stage it anyway.
6. Views: `PY -I ops/routines/tools/calendar_view.py --repo . --stale <scratch>\stale.json --start <N> --out ops/routines/CALENDAR.md`.
   Update the tracker's send table and engaged rows.
7. `lf_fix.py "ops/queue/*.json" "ops/manifests/*.json" "ops/prepared/*.json"`, write `ops/routines/done/closeout_<today>.txt`,
   commit and push to main (only files this run changed), then append to `run_log.md`:
   `<today> <HH:MM> ET close-out: logged <s>/<m> (skipped k, dropped d, pending p, uncertain u); replies r; planned <N>: S1 a/5, follow-ups b, total c/15; buffer <N+1> x written; gate pass/fail; prepared <draft id> (<sha8>); ready reserve <x> (<y> business days); usage ...`.
   Alert per README.
