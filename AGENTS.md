# AGENTS.md: instructions for Codex (and any non-Claude agent)

Jobsite Intelligence sells new construction sites, found in TCEQ stormwater records (TXR15
authorizations), to independent roll-off and portable toilet haulers. Claude runs operations
(Gmail drafts, manifests, logging, the tracker). **Codex's job here is prospecting only.**
`CLAUDE.md` is the full map; the rules below are what you need.

## Your role: prospector

You may:
- Run the repo's pull scripts: `scripts/pull_noi_sites.py` (TCEQ sites), `scripts/enrich_haulers.py`
  (FMCSA haulers plus a scan of each hauler's own website) and `scripts/build_packet.py` (pairs each
  hauler with its nearest site). Metros are in `scripts/metros.py`.
- Read public sources: data.texas.gov (TCEQ Central Registry files, Comptroller permits), FMCSA
  Company Census, and a hauler's own website.
- Add **new** haulers to `data/hauler_list_<metro>.csv` with `outreach_status` = `Not contacted`,
  same columns as the existing rows.
- Write a hook packet, `outreach/<Batch>_Hook_Packet.md`, in the same format as
  `outreach/H1-H2_Hook_Packet.md`, plus its CSV `data/packet_<Batch>.csv`.
- Run `python3 scripts/check_packet.py data/packet_<Batch>.csv`. It must print `0 flags`. Drop or
  replace a flagged row; never edit the lists to make a flag go away.

You must never:
- Change any existing row's `outreach_status`, or edit `data/outreach_results.csv`,
  `data/send_ledger.csv`, `data/do_not_contact.csv`, `ops/`, or the tracker.
- Write email copy (`outreach/*_Copy*.md`) or samples (`jobsite-report/`). Those are other roles.
- Send email, submit contact forms, or contact anyone.
- Add a company that is on `data/do_not_contact.csv` or the tracker's Excluded list.
- Use team@claimcascade.com anywhere.
- Guess an email. Grades: A = on the hauler's own site; B-dir = filed with FMCSA on the hauler's
  own business domain. Free-mail only: mark `needs email pass`. No email at all: give the contact
  form URL and say so.

## Current priority (Oct 14)

Houston is the only live metro (the sender is "Houston Jobsite Intelligence"). Of 273 Houston
FMCSA candidates, only 22 passed the fit check with an email and 19 are already used, so:

1. **Houston second pass.** In `data/hauler_list_houston.csv`, recheck the rows with `fit` False
   that have an email (about 56) and the rows with no email (about 195). A row becomes fit only
   when the hauler's own site or listing says roll-off dumpsters or portable toilets for
   construction or commercial customers in the Houston area. Find emails on the hauler's own site.
   Record what you found in `notes`; set `fit` and `email`/`email_confidence` only from evidence.
2. **New Houston haulers** missed by FMCSA (portable toilet companies often aren't carriers):
   Comptroller sales-tax permits (NAICS 562111, 562119, 562991) in the Houston counties.
3. Only when the user says so: DFW or San Antonio (`enrich_haulers.py --metro DFW`).

## Quality bar

- Prospects: an independent, owner-run hauler (no national haulers, franchises, or fleets over
  60 power units) with a real website or registry listing, whose yard is in the metro.
- Sites: priority 1-2 TXR15 sites (commercial, industrial, institutional, amenity, multifamily)
  with a street address, authorized recently. A site is used once per batch.
- Never name individuals, including in site names (skip sites named for a person). Never claim
  work has started, a vendor is unselected, or work is open for bid. Web pages are leads; cite
  the TCEQ record (RN and authorization ID). No em dashes anywhere.
- About 15 new contacts per working day is the pace (Jobsite's share of the mailbox).

## How to deliver

- Work on a branch named `codex/<short-topic>` and open a pull request to `main`. **Do not push
  to main.** Claude reviews (runs `check_packet.py`) and merges.
- PR description: packet name, metro, row count, how many rows were rechecked and changed, the
  `check_packet.py` output, and anything you could not verify.
- Tests: `python3 -m unittest discover -s tests` must still pass.
- Scratch output (raw pulls) goes in `data/` or your own temp folder, never next to scripts.
