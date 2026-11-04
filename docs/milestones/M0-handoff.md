<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Running implementation handoff

Updated: 2026-11-03 (America/Indiana/Indianapolis). **M0 incomplete. Never start M1 until the M0 exit criteria pass and the director receives the report.** Update this document before ending a work session and after material results. It is the resumption entry point; use the linked reports and raw evidence rather than reconstructing state from chat.

## Authority and workspace

Read `/Users/grantdcongdon/Downloads/integrated-photonics-eda-plan.md` completely before making new architecture decisions. User directs M0 only, parallel research where useful, small DCO-signed commits, no Python solvers, same GUI/Python API, PDK independence, primary-source verification and no fabricated numbers. Questions restricted to section15; defaults apply. Never bundle restricted PDK data or call a solver verified without passing CI and stored outputs.

Repository: `/Users/grantdcongdon/Documents-local/Projects/Quantum Optics Statistical Solver/heavisolve`. Branch main. Implementation checkpoints: `901e872` transitive audit, `8fd4c04` native feasibility evidence, `d4da96e` SPICE conformance. The final report/handoff checkpoint follows these; inspect current git log/status for its hash. Do not discard uncommitted work if any appears. `git status --short` is authoritative. Prior agents may have hit usage limits; their file outputs are shared, but do not assume a running agent survives interruption.

## Current result summary

- Serial MFEM4.8 Poisson convergence and cavity local PASS; stored old failures retained.
- C++/Rust independent mixed-element slab, four refinements: local PASS, second-order convergence; portable CMake/macOS repeat PASS. ADR001 scores134/86. Equivalent ctypes/C-ABI binding experiment now passes for both languages (commit fb2302f). Nanobind/PyO3 comparison and reliable historical engineering-time records remain unmeasured.
- S3a ngspice47 native callback RC, IHP HBT and OpenVAF-compiled OSDI PASS locally.
- Xyce7.10 now builds on macOS, and its C interface passes50-step RC testing; native shared circuit IR and per-engine emitters run RC/RLC/diode/IHP DC/AC/transient. HB RLC/cubic local PASS. IHP AC differs8–10%; strict DC settings still differ1.0304146e-4 against1e-4 tolerance; avalanche-off diagnostic localizes the difference without passing the original model. Do not change pinned models or relax tolerance to claim success. ADR003 co-primary targets,98/160 vs94/160; acceptance blocked.
- S4 custom256-prism ring passes positive-Jacobian/volume/MFEM H(curl) import checks; Gmsh/Netgen quality pass after retained initial failure.
- S5 Qt6.12/VTK9.7.1 visible cut plane and10k polygons:75.7988 repaint/s at798×717,dpr2; earlier56.1598 failure retained. Repaint throughput is not compositor presentation rate.
- S6 KLayout pinned IHP and SiEPIC GDS/OAS geometry roundtrips PASS; gdstk SiEPIC OAS changes geometry and FAILS. Million-polygon revised viewport68.2641 repaint/s; earlier58.3282 failure retained. Clipper booleans pass but upstream archived.
- S7 gRPC/protobuf and ZeroMQ/FlatBuffers separately launched native processes map100MB, checksum and progress PASS; no array bytes in control channel. No profiler-based universal zero-copy or remote transport claim.
- R1 maintenance sweep now has41 exact GitHub head commit dates/SHAs; archived candidates flagged. Direct dependency inventory updated, unknown mixed ngspice licensing kept outside approved entries.

## Immediate next work

1. Complex-stack run41715967429 on cb9d540 passes BOTH Linux/macOS. SHA256-verified artifacts13270113949/13270538208 and numerical/configuration/environment/license output are retained in verification/results/ci-41715967429. S1 platform/cavity gate is true; no need to rebuild it absent changes. Current remaining hosted gap is SPICE: first Linux run41768558047 failed before compilation on a non-UTF8 ngspice generator input. The recipe now uses byte-preserving patching; push/check the next run and retain concrete failures.
2. Resolve IHP conformance using scoped diagnostics. Isothermal AC/transient pass; original self-heated AC and strict DC base-current comparison fail. Preserve original models, outputs and thresholds. See S3 follow-up; matching copied ikp/delay did not fix failures.
3. Finish Xyce native stepwise API experiment verification/spice/xyce_step.cpp. Build the upstream excluded target xycecinterface, then link libxycecinterface (libxyce alone lacks C interface symbols). Executable and circuit at /tmp/heavisolve-spice/xyce-step*. Results saved under verification/results/s3-xyce-step*. Runtime PASS is stored with50 samples and maximum error7.1045086396173684e-7V. Linux SPICE/source recipes and full integration license audits remain open.
4. Keep reports, decisions and task list synchronized. Historical engineering hours cannot be reconstructed; do not invent them. The authoritative Downloads plan is currently missing; read it if restored before new architecture decisions.
5. Run foundation, REUSE, strict docs, DCO and applicable tests; store results. The M0 gate must remain false for missing evidence. Commit small DCO-signed checkpoints and push only m0-evidence, authorized by user. Remote main must remain unchanged.

