"""Tests for scripts/ji_ops.py against Jobsite's own ops/rules.json. Run: python3 -m unittest discover -s tests -v

Fixtures live in a temp directory; the real data/ files are never touched. The rules are read from
ops/rules.json and treated as reviewed here (the tests check the tooling, not the review).
"""
import copy
import csv
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import ji_ops as ops  # noqa: E402

with open(os.path.join(ROOT, "ops", "rules.json"), encoding="utf-8") as _f:
    RULES = json.load(_f)
RULES["reviewed"] = True
SIG = ops.signature(RULES, "Houston")
PRICE = RULES["standard_price_line"]
FOOT = ops.footer_text(RULES, "S1")
FIELDS = ["company", "email", "site_emails", "metro", "outreach_status"]


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


class Base(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        write_csv(os.path.join(self.d, "hauler_list_houston.csv"), FIELDS, [
            {"company": "CITY WASTE LP", "email": "sales@city-waste.com", "site_emails": "ops@city-waste.com",
             "metro": "Houston", "outreach_status": "Not contacted"},
            {"company": "Replied Hauling", "email": "info@replied.com", "site_emails": "", "metro": "Houston",
             "outreach_status": "Replied 2026-10-20"},
            {"company": "Blocked Roll-Off", "email": "x@blocked.com", "site_emails": "", "metro": "Houston",
             "outreach_status": "Not contacted"}])
        write_csv(os.path.join(self.d, "do_not_contact.csv"), ops.DNC_FIELDS, [
            {"company": "Blocked Roll-Off", "email": "sales@blocked.com", "domain": "blocked.com", "phone": "",
             "address": "", "reason": "no thanks", "date": "2026-10-20", "source": "test"}])
        write_csv(os.path.join(self.d, "outreach_results.csv"), ops.RESULTS_FIELDS, [])
        self.row = {"id": "JI-H1-S1-01", "seq": 1, "batch": "JI-H1", "company": "City Waste LP", "city": "Houston",
                    "stage": "S1", "from": "sites@asterfieldgroup.com", "to": "sales@city-waste.com",
                    "subject": "Central Office Annex, 1617 Lauder Rd",
                    "body": f"Hi City Waste team,\n\nTCEQ lists a filing.\n\n{PRICE}\n\nWant the free five-site sample?\n\n{SIG}",
                    "reply_to_message_id": None, "attachments": [], "hook_type": "", "status": "queued",
                    "draft": None, "footer": FOOT}

    def tearDown(self):
        shutil.rmtree(self.d)

    def errs(self, **over):
        r = {**copy.deepcopy(self.row), **over}
        return ops.validate_queue({"records": [r], "packet": None}, RULES, self.d, run_dup_check=False)

    def has(self, errs, text):
        self.assertTrue(any(text in e for e in errs), errs)


class Rules(Base):
    def test_valid_record(self): self.assertEqual(self.errs(), [])
    def test_signature_is_houston_jobsite(self):
        self.assertEqual(SIG, "Houston Jobsite Intelligence\nAsterfield Group\nsites@asterfieldgroup.com")
    def test_asi_alias_refused(self): self.has(self.errs(**{"from": "houston@asterfieldgroup.com"}), "wrong sender")
    def test_never_claimcascade(self):
        self.has(self.errs(body=self.row["body"].replace("TCEQ lists", "team@claimcascade.com lists")), "banned address")
    def test_em_dash(self): self.has(self.errs(body=self.row["body"].replace("a filing", "a filing — new")), "em dash")
    def test_banned_claim(self): self.has(self.errs(body=self.row["body"].replace("a filing", "a site that broke ground")), "banned phrase")
    def test_call_offer(self): self.has(self.errs(body=self.row["body"].replace("a filing", "a filing; quick call?")), "banned phrase")
    def test_price_line_once(self): self.has(self.errs(body=self.row["body"].replace(PRICE + "\n\n", "")), "price line")
    def test_refund_word(self): self.has(self.errs(body=self.row["body"].replace("a filing", "a filing, refund if not")), "refund")
    def test_short_signature(self): self.has(self.errs(body=self.row["body"].replace("\nAsterfield Group", "")), "signature")
    def test_do_not_contact(self): self.has(self.errs(to="x@blocked.com", company="Blocked Roll-Off"), "do-not-contact")
    def test_not_in_list(self): self.has(self.errs(to="new@nowhere.com"), "not in any prospect list")
    def test_alternate_email_is_in_list(self): self.assertEqual(self.errs(to="ops@city-waste.com"), [])
    def test_replied_blocks_cold_email(self): self.has(self.errs(to="info@replied.com"), "does not allow S1")
    def test_footer_required(self): self.has(self.errs(footer=""), "opt-out footer")
    def test_follow_up_needs_thread(self):
        self.has(self.errs(stage="S2", subject="Re: x"), "reply_to_message_id")


class Convert(Base):
    def test_jobsite_copy_format(self):
        p = os.path.join(self.d, "copy.md")
        body = f"Hi City Waste team,\n\nText.\n\n{SIG}\n\n{FOOT}"
        with open(p, "w") as fh:
            fh.write(f"# T\n\n## 1. H1: City Waste LP\n- To: sales@city-waste.com (A)\n- Subject: Annex, Lauder Rd\n\n```\n{body}\n```\n\n"
                     f"## 2. H2: Astro Waste Inc\n- To: info@astrowaste.com (B-dir)\n- Subject: S2\n\n```\n{body}\n```\n")
        q = ops.convert(p, "JI-H1", "Houston", "S1", RULES, title_prefix="H1")
        r = q["records"][0]
        self.assertEqual((len(q["records"]), r["id"], r["company"], r["to"]),
                         (1, "JI-H1-S1-01", "City Waste LP", "sales@city-waste.com"))
        self.assertTrue(r["body"].endswith(SIG))
        self.assertEqual(ops.payload(r)["body"].count(FOOT), 1)


class SharedMailbox(Base):
    """User, Oct 14: one mailbox, 60 a day; Jobsite plans to 15, ASI to 45; the ASI Sender enforces both."""
    def test_plan_stops_at_jobsite_share(self):
        q = {"records": [{**self.row, "id": f"JI-H1-S1-{i:02d}", "seq": i, "to": f"s{i}@example.com"} for i in range(19)]}
        picked, deferred = ops.plan_day([("q", q)], RULES, self.d, "2026-10-15")
        self.assertEqual((len(picked), len(deferred)), (15, 4))

    def test_manifest_for_the_sender(self):
        r = {**self.row, "status": "drafted"}
        r["draft"] = {"draft_id": "r-1", "message_id": "m", "thread_id": "t", "payload_sha256": ops.payload_hash(r)}
        m = ops.build_manifest([("q", {"records": [r]})], RULES, self.d, "2026-10-15")
        e = m["entries"][0]
        self.assertEqual((m["business"], m["max_total"], m["share"]), ("Jobsite Intelligence", 60, 15))
        self.assertEqual(m["aliases"], {"sites@asterfieldgroup.com": "Houston Jobsite Intelligence"})
        self.assertEqual((e["from_alias"], e["display_name"]), ("sites@asterfieldgroup.com", "Houston Jobsite Intelligence"))
        self.assertIn("blocked.com", m["dnc_domains"])
        subject, _ = ops.manifest_draft(m)
        self.assertTrue(subject.startswith("ASI-MANIFEST v1 2026-10-15 "))   # the shared sender's format
        self.assertIs(m["dry_run_only"], False)
        test = ops.build_manifest([("q", {"records": [r]})], RULES, self.d, "2026-10-15", dry_run_only=True)
        self.assertIs(test["dry_run_only"], True)   # a test manifest is only checked, never sent

    def test_manifest_refuses_engaged_and_unrecorded(self):
        r = {**self.row, "status": "drafted", "draft": None}
        with self.assertRaises(ops.OpsError):
            ops.build_manifest([("q", {"records": [r]})], RULES, self.d, "2026-10-15")


class Logging(Base):
    def test_log_sets_status_and_results(self):
        q = {"records": [{**self.row, "status": "drafted",
                          "draft": {"draft_id": "r-1", "message_id": "m0", "thread_id": "t1", "payload_sha256": "x",
                                    "created_at": "2026-10-15T13:00:00+00:00"}}]}
        ev = [{"outreach_id": "JI-H1-S1-01", "kind": "gmail_sent", "evidence_id": "m1", "thread_id": "t1",
               "sent_at": "2026-10-15T14:00:00+00:00", "from": "sites@asterfieldgroup.com", "to": "sales@city-waste.com"}]
        plan = ops.plan_log(q, ev, self.d, rules=RULES)
        ops.apply_log(q, plan, self.d, None)
        with open(os.path.join(self.d, "hauler_list_houston.csv"), newline="", encoding="utf-8") as f:
            rows = {r["email"]: r for r in csv.DictReader(f)}
        self.assertEqual(rows["sales@city-waste.com"]["outreach_status"], "S1 sent 2026-10-15 (sites@)")
        with open(os.path.join(self.d, "outreach_results.csv"), newline="", encoding="utf-8") as f:
            self.assertEqual([r["base"] for r in csv.DictReader(f)], ["Houston"])
        self.assertEqual(q["records"][0]["status"], "sent_confirmed")


class LinkThreads(Base):
    def test_s2_replies_to_the_logged_s1(self):
        write_csv(os.path.join(self.d, ops.LEDGER), ops.LEDGER_FIELDS, [
            {**{k: "" for k in ops.LEDGER_FIELDS}, "outreach_id": "JI-H1-S1-01", "kind": "gmail_sent",
             "evidence_id": "1a13bb05fcc96d4f", "thread_id": "1a13ba7b4a2819dd", "to": "sales@city-waste.com",
             "sent_at": "2026-10-14T18:32:56+00:00"}])
        q = {"records": [{**self.row, "id": "JI-H1-S2-01", "stage": "S2", "subject": "Re: Central Office Annex, 1617 Lauder Rd"}]}
        ops.link_threads(q, self.d, RULES)
        self.assertEqual(q["records"][0]["reply_to_message_id"], "1a13bb05fcc96d4f")


if __name__ == "__main__":
    unittest.main()
