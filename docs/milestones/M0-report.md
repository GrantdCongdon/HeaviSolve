<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 implementation and acceptance report

Updated 2026-11-03. **M0 remains incomplete; M1 has not started. No solver is claimed verified.** Substantial local feasibility work is complete, but IHP conformance, dependency admission and hosted CI block the exit. Future sessions should start with the [running handoff](M0-handoff.md), then [tasks](M0-tasks.md), [decisions](M0-decisions.md) and [next checkpoint](M0-next-checkpoint.md).

## Measured results

| Check | Result and limits | Evidence |
|---|---|---|
| MFEM Poisson | LOCAL PASS; observed orders1.97318,1.99316,1.99828 vs2±0.15 | [S1](../spikes/S1-mfem.md) |
| Serial cavity | LOCAL PASS; first-six maximum frequency relative error4.9435656e-5 vs1e-3; coarse failure retained | [S1](../spikes/S1-mfem.md) |
| Complex source-built cavity | LOCAL PASS; MFEM4.10/PETSc/SLEPc/SuperLU_DIST,4356 DOFs, one rank, maximum error4.9435655966822978e-5 | [Output](../../verification/results/fem-clean-cavity.log) |
| Full S1 admission/platform gate | NOT PASS; restricted original environment rejected, smaller environment review and Linux/macOS CI incomplete | [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md) |
| C++/Rust slab | LOCAL PASS; four refinements, near-second-order convergence, maximum language difference9.37e-14; bindings/time-accounting incomplete | [ADR-001](../adr/ADR-001-language.md) |
| S2 Palace | Documentary PASS; reference/study, no stable-link integration claim | [S2](../spikes/S2-palace.md) |
| S3a ngspice | LOCAL PASS; callback RC max error3.0578e-8V; IHP HBT smoke; compiled OSDI current agrees within1e-12A | [S3](../spikes/S3-spice.md) |
| S3b Xyce | macOS build and HB subtests PASS; RLC relative error3.7609e-16, cubic3.5237e-15; Linux/coupling gate pending | [S3](../spikes/S3-spice.md) |
| S3c conformance | FAIL; IHP AC voltage/current disagreement8.35%/9.81%, tighter DC current1.0326e-4 exceeds1e-4; linear cases pass | [S3](../spikes/S3-spice.md) |
| S4 mesh | LOCAL PASS; optimized4324 tets; custom256 prisms, positive Jacobians, volume and MFEM import checks | [S4](../spikes/S4-meshing.md) |
| S5 GUI | Visible VTK cut plane;10k-item75.7988 repaint/s, earlier56.1598 failure retained; compositor fps unmeasured | [S5](../spikes/S5-gui.md) |
| S6 layout | KLayout IHP/SiEPIC GDS/OAS PASS; gdstk SiEPIC OAS FAIL; revised1M viewport68.2641 repaint/s | [S6](../spikes/S6-layout.md) |
| S7 IPC | Both native protocols PASS100MB shared mapping/checksum/progress in independent processes; no remote-copy or profiler claim | [S7](../spikes/S7-ipc.md) |
| Foundation | LOCAL PASS2/2: direct inventory and fail-closed transitive-policy checks | [Output](../../verification/results/foundation-final.log) |
| REUSE/docs | Local lint and strict docs build pass; not a full distribution audit | [REUSE output](../../verification/results/reuse-final.log) |
| M0 acceptance | FAIL: numerical tests pass, explicit evidence gate remains false | [CTest output](../../verification/results/m0-final.log) |

## Decisions, deviations and risks

C++20 is the recommended direction after measured slab comparison and weighted134/86 suitability scores. R6 records98/160 ngspice versus94/160 Xyce, insufficient to select a sole winner; both remain co-primary targets. Their IHP model differences are potential explanations, not yet proven causes. Tolerances and foundry data were not changed to manufacture agreement.

ADR-004 records corrected Palace capabilities, Femwell licensing, public CORNERSTONE cspdk, engine-specific Verilog-A routes and passive-permittivity sign. ADR-005 rejects the ParMETIS-bearing binary environment. The manual slab assembly and missing binding/effort measurements are explicit ADR-001 deviations. GUI throughput is scoped to repaints. Archived Clipper2 and Strawberry Fields are flagged in the refreshed survey. No candidate bypasses the component admission rubric.

Repository foundations include the requested layout, license/DCO/REUSE, CI definitions for Linux/macOS, stored-output uploads, docs site, coding standards and dependency strategy. Direct primary-source licenses are inventoried; ngspice mixed-license and transitive runtime reviews remain open. Docker/Spack recipes are unproven starters, not tested release environments. No restricted PDK data is bundled.

## External gate and next checkpoint

No remote repository is configured and no hosted CI artifacts exist. The available connector cannot create the repository; the browser creation page requires sign-in. Local outputs cannot satisfy the explicit CI requirement. Complete remaining M0 checks, resolve model/license issues and obtain actual CI evidence before accepting final ADRs or starting M1.

The quick name check found no conflict; HeaviSolve is unchanged. [Availability evidence](../research/name-availability.md) is a limited registry/search check, not trademark clearance or a reservation.
