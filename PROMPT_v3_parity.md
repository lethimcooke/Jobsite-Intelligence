Kit v3 for Jobsite operations (attached JI_Ops_Kit_v3.zip): parity with ASI. Read KIT_README.md, install the v3 files, run the tests (22 pass) and the example export, apply the CLAUDE.md fixes, then commit and push. Then do the items below in this order. Each says when it's needed.

**By Oct 15 (first possible "send it" reply)**
1. **Sample report:** `jobsite-report/` is installed and the example exports. When a hauler says yes, build its sample the same day:
   - 5 TCEQ sites in its service area, picked for its services; the site from its S1 hook can be #1;
   - follow `jobsite-report/README.md`, export the PDF, and draft the E1 from docs/Outreach_Copy_v2.md in the hauler's thread;
   - label the draft JI/Send manually and tell the user to attach the PDF and set From to sites@ before sending.

   Reminder from ASI on Oct 14: an engaged email went out from operations@ because From wasn't switched. Say it in every hand-off.
2. **Engaged tracking:** keep the tracker's Engaged prospects table the way ASI does, one row per prospect:
   - columns: Company | Batch | Latest event (date, time CT, their words) | Status | Required next action;
   - cadence: E1 the same day as the reply, E2 at sample + 2 business days, E3 after useful feedback or at sample + 5 business days;
   - any reply freezes the silent sequence, and list status becomes "Replied <date> (...)".

**By Oct 16**
3. **Follow-up copy:** every S2 and S5 needs an approved copy file per batch, in the same format as the S1 file:
   - each section is `## N. H1: Company`, then `- To:`, then `- Subject: Re: <exact S1 subject>`, then a fenced body ending with the three-line signature;
   - City Waste's S2 (`outreach/JI-H1_S2_Copy.md`, #1 only, thread 1a13ba7b4a2819dd) is due Oct 16;
   - the Oct 15 batch's S2s are due Oct 17, and S5 comes at S1 + 13 business days.

   Write them yourself from Outreach_Copy_v2.md, or give the user a copywriter prompt. Then: convert, `link-threads`, plan, validate, draft, manifest.

**Before the first E3**
4. **Payment:** ask the user to create a Stripe Payment Link, "Jobsite Intelligence 30-day pilot, $500". Same Asterfield Stripe account as ASI, a separate product so revenue stays split by business.
   - Record the link in the tracker's standing rules: "Payment: Stripe Payment Link by default; Stripe invoice if the buyer asks; first list within a week of payment."
   - Send it only after the hauler says yes to the E3, never in S1 or E1.

**When convenient (not blocking)**
5. **Packet checker:** write `scripts/check_packet.py` (Jobsite's equivalent of ASI's check_duplicates.py) and run it on every new packet. It flags any row whose company, email or domain:
   - is on data/do_not_contact.csv;
   - has a list status other than Not contacted;
   - repeats another row's domain within the packet;
   - is on the excluded list.
6. **Stats:** `python3 scripts/outreach_stats.py` reads data/outreach_results.csv. Fill each queue record's `hook_type` (site type) so the stats group by it.
7. **Cloud setup:** ask the user to paste `scripts/cloud_setup.sh` into the Jobsite environment's Setup script field, then verify with `agent-reach --version` and `agent-reach doctor --json`.
8. **Contact forms:** `scripts/fill_form.cjs` only under the approval rule in KIT_README.md. Only for haulers with no email.
9. **Codex prospector:** only if the user wants one. Write `AGENTS.md` from `docs/reference_from_ASI/ASI_AGENTS.md`, adapted to haulers, TCEQ and FMCSA:
   - prospecting only, on `codex/*` branches, with PRs to main;
   - never touches statuses, the ledger, copy, samples or anything that sends;
   - review each PR with check_packet.py before merging.

The sync rule stands: ASI owns ji_ops.py and ops/sender/Code.gs. Everything else in v3 is yours to adapt.
