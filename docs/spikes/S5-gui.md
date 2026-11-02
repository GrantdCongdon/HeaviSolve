<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S5: GUI feasibility

Overall: **BLOCKED / NOT PASS**.

CMake prerequisite probe requests Qt6 Widgets/OpenGLWidgets and VTK GUISupportQt/RenderingOpenGL2/FiltersCore. [Actual configure log](../../verification/results/s5-configure.log) fails at missing Qt6 package configuration. VTK is therefore not reached by this configure; its availability is not inferred from that failure. No shell,10k scene, fps result or VTK field cut-plane was produced. Do not report60fps based on item creation or offscreen timing.

Next: isolated conda/Qt SDK environment with matching Qt major version in VTK, build C++ docking/QGraphicsView/QVTK widget, measure warmed pan/zoom frame times on a visible display and capture field cut-plane output. Include renderer, resolution, device-pixel ratio, hardware and scene distribution. Offscreen rendering is a correctness/screenshot check, not a substitute for visible-display performance. Qt remains provisional. The installed KLayout application does not establish a usable Qt6 developer SDK.
