<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S6: layout feasibility

**LOCAL round-trip and viewport experiments completed; integration and hosted CI remain pending.** KLayout passes the tested real-PDK conversions. gdstk fails one SiEPIC OASIS conversion. The million-polygon viewport was actually rendered; its timing is a repaint measurement, not a display presentation rate.

The existing isolated photonics environment provides gdstk 1.0.0 and KLayout 0.30.9 native geometry libraries through Python bindings. Python orchestrates geometry tests and contains no solver implementation. Earlier synthetic annulus and 100-cell round trips remain in [raw output](../../verification/results/s6-layout.log).

## Public fixture provenance

The fixtures remain outside the repository in `.work/s6`; no PDK data is bundled. Exact paths were recovered by matching each local file's Git blob hash against the pinned repository tree.

| Fixture | Pinned public source | SHA-256 |
|---|---|---|
| SiEPIC ring | [SiEPIC-Tools, Examples/RingResonator.gds](https://github.com/SiEPIC/SiEPIC-Tools/blob/363fbb52eefa8669100499ab531d3fe7befc4867/Examples/RingResonator.gds), repository MIT license | a4c920a9035a09b43982d4a0350c88e274629b2fbb3d127baccb504a42fc994f |
| IHP standard cells | [IHP Open PDK, sg13g2_stdcell.gds](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds), repository Apache-2.0 license | ab9f2802c78935d4463093c24860f9d3f244057a839179fb19fc0243a18cf3f4 |

## Measurements and selection

`verification/layout/pdk_roundtrip.py` writes each fixture through each engine as GDS and OASIS, then compares database units, layer sets, cell names and merged filled regions with the same KLayout reader. The required geometry XOR area is exactly zero in database units. This reader-based test does not establish complete format semantics or independent-reader equivalence.

| Fixture | gdstk GDS | gdstk OASIS | KLayout GDS | KLayout OASIS |
|---|---|---|---|---|
| SiEPIC: 18 cells, 6 layers | PASS | FAIL: 19 cells, XOR area 3,184,242,529 dbu² | PASS | PASS |
| IHP: 84 cells, 15 layers | PASS | PASS | PASS | PASS |

[Raw output](../../verification/results/s6-pdk-roundtrip.log) retains gdstk property warnings. Its SiEPIC OASIS conversion exposes the reserved `$$$CONTEXT_INFO$$$` cell as ordinary geometry, whereas the GDS reader treats it as context metadata. The test therefore selects KLayout for these PDK round trips. The earlier cell-name diagnostic is [retained](../../verification/results/s6-pdk-roundtrip-diagnostic.log). PCell regeneration, all properties, text semantics and exact hierarchy relationships are not covered.

Native Clipper2 1.5.4 produces intersection area 50, union 150 and difference 50 for overlapping 10-by-10 squares; [output](../../verification/results/s6-clipper.log). This is a small boolean smoke test, not a robustness comparison across process layouts.

The native Qt/VTK spike rendered 1,000,000 distinct polygon items at a 1078 × 717 viewport and device-pixel ratio 2. Across 240 measured frames it recorded 4.1146462919999998 seconds, 58.328221423704335 viewport repaints/s, 8.7015829999999994 ms p95 paint time and 2344 cut-plane cells. See [output](../../verification/results/s6-million-viewport.log) and [screenshot](../../verification/results/s6-million.png). The executable returned failure against its 60-fps threshold; the plan explicitly assigns 60 fps to S5's 10k case and only requests a 1M viewport test for S6. We retain the failure rather than relabeling it. Source changes to panel sizing followed this run; capture-time hashes are not exact run-time GUI hashes.

A subsequent run after widening the VTK panel reduced the schematic viewport to 798 × 717, with the same device-pixel ratio 2 and one million polygons. It recorded 240 frames in 3.515754625 seconds: **68.264149691618485 repaints/s**, p95 paint time 7.5314579999999998 ms, and 2344 cut-plane cells; the executable's 60-fps check passed. See [revised output](../../verification/results/s6-million-revised.log) and [screenshot](../../verification/results/s6-million-revised.png). No renderer optimization was applied between these cases; the viewport area changed. Runs used an Apple M1 with 8 CPU cores, 8 GPU cores and 16 GB RAM while builds could be active, so they are not controlled idle-machine comparisons. Neither measures compositor presentation rate.

[gdstk](https://github.com/heitzmann/gdstk/blob/main/LICENSE) and [Clipper2](https://github.com/AngusJohnson/Clipper2/blob/Clipper2_1.5.4/LICENSE) use BSL-1.0; [KLayout](https://github.com/KLayout/klayout/blob/master/LICENSE) uses GPLv3 terms. Full integration still needs the ADR rubric, maintenance confirmation and transitive audit. Preserve the required out-of-process Python PCell bridge. [Evidence provenance](../../verification/results/s4-s6-s7-provenance.json) records hashes.
