# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Acceptance must not silently certify missing decisions or milestone exit."""
import importlib.util
import pathlib
import tempfile
import unittest

root = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('m0_gate', root / 'tools/m0_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class GateTest(unittest.TestCase):
    def test_missing_records_fail_closed(self):
        self.assertTrue(gate.missing_records({}, ('acceptance',)))
        status = {'acceptance': dict.fromkeys(gate.REQUIRED['acceptance'], True)}
        self.assertEqual(gate.missing_records(status, ('acceptance',)), [])
        for key in gate.REQUIRED['acceptance']:
            changed = {'acceptance': dict(status['acceptance'])}
            changed['acceptance'][key] = False
            self.assertIn('acceptance.' + key, gate.missing_records(changed, ('acceptance',)))
        self.assertTrue(gate.missing_records(status, ('exit',)))
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(gate.missing_records(status, ('acceptance',), pathlib.Path(directory)))

    def test_failed_spike_does_not_become_passed(self):
        status = {'acceptance': dict.fromkeys(gate.REQUIRED['acceptance'], True),
                  'spikes': {'S3c': 'FAIL'}}
        self.assertEqual(gate.missing_records(status, ('acceptance',)), [])
        self.assertEqual(status['spikes']['S3c'], 'FAIL')
        self.assertTrue(gate.missing_records(status, tuple(gate.REQUIRED)))

if __name__ == '__main__':
    unittest.main()