## Build locations and commands

- `.work/tools-env/bin/reuse lint`; `.work/tools-env/bin/python tools/build_docs.py`; `python3 tools/license_scan.py`; `python3 verification/license_audit_test.py`.
- Language: `cmake -S verification/language -B <build>`; `python3 verification/language/compare.py <build>`. Isolated Rust uses `.work/language/cargo/bin/rustc`, with absolute RUSTUP_HOME `.work/language/rustup`, CARGO_HOME `.work/language/cargo`.
- Qt/VTK: `.work/gui-env`, `.work/gui-build/gui_spike small|million <png>`. Visible Cocoa execution requires permission outside restricted execution. Do not rerun under load to cherry-pick a pass.
- IPC: `/tmp/heavisolve-ipc`, `.work/ipc-build`; verification/ipc/run_compare.py. Local sockets need execution permission in this environment.
- SPICE: `/tmp/heavisolve-spice/install` ngspice shared; `/tmp/heavisolve-spice/xyce/bin/Xyce`; Trilinos16.1 `/tmp/heavisolve-spice/trilinos`. Xyce7.10 source patch `std::abs<double>(val)`→`std::abs(val)` in N_LAS_BlockSystemHelpers.C; Trilinos Fortran required `-fsecond-underscore`; build with M4 pointing to `/tmp/heavisolve-spice/deps/bin/m4`. All archives hashes stored in verification/results/native-archive-hashes.json.
- Clean FEM: OpenMPI wrappers require OMPI_CC=clang OMPI_CXX=clang++; OpenBLAS actual file is libopenblas.0.dylib. PETSc configure disabled ParMETIS/METIS, complex scalar, source SuperLU_DIST9.2.1. Configure/build/install logs in `/tmp/heavisolve-petsc-*.log`, `/tmp/heavisolve-slepc-*.log`; MFEM logs `.work/mfem410-clean-*.log`. Full exact source archives remain `.work` (ignored); never assume /tmp persists forever.

## External blockers and cautions

Baseline Linux/macOS CI has passed all six jobs (run41668976621); outputs and SHA256-verified artifact provenance are in verification/results/ci-41668976621. Later baseline runs also passed; latest41715967441 was finishing its Linux numerical job. The public canonical remote is git@github.com:GrantdCongdon/HeaviSolve.git. The user explicitly approved publishing M0 source/reports/screenshots/test outputs to m0-evidence. Push authorization persists. Remote main remains at1c9b432e0de5e322dd2b66d684998b6c9c3537ee. Earlier automatic review rejections were resolved by user approval and an archive content audit; no unresolved upload-permission blocker remains.

GitHub connector cannot create repositories/dispatch workflows, but supports reading repository Actions endpoints. Native Firefox automation hung previously; avoid it.

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

- Latest resumed work: binding experiment LOCAL PASS, explicit-prefix FEM CMake/CTest LOCAL PASS, exact clean-environment license metadata audit PASS. Agent IHP diagnostics localized dominant AC discrepancy to self-heating: both engines DC finite-difference slope~-4.5841, Xyce low-frequency AC~-4.58408, ngspice~-4.20135; isothermal AC/transient pass but base-current DC remains just above1e-4. New diagnose_ihp_dc.py explores copied model ikp/delay without changing originals or tolerances. Its output and repeated gmin sweep are in progress; review completed files before documenting. Both research agents hit usage limits; do not assume their docs were finalized. Current uncommitted diagnostic files must be preserved.

- IHP follow-up completed: self-heated AC discrepancy localized with finite-difference DC slopes, isothermal AC/transient pass, strict DC remains1.0304146e-4 (FAIL). Matching copied-model ikp/delay does not fix DC. New raw diagnostic archive excludes model files; S3 report updated. Upload approval explicitly received in chat; review-branch push in progress.

