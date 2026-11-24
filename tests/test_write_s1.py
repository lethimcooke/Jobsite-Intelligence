"""write_s1.py: v2 S1 copy, portable dates, the no-yard (service-area) variant, UTF-8 price line."""
import csv
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import write_s1  # noqa: E402

COLS = ["batch", "company", "email", "email_confidence", "yard_city", "fit_phrase_our_read", "site_name",
        "site_address", "county", "tceq_authorization", "date_on_file", "operator_on_file", "site_rn",
        "site_source_url", "services_published", "miles_from_yard_our_read", "service_area_city"]


class WriteS1Test(unittest.TestCase):
    def test_month_day_has_no_leading_zero(self):
        self.assertEqual(write_s1.month_day("2026-11-09"), "November 9")

    def test_fit_lines_without_yard_uses_service_area(self):
        line, close = write_s1.fit_lines({"miles_from_yard_our_read": "", "service_area_city": "Rosenberg",
                                          "site_address": "1 A St, Rosenberg, TX"}, "school", "roll-off containers")
        self.assertTrue(line.startswith("It's in Rosenberg, one of the areas you serve, and a school job"))
        self.assertEqual(close, "Want five sites like this in your service area, free?")

    def test_fit_lines_with_yard(self):
        line, close = write_s1.fit_lines({"miles_from_yard_our_read": "6", "yard_city": "KATY",
                                          "site_address": "1 A St, Katy, TX"}, "industrial", "roll-offs")
        self.assertTrue(line.startswith("It's about 6 miles from your Katy yard, and an industrial job"))
        self.assertEqual(close, "Want five sites like this near your yard, free?")

    def test_cli_writes_utf8_price_line_once_per_body(self):
        row = dict.fromkeys(COLS, "")
        row.update(batch="HX", company="Acme Roll Off LLC", email="info@acme.example", email_confidence="A",
                   fit_phrase_our_read="roll-off dumpsters", site_name="BIG WAREHOUSE PARK",
                   site_address="100 MAIN ST, HOUSTON, TX", county="HARRIS", tceq_authorization="TXR1500ZZ",
                   date_on_file="2026-11-09", operator_on_file="BUILDER CO LLC", site_rn="RN100000000",
                   service_area_city="Houston")
        with tempfile.TemporaryDirectory() as d:
            packet, out = os.path.join(d, "p.csv"), os.path.join(d, "o.md")
            with open(packet, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLS)
                w.writeheader()
                w.writerow(row)
            subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "write_s1.py"), "--packet", packet,
                            "--metro", "Houston", "--out", out], check=True, capture_output=True)
            text = open(out, encoding="utf-8").read()
        price = write_s1.RULES["standard_price_line"]
        self.assertEqual(text.count(price), 1)
        self.assertIn("with a record date of November 9 for Big Warehouse Park", text)
        self.assertIn("in Harris County", text)
        self.assertNotIn("—", text)


if __name__ == "__main__":
    unittest.main()
