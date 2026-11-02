<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Next checkpoint: close M0 before M1

1. Finish the paired first-order Nédélec/Lagrange slab spike with independent TE/TM roots and equal meshes/tolerances. Log actual effort, memory, runtime, line counts and binding work. Broaden Rust library evidence before final scoring.
2. Resolve and lock complex PETSc/SLEPc, MFEM/hypre and a complex direct solver for both target platforms. Run the cavity/convergence suite on hosted runners and retain outputs. The serial dense diagnostic is useful but not a substitute.
3. Build a pinned Xyce/Trilinos stack; run RC, IHP and VER-SP-05. Compile/load a license-cleared OSDI model in ngspice. Implement the shared circuit corpus and record per-engine differences before filling ADR-003 scores.
4. Finish custom layer extrusion/MFEM mapping, actual PDK layout fixtures, Qt6/VTK visible rendering and both IPC control-channel prototypes. Do not promote partial subtests to completed spikes.
5. Close survey maintenance/license unknowns; audit transitive dependencies, generate platform locks and release SBOM pipeline. Test Spack/Docker recipes and pin CI actions to audited commits.
6. Run `ctest -L m0`, license/doc/DCO checks and the self-review. Accept/merge final ADRs only with linked evidence.

Roadmap recommendation: keep an explicit M0 closure checkpoint. Do not fold missing experimental work into M1 while claiming foundations complete. No hard requirement is relaxed.

## Proposed M1 walking skeleton (blocked on M0)

User-defined process → simple capacitor geometry/mesh → C++ statics job in worker → shared versioned API → minimal Qt shell and Python binding → result plot. Both frontends call the same service. Require VER-ES-01, process roundtrip, deterministic provenance, server-crash isolation and screenshot/API parity tests.

## Self-review

- [x] Scope respects no Python solvers, PDK independence, shared API and worker isolation.
- [x] Benchmark and licensing claims distinguish passed, failed and missing evidence.
- [ ] Architecture decisions supported by complete Phase R experiments.
- [ ] Linux/macOS CI artifacts reviewed.
- [ ] M0 acceptance green and final ADRs merged.

Result: walking-skeleton design outline reviewed, but approval to start dependent M1 work is withheld by the plan's gate.
