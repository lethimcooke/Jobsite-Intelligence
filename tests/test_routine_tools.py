"""Tests for the Jobsite routine tools (ops/routines/tools) and the JSI publisher (ops/sender/JsiPublisher.gs).

Run: python3 -m unittest discover -s tests
Each test builds a throwaway repo in a temp directory (a copy of scripts/ji_ops.py, ops/rules.json, holidays.txt and
the sender files, plus fixture lists, ledger and queues) and runs the tools against it as the routines do
(`python -I <tool> --repo <tmp>`). The real data/ and ops/ files are never touched. No network: hook checks replay
saved facts (--facts). Node tests (publisher) are skipped when node is not installed.
"""
import base64, csv, gzip, hashlib, json, os, shutil, subprocess, sys, tempfile, unittest
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "ops", "routines", "tools")
sys.path.insert(0, TOOLS); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import jsi_common as jc  # noqa: E402
import ji_ops as ops  # noqa: E402

with open(os.path.join(ROOT, "ops", "rules.json"), encoding="utf-8") as _f:
    RULES = json.load(_f)
SIG = ops.signature(RULES, "Houston")
PRICE = RULES["standard_price_line"]
FOOT = ops.footer_text(RULES, "S1")
NODE = shutil.which("node")
LIST_FIELDS = ["company", "email", "site_emails", "metro", "outreach_status"]
LEDGER_FIELDS = ops.LEDGER_FIELDS


def write_csv(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)


def s1_body(company, auth="TXR1594ZB", when="with a record date of November 5"):
    return (f"Hi {company} team,\n\nTCEQ's Central Registry lists a construction stormwater authorization ({auth}) {when} "
            f"for Cypress Fields Business Park at 15101 Cypress Fields Ave, Cypress in Harris County.\n\n"
            f"It's in Cypress, one of the areas you serve; that's our read, not the filing.\n\n{PRICE}\n\n"
            f"Want five sites like this in your service area, free?\n\n{SIG}")


def s1(i, to, company, **over):
    r = {"id": f"JI-T1-S1-{i:02d}", "seq": i, "batch": "JI-T1", "company": company, "city": "Houston", "stage": "S1",
         "from": "sites@asterfieldgroup.com", "to": to, "subject": "Cypress Fields Business Park", "body": s1_body(company),
         "reply_to_message_id": None, "attachments": [], "hook_type": "commercial", "status": "queued", "draft": None, "footer": FOOT}
    r.update(over)
    return r


def ledger_row(oid, stage, to, company, sent_at, kind="gmail_sent"):
    return {"logged_at": sent_at, "outreach_id": oid, "batch": oid.rsplit("-", 2)[0], "stage": stage, "city": "Houston",
            "company": company, "kind": kind, "evidence_id": "m-" + oid, "sent_message_id": "", "thread_id": "t-" + oid,
            "sent_at": sent_at, "from": "sites@asterfieldgroup.com", "to": to, "form_url": "", "confirmation_ref": "", "note": ""}


