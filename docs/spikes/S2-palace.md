<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S2 — Palace reuse investigation

Date: 2026-11-02. Result: **PASS for documentary decision; no successful linkage experiment claimed.**

The criterion is a documented reuse decision supported by evidence. Recommend a subprocess reference adapter and study of algorithms, with MFEM as the candidate infrastructure for custom physics. Do not integrate Palace internals yet: the integration rubric requires demonstrated stable embedding, benchmarks and lossless data mapping, which have not passed. This is an engineering choice, not a legal requirement or a claim that linking is impossible.

## Primary evidence and correction to the handoff

- [Palace CMake](https://github.com/awslabs/palace/blob/main/palace/CMakeLists.txt) defines `LIB_TARGET_NAME libpalace`, calls `add_library`, and installs both executable and library targets. Therefore the plan's characterization must not become a claim that Palace has no library. Include paths refer to its source/generated trees; the inspected installation section only expressly installs qfunction headers. No supported public SDK contract was established by this inspection.
- [Changelog](https://github.com/awslabs/palace/blob/main/CHANGELOG.md) identifies 0.18.1 dated 2026-09-21 and warns of changing pre-1.0 interfaces. It records Floquet phase-delay periodic boundaries and subsequent fixes. Periodicity is already implemented, contrary to the preliminary roadmap premise.
- [Current boundary guide](https://awslabs.github.io/palace/dev/guide/boundaries/) still says PML is not implemented; [issue 916](https://github.com/awslabs/palace/issues/916) tracks it. This supports investigation of a custom PML layer but does not establish that all dispersive/plasmonic physics is absent.
- [Stable overview](https://awslabs.github.io/palace/stable/) documents a 2D mode analysis, EPR, eigen/driven/transient/statics, AMR and GPU features. Reimplementing all of these without benchmarking would waste existing evidence.
- [Repository license](https://github.com/awslabs/palace/blob/main/LICENSE) is Apache-2.0. Any copied implementation requires upstream notices, attribution, change notices and a dependency audit, not just citing the project.

## Rubric

| Gate | Evidence | Result |
|---|---|---|
| License | Apache-2.0 project license; transitive audit outstanding | Candidate |
| Stable embeddable API | Internal library exists; no public stability contract demonstrated | Not met |
| Maintenance within ~12 months | 0.18.1, 2026-09-21 | Met |
| HeaviSolve benchmark tests | Not executed | Not met |
| Lossless data mapping | No adapter tested | Not met |

No source was copied. No Palace benchmark numbers were generated. The lead should record these factual corrections in the deviation ADR before architecture lock. A future linking spike should pin the source, construct a minimal external client, install into a clean prefix, and exercise cavity and wave-port outputs with provenance. Reconsider integration only after those tests pass.
