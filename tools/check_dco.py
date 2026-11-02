# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check every PR commit for a nonempty DCO sign-off trailer."""
import re
import subprocess
import sys
if len(sys.argv) != 3:
    raise SystemExit('usage: check_dco.py base_sha head_sha')
for sha in sys.argv[1:]:
    if not re.fullmatch(r'[0-9a-fA-F]{40,64}', sha):
        raise SystemExit('Expected a full commit object ID')
commits = subprocess.check_output(['git','rev-list',f'{sys.argv[1]}..{sys.argv[2]}'],text=True).split()
failed=[]
for commit in commits:
    trailers=subprocess.check_output(['git','show','-s','--format=%(trailers:key=Signed-off-by,valueonly)',commit],text=True)
    if not re.search(r'^\S[^\n]* <[^<>\s]+@[^<>\s]+>$',trailers,re.M):
        failed.append(commit)
if failed: raise SystemExit('Missing DCO sign-off: '+', '.join(failed))
print(f'PASS: {len(commits)} commit trailers checked; certification remains contributor responsibility')