class Repo(unittest.TestCase):
    """A throwaway Jobsite checkout."""
    def setUp(self):
        self.r = tempfile.mkdtemp()
        for rel in ("scripts/ji_ops.py", "ops/rules.json", "ops/routines/holidays.txt",
                    "ops/sender/Code.gs", "ops/sender/JsiPublisher.gs", "ops/sender/hook_facts.cjs"):
            os.makedirs(os.path.dirname(os.path.join(self.r, rel)), exist_ok=True)
            shutil.copy(os.path.join(ROOT, rel), os.path.join(self.r, rel))
        os.makedirs(os.path.join(self.r, "ops", "queue"))
        write_csv(self.p("data/hauler_list_houston.csv"), LIST_FIELDS, [
            {"company": "A Roll-Off", "email": "info@aroll.com", "site_emails": "", "metro": "Houston", "outreach_status": "Not contacted"},
            {"company": "B Waste", "email": "sales@bwaste.com", "site_emails": "", "metro": "Houston", "outreach_status": "Not contacted"},
            {"company": "C Portables", "email": "c@cport.com", "site_emails": "", "metro": "Houston", "outreach_status": "Not contacted"},
            {"company": "D Dumpsters", "email": "d@ddump.com", "site_emails": "", "metro": "Houston", "outreach_status": "S1 sent 2026-11-23 (sites@)"},
            {"company": "E Hauling", "email": "e@ehaul.com", "site_emails": "", "metro": "Houston", "outreach_status": "S1 sent 2026-11-24 (sites@)"},
            {"company": "F Replied", "email": "f@frep.com", "site_emails": "", "metro": "Houston", "outreach_status": "Replied 2026-11-25 (asked for sample)"},
            {"company": "G Bounced", "email": "g@gbounce.com", "site_emails": "", "metro": "Houston", "outreach_status": "S1 sent 2026-11-23 (sites@)"}])
        write_csv(self.p("data/do_not_contact.csv"), ops.DNC_FIELDS, [
            {"company": "Opted Out Co", "email": "no@optout.com", "domain": "optout.com", "phone": "", "address": "",
             "reason": "no thanks", "date": "2026-11-01", "source": "test"}])
        write_csv(self.p("data/outreach_results.csv"), ops.RESULTS_FIELDS, [])
        write_csv(self.p("data/send_ledger.csv"), LEDGER_FIELDS, [
            ledger_row("JI-T0-S1-01", "S1", "d@ddump.com", "D Dumpsters", "2026-11-23T15:00:00+00:00"),
            ledger_row("JI-T0-S1-02", "S1", "e@ehaul.com", "E Hauling", "2026-11-24T15:00:00+00:00"),
            ledger_row("JI-T0-S1-03", "S1", "f@frep.com", "F Replied", "2026-11-23T15:00:00+00:00"),
            ledger_row("JI-T0-S1-04", "S1", "g@gbounce.com", "G Bounced", "2026-11-23T15:00:00+00:00"),
            ledger_row("JI-T0-S1-04", "S1", "g@gbounce.com", "G Bounced", "2026-11-23T15:05:00+00:00", kind="gmail_bounce")])

    def tearDown(self):
        shutil.rmtree(self.r, ignore_errors=True)

    def p(self, rel):
        path = os.path.join(self.r, *rel.split("/")); os.makedirs(os.path.dirname(path), exist_ok=True); return path

    def queue(self, name, records, packet=None):
        q = {"batch": "JI-T1", "city": "Houston", "stage": records[0]["stage"], "packet": packet, "created_at": "2026-11-20T00:00:00+00:00", "records": records}
        with open(self.p(f"ops/queue/{name}.json"), "w", encoding="utf-8", newline="\n") as fh: json.dump(q, fh, indent=2)

    def read_queue(self, name):
        with open(self.p(f"ops/queue/{name}.json"), encoding="utf-8") as fh: return json.load(fh)

    def tool(self, name, *args, ok=True):
        r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, name), "--repo", self.r, *args],
                           capture_output=True, text=True, encoding="utf-8")
        if ok: self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def drafted(self, rec, day):
        rec = dict(rec, status="drafted", planned_for=day)
        rec["draft"] = {"draft_id": "r-" + rec["id"], "message_id": "m-" + rec["id"], "thread_id": "t-" + rec["id"], "payload_sha256": ops.payload_hash(rec)}
        return rec


