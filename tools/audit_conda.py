# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fail closed on every package in an isolated conda prefix; emit inventory."""
import argparse
import json
import pathlib
import sys
from license_scan import ALLOWED
parser = argparse.ArgumentParser()
parser.add_argument('prefix', type=pathlib.Path)
args = parser.parse_args()
records = sorted((args.prefix / 'conda-meta').glob('*.json'))
if not records:
    sys.exit('FAIL: no conda package metadata found')
failed = False
for path in records:
    data = json.loads(path.read_text())
    license_id = data.get('license', '')
    approved = license_id in ALLOWED
    failed |= not approved
    print(json.dumps({'name': data['name'], 'version': data['version'],
                      'build': data.get('build'), 'license': license_id,
                      'sha256': data.get('sha256'),
                      'decision': 'ALLOW_EXACT' if approved else 'REVIEW_OR_DENY'}, sort_keys=True))
print('FAIL: unapproved expressions; no redistribution admission' if failed else
      'PASS: metadata expressions allowed; bundled-file and linkage review still required')
sys.exit(int(failed))
