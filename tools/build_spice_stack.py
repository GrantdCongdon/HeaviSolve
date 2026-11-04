# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Linux research recipe, not dependency admission or a distributable installer.

The selected SPICE source/binary license closure is still open (ADR-002).
No PDK files are downloaded. Python builds native code and checks output only.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import platform
import pathlib
import shutil
import subprocess
import tarfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--work', type=pathlib.Path, required=True)
p.add_argument('--jobs', type=int, default=2)
p.add_argument('--research-candidates', action='store_true', help='acknowledge unapproved research-only dependency closure')
a = p.parse_args()
if not a.research_candidates:
    p.error('Selected SPICE dependency closure is not approved; this recipe is research-only')
if platform.system() != 'Linux':
    p.error('This unvalidated recipe targets Linux only')
if a.jobs < 1 or ' ' in str(a.work.resolve()):
    p.error('Use positive jobs and a space-free work directory')
work = a.work.resolve(); work.mkdir(parents=True, exist_ok=True)
evidence = work/'evidence'; evidence.mkdir(exist_ok=True)
env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
pins = json.loads((ROOT/'verification/results/native-archive-hashes.json').read_text())

def run(name, command, cwd=work):
    with (evidence/(name+'.log')).open('w') as log:
        log.write('COMMAND '+json.dumps([str(x) for x in command])+'\n'); log.flush()
        subprocess.run([str(x) for x in command], cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)

def archive(name, url, digest):
    target = work/name
    if not target.exists():
        with urllib.request.urlopen(url) as response, target.open('wb') as out:
            shutil.copyfileobj(response, out)
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise RuntimeError('Archive digest mismatch: '+name)
    with tarfile.open(target) as source:
        root = source.getnames()[0].split('/')[0]
        if not (work/root).exists():
            source.extractall(work, filter='data')
    return work/root

xy = archive('spice-xyce710.tar.gz', 'https://github.com/Xyce/Xyce/archive/refs/tags/Release-7.10.0.tar.gz', pins['spice-xyce710.tar.gz'])
tri = archive('spice-trilinos.tar.gz', 'https://github.com/trilinos/Trilinos/archive/refs/tags/trilinos-release-16-1-0.tar.gz', pins['spice-trilinos.tar.gz'])
ng = archive('ngspice-47.tar.gz', 'https://downloads.sourceforge.net/project/ngspice/ng-spice-rework/47/ngspice-47.tar.gz', '894e649651f1838a14095e5a5439e7d3aa63e87ede14d283173fda4fcdef675f')
# Reproduce the already documented compiler fix, fail on an unexpected source.
patch = xy/'src/LinearAlgebraServicesPKG/N_LAS_BlockSystemHelpers.C'
text = patch.read_text()
if 'std::abs<double>(val)' in text:
    if text.count('std::abs<double>(val)') != 2:
        raise RuntimeError('Unexpected Xyce patch context')
    patch.write_text(text.replace('std::abs<double>(val)', 'std::abs(val)'))
# Apply missing standard declarations to the source generator input, not generated C.
mod = ng/'src/xspice/icm/xtradev/seegenerator/cfunc.mod'
data = mod.read_bytes()
if b'#include <stdlib.h>' not in data:
    mod.write_bytes(b'#include <stdlib.h>\n'+data)