class Hook(unittest.TestCase):
    def test_both_phrasings(self):
        h = jc.hook_for(s1_body("A"), "", None, date(2026, 11, 25))
        self.assertEqual((h["kind"], h["id"], h["cited"]), ("NOI", "TXR1594ZB", "2026-11-05"))
        old = jc.hook_for(s1_body("A", "TXR1573ZR", "dated October 8"), "", None, date(2026, 11, 2))
        self.assertEqual((old["id"], old["cited"]), ("TXR1573ZR", "2026-10-08"))

    def test_year_rolls_back_across_new_year(self):
        h = jc.hook_for(s1_body("A", when="with a record date of December 20"), "", None, date(2027, 1, 12))
        self.assertEqual(h["cited"], "2026-12-20")

    def test_no_hook_raises(self):
        with self.assertRaises(ValueError): jc.hook_for(s1_body("A", "TXR", "dated October 8"), "", None, date(2026, 11, 2))
        with self.assertRaises(ValueError): jc.hook_for(s1_body("A", when="last month"), "", None, date(2026, 11, 2))

    def test_packet_line_supplies_a_missing_authorization(self):
        h = jc.hook_for(s1_body("A", "(see record)", "dated October 8"), "H1,A,info@aroll.com,TXR1599ZS,", None, date(2026, 11, 2))
        self.assertEqual(h["id"], "TXR1599ZS")

    def test_rule(self):
        H = {"kind": "NOI", "id": "TXR1594ZB", "cited": "2026-11-05"}
        act = {"rows": [{"status": "ACTIVE", "date": "2026-11-05"}, {"status": "ACTIVE", "date": "2026-08-07"}]}
        self.assertEqual(jc.noi_problem(H, act, "2026-11-25"), "")
        self.assertEqual(jc.noi_problem(H, act, "2026-12-20"), "")                       # day 45 still passes
        self.assertIn("over 45", jc.noi_problem(H, act, "2026-12-21"))                   # day 46 (786 Dumpsters case)
        self.assertIn("not on the live record", jc.noi_problem(dict(H, cited="2026-10-08"), act, "2026-11-13"))   # Hero Portables case
        self.assertIn("is TERMINATED", jc.noi_problem(H, {"rows": [{"status": "TERMINATED", "date": "2026-11-05"}]}, "2026-11-25"))
        self.assertIn("not found", jc.noi_problem(H, {"rows": []}, "2026-11-25"))
        self.assertIn("unavailable", jc.noi_problem(H, {"unavailable": True}, "2026-11-25"))
        self.assertEqual(jc.noi_problem({"kind": "NONE"}, {}, "2026-11-25"), "")

    @unittest.skipUnless(NODE, "node not installed")
    def test_python_rule_equals_the_publisher_rule(self):
        cases = []
        for cited in ("2026-11-05", "2026-10-08", "2026-09-24"):
            for fact in ({"rows": [{"status": "ACTIVE", "date": "2026-11-05"}, {"status": "ACTIVE", "date": "2026-09-24"}]},
                         {"rows": [{"status": "INACTIVE", "date": cited}]}, {"rows": []}, {"unavailable": True}):
                for day in ("2026-11-08", "2026-11-25", "2026-12-21"):
                    cases.append([{"kind": "NOI", "id": "TXR1594ZB", "cited": cited}, fact, day])
        js = ("const S=require(process.argv[1]+'/Code.gs');global.CFG=S.CFG;const P=require(process.argv[1]+'/JsiPublisher.gs');"
              "const c=JSON.parse(require('fs').readFileSync(0,'utf8'));console.log(JSON.stringify(c.map(x=>P.noiProblem_(x[0],x[1],x[2]))));")
        out = subprocess.run([NODE, "-e", js, os.path.join(ROOT, "ops", "sender")], input=json.dumps(cases), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout), [jc.noi_problem(*c) for c in cases])

    def test_business_days_skip_thanksgiving(self):
        hol = jc.holidays(ROOT)
        self.assertEqual(jc.next_bd(date(2026, 11, 25), hol), date(2026, 11, 30))
        self.assertEqual(jc.bd_add(date(2026, 11, 24), 2, hol), date(2026, 11, 30))


