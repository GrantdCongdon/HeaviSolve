<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Running implementation handoff

Updated: 2026-11-03 (America/Indiana/Indianapolis). **M0 incomplete. Never start M1 until the M0 exit criteria pass and the director receives the report.** Update this document before ending a work session and after material results. It is the resumption entry point; use the linked reports and raw evidence rather than reconstructing state from chat.

## Authority and workspace

Read `/Users/grantdcongdon/Downloads/integrated-photonics-eda-plan.md` completely before making new architecture decisions. User directs M0 only, parallel research where useful, small DCO-signed commits, no Python solvers, same GUI/Python API, PDK independence, primary-source verification and no fabricated numbers. Questions restricted to section15; defaults apply. Never bundle restricted PDK data or call a solver verified without passing CI and stored outputs.

Repository: `/Users/grantdcongdon/Documents-local/Projects/Quantum Optics Statistical Solver/heavisolve`. Branch main. Implementation checkpoints: `901e872` transitive audit, `8fd4c04` native feasibility evidence, `d4da96e` SPICE conformance. The final report/handoff checkpoint follows these; inspect current git log/status for its hash. Do not discard uncommitted work if any appears. `git status --short` is authoritative. Prior agents may have hit usage limits; their file outputs are shared, but do not assume a running agent survives interruption.

## Current result summary

- Serial MFEM4.8 Poisson convergence and cavity local PASS; stored old failures retained.
- C++/Rust independent mixed-element slab, four refinements: local PASS, second-order convergence; portable CMake/macOS repeat PASS. ADR001 scores134/86. Missing actual binding-effort experiment and reliable historical engineering-time records.
- S3a ngspice47 native callback RC, IHP HBT and OpenVAF-compiled OSDI PASS locally.
- Xyce7.10 now builds; native shared circuit IR and per-engine emitters run RC/RLC/diode/IHP DC/AC/transient. HB RLC/cubic local PASS. IHP AC differs8–10%; tighter DC settings still differ1.0325884e-4 against1e-4 tolerance. Do not change pinned models or relax tolerance to claim success. ADR003 co-primary targets,98/160 vs94/160; acceptance blocked.
- S4 custom256-prism ring passes positive-Jacobian/volume/MFEM H(curl) import checks; Gmsh/Netgen quality pass after retained initial failure.
- S5 Qt6.12/VTK9.7.1 visible cut plane and10k polygons:75.7988 repaint/s at798×717,dpr2; earlier56.1598 failure retained. Repaint throughput is not compositor presentation rate.
- S6 KLayout pinned IHP and SiEPIC GDS/OAS geometry roundtrips PASS; gdstk SiEPIC OAS changes geometry and FAILS. Million-polygon revised viewport68.2641 repaint/s; earlier58.3282 failure retained. Clipper booleans pass but upstream archived.
- S7 gRPC/protobuf and ZeroMQ/FlatBuffers separately launched native processes map100MB, checksum and progress PASS; no array bytes in control channel. No profiler-based universal zero-copy or remote transport claim.
- R1 maintenance sweep now has41 exact GitHub head commit dates/SHAs; archived candidates flagged. Direct dependency inventory updated, unknown mixed ngspice licensing kept outside approved entries.

## Immediate next work

1. Clean complex FEM cavity is now LOCAL PASS; final source build and explicit-link command are below. Finish its remaining transitive-license review and portable build recipe/CI execution. `verification/fem-stack` CMake still needs a pkg-config executable on this host; the local direct compile bypassed that missing tool. Do not repeat the lengthy source build unless necessary.
2. Resolve IHP conformance using scoped diagnostic experiments. Preserve original model files, results and tolerances. Distinguish engine equations, model parameters, temperature/self-heating and linearization; no model normalization has yet been validated. Consider a separate normalized diagnostic copy only with explicit provenance, never overwrite pinned originals.
3. Review agent-produced S3 sources/results/docs; agent ended with usage limit. Raw conformance JSON, tight-DC JSON, output archive/provenance are in verification/results. Preserve conformance failures; primary source model differences need investigation.
4. Reports/decisions/tasks are refreshed through the clean cavity result. Keep them current; add missing binding-effort evidence and reproducible source recipes.
5. Run foundation, REUSE, strict docs, DCO and numerical tests; store outputs. `ctest -L m0` must still fail for missing evidence. Do not toggle boolean gates merely to satisfy the command.
6. Continue small DCO-signed commits. No remote is configured. Report honestly before M1; do not label M0 complete while blockers remain.

## Build locations and commands