(evidence/'source-patches.json').write_text(json.dumps({str(f.relative_to(work)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (patch,mod)},indent=2)+'\n')
triprefix = work/'trilinos'; xyprefix = work/'xyce'; ngprefix = work/'ngspice'
flags = ['-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_POSITION_INDEPENDENT_CODE=ON', '-DCMAKE_INSTALL_LIBDIR=lib', '-DBUILD_SHARED_LIBS=OFF', '-DCMAKE_Fortran_FLAGS=-fsecond-underscore', '-DTrilinos_ENABLE_Fortran=ON', '-DTrilinos_ENABLE_ALL_PACKAGES=OFF', '-DTrilinos_ENABLE_TESTS=OFF', '-DTrilinos_ENABLE_EXAMPLES=OFF', '-DTPL_ENABLE_MPI=OFF', '-DTPL_ENABLE_ParMETIS=OFF', '-DTPL_ENABLE_AMD=ON', '-DAMD_INCLUDE_DIRS=/usr/include/suitesparse', '-DEpetraExt_BUILD_BTF=ON', '-DEpetraExt_BUILD_EXPERIMENTAL=ON', '-DEpetraExt_BUILD_GRAPH_REORDERINGS=ON', '-DTrilinos_ENABLE_COMPLEX_DOUBLE=ON']
flags += ['-DTrilinos_ENABLE_'+name+'=ON' for name in ['Amesos','AztecOO','Belos','EpetraExt','Ifpack','NOX','Sacado','Teuchos','TrilinosCouplings']]
run('trilinos-configure', ['cmake','-S',tri,'-B',work/'trilinos-build','-G','Ninja','-DCMAKE_INSTALL_PREFIX='+str(triprefix),*flags])
run('trilinos-build', ['cmake','--build',work/'trilinos-build','--parallel',a.jobs])
run('trilinos-install', ['cmake','--install',work/'trilinos-build'])
run('xyce-configure', ['cmake','-S',xy,'-B',work/'xyce-build','-G','Ninja','-DCMAKE_BUILD_TYPE=Release','-DBUILD_SHARED_LIBS=ON','-DBUILD_TESTING=OFF','-DXyce_USE_FFT=ON','-DXyce_USE_FFTW=ON','-DCMAKE_INSTALL_RPATH='+str(xyprefix/'lib'),'-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON','-DXyce_PARALLEL_MPI=OFF','-DXyce_NONFREE_MODELS=OFF','-DXyce_RAD_MODELS=OFF','-DTrilinos_ROOT='+str(triprefix),'-DCMAKE_PREFIX_PATH='+str(triprefix),'-DCMAKE_INSTALL_PREFIX='+str(xyprefix)])
run('xyce-build', ['cmake','--build',work/'xyce-build','--parallel',a.jobs])
run('xyce-interface-build', ['cmake','--build',work/'xyce-build','--target','xycecinterface','--parallel',a.jobs])
run('xyce-install', ['cmake','--install',work/'xyce-build'])
ngbuild=work/'ngspice-build'; ngbuild.mkdir(exist_ok=True)
run('ngspice-configure', [ng/'configure','--prefix='+str(ngprefix),'--with-ngshared','--without-x','--disable-openmp','--disable-klu','--with-readline=no'],ngbuild)
run('ngspice-build', ['make','-j'+str(a.jobs)],ngbuild)
run('ngspice-install', ['make','install'],ngbuild)
for name, prefix, lib in [('ngspice_rc',ngprefix,'ngspice'),('xyce_step',xyprefix,'xycecinterface')]:
    run(name+'-compile',['c++','-std=c++20','-O2','-Wall','-Wextra','-Wpedantic','-Werror','-I'+str(prefix/'include'),ROOT/'verification/spice'/ (name+'.cpp'),'-L'+str(prefix/'lib'),'-l'+lib,'-Wl,-rpath,'+str(prefix/'lib'),'-o',work/name])
run('ngspice-rc', [work/'ngspice_rc',evidence/'ngspice-rc.csv'])
shutil.copyfile(ROOT/'verification/spice/xyce_step.cir',work/'xyce-step.cir')
run('xyce-step', [work/'xyce_step',work/'xyce-step.cir',evidence/'xyce-step.csv'])
run('emitter-compile',['c++','-std=c++20','-O2',ROOT/'verification/spice/conformance.cpp','-o',work/'emit'])
results=[]
for circuit in ['rlc','cubic']:
    deck=work/(circuit+'.cir')
    run(circuit+'-emit',[work/'emit',circuit,'xyce','hb','unused',deck])
    run(circuit+'-hb',[xyprefix/'bin/Xyce',deck])
    raw=pathlib.Path(str(deck)+'.HB.FD.csv'); shutil.copyfile(raw,evidence/raw.name)
    with raw.open() as stream: rows=[[float(v) for v in row] for row in list(csv.reader(stream))[1:]]
    fundamental=min(rows,key=lambda r:abs(r[0]-1e6))
    if circuit=='rlc':
        omega=2*math.pi*1e6; expected=1/(1000+1j*(omega*.001-1/(omega*1e-9)))
        error=abs(-complex(*fundamental[3:5])/(-.5j)-expected)/abs(expected)
    else:
        third=min(rows,key=lambda r:abs(r[0]-3e6))
        error=max(abs(2*abs(complex(*fundamental[3:5]))-.001075)/.001075,abs(2*abs(complex(*third[3:5]))-.000025)/.000025)
    results.append(dict(circuit=circuit,relative_error=error,tolerance=1e-3,passed=math.isfinite(error) and error<1e-3))
(evidence/'hb-results.json').write_text(json.dumps(results,indent=2)+'\n')
if not all(r['passed'] for r in results): raise SystemExit('HB benchmark failed')
print('Research RC/stepwise/HB subset passed; no PDK, OSDI or dependency-admission claim')