class Followups(Repo):
    def test_due_dates_skip_the_holiday_and_exclusions(self):
        out = self.p("due.json")
        self.tool("followups_due.py", "--date", "2026-12-01", "--out", out)
        with open(out, encoding="utf-8") as fh: res = json.load(fh)
        due = {x["to"]: x for x in res["due"]}
        self.assertEqual(due["d@ddump.com"]["due"], "2026-11-25")          # Mon Nov 23 + 2
        self.assertEqual(due["e@ehaul.com"]["due"], "2026-11-30")          # Tue Nov 24 + 2, over Thanksgiving
        self.assertNotIn("f@frep.com", due)                                # replied
        self.assertNotIn("g@gbounce.com", due)                             # bounced
        self.assertEqual(res["summary"]["by_stage"], {"S2": 2})

    def test_s5_after_s2(self):
        rows = [ledger_row("JI-T0-S2-01", "S2", "d@ddump.com", "D Dumpsters", "2026-11-25T15:00:00+00:00")]
        with open(self.p("data/send_ledger.csv"), "a", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=LEDGER_FIELDS, lineterminator="\n").writerows(rows)
        out = self.p("due.json")
        self.tool("followups_due.py", "--date", "2026-12-31", "--out", out)
        with open(out, encoding="utf-8") as fh: due = {x["to"]: x for x in json.load(fh)["due"]}
        self.assertEqual((due["d@ddump.com"]["next"], due["d@ddump.com"]["due"]), ("S5", "2026-12-14"))   # Nov 23 + 13 bd
        self.assertEqual(due["d@ddump.com"]["reply_to_message_id"], "m-JI-T0-S2-01")


class Gate(Repo):
    def facts(self, recs):
        path = self.p("facts.json")
        with open(path, "w", encoding="utf-8") as fh: json.dump({"checked_at": "2026-11-24T15:00:00Z", "records": recs}, fh)
        return path

    @unittest.skipUnless(NODE, "node not installed")
    def test_gate_holds_stale_and_releases_outage_rows(self):
        self.queue("JI-T1-S1", [
            s1(1, "info@aroll.com", "A Roll-Off"),
            s1(2, "sales@bwaste.com", "B Waste", body=s1_body("B Waste", "TXR1574ZN", "with a record date of September 24")),
            s1(3, "c@cport.com", "C Portables", body=s1_body("C Portables", "TXR", "last month")),
            s1(4, "z@zz.com", "Z", status="held_stale", hold_note="2026-11-23: stale hook (TCEQ outage: x); needs a re-hook"),
            s1(5, "y@yy.com", "Y", status="drafted", planned_for="2026-11-25")])
        facts = self.facts({"TXR1594ZB": {"rows": [{"status": "ACTIVE", "date": "2026-11-05"}]},
                            "TXR1574ZN": {"rows": [{"status": "ACTIVE", "date": "2026-09-24"}]}})
        gate = self.p("gate.json")
        self.tool("hook_gate.py", "--send-date", "2026-11-30", "--out", gate, "--facts", facts)
        with open(self.p("gate.stale.json"), encoding="utf-8") as fh: stale = json.load(fh)
        self.assertEqual(sorted(stale), ["JI-T1-S1-02", "JI-T1-S1-03"])
        self.assertIn("over 45", stale["JI-T1-S1-02"])
        with open(self.p("gate.release.txt"), encoding="utf-8") as fh: self.assertEqual(fh.read(), "JI-T1-S1-04")
        r = self.tool("hook_gate.py", "--send-date", "2026-11-25", "--out", self.p("g2.json"), "--facts", facts, "--include-drafted")
        with open(self.p("g2.json"), encoding="utf-8") as fh:
            self.assertIn("JI-T1-S1-05", [x["id"] for x in json.load(fh)["results"]])   # pre-send re-checks today's drafts too
        self.tool("hold_stale.py", "--stale", self.p("gate.stale.json"), "--apply")
        self.tool("hold_stale.py", "--release", "JI-T1-S1-04", "--apply")
        st = {r["id"]: r["status"] for r in self.read_queue("JI-T1-S1")["records"]}
        self.assertEqual(st, {"JI-T1-S1-01": "queued", "JI-T1-S1-02": "held_stale", "JI-T1-S1-03": "held_stale",
                              "JI-T1-S1-04": "deferred", "JI-T1-S1-05": "drafted"})


