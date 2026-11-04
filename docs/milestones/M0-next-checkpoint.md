<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Next checkpoint after completed M0

1. Preserve the explicit accept/reject/defer dispositions in [ADR008](../adr/ADR-008-phase-r-component-dispositions.md). This decision review is complete; ngspice remains unapproved for production until its selected dependency graph passes ADR002. Research measurements do not authorize adoption.
2. Preserve the completed Linux SPICE run41858845394 and its checksum-verified artifacts: builds, ngspice RC, Xyce forward stepping and HB pass. IHP/OSDI were excluded from that hosted subset. Avoid repeating this or the passing Linux/macOS complex-cavity build without changed inputs.
3. Preserve completed acceptance evidence: run41922593403 at239cb7f passes all6 jobs, including `ctest -L m0`3/3 on Linux and macOS. Verified numerical/language artifacts and full foundation logs are retained. Container41922593302 at the same revision passes3/3 foundation checks.
4. M0 is complete: user-approved PR1 merged at4025a1d after all final-head checks passed; the exit review now passes. Preserve the final report, one-page decisions and handoff. Stop before M1 implementation.

[ADR007](../adr/ADR-007-m0-acceptance-scope.md) corrects the previous requirement that every feasibility experiment pass before M0 acceptance. Original-model S3c still fails. Full supported-engine conformance remains mandatory at M7, and release audits remain mandatory before binary distribution. No model or tolerance changes are proposed to hide failures.

## Proposed M1 checkpoint — design only

The [walking-skeleton plan and self-review](../developer/walking-skeleton-plan.md) define a user-process → capacitor geometry/mesh → C++ statics worker → shared API → Qt/Python → result-plot path. Require VER-ES-01, process roundtrip, geometry/mesh checks, provenance, worker-crash isolation, API parity and screenshots. M1 exits with an externally supplied IHP stack visible in3D. The design is self-reviewed; M0 exit is now met; implementation has not started and is outside this completed session.

## Roadmap recommendations

Keep both SPICE engines as co-primary targets and carry the failed self-heated AC/avalanche DC comparisons into the M7 risk register. Investigate identically versioned compact-model sources via engine-specific compiler routes only after grant/compiler/thermal mapping review. Preserve original models and tolerances.

Prefer tested KLayout geometry round trips over the failing gdstk SiEPIC OAS route, and source-selected FEM packages over the rejected ParMETIS-bearing environment. Keep Spack/HPC and binary-release certification explicit future validation work. These choices preserve the hard requirements and do not authorize unreviewed dependencies.
