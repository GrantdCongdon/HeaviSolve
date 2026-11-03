<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-005: reject the convenient FEM binary environment

Status: accepted rejection; replacement source build under evaluation. Date: 2026-11-02.

The complex conda PETSc/SLEPc environment resolved and executed a cavity experiment, but its transitive package inventory includes ParMETIS (`LicenseRef-ParMETIS`). The [upstream license](https://github.com/KarypisLab/ParMETIS/blob/main/LICENSE) restricts permitted use and redistribution. This violates ADR-002, irrespective of PETSc's own BSD license. That environment is rejected for integration and redistribution. Its numerical output is retained only as an experiment and never establishes license admission or solver verification. No ParMETIS binary or source is committed or distributed.

The [full environment audit](../../verification/results/fem-conda-license-audit.log) also flags CeCILL-C packages, blank metadata, runtime exceptions and other expressions outside the exact allow-list. These are not silently accepted as equivalent. The direct inventory scan was insufficient to establish a complete dependency audit. `tools/audit_conda.py <prefix>` now scans every installed conda record, records version/build/hash and fails closed on unknown expressions. Metadata approval alone still requires bundled-file and actual linked-library review before release.

Replacement: build PETSc 3.26.1 (complex) and SLEPc 3.26.0 from upstream source, with SuperLU_DIST 9.2.1 configured without ParMETIS. Use a smaller OpenMPI/hypre/OpenBLAS/METIS environment. PETSc's license explicitly excludes downloaded third-party packages; each remains separately reviewed. [PETSc license](https://github.com/petsc/petsc/blob/v3.26.1/LICENSE), [SLEPc license](https://github.com/slepc/slepc/blob/v3.26.0/LICENSE.md), [SuperLU_DIST license](https://github.com/xiaoyeli/superlu_dist/blob/v9.2.1/License.txt).

The [smaller environment audit](../../verification/results/fem-clean-conda-license-audit.log) is also fail-closed: removing ParMETIS does not automatically approve compiler runtime exceptions or missing/alternative license expressions. The local build is a candidate, not a redistributable artifact. Source-built numerical dependencies avoid the rejected graph; release admission remains blocked until every transitive license is resolved.

MFEM 4.7 from the first conda attempt was incompatible with hypre 3.2 private-header changes. The MPI-stack experiment therefore moves to MFEM 4.10, while the already-recorded serial baseline remains 4.8. This version deviation is explicit; it does not rewrite the prior measurements. Linux/macOS hosted build evidence is still required by S1.
