<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Next checkpoint: complete M0 and report before M1

1. Preserve the explicit accept/reject/defer dispositions in [ADR008](../adr/ADR-008-phase-r-component-dispositions.md). This decision review is complete; ngspice remains unapproved for production until its selected dependency graph passes ADR002. Research measurements do not authorize adoption.
2. Finish Linux SPICE run41858845394, retaining output and any failure. Its previous attempt built Trilinos but lacked Flex headers for Xyce; the workflow now includes them. Avoid repeating the already passing Linux/macOS complex-cavity build without changed inputs.
3. Validate the revised `ctest -L m0` command on the authorized review branch and retain results. Locally it passes3/3; foundation checks pass3/3. Docker CI41858845826 also passes its two foundation tests at that recorded revision.
4. Review and integrate final ADRs, then confirm the separate deliverable/exit checks. Remote main remains unchanged under the current review-branch authorization. Present the final report, one-page decisions and proposed next checkpoint before starting M1.

[ADR007](../adr/ADR-007-m0-acceptance-scope.md) corrects the previous requirement that every feasibility experiment pass before M0 acceptance. Original-model S3c still fails. Full supported-engine conformance remains mandatory at M7, and release audits remain mandatory before binary distribution. No model or tolerance changes are proposed to hide failures.

## Proposed M1 checkpoint — design only

The [walking-skeleton plan and self-review](../developer/walking-skeleton-plan.md) define a user-process → capacitor geometry/mesh → C++ statics worker → shared API → Qt/Python → result-plot path. Require VER-ES-01, process roundtrip, geometry/mesh checks, provenance, worker-crash isolation, API parity and screenshots. M1 exits with an externally supplied IHP stack visible in3D. The design is self-reviewed; implementation remains blocked on M0 exit and reporting.

## Roadmap recommendations

Keep both SPICE engines as co-primary targets and carry the failed self-heated AC/avalanche DC comparisons into the M7 risk register. Investigate identically versioned compact-model sources via engine-specific compiler routes only after grant/compiler/thermal mapping review. Preserve original models and tolerances.

Prefer tested KLayout geometry round trips over the failing gdstk SiEPIC OAS route, and source-selected FEM packages over the rejected ParMETIS-bearing environment. Keep Spack/HPC and binary-release certification explicit future validation work. These choices preserve the hard requirements and do not authorize unreviewed dependencies.
