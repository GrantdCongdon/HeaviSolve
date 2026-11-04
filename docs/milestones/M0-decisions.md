<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 decision summary — 2026-11-04

**M0 complete: user-approved PR1 merged at4025a1d. M1 has not started.**

- **Licensing:** retain AGPL-3.0-or-later code, CC-BY-SA-4.0 prose and DCO without CLA. Direct grants and REUSE pass locally. Reject the convenient FEM environment because ParMETIS restricts use/redistribution; the new transitive audit fails closed. ADR006 now records13 exact macOS and14 exact Linux runtime-package reviews; redistribution auditing remains separate. [ADR-002](../adr/ADR-002-licensing.md), [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md).
- **Language:** accept C++20 under ADR008. Independently assembled C++/Rust slab implementations both converge at roughly second order and agree within9.37e-14. Weighted roadmap suitability is134/145 versus86/145; no controlled speed advantage is claimed. Equivalent ctypes/C-ABI bindings pass on both hosted platforms; full framework comparison and historical development hours remain unmeasured. [ADR-001](../adr/ADR-001-language.md).
- **FEM:** select MFEM infrastructure, with production mapping/configuration admission still gated under ADR008. Serial and complex source-stack cavity tests locally meet1e-3; the clean complex result is4.9436e-5 on one rank. MFEM4.10 resolves the older-package/hypre header incompatibility. Baseline Linux/macOS CI passes; complex-stack cavity and declared runtime-license audits now pass on both platforms. [S1](../spikes/S1-mfem.md).
- **Palace:** use as reference/study. libpalace and Floquet exist; stable API/data mapping and HeaviSolve benchmarks remain unproven. [S2](../spikes/S2-palace.md).
- **SPICE:** retain both engines as co-primary targets:98/160 versus94/160 does not satisfy the sole-winner rule. Xyce HB/forward stepping and ngspice callbacks pass locally and in Linux CI41858845394; OSDI remains locally tested, excluded from that hosted subset. IHP AC differs8–10%, so equal-accuracy support is not established. Preserve engine-specific model routes and investigate rather than relaxing tolerances. [ADR-003](../adr/ADR-003-spice-engine.md).
- **PDKs/layout:** keep process specifications user-defined and fixtures externally loaded. Prefer KLayout for tested public IHP/SiEPIC geometry round trips: all pass, while gdstk's SiEPIC OAS route changes geometry. No unrestricted general PCell/property fidelity claim. [R3](../research/pdk-survey.md), [S6](../spikes/S6-layout.md).
- **Mesh/GUI/IPC:** native prism extrusion imports into MFEM with volume/Jacobian checks. Qt/VTK renders the field cut plane;10k and1M scenes reach75.8/68.3 repaint/s, with lower earlier results retained. Both IPC candidates exchange progress plus100MB mapped-array descriptors/checksums. Prefer structured RPC as the future interface direction, but neither timing run establishes an overall transport winner. [S4](../spikes/S4-meshing.md), [S5](../spikes/S5-gui.md), [S7](../spikes/S7-ipc.md).
- **Name/conventions:** keep HeaviSolve; quick availability checks found no conflict. For exp(+jωt), passive permittivity has nonpositive imaginary part. [ADR-004](../adr/ADR-004-plan-corrections.md).

- **Milestone scope:** ADR007 aligns acceptance with section12: measured spike reports may contain failures. M0 acceptance passes3/3 on both platforms in six-job CI41922593403 at239cb7f; verified artifacts are retained. Acceptance, deliverables and exit are complete after the approved PR1 merge. ADR008 completes component dispositions while withholding unproved production admission. Docker CI41922593302 passes3/3; walking-skeleton design self-review is complete. S3c remains a failed feasibility result and M7 conformance blocker. [ADR-007](../adr/ADR-007-m0-acceptance-scope.md), [ADR-008](../adr/ADR-008-phase-r-component-dispositions.md).

Full binary-release audits remain required before distribution. No production solver is called verified.

Final exit: all final-head checks passed and PR1 merged on2026-11-04. The next proposed checkpoint is the M1 capacitor walking skeleton; stop here before implementation.
