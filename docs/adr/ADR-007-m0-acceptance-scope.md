<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-007: align M0 acceptance with the director's milestone boundaries

Status: accepted correction; M0 exit complete through approved PR1 (4025a1d). Date: 2026-11-04.

## Evidence and problem

The director's version1.0 plan, section12, defines M0 acceptance as MFEM Poisson convergence, the PEC cavity within1e-3, scored C++/Rust investigation, ADR003 scoring supported by S3a–c measurements, and a green skeleton license scan. Its deliverables include **spike reports**, and its exit criteria are **ADRs merged** and **walking-skeleton plan approved by self-review**. Section2 time-boxes feasibility spikes. The user's assignment explicitly requires reporting failed spikes, what was tried, and alternatives.

Our implementation incorrectly combined those requirements with passing every feasibility experiment, full SPICE compatibility, and final binary-distribution certification. Section12 assigns the supported-engine VER-SP-01…06 suite and IHP curves to **M7**, and the complete release audit/SBOM/installers to **M10**. That accidental expansion caused the local M0 acceptance command to fail despite passing the specified numerical and research-evidence checks.

The original Downloads file became unavailable. Its recorded initial reads were recovered from this same chat: the original cat output supplies the beginning/end, and overlapping sed190–460 and460–730 outputs restore the middle without persistence truncation. The reconstructed851-line plan agrees with an independently retained first225-line copy. The private working copy is `.work/director-plan-recovered.md`; it is not bundled as a newly authored project document.

## Decision

Separate three assessments:

1. **M0 acceptance:** run the specified numerical tests and check the research/report/license evidence. Require the deliverables to exist and cite their measured outcomes, including failures.
2. **Feasibility results:** retain each spike's actual PASS/FAIL/partial result. A report being complete never converts its failed experiment into a pass.
3. **M0 exit:** check decision integration and the walking-skeleton design self-review separately. Passing acceptance alone never announces milestone completion or starts M1.

Replace the ambiguous `all_feasibility_spikes` boolean with an explicit report-completeness requirement. Preserve S3c's failing original-model results and the stricter full-stack S1 evidence already obtained. Complete the Docker image build/check and finish the documented Linux SPICE attempt. Do not claim a tested platform from a recipe alone.

## Preserved obligations and risks

No numerical threshold, foundry model, hard architectural requirement, licensing allowlist, or solver verification rule changes. Both SPICE engines remain co-primary targets under ADR003. Their production integration still requires VER-SP-01…06 and capability diagnostics; the current implementations are research harnesses. Self-heated IHP AC and residual avalanche-related DC differences remain unresolved M7 blockers, with an identically versioned compact-model route proposed for investigation.

Every dependency proposed for actual adoption still needs ADR002 admission before merge. A candidate survey or a research-build pass does not admit its full source/runtime graph. Binary redistribution and a release SBOM remain mandatory before shipping binaries. The foundation container is built for testing; no binary image is published by that check.

This corrects our implementation's milestone interpretation rather than weakening the director's stated acceptance tests. Earlier reports that called original-model SPICE compatibility an unconditional M0 exit blocker are superseded on scope only; their measurements remain valid.