class Prepare(Repo):
    def make(self):
        a = self.drafted(s1(1, "info@aroll.com", "A Roll-Off"), "2026-11-25")
        later = self.drafted(s1(2, "sales@bwaste.com", "B Waste"), "2026-11-30")
        self.queue("JI-T1-S1", [a, later])
        f = self.drafted({"id": "JI-T0-S2-01", "seq": 1, "batch": "JI-T0", "company": "D Dumpsters", "city": "Houston", "stage": "S2",
                          "from": "sites@asterfieldgroup.com", "to": "d@ddump.com", "subject": "Re: Cypress Fields Business Park",
                          "body": f"Hi D Dumpsters team,\n\nOne more note on the Cypress Fields site.\n\n{SIG}",
                          "reply_to_message_id": "m-JI-T0-S1-01", "attachments": [], "hook_type": "commercial", "footer": FOOT}, "2026-11-25")
        self.queue("JI-T0-S2", [f])

    def test_prepared_batch_for_the_publisher(self):
        self.make()
        out = self.p("ops/prepared/2026-11-25.json")
        r = self.tool("prepare_batch.py", "--send-date", "2026-11-25", "--out", out)
        subject = r.stdout.split("SUBJECT: ")[1].split("\n")[0]
        body = r.stdout.split("BODY:\n")[1]
        self.assertTrue(subject.startswith("JSI-PREPARED v1 2026-11-25 "))
        raw = gzip.decompress(base64.b64decode("".join(body.split())))
        self.assertEqual(hashlib.sha256(raw).hexdigest(), subject.split()[-1])
        p = json.loads(raw)
        self.assertEqual((p["kind"], p["business"], p["share"], p["max_s1"]), ("prepared", "Jobsite Intelligence", 15, 5))
        hooks = {e["outreach_id"]: e["hook"] for e in p["entries"]}
        self.assertEqual(sorted(hooks), ["JI-T0-S2-01", "JI-T1-S1-01"])    # the Nov 30 draft stays out
        self.assertEqual((hooks["JI-T1-S1-01"]["kind"], hooks["JI-T1-S1-01"]["id"], hooks["JI-T1-S1-01"]["cited"]), ("NOI", "TXR1594ZB", "2026-11-05"))
        self.assertEqual(hooks["JI-T0-S2-01"]["kind"], "NONE")
        with open(out, encoding="utf-8") as fh: self.assertEqual(json.load(fh)["subject"], subject)
        self.prepared_out = r.stdout

    def test_nothing_drafted_is_refused(self):
        self.make()
        r = self.tool("prepare_batch.py", "--send-date", "2026-12-01", "--out", self.p("x.json"), ok=False)
        self.assertNotEqual(r.returncode, 0); self.assertIn("no drafted records", r.stdout + r.stderr)

    def test_changed_copy_is_refused(self):
        self.make()
        q = self.read_queue("JI-T1-S1"); q["records"][0]["subject"] = "Edited after drafting"
        with open(self.p("ops/queue/JI-T1-S1.json"), "w", encoding="utf-8") as fh: json.dump(q, fh)
        r = self.tool("prepare_batch.py", "--send-date", "2026-11-25", "--out", self.p("x.json"), ok=False)
        self.assertIn("re-draft", r.stdout + r.stderr)

    @unittest.skipUnless(NODE, "node not installed")
    def test_end_to_end_with_the_publisher_and_sender(self):
        self.test_prepared_batch_for_the_publisher()
        txt = self.p("prepared.out.txt")
        with open(txt, "w", encoding="utf-8") as fh: fh.write(self.prepared_out)
        r = subprocess.run([NODE, os.path.join(ROOT, "ops", "sender", "test_publisher.cjs"), txt], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("end to end", r.stdout)


class Reconcile(Repo):
    def test_prepared_file_and_publisher_drops(self):
        prep = {"subject": "JSI-PREPARED v1 2026-11-25 x", "prepared": {"send_date": "2026-11-25", "entries": [
            {"outreach_id": "JI-T1-S1-01", "stage": "S1", "to": "info@aroll.com", "from_alias": "sites@asterfieldgroup.com"},
            {"outreach_id": "JI-T1-S1-02", "stage": "S1", "to": "sales@bwaste.com", "from_alias": "sites@asterfieldgroup.com"}]}}
        with open(self.p("prep.json"), "w", encoding="utf-8") as fh: json.dump(prep, fh)
        cols = ["time (Central)", "mode", "result", "outreach_id", "stage", "to", "from_alias", "detail", "message_id"]
        write_csv(self.p("log.csv"), cols, [
            {"time (Central)": "2026-11-25 06:12:00", "mode": "JSI-PUBLISH", "result": "DROPPED", "outreach_id": "JI-T1-S1-02",
             "detail": "record date 2026-10-01 is 55 days before 2026-11-25 (over 45)"},
            {"time (Central)": "2026-11-25 08:04:00", "mode": "LIVE", "result": "SENT", "outreach_id": "JI-T1-S1-01", "message_id": "mm1"}])
        sent = {"threads": [{"id": "t1", "messages": [{"id": "mm1", "threadId": "t1", "labelIds": ["SENT"], "toRecipients": ["info@aroll.com"],
                                                       "sender": "sites@asterfieldgroup.com", "date": "2026-11-25T14:04:00Z"}]}]}
        with open(self.p("sent.json"), "w", encoding="utf-8") as fh: json.dump(sent, fh)
        r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "reconcile_check.py"), "--manifest", self.p("prep.json"),
                            "--sender-log", self.p("log.csv"), "--sent", self.p("sent.json"), "--out", self.p("rec.json")],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.p("rec.json"), encoding="utf-8") as fh: rep = json.load(fh)
        self.assertEqual(rep["counts"], {"SENT": 1, "DROPPED": 1})


