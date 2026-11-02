<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S4: meshing feasibility

Overall: **PARTIAL / NOT PASS**. Gmsh ring/Netgen optimization quality subtest passes; custom layer extrusion and MFEM import are untested.

Native C++ Gmsh4.15.2 creates a radius10/9 annulus, extrudes0.5 (dimensionless test units), then tetrahedralizes at size0.35–0.5. Gate declared in source: positive minimum Jacobian and minSICN>0.05. Initial mesh:2617 elements,minSICN0.020583581134155957 — FAIL. The same geometry with `mesh::optimize("Netgen")`:4324 elements,minSICN0.42782904872064897,minJacobian0.0082792378589275177 — PASS. Both outputs retained. This exercises Netgen optimization through Gmsh, not an independent Netgen adapter.

Compile `verification/meshing/ring.cpp` with C++20, Gmsh headers/library and matching runtime path. No geometry data is bundled. [Gmsh license](https://gmsh.info/LICENSE.txt) is GPL-2.0-or-later with a named-library combination exception; do not characterize it as a general proprietary-linking exception. The GPLv3 option is compatible with the project policy. The existing host binary is research infrastructure; redistribution requires transitive audit.

Remaining: custom prism/layer extrusion, region-preserving MFEM conversion, independently specified dihedral/aspect-ratio and wavelength/skin-depth gates, standalone Netgen comparison, Linux/macOS CI. This synthetic ring is not a complete optical resonator simulation.
