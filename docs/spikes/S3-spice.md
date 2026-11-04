<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S3a–c: SPICE feasibility

## S3a ngspice — LOCAL PASS, hosted CI pending

Built ngspice47 shared library on macOS arm64. Source archive SHA256 `894e649651f1838a14095e5a5439e7d3aa63e87ede14d283173fda4fcdef675f`. Configure: `--prefix=/tmp/heavisolve-spice/install --with-ngshared --without-x --disable-openmp --disable-klu --with-readline=no`, then `make -j6`, `make install`.

First attempt in workspace failed because XSPICE rules split paths containing spaces. Retried in `/tmp/heavisolve-spice`. AppleClang rejected missing malloc/free declarations in generated `src/xspice/icm/xtradev/seegenerator/cfunc.c`; prepended `#include <stdlib.h>` locally. This is a patched build, not an unmodified reproducibility success. Proper remediation: patch upstream `.mod` source and submit a reviewed fix separately, or evaluate a release/compiler combination that builds unchanged. No upstream message was sent.

C++ harness linked libngspice with rpath to isolated prefix. RC external-source callbacks:5018 samples,10041 callbacks, maximum absolute voltage error3.0577875786974573e-8 against1e-4 tolerance. [Raw output](../../verification/results/ngspice-rc.log), [samples](../../verification/results/ngspice-rc.csv). First run failed because `ngGet_Vec_Info` reuses result storage; copying its metadata before a second lookup fixed the harness. Failure preserved.

IHP npn13G2 VBIC smoke test: VCE1V,VBE0.8V, collector current0.00013991752401704821A. This is a finite-positive-current smoke check, not validation against measurement. Uses Apache-2.0 headers in the public HBT model/corner/stat files, loaded from ignored `.local`; no model data bundled. Missing corner/model include failures were resolved without changing device parameters. [Output](../../verification/results/ngspice-ihp.log). R3 records upstream research pin; model file digests are in provenance.

OpenVAF-Reloaded v24.0.2mob macOS arm64 compiled the project's cubic Verilog-A conductance to OSDI. Archive SHA256 `022d5659257239af98f5e8ee59e2fe4403e1b2e694a06461152d5251c0ad0196`. Native `ngspice_osdi.cpp` loads it with the shared-library `osdi` command (not `pre_osdi`), then computes 0.0011000000000000001 A at 1 V, identical to the analytic result within 1e-12 A. [Output](../../verification/results/s3-osdi.log). A space-free temporary path avoids ngspice command quoting limitations. The compiler version string itself reports unknown; the release asset hash is the pin. Linux, rollback and hosted CI remain untested.

## S3b Xyce — numerical subtests LOCAL PASS; platform gate NOT PASS

Built release 7.10.0 on macOS arm64 with Trilinos16.1.0, FFTW, AMD and SuiteSparseConfig. Xyce archive SHA256 `b5a883196f0a2b3972fd13c541fecf04735bfabc7d124d7c7e17de707204f4e2`; Trilinos SHA256 `e9651c88f581049457036cfc01b527a9d3903c257338eeeab942befd7452f23a`. Failed exploratory master configure remains stored. This successful build required Fortran enabled in Trilinos, `-fsecond-underscore` to match AztecOO symbol declarations, explicit `M4` for bison, and replacing two `std::abs<double>(val)` calls with `std::abs(val)` in `N_LAS_BlockSystemHelpers.C`. These compatibility patches must be reproduced in CI; Linux has not run.

The research runner launches Xyce as a subprocess. The native stepwise library experiment below now exercises `simulateUntil` and circuit-value reads on macOS; rollback and general external-device coupling remain untested. ADMS was unavailable; the pinned IHP Xyce HBT uses built-in VBIC level12 and runs without an ADMS plugin. ngspice uses its corresponding level9 file. Neither route establishes MOS coverage.

Xyce HB series RLC: R=1000 ohm, L=1mH, C=1nF, 1MHz sinusoid. Fundamental current phasor relative error **3.760856706849292e-16** versus `1/(R+j(omega L-1/(omega C)))`. Cubic conductance g1=0.001 S, g3=0.0001 A/V³: fundamental/third-harmonic maximum relative error **3.5236570605778894e-15**. Xyce outputs complex Fourier coefficients: nonzero-frequency peak amplitude is twice their magnitude. ngspice transient followed by a 4096-point FFT on the final period gives fundamental **0.0010749964632357002 A**, third **2.4999259632067543e-5 A**, maximum relative error **2.9614717298327145e-5**. All pass the declared 1e-3 HB/FFT threshold. These are local tests, not CI verification.

