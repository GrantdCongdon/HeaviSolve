<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors
SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Dependency strategy

Developers: conda-forge/Pixi isolated environments, with platform-specific lockfiles before claims of reproducibility. HPC: Spack concretization plus compiler/MPI hashes. CI/container: pinned source archives with checksums, retained configure/build logs and outputs. Never mutate an existing user environment.

The baseline uses pinned MFEM4.8 serial + LAPACK and passes the Poisson/cavity subset in Linux/macOS CI. Complex-stack evidence is separate: macOS run41670183802 passed; the corrected Linux build is tracked in the M0 handoff. No lockfile is invented for an environment that has not resolved.

MkDocs (BSD-2-Clause) is the lightweight documentation skeleton; C++ API extraction/Doxygen can follow once APIs exist. CI tools are development-only and need pinned versions and license review too. Docker recipe is a build starting point, not a published or tested image.

Build the site with `python tools/build_docs.py`; it stages raw verification evidence alongside the pages before strict MkDocs validation.

The later S1 candidate builds MFEM 4.10 with hypre 3.2 and source-built complex PETSc 3.26.1 / SLEPc 3.26.0 / SuperLU_DIST 9.2.1. The convenient prebuilt PETSc environment is **rejected** because it pulls restricted ParMETIS: see [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md). Do not use that environment as a distribution recipe. Every candidate conda prefix must also run `python tools/audit_conda.py <prefix>`; unknown expressions fail closed. This additional check does not replace review of bundled source licenses or binary linkage.

The language experiment now has its own portable CMake project and a Linux/macOS artifact-producing workflow. Its independent native C++/Rust slabs and ctypes bindings pass on both hosted platforms, with retained artifact provenance under verification/results/ci-41668976621. Research-only GUI, IPC and complex-cavity experiments have separate CMake projects under `verification/`; none commits production application architecture before Phase R acceptance.

The complex build entry point is `python tools/build_complex_stack.py --prefix <isolated-conda-prefix> --work <space-free-work-directory> --jobs 2`. Source archives are SHA256-pinned. The workflow records the resolved package URLs, complete package metadata, source configure logs and numerical output. ADR006 admits exact platform/version/build/SHA256 identities for mixed runtime-license expressions; any changed unreviewed identity fails the audit. These records reproduce the tested environment but are not yet a polished installer or a binary redistribution approval. Spack and Docker remain untested starter recipes and must not be presented as the approved complex-stack configuration.
