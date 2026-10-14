# AGENTS.md: instructions for Codex (and any non-Claude agent)

This repo runs a cold-outreach business selling verified early construction-project leads to
sign shops and adjacent trades in Austin, Houston, DFW and San Antonio. Claude runs operations
(Gmail drafts, logging, the tracker). **Codex's job here is prospecting only**, while Claude
is unavailable. `CLAUDE.md` is the full map; the rules below are what you need.

## Your role: prospector

You may:
- Pull public project data with the repo scripts (`scripts/pull_signals.js`,
  `scripts/pull_named_projects.py`) and the public sources in
  `Claude MDs/Prospecting_Method_v2.md` (TDLR TABS, data.texas.gov, Austin Socrata,
  San Antonio open data, FMCSA, a business's own website).
- Add **new** companies to `data/master_prospect_list.csv` (sign shops) or
  `data/adjacent_trades_list.csv` (access control, window film/shade, awnings, low-voltage/AV),
  with `outreach_status` = `Not contacted`, same columns as the existing rows.
- Write a hook packet: `outreach/<Name>_Hook_Packet.md`, in the same format as
  `outreach/Adjacent_T8_Hook_Packet.md` (numbered table, one project hook per row, source
  record ID such as `TABS2027001931`, fit line from the company's own site, email grade).
- Run `python3 scripts/check_duplicates.py outreach/<packet>.md`. It must print `0 flags`.
  Drop or replace any flagged row; never edit the lists to make a flag go away.

You must never:
- Change any existing row's `outreach_status`, or edit `data/outreach_results.csv`,
  `data/send_ledger.csv`, `data/do_not_contact.csv`, `ops/`, or the tracker's send tables.
- Write email copy (`*_S1_Copy.md`) or samples (`austin-signage-report/`). Those are other roles.
- Send email, submit contact forms, or contact anyone. Nothing is sent except by the user.
- Add a company in `data/do_not_contact.csv` or `data/master_prospect_exclusions.csv`.
- Use team@claimcascade.com anywhere.
- Guess an email. Grades: A = on the company's own site; B = pattern or directory with a
  mail-server (MX) check; B-dir = public registry (FMCSA) matched on phone, owner or domain.
  No email found: use the website contact form URL and say so.

## Quality bar (from the tracker; these decide whether a row is usable)

- Projects: a named business with a public filing (TABS, city permit, TABC, Comptroller),
  filed start in the future or recent. No national chains with their own sign programs
  (Olive Garden, Chipotle, Taco Bell and similar). Never claim construction started, a vendor
  is unselected, or work is open for bid. Web pages are leads; cite the filing.
- Prospects: an independent shop or trade firm with a real website or registry listing, in the
  metro of the project. A shop's own recent job (from permits or its site) is the best hook
  (Tier A); otherwise Tier B with a fit line from its listed work.
- Don't name individuals in hooks. No em dashes anywhere (use commas or semicolons).
- About 20 new contacts per working day is the pace the business needs.

## How to deliver

- Work on a branch named `codex/<short-topic>` and open a pull request to `main`. **Do not
  push to main.** Claude reviews and merges.
- PR description: packet name, metro, row count, tiers, the `check_duplicates.py` output, and
  anything you could not verify.
- Tests: `python3 -m unittest discover -s tests` must still pass.
