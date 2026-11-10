import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('enrich_haulers', SCRIPTS / 'enrich_haulers.py')
enrich = importlib.util.module_from_spec(spec)
spec.loader.exec_module(enrich)


class MalformedFiledEmailTest(unittest.TestCase):
    def test_missing_at_does_not_crash_or_become_a_domain(self):
        carriers = [
            {'dot_number': '1', 'legal_name': 'Example Roll Off LLC',
             'email_address': 'not-an-address', 'power_units': '1'},
            {'dot_number': '2', 'legal_name': 'Another Dumpster LLC',
             'email_address': 'published@gmail.com', 'power_units': '1'},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = str(Path(tmp) / 'haulers.csv')
            with patch.object(sys, 'argv', ['enrich_haulers.py', '--metro', 'Houston', '--out', out]), \
                 patch.object(enrich.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(carriers).encode())), \
                 patch.object(enrich, 'scan_site') as scan, contextlib.redirect_stderr(io.StringIO()):
                enrich.main()
            with open(out, newline='') as handle:
                rows = {r['usdot']: r for r in csv.DictReader(handle)}
        self.assertEqual(rows['1']['fmcsa_email'], '')
        self.assertEqual(rows['1']['domain'], '')
        self.assertEqual(rows['1']['email'], '')
        self.assertEqual(rows['2']['fmcsa_email'], 'published@gmail.com')
        scan.assert_not_called()
