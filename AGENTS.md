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

## Current priority (Oct 14): find new Houston haulers by public research

Projects are not the bottleneck: TCEQ adds about 745 construction sites a month statewide and
Houston had 84 usable ones in three weeks. Buyers are. Of 273 Houston FMCSA candidates only 22 were
usable and 19 are already in sequence. Target: **at least 60 new fit Houston haulers** (four weeks
of first emails at 15 a day), delivered in packets of about 15.

Research sources, in order. Every row cites where it came from (`notes`: source URL or record ID):
1. **Public directories and registries** for roll-off dumpster and portable toilet companies in
   Harris, Fort Bend, Montgomery, Brazoria and Galveston counties: city hauler permit or
   registration lists (check whether City of Houston and the suburbs publish permitted commercial
   solid waste haulers), Comptroller sales-tax permits (NAICS 562111, 562119, 562991 on
   data.texas.gov), Portable Sanitation Association International member directory, chamber of
   commerce and BBB business listings, and plain web search ("roll off dumpster rental Katy",
   "portable toilet rental Conroe", one search per suburb).
2. **The hauler's own website**: confirm it rents roll-offs or portable toilets to contractors or
   commercial customers, its service area includes the Houston area, and find its published email.
3. **Recheck the existing list**: rows in `data/hauler_list_houston.csv` with `fit` False (about 56
   with an email, about 195 without), using the same website check.

Skip: national haulers and franchises (WM, Republic, WCA, GFL, Waste Connections, Budget Dumpster,
United Site Services and similar), brokers and lead-gen sites that don't own containers, junk
removal only, residential-only, and anyone already in `data/packet_H1-H2.csv`.

Only when the user says so: DFW or San Antonio (`enrich_haulers.py --metro DFW`).

## Quality bar

- Prospects: an independent, owner-run hauler (no national haulers, franchises, or fleets over
  60 power units) with a real website or registry listing, whose yard or service area is in the metro.
  New rows need at least: company, email (graded), website, yard or service-area city, services
  (roll-off, portable toilets, both), source.
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
