# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Controlled native-engine diagnostics; original foundry files stay untouched."""
import csv
import hashlib
import json
import math
import pathlib
import shutil
import subprocess
ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = pathlib.Path('/tmp/heavisolve-spice/conformance')
WORK = pathlib.Path('/tmp/heavisolve-spice/ihp-diagnostic')
WORK.mkdir(exist_ok=True)
variants = ['baseline', 'selfheat_off', 'ng_nqs_on', 'xy_delay_off', 'xy_ikp_match']
results = []
provenance = {}
for variant in variants:
    arrays = {}
    for engine in ['ngspice', 'xyce']:
        directory = WORK / variant / engine
        directory.mkdir(parents=True, exist_ok=True)
        source = ROOT / '.local' if engine == 'ngspice' else BASE / 'ihp-xyce'
        for name in ['cornerHBT.lib', 'sg13g2_hbt_mod.lib', 'sg13g2_hbt_stat.lib']:
            original = source / name
            shutil.copyfile(original, directory / name)
            provenance[str(original)] = hashlib.sha256(original.read_bytes()).hexdigest()
        model = directory / 'sg13g2_hbt_mod.lib'
        text = model.read_text(encoding='latin1')
        if variant == 'xy_delay_off' and engine == 'xyce':
            text = text.replace("+ td = '2.80E-13*(Nx*0.25)**0'", "+ td = 0")
        if variant == 'xy_ikp_match' and engine == 'xyce':
            text = text.replace("+ ikp = '.00E-04*(Nx*0.25)'", "+ ikp = '1.00E-04*(Nx*0.25)'")
        model.write_text(text, encoding='latin1')
        deck = directory / 'diagnostic.cir'
        content = (BASE / f'ihp-{engine}-ac.cir').read_text()
        old = str(source / 'cornerHBT.lib')
        content = content.replace(old, str(directory / 'cornerHBT.lib'))
        if variant == 'selfheat_off':
            content = content.replace('Xq out b 0 0 npn13G2', 'Xq out b 0 0 npn13G2 selft=0')
        if variant == 'ng_nqs_on' and engine == 'ngspice':
            content = content.replace('Xq out b 0 0 npn13G2', 'Xq out b 0 0 npn13G2 sw_nqs=1')
        deck.write_text(content)
        cmd = [str(BASE / 'ng-run'), str(deck), 'ac', str(deck)+'.csv'] if engine == 'ngspice' else ['/tmp/heavisolve-spice/xyce/bin/Xyce', str(deck)]
        with (directory / 'engine.log').open('w') as out:
            subprocess.run(cmd, cwd=directory, stdout=out, stderr=subprocess.STDOUT, check=True)
        file = pathlib.Path(str(deck) + ('.csv' if engine == 'ngspice' else '.FD.csv'))
        with file.open() as stream:
            rows = list(csv.reader(stream))[1:]
        arrays[engine] = [[float(x) for x in row] for row in rows]
    ng, xy = arrays['ngspice'], arrays['xyce']
    assert len(ng) == len(xy)
    assert all(abs(a[0]/b[0]-1) < 1e-12 for a,b in zip(ng,xy))
    errors = {}
    for label, column in [('voltage',1),('current',3)]:
        av = [complex(r[column],r[column+1]) for r in ng]
        bv = [complex(r[column],r[column+1]) for r in xy]
        errors[label+'_relative_rms'] = math.sqrt(sum(abs(a-b)**2 for a,b in zip(av,bv))/sum(abs(a)**2 for a in av))
        errors[label+'_1khz_ng'] = [av[0].real,av[0].imag]
        errors[label+'_1khz_xy'] = [bv[0].real,bv[0].imag]
    results.append(dict(variant=variant, **errors))
