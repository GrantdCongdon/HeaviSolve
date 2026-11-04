# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Build/load equivalent native C ABI bindings; Python is orchestration/oracle only."""
import argparse
import ctypes
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'verification/oracles'))
from slab import fundamental

parser = argparse.ArgumentParser()
parser.add_argument('--build', type=pathlib.Path, required=True)
parser.add_argument('--rustc', default='rustc')
parser.add_argument('--cxx', default='clang++')
args = parser.parse_args()
args.build.mkdir(parents=True, exist_ok=True)
sources = ROOT / 'verification/language'
mac = sys.platform == 'darwin'
extension = '.dylib' if mac else '.so'
records = []
for language in ('cpp', 'rust'):
    library = (args.build / ('slab-' + language + extension)).resolve()
    command = ([args.cxx, '-std=c++20', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                '-dynamiclib' if mac else '-shared', '-fPIC', str(sources / 'binding.cpp'),
                '-o', str(library)] + (['-framework', 'Accelerate'] if mac else ['-llapack'])
               if language == 'cpp' else
               [args.rustc, '--edition=2024', '--crate-type=cdylib', '-C', 'opt-level=2',
                '-D', 'warnings', str(sources / 'binding.rs'), '-o', str(library)])
    start = time.perf_counter()
    build = subprocess.run(command, capture_output=True, text=True)
    build_seconds = time.perf_counter() - start
    (args.build / (language + '-build.log')).write_text(build.stdout + build.stderr)
    build.check_returncode()
    native = ctypes.CDLL(str(library))
    call = native.hs_slab
    call.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t,
                     ctypes.POINTER(ctypes.c_size_t)]
    call.restype = ctypes.c_int
    output = (ctypes.c_double * 8)(*([-123.] * 8))
    count = ctypes.c_size_t()
    start = time.perf_counter()
    assert call(4, output, len(output), ctypes.byref(count)) == 0
    call_seconds = time.perf_counter() - start
    values = list(output[:count.value])
    assert count.value >= 2
    errors = [abs(values[0] - fundamental()), abs(values[1] - fundamental(True))]
    assert max(errors) < 1e-4, errors
    # The host view aliases caller-owned storage; native Vec/vector -> output copies.
    alias = (ctypes.c_double * 8).from_buffer(output)
    assert ctypes.addressof(alias) == ctypes.addressof(output)
    alias[7] = 42.
    assert output[7] == 42.
    snapshot = list(output)
    invalid = [call(0, output, len(output), ctypes.byref(count)),
               call(9, output, len(output), ctypes.byref(count)),
               call(1, None, len(output), ctypes.byref(count)),
               call(1, output, len(output), None)]
    assert invalid == [1, 1, 1, 1] and list(output) == snapshot
    assert call(1, output, 1, ctypes.byref(count)) == 2
    assert count.value >= 2 and list(output) == snapshot
    # A second allocation/call must not invalidate previously returned caller data.
    another = (ctypes.c_double * 8)()
    assert call(1, another, len(another), ctypes.byref(count)) == 0
    assert list(output) == snapshot
    records.append(dict(language=language, build_command=command, build_seconds=build_seconds,
                        refinement=4, call_seconds=call_seconds, indices=values,
                        fundamental_absolute_errors=errors, invalid_argument_statuses=invalid,
                        insufficient_capacity_status=2, caller_owned_alias=True,
                        native_result_copy=True, lifetime_independence=True, status='PASS'))
assert max(abs(a-b) for a,b in zip(records[0]['indices'], records[1]['indices'])) < 1e-10
print(json.dumps(dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    host=sys.platform, test='equivalent C ABI through ctypes; not nanobind/PyO3',
    source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in [sources/'binding.cpp', sources/'binding.rs', sources/'check_bindings.py',
                             sources/'slab.cpp', sources/'slab.rs']}, results=records), indent=2))
