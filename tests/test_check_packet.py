import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('check_packet', Path(__file__).resolve().parents[1] / 'scripts/check_packet.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PacketChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'data').mkdir()
        (self.root / 'ops').mkdir()
        (self.root / 'ops/rules.json').write_text(json.dumps({'lists': {'files': ['haulers.csv']}}))

    def write_rows(self, name, rows):
        with (self.root / 'data' / name).open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def check(self, rows):
        return checker.check(rows, str(self.root))

    def test_clean_not_contacted(self):
        row = {'company': 'Example Hauling LLC', 'email': 'office@example.test', 'outreach_status': 'Not contacted'}
        self.write_rows('haulers.csv', [row])
        self.assertEqual(self.check([row]), [])

    def test_blocked_domain_with_different_company_and_email(self):
        self.write_rows('haulers.csv', [{'company': 'Original Hauler', 'email': 'sales@example.test', 'outreach_status': 'Replied (interested)'}])
        self.assertTrue(self.check([{'company': 'Alias Hauler', 'email': 'office@example.test'}]))

    def test_dnc_company_normalization_and_exact_domain(self):
        self.write_rows('do_not_contact.csv', [{'company': 'Example-Hauling LLC', 'domain': 'blocked.test'}])
        self.assertTrue(self.check([{'company': 'Example Hauling', 'email': 'office@new.test'}]))
        self.assertEqual(self.check([{'company': 'Other Hauler', 'email': 'office@notblocked.test'}]), [])

    def test_dnc_email(self):
        self.write_rows('do_not_contact.csv', [{'email': 'office@example.test'}])
        self.assertTrue(self.check([{'company': 'Hauler', 'email': 'office@example.test'}]))

    def test_alternate_email_and_later_clean_alias_cannot_hide_reply(self):
        self.write_rows('haulers.csv', [
            {'company': 'Example Hauling', 'email': 'office@example.test', 'site_emails': 'service@alternate.test', 'outreach_status': 'Replied'},
            {'company': 'Example Hauling LLC', 'email': 'office@example.test', 'site_emails': '', 'outreach_status': 'Not contacted'},
        ])
        self.assertTrue(self.check([{'company': 'Other Hauler', 'email': 'service@alternate.test'}]))
        self.assertTrue(self.check([{'company': 'Example Hauling', 'email': 'office@example.test'}]))

    def test_form_only_duplicate_website(self):
        self.assertTrue(self.check([
            {'company': 'First Hauler', 'website': 'https://www.example.test/contact'},
            {'company': 'Other Hauler', 'website': 'example.test'},
        ]))

    def test_excluded_company_and_csv_domain(self):
        (self.root / 'Jobsite_Intelligence_Outreach_Tracker.md').write_text('## Excluded\n\n- Example Hauling LLC (Oct 14): mismatch.\n')
        self.assertTrue(self.check([{'company': 'Example Hauling', 'email': 'office@example.test'}]))
        self.write_rows('master_prospect_exclusions.csv', [{'company': 'Other', 'domain': 'excluded.test'}])
        self.assertTrue(self.check([{'company': 'Alias', 'email': 'office@excluded.test'}]))

    def test_empty_packet_fails(self):
        self.assertTrue(self.check([]))

    def test_distinct_free_mail_users_not_same_business(self):
        self.assertEqual(self.check([
            {'company': 'First Hauler', 'email': 'first@gmail.com'},
            {'company': 'Other Hauler', 'email': 'second@gmail.com'},
        ]), [])


if __name__ == '__main__':
    unittest.main()
