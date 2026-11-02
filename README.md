<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors
SPDX-License-Identifier: CC-BY-SA-4.0 -->

# HeaviSolve

Integrated plasmonic, photonic, quantum-optic and BiCMOS design and simulation.

**Status: M0 research in progress; not a verified simulator.** Original code is AGPL-3.0-or-later; documentation is CC-BY-SA-4.0. No restricted PDK data is included.

Build the foundation checks:

```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build -L foundation --output-on-failure
```

M0 numerical checks additionally require MFEM 4.8 with LAPACK:

```sh
cmake -S . -B build -DHS_ENABLE_MFEM_SPIKES=ON -DMFEM_DIR=/path/to/mfem/lib/cmake/mfem
cmake --build build
ctest --test-dir build -L m0 --output-on-failure
```

See [task list](docs/milestones/M0-tasks.md), [report](docs/milestones/M0-report.md), and [contribution rules](CONTRIBUTING.md).
