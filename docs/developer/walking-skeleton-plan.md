<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# M1 walking-skeleton design for M0 self-review

Design only. M1 implementation must wait for the M0 exit report.

## Smallest complete path

A user-defined, versioned process specification supplies material properties, units and layer thicknesses. A simple capacitor example generates geometry and a mesh, then submits an electrostatics job to a separate native C++ worker. The worker returns capacitance, field data and provenance. A minimal Qt shell displays progress and the result. The Python client submits the identical request and receives the same result through the same versioned service API.

Start with the parallel-plate ideal-boundary and coaxial analytic cases in VER-ES-01. Separate idealized boundary tests from finite structures with fringing fields; never compare the latter against an inappropriate ideal formula. Use the established MFEM build and independent test oracles. Python performs orchestration and result analysis only.

## Contract and boundaries

The shared service exposes project/process loading, validation, simulation submission, job status/cancellation and result retrieval. Define request/result schema versions, SI values, stable identifiers, diagnostics and capability metadata before either frontend adds private calls. The GUI command registry invokes this service rather than solver internals. Python uses the same protocol through a thin client; native array bindings must document ownership and lifetime.

Use structured RPC for control/progress and explicit shared-memory descriptors for local large arrays, with generation IDs and release/cleanup rules. The S7 checksum test demonstrates a feasible local path, not an implemented production memory-lifecycle protocol. Validate sizes, types and offsets before mapping. Remote transfer and GPU execution remain outside this slice.

The server owns job lifecycle and provenance. A worker failure marks its job failed, preserves diagnostics, releases mappings, and leaves the GUI/server responsive. Cancellation must terminate work and clean up deterministically. Record code/source versions, process/mesh/input hashes, solver settings and numerical status with each result.

The GUI initially needs activity/sidebar navigation, tabbed process/result views, command palette, job/output/problems panel and unit-aware properties. Use the tested Qt/VTK direction; do not build the full schematic/PCell editor in the first slice. Render one mesh and field cut plane, and expose every operation through the shared API.

## M1 acceptance and exit checks

- Process-schema round trip, invalid references/units and deterministic hashing.
- Extrusion volumes/z extents and mesh Jacobian/quality checks.
- VER-ES-01 within the declared TierA tolerance, with refinement toward1e-6 and theory-consistent convergence. Store output in CI; no verification claim before it passes.
- GUI/API requests yield identical result provenance and numerical values within declared tolerances.
- Offscreen shell screenshot and command-registry tests; visible rendering smoke check where available.
- Worker-crash and cancellation tests leave GUI/server usable and release large-array resources.
- Public pinned IHP stack import visible in3D at M1 exit. Fixtures remain externally downloaded with explicit licensing; private PDKs are user-supplied only.

## Self-review checklist

- [x] Native solvers only; Python remains bindings/orchestration/oracles.
- [x] GUI and Python share one service contract.
- [x] Process definitions are user-defined and PDK-agnostic.
- [x] Solver correctness has independent closed forms, convergence and stored-CI requirements.
- [x] Process isolation and explicit result ownership address crash/lifetime risks.
- [x] Scope is a capacitor vertical slice; no dependency on unresolved M7 SPICE conformance.
- [x] No restricted PDK data or unapproved production dependency is introduced by this design.
- [x] M1 acceptance and exit map to the director's section12.

Design self-review: approved for the proposed M1 checkpoint, conditional on M0 exit. This does not begin M1 or certify any unimplemented feature.
