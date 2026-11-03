<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S1: FEM stack

Overall: **NOT PASS**. Serial local numerical subset passes; full-stack Linux/macOS CI is missing.

Built MFEM 4.8 from source with MPI/METIS disabled and LAPACK enabled. Archive SHA256: `65472f732d273832c64b2c39460649dd862df674222c71bfa82cf2da76705052`. Compile/configure recipe is in the workflow. Local AppleClang21 arm64 uses Accelerate LAPACK. This is a diagnostic implementation, not a production backend selection.

[Raw numerical output](../../verification/results/mfem-local.log): P1 triangle Poisson manufactured solution sin(pi x)sin(pi y), uniform n=8,16,32,64, observed L2 orders 1.973178360142166, 1.9931571751678783, 1.9982788165534278 against expected2 with tolerance0.15. Refined order3 H(curl) rectangular PEC cavity (1×0.8×0.6, four hexes per dimension):4356 free degrees,1331 gradient null modes matching discrete H1 interior dimension; first six positive eigenfrequencies maximum relative error4.9435656211072043e-5, below1e-3. This only checks the first six physical modes, not all spectral modes. Dense LAPACK does not test SLEPc or scalable preconditioning.

The order2 trial failed on mode6 at0.0027727428346264738. [Failure retained](../../verification/results/cavity-coarse-failure.log); increasing order, without changing tolerance, passed. Dense eigen runtime22.09s in this recorded run; not a scalability benchmark.

Conda dry resolution of MFEM+hypre+SuperLU_DIST+SLEPc succeeded on osx-arm64, but selected real PETSc/SLEPc. [Resolver output](../../verification/results/s1-conda-resolve.log) is not installation/build evidence and does not satisfy complex arithmetic. Next: explicitly resolve complex variants, lock, test complex linear solve and SLEPc cavity on both CI platforms; separately concretize Spack. No CI run exists yet.

## Complex source-stack follow-up (2026-11-03)

The convenient complex conda environment was built and produced a cavity result, but is **rejected** because it includes restricted ParMETIS; see [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md). Do not mistake numerical success for dependency admission.

A replacement stack now builds locally: MFEM4.10, hypre3.2, complex PETSc3.26.1, SLEPc3.26.0 and SuperLU_DIST9.2.1 with ParMETIS disabled. [Archive hashes](../../verification/results/native-archive-hashes.json), [PETSc configure](../../verification/results/petsc-clean-configure.log), [SLEPc configure](../../verification/results/slepc-clean-configure.log). This moves MFEM to4.10 because the earlier4.7 binary package could not compile against hypre3.2 headers.

The same4356-free-DOF cavity now passes with complex PETSc matrices and SuperLU_DIST shift-invert SLEPc: maximum first-six frequency relative error **4.9435655966822978e-5**, tolerance1e-3. [Raw output](../../verification/results/fem-clean-cavity.log). It ran one MPI rank;12 eigenpairs converged, and the first six physical modes were compared. A local TCP-bind warning is retained; the single-rank calculation completed. This is neither multi-rank scaling nor a complex-material benchmark.

The replacement still has unreviewed runtime-license expressions in its conda support environment. Therefore the local numerical subtest passes, but S1's complete license-approved, reproducible Linux/macOS CI gate remains **NOT PASS**. The checked-in CMake project requires pkg-config; this host lacked it, so the final local executable was compiled with explicit include/library paths. Exact resumption paths and build flags are recorded in the [running handoff](../milestones/M0-handoff.md).
