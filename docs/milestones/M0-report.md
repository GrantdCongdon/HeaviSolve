<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 implementation and acceptance report

Updated 2026-11-04. **M0 remains incomplete; M1 has not started.** The specified M0 acceptance label passes locally (3/3), and its numerical and license components have stored Linux/macOS CI passes. The revised aggregate label still needs hosted validation. ADR008 completes Phase R decision dispositions; remaining exit work is remote integration of the accepted ADRs. The walking-skeleton design has completed self-review, conditional on M0 exit.

[ADR-007](../adr/ADR-007-m0-acceptance-scope.md) corrects the earlier report's scope: M0 requires measured feasibility reports, including failures; full supported-engine SPICE conformance belongs to M7. S3c remains **FAIL**, not a pass obtained by moving a gate. Dependency admission still precedes adoption, and binary distribution still requires its release audit. Start future sessions with the [running handoff](M0-handoff.md), then [tasks](M0-tasks.md), [decisions](M0-decisions.md) and [next checkpoint](M0-next-checkpoint.md).

## Measured results

| Check | Result and limits | Evidence |
|---|---|---|
| MFEM Poisson | Linux/macOS CI PASS; observed orders1.97318,1.99316,1.99828 vs2±0.15 | [S1](../spikes/S1-mfem.md) |
| Serial cavity | Linux/macOS CI PASS; first-six maximum frequency relative error4.9435656e-5 vs1e-3; coarse failure retained | [S1](../spikes/S1-mfem.md) |
| Complex source-built cavity | Linux/macOS CI PASS; MFEM4.10/PETSc/SLEPc/SuperLU_DIST,4356 DOFs, one rank, maximum error4.943565595971755e-5 Linux /4.9435655969265468e-5 macOS | [Hosted provenance](../../verification/results/ci-41715967429/provenance.json) |
| S1 platform/cavity spike | PASS; source-selected complex stack and declared runtime-license audit pass on Linux/macOS; no full binary-release certification | [ADR-005](../adr/ADR-005-transitive-fem-dependencies.md) |
| C++/Rust slab | Linux/macOS CI PASS; four refinements, near-second-order convergence, maximum language difference9.37e-14; ctypes/C-ABI bindings also pass locally and in CI; framework comparison/historical time-accounting limited | [ADR-001](../adr/ADR-001-language.md) |
| S2 Palace | Documentary PASS; reference/study, no stable-link integration claim | [S2](../spikes/S2-palace.md) |
| S3a ngspice | LOCAL PASS; callback RC max error3.0578e-8V; IHP HBT smoke; compiled OSDI current agrees within1e-12A | [S3](../spikes/S3-spice.md) |
| S3b Xyce | macOS build, native forward stepping and HB subtests PASS; RLC relative error3.7609e-16, cubic3.5237e-15; Linux build pending | [S3](../spikes/S3-spice.md) |
| S3c conformance | FAIL; IHP AC voltage/current disagreement8.35%/9.81%, strict DC current1.0304146e-4 exceeds1e-4; linear cases pass | [S3](../spikes/S3-spice.md) |
| S4 mesh | LOCAL PASS; optimized4324 tets; custom256 prisms, positive Jacobians, volume and MFEM import checks | [S4](../spikes/S4-meshing.md) |
| S5 GUI | Visible VTK cut plane;10k-item75.7988 repaint/s, earlier56.1598 failure retained; compositor fps unmeasured | [S5](../spikes/S5-gui.md) |
| S6 layout | KLayout IHP/SiEPIC GDS/OAS PASS; gdstk SiEPIC OAS FAIL; revised1M viewport68.2641 repaint/s | [S6](../spikes/S6-layout.md) |
| S7 IPC | Both native protocols PASS100MB shared mapping/checksum/progress in independent processes; no remote-copy or profiler claim | [S7](../spikes/S7-ipc.md) |
| Foundation | LOCAL PASS3/3: inventory, transitive policy and milestone-gate policy | [Output](../../verification/results/foundation-current.log) |
| REUSE/docs | Local lint and strict docs build pass; not a full distribution audit | [REUSE output](../../verification/results/reuse-final.log) |
| M0 acceptance | LOCAL PASS3/3; revised aggregate label awaiting hosted CI | [Current numerical-build CTest output](../../verification/results/m0-acceptance-current.log) |

## Decisions, deviations and risks

C++20 is the accepted implementation direction under ADR008 after measured slab comparison and weighted134/86 suitability scores. R6 records98/160 ngspice versus94/160 Xyce, insufficient to select a sole winner; both remain co-primary targets. The residual IHP DC disagreement is now localized to avalanche behavior; the full source-level cause remains unproven. Tolerances and foundry data were not changed to manufacture agreement.

ADR-004 records corrected Palace capabilities, Femwell licensing, public CORNERSTONE cspdk, engine-specific Verilog-A routes and passive-permittivity sign. ADR-005 rejects the ParMETIS-bearing binary environment. The manual slab assembly, limited binding-framework comparison and missing historical effort measurements are explicit ADR-001 deviations. GUI throughput is scoped to repaints. Archived Clipper2 and Strawberry Fields are flagged in the refreshed survey. No candidate bypasses the component admission rubric.