- Hosted CI checkpoint: user-approved push succeeded. Canonical repository GrantdCongdon/HeaviSolve, branch m0-evidence. Baseline run41668976621 on47b8352 passed all6 jobs; numerical/language artifact ZIP digests verified and outputs retained in verification/results/ci-41668976621. Two factual gate flags now true: ci_stored_numerical_outputs and ci_license_scan_green. Full M0 remains open.
- Complex CI: first run41669787651 failed macOS missingCONDA and Linux libopenblas.so.0 lookup; failures retained. Commit3185ea9 fixes both. Run41670183802 is actively compiling on both platforms. tools/build_complex_stack.py builds pinned PETSc/SLEPc/SuperLU_DIST/MFEM and disables ParMETIS and X11; platform-support packages from conda. Exact Linux package reviews added to ADR006 and manifest after downloading14 archive identities and checkinglicense evidence. These new reviews are not pushed yet, so the currently running Linux audit may fail with the older policy even if numerics succeed. Need review latestmacOS metadata too, commit policy updates, and rerun as necessary.
- Upload review initially rejected the11MB diagnostic archive as possibly containing PDK data; inspection proved all170 entries are own decks/numericCSV/logs/JSON, no model definitions/files. The audit is committed, and review-branch push then succeeded. Authorization persists; do not ask again absent a materially different payload.

- Current continuation: baseline evidence retained; macOS complex CI artifact13249002660 SHA256 checked and selected logs saved. Latest cb9d540 fixes Linux SLEPC_DIR and adds14 exact Linux package reviews; current complex run41715967429 building. Xyce C API experiment added; initial libxyce-only link failed, upstream xycecinterface target builds successfully. Runtime LOCAL PASS:50 stops, maximum absolute error7.1045086396173684e-7V <1e-4V; source/deck/output hashes saved. M1 untouched.

- Latest diagnostic: verification/spice/diagnose_ihp_avalanche.py reproduces strict DC baseline then disables avc1 in both separate copies. Error falls from1.0304146187721579e-4 to4.317717800750406e-9, max8.623976484614605e-16A. Source hashes/formulas retained in s3-ihp-avalanche-provenance.json; ngspice and Xyce VBIC1.3 avalanche smoothing differ. Original models/tolerances unchanged, baseline stillFAIL. Potential next route: same versioned VA compact model via OSDI/ADMS, subject to grant/compiler/thermal checks. No compiler route attempted yet.
- Continuation checks: local numerical-build M0 CTest has Poisson/cavityPASS and acceptancegateFAIL. Foundation-only build predictably lacks MFEM; separate failure log retained. DCO trailers pass12 commits through802241c; subsequent5eff73a signed survey updates resolve HSPICE/RSoft/pyEPR primary sources. Review branch pushed through802241c, later changes require a final commit/push. M1 untouched.

- Plan recovery: /tmp/heavisolve-binding-plan-read.txt contains the first225 lines of the director plan (through start of3.1), fully reread this session. It confirms S1 hosted complex-cavity and S3b Linux/macOS build requirements, and S3c unchanged tolerances. It is only a partial copy and does not restore section12 or later appendices. Original Downloads file remains unavailable; do not treat this excerpt as the complete plan.

- S3b scope reconciliation from retained plan excerpt: native forward stepping addresses the API feasibility question; remaining S3b required gap is Linux build. Rollback/general external-device exchange remain reported limitations, not newly invented S3b exit criteria. A subagent is preparing tools/build_spice_stack.py and .github/workflows/spice-research.yml for review; do not assume unpublished files or runs exist.

- S1 closure: Linux complex job126195902515 in run41715967429 succeeded on cb9d540. Artifact13270113949 SHA256 a13e4b29801d12457dd1a7b93a9af5946c4bdb864d765ed4ccf303f22fca946d verified; selected output/config/environment/license logs retained in verification/results/ci-41715967429. Maximum first-six cavity error4.943565595971755e-5. One-rank success follows UCX initialization failure, so no UCX/multi-rank claim. Prior macOS run41670183802 already passed; full_fem_stack_linux_macos now true. Current macOS rerun still in progress; retrieve it when complete for same-revision evidence.

- Linux SPICE recipe reviewed: tools/build_spice_stack.py + .github/workflows/spice-research.yml. Trigger is push of relevant paths to authorized m0-evidence branch or manual dispatch. Existing research candidates only; explicit research flag, no PDK/OSDI download, no production admission. New source patches target exact Xyce abs calls and ngspice generator input. Local Python syntax/help checked; native Linux build still unexecuted until pushed CI finishes. Need inspect logs, fix concrete build errors, retain failed output and do not mark conformance passed.

- Same-revision complex FEM completion: macOS job126195902261 passed; artifact13270538208 SHA2565a70e84447dd5add61f23d25dec36d74e6141666097e9405c24576ebbeefef55 verified. Bothplatform outputs saved. Linux SPICE first run41768558047 failed at cfunc.mod UTF8decode; byte-preserving patch tested locally, next CI pending. Full failure excerpt stored as spice-linux-first-failure.log.
