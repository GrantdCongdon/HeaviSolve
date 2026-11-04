<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-001: Recommend C++20 after paired native slab experiments

Status: accepted research decision by ADR008; merged into main through approved PR1 (4025a1d); numerical and C ABI binding comparisons passed locally and on Linux/macOS CI; production binding-framework comparison remains open. Updated: 2026-11-03.

## Decision

Recommend C++20 for backend and GUI. Both native implementations reproduce the slab's fundamental TE/TM indices with second-order convergence. This experiment supplies no evidence of a numerical-performance advantage for either language. C++ offers the directly exercised FEM, meshing, SPICE, Qt and VTK ecosystem; Rust has not demonstrated the plan's required clear win on three weighted criteria. Do not introduce Rust into production solely because the research prototype works. This recommendation does not close the overall Phase R gate or authorize M1.

## Paired experiment and deviation from the requested library comparison

The [C++ implementation](../../verification/language/slab.cpp) and [Rust implementation](../../verification/language/slab.rs) each assemble the same lowest-order rectangular Nédélec transverse / bilinear Lagrange longitudinal mixed vector eigenproblem. There is no shared FEM assembly implementation. Both call the same LAPACK `dggev` routine in Apple's Accelerate framework; the Rust implementation therefore is not a pure-Rust numerical stack. This controls the algebra backend while comparing native assembly and FFI mechanics.

This is a deliberately narrow deviation from “best available libraries in each”: neither slab implementation uses a general FEM library. MFEM's mature H(curl) infrastructure is exercised separately in S1; a comparably complete Rust library integration was not demonstrated. The experiment establishes feasibility and correctness for these implementations, not relative ecosystem completeness or general solver quality. A library-backed Rust-versus-MFEM benchmark remains unperformed. These prototypes are research code, not the M2 mode solver.

The dimensionless geometry uses core width 1, core/cladding permittivity 2.25/1, vacuum wavenumber 2π, and cladding extent 4 on each side. The transverse y direction is periodic, width 0.2 with two elements. Distant x walls use PEC truncation. Refinement doubles the 16 core cells and 12 graded cells per cladding side; the resulting mixed systems have 236, 476, 956 and 1916 degrees of freedom. Two-point tensor quadrature integrates the element forms. The singular generalized pencil includes longitudinal variables; finite real indices between 1 and 1.5 are sorted, and the first two are compared with TE0/TM0. Six guided indices are found at every refinement. This is not a proof that the entire spectrum is free of spurious modes.

The independent [closed-form oracle](../../verification/oracles/slab.py) bisects the symmetric-slab TE/TM dispersion relations for 80 iterations. Python only evaluates the test oracle and orchestrates native executables; FEM assembly and eigensolution are native. Oracle indices are TE0 = 1.44911671483852 and TM0 = 1.4339748985055536.

## Measured local results

[Unedited run output](../../verification/results/language-comparison.csv) and [calculated evidence audit](../../verification/results/language-evidence-audit.log) retain full precision, convergence rates and source hashes. Host: macOS arm64, AppleClang 21.0.0, Rust 1.99.1. Timing runs overlapped other build activity and were not repeated as a controlled performance study.

| Quantity at refinement 8 | C++ | Rust |
|---|---:|---:|
| TE0 index | 1.4491101425508708 | 1.44911014255077708 |
| TE0 absolute error | 6.572287649220243e-6 | 6.572287742923066e-6 |
| TM0 index | 1.43397655139923 | 1.43397655139922375 |
| TM0 absolute error | 1.652893676373779e-6 | 1.65289367015653e-6 |
| Assembly seconds | 0.032167083 | 0.0067285 |
| Eigensolve seconds | 20.019778209 | 20.841110917 |
| Physical source lines, including headers | 80 | 66 |

