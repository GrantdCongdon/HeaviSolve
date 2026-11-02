<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# R6: SPICE engine comparison

Research date: 2026-11-02. Status: **incomplete experimental gate**. Documentation evidence is not a benchmark result. Neither engine is claimed verified or fully compatible.

## Primary-source findings

| Question | ngspice | Xyce |
|---|---|---|
| Version / maintenance evidence | Official NEWS lists 47, released 2026-08-11 [1]. Release 47 source downloaded for this spike. | GitHub release listing identifies 7.10 as latest [2]; current master source contains 7.11 build changes. Downloaded master is an exploratory snapshot, not an approved release pin. A full commit/date pin is still required. |
| Method and language | C SPICE-family nonlinear circuit simulation. | C++ differential-algebraic circuit solver, serial/MPI. |
| License | Release 47 COPYING: primarily modified BSD (BSD-3-Clause), with MPL-2.0 OSDI, LGPL numparam, public-domain XSPICE and GPL-2.0-or-later table code. Do not inventory the whole distribution as BSD alone. | COPYING is GPLv3; `src/CircuitPKG/N_CIR_Xyce.C` explicitly permits v3 or later. GPL-3.0-or-later candidate under ADR-002. |
| Library API | Official shared-library documentation exposes simulation control, callbacks and data vectors [3]. Release header exports `ngSpice_Init_Sync`, external voltage/current callbacks, and synchronization callback. | `Circuit::Simulator::simulateUntil(requestedUntilTime, completedUntilTime)` is in the downloaded header. General-coupling application note documents time advancement and external device coupling [4]. Library co-simulation exists; suitability and rollback need experiments. |
| Analyses | Standard circuit analyses; OSDI documented since v39 [5]. No harmonic-balance compatibility claim is made. Periodic steady-state news is not proof of HB equivalence. | Official description lists DC, transient, AC, noise, HB and MPDE [6]. FFT dependency is required for HB. |
| SG13G2 Verilog-A route | IHP: OpenVAF compiles OSDI binaries. | IHP: ADMS compiles Xyce shared-library plugins [7]. This is distinct from OpenVAF/OSDI. |
| Build/platform | Shared-library release build attempted on macOS arm64. Linux not run in this session. | CMake configure on macOS failed on missing Trilinos. No Linux execution evidence. Current source guide requires C++17, Trilinos >=14.4 (versions beyond16.1 untested), SuiteSparse AMD/config and flex/bison; FFTW for HB [8]. |
| Interchange | Must emit engine-specific analysis/output syntax and model bindings. `.control` is not a portable IR construct. | SPICE3F5-like syntax with extensions is documented [9]; do not assume arbitrary ngspice netlists translate losslessly. |
| Strength | Small C embedding interface and explicit external-source callback. | HB and large-circuit parallelism; documented library stepping. |
| Limitation | Engine global state motivates separate workers; platform/compiler and model ABI must be tested. | Build weight; device/plugin compilation differs; API behavior unmeasured here. |

## Weighted evaluation

The director requires 1–5 scores supported by S3a–c measurements. Unmeasured categories are **not scored**; assigning neutral scores would fabricate a comparison. Weight total is 32; normalized score is `100 * sum(weight * score)/(5 * 32)`. A primary engine requires a lead of at least15 percentage points and no uniquely necessary weight-5 capability in the other engine.

| Criterion | Weight | ngspice score | Xyce score | Evidence still required |
|---|---:|---|---|---|
| Embeddability / co-simulation | 5 | Pending | Pending | External-source RC, step synchronization, reset/restart and worker isolation |
| Analysis coverage | 5 | Pending | Pending | Executed DC/AC/transient/noise plus HB and transient-FFT comparison |
| Open-PDK device coverage | 5 | Pending | Pending | SG13G2 MOS/HBT/passives, SKY130 and GF180 model runs |
| Accuracy | 4 | Pending | Pending | VER-SP-01…05 and engine conformance |
| Build / distribution | 4 | Pending | Pending | Linux/macOS reproducible builds; Windows optional |
| Scalability | 3 | Pending | Pending | Same large circuit, resource/time measurements |
| Dialect / ecosystem | 3 | Pending | Pending | Common IR corpus and explicit translation differences |
| License / maintenance | 3 | Pending | Pending | Complete linked-dependency inventory and pinned maintenance evidence |
| Normalized total | 32 | Not computable | Not computable | No numerical ranking until complete |

There is no demonstrated clear winner. **Provisional Outcome B** retains both as first-class integration targets, without claiming that two working adapters exist. The M0 gate remains open. See ADR-003.

## Candidate integration rubric

Both are candidates, not approved solver integrations. License review is partially supported; APIs are documented. Benchmark pass, full maintenance pinning and lossless circuit/model mapping are not demonstrated. Do not replace them with a new SPICE solver: section4.7 explicitly forbids that. Keep candidate status until requirements pass.

## Dialect and validation contract

The future common IR must encode typed device instances, SI-valued parameters, connectivity, analysis requests and engine-specific model bindings. Emit `.tran`, `.ac`, `.dc` and output selection per engine; reject unsupported elements. Store exact emitted decks. Run RC, RLC, diode, HBT/MOS amplifier and pinned IHP cases against each engine's standalone execution. Record interpolation grid and units before cross-engine comparison. Initial tolerances: DC relative1e-4, AC1e-3, transient NRMSE1e-3; define absolute floors at zero crossings before running, and document any change. No conformance corpus has passed yet.

## OpenVAF caution

The original project and community forks must not be conflated. OpenVAF-Reloaded documents OSDI0.4 versus earlier0.3 and different binary names [10]. Pin compiler, emitted ABI and simulator together. Its repository warns that some integration-test model licenses differ from the compiler license [11]; do not redistribute that fixture tree indiscriminately. No OpenVAF toolchain was installed for this spike. Local callback RC and an IHP VBIC smoke test subsequently passed; see S3 for measurements. These do not close OSDI or cross-engine gates.

## Sources

1. [ngspice NEWS](https://ngspice.sourceforge.io/news.html)
2. [Xyce releases](https://github.com/Xyce/Xyce/releases)
3. [ngspice shared library](https://ngspice.sourceforge.io/shared.html)
4. [Xyce general coupling application note](https://xyce.sandia.gov/files/xyce/documentation/AppNote-GenExt.pdf)
5. [ngspice OSDI](https://ngspice.sourceforge.io/osdi.html)
6. [Xyce analyses and models](https://xyce.sandia.gov/about-xyce/)
7. [IHP model compilation](https://ihp-open-pdk-docs.readthedocs.io/en/latest/install/installation.html)
8. [Current Xyce source build guide](https://github.com/Xyce/Xyce/blob/master/INSTALL.md). The older [website build guide](https://xyce.sandia.gov/documentation-tutorials/building-guide/) differs; use documentation at the exact source revision.
9. [Xyce FAQ](https://xyce.sandia.gov/documentation-tutorials/frequently-asked-questions/)
10. [OpenVAF-Reloaded ABI notes](https://github.com/OpenVAF-Reloaded/OpenVAF)
11. [OpenVAF community fork license notes](https://github.com/OpenVAF/OpenVAF-Reloaded)

Local release evidence: ngspice47 `COPYING`, `src/include/ngspice/sharedspice.h`, `src/frontend/numparam/readme.txt`; Xyce snapshot `COPYING`, `INSTALL.md`, `src/CircuitPKG/N_CIR_Xyce.h` and `.C`. Source archive hashes and executed commands appear in S3.
