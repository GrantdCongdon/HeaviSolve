<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors
SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-004: evidence-based corrections to the director plan

Status: accepted corrections; architecture remains gated. Date: 2026-11-02.

1. With exp(+j omega t), positive conductivity contributes -j sigma/omega to complex permittivity. Therefore a passive local dielectric has Im(epsilon) <= 0, reversing §5.2. Derivation: Ampere current sigma E + j omega epsilon E = j omega (epsilon - j sigma/omega) E. Add convention tests in M1.
2. Palace has a libpalace target and Floquet phase-delay periodic support; it is not categorically un-linkable and that boundary capability is not future-only. Stable API, PML and dispersive coverage require separate evidence. See S2 and R1 primary links.
3. Femwell is GPL-3.0 rather than the plan's MIT label; use only after exact license audit. See R1.
4. CORNERSTONE public cspdk is distinct from gated foundry data. Import/redistribution is assessed per artifact. See R3.
5. Xyce's documented IHP route uses ADMS-generated plugins, while ngspice uses OpenVAF/OSDI. Do not promise OSDI on both without an executable test. See ADR-003.
6. Missing measurements keep M0 open; preliminary research scores must never be presented as completed language or SPICE benchmarks. No architecture lock or M1 implementation is authorized by an incomplete spike.

7. IHP's top-level Apache-2.0 does not cover every model: R3 found ECL-2.0 under r3_cmc. This is outside the current allow-list and remains excluded pending a separate policy decision. The inspected ngspice HBT library is VBIC, not an assumed HICUM binding. Google GF180MCU is archived; select and audit its maintained successor before importer adoption.
8. Gmsh's linking exception is limited to named libraries, not a blanket arbitrary-code exception. gdstk is BSL-1.0. Both facts were checked against upstream license files.
