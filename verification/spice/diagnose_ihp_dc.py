# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Separate diagnostic copies test model-parameter differences; no acceptance rewrite."""
import csv
import hashlib
import json
import math
import pathlib
import shutil
import subprocess
ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = pathlib.Path('/tmp/heavisolve-spice/conformance')
WORK = pathlib.Path('/tmp/heavisolve-spice/ihp-dc-diagnostic')
results = []
for variant in ('original', 'xy_ikp_match', 'xy_delay_off', 'both'):
    arrays = {}
    evidence = {}
    for engine in ('ngspice', 'xyce'):
        source = ROOT/'.local' if engine == 'ngspice' else BASE/'ihp-xyce'
        directory = WORK/variant/engine
        directory.mkdir(parents=True, exist_ok=True)
        for name in ('cornerHBT.lib', 'sg13g2_hbt_mod.lib', 'sg13g2_hbt_stat.lib'):
            shutil.copyfile(source/name, directory/name)
        model = directory/'sg13g2_hbt_mod.lib'
        original = model.read_bytes()
        text = original.decode('latin1')
        if engine == 'xyce' and variant in ('xy_ikp_match', 'both'):
            before = "+ ikp = '.00E-04*(Nx*0.25)'"
            assert before in text
            text = text.replace(before, "+ ikp = '1.00E-04*(Nx*0.25)'")
        if engine == 'xyce' and variant in ('xy_delay_off', 'both'):
            before = "+ td = '2.80E-13*(Nx*0.25)**0'"
            assert before in text
            text = text.replace(before, '+ td = 0')
        model.write_bytes(text.encode('latin1'))
        evidence[engine] = {'original_sha256': hashlib.sha256(original).hexdigest(),
                            'diagnostic_sha256': hashlib.sha256(model.read_bytes()).hexdigest()}
        text = (BASE/f'ihp-{engine}-dc.cir').read_text()
        text = text.replace(str(source/'cornerHBT.lib'), str(directory/'cornerHBT.lib'))
        text = text.replace('Xq out b 0 0 npn13G2', 'Xq out b 0 0 npn13G2 selft=0')
        text = text.replace('reltol=1e-8', 'reltol=1e-11').replace('abstol=1e-14', 'abstol=1e-18')
        options = '.options gmin=1e-16 vntol=1e-12' if engine == 'ngspice' else '.options DEVICE GMIN=1e-16'
        text = text.replace('.end', options+'\n.end')
        deck = directory/'dc.cir'; deck.write_text(text)
        command = [str(BASE/'ng-run'),str(deck),'dc',str(deck)+'.csv'] if engine == 'ngspice' else ['/tmp/heavisolve-spice/xyce/bin/Xyce',str(deck)]
        with (directory/'engine.log').open('w') as log:
            subprocess.run(command,cwd=directory,stdout=log,stderr=subprocess.STDOUT,check=True)
        with pathlib.Path(str(deck)+'.csv').open() as stream:
            arrays[engine] = [[float(x) for x in row] for row in list(csv.reader(stream))[1:]]
    ng,xy = arrays['ngspice'],arrays['xyce']
    assert len(ng)==len(xy)
    assert all(abs(a[0]-b[0])<1e-12 for a,b in zip(ng,xy))
    error = math.sqrt(sum((a[3]-b[2])**2 for a,b in zip(ng,xy))/sum(a[3]**2 for a in ng))
    results.append({'variant':variant,'selft':0,'gmin':1e-16,'reltol':1e-11,'abstol':1e-18,
                    'base_current_relative_rms':error,'maximum_absolute_difference_a':max(abs(a[3]-b[2]) for a,b in zip(ng,xy)),
                    'acceptance_tolerance':1e-4,'within_tolerance':error<1e-4,
                    'model_sha256':evidence,'scope':'diagnostic only; original-model acceptance unchanged'})
print(json.dumps(results,indent=2))