Every measured refinement transition has error order between 1.9859 and 1.9994, inside the harness's 1.8–2.2 interval. The maximum cross-language index difference is 9.370282327836321e-14, below 1e-10. Both final index errors are below the spike's 1e-4 threshold. **Local paired numerical check: PASS.** This threshold does not meet or replace M2's eventual 1e-6 acceptance target. The later hosted runs cited below passed and retained this scoped slab/binding evidence; this does not verify a production mode solver.

Line counts are literal physical lines, not normalized complexity: both files use compressed formatting. Peak memory was not measured. A timestamp records the start of the language work, but interruptions and concurrent work prevent a reliable engineering-time comparison; development hours are **not measured**, and the 1–2 week budget is not an observed duration. A later equivalent C ABI/ctypes binding experiment is recorded below; nanobind/PyO3 and zero-copy NumPy behavior remain **not measured**. Rust required an isolated toolchain installation and an explicit unsafe C ABI declaration; no external Rust FEM crate was used. The numerical comparison is complete locally, while those requested comparison dimensions remain limitations of R2.

## Weighted assessment

Scores are engineering judgments informed by the cited ecosystem and local experiments, not quantities inferred from the timing table. A score of 1 is least suitable and 5 most suitable for this project's roadmap.

| Criterion | Weight | C++ | Rust | Evidence and limits |
|---|---:|---:|---:|---|
| H(curl)/high-order FEM | 5 | 5 | 2 | MFEM ND spaces exercised in S1; both slab prototypes work, but neither establishes a mature Rust general FEM stack |
| Sparse algebra/eigensolvers | 5 | 5 | 2 | MFEM/PETSc/SLEPc native interfaces exercised in S1; both slab prototypes use dense LAPACK, so no sparse performance comparison |
| SPICE interop | 4 | 5 | 3 | libngspice callbacks and OSDI exercised from C++; Rust foreign calls possible but SPICE adapter untested |
| GUI/3D | 4 | 5 | 3 | Qt/VTK C++ shell exercised in S5; no equivalent Rust GUI spike |
| CAD/meshing | 3 | 5 | 3 | Gmsh C++ API and native extrusion exercised in S4; Rust wrappers untested |
| Python bindings | 3 | 4 | 4 | Equivalent C ABI/ctypes wrappers pass locally; nanobind/PyO3 ergonomics and zero-copy NumPy remain untested, so equal score retained |
| Safety/tooling | 3 | 3 | 5 | Rust checked ownership and bounds in assembly; unsafe LAPACK ABI remains; C++ needs RAII, sanitizers and review |
| Maintainability | 2 | 4 | 3 | C++ aligns with selected native dependencies; contributor recruitment and maintenance effort not measured |
| **Weighted sum (maximum 145)** | **29** | **134** | **86** | **Subjective suitability, not a measured performance score** |

Rust wins one criterion, not the three required by the plan. The binding tie and ecosystem judgments should be revisited if a concrete component presents a measurable Rust advantage. Do not generalize this small prototype into a claim that Rust cannot support FEM.

## Reproduction and remaining checks

From the repository root on the measured macOS host:

```sh
mkdir -p .work/language
clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror verification/language/slab.cpp -framework Accelerate -o .work/language/slab-cpp
rustc --edition=2024 -C opt-level=2 -D warnings verification/language/slab.rs -o .work/language/slab-rust
python3 verification/language/compare.py > .work/language/comparison.csv
```

For the isolated toolchain used here, set `RUSTUP_HOME` to `.work/language/rustup` and `CARGO_HOME` to `.work/language/cargo` using absolute paths, then use that cargo directory's `bin/rustc`. The initial source targeted Accelerate; the later portable CMake configuration and Linux LAPACK path passed the hosted runs cited below. The later repeatable C ABI binding smoke test supplies narrow binding evidence; full framework comparison and historical effort accounting remain limitations of the requested R2 comparison.

