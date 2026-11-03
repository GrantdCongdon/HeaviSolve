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
