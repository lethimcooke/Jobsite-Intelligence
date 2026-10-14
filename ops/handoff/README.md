# Operations hand-off, October 14, 2026

The baseline live repository is c803cfa. The attached JI_Codex_Prospector_Kit.zip is not the
requested JI_Ops_Kit_v3.zip. It contains neither KIT_README.md nor the v3 operations install
payload. Exact v3 installation and fix-list parity remain unverified. These changes use
existing live files and the user's explicit operational instructions, which override the
prospector-only role for this task. ASI-owned ji_ops.py and ops/sender/Code.gs are unchanged.

## Ready now

- Baseline: 22 tests passed. With nine packet-checker regression tests: 31 passed.
- Five-page EXAMPLE exported and passed the line-budget checks. Never send it to a prospect.
- City Waste's existing S2 copy is retained. Its live queue is linked to sent message
  1a13bb05fcc96d4f, thread 1a13ba7b4a2819dd; plan selects it for October 16; validation PASS.
  City_Waste_S2_Draft_Payload.json is the next command's actual draft payload, not a Gmail draft.
- Complete H1/H2 S2/S5 copy is in outreach/review/, pending approval. All four files pass
  check_copy.py: 9 H1 plus 8 H2 accounts per stage. Excluded Red Dog and Waste Falcon are omitted.
- Converted review queues are in ops/review/queues/. hook_type is a site type; subject-arm and
  legacy copy notes are separate metadata. Historical results and send evidence are unchanged.
- Checker CLI: 0 flags on the 16 unused, non-excluded existing S1 accounts. The historical
  19-row H1/H2 packet correctly reports three flags: City Waste already contacted, Red Dog and
  Waste Falcon excluded. See Historical_Packet_Check.txt; no lists were changed to clear flags.
- Statistics run successfully; historical hook notes no longer split the project-type groups.
- The tracker's engaged columns, freeze-on-reply rule and cadence are recorded. No reply is
  invented and no prospect status was changed. E2 is sample +2 business days, E3 after useful
  feedback or sample +5 business days; template timing now agrees with the tracker.

## Next operations steps

1. Check sites@ replies and bounces in Gmail first. Any reply freezes cold follow-ups. Record
   their exact words, date and time CT, status and next action in one engaged row per account;
   set the list status to Replied (...). Opt-outs also belong in do_not_contact.csv.
2. When a hauler asks for a sample, build its own five-site report that day from TCEQ records,
   matched to its yard and published services. Its S1 site may be #1. Use jobsite-report/README.md.
   Draft E1 in the hauler's thread and label JI/Send manually.
   Every hand-off: attach the PDF and set From to sites@asterfieldgroup.com.
3. Review and approve outreach/review/ copy. Keep existing live City Waste S2; do not also
   activate its duplicate review record. Other review records lack S1 sends and thread links.
   Validation correctly rejects those records. Do not change statuses to force a pass.
4. After actual S1 evidence is logged, regenerate or activate the approved follow-ups, run
   link-threads against the latest ledger, plan alongside due S1s, validate, create Gmail drafts,
   record their actual IDs, then generate the manifest. Nothing is marked sent without evidence.
   Existing October 15 S1 drafts and manifest are untouched. Recheck replies immediately before
   using City Waste's prepared payload; a later reply makes the snapshot obsolete.
5. No Gmail tools exist in this session. Draft creation, labeling, mailbox checks and an actual
   follow-up manifest are pending. No empty or fictional-draft manifest was generated.
6. Before the first E3, the user creates a Stripe Payment Link for
   "Jobsite Intelligence 30-day pilot, $500", a separate product in the Asterfield Stripe account.
   Record the URL in the tracker and rules. Share only after a hauler says yes to E3.
7. In the Jobsite environment's Setup script field, paste scripts/cloud_setup.sh. This session
   is attached to the Austin Signage environment, so its saved setup was not overwritten.
   Here agent-reach --version reports v1.5.0 and doctor --json completes: public web/RSS are OK,
   GitHub/Exa are unverified warnings and login-backed social channels are off or warnings.
   No fresh Jobsite environment or saved Jobsite setup publication is verified.
8. No contact forms were filled or submitted. Only haulers without email qualify; fill and
   screenshot first, obtain approval for that specific screenshot, then submit and save confirmation.
   KIT_README.md is missing, so its exact additional approval rules remain unverified.
9. AGENTS.md already exists and no new prospector was launched. Codex prospecting uses codex/*
   branches and review PRs; check_packet.py is a reviewer gate on new packets, not a way to approve
   historical packets or follow-ups to already-contacted companies.

## Dates requiring attention

October 17 is Saturday. October 15 S1 +2 business days is October 19; October 16 S1 +2 is
October 20. City Waste October 14 S1 +2 is October 16. S5 +13 weekdays is November 2, 3 or 4
for S1s on October 14, 15 or 16 respectively. Recompute from actual sends, not planned dates.
No extra holiday calendar has been applied.