Primary sources underlying the ecosystem assessment: [MFEM examples](https://mfem.org/examples/), [Fenris README](https://github.com/InteractiveComputerGraphics/fenris/blob/master/README.md), [Fenris element definitions](https://github.com/InteractiveComputerGraphics/fenris/blob/master/src/element.rs), [nanobind](https://nanobind.readthedocs.io/en/latest/), [PyO3](https://pyo3.rs/), [Qt](https://doc.qt.io/qt-6/), [Gmsh API](https://gmsh.info/doc/texinfo/). Fenris' dated status paragraph is not a current maintenance timestamp. This update records local experiment evidence; it does not claim a new upstream maintenance audit.

Portability follow-up: the Rust LAPACK declaration now selects Accelerate only on macOS and `lapack` elsewhere using conditional link attributes. The stored audit hash describes the original macOS-only source used for the recorded numerical run. The subsequent Linux CI run cited below exercises this path; the source change alone was not evidence of a pass.

The portable CMake project was subsequently built and the full comparison repeated locally on macOS: [repeat output](../../verification/results/language-portable-comparison.csv). Numerical tolerances pass again. Linux/macOS workflow run41668976621 now passes and stores the comparison output. Different timings across these runs reinforce that no controlled language-speed comparison is claimed.


## Equivalent Python-callable C ABI binding experiment — 2026-11-03

[Native C++ wrapper](../../verification/language/binding.cpp), [native Rust wrapper](../../verification/language/binding.rs), [orchestration harness](../../verification/language/check_bindings.py), and [raw measured output](../../verification/results/language-bindings.json).

Both shared libraries expose the same synchronous `hs_slab(refinement, output, capacity, count)` C ABI and reuse the existing native slab implementation. Python `ctypes` allocates output storage and calls native assembly/eigensolution. The wrappers return explicit invalid-argument, insufficient-capacity and numerical-failure statuses. C++ catches exceptions (LAPACK failures now throw instead of exiting the interpreter); Rust catches unwinding panics. Invalid non-null pointers are still a caller contract, and fatal signals/allocator aborts are not caught. Fault injection, thread safety and cancellation were not tested.

Both bindings pass at refinement4 against the independent TE/TM roots: errors approximately2.62767e-5 and6.60865e-6, below1e-4. All six returned indices agree between languages within1e-10. Tests also pass for invalid refinement, null pointers, insufficient capacity with unchanged output, and persistence of one caller-owned result while a subsequent call fills a different buffer. An aliased ctypes host view has the same address as its backing buffer. **This is not end-to-end zero-copy:** native vectors are copied into caller-owned output; no NumPy zero-copy claim is made.

| Measured quantity | C++ | Rust |
|---|---:|---:|
| Wrapper physical lines, including headers |22|30|
| Shared-library compilation seconds |0.9333750419900753|1.208748333971016|
| Refinement4 native call including ctypes dispatch, seconds |1.2708804590511136|1.2379625409957953|

The shared Python build/test harness has82 physical lines. First timestamped inspection was2026-11-03T15:24:00Z; successful result capture was15:25:20.261941Z, an80.261941-second wall-clock interval for this joint agent-driven experiment. This is not human engineering time, not a per-language effort comparison, and does not reconstruct the earlier solver-development hours. Compile/call times are one sample each and do not isolate binding overhead or establish a speed winner. No dependency beyond the existing toolchains, LAPACK and Python standard library was added.

Reproduce on the measured host with the isolated Rust environment described above:

```sh
python3 verification/language/check_bindings.py --build .work/language-bindings --rustc "$CARGO_HOME/bin/rustc"
```

The Linux `-shared`/LAPACK path now passes in hosted CI, alongside the macOS path. C ABI feasibility supplies evidence of callable native solvers and explicit buffer ownership; it is a documented narrow substitute for a full nanobind-versus-PyO3 framework comparison, not completion of that comparison. Weighted scores remain unchanged; full M0 and production framework gates remain open.

Hosted evidence: [run41668976621](https://github.com/GrantdCongdon/HeaviSolve/actions/runs/41668976621), commit47b8352; [artifact hashes and retained outputs](../../verification/results/ci-41668976621/provenance.json). Both paired-language jobs passed the slab and binding checks.