- `.work/tools-env/bin/reuse lint`; `.work/tools-env/bin/python tools/build_docs.py`; `python3 tools/license_scan.py`; `python3 verification/license_audit_test.py`.
- Language: `cmake -S verification/language -B <build>`; `python3 verification/language/compare.py <build>`. Isolated Rust uses `.work/language/cargo/bin/rustc`, with absolute RUSTUP_HOME `.work/language/rustup`, CARGO_HOME `.work/language/cargo`.
- Qt/VTK: `.work/gui-env`, `.work/gui-build/gui_spike small|million <png>`. Visible Cocoa execution requires permission outside restricted execution. Do not rerun under load to cherry-pick a pass.
- IPC: `/tmp/heavisolve-ipc`, `.work/ipc-build`; verification/ipc/run_compare.py. Local sockets need execution permission in this environment.
- SPICE: `/tmp/heavisolve-spice/install` ngspice shared; `/tmp/heavisolve-spice/xyce/bin/Xyce`; Trilinos16.1 `/tmp/heavisolve-spice/trilinos`. Xyce7.10 source patch `std::abs<double>(val)`→`std::abs(val)` in N_LAS_BlockSystemHelpers.C; Trilinos Fortran required `-fsecond-underscore`; build with M4 pointing to `/tmp/heavisolve-spice/deps/bin/m4`. All archives hashes stored in verification/results/native-archive-hashes.json.
- Clean FEM: OpenMPI wrappers require OMPI_CC=clang OMPI_CXX=clang++; OpenBLAS actual file is libopenblas.0.dylib. PETSc configure disabled ParMETIS/METIS, complex scalar, source SuperLU_DIST9.2.1. Configure/build/install logs in `/tmp/heavisolve-petsc-*.log`, `/tmp/heavisolve-slepc-*.log`; MFEM logs `.work/mfem410-clean-*.log`. Full exact source archives remain `.work` (ignored); never assume /tmp persists forever.

## External blockers and cautions

Hosted Linux/macOS CI is not executed. GitHub connector is authenticated but lacks repository creation/workflow dispatch capabilities; no heavisolve remote exists. In-app browser github.com/new redirected to sign-in. Do not retrieve credentials or claim CI green. Native Firefox automation hung previously; avoid retrying it. No deployment/publication requested.

Do not commit `.work`, `.local`, downloaded PDK fixtures, full hardware identity output or binary environments. REUSE aggregate covers original generated results; third-party content requires its own licensing. New source files need SPDX headers. Code-generated SPDX strings must split the literal marker to avoid REUSE parsing them as malformed source headers. Keep raw failed measurements, and identify changed source hashes separately rather than rewriting old output.

## Running session ledger

- 2026-11-03: resumed after usage limit; clean MFEM and SLEPc builds found complete; final cavity CMake blocked by missing pkg-config executable. Created this handoff at user request. Next actions above remain active.
- 2026-11-03 follow-up: clean complex cavity now completed PASS (maximum frequency error4.9435655966822978e-5). Explicit clang++ link bypassed missing pkg-config; output stored as `verification/results/fem-clean-cavity.log`. S1 and M0 report/decisions refreshed. Foundation2/2 and REUSE pass; M0 gate remains intentionally failing. Finish review, exact command/provenance preservation and commits next.

### Final cavity compile command used locally

Run from the repository root after the source stacks have built (research-only, not a portable installer):

```sh
clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  -isystem .work/mfem410-clean-build -isystem .work/mfem-4.10 \
  -isystem /tmp/heavisolve-fem-clean/include \
  -isystem /tmp/heavisolve-fem-clean/petsc/include \
  -isystem /tmp/heavisolve-fem-clean/slepc/include \
  verification/fem-stack/cavity.cpp .work/mfem410-clean-build/libmfem.a \
  -L/tmp/heavisolve-fem-clean/lib -L/tmp/heavisolve-fem-clean/petsc/lib \
  -L/tmp/heavisolve-fem-clean/slepc/lib -lslepc -lpetsc -lHYPRE -lmetis -lmpi \
  -framework Accelerate -Wl,-rpath,/tmp/heavisolve-fem-clean/lib \
  -Wl,-rpath,/tmp/heavisolve-fem-clean/petsc/lib \
  -Wl,-rpath,/tmp/heavisolve-fem-clean/slepc/lib \
  -o .work/fem-clean-cavity/complex-cavity
.work/fem-clean-cavity/complex-cavity
```

PETSc uses OpenBLAS; MFEM's auxiliary LAPACK symbols use host Accelerate in this local link. Direct binary linkage is recorded in `verification/results/fem-clean-direct-linkage.log`; this is not a recursive distribution audit.

- 2026-11-03 checkpoint: implementation saved in three DCO-signed commits listed above. Foundation2/2, REUSE170/170 and strict docs pass locally; numerical M0 tests pass but acceptance gate fails. Only factual slab-comparison and measured-SPICE-scoring flags changed to true. Reports and handoff refreshed; M1 untouched. Final reporting checkpoint commits research maintenance evidence and continuity files.
