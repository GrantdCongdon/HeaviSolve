# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Pinned native S1 source build; Python performs orchestration, never numerics."""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tarfile
import urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--prefix', type=pathlib.Path, required=True, help='Isolated MPI/hypre/OpenBLAS/METIS conda prefix')
p.add_argument('--work', type=pathlib.Path, required=True)
p.add_argument('--jobs', type=int, default=2)
a = p.parse_args()
prefix = a.prefix.resolve(); work = a.work.resolve(); work.mkdir(parents=True, exist_ok=True)
if ' ' in str(prefix) or ' ' in str(work):
    sys.exit('MPI wrapper/source build prefixes must be space-free')
if a.jobs < 1:
    sys.exit('jobs must be positive')
metadata = [json.loads(x.read_text()) for x in (prefix/'conda-meta').glob('*.json')]
if not metadata or any(x['name'] == 'parmetis' for x in metadata):
    sys.exit('Missing dependency metadata or prohibited ParMETIS environment')
(work/'environment.json').write_text(json.dumps(metadata, indent=2)+'\n')
env = dict(os.environ, OMPI_CC='cc', OMPI_CXX='c++', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
env['PATH'] = str(prefix/'bin')+os.pathsep+env['PATH']
hashes = json.loads((ROOT/'verification/results/native-archive-hashes.json').read_text())
archives = [
 ('mfem410.tar.gz','https://github.com/mfem/mfem/archive/refs/tags/v4.10.tar.gz','mfem-4.10'),
 ('petsc326.tar.gz','https://github.com/petsc/petsc/archive/refs/tags/v3.26.1.tar.gz','petsc-3.26.1'),
 ('slepc326.tar.gz','https://github.com/slepc/slepc/archive/refs/tags/v3.26.0.tar.gz','slepc-3.26.0'),
 ('superlu-dist921.tar.gz','https://github.com/xiaoyeli/superlu_dist/archive/refs/tags/v9.2.1.tar.gz','superlu_dist-9.2.1')]
for name, url, directory in archives:
    target = work/name
    if not target.exists():
        urllib.request.urlretrieve(url, target)
    if hashlib.sha256(target.read_bytes()).hexdigest() != hashes[name]:
        sys.exit('Archive hash mismatch: '+name)
    if not (work/directory).exists():
        with tarfile.open(target) as archive:
            archive.extractall(work, filter='data')
def run(label, command, cwd=ROOT, extra=None):
    print(json.dumps({'step':label,'command':[str(x) for x in command],'cwd':str(cwd)}), flush=True)
    current = dict(env, **(extra or {}))
    with (work/(label+'.log')).open('w') as log:
        completed = subprocess.run([str(x) for x in command], cwd=cwd, env=current,
                                   stdout=log, stderr=subprocess.STDOUT)
    if completed.returncode:
        print((work/(label+'.log')).read_text()[-12000:])
        sys.exit(completed.returncode)
suffix = '.dylib' if sys.platform == 'darwin' else '.so'
def library(name):
    candidates = [prefix/'lib'/('lib'+name+suffix),prefix/'lib'/('lib'+name+'.0'+suffix)]
    for path in candidates:
        if path.exists(): return path
    sys.exit('Shared library missing: '+name)
blas = library('openblas'); mpi = library('mpi')
petsc = work/'petsc-install'; slepc = work/'slepc-install'
run('petsc-configure',[sys.executable,'configure','PETSC_ARCH=arch-heavisolve-complex',
    '--with-scalar-type=complex','--with-debugging=0','--with-fc=0','--with-x=0',
    '--with-parmetis=0','--with-metis=0','--with-shared-libraries=1',
    '--with-mpi-dir='+str(prefix),'--with-blaslapack-lib='+str(blas),
    '--download-superlu_dist='+str(work/'superlu-dist921.tar.gz'),'--prefix='+str(petsc)],work/'petsc-3.26.1')
penv = {'PETSC_DIR':str(work/'petsc-3.26.1'),'PETSC_ARCH':'arch-heavisolve-complex'}
run('petsc-build',['make','-j'+str(a.jobs),'all'],work/'petsc-3.26.1',penv)
run('petsc-install',['make','install'],work/'petsc-3.26.1',penv)
senv = {'PETSC_DIR':str(petsc),'PETSC_ARCH':''}
run('slepc-configure',[sys.executable,'configure','--prefix='+str(slepc)],work/'slepc-3.26.0',senv)
run('slepc-build',['make','-j'+str(a.jobs)],work/'slepc-3.26.0',senv)
run('slepc-install',['make','install'],work/'slepc-3.26.0',senv)
mfem = work/'mfem-build'
run('mfem-configure',['cmake','-S',work/'mfem-4.10','-B',mfem,'-DCMAKE_BUILD_TYPE=Release',
    '-DMFEM_USE_MPI=ON','-DMFEM_USE_METIS=ON','-DMFEM_USE_LAPACK=ON',
    '-DMFEM_ENABLE_EXAMPLES=OFF','-DMFEM_ENABLE_MINIAPPS=OFF',
    '-DHYPRE_DIR='+str(prefix),'-DMETIS_DIR='+str(prefix),
    '-DBLAS_LIBRARIES='+str(blas),'-DLAPACK_LIBRARIES='+str(blas),
    '-DMPI_CXX_COMPILER='+str(prefix/'bin/mpicxx'),
    '-DMPI_CXX_COMPILER_INCLUDE_DIRS='+str(prefix/'include'),
    '-DMPI_CXX_HEADER_DIR='+str(prefix/'include'),'-DMPI_CXX_LIB_NAMES=mpi',
    '-DMPI_mpi_LIBRARY='+str(mpi),'-DMPI_CXX_LINK_FLAGS='])
run('mfem-build',['cmake','--build',mfem,'-j',str(a.jobs)])
build = work/'cavity-build'
run('cavity-configure',['cmake','-S',ROOT/'verification/fem-stack','-B',build,
    '-DCMAKE_BUILD_TYPE=Release','-DMFEM_DIR='+str(mfem),
    '-DHS_PETSC_ROOT='+str(petsc),'-DHS_SLEPC_ROOT='+str(slepc)])
run('cavity-build',['cmake','--build',build,'-j',str(a.jobs)])
run('cavity-test',['ctest','--test-dir',build,'-V'])
print((work/'cavity-test.log').read_text())
