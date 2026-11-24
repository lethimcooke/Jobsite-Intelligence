# JSI late reconcile (Mon-Fri 6:33 PM ET)

After the send window closes (6 PM ET). Weekend or `holidays.txt` date: log "no send day" and stop. Otherwise run
`JSI_CloseOut.md` section A again (Sender Log export, Gmail Sent from sites@, `reconcile_check.py` against
`ops/manifests/<today>.json` or `ops/prepared/<today>.json`, evidence and log for SENT entries only, skip and DROPPED
handling, UNCERTAIN resolution), plus:
- Entries still PENDING did not send today. Do not retry, rebuild or touch their drafts. Confirm each draft still exists
  and nothing is in Sent for that recipient; leave the record `drafted`. The next close-out's `plan` carries it into the
  next send day with its draft, so it goes out once. Alert if 3 or more did not send.
- Bounces since the morning: `from:(mailer-daemon OR postmaster) newer_than:1d`; log bounces for our addresses as
  `kind: gmail_bounce` evidence and add hard bounces to `data/do_not_contact.csv`.
- Commit and push only if this run wrote files. Append one line to `run_log.md` (with the usage measurement, README).
