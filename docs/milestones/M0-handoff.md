<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Running implementation handoff

Updated 2026-11-04. **M0 is not complete; M1 has not started.** This is the resumption entry point. Update it before interruption or after material results. Historical commands and intermediate findings are preserved in [session history](M0-session-history.md); its older status statements are superseded here.

## Authority and authorization

Read AGENTS.md and the full director plan before new architecture decisions. The Downloads original is currently missing. The complete851-line plan was recovered from this same chat's archived command outputs, cross-checked at overlapping ranges and against an independent225-line excerpt, and reread completely. It is retained privately in `.work/director-plan-recovered.md`. Do not publish it as original project documentation.

User scope is M0 only. Native solvers, shared GUI/Python API, user-defined processes, primary-source research, stored CI benchmarks, SPDX/DCO and ADR002 admission remain binding. No restricted PDK data. Defaults from section15 apply. The user explicitly approved pushing source/reports/screenshots/test output to the public **m0-evidence review branch**. Do not ask again for that action. Remote main must remain unchanged at1c9b432e0de5e322dd2b66d684998b6c9c3537ee; approval to publish a review branch is not approval to merge main.

## Current assessment

- Section12 acceptance: revised local `ctest --test-dir build-numerical -L m0` **3/3 PASS** (Poisson, cavity, evidence gate). Foundation **3/3 PASS**. Logs: `verification/results/{m0-acceptance-current,foundation-current}.log`.
- Full review `python3 tools/m0_gate.py --stage all` deliberately fails: Accepted/merged ADRs remain open; ADR008 now records the PhaseR component dispositions. Acceptance does not equal milestone exit.
- ADR007 corrects our earlier overbroad all-spikes-pass gate. Section12 requests completed spike reports; full supported-engine SPICE conformance is M7. Original S3c failures remain failures. The walking-skeleton design/self-review is written, **design only**.
- Baseline Linux/macOS CI has passed all six jobs; retained artifact provenance at `verification/results/ci-41668976621`. The revised aggregate acceptance passed all6 jobs in41922593403 on239cb7f, including3/3 M0 checks on each platform. Verified numerical/language artifacts and foundation logs are retained at verification/results/ci-41922593403. Earlier41858845340 had cancelled macOS jobs and is not counted as a complete pass.
- Complex S1 **PASS both platforms** on cb9d540, run41715967429. SHA256-verified outputs in `verification/results/ci-41715967429`. First-six cavity relative errors4.943565595971755e-5 Linux and4.9435655969265468e-5 macOS. One MPI rank only; Linux UCX warning/fallback retained. Do not repeat this heavy build absent changed inputs.
- Container **PASS**, initial run41858845826 on ceeb4d7 (2/2) and updated run41922593302 on239cb7f (3/3). Both verified build/test/image-ID artifacts are retained under their ci-* result directories. Image built/tested, not published.
- Linux SPICE run41858845394 on ceeb4d7 **PASS**; verified complete logs and RC/API/HB results are retained at verification/results/ci-41858845394. Prior failures: ngspice generator byte encoding (fixed); unintended Trilinos optional NetCDF (disabled); missing FLEX header after successful Trilinos build (libfl-dev added). Retained failure artifacts at ci-41768804564 and ci-41769077217.
- Local Xyce7.10 forward stepping **PASS**,50 stops, maximum absolute error7.1045086396173684e-7V. HB RLC/cubic also localPASS. ngspice47 callbacks/OSDI localPASS. Neither production adapter is complete or admitted by these results.
- S3c original IHP self-heated AC differs8–10%; strict DC relative base-current error1.0304146187721579e-4 exceeds1e-4. Isothermal AC/transient pass. Disabling avalanche in marked copies reduces DC discrepancy to4.317717800750406e-9; original models/tolerances unchanged. Shared compact-model/compiler route remains untested. These are M7 integration risks.
- S4 local meshingPASS. S5/S6 repaint throughput measured, not compositorfps. KLayout layout geometryPASS; gdstk SiEPIC OASFAIL. S7 local100MB mapped native-process pathPASS, not universal zero-copy. Detailed reports preserve all limitations.
- New bounded ngspice47 source-license mapping is documented, but no scanner exception/admission has been granted. Source-grant review and release binary audit are distinct obligations.

## Immediate next actions

1. Inspect git status before editing. All required hosted research/acceptance results are now recorded; no heavy rebuild is needed without changed inputs. Latest tested executable revision is239cb7f; later evidence/report-only commits retain the outputs.
2. ADR008 records explicit PhaseR dispositions, including deferred candidates and rejected defaults. Review these without admitting unknown dependency graphs through a documentation flag.
3. The review package contains report, one-page decisions and next-checkpoint plan. Validate docs/REUSE/DCO and publish remaining evidence commits to **m0-evidence only**. Prepare/review the pull request; do not change remote main under review-branch-only approval.
4. Keep exit false until ADR integration actually occurs. The only remaining M0 exit item is merging the reviewed ADRs. The previous upload approval expressly left remote main unchanged; obtain approval for the concrete reviewed integration before merging. After authorized integration, record merge evidence and final exit/report metadata; stop before M1.

## Reproduction and persistent evidence

- Foundation: `cmake -S . -B build`; `ctest --test-dir build -L foundation --output-on-failure`.
- Numerical: existing `build-numerical` uses `.work/mfem-build`; `ctest --test-dir build-numerical -L m0 --output-on-failure`.
- Policy/docs: `.work/tools-env/bin/reuse lint`; `.work/tools-env/bin/python tools/build_docs.py`; `python3 tools/license_scan.py`. DCO script requires full base/head hashes.
- Native stack recipes: `tools/build_complex_stack.py`, `tools/build_spice_stack.py`. SPICE recipe explicitly requires research-candidate mode; this does not grant production admission.
- Local SPICE prefix `/tmp/heavisolve-spice/install`; Xyce `/tmp/heavisolve-spice/xyce`; C interface `/tmp/heavisolve-spice/xyce-build/utils/XyceCInterface/libxycecinterface.dylib`; Trilinos `/tmp/heavisolve-spice/trilinos`. Temporary prefixes may disappear: committed scripts, pinned hashes and raw results are authoritative.
- Language toolchain `.work/language/cargo/bin/rustc`, isolated RUSTUP_HOME/CARGO_HOME under `.work/language`. GUI `.work/gui-env` and `.work/gui-build`; IPC `/tmp/heavisolve-ipc` and `.work/ipc-build`. More exact historical commands are in session history.
- GitHub connector GET supports run/job/artifact metadata; download workflow artifacts, verify archive SHA256 and retain selected outputs plus provenance. Never store signed download URLs.
- Do not commit `.work`, `.local`, environments, downloaded PDK fixtures or hardware identifiers. Preserve failed numerical output; do not hand-edit measurements.

## Final review checkpoint

Draft [pull request1](https://github.com/GrantdCongdon/HeaviSolve/pull/1) is open from m0-evidence to main. Evidence/report checkpoint846c778 contains the stored passing runs; executable sources/workflows match tested239cb7f. Acceptance and deliverables pass; only `exit.adrs_accepted_and_merged` remains false. Before merging, verify current PR checks and obtain the separate integration approval: prior approval only covered review-branch publication. After approval, preserve DCO history and record the actual merge before marking exit complete. Do not start M1.

The connector can read PRs and Actions but its PR-create operation returned403. The installed `gh` client works with network permission and created the draft; its restricted-network auth check misleadingly reported an invalid token, while the permitted check succeeded. Do not reauthenticate or replace credentials. Source/report uploads remain authorized to m0-evidence. This is a capability limitation, not an automatic approval rejection.
