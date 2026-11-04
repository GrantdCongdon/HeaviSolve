# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fail closed on unreviewed dependency licenses; no solver implementation."""
import pathlib
import sys
import tomllib
ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWED = {'MIT','BSD-2-Clause','BSD-3-Clause','ISC','Zlib','BSL-1.0','Apache-2.0',
           'MPL-2.0','LGPL-2.1-or-later','LGPL-3.0-only','LGPL-3.0-or-later',
           'GPL-2.0-or-later','GPL-3.0-only','GPL-3.0-or-later',
           'AGPL-3.0-only','AGPL-3.0-or-later'}
def main():
    errors=[]
    for dependency in tomllib.loads((ROOT/'dependencies.toml').read_text())['dependency']:
        if dependency['license'] not in ALLOWED:
            errors.append(f"{dependency['name']}: unapproved exact license {dependency['license']}")
        for field in ('version','source','scope','review'):
            if not dependency.get(field): errors.append(f"{dependency['name']}: missing {field}")
    if errors:
        print('\n'.join(errors));sys.exit(1)
    print('PASS: declared direct dependency inventory; not a transitive distribution certification')

if __name__ == "__main__":
    main()
