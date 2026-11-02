<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S1: FEM stack

Overall: **NOT PASS**. Serial local numerical subset passes; full-stack Linux/macOS CI is missing.

Built MFEM 4.8 from source with MPI/METIS disabled and LAPACK enabled. Archive SHA256: `65472f732d273832c64b2c39460649dd862df674222c71bfa82cf2da76705052`. Compile/configure recipe is in the workflow. Local AppleClang21 arm64 uses Accelerate LAPACK. This is a diagnostic implementation, not a production backend selection.

[Raw numerical output](../../verification/results/mfem-local.log): P1 triangle Poisson manufactured solution sin(pi x)sin(pi y), uniform n=8,16,32,64, observed L2 orders 1.973178360142166, 1.9931571751678783, 1.9982788165534278 against expected2 with tolerance0.15. Refined order3 H(curl) rectangular PEC cavity (1×0.8×0.6, four hexes per dimension):4356 free degrees,1331 gradient null modes matching discrete H1 interior dimension; first six positive eigenfrequencies maximum relative error4.9435656211072043e-5, below1e-3. This only checks the first six physical modes, not all spectral modes. Dense LAPACK does not test SLEPc or scalable preconditioning.

The order2 trial failed on mode6 at0.0027727428346264738. [Failure retained](../../verification/results/cavity-coarse-failure.log); increasing order, without changing tolerance, passed. Dense eigen runtime22.09s in this recorded run; not a scalability benchmark.

Conda dry resolution of MFEM+hypre+SuperLU_DIST+SLEPc succeeded on osx-arm64, but selected real PETSc/SLEPc. [Resolver output](../../verification/results/s1-conda-resolve.log) is not installation/build evidence and does not satisfy complex arithmetic. Next: explicitly resolve complex variants, lock, test complex linear solve and SLEPc cavity on both CI platforms; separately concretize Spack. No CI run exists yet.
