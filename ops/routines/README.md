# Jobsite Intelligence weekday routines (local Claude Desktop scheduled tasks)

Permanent weekday workflow, no end date. First end-to-end test: Friday, Nov 13, 2026. Times are Central.
Follow `ops/README.md` (the daily loop) and `CLAUDE.md`; these files only say what runs when, unattended.
PY = `D:\Workspace\tools\asi-venv\Scripts\python.exe` (or `python` 3.13). Scratch:
`D:\Workspace\tools\scratch\routines\<today>\jsi\`.

| Task | When (Central) | What it does |
|---|---|---|
| JSI pre-send | Mon-Fri 5:55 AM | Keep a valid published JSI manifest; build and publish today's if missing or empty and drafted JI- rows exist |
| JSI close-out | Mon-Fri 1:54 PM | Reconcile today, mailbox (our lane), plan and draft the next business day (no manifest) |
| JSI late reconcile | Mon-Fri 5:33 PM | Reconcile what sent after the close-out; leave unsent drafts for the next plan |
| JSI replenish | Mon-Fri 3:55 PM | Add send-ready first touches to the reserve (verified, fresh TCEQ site, check_packet 0 flags) |

## Rules

- **Our lane only:** `sites@`, `JI-` records, `JI/` labels, our manifest drafts. Never open, edit, label or delete
  ASI's drafts or manifests. Both businesses' manifests share the subject prefix `ASI-MANIFEST v1 <date> <sha>`;
  tell ours apart by the exact SHA in `ops/manifests/<date>.json`.
- **Cadence:** up to 5 first touches plus eligible follow-ups (S2 at S1 + 2 business days, S5 at S1 + 13), 15 total;
  the shared mailbox cap is 60 and ASI plans 45. The sender enforces all of them.
- **Manifest freshness:** dated the send day, at most 36 hours old at 8 AM, so built each send morning by the
  pre-send. Friday's close-out drafts Monday; Monday's pre-send publishes Monday's manifest.
- **Reruns:** `tools/presend_check.py --id-prefix JI-` before any build (KEEP and SENDING are never replaced);
  `tools/reconcile_check.py` before any retry; UNCERTAIN entries are checked against the draft and Sent, never resent.
- **First run (Nov 13):** the ledger has no rows for the Nov 6 manifest (15 sends, Sender Log rows JI-...). The first
  close-out reconciles `ops/manifests/2026-11-06.json` before planning.
- **Line endings:** after any `ji_ops.py` write, `tools/lf_fix.py "ops/queue/*.json" "ops/manifests/*.json"`.
- **Never:** send, reply, forward or trash mail; change the sender's MODE or triggers; touch ASI files.

## Steps

**Pre-send:** weekend or `holidays.txt` -> stop. Save `list_drafts` (`subject:"ASI-MANIFEST v1 <today>"`, DRAFT_VIEW_FULL)
and the Sender Log export (Drive file `1qBaAWdp2rR9NVlNrL9qkaaKn-SVqh2xI7Et4Rj--4ro`, text/csv). Run
`PY -I ops/routines/tools/presend_check.py --repo . --date <today> --id-prefix JI- --gmail-drafts ... --sender-log ...`.
KEEP/SENDING/NOTHING: log. BUILD: re-check each drafted row's site record and Gmail history, `reconcile-drafts`,
then ops/README.md step 6 (manifest, decode-check, `create_draft` exactly, read back, label `JI/Do not send`).

**Close-out:** (A) reconcile today: Sent `in:sent from:sites@asterfieldgroup.com after:<today> before:<tomorrow>`,
`reconcile_check.py` against `ops/manifests/<today>.json`, then ops/README.md steps 7 and 8 for SENT entries; also any
earlier manifest with unlogged entries (Nov 6 on the first run). (B) ops/README.md step 1 (replies, bounces, opt-outs;
engaged replies are not drafted unattended: alert). (C) Plan the next business day: due follow-ups (write S2/S5
copy per the copy rules if missing, convert, link-threads), `ji_ops.py plan ... --send-date <N> --apply`, re-check each
planned row, `validate`, draft with `next` + `create_draft` + `record-draft`, read back and compare. No manifest.

**Late reconcile:** close-out section A again; leave PENDING drafts as `drafted` (the next plan carries them over).

**Replenish:** new packets only through `scripts/check_packet.py` (0 flags) and the copy rules; stop at 25 ready first touches.

## Logging and alerts

One line per run in `ops/routines/run_log.md`. Alert (PushNotification, or an `ALERT` line and the task's final
message) only for a reply needing the user's decision, an issue that prevents or cuts 3 or more of the day's
planned sends, an UNCERTAIN send, or a reserve under 15 ready first touches.