## S3c dialect conformance — FAIL, substantive model differences

`verification/spice/conformance.cpp` is a small native engine-neutral circuit IR with per-engine output/options/model emitters. `ngspice_run.cpp` extracts native engine vectors; Python only launches engines, interpolates and compares results. The corpus contains RC, series RLC, diode and IHP npn13G2 common-emitter amplifier. Analyses are DC source sweep0.7–0.8V, AC1kHz–100MHz, and 10us transient. Compare output voltage and drive-source current. Linear interpolation uses ngspice sample times inside the Xyce time range; relative RMS normalization has a 1e-12 absolute denominator floor. DC bound1e-4, AC/transient1e-3; no tolerance was relaxed. These scoped checks do not establish arbitrary lossless netlist translation.

[Full numerical summary](../../verification/results/s3-conformance.json), [raw emitted decks, engine logs and CSV outputs](../../verification/results/s3-conformance-output.tar.gz), [source/model hashes](../../verification/results/s3-conformance-provenance.json).

| Case | DC | AC | Transient |
|---|---|---|---|
| RC | PASS | PASS | PASS; voltage NRMSE7.75509e-6 |
| RLC | PASS | PASS | PASS; voltage NRMSE2.01837e-5 |
| Diode | FAIL at original solver settings; current relative RMS1.004918e-4 | PASS | PASS |
| IHP HBT amplifier | FAIL; base-current relative RMS1.359698e-4 | FAIL; voltage relative RMS0.0834799, current0.0980982 | PASS; voltage5.64525e-6/current7.69790e-5 |

A separate [solver-tolerance sensitivity test](../../verification/results/s3-dc-tolerance-sensitivity.json) tightened numerical reltol1e-8→1e-10 and abstol1e-14→1e-16 without changing models or acceptance bounds. Diode DC then passes at9.7835463e-5; IHP DC remains above threshold at1.0325884e-4. The original failures remain recorded. No full-suite pass is claimed.

The pinned foundry files differ beyond syntax: ngspice has `ikp=1.00E-04*(Nx*0.25)` while the Xyce counterpart has `.00E-04*(Nx*0.25)`; delay/NQS defaults differ, and the engines use different VBIC implementations. These differences are observed potential causes, not a proven attribution of the AC discrepancy. Model files were not edited. The 8–10% AC disagreement blocks equal-accuracy support and requires a focused model/linearization investigation before M0 closes. No restricted or public foundry model files are included in the stored result archive.

Harness failures were also retained: initial Xyce DC column assumptions and ngspice complex-frequency metadata handling. The corrected runner copies ngspice vector metadata and reads complex frequency correctly. Stored output was not hand-edited.

## Follow-up: isolate self-heating and residual DC disagreement (2026-11-03)

[Controlled AC variants](../../verification/results/s3-ihp-diagnostic-repeat.json), [independent DC slopes](../../verification/results/s3-ihp-dc-slopes-repeat.json), [isothermal/gmin sweep](../../verification/results/s3-ihp-isothermal-gmin.json), [copied-model DC parameter test](../../verification/results/s3-ihp-dc-parameter-diagnostic.json), [raw decks/output](../../verification/results/s3-ihp-diagnostic-output.tar.gz), [provenance](../../verification/results/s3-ihp-diagnostic-provenance.json).

Explicitly setting the public instance parameter `selft=0` in both engines reduces AC voltage/current relative RMS from0.0834799/0.0980982 to3.56466e-5/5.46809e-5: within the existing1e-3 criterion. The original foundry files remain unchanged. Matching the delay/NQS settings or `ikp` individually in marked diagnostic copies does not remove the baseline AC mismatch.

With self-heating enabled, central-difference DC slopes at perturbations1e-5,1e-6 and1e-7V agree near−4.5841V/V in both engines. Xyce's1kHz AC gain is−4.58407865; ngspice's is−4.20134588. With self-heating disabled, DC slopes and AC gains agree near−4.223104. This points to the tested ngspice VBIC self-heated AC linearization path, rather than simply a different DC operating point. It is evidence of a specific behavioral inconsistency, not a proven source-line diagnosis or an upstream bug report.

The full isothermal test has passing AC and transient comparisons, but still fails DC base-current agreement. Tight reltol/abstol, matched gmin down to1e-16, and voltage tolerance checks reduce but do not eliminate the residual. The stricter diagnostic original-model case measures1.0304146187721579e-4 relative RMS, just above1e-4, with maximum absolute difference1.0837545900853101e-11A. Matching `ikp` or delay on the diagnostic Xyce copy does not remove it. No acceptance bound was changed and no copied model is promoted as a validated replacement.

