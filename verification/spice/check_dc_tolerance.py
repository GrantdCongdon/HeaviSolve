# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Sensitivity check on existing emitted decks; preserve model data and acceptance bounds."""
import pathlib,subprocess,json
import numpy as np
w=pathlib.Path('/tmp/heavisolve-spice/conformance')
results=[]
for kind in ['diode','ihp']:
 for engine in ['ngspice','xyce']:
  deck=w/f'{kind}-{engine}-dc-strict.cir'
  deck.write_text((w/f'{kind}-{engine}-dc.cir').read_text().replace('reltol=1e-8','reltol=1e-10').replace('abstol=1e-14','abstol=1e-16'))
  cmd=[str(w/'ng-run'),str(deck),'dc',str(deck)+'.csv'] if engine=='ngspice' else ['/tmp/heavisolve-spice/xyce/bin/Xyce',str(deck)]
  with deck.with_suffix('.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=w/'ihp-xyce' if engine=='xyce' else pathlib.Path.cwd()/'.local',check=True)
 ng=np.loadtxt(str(w/f'{kind}-ngspice-dc-strict.cir.csv'),delimiter=',',skiprows=1)
 xy=np.loadtxt(str(w/f'{kind}-xyce-dc-strict.cir.csv'),delimiter=',',skiprows=1)
 err=float(np.sqrt(np.mean((ng[:,3]-xy[:,2])**2))/np.sqrt(np.mean(ng[:,3]**2)))
 results.append(dict(circuit=kind,current_relative_rms=err,tolerance=1e-4,status='PASS' if err<1e-4 else 'FAIL'))
print(json.dumps(results,indent=2))
