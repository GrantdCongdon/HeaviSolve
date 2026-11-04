# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Run native implementations and compare against an independent slab oracle."""
import csv
import io
import json
import math
import pathlib
import subprocess
import sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'verification/oracles'))
from slab import fundamental
oracle=[fundamental(False),fundamental(True)]
binary_dir=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'.work/language'
rows=[]
for refinement in (1,2,4,8):
    pair=[]
    for language in ('cpp','rust'):
        run=subprocess.run([str(binary_dir/f'slab-{language}'),str(refinement)],capture_output=True,text=True,check=True)
        row=next(csv.DictReader(io.StringIO(run.stdout)))
        values=[float(row['te0_neff']),float(row['tm0_neff'])]
        errors=[abs(x-y) for x,y in zip(values,oracle)]
        row.update(te0_error=errors[0],tm0_error=errors[1])
        pair.append(values);rows.append(row)
    assert max(abs(x-y) for x,y in zip(*pair))<1e-10
for language in ('cpp','rust'):
    subset=[row for row in rows if row['language']==language]
    for key in ('te0_error','tm0_error'):
        rates=[math.log2(float(a[key])/float(b[key])) for a,b in zip(subset,subset[1:])]
        assert all(1.8<rate<2.2 for rate in rates),(language,key,rates)
        assert float(subset[-1][key])<1e-4
print('# SPDX-' + 'FileCopyrightText: 2026 HeaviSolve contributors')
print('# SPDX-' + 'License-Identifier: AGPL-3.0-or-later')
print('# Independent exact TE0='+repr(oracle[0])+' TM0='+repr(oracle[1]))
writer=csv.DictWriter(sys.stdout,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
