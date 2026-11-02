<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S3a–c: SPICE feasibility

## S3a ngspice — PARTIAL, overall NOT PASS

Built ngspice47 shared library on macOS arm64. Source archive SHA256 `894e649651f1838a14095e5a5439e7d3aa63e87ede14d283173fda4fcdef675f`. Configure: `--prefix=/tmp/heavisolve-spice/install --with-ngshared --without-x --disable-openmp --disable-klu --with-readline=no`, then `make -j6`, `make install`.

First attempt in workspace failed because XSPICE rules split paths containing spaces. Retried in `/tmp/heavisolve-spice`. AppleClang rejected missing malloc/free declarations in generated `src/xspice/icm/xtradev/seegenerator/cfunc.c`; prepended `#include <stdlib.h>` locally. This is a patched build, not an unmodified reproducibility success. Proper remediation: patch upstream `.mod` source and submit a reviewed fix separately, or evaluate a release/compiler combination that builds unchanged. No upstream message was sent.

C++ harness linked libngspice with rpath to isolated prefix. RC external-source callbacks:5018 samples,10041 callbacks, maximum absolute voltage error3.0577875786974573e-8 against1e-4 tolerance. [Raw output](../../verification/results/ngspice-rc.log), [samples](../../verification/results/ngspice-rc.csv). First run failed because `ngGet_Vec_Info` reuses result storage; copying its metadata before a second lookup fixed the harness. Failure preserved.

IHP npn13G2 VBIC smoke test: VCE1V,VBE0.8V, collector current0.00013991752401704821A. This is a finite-positive-current smoke check, not validation against measurement. Uses Apache-2.0 headers in the public HBT model/corner/stat files, loaded from ignored `.local`; no model data bundled. Missing corner/model include failures were resolved without changing device parameters. [Output](../../verification/results/ngspice-ihp.log). R3 records upstream research pin; model file digests are in provenance.

OpenVAF/OSDI loading, synchronization/rollback, Linux execution and standalone-netlist equivalence remain untested. Therefore the full S3a criterion is NOT PASS.

## S3b Xyce — BLOCKED / NOT PASS

Exploratory master archive SHA256 `5fc373fd2eec5c228352ec770f9276e0fa6e58b782b6254ad627c1a86052a969`; not a release pin. CMake configuration failed because TrilinosConfig.cmake was absent. [Log](../../verification/results/s3-xyce-configure.log). No Xyce executable, RC/IHP output or HB comparison was produced. Current source uses CMake/C++17; use version-matched instructions, not the older website recipe. Next alternative: a pinned Xyce release with its supported Trilinos configuration in a dedicated Linux build image, then macOS port. IHP uses ADMS-generated plugins, not assumed OSDI.

## S3c dialect conformance — NOT RUN / NOT PASS

Cannot compare engines without working Xyce. No common IR/dialect implementation or RC/RLC/diode/amplifier corpus was completed. Proposed initial thresholds remain DC1e-4 relative, AC1e-3, transient NRMSE1e-3 with absolute floors to define before execution. No score or agreement number is fabricated. ADR-003 remains proposed.
