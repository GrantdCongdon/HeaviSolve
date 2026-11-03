# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ensure transitive metadata cannot bypass the exact license gate."""
import json
import pathlib
import subprocess
import sys
import tempfile
root = pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as folder:
    prefix = pathlib.Path(folder)
    records = prefix / 'conda-meta'
    records.mkdir()
    for expression, expected in [('BSD-3-Clause', 0), ('LicenseRef-ParMETIS', 1),
                                 ('', 1), ('MIT OR GPL-2.0-only', 1)]:
        (records / 'transitive.json').write_text(json.dumps({
            'name': 'indirect-dependency', 'version': 'test', 'license': expression}))
        result = subprocess.run([sys.executable, str(root / 'tools/audit_conda.py'), str(prefix)],
                                capture_output=True, text=True)
        assert result.returncode == expected, (expression, result.stdout, result.stderr)
print('PASS: allow exact, deny restricted, reject blank and unreviewed OR')
# A review approves one archive identity, never all versions of that package/license.
import tomllib
reviews = tomllib.loads((root / 'tools/conda-license-reviews.toml').read_text())['review']
review = reviews[0]
identity = ('name', 'version', 'build', 'sha256', 'subdir', 'license')
with tempfile.TemporaryDirectory() as folder:
    prefix = pathlib.Path(folder)
    records = prefix / 'conda-meta'
    records.mkdir()
    original = {key: review[key] for key in identity}
    cases = [(original, 0)]
    for key in identity:
        changed = dict(original)
        changed[key] = 'unreviewed'
        cases.append((changed, 1))
    for data, expected in cases:
        (records / 'reviewed.json').write_text(json.dumps(data))
        result = subprocess.run([sys.executable, str(root / 'tools/audit_conda.py'), str(prefix)],
                                capture_output=True, text=True)
        assert result.returncode == expected, (data, result.stdout, result.stderr)
print('PASS: reviewed archive accepted; identity/license drift rejected')
