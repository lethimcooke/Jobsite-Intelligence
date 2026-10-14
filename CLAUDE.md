# CLAUDE.md: Jobsite Intelligence

Asterfield Group's second cold-outreach business: new construction sites from TCEQ stormwater
records (TXR15 authorizations), sold as research to independent roll-off and portable toilet
haulers. Sister business to Austin Signage Intelligence (lethimcooke/Austin-Signage), which
runs the same engine. This file is a map; the files below win over anything summarized here.

## Sources of truth

- `Jobsite_Intelligence_Outreach_Tracker.md`: standing rules, batches, send log, engaged prospects.
  Update it on every send. It wins over `ops/rules.json` (change both in the same commit).
- `ops/README.md`: the daily operations loop (`scripts/ji_ops.py`). Tests: `python3 -m unittest discover -s tests`.
- `README.md`: launch plan, open decisions, test and go/no-go rule.
- `ops/rules.json`: validator rules (senders, signature, exact price line, footer, banned claims).
- `docs/Outreach_Copy_v2.md`: copy formulas (S1, S2, S5, E1, E2, E3, objection replies); replaces v1.
- `jobsite-report/README.md`: the free sample report (one per hauler; never attach an EXAMPLE).
- `AGENTS.md`: Codex as prospector only (codex/* branches, PRs to main, `check_packet.py` 0 flags).
- `docs/Business_Selection_Research.md`: why this business was picked, with sources.
- `scripts/pull_noi_sites.py`, `scripts/pull_haulers.py`: site and prospect pulls (stdlib Python).

## Hard limits (same as ASI, never change without the user)

- No email is sent except by the user or by the ASI Sender (a Google Apps Script in the user's Gmail,
  owned by the Austin-Signage repo), which sends only the S1, S2 and S5 drafts listed in that day's
  validated manifest (`scripts/ji_ops.py manifest`), from sites@ as "Houston Jobsite Intelligence".
  Claude never sends email. Engaged replies (E1-E3) stay with the user. The mailbox is shared with
  ASI: touch only sites@ threads, our own drafts and manifest, and JI/ labels. Daily share: 15 of 60.
  Daily operations: `ops/README.md`.
- `scripts/ji_ops.py` and `ops/sender/Code.gs` are owned by the ASI repo: never edit them here; tell
  the user if they need a change.
- No calls offered. No em dashes. Never use team@claimcascade.com.
- Business names only, never a person's name, including in site names.
- Every claim cites a public record; our read is labeled as our read. Never say work has
  started, a vendor is unselected, or work is open for bid.
- One company, one business: the ASI Sender enforces it at send time (every manifest's do-not-contact
  applies to all; a first email is refused if anyone at that domain already has email with us). Jobsite
  can't read ASI's repo; a sender SKIP for that reason means the company belongs to ASI: drop it.
- Contact forms (Option A): `scripts/fill_form.cjs` fills and screenshots; submit only after the user
  approves that form's filled screenshot in chat. CAPTCHA and no-solicitation forms stay manual. Log a
  form only with a confirmation screenshot. Only for haulers with no email.
- The mailbox total (60 sends a day) is shared with ASI; Jobsite's share is 15. First emails always
  go first; follow-ups wait. There is no separate first-email cap (user, Oct 14).

Scratch output (pulled CSVs) goes to the session scratchpad or `data/`, never next to scripts.

## Cloud environment

Skills live in the repo under `.claude/skills/` (agent-reach, claude-automation-recommender; see
`.claude/skills/PROVENANCE.md`). CLI tools come from `scripts/cloud_setup.sh`, pasted into the Jobsite
environment's Setup script field. If `agent-reach` or `mcporter` is missing, the setup script didn't run:
tell the user rather than installing ad hoc.

## Operations hand-off checks (October 14)

- E1: build the hauler-specific five-site PDF and draft in its thread the same day as its reply.
  Label JI/Send manually. Every hand-off: attach the PDF and set From to sites@asterfieldgroup.com.
  Never send the EXAMPLE PDF. Gmail creates drafts from operations@ by default.
- Engaged tracking: one row per prospect, with Company, Batch, Latest event (date, time CT,
  their words), Status and Required next action. Any reply freezes the cold sequence and sets
  the list status to Replied (...). E2 is sample +2 business days; E3 follows useful feedback
  or sample +5 business days. Do not imply positive feedback when none was received.
- Payment: Stripe Payment Link by default; Stripe invoice if requested; first list within a
  week of payment. Separate Jobsite Intelligence 30-day pilot, $500 product in Asterfield's
  Stripe account. Obtain the user-created link before the first E3; share it only after the
  buyer says yes to the E3, never in S1 or E1.
- S2 and S5 need approved batch copy with exact Re: S1 subjects, then convert, link-threads,
  plan, validate, draft and manifest. A prepared review file is not approved copy. No thread
  IDs or send evidence may be invented. Only generate a live manifest for actual Gmail drafts.
- Calendar: October 17, 2026 is Saturday. An October 15 S1 reaches +2 business days on
  October 19; an October 16 S1 reaches it on October 20. Use actual sent dates from the ledger.
- scripts/ji_ops.py and ops/sender/Code.gs remain ASI-owned and unchanged here.
