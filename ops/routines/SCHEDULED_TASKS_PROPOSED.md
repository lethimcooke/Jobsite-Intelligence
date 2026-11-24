# Proposed SKILL.md text for the four jsi-* scheduled tasks (Nov 24, 2026)

Proposal only. The user paused these tasks on Nov 18; nothing here has been applied. To apply: in Claude Desktop >
Scheduled, edit each task, replace its prompt with the text below, set the schedule shown, and set the permission mode
to Auto. Times are Eastern (the PC's clock). Turn them back on only after the steps in `TRANSFER_2026-11-24.md`.

The usage line matches the one the user added to asi-replenish on Nov 18; here all four tasks carry it.

## jsi-presend

Schedule: Mon-Fri 6:55 AM ET while the JSI publisher is not installed; 8:35 AM ET after it is.

```
---
name: jsi-presend
description: Weekdays 6:55 AM ET (8:35 AM ET once the JSI publisher runs): keep or publish today's Jobsite manifest before the 9 AM ET send window.
---

Run the Jobsite Intelligence pre-send routine. Work in D:\Workspace\jobsite-intelligence-repo (branch main). Read CLAUDE.md and ops/routines/README.md, then follow ops/routines/JSI_PreSend.md exactly. Once the Sender Log shows JSI-PUBLISH rows, only report the publisher's result unless that file says to build. Our lane only: sites@, JI- records, JI/ labels, our own manifest and JSI-PREPARED drafts. Never open, edit, label or delete ASI's drafts, manifests or prepared batches, never send, reply, forward or trash mail, never change the sender's MODE, Script properties or triggers, and never replace a manifest the check calls KEEP or SENDING. Log one line to ops/routines/run_log.md. Alert the user only for the conditions in the README.
Usage measurement: as your very first action and again as your last before logging, call mcp__ccd_session_mgmt__get_usage (load it with ToolSearch if deferred) and end the run log line with "usage 5h A%->B%, weekly C%->D%; wall clock N min". If the tool is unavailable, say so in the log line.
```

## jsi-closeout

Schedule: Mon-Fri 2:54 PM ET.

```
---
name: jsi-closeout
description: Weekdays 2:54 PM ET: reconcile today's Jobsite sends, handle our replies, plan and draft the next business day, stage the JSI-PREPARED batch and the next day's follow-up copy.
---

Run the Jobsite Intelligence close-out routine. Work in D:\Workspace\jobsite-intelligence-repo (branch main). Read CLAUDE.md, ops/README.md and ops/routines/README.md, then follow ops/routines/JSI_CloseOut.md exactly: reconcile today against Gmail Sent (from sites@) and the Sender Log, log confirmed sends, record replies, bounces and opt-outs, run the hook gate, plan and draft the next business day (up to 5 first touches plus follow-ups, 15 total), stage the JSI-PREPARED batch, and write the follow-up copy buffer for the send day after it (no manifest). Our lane only; never touch ASI's drafts, manifests, prepared batches, labels or files. Never send, reply, forward or trash mail, never resend or retry an uncertain send, never change the sender's MODE, Script properties or triggers. Log one line to ops/routines/run_log.md. Alert the user only for the conditions in the README.
Usage measurement: as your very first action and again as your last before logging, call mcp__ccd_session_mgmt__get_usage (load it with ToolSearch if deferred) and end the run log line with "usage 5h A%->B%, weekly C%->D%; wall clock N min". If the tool is unavailable, say so in the log line.
```

## jsi-late-reconcile

Schedule: Mon-Fri 6:33 PM ET.

```
---
name: jsi-late-reconcile
description: Weekdays 6:33 PM ET: reconcile Jobsite sends made after the close-out; leave unsent drafts for the next plan.
---

Run the Jobsite Intelligence late reconcile routine. Work in D:\Workspace\jobsite-intelligence-repo (branch main). Read ops/routines/README.md, then follow ops/routines/JSI_LateReconcile.md exactly. Our lane only; never send, reply, forward or trash mail, never resend or retry, never touch ASI items, never change the sender's MODE, Script properties or triggers. Log one line to ops/routines/run_log.md. Alert the user only for the conditions in the README.
Usage measurement: as your very first action and again as your last before logging, call mcp__ccd_session_mgmt__get_usage (load it with ToolSearch if deferred) and end the run log line with "usage 5h A%->B%, weekly C%->D%; wall clock N min". If the tool is unavailable, say so in the log line.
```

## jsi-replenish

Schedule: Mon, Wed, Fri 4:55 PM ET (was every weekday; matches asi-replenish since Nov 18).

```
---
name: jsi-replenish
description: Mon, Wed, Fri 4:55 PM ET: add send-ready Jobsite first touches to the reserve and run the shared MillionVerifier CSV (website only).
---

Run the Jobsite Intelligence replenish routine. Work in D:\Workspace\jobsite-intelligence-repo (branch main). Read CLAUDE.md, AGENTS.md, ops/routines/README.md and docs/Outreach_Copy_v2.md, then follow ops/routines/JSI_Replenish.md exactly. New packets only through scripts/check_packet.py (0 flags); no copy for an unverified address. MillionVerifier is website only: never call its API and never read, print or store MILLIONVERIFIER_API_KEY; import with mv_bulk.py import-inbox and export with mv_bulk.py collect, and never move or delete files in D:\Workspace\austin-signage-repo\verify. Do not touch records planned or drafted for today or the next business day. Our lane only; never send, reply, forward or trash mail, never touch ASI items. Log one line to ops/routines/run_log.md. Alert the user only for the conditions in the README.
Usage measurement: as your very first action and again as your last before logging, call mcp__ccd_session_mgmt__get_usage (load it with ToolSearch if deferred) and end the run log line with "usage 5h A%->B%, weekly C%->D%; wall clock N min". If the tool is unavailable, say so in the log line.
```
