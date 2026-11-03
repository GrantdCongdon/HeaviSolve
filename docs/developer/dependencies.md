<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors
SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Dependency strategy

Developers: conda-forge/Pixi isolated environments, with platform-specific lockfiles before claims of reproducibility. HPC: Spack concretization plus compiler/MPI hashes. CI/container: pinned source archives with checksums, retained configure/build logs and outputs. Never mutate an existing user environment.

M0 uses pinned MFEM 4.8 serial + LAPACK for a local diagnostic subset. This does not establish the required MFEM+hypre+complex direct solver+SLEPc stack or Linux/macOS portability. Complete that stack and audit its transitive licenses before adoption. No lockfile is invented for an environment that has not resolved.

MkDocs (BSD-2-Clause) is the lightweight documentation skeleton; C++ API extraction/Doxygen can follow once APIs exist. CI tools are development-only and need pinned versions and license review too. Docker recipe is a build starting point, not a published or tested image.

Build the site with `python tools/build_docs.py`; it stages raw verification evidence alongside the pages before strict MkDocs validation.

The later S1 candidate builds MFEM 4.10 with hypre 3.2 and source-built complex PETSc 3.26.1 / SLEPc 3.26.0 / SuperLU_DIST 9.2.1. The convenient prebuilt PETSc environment is **rejected** because it pulls restricted ParMETIS: see [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md). Do not use that environment as a distribution recipe. Every candidate conda prefix must also run `python tools/audit_conda.py <prefix>`; unknown expressions fail closed. This additional check does not replace review of bundled source licenses or binary linkage.

The language experiment now has its own portable CMake project and a Linux/macOS artifact-producing workflow. Its recorded local repeat passes; hosted execution remains pending. Research-only GUI, IPC and complex-cavity experiments have separate CMake projects under `verification/`; none commits production application architecture before Phase R acceptance.