Consequently, keep self-heated AC explicitly unsupported for cross-engine equivalence in this tested configuration. Isothermal AC/transient feasibility is now demonstrated locally; the full IHP conformance gate remains FAIL pending DC investigation and CI. Neither replacing the default case nor suppressing base-current comparisons is an acceptable way to declare a pass.

## Follow-up: native Xyce stepwise API (2026-11-03)

[Native harness](../../verification/spice/xyce_step.cpp) and [RC deck](../../verification/spice/xyce_step.cir) drive the C interface through50 successive100ns requests to5us. Every returned time matches the requested time within1ps and advances monotonically. At each stop the harness reads V(out) and compares it against the closed-form zero-initial-condition sine-driven RC response. Maximum absolute error7.1045086396173684e-7V is below1e-4V: **LOCAL PASS**. [Samples](../../verification/results/s3-xyce-step.csv), [runtime output](../../verification/results/s3-xyce-step.log), [provenance](../../verification/results/s3-xyce-step-provenance.json).

The first link against libxyce alone failed: the exported C-interface functions reside in a separate upstream target excluded from the default build. Explicitly building `xycecinterface` succeeded. This is an upstream build option, not a source patch. Reproduce against the existing pinned Xyce build:

```sh
cmake --build /tmp/heavisolve-spice/xyce-build --target xycecinterface -j2
clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror   -I/tmp/heavisolve-spice/xyce/include verification/spice/xyce_step.cpp   -L/tmp/heavisolve-spice/xyce-build/utils/XyceCInterface -lxycecinterface   -Wl,-rpath,/tmp/heavisolve-spice/xyce-build/utils/XyceCInterface   -o /tmp/heavisolve-spice/xyce-step
cp verification/spice/xyce_step.cir /tmp/heavisolve-spice/xyce-step.cir
/tmp/heavisolve-spice/xyce-step /tmp/heavisolve-spice/xyce-step.cir verification/results/s3-xyce-step.csv
```

This narrows the API uncertainty to unsupported experiments: rollback, exchanged external-device values, and Linux execution. It does not establish full co-simulation conformance or change ADR003 scores without a comparable re-evaluation.

## Follow-up: residual DC localized to avalanche (2026-11-03)

The [bounded copied-model diagnostic](../../verification/spice/diagnose_ihp_avalanche.py) first reproduces the original strict isothermal DC base-current error1.0304146187721579e-4. Setting `avc1=0` in both diagnostic copies reduces it to4.317717800750406e-9, with maximum absolute difference8.623976484614605e-16A. [Results and output hashes](../../verification/results/s3-ihp-avalanche.json), [source/formula provenance](../../verification/results/s3-ihp-avalanche-provenance.json). Original foundry models remain unchanged and their baseline remains FAIL.

The native ngspice and Xyce VBIC1.3 implementations use different avalanche smoothing expressions. The upstream VBIC1.3 source explicitly describes an avalanche-function modification for forward/low reverse bias; generated Xyce code includes the additional smoothing shift. Disabling the contribution localizes the discrepancy to avalanche behavior; no source-patch experiment has proven the smoothing shift alone explains every residual. This is evidence of model-implementation differences, not a generic engine accuracy ranking or a reason to remove avalanche from production models.

A possible next experiment is an identically versioned compact-model source through ngspice OSDI and Xyce ADMS. Its source grant, compiler compatibility, thermal behavior and parameter mapping must be checked first. That route remains untested and is not an accepted replacement. Full original-model conformance and the M0 gate remain open.

## Linux source-recipe checkpoint

`tools/build_spice_stack.py` and `.github/workflows/spice-research.yml` reproduce the observed source-build settings for pinned ngspice47, Trilinos16.1 and Xyce7.10. They run native callback RC, stepwise RC and HB RLC/cubic checks, with closed-form oracles and retained output. The Xyce abs compatibility fix is context-checked; the ngspice declaration fix is applied to its generator input. No foundry models or OSDI compiler are downloaded by this subset. Linux execution remains pending until the workflow completes.

This uses the existing research candidates and is not a production dependency admission or binary-release recipe. The explicit `--research-candidates` guard prevents presenting it as an approved installer; ADR002 still requires the selected-source/runtime license review before merge/adoption. It records distro package versions, but does not claim a fully locked apt environment. Passing this subset will not close original IHP conformance.

First Linux run41768558047 failed before compilation because cfunc.mod contains non-UTF8 bytes. [Failure excerpt](../../verification/results/spice-linux-first-failure.log) is retained. The declaration patch now operates on bytes, preserving the upstream payload; retry is pending.