print(json.dumps({'original_model_sha256':provenance,'results':results}, indent=2))
# Central-difference DC slope is an independent check of low-frequency AC linearization.
slopes = []
for variant in ['baseline', 'selfheat_off']:
    for step in [1e-5, 1e-6, 1e-7]:
        item = dict(variant=variant, step_v=step)
        for engine in ['ngspice', 'xyce']:
            directory = WORK / variant / engine
            text = (directory / 'diagnostic.cir').read_text()
            text = text.replace('.ac dec 10 1k 100meg', f'.dc Vdrive {0.8-step:.17g} {0.8+step:.17g} {step:.17g}')
            text = text.replace('.print ac format=csv precision=16 VR(out) VI(out) IR(Vdrive) II(Vdrive)', '.print dc format=csv precision=16 V(b) V(out) I(Vdrive)')
            text = text.replace('reltol=1e-8', 'reltol=1e-11').replace('abstol=1e-14', 'abstol=1e-18')
            deck = directory / f'difference-{step:.0e}.cir'
            deck.write_text(text)
            cmd = [str(BASE/'ng-run'),str(deck),'dc',str(deck)+'.csv'] if engine == 'ngspice' else ['/tmp/heavisolve-spice/xyce/bin/Xyce',str(deck)]
            with pathlib.Path(str(deck)+'.log').open('w') as log:
                subprocess.run(cmd,cwd=directory,stdout=log,stderr=subprocess.STDOUT,check=True)
            with pathlib.Path(str(deck)+'.csv').open() as stream:
                rows = [[float(x) for x in row] for row in list(csv.reader(stream))[1:]]
            width = rows[-1][0]-rows[0][0]
            item[engine+'_voltage_slope'] = (rows[-1][1]-rows[0][1])/width
            ic = 3 if engine=='ngspice' else 2
            item[engine+'_current_slope'] = (rows[-1][ic]-rows[0][ic])/width
        slopes.append(item)
(WORK/'dc-slopes.json').write_text(json.dumps(slopes,indent=2)+'\n')
# Full isothermal corpus: explicit public instance parameter, no model edits.
import bisect
isothermal = []
for gmin in [1e-12,1e-14,1e-16]:
    for analysis in ['dc','ac','tran']:
        arrays = {}
        for engine in ['ngspice','xyce']:
            source = ROOT/'.local' if engine=='ngspice' else BASE/'ihp-xyce'
            directory = WORK/'isothermal'/str(gmin)/engine
            directory.mkdir(parents=True,exist_ok=True)
            text = (BASE/f'ihp-{engine}-{analysis}.cir').read_text()
            text = text.replace('Xq out b 0 0 npn13G2', 'Xq out b 0 0 npn13G2 selft=0')
            text = text.replace('reltol=1e-8','reltol=1e-10').replace('abstol=1e-14','abstol=1e-16')
            text = text.replace('.end', (f'.options gmin={gmin}' if engine=='ngspice' else f'.options DEVICE GMIN={gmin}')+'\n.end')
            deck=directory/f'{analysis}.cir';deck.write_text(text)
            cmd=[str(BASE/'ng-run'),str(deck),analysis,str(deck)+'.csv'] if engine=='ngspice' else ['/tmp/heavisolve-spice/xyce/bin/Xyce',str(deck)]
            with pathlib.Path(str(deck)+'.log').open('w') as log:
                subprocess.run(cmd,cwd=source,stdout=log,stderr=subprocess.STDOUT,check=True)
            file=pathlib.Path(str(deck)+('.FD.csv' if analysis=='ac' and engine=='xyce' else '.csv'))
            with file.open() as stream:
                arrays[engine]=[[float(x) for x in row] for row in list(csv.reader(stream))[1:]]
        ng,xy=arrays['ngspice'],arrays['xyce'];xs=[r[0] for r in xy]
        row=dict(analysis=analysis,gmin=gmin,temperature_c=27,selft=0,reltol=1e-10,abstol=1e-16,tolerance=1e-4 if analysis=='dc' else 1e-3)
        for label,ni,xi in [('voltage',1,1),('current',3,3 if analysis=='ac' else 2)]:
            num=den=0.; max_abs=0.; absolute_values=[]
            for nr in ng:
                if nr[0]<xs[0] or nr[0]>xs[-1]: continue
                j=max(0,min(len(xs)-2,bisect.bisect_right(xs,nr[0])-1));fraction=(nr[0]-xs[j])/(xs[j+1]-xs[j])
                def val(r):return complex(r[xi],r[xi+1]) if analysis=='ac' else complex(r[xi],0)
                interp=val(xy[j])+(val(xy[j+1])-val(xy[j]))*fraction
                native=complex(nr[ni],nr[ni+1]);num+=abs(native-interp)**2;den+=abs(native)**2
                max_abs=max(max_abs,abs(native-interp));absolute_values.append(abs(native))
            row[label+'_relative_rms']=math.sqrt(num/den)
            row[label+'_maximum_absolute_difference']=max_abs
            row[label+'_ng_absolute_min']=min(absolute_values)
            row[label+'_ng_absolute_max']=max(absolute_values)
        row['status']='PASS' if max(row['voltage_relative_rms'],row['current_relative_rms'])<row['tolerance'] else 'FAIL'
        isothermal.append(row)
(WORK/'isothermal.json').write_text(json.dumps(isothermal,indent=2)+'\n')