Repository foundations include the requested layout, license/DCO/REUSE, CI definitions for Linux/macOS, stored-output uploads, docs site, coding standards and dependency strategy. Direct primary-source licenses are inventoried; ngspice mixed-license and transitive runtime reviews remain open. The foundation Docker image builds and passes its two checks in CI run41858845826; retained logs and image identity establish that narrow result, not a published release image. Spack remains an untested HPC starter. No restricted PDK data is bundled.

## Hosted CI and next checkpoint

The user configured the public GrantdCongdon/HeaviSolve repository and explicitly approved review-branch uploads. Remote main remains unchanged. [Run41668976621](https://github.com/GrantdCongdon/HeaviSolve/actions/runs/41668976621), commit47b8352, passed all six jobs: Linux/macOS foundations, Poisson/cavity diagnostics, and paired-language/binding tests. [Artifact provenance and checksums](../../verification/results/ci-41668976621/provenance.json) accompany locally retained numerical outputs. These are scoped benchmark passes, not full M0 certification.

The separate source-built complex-stack run first failed on missing macOS conda and Linux OpenBLAS filename handling. Both setup issues were fixed; run41670183802 passed on macOS (maximum cavity error4.9435655969265468e-5), with [retained configuration, numerical and license evidence](../../verification/results/ci-41670183802/provenance.json). Linux failed due to missing SLEPC_DIR during make; cb9d540 fixes this and adds exact reviews for14 Linux runtime packages. Linux job126195902515 in run41715967429 passes that correction, with maximum cavity error4.943565595971755e-5 and passing runtime-license audit; no exception silently admits unknown packages. The IHP default self-heated AC and residual DC failures remain blockers for the promised M7 conformance, not blanket M0 acceptance conditions.

Linux output records a UCX initialization error before the one-rank solve succeeds; multi-rank/UCX transport support is not established.

Complete the remaining M0 hosted checks and remote ADR integration before starting M1. Component-specific production admission remains mandatory before adding each dependency.

The quick name check found no conflict; HeaviSolve is unchanged. [Availability evidence](../research/name-availability.md) is a limited registry/search check, not trademark clearance or a reservation.

## Latest investigation and license follow-up

Equivalent C++/Rust C ABI wrappers called through Python pass argument, capacity, oracle and lifetime checks on Linux/macOS CI. This is a narrow binding comparison, not nanobind/PyO3 validation. ADR006 admits13 exact macOS and14 exact Linux runtime-package identities after reviewing shipped grants; metadata admission does not certify redistribution compliance. The IHP AC discrepancy was localized with independent DC slopes to the tested self-heated ngspice path; explicit isothermal AC/transient pass, while strict DC base-current relative RMS remains1.0304146e-4 against1e-4. Original models and tolerances remain intact.

Native Xyce C-interface forward stepping now passes locally:50 stops, maximum RC voltage error7.1045086396173684e-7V against1e-4V. The separate xycecinterface build target is required. Rollback, external-device exchange and Linux remain untested.

The strict original-model DC failure was reproduced. Disabling avalanche only in marked diagnostic copies reduces base-current disagreement to4.317717800750406e-9, localizing the residual to model implementation differences. The original test still fails; an identically versioned OSDI/ADMS compact-model route is an untested next experiment, not an approved replacement.

Run41715967429 passes on both Linux/macOS at cb9d540; [same-revision artifacts and digests](../../verification/results/ci-41715967429/provenance.json) are retained. Linux SPICE attempts exposed a non-UTF8 generator input, unwanted optional NetCDF configuration and a missing Flex header. The recipe now preserves source bytes, disables optional Trilinos packages, and installs the Flex development headers. Trilinos built successfully in run41769077217; Xyce Linux remains pending in run41858845394. Failed outputs are retained, including [the third attempt](../../verification/results/ci-41769077217/provenance.json).

The [ngspice selected-build license audit](../research/ngspice47-license-scope.md) records source hashes, exact grants and local configuration evidence. Scoped Sparse/public-domain/m4 mappings are documented, but the candidate remains outside approved production dependencies. Passing a research build does not authorize its full runtime graph.

## Acceptance, deliverables and exit

- **Acceptance:** local `ctest --test-dir build-numerical -L m0` passes3/3; the revised aggregate CI command must run on the review branch. Baseline hosted numerical/language/license results remain valid evidence at their recorded commits.
- **Deliverables:** surveys, scored ADRs, all spike reports, skeleton, Linux/macOS CI, docs and coding standards exist. The [container build/test evidence](../../verification/results/ci-41858845826/provenance.json) is stored. [ADR008](../adr/ADR-008-phase-r-component-dispositions.md) completes Phase R component dispositions; experimental dependencies remain outside production admission where their checks are unfinished.
- **Exit:** the [walking-skeleton design](../developer/walking-skeleton-plan.md) is self-reviewed. Research decisions are accepted in ADR008, but remote integration remains open and remote main has not changed. The [all-stage review](../../verification/results/m0-exit-current.log) retains `adrs_accepted_and_merged` as incomplete.

No production solver or full milestone completion is claimed. Report the completed M0 checkpoint before beginning M1.
