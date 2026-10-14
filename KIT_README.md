# JI Ops Kit v3: parity with ASI

Built by the ASI operations session, Oct 14, from Austin-Signage commit 16f6e92. v1 and v2 are
already installed (ji_ops.py, tests, daily loop, rules, settings, City Waste logged). v3 adds what
ASI has and Jobsite didn't. 22 tests pass.

## What's new in v3 (copy in, keeping paths)

| Kit path | What it is | Needed by |
| --- | --- | --- |
| `jobsite-report/` | The free sample report: ASI's template adapted for haulers (TCEQ sites, "Authorized" date, "From your yard" distance, hauling tags), `report-data-example.json` (format only, never send) and `README.md`. Tested: the example exports a clean 5-page PDF. | First "send it" reply (could be Oct 15) |
| `scripts/ji_ops.py` | Resynced: new `link-threads QUEUE` fills each follow-up's `reply_to_message_id` from the ledger (latest send to that recipient). | Oct 16 (City Waste S2) |
| `tests/test_ji_ops.py` | +1 test (City Waste S2 links to its S1). | Now |
| `scripts/outreach_stats.py` | Reply rates from `data/outreach_results.csv` (identical to ASI's). | After the first replies |
| `scripts/fill_form.cjs` | Contact-form filler (fills and screenshots; submits only with `--submit` after the user approves the screenshot; refuses CAPTCHA and no-solicitation forms). Uses `jobsite-report/node_modules` for Playwright. | Only for haulers with no email |
| `scripts/cloud_setup.sh` | Environment setup script (agent-reach, mcporter). The user pastes it into the Jobsite cloud environment's Setup script field. | Before using agent-reach |
| `.claude/skills/` | `agent-reach` (adapted to Jobsite) and `claude-automation-recommender`, with `PROVENANCE.md`. | With cloud_setup.sh |
| `.gitignore.add` | Now also ignores `jobsite-report/node_modules/`. | Now |

## Install

1. Copy the files in. Append `.gitignore.add` lines that aren't already in `.gitignore`.
2. `python3 -m unittest discover -s tests` (22 pass).
3. `cd jobsite-report && npm install && node export.js report-data-example.json EXAMPLE_check.pdf`
   must end with "Done". Delete `exports/EXAMPLE_check.pdf` afterwards; never attach an EXAMPLE.
4. Update `ops/README.md`:
   - step 2: follow-ups run `python3 scripts/ji_ops.py link-threads ops/queue/<Q>.json` after convert;
   - the E1 step: a sample is made per hauler in `jobsite-report/` and attached.
5. Update `CLAUDE.md` (see "CLAUDE.md fixes" below). Commit and push.

## CLAUDE.md fixes

- Replace "One company, one sequence across both businesses: check ASI's lists and do-not-contact
  file before any draft" with: "One company, one business: the ASI Sender enforces it at send time
  (every manifest's do-not-contact applies to all; a first email is refused if anyone at that domain
  already has email with us). Jobsite can't read ASI's repo; a sender SKIP for that reason means the
  company belongs to ASI: drop it."
- Add the sample report (`jobsite-report/README.md`), the contact-form rule (Option A: submit only after
  the user approves that form's filled screenshot in chat; CAPTCHA and no-solicitation forms stay manual;
  log a form only with a confirmation screenshot), and the cloud setup note (skills live in
  `.claude/skills/`; if agent-reach or mcporter is missing, the setup script didn't run: tell the user).

## Sync rule

The ASI repo owns `ji_ops.py` (a copy of `asi_ops.py`) and `ops/sender/Code.gs`. The report template,
stats, form tool, skills and setup script are Jobsite's own copies from here on: change them freely.
