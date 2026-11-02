<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 decision summary (one page)

**M0 remains open.** Research hypotheses are not architecture approval.

- **License:** AGPL-3.0-or-later code, CC-BY-SA-4.0 prose, DCO without CLA. Primary license texts and REUSE checks implement the owner choice. AGPL obligations do not mean every private fork must be published. ADR-002 records exact legal scope and pre-release review.
- **Language:** C++20 is still provisional. Native MFEM, Gmsh and libngspice experiments work locally; the paired Rust/C++ slab study is incomplete. ADR-001 must not be treated as a measured final ranking.
- **FEM:** MFEM4.8 is a viable serial research candidate: Poisson observed order approaches2 and six cavity frequencies meet1e-3 after p-refinement. This is not the required parallel complex stack or CI verification. No production architecture lock.
- **Palace:** keep as reference/study candidate. It has libpalace and Floquet support; public API stability and HeaviSolve benchmarks are unproven. PML remains a documented gap. S2 supports the reference decision.
- **SPICE:** retain both ngspice/Xyce as co-primary targets until measured scores establish a winner. ngspice callback RC passes locally; Xyce configuration fails at missing Trilinos. Use per-engine model routes: OpenVAF/OSDI versus ADMS/plugin. Full compatibility is not claimed.
- **PDKs:** preserve user-defined process specs and per-artifact licenses. Public cspdk is distinct from gated CORNERSTONE distributions. IHP includes VBIC models and a nested ECL-2.0 exception needing separate review. Never bundle restricted data.
- **Geometry/GUI/IPC:** ring optimization and synthetic GDS/OASIS/100MB shared-memory subtests provide limited feasibility evidence. They do not establish custom extrusion, real-PDK fidelity,60fps or a chosen RPC transport.
- **Names and conventions:** keep HeaviSolve; quick checks found no conflict, without trademark clearance. For exp(+j omega t), passive epsilon has nonpositive imaginary part; ADR-004 corrects the opposite validation sign in the plan.

Evidence is linked in the individual research/spike reports and raw outputs under verification/results. Hosted CI has not run, so no solver is called verified.
