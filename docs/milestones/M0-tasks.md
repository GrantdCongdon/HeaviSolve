<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 task list — 2026-11-04

## Research and foundations

- [x] Read/recover the complete director plan; preserve the section3.2 repository skeleton.
- [x] R1/R3/R6 surveys with primary-source links and explicit unknowns.
- [x] ADR001 scored C++/Rust slab and narrow C-ABI binding comparison, with unmeasured effort/framework limits disclosed.
- [x] ADR002, AGPL license, SPDX/REUSE, DCO, direct inventory scan and fail-closed transitive policy.
- [x] ADR003 measured dual-engine scoring; retain both as co-primary targets.
- [x] S1–S7 reports including S3a–c, actual failures and alternatives.
- [x] Linux/macOS baseline and complex FEM CI with stored outputs.
- [x] Docker foundation image built and tested in CI41858845826; no image published.
- [x] Dependency strategy, Spack starter, docs skeleton and coding standards.
- [x] Name-availability check; retain HeaviSolve.
- [x] ADR007 separates acceptance, reported feasibility outcomes and final exit.
- [x] ADR008 records explicit Phase R component dispositions without admitting unreviewed dependencies.
- [ ] Finish current Linux SPICE attempt41858845394 and record its outcome; no platform pass inferred from a recipe.

## Acceptance and exit

- [x] Local revised `ctest -L m0`:3/3 pass (Poisson, cavity, evidence gate).
- [x] Local foundation checks:3/3 pass, including gate policy tests.
- [ ] Push/review the revised aggregate M0 label in hosted Linux/macOS CI and retain results.
- [x] Walking-skeleton design self-review, conditional on M0 exit.
- [ ] Final ADRs accepted and merged; remote main currently unchanged.
- [ ] Deliver final M0 report, decision summary and next-checkpoint plan. **M1 must not start before exit and reporting.**

## Retained limitations and later gates

- S3c **FAIL**: original self-heated IHP AC and strict DC disagree; full VER-SP conformance remains required at M7. Diagnostic model copies do not replace original acceptance data.
- S6 gdstk SiEPIC OAS geometry **FAIL**; prefer tested KLayout route subject to component admission.
- S5/S6 repaint throughput is measured; compositor frame rate is unmeasured.
- Historical language-development hours and full nanobind/PyO3 comparison remain explicitly limited.
- Full binary redistribution audit, release SBOM and installation certification remain required before shipping binaries; the Docker check does not supply them.