class Verify(Repo):
    def setUp(self):
        super().setUp()
        self.outbox = self.p("verify/outbox/x").rsplit(os.sep, 1)[0]
        write_csv(self.p("data/to_verify_2026-11-24.csv"), ["email", "company", "metro", "site"], [
            {"email": "new1@haul.com", "company": "New One", "metro": "Houston", "site": "RN1"},
            {"email": "new2@haul.com", "company": "New Two", "metro": "Houston", "site": "RN2"},
            {"email": "x@optout.com", "company": "Opted", "metro": "Houston", "site": "RN3"},       # do-not-contact domain
            {"email": "d@ddump.com", "company": "D", "metro": "Houston", "site": "RN4"},          # already emailed
            {"email": "old@haul.com", "company": "Old", "metro": "Houston", "site": "RN5"}])
        write_csv(self.p("data/verified_2026-11-06_millionverifier.csv"), ["email", "result"], [{"email": "old@haul.com", "result": "ok"}])
        with open(os.path.join(self.outbox, "2026-11-24.csv"), "w", encoding="utf-8", newline="") as fh:
            fh.write("email,business\nasi1@signs.com,ASI\n")

    def test_collect_appends_to_the_shared_outbox_once(self):
        self.tool("mv_bulk.py", "collect", "--today", "2026-11-24", "--outbox", self.outbox)
        self.tool("mv_bulk.py", "collect", "--today", "2026-11-24", "--outbox", self.outbox)   # nothing new
        with open(os.path.join(self.outbox, "2026-11-24.csv"), encoding="utf-8") as fh: rows = list(csv.DictReader(fh))
        self.assertEqual([(r["email"], r["business"]) for r in rows],
                         [("asi1@signs.com", "ASI"), ("new1@haul.com", "JSI"), ("new2@haul.com", "JSI")])

    def test_open_batch_does_not_block_a_new_one(self):
        self.tool("mv_bulk.py", "collect", "--today", "2026-11-24", "--outbox", self.outbox)
        write_csv(self.p("data/to_verify_2026-11-25.csv"), ["email", "company", "metro", "site"],
                  [{"email": "new3@haul.com", "company": "New Three", "metro": "Houston", "site": "RN6"}])
        self.tool("mv_bulk.py", "collect", "--today", "2026-11-25", "--outbox", self.outbox)
        with open(self.p("data/verify_batches/state.json"), encoding="utf-8") as fh: st = json.load(fh)
        self.assertEqual([(b["id"], b["emails"]) for b in st["batches"]],
                         [("2026-11-24", ["new1@haul.com", "new2@haul.com"]), ("2026-11-25", ["new3@haul.com"])])
        r = self.tool("mv_bulk.py", "collect", "--today", "2026-11-25", "--outbox", self.outbox)
        self.assertIn("nothing pending", r.stdout)                         # every address is already in a batch

    def test_import_shared_takes_only_our_rows(self):
        self.tool("mv_bulk.py", "collect", "--today", "2026-11-24", "--outbox", self.outbox)
        res = self.p("inbox/results.csv")
        write_csv(res, ["email", "business", "quality", "result"], [
            {"email": "asi1@signs.com", "business": "ASI", "quality": "good", "result": "ok"},
            {"email": "new1@haul.com", "business": "JSI", "quality": "good", "result": "ok"},
            {"email": "new2@haul.com", "business": "JSI", "quality": "risky", "result": "unknown"}])
        self.tool("mv_bulk.py", "import-inbox", "--today", "2026-11-25", "--inbox", self.p("inbox/x").rsplit(os.sep, 1)[0])
        with open(self.p("data/verified_emails.csv"), encoding="utf-8") as fh: v = list(csv.DictReader(fh))
        self.assertEqual([(r["email"], r["result"]) for r in v], [("new1@haul.com", "Deliverable")])
        self.assertTrue(os.path.exists(res + ".jsi_imported.txt"))
        # the unknown address returns to pending once; a second run of the inbox finds nothing new to import
        r = self.tool("mv_bulk.py", "import-inbox", "--today", "2026-11-25", "--inbox", self.p("inbox/x").rsplit(os.sep, 1)[0])
        self.assertIn("no results files", r.stdout)
        r = self.tool("mv_bulk.py", "status")
        self.assertIn("pending now: 1", r.stdout)

    def test_no_api_and_no_key(self):
        with open(os.path.join(TOOLS, "mv_bulk.py"), encoding="utf-8") as fh: src = fh.read()
        self.assertNotIn("environ", src)
        self.assertNotIn("urllib", src)
        self.assertNotIn("millionverifier.com/api", src)


