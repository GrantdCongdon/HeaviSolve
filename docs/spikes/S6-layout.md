<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S6: layout feasibility

Overall: **PARTIAL / NOT PASS**.

Existing isolated photonics environment provided gdstk1.0.0 and KLayout0.30.9 native geometry libraries through Python bindings. The harness contains no solver code. Synthetic annulus boolean plus100 repeated cells round-tripped GDS and OASIS through both libraries. Areas in [raw output](../../verification/results/s6-layout.log) agree within the predeclared1e-4 relative tolerance. Before quantization:5968.7645999999904 square micrometres; GDS after gdstk:5968.7709999999925; OASIS:5968.7646000000032.

A hierarchical million-instance reference was created, but was NOT flattened, drawn or timed as a viewport benchmark. Its creation time is not evidence of rendering speed. No IHP/SiEPIC real-layout roundtrip or Clipper2 direct comparison was run. Consequently the plan's S6 gate does not pass.

[gdstk license](https://github.com/heitzmann/gdstk/blob/main/LICENSE) is BSL-1.0; [KLayout](https://github.com/KLayout/klayout/blob/master/LICENSE) GPLv3 family. Both are candidates under ADR-002; upstream bundled dependencies still require audit. Next: license-cleared pinned IHP/SiEPIC fixtures, layer/hierarchy/units/property equality checks, native C++ integration cost, Clipper2 comparison and measured1M-polygon visible viewport. Preserve the required out-of-process Python PCell bridge independently of the geometry-library decision.
