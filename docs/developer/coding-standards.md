<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors
SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Coding standards

C++20 is selected by ADR001/008. Production solvers never use Python. Python is limited to bindings, orchestration and independent test oracles. Use RAII, explicit ownership, checked dimensions, SI internal units, deterministic seeds and structured errors. No silent fallback when a requested engine capability is absent. New C++ builds with -Wall -Wextra -Wpedantic -Werror. Format with clang-format; add ASan/UBSan checks and separate TSan jobs when threaded code arrives.

Use exp(+j omega t); passive dielectric loss has Im(epsilon) <= 0 under this convention. The plan §5.2 opposite sign is corrected in ADR-004. Results record source revision, dependency versions, process/mesh hashes, settings and host. Test analytical oracles independently and record convergence, not just one resolution. Never relabel an unavailable test PASS.

Phase R decisions are recorded; M1 implementation remains gated on the M0 exit report. The GUI and Python must share the versioned API; solvers run in isolated workers. All processes are user-defined; importers generate process specifications without requiring a particular PDK. Review changes in small signed-off commits.
