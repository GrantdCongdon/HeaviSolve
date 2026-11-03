<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Next checkpoint: M0 closure, before M1

1. Resolve IHP cross-engine DC/AC differences from the pinned engine-specific compact models. Keep original data intact; identify parameter/default/model-form differences and validate any normalization separately. Do not loosen tolerances simply to pass. Retain dual-engine support and capability diagnostics.
2. Finish source-built complex FEM evidence without ParMETIS. Review every remaining transitive license expression and linked library, then lock the approved Linux/macOS environments. Test the HPC/container recipes rather than treating templates as proven builds.
3. Run the configured hosted Linux/macOS jobs and retain numerical/license artifacts against the exact reviewed commit. The user-approved m0-evidence branch now has passing baseline Linux/macOS CI (run41668976621). Finish the separate complex-stack recipe and retain its numerical outputs/license decisions; remote main remains unchanged.
4. Close the language spike's missing binding-effort measurements and outstanding survey evidence. Recorded engineering hours cannot be reconstructed honestly; retain that limitation in ADR-001.
5. Run the complete M0 acceptance label, review the dependency/component gates, accept final ADRs and complete the self-review below. Report that checkpoint to the director before any M1 implementation.

Roadmap recommendation: retain a separate M0 closure checkpoint. Promote KLayout for PDK round trips because the tested gdstk SiEPIC OAS route changes geometry. Prefer source-selected FEM dependencies over the rejected broad binary environment. Keep ngspice and Xyce capability-specific until conformance is resolved. No hard requirement is relaxed.

## Proposed M1 walking skeleton — blocked

User-defined process → simple capacitor geometry/mesh → C++ statics worker → shared versioned API → minimal Qt shell and Python binding → result plot. Both frontends use the same service. Require VER-ES-01, process roundtrip, deterministic provenance, server-crash isolation, screenshot and API-parity tests. Research spike code must be reviewed before any production reuse.

## Self-review

- [x] No Python solver implementation; process independence, shared API and isolated workers preserved.
- [x] Measured passes, failures, unmeasured quantities and license rejections remain explicit.
- [x] No restricted PDK data bundled; pinned public fixtures downloaded externally.
- [ ] Full Phase R component admission and complete acceptance evidence.
- [ ] Linux/macOS CI artifacts reviewed; license job green remotely.
- [ ] M0 acceptance green and final ADRs accepted/merged.

The design outline is reviewed; approval to begin M1 is withheld by the unmet M0 gate.
