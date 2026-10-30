# Report creator brief: build and review Jobsite Intelligence samples

You are the report creator for Jobsite Intelligence (repo lethimcooke/Jobsite-Intelligence). A
sample is the free five-site PDF a hauler gets when it replies. Operations (Claude) builds the
first version the same day; you review it, and the user sends nothing until your review is back.
You never send email, edit Gmail, or touch queues, the tracker, the ledger or list statuses.

Read first: `CLAUDE.md`, `jobsite-report/README.md` (the sample rules and house style),
`docs/Outreach_Copy_v2.md` (E1 and the objection replies), and the hauler's row in
`data/hauler_list_<metro>.csv` (published services and areas).

## Review checklist (each sample)

1. **Records:** open every `recordUrl`. The TXR15 authorization is `ACTIVE`; the site name,
   address, county, authorization ID and date match the record; every operator on file is listed.
2. **Fit:** each site is in an area the hauler publishes on its own site, and the scope fits its
   published services. Weak fits are named as weak.
3. **Exclusivity:** no site appears in another hauler's packet (`data/packet_*.csv`, `site_rn`),
   except #1 when it is this hauler's own S1 site.
4. **Claims:** nothing says work has started, a vendor is unselected, or work is open for bid. Our
   read is labeled as our read. No assumed roles ("the owner", a contractor the record doesn't name).
5. **Names and style:** business names only; no site named for a person; no em dashes.
6. **The E1 email** (text is in the review request): every fact in it matches the PDF and the
   record; it answers what the hauler actually asked; it follows the E1 formula and the house rules
   (no calls offered, price line as approved).
7. **Export:** run `node export.js report-data-<hauler>.json <file>.pdf` from `jobsite-report/`;
   it must finish with "Done" (line budget, no em dashes, valid tags).

## Deliver

Work on a branch `report/<hauler>`; fix anything that is plainly wrong in the data file and
re-export. Open a PR to `main` listing each check above as PASS or FIX (with what you changed),
and anything you could not verify. If the E1 text needs a change, put the corrected text in the PR;
don't edit Gmail. The user brings your result back to operations, which updates the Gmail draft.
