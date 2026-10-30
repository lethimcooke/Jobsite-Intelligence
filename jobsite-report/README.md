# Jobsite Intelligence: sample report

The free five-site sample a hauler gets in E1 when it says "send it". Adapted from ASI's
`austin-signage-report/` (same Asterfield design system, renderer and PDF export).

## Make a sample

1. Copy `report-data-example.json` to `report-data-<hauler>.json` and replace everything:
   - `report`: `city`, `preparedFor`, `territory`, `reportShortLabel` (e.g. "CITY WASTE SAMPLE"),
     `headline`, `supportingCopy`, `preparedDate`, `footerLine` (drop "EXAMPLE").
   - `projects`: 4-6 sites (5 is standard), each from a TCEQ construction stormwater record
     (`recordLabel` "TCEQ TXR...", `recordUrl` the data.texas.gov record), picked for that hauler's
     service area and services.
2. `npm install` once (Playwright; in the cloud, Chromium is preinstalled), then
   `node export.js report-data-<hauler>.json <Hauler>_Houston_Sample.pdf`.
   The PDF lands in `exports/`. The export fails on em dashes, wrong tags, missing fields, or any
   card section that is too long or short: rewrite the field, never the layout.
3. Attach it to the hauler's E1 (`attachments: ["jobsite-report/exports/<file>.pdf"]` in the queue);
   the E1 goes to the user to send by hand from sites@.

## Fields that differ from ASI

| Field | Jobsite use |
| --- | --- |
| `tag` | exactly `Roll-off`, `Portable toilets` or `Roll-off + portable toilets` |
| `dateLabel`, `filedStart` | `Authorized` and the authorization date on file |
| `valueLabel`, `value` | `From your yard` and e.g. `About 7 mi (our read)` (TCEQ records carry no value) |
| `likelyScope` | hauling scope, our read (label from `report.scopeLabel`) |

## House style (same rules as the emails)

- No em dashes. Business names only, never a person's name, including in site names.
- Every fact comes from the record; distance and scope are labeled as our read.
- Never say work has started, a hauler is unselected, or work is open for bid. "No hauler is named
  in the record" is fine; "no hauler chosen" is not.
- A site already used in an S1 hook to that hauler may be #1 (it's the job they asked about); don't
  give the same site to two competing haulers in the same week.
- `report-data-example.json` is a format example with placeholder distances. Never send it.
- **Live record check (Oct 30):** before a site goes in a sample, re-read its record on
  data.texas.gov and confirm the TXR15 authorization shows `ACTIVE`. A fresh pull can still carry a
  cancelled authorization (Yokogawa Park, TXR15R222, was CANCELLED). List every operator on file.
- **Not someone else's hook:** a site in any hauler's packet (`data/packet_*.csv`, by `site_rn`) is
  off limits for another hauler's sample unless it is the requesting hauler's own S1 site (#1).
- **No assumptions as facts:** don't call an operator "the owner" or name a contractor the record
  doesn't list. A site name built on a person's name (for example a road named after someone) is
  skipped, as in the emails.
- **Review before the user sends (user, Oct 30):** every sample and its E1 email go to the
  report creator for review (`jobsite-report/Report_Review_Brief.md`). Operations hands the user a
  ready-to-paste review prompt and never presents a sample as ready until the review is back.

## Verified cloud export (October 14)

If the default npm cache is read-only or the image has no compatible Playwright browser,
use a writable cache and Playwright's pinned browser download. Run from `jobsite-report/`:

```sh
npm ci --cache /tmp/ji-npm-cache --no-audit --no-fund
PLAYWRIGHT_BROWSERS_PATH=/tmp/ji-browser-cache npx playwright install chromium
PLAYWRIGHT_BROWSERS_PATH=/tmp/ji-browser-cache node export.js report-data-example.json EXAMPLE_v3_verification.pdf
```

This produced five pages and passed every card's line budget. The EXAMPLE is a validation
artifact only. For a real sample, replace the example data using the steps above, then attach
the hauler-specific PDF and set From to sites@asterfieldgroup.com in the engaged thread.
