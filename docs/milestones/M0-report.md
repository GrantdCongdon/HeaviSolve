<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M0 progress and acceptance report

Date:2026-11-02. **M0 NOT COMPLETE. Do not start M1. No solver is claimed verified.**

Repository foundations and several real local experiments are delivered. Missing paired-language, full-stack, Xyce, GUI and hosted-CI evidence prevent the requested exit criteria. See [tasks](M0-tasks.md), [one-page decisions](M0-decisions.md), and [next checkpoint](M0-next-checkpoint.md).

## Results

| Check | Result | Evidence |
|---|---|---|
| MFEM P1 Poisson | LOCAL PASS; orders1.97318,1.99316,1.99828 vs2±0.15 | [S1](../spikes/S1-mfem.md) |
| PEC cavity, first six positive modes | LOCAL PASS; maximum frequency relative error4.9435656211072043e-5 after order3 refinement;1331 expected gradient zeros | [Raw output](../../verification/results/mfem-local.log) |
| Coarse cavity | FAIL retained; sixth-mode error0.0027727428346264738 | [Raw failure](../../verification/results/cavity-coarse-failure.log) |
| Full S1 parallel complex stack | NOT PASS; conda dry resolve only, selected real variants | [S1](../spikes/S1-mfem.md) |
| S2 Palace reuse | Documentary PASS; reference/study decision, no link benchmark | [S2](../spikes/S2-palace.md) |
| S3a callback RC | LOCAL PASS;5018 samples,10041 callbacks,max error3.0577875786974573e-8V | [S3](../spikes/S3-spice.md) |
| IHP VBIC device | SMOKE PASS; collector current0.00013991752401704821A at VCE1V,VBE0.8V; no measured-data validation | [S3](../spikes/S3-spice.md) |
| S3a OSDI / S3b Xyce / S3c conformance | NOT PASS; OSDI not run, Xyce missing Trilinos, comparison unavailable | [ADR-003](../adr/ADR-003-spice-engine.md) |
| S4 ring quality | Optimized subtest PASS:4324 tets,minSICN0.42782904872064897; initial mesh FAIL | [S4](../spikes/S4-meshing.md) |
| S5 Qt6/VTK GUI | BLOCKED at Qt6 configuration; no fps | [S5](../spikes/S5-gui.md) |
| S6 GDS/OASIS | Synthetic roundtrip PASS; real-PDK and1M viewport not run | [S6](../spikes/S6-layout.md) |
| S7 IPC |100MB inherited shared mapping checksum PASS; protocol comparison not run | [S7](../spikes/S7-ipc.md) |
| R2 language | NOT COMPLETE; subjective research table only, no paired slab solver | [ADR-001](../adr/ADR-001-language.md) |
| Local foundation/license/docs checks | LOCAL PASS: foundation 1/1, REUSE no missing licenses/copyrights, strict docs build; hosted green status not claimed | CI workflow is configured, not executed remotely |
| `ctest -L m0` | FAIL: 2/3 tests pass; explicit acceptance gate fails on missing evidence | Machine-readable m0-status.toml fails closed |

## Deliverables and limitations

The section3.2 module layout exists with reserved directories. Added CMake research checks, Linux/macOS GitHub Actions jobs with output uploads, direct-license inventory enforcement, REUSE/DCO, original license texts, documentation site, coding standards and dependency strategy. Source SPDX inventory is not a full release binary SBOM. Conda/Spack/Docker are starter recipes, not fully locked tested environments. No remote repository is configured; no hosted CI runs or merge evidence exist. Research docs cover the requested landscape but explicitly retain unknown maintenance dates/exact grants. No restricted PDK data is committed.

## Deviations and failures

[ADR-004](../adr/ADR-004-plan-corrections.md) records Palace library/Floquet updates, Femwell license, public cspdk, engine-specific Verilog-A routes and the passive-permittivity sign correction. ngspice required a space-free build path and a local stdlib header patch. The RC test initially mishandled reusable vector metadata; the IHP test initially lacked corner/includes. These harness failures were fixed and retained. No benchmark number was manually adjusted.

## Name check

No conflict found in the quick GitHub search and exact package/domain queries; no name change or reservation. See [availability evidence](../research/name-availability.md). Absence of a current registry record is not trademark clearance or a guarantee that registration will succeed.

## Exit assessment

ADRs001/003 remain proposed. The final Phase R gate and walking-skeleton approval are open. Deliver this as an honest progress report, not a completed-M0 report. Next checkpoint is M0 closure, not M1.