class Views(Repo):
    def test_status_and_calendar_run_on_a_small_repo(self):
        self.queue("JI-T1-S1", [s1(1, "info@aroll.com", "A Roll-Off"), s1(2, "sales@bwaste.com", "B Waste"),
                                s1(3, "c@cport.com", "C Portables", city="DFW")])
        out = self.p("status.md")
        self.tool("daily_status.py", "--out", out, "--today", "2026-11-24", "--now", "18:30", "--stale-out", self.p("stale.json"))
        with open(out, encoding="utf-8") as fh: s = fh.read()
        self.assertIn("RESERVE LOW: 2 ready", s)
        self.assertIn("waits for a sender alias (DFW) 1", s)
        self.assertIn("MISSING BATCH for 2026-11-25", s)
        cal = self.p("ops/routines/CALENDAR.md")
        self.tool("calendar_view.py", "--start", "2026-11-25", "--out", cal)
        with open(cal, encoding="utf-8") as fh: c = fh.read()
        self.assertIn("| 1 | Wed Nov 25 | 0 | 2 | 2 | 3 |", c)
        self.assertIn("| 2 | Mon Nov 30 |", c)                            # Thanksgiving skipped


@unittest.skipUnless(NODE, "node not installed")
class Publisher(unittest.TestCase):
    def test_publisher_unit_tests(self):
        r = subprocess.run([NODE, os.path.join(ROOT, "ops", "sender", "test_publisher.cjs")], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class NoEmDashes(unittest.TestCase):
    def test_new_routine_files_have_no_em_dash(self):
        files = [os.path.join(ROOT, "ops", "routines", f) for f in os.listdir(os.path.join(ROOT, "ops", "routines")) if f.endswith(".md")]
        files += [os.path.join(TOOLS, f) for f in os.listdir(TOOLS) if f.endswith((".py", ".js"))]
        files += [os.path.join(ROOT, "ops", "sender", f) for f in ("JsiPublisher.gs", "hook_facts.cjs", "dry_publish.cjs", "test_publisher.cjs")]
        for f in files:
            if os.path.exists(f):
                with open(f, encoding="utf-8") as fh: self.assertNotIn("—", fh.read(), f)


if __name__ == "__main__":
    unittest.main()
