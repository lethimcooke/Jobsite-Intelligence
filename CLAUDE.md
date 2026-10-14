# CLAUDE.md: Jobsite Intelligence

Asterfield Group's second cold-outreach business: new construction sites from TCEQ stormwater
records (TXR15 authorizations), sold as research to independent roll-off and portable toilet
haulers. Sister business to Austin Signage Intelligence (lethimcooke/Austin-Signage), which
runs the same engine. This file is a map; the files below win over anything summarized here.

## Sources of truth

- `README.md`: launch plan, open decisions, test and go/no-go rule.
- `ops/rules.json`: validator rules (senders, signature, exact price line, footer, banned claims).
- `docs/Outreach_Copy_v1.md`: copy formulas (S1, S2, S5, E1, E3).
- `docs/Business_Selection_Research.md`: why this business was picked, with sources.
- `scripts/pull_noi_sites.py`, `scripts/pull_haulers.py`: site and prospect pulls (stdlib Python).

## Hard limits (same as ASI, never change without the user)

- No email is sent except by the user. No calls offered. No em dashes.
- Business names only, never a person's name, including in site names.
- Every claim cites a public record; our read is labeled as our read. Never say work has
  started, a vendor is unselected, or work is open for bid.
- One company, one sequence across both businesses: check ASI's lists and do-not-contact file
  before any draft, and keep sites in ASI packets or samples out of this business.
- The mailbox total (60 sends a day) is shared with ASI. First emails always go first; follow-ups
  wait. There is no separate first-email cap (user, Oct 14).

Scratch output (pulled CSVs) goes to the session scratchpad or `data/`, never next to scripts.
