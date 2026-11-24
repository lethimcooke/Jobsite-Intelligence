# JSI replenish (Mon, Wed, Fri 4:55 PM ET)

Separate from sending: adds send-ready first touches to the reserve without touching records planned or drafted for today
or the next business day. Scaled from ASI (5 first touches a day instead of 15): **target 25 newly ready first touches
a week** (about 8 a run); **reserve line 50** ready (10 business days).

**Run targets.** Two numbers, both logged:
- **8 send-ready first touches added**, all from usable addresses (MillionVerifier ok, or published on the hauler's own
  site under the tracker's rules). Step 1 comes first and is the main source.
- **150 new addresses found for verification (user, Nov 24, same as ASI; was 20).** Never skip or cut the search short
  because of an unverified backlog: finding addresses for the user to verify is this routine's main job, and a big backlog
  is fine. Stop only at the target, the time cap, or 5-hour usage over 90%. Hauler-first: FMCSA and Comptroller pulls (`scripts/enrich_haulers.py`,
  `scripts/pull_haulers.py`), then Exa (two queries per service and area, `numResults=10`), then Crawl4AI for own-site
  emails. A hauler qualifies when its email is on its own site, it publishes roll-off, dumpster or portable toilet
  service, and a fresh TCEQ site sits in an area it publishes.
- **No copy before verification.** An unverified address gets a `data/to_verify_<today>.csv` row (columns email, company,
  metro, site: the matched site's RN) and nothing else: no copy, no queue row.
- **Reserve full (ready at or over 50): focus mode.** Still run, but only where leads come easiest: read
  `data/research/yield.csv` and work the 2 service and area pairs with the most own-site emails per search over the last
  3 runs (a pair with no history counts as average). Targets drop to 100 new addresses (user, Nov 24); step 1 still runs first; stop at
  45 minutes. Every run appends one row per pair it worked to `data/research/yield.csv` (columns date, metro, service,
  area, searches, own_site_emails, send_ready_added; create it with that header if missing).
Work until both targets are met or the run reaches 2 hours (45 minutes in focus mode), as ASI. If it ends short, the run log line
starts with "SHORT:" plus the counts and says what ran out (fresh ACTIVE sites, haulers with an own-site email, or
verified haulers to match); that line is an alert.

Read `README.md` here, `AGENTS.md` (prospector rules), `docs/Outreach_Copy_v2.md` (S1) and the tracker's site rules
(45-day window, ACTIVE, priority 1-2, not named for a person, used once). Claude buys nothing.
PY = `D:\Workspace\austin-signage-repo\local\tools\asi-venv\Scripts\python.exe`. Scratch: `D:\Workspace\austin-signage-repo\local\tools\scratch\routines\<today>\jsi\replenish\`.
Call `get_usage` first (README, Logging).

1. **Recover what is close to ready** (cheapest):
   - Verified haulers with no live first touch (`data/verified_emails.csv` Deliverable, older `data/verified_*.csv` ok, own-site
     catch-all under the tracker's rule): match each to a fresh site from step 2, write the S1.
   - Held stale rows (`status: held_stale`): a fresh ACTIVE site in the same hauler's published area -> rewrite the S1 with
     the new hook, convert into a new queue `ops/queue/JI-<B>R-S1.json` and leave the old row held.
2. **Sites:** `PY scripts/pull_noi_sites.py --metro Houston --days 45 --out <scratch>\sites_houston_<today>.csv`. Keep priority
   1-2, a business operator, not person-named, record date at most 30 days old today (so it survives to a send day inside
   45), and not used in any `data/packet_*.csv`. Check each kept site live with `node ops/routines/tools/hook_recheck.js <TXR15 IDs>`
   (ACTIVE only; PENDING sites are rechecked next run). DFW sites and haulers wait until a DFW sender alias exists.
3. **Haulers for the kept sites:**
   - FMCSA and Comptroller first (`enrich_haulers.py`, `pull_haulers.py`); then Exa (PowerShell only):
     `& (Join-Path (npm prefix -g) 'mcporter.ps1') call exa.web_search_exa query="roll-off dumpster rental <area> TX" numResults=10`
     and `"portable toilet rental <area> TX"`. Time each search; save raw output under scratch.
   - Own-site evidence with Crawl4AI: `D:\Workspace\austin-signage-repo\local\tools\crawl4ai-venv\Scripts\python.exe ops/routines/tools/crawl_sites.py <scratch>\sites <home, services and contact URLs>`.
     Services and areas from the hauler's own pages; email only if published there (grade A), else the contact form URL
     (Option A forms stay with the user, CLAUDE.md). Skip national haulers, franchises and anyone in another business's list.
4. **Packet and dedupe:** `PY scripts/build_packet.py ...` (or by hand in its columns) into `data/packet_<B>.csv` (batch `<B>` =
   next H number), then `PY scripts/check_packet.py data/packet_<B>.csv`: 0 flags, or drop the flagged rows (never edit
   lists to clear a flag).
5. **Verification and copy:** rows with usable evidence get the S1 now: `PY scripts/write_s1.py --packet data/packet_<B>.csv --metro Houston --out outreach/<B>_S1_Copy.md`
   (review the names table), `check_copy.py ... --stage S1`, `check_packet.py outreach/<B>_S1_Copy.md` (0 flags), then
   `ji_ops.py convert outreach/<B>_S1_Copy.md --batch JI-<B> --city Houston --stage S1 --title-prefix <B> --out ops/queue/JI-<B>-S1.json`,
   fill `hook_type`, `validate` PASS for the next send day. Not planned here. Rows without evidence go to
   `data/to_verify_<today>.csv` (append if it exists) with no copy and no queue row; add the hauler to
   `data/hauler_list_houston.csv` as `Not contacted`.
5b. **MillionVerifier: website only, one CSV for ASI and Jobsite (user, Nov 20).** Never call the API; the tool has no API
   code and never reads `MILLIONVERIFIER_API_KEY`.
   - Import first: `PY -I ops/routines/tools/mv_bulk.py --repo . import-inbox` (every results file in
     `D:\Workspace\austin-signage-repo\verify\inbox\` and `inbox\done\` without a Jobsite marker; only addresses in Jobsite's open batches are
     taken, ASI's rows are ignored; it writes `<file>.jsi_imported.txt` beside each file). Never move or delete files there:
     ASI moves a file to `done\` once both businesses have imported it. Then write copy (step 5) for every new ok row, and
     for catch-all rows whose address is on the hauler's own site, matched to its site.
   - Export last: `PY -I ops/routines/tools/mv_bulk.py --repo . collect --max 1000` appends the new addresses to
     `D:\Workspace\austin-signage-repo\verify\outbox\<today>.csv` (columns `email,business`, business `JSI`; it creates the file with that header
     if missing and never repeats an address already there; an open, unverified batch never blocks a new one). The run report ends with: "Verify
     `D:\Workspace\austin-signage-repo\verify\outbox\<today>.csv` on the MillionVerifier website and save the results file in
     `D:\Workspace\austin-signage-repo\verify\inbox\`." Log the batch id, rows, and per-result counts of each import.
6. **Record the run:** commit and push (only files this run changed), then one line in `run_log.md`: sites pulled and kept,
   haulers found (Exa searches and seconds per search), send-ready added (verified), unverified rows queued, ready reserve
   and business days, week's total against 25, mode (full or focus), usage. Alert when SHORT (fewer new addresses than the
   run's target), or when the week's added ready rows are under 15 by Friday. An unverified backlog is not an alert; the
   run report always ends with the verify line.
