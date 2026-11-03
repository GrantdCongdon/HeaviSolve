<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S5: GUI feasibility

Local repaint-throughput criterion PASS on a visible Cocoa window; compositor presentation rate and hosted GUI CI remain unmeasured. Qt 6.12.0 / VTK 9.7.1 C++ docking shell contains 10,000 QGraphicsScene polygons and a QVTKOpenGLNativeWidget showing a manufactured scalar-field cut plane (2,344 cells). This is an M0 experiment, not the M1 application or shared-API implementation.

The native harness performs 60 warm-up updates followed by 240 measured pan/zoom updates, synchronously repainting the viewport. On an Apple M1 MacBook Pro (8 CPU cores, 8 GPU cores, 16 GB RAM), the corrected layout at 798×717 logical pixels and device-pixel ratio 2 measured **75.798814882813176 repaints/s**, p95 paint duration **5.209625 ms**. [Raw result](../../verification/results/s5-shell-idle.log), [screenshot](../../verification/results/s5-shell-idle.png). The file's historical “idle” label does not establish controlled system load: dependency builds were running during this session. No hardware identifiers are included in committed evidence.

The same corrected layout earlier measured **56.15977 repaints/s**, below the 60 criterion, during dependency compilation; [failure retained](../../verification/results/s5-shell-revised.log). The original wider viewport measured 72.72454 repaints/s, but its field dock was too narrow; [original result](../../verification/results/s5-shell-run-visible.log). Neither rerun erases that variability. The screenshot was visually inspected: explorer, geometry and full-width colored cut plane are visible. Repaint throughput is not a measurement of distinct compositor-presented frames; strict display-fps certification remains open.

Reproduce with `cmake -S verification/gui -B .work/gui-build -DCMAKE_PREFIX_PATH=<Qt6-and-VTK-prefix>`, build, then run `.work/gui-build/gui_spike small verification/results/s5-shell.png` on a visible desktop. A native desktop session is required; restricted execution initially failed to connect to Cocoa. The original missing-Qt configuration failure remains [stored](../../verification/results/s5-configure.log).

Qt/VTK remain integration candidates pending the complete component/license gate. The large conda development environment is not an approved redistributable runtime. The scene uses deterministic filled rectangles; real schematic wires, text, selection, editing, accessibility and the shared GUI/Python API belong to later milestones.
