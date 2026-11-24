# ASI Sender: reference copy

`Code.gs` here is a read-only copy of `ops/sender/Code.gs` in the Austin-Signage repo, which owns it.
The live script runs in the user's Gmail (operations@asterfieldgroup.com) and serves both businesses.
Don't edit this copy; if the sender needs a change, tell the user, who brings it to the ASI session.

What it does for Jobsite: reads our manifest draft ("ASI-MANIFEST v1 <date> <sha256>", business
"Jobsite Intelligence"), re-checks every listed draft (exact recipient, subject and text; sites@ with
"Houston Jobsite Intelligence" in the signature and as a verified Send-mail-as alias; do-not-contact;
no reply or bounce; thread unchanged; first emails only to companies with no email history), and sends
it from sites@. Caps: 60 a day for the mailbox, 15 of them ours, first emails first. Modes: DRY_RUN,
TEST, LIVE, PAUSED (script property MODE, set by the user).

## JSI publisher (Jobsite's own code, `JsiPublisher.gs`)

Unlike `Code.gs`, `JsiPublisher.gs` is owned here. It is a second publisher entry in the same Apps Script project,
next to ASI's `Publisher.gs`, built from ASI's "JSI template" (ASI repo, `ops/routines/STATUS.md`):

- The JSI close-out stages `JSI-PREPARED v1 <date> <sha256>` (a draft to operations@, from
  `ops/routines/tools/prepare_batch.py`). `jsiPublishManifest` (6:10, 6:30, 6:50, 7:10 AM Central) re-checks each
  entry with the sender's own `checkEntry_` plus the TCEQ hook (`noiProblem_`: authorization ACTIVE, cited record date
  on the live record, at most 45 days old) and publishes one `ASI-MANIFEST v1` draft with business
  "Jobsite Intelligence". `jsiWatchdog` (7:50 AM) and `jsiConfirmSends` (5:15 PM) email operations@ only when action is needed.
- Every global is prefixed `jsi`/`JSI`/`JPUB`, Sender Log rows use mode `JSI-PUBLISH`, and `installJsiPublisher` /
  `removeJsiPublisher` touch only `jsiPublishManifest`, `jsiWatchdog` and `jsiConfirmSends` triggers, so ASI's publisher
  and `runSender` are never affected.
- Tests: `node ops/sender/test_publisher.cjs [prepare_batch output]` (also run by `python3 -m unittest discover -s tests`).
  Dry run against the live Central Registry, publishing nothing: `node ops/sender/dry_publish.cjs <prepare_batch output>`.
- `hook_facts.cjs` runs the same rule from the PC for `ops/routines/tools/hook_gate.py`.

Installing it is the user's step (paste the file into the project, run `installJsiPublisher`, then `jsiTestAlert`); see
`ops/routines/TRANSFER_2026-11-24.md`.
