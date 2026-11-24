# Jobsite Intelligence weekday routines (local Claude Desktop scheduled tasks)

Permanent weekday workflow, no end date, ported from ASI's proven setup on Nov 24, 2026
(`TRANSFER_2026-11-24.md`). Times are Eastern (the PC's clock; the ASI Sender and the publisher run on Central, one hour
earlier). Each task's prompt says: open `D:\Workspace\jobsite-intelligence-repo` and follow the matching file here, plus
`ops/README.md` (the daily loop) and `CLAUDE.md`.
PY = `D:\Workspace\austin-signage-repo\local\tools\asi-venv\Scripts\python.exe` (or `python` 3.13). Scratch: `D:\Workspace\austin-signage-repo\local\tools\scratch\routines\<today>\jsi\`.

| Task | When (ET) | File | What it does |
|---|---|---|---|
| JSI pre-send | Mon-Fri 6:55 AM (8:35 AM once the JSI publisher is installed) | `JSI_PreSend.md` | Until the publisher is live: keeps or builds today's manifest. After: backup only, reports the publisher's result |
| JSI close-out | Mon-Fri 2:54 PM | `JSI_CloseOut.md` | Reconciles today, mailbox (our lane), plans and drafts the next business day, stages the prepared batch, writes the next day's follow-up copy buffer |
| JSI late reconcile | Mon-Fri 6:33 PM | `JSI_LateReconcile.md` | Reconciles what sent after the close-out; leaves unsent drafts for the next plan |
| JSI replenish | Mon, Wed, Fri 4:55 PM | `JSI_Replenish.md` | Adds send-ready first touches to the reserve (verified address, fresh TCEQ site, check_packet 0 flags); runs the shared MillionVerifier CSV |

ASI runs the same four steps from its own repo. The two never edit each other's files, drafts, labels or manifests,
so a blocker in one leaves the other free.

## Fixed rules

- **Our lane only:** `sites@`, `JI-` records, `JI/` labels, our manifest and `JSI-PREPARED` drafts. Never open, edit,
  label or delete ASI's drafts, manifests or prepared batches. Both businesses' manifests use the subject
  `ASI-MANIFEST v1 <date> <sha>`; ours is the one whose decoded business is "Jobsite Intelligence" (repo-built: the SHA in
  `ops/manifests/<date>.json`; publisher-built: the `JSI-PUBLISH PUBLISHED` row in the Sender Log).
- **Cadence:** up to 5 first touches plus follow-ups (S2 at S1 + 2 business days, S5 at S1 + 13), 15 total; the shared
  mailbox cap is 60 and ASI plans 45. The sender enforces all of them. First touches only to Houston until a DFW alias exists.
- **Gates for every first touch:** verified address (MillionVerifier ok, or published on the hauler's own site under the
  tracker's rules), hook re-checked live (`tools/hook_gate.py` / `tools/hook_recheck.js`: authorization ACTIVE, cited record
  date on the live record, at most 45 days old on the send day), stale rows held (`tools/hold_stale.py`), list status,
  do-not-contact and send ledger by address and domain, Gmail history, `ji_ops.py validate` PASS.
- **Manifest freshness:** dated the send day and at most 36 hours old at 8 AM CT. The close-out stages a prepared batch
  (`JSI-PREPARED v1`); the publisher or, until it is installed, the pre-send turns it into the send-day manifest.
- **Reruns:** `tools/presend_check.py --id-prefix JI-` before any build (KEEP and SENDING are never replaced);
  `tools/reconcile_check.py` before any retry; UNCERTAIN entries are checked against the draft and Sent, never resent.
- **No copy before verification** (user, Nov 19, same as ASI): an unverified address gets a `data/to_verify_<date>.csv` row
  and nothing else. MillionVerifier is website-only: never call its API, never read, print or store `MILLIONVERIFIER_API_KEY`.
- **Line endings:** after any `ji_ops.py` write, `tools/lf_fix.py "ops/queue/*.json" "ops/manifests/*.json"`.
- **Holidays:** `holidays.txt` (no sends; Thanksgiving Nov 26-27, 2026). The next business day skips them; Wed Nov 25's
  close-out plans Mon Nov 30.
- **Never:** send, reply, forward or trash mail; create Gmail drafts other than our S1/S2/S5 drafts, our manifest and our
  prepared batch; change the sender's MODE, Script properties or triggers; touch ASI files; edit `scripts/ji_ops.py` or
  `ops/sender/Code.gs` (ASI owns them: tell the user).

## Logging and alerts

Every run appends one line to `run_log.md`: date and time (ET), task, result, counts, and the usage measurement:
call `mcp__ccd_session_mgmt__get_usage` first and last (load it with ToolSearch if deferred) and end the line with
`usage 5h A%->B%, weekly C%->D%; wall clock N min` (or "usage tool unavailable"). Routine successes go only there.
Alert (PushNotification, or a line starting `ALERT` in the run log and the task's final message) only when:
- a reply, sample request or opt-out needs the user's decision (engaged replies stay with the user);
- an unresolved issue prevents or cuts 3 or more of the day's planned sends (sender did not run, manifest or prepared
  batch could not be built, publisher dropped 3+, UNCERTAIN sends);
- ready first touches fall below 3 business days of cover (15), or a replenish run ends SHORT.

## Views

- `CALENDAR.md`: rolling 15-business-day first-touch calendar plus follow-ups (`tools/calendar_view.py`), refreshed by each close-out.
- `tools/daily_status.py`: the close-out's read-only status (send confirmation, next day's batch, reserve, copy buffer,
  verification backlog). The reserve line is 50 (10 business days at 5 a day): under it, replenish runs in full mode.
