<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-001: C++20 remains the provisional default

Status: proposed; R2 experimental gate NOT MET. Date: 2026-11-02.

The requested mixed Nédélec/Lagrange dielectric-slab implementation in both languages has not been completed. The 1–2 week ceiling is not evidence that such a comparison was performed. Local environment inspection found AppleClang 21 and no cargo/rustc. No Rust speed, line-count or development-effort claim is made. The C++ Poisson/cavity diagnostics are different problems and cannot substitute for VER-WG-01.

## Evidence-based preliminary scores (expert judgments, not measured performance)

| Criterion | Weight | C++ | Rust | Evidence / limitation |
|---|---:|---:|---:|---|
| H(curl)/high order | 5 | 5 | 2 | MFEM ND spaces exercised locally; Fenris element listing is Lagrange-focused; broader Rust search incomplete |
| Sparse algebra/eigensolvers | 5 | 5 | 2 | MFEM native solver ecosystem; Fenris explicitly delegates solving and excludes distributed/GPU scope |
| SPICE interop | 4 | 5 | 3 | C API exercised from C++; Rust C FFI possible but untested |
| GUI/3D | 4 | 5 | 3 | Qt/VTK C++ APIs documented; neither GUI spike completed |
| CAD/meshing | 3 | 5 | 3 | Gmsh C++ API tested; Rust foreign wrappers possible, untested |
| Python bindings | 3 | 4 | 4 | nanobind/PyO3 candidates, binding spike pending; tied placeholder judgment, not benchmark |
| Safety/tooling | 3 | 3 | 5 | Rust ownership advantages; C++ requires sanitizers/RAII; toolchain comparison pending |
| Maintainability | 2 | 4 | 3 | One native ecosystem fits project dependencies; contributor survey absent |

Weights total 29. These subjective ordinal judgments favor C++, but are not the measured R2 scoring required for M0 and must not be used to claim a completed head-to-head trial. Rust does not demonstrate the required clear win on three weighted criteria; nevertheless absence of an implementation is not proof of impossibility.

## Decision and closure

Keep C++20 as the provisional research language and avoid introducing a second production toolchain. Do not lock architecture until the paired slab spike or a director-approved scoped alternative is complete. A Rust prototype may use a narrow C ABI to MFEM, but distinguish that from a pure-Rust FEM implementation and measure binding cost separately. Compare the same mesh, mixed spaces, boundary truncation, solver tolerance and analytic slab roots. Record wall time, memory, source lines (excluding generated/vendor code), actual effort log and bindings. Do not invent elapsed development time retrospectively.

Primary sources: [MFEM examples](https://mfem.org/examples/), [Fenris README](https://github.com/InteractiveComputerGraphics/fenris/blob/master/README.md), [Fenris element definitions](https://github.com/InteractiveComputerGraphics/fenris/blob/master/src/element.rs), [nanobind](https://nanobind.readthedocs.io/en/latest/), [PyO3](https://pyo3.rs/), [Qt](https://doc.qt.io/qt-6/), [Gmsh API](https://gmsh.info/doc/texinfo/). Fenris' old status paragraph is still present; do not mislabel its 2021 paragraph as a current maintenance timestamp.
