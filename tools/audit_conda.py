# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fail closed on every package in an isolated conda prefix; emit inventory."""
import argparse
import json
import pathlib
import sys
import re
import tomllib
from license_scan import ALLOWED
parser = argparse.ArgumentParser()
parser.add_argument('prefix', type=pathlib.Path)
parser.add_argument('--reviews', type=pathlib.Path, default=pathlib.Path(__file__).with_name('conda-license-reviews.toml'))
args = parser.parse_args()
identity = ('name', 'version', 'build', 'sha256', 'subdir', 'license')
reviews = {}
if args.reviews.exists():
    document = tomllib.loads(args.reviews.read_text())
    if document.get('schema_version') != 1:
        sys.exit('FAIL: unknown review schema')
    for review in document.get('review', []):
        required = identity + ('selected_license', 'decision', 'adr', 'source', 'obligations', 'evidence_sha256')
        if any(not isinstance(review.get(key), str) or not review[key] for key in required):
            sys.exit('FAIL: incomplete license review')
        if review['decision'] != 'allow' or not re.fullmatch('[0-9a-f]{64}', review['sha256']):
            sys.exit('FAIL: invalid license review')
        if not re.fullmatch('[0-9a-f]{64}', review['evidence_sha256']):
            sys.exit('FAIL: missing license evidence digest')
        key = tuple(review[field] for field in identity)
        if key in reviews:
            sys.exit('FAIL: duplicate license review')
        reviews[key] = review
records = sorted((args.prefix / 'conda-meta').glob('*.json'))
if not records:
    sys.exit('FAIL: no conda package metadata found')
failed = False
for path in records:
    data = json.loads(path.read_text())
    license_id = data.get('license', '')
    review = reviews.get(tuple(data.get(field) for field in identity))
    approved = license_id in ALLOWED or review is not None
    failed |= not approved
    print(json.dumps({'name': data['name'], 'version': data['version'],
                      'build': data.get('build'), 'license': license_id,
                      'sha256': data.get('sha256'),
                      'decision': 'ALLOW_REVIEWED' if review else 'ALLOW_EXACT' if approved else 'REVIEW_OR_DENY',
                      'review_adr': review['adr'] if review else None,
                      'selected_license': review['selected_license'] if review else license_id}, sort_keys=True))
print('FAIL: unapproved expressions; no redistribution admission' if failed else
      'PASS: metadata expressions allowed; bundled-file and linkage review still required')
sys.exit(int(failed))
