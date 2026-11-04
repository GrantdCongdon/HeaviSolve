<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 decision summary — 2026-11-03

**M0 remains open; these decisions do not authorize M1.**

- **Licensing:** retain AGPL-3.0-or-later code, CC-BY-SA-4.0 prose and DCO without CLA. Direct grants and REUSE pass locally. Reject the convenient FEM environment because ParMETIS restricts use/redistribution; the new transitive audit fails closed. ADR006 now records13 exact macOS and14 exact Linux runtime-package reviews; redistribution auditing remains separate. [ADR-002](../adr/ADR-002-licensing.md), [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md).
- **Language:** recommend C++20. Independently assembled C++/Rust slab implementations both converge at roughly second order and agree within9.37e-14. Weighted roadmap suitability is134/145 versus86/145; no controlled speed advantage is claimed. Equivalent ctypes/C-ABI bindings pass on both hosted platforms; full framework comparison and historical development hours remain unmeasured. [ADR-001](../adr/ADR-001-language.md).
- **FEM:** retain MFEM infrastructure as candidate. Serial and complex source-stack cavity tests locally meet1e-3; the clean complex result is4.9436e-5 on one rank. MFEM4.10 resolves the older-package/hypre header incompatibility. Baseline Linux/macOS CI passes; complex-stack cavity and declared runtime-license audits now pass on both platforms. [S1](../spikes/S1-mfem.md).
- **Palace:** use as reference/study. libpalace and Floquet exist; stable API/data mapping and HeaviSolve benchmarks remain unproven. [S2](../spikes/S2-palace.md).
- **SPICE:** retain both engines as co-primary targets:98/160 versus94/160 does not satisfy the sole-winner rule. Xyce HB and ngspice callbacks/OSDI work locally. IHP AC differs8–10%, so equal-accuracy support is not established. Preserve engine-specific model routes and investigate rather than relaxing tolerances. [ADR-003](../adr/ADR-003-spice-engine.md).
- **PDKs/layout:** keep process specifications user-defined and fixtures externally loaded. Prefer KLayout for tested public IHP/SiEPIC geometry round trips: all pass, while gdstk's SiEPIC OAS route changes geometry. No unrestricted general PCell/property fidelity claim. [R3](../research/pdk-survey.md), [S6](../spikes/S6-layout.md).
- **Mesh/GUI/IPC:** native prism extrusion imports into MFEM with volume/Jacobian checks. Qt/VTK renders the field cut plane;10k and1M scenes reach75.8/68.3 repaint/s, with lower earlier results retained. Both IPC candidates exchange progress plus100MB mapped-array descriptors/checksums. Prefer structured RPC as the future interface direction, but neither timing run establishes an overall transport winner. [S4](../spikes/S4-meshing.md), [S5](../spikes/S5-gui.md), [S7](../spikes/S7-ipc.md).
- **Name/conventions:** keep HeaviSolve; quick availability checks found no conflict. For exp(+jωt), passive permittivity has nonpositive imaginary part. [ADR-004](../adr/ADR-004-plan-corrections.md).

Next checkpoint is M0 closure: resolve conformance and license issues, finish missing experiments, run hosted CI with stored output, then self-review and report before M1. No solver is called verified.
