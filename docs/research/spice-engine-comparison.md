<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# R6: SPICE engine comparison

Research date: 2026-11-02. Status: **incomplete experimental gate**. Documentation evidence is not a benchmark result. Neither engine is claimed verified or fully compatible.

## Primary-source findings

| Question | ngspice | Xyce |
|---|---|---|
| Version / maintenance evidence | Official NEWS lists 47, released 2026-08-11 [1]. Release 47 source downloaded for this spike. | GitHub release listing identifies 7.10 as latest [2]; current master source contains 7.11 build changes. Release7.10.0 was subsequently source-built; archive digest and patches are recorded in S3. |
| Method and language | C SPICE-family nonlinear circuit simulation. | C++ differential-algebraic circuit solver, serial/MPI. |
| License | Release 47 COPYING: primarily modified BSD (BSD-3-Clause), with MPL-2.0 OSDI, LGPL numparam, public-domain XSPICE and GPL-2.0-or-later table code. Do not inventory the whole distribution as BSD alone. | COPYING is GPLv3; `src/CircuitPKG/N_CIR_Xyce.C` explicitly permits v3 or later. GPL-3.0-or-later candidate under ADR-002. |
| Library API | Official shared-library documentation exposes simulation control, callbacks and data vectors [3]. Release header exports `ngSpice_Init_Sync`, external voltage/current callbacks, and synchronization callback. | `Circuit::Simulator::simulateUntil(requestedUntilTime, completedUntilTime)` is in the downloaded header. General-coupling application note documents time advancement and external device coupling [4]. Library co-simulation exists; suitability and rollback need experiments. |
| Analyses | Standard circuit analyses; OSDI documented since v39 [5]. No harmonic-balance compatibility claim is made. Periodic steady-state news is not proof of HB equivalence. | Official description lists DC, transient, AC, noise, HB and MPDE [6]. FFT dependency is required for HB. |
| SG13G2 Verilog-A route | IHP: OpenVAF compiles OSDI binaries. | IHP: ADMS compiles Xyce shared-library plugins [7]. This is distinct from OpenVAF/OSDI. |
| Build/platform | Shared-library release build attempted on macOS arm64. Linux not run in this session. | Release7.10.0 built on macOS with Trilinos16.1 and compatibility fixes. No Linux execution evidence. Current source guide requires C++17, Trilinos >=14.4 (versions beyond16.1 untested), SuiteSparse AMD/config and flex/bison; FFTW for HB [8]. |
| Interchange | Must emit engine-specific analysis/output syntax and model bindings. `.control` is not a portable IR construct. | SPICE3F5-like syntax with extensions is documented [9]; do not assume arbitrary ngspice netlists translate losslessly. |
| Strength | Small C embedding interface and explicit external-source callback. | HB and large-circuit parallelism; native library forward stepping demonstrated locally. |
| Limitation | Engine global state motivates separate workers; platform/compiler and model ABI must be tested. | Build weight; device/plugin compilation differs; external-device exchange and rollback untested. |

## Weighted evaluation

Scores below are **engineering judgments about demonstrated readiness**, not measured performance numbers. Scale:1=not experimentally established,2=narrow/limited evidence,3=working with material gaps,4=strong local evidence,5=criterion demonstrated in the scoped spike. In particular, scalability1 means untested, not that either engine scales poorly. Broad PDK coverage and Linux/Windows distribution remain unestablished. The numerical evidence comes from [S3](../spikes/S3-spice.md), including its failures.

| Criterion | Weight | ngspice | Xyce | Evidence and limitation |
|---|---:|---:|---:|---|
| Embeddability / co-simulation |5|4|3|ngspice C++ callbacks produced10041 calls; Xyce native library advances50 requested stops within1ps and passes RC oracle; external-device exchange/rollback remain untested |
| Analysis coverage |5|4|5|Both DC/AC/transient; Xyce native HB RLC/cubic passed; ngspice transient FFT passed; noise not tested |
| Open-PDK devices |5|2|2|IHP built-in HBT runs; no MOS/SKY130/GF180 coverage demonstrated |
| Accuracy / conformance |4|3|3|RC/RLC pass; HB/FFT pass; IHP AC disagreement and DC failures remain |
| Build / distribution burden |4|3|2|Both macOS source-built; ngspice patch small; Xyce needs Trilinos/Fortran/FFTW and compiler patches; Linux pending |
| Scalability |3|1|1|No matched large-netlist performance experiment; do not infer ranking |
| Dialect / ecosystem |3|4|4|One native research IR ran4circuits×3analyses; engine-specific model bindings required |
| License / maintenance |3|3|3|Release sources identified and compatible candidate licenses; transitive redistribution audit incomplete |
| Weighted sum /160 |32|98|94|Normalized61.25% versus58.75%; difference2.5percentage points |

The Xyce API score remains3: forward stepping is now demonstrated, but the broader external-device exchange part of this criterion remains untested. The score lead is below15points. Xyce's demonstrated native HB is also a uniquely required weight-5 capability. **Outcome B: retain both engines as first-class implementation targets.** This decision does not assert full compatibility: S3c currently fails, and the experimental acceptance gate remains open. The score is readiness under current evidence, not a comprehensive product-quality ranking. Revisit it when model conformance and platform evidence improve.

## Candidate integration rubric

Both are candidates, not approved solver integrations. License review is partially supported; APIs are documented. Benchmark pass, full maintenance pinning and lossless circuit/model mapping are not demonstrated. Do not replace them with a new SPICE solver: section4.7 explicitly forbids that. Keep candidate status until requirements pass.

## Dialect and validation contract

The future common IR must encode typed device instances, SI-valued parameters, connectivity, analysis requests and engine-specific model bindings. Emit `.tran`, `.ac`, `.dc` and output selection per engine; reject unsupported elements. Store exact emitted decks. Run RC, RLC, diode, HBT/MOS amplifier and pinned IHP cases against each engine's standalone execution. Record interpolation grid and units before cross-engine comparison. Initial tolerances: DC relative1e-4, AC1e-3, transient NRMSE1e-3; define absolute floors at zero crossings before running, and document any change. The scoped corpus now runs; S3 records passing cases and unresolved IHP AC/DC failures.

## OpenVAF caution

The original project and community forks must not be conflated. OpenVAF-Reloaded documents OSDI0.4 versus earlier0.3 and different binary names [10]. Pin compiler, emitted ABI and simulator together. Its repository warns that some integration-test model licenses differ from the compiler license [11]; do not redistribute that fixture tree indiscriminately. Pinned OpenVAF-Reloaded subsequently compiled the project cubic model, and libngspice loaded it successfully. See S3 for measurements. Cross-engine model conformance remains failed.

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
