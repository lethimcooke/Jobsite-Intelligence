# JSI pre-send (Mon-Fri 6:55 AM ET; 8:35 AM ET once the JSI publisher is installed)

Goal: before the 9:00 AM ET (8:00 CT) send window, today's Jobsite manifest is published, valid and non-empty whenever
drafted rows exist. Read `README.md` here first. One live publisher at a time: once the JSI publisher
(`ops/sender/JsiPublisher.gs`) runs in Apps Script, this task only reports.

0. Weekend or `holidays.txt` date: log "no send day" and stop.
1. Save Gmail state (read-only), under `D:\Workspace\tools\scratch\routines\<today>\jsi\`:
   - `list_drafts` query `subject:"ASI-MANIFEST v1 <today>"` (DRAFT_VIEW_FULL, pageSize 5) to `gmail_manifests.json`
     (keep `id` and `subject`); ASI's manifest is in the same list: never open, edit or label it.
   - Export the Sender Log (Drive `download_file_content`, file `1qBaAWdp2rR9NVlNrL9qkaaKn-SVqh2xI7Et4Rj--4ro`, text/csv)
     and decode it with PY into `sender_log.csv`.
2. **Publisher installed** (the Sender Log has `JSI-PUBLISH` rows for any day): read today's `JSI-PUBLISH` rows.
   - `PUBLISHED n of m`: log it (with each `DROPPED` reason). If 3 or more were dropped, alert. Stop.
   - `MISSING`, `NOTHING`, `ERROR`, `PARTIAL` with no later `PUBLISHED`, or no row by 8:35 AM ET: alert with the rows, then
     continue at step 3 only if the decision there is BUILD and it is before 9:30 AM ET (the publisher will not publish
     over a manifest that exists). Otherwise stop.
3. `PY -I ops/routines/tools/presend_check.py --repo . --date <today> --id-prefix JI- --gmail-drafts <gmail_manifests.json> --sender-log <sender_log.csv> --out <scratch>\presend.json`
   - **KEEP** or **SENDING**: change nothing. Log it.
   - **NOTHING**: log the reason. If the reason is a missed close-out, alert.
   - **BUILD**: re-check the drafted S1s first:
     `PY -I ops/routines/tools/hook_gate.py --repo . --send-date <today> --include-drafted --out <scratch>\gate_<today>.json`
     (live Central Registry: ACTIVE, cited record date on the record, at most 45 days), then
     `PY -I ops/routines/tools/hold_stale.py --repo . --stale <scratch>\gate_<today>.stale.json --apply` (a held drafted row
     leaves today's plan; its Gmail draft stays untouched). Search Gmail (our lane) for each remaining recipient: a reply,
     bounce or opt-out is recorded per ops/README.md step 1 and the row is left out. Then
     `list_drafts` and `ji_ops.py reconcile-drafts`, and build:
     `PY scripts/ji_ops.py manifest <queues from the decision> --send-date <today> --out ops/manifests/<today>.json`
     (it refuses the whole list on any error; drop the failing records with a hold note and rebuild). Decode-check the
     BODY (gzip+base64 decodes to the manifest JSON; its SHA-256 equals the subject hash), `create_draft` to
     operations@asterfieldgroup.com with SUBJECT and BODY exactly, read it back and decode-check again, label it
     `JI/Do not send` (if the label call fails, say so in the log: the user adds it).
4. `PY -I ops/routines/tools/lf_fix.py "ops/queue/*.json" "ops/manifests/*.json"`, then update the tracker's send table row.
5. Append to `run_log.md`: `<today> <HH:MM> ET pre-send: <decision>, <n> entries, <reasons>; usage ...`. Alert only per README.
