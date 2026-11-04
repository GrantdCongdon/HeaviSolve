<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-003: retain two SPICE candidates; use engine-specific Verilog-A routes

Status: **M0 engine direction recorded; production integration withheld**. Updated: 2026-11-04. Scope clarified by ADR007.

## Context and evidence

R6 requires measured scoring from S3a–c. The [comparison](../research/spice-engine-comparison.md) records scoped readiness scores and their evidence:98/160 ngspice versus94/160 Xyce, a2.5percentage-point difference. Untested scalability is scored as insufficient evidence, not a performance ranking. [S3](../spikes/S3-spice.md) records executable attempts. There is no15-point lead; full dual-engine compatibility has not been demonstrated.

ngspice exposes shared-library external-source callbacks. Xyce documents `simulateUntil` and general device coupling; it is not limited to subprocess operation. Xyce offers HB, while ngspice's documented OSDI path is useful for SG13G2. Native Xyce HB and ngspice transient/FFT now pass the RLC/cubic local checks. These complementary capabilities establish Outcome B as the implementation target.

## Decision

Retain ngspice and Xyce as **co-primary integration targets under Outcome B**, behind one future `SpiceEngine` contract with explicit capability flags, model bindings and per-engine emitters. Do not claim working support until tests pass. No primary winner is selected. The shared native IR exposes IHP AC disagreements of8–10% and residual DC disagreement. These are failed feasibility findings and M7 integration blockers, not a replacement for section12 M0 acceptance. Maintain the tolerances and investigate model/linearization differences; do not silently alter foundry models.

Use separate worker processes for isolation. Embedding can occur inside a worker; a library API does not require sharing the GUI process. Preserve a shared API for Python and GUI.

## Explicit deviations from the plan

The statement “Verilog-A via OSDI either way” is not supported by IHP's official installation instructions. Those specify **OpenVAF→OSDI for ngspice and ADMS→Xyce shared plugin for Xyce**. Adopt these per-engine build routes, subject to pinned-source license review and executable validation. A future Xyce OSDI implementation would require separate evidence and must not be presumed.

The current Xyce source guide supersedes the older website build recipe: it describes CMake-only starting7.11, C++17, and newer Trilinos requirements. Record exact release/source revision rather than mixing guides. An exploratory master configure does not establish a reproducible version pin.

## Integration rubric

| Gate | ngspice | Xyce |
|---|---|---|
| License-compatible selected build | Candidate; mixed-license audit required | GPL-3.0-or-later source; transitive audit required |
| Embeddable API | Documented C API | Documented C++ API |
| Maintained within ~12months | Release47 date supports this | Release7.10.0 archive pinned; see S3 |
| Required benchmarks pass | No | No |
| Lossless data-model mapping | Not demonstrated | Not demonstrated |

Integration is therefore **not approved as complete**. The explicit requirement to wrap existing SPICE engines remains in force; incomplete evidence is not a reason to write a replacement SPICE engine.

## Consequences and closure

Complete Linux/macOS CI and resolve the measured IHP conformance failures. Both adapters, diagnostics, conformance suite and capability matrix remain equal requirements. ADR007 separates the completed M0 measured-scoring deliverable from M7 compatibility requirements. The selected engine direction is recorded; production integration approval is withheld.

## Diagnostic refinement — 2026-11-03

[S3 follow-up](../spikes/S3-spice.md) now demonstrates Xyce forward stepping through its separate C-interface library. Default self-heated ngspice AC still disagrees with independent DC slopes. The residual isothermal DC failure is localized to the avalanche contribution: disabling it in both marked diagnostic copies reduces relative base-current disagreement from1.0304e-4 to4.3177e-9. The engines implement different avalanche smoothing formulas. No threshold or original model changed.

Consequently, a shared dialect alone is insufficient to promise cross-engine model equivalence. Any eventual `SpiceEngine` model binding must record the compact-model implementation/version and tested capabilities. The next candidate experiment uses an identically versioned model through the separate supported compiler routes, subject to source-grant review and thermal tests. This is an investigation direction, not approval of a replacement or a passed conformance gate. The co-primary decision remains unchanged. M0 exit still requires its decision review and integration; see ADR007.
