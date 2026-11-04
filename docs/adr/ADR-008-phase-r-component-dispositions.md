<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-008: Phase R component decisions and admission boundaries

Status: accepted research decisions; remote-main integration pending. Date: 2026-11-04.

## Decision and explicit deviation

Accept C++20 as the implementation language under ADR001, AGPL-3.0-or-later and DCO under ADR002, and the co-primary SPICE target under ADR003. Accept ADR004–007 corrections and the walking-skeleton design self-review. These are M0 decisions, not a claim that the production application or every candidate integration exists.

Section0.2 says to integrate only if license, stable API, recent maintenance, benchmarks and lossless data mapping all pass, otherwise build custom. Apply that rule strictly to **actual component admission**. Where research identifies a useful framework but leaves an admission requirement open, retain it as a blocked candidate rather than immediately write a replacement framework. This is an explicit deviation from the literal immediate “otherwise build custom” instruction: replacing Qt, VTK or RPC libraries before a bounded admission check would enlarge scope without evidence of benefit. For SPICE, section4.7 independently prohibits writing a replacement engine. Failed admission never becomes a pass through process isolation or a future-work promise.

No new dependency or license exception is admitted by this ADR. `dependencies.toml` retains its exact scopes; an approved direct source grant is not approval of every installed module or transitive graph. Unknown licenses still fail closed. Resolve admission before the corresponding production dependency is added, not merely before release.

## Component dispositions

The [solver survey](../research/solver-survey.md), its maintenance evidence, and [PDK survey](../research/pdk-survey.md) supply primary-source references. Spike reports retain measured outcomes and scope. The table records which parts of the integration rubric remain unproved rather than marking future work as complete.

| Component | Decision and evidence | Admission scope / unresolved rubric terms |
|---|---|---|
| C++20 / Rust | C++20, ADR001:134/145 versus86/145 suitability; independent native slab and equivalent C ABI bindings pass Linux/macOS CI | No language speed winner; engineering hours and full nanobind/PyO3 comparison unmeasured. Rust research prototype is not a second production language |
| MFEM | Selected infrastructure for custom physics; S1 and serial Poisson/cavity CI pass, source grants and exact support-package reviews recorded | Existing benchmark-only builds are admitted at their recorded scope. Production wrappers must test material/boundary/field mapping and pin their exact configuration; no general Maxwell verification claim |
| Palace | Optional reference/study; custom physics on MFEM | S2: internal library exists and project maintained, but public stable embedding and lossless application mapping unproved. No source copied |
| Gmsh / layered extrusion | Preferred tetrahedral candidate plus custom native extrusion; S4 quality/Jacobian/volume/H(curl) checks pass locally | Direct grant reviewed; production material/boundary conversion and selected dependency closure still require admission and CI |
| Netgen | Alternative/reference | S4 uses Netgen optimization through Gmsh, not a separately integrated Netgen library |
| Qt6 / VTK | Selected GUI/field-viewer direction; S5 native embedding and cut plane work | Selected modules/runtime graph and production API integration remain gated. Measured repaint throughput does not establish compositor presentation FPS |
| gRPC/protobuf / mapped arrays | Preferred control and local-array direction, S7 native processes/checksum/progress pass | Choice follows generated service fit, not a statistically supported speed comparison. Runtime closure, lifecycle, cancellation and descriptor validation remain production gates |
| ZeroMQ/FlatBuffers | Tested alternative | No measured basis to reject it for speed; not default, no new production adoption |
| KLayout | Preferred isolated layout/PCell bridge candidate; S6 IHP/SiEPIC geometry round trips pass | Geometry equality alone does not prove all metadata, hierarchy or PCell semantics. Pin exact bridge/data contract, module grant and runtime dependencies before integration |
| gdstk | Reject as default for tested SiEPIC OASIS conversion | S6 geometry changed. Retain failed result and reference role; not a claim every format/input fails |
| Clipper2 | Reject archived candidate as default | Recent-maintenance rubric fails. Evaluate KLayout polygon operations or a maintained alternative before adopting boolean infrastructure; round-trip evidence alone does not validate booleans |
| ngspice / Xyce | Co-primary targets, ADR003 OutcomeB;98/160 versus94/160, below15-point lead | Full integration withheld: original IHP conformance fails, ngspice mixed-license admission and Xyce transitive review unfinished. Research harnesses are not production adapters |
| OpenVAF / ADMS | Engine-specific compiler-route targets | OSDI locally tested for ngspice; do not imply Xyce uses OSDI. Exact compiler/model grants and Xyce plugin route need executable validation |
| Other physics families | Native custom layers, with optional survey-listed cross-check references | No untested reference is adopted as a backend. Each implementation milestone applies its own closed-form/convergence and dependency gates |
| PDK importers | User-defined process schema; public pinned IHP/SiEPIC/generic targets | External fixtures retain file-specific grants. ECL-2.0 model subtree excluded under current policy; gated/NDA data user-supplied only |

## Consequences and checkpoint review

Phase R now has a recorded disposition for each investigated component. M0 can report failed experiments without hiding them or requiring completion of M7. This resolves the decision-deliverable review, but not the remote integration exit criterion. The revised acceptance workflow must pass on the review branch, outputs must be retained, and ADR integration must actually occur before M0 is declared complete. No M1 code is added.

The next checkpoint begins with the narrowly selected M1 dependency configuration and its admission checks, then the capacitor vertical slice described in the [walking-skeleton plan](../developer/walking-skeleton-plan.md). Unresolved SPICE conformance stays tracked for M7; it does not become a hidden prerequisite for electrostatic geometry/API work. The release SBOM and binary redistribution audit remain M10 deliverables, separate from the earlier mandatory dependency admission.
