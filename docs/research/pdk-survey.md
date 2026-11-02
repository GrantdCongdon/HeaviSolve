<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# R3: PDK and process survey

Research date: 2026-11-02. This is an importer requirements survey, not a claim of tested PDK support. No PDK files were bundled. Public sources were inspected through web and GitHub read tools. No foundry login, registration, or restricted download was attempted.

## Recommendation and evidence limits

Start with IHP SG13G2, SiEPIC EBeam, and the gdsfactory generic process. Keep the process schema independent of all three. Import geometric layer maps separately from physical material models: a GDS layer/color is not a dielectric function, and a fabrication cross-section is not a complete optical-dispersion dataset. Require source provenance, units, temperature/frequency ranges and explicit missing-data diagnostics. Never invent optical constants from electronic process parameters.

The IHP main revision inspected is [`5e6d592e4002946a4616f798c357f0f3c06cf3b6`](https://github.com/IHP-GmbH/IHP-Open-PDK/commit/5e6d592e4002946a4616f798c357f0f3c06cf3b6), committed 2026-09-01. This is a **research pin**, not a tested importer pin. All other mutable links below need a revision pin before fixtures or importer tests are approved. There are currently **zero tested importer revisions**.

## Survey

“Unknown” means not established by inspected public primary sources. An agreement-gated kit is treated as restricted even where the public page does not establish whether the agreement is technically an NDA. Public code's license does not automatically cover a different portal download or every nested model.

| PDK / platform | Redistribution class and license evidence | Layer stack / material availability | PCells and layout | Compact models | EM simulation material | Required importer and decision |
|---|---|---|---|---|---|---|
| IHP SG13G2 | Open repository, Apache-2.0 top level; file-level exceptions exist; preview/alpha status [I1–I4] | Public process specification, layout rules, BEOL stack; RF electrical parameters; optical dispersion completeness not established | KLayout `.lyp`/`.lyt`, Python PyCells with compatibility API, GDS | Separate ngspice/Xyce models, Verilog-A PSP103; inspected ngspice HBT is **VBIC** [I5–I7] | openEMS examples, measurements; current tree also has Palace integration [I1,I3] | First BiCMOS target: layer/stack, units and material provenance; per-engine include bindings; isolated PCell bridge. Pin entire recursive dependency graph before use |
| IHP SG13CMOS5L | Open variant announced by IHP in 2026; exact file inventory/license audit outstanding [I2] | Reduced metal-stack CMOS subset, not a substitute for BiCMOS HBT support | Tool files need separate audit | Device subset must be discovered from variant, not inherited from SG13G2 assumptions | Not evaluated | Future extension to IHP importer; no tested support |
| IHP SG13G3 | **Unknown** public open-PDK availability; no open release established in inspected IHP sources | Unknown | Unknown | Unknown | Unknown | No compatibility claim; user-supplied process route until evidence exists |
| SiEPIC EBeam PDK + SiEPIC-Tools | Open, MIT for both inspected license files [S1,S2] | Public technology/layout files; a complete broadband material dataset has not been established | KLayout Python PCells, GDS libraries, `.lyt` technology; Tools supplies extraction/connectivity workflows | EBeam compact-model library and INTERCONNECT workflow; exact portable table inventory requires a pinned audit [S3] | Layout verification examples; no independently tested EM stack in this session | First photonic target: `.lyp/.lyt`, layer stack, PCell metadata and S-parameter tables where available. Run Python PCells in isolated bridge, not solver core |
| gdsfactory generic PDK | Open, MIT [G1] | Explicit LayerStack with thickness, z-position, material labels; cross-sections [G2] | Python component factories and cross-section functions; GDS/OASIS export | Generic/model integrations are references, not a C++ solver implementation | Simulation integrations exist; no validation of fabricated process accuracy implied | Import declarative geometry/process export through an isolated Python bridge. Require material source metadata and no silent layer loss |
| gdsfactory community PDKs | **Per repository**, not universally MIT merely because gdsfactory is MIT [G3] | Depends on kit | gdsfactory components/cross-sections, sometimes other tool assets | Depends on kit | Depends on kit | Reuse generic bridge only after individual manifest/license audit. Public examples include cspdk; gated foundry packages excluded |
| CORNERSTONE public `gdsfactory/cspdk` | **Open, MIT**, checked license [C1]; correction to blanket registration classification | Documented layer stack and multiple silicon/SiN/Ge variants [C2] | gdsfactory cells | SAX models advertised for each variant; Python reference only | Public Meep directional-coupler/MMI notebooks [C2] | Optional open photonic target through generic bridge; audit actual tables/file notices before redistribution |
| CORNERSTONE portal/tool-specific kits | Open-access with registration/agreement terms to inspect; **not redistributable by assumption** [C3] | Foundry design guidance is public; portal assets not fetched | IPKISS, GDSFactory, Cadence, L-Edit variants advertised | Wave Photonics S-parameters advertised | Unknown for gated distribution | User-supplied path only; do not mix public cspdk rights with portal rights |
| SkyWater SKY130 | Open Apache-2.0 repository [K1] | Public process-stack diagram, GDS layer definitions and electrical design rules [K2]; optical material completeness unknown | Foundry device/layout libraries; tool/PCell formats depend on chosen open tool distribution | SPICE device models; exact engine compatibility and version need tests | No openEMS fixture validated here | Electronics-only follow-up importer: layer map/stack and engine-specific model bindings. Do not claim photonic foundry support |
| GlobalFoundries GF180MCU | Open Apache-2.0 release [F1,F2]; Google repository archived 2026-09-23 [F1] | Public custom-design/process documentation; experimental-preview warning [F3] | Primitive/layout libraries and tool decks; exact PCell implementation needs pinned audit | SPICE models in ecosystem; no engine run in this session | No EM example validated | Follow-up CMOS importer. Select maintained successor/source and pin before adoption; archived root is not evidence of current maintenance |
| AIM Photonics | Agreement/registration-gated. Public access page requires executed agreements; different libraries have different development/commercialization terms [A1,A2] | Public stack overview, detailed kit gated | Component libraries and vendor scripts advertised; exact formats private/uninspected | Models within licensed kit; portable formats unknown | Unknown | User-supplied path only; generic layer/stack/model mapping. No kit bundling, no inferred blanket redistribution rights |
| imec iSiPP | Agreement-gated; public design-kit agreement offered [P1] | SOI photonics and heater/interconnect overview public; detailed material data uninspected | Vendor-specific kit; public Luceda catalog advertises IPKISS layout/model views [P2] | Vendor simulation models; portable format unknown | Unknown | User-supplied path and explicit metadata export; no restricted files in tests |
| GlobalFoundries photonics / GF Fotonix | Restricted pending exact agreement; no open license established [P3] | Public platform description; customer PDK includes device-simulation technology files | Vendor ecosystem (Ansys/Cadence/Synopsys); exact PCell format uninspected | Electro-photonic kit; exact portable formats unknown | Technology files advertised, not downloaded | User-supplied path only. Do not confuse open GF180MCU with GF Fotonix |
| LIGENTEC | Agreement-gated: signed Design Kit License Agreement required [P4] | Platform information may be shared before full PDK; material tables uninspected | Vendor components for Luceda/Synopsys/Lumerical/GDSFactory | Validated simulation models advertised, exact format uninspected | Unknown | User-supplied path only; preserve platform/version and model capability diagnostics |
| LioniX / TriPleX | Restricted pending agreement inspection; public MPW manual advertises PDK [P5] | Platform overview public; detailed dispersion/process tables uninspected | Vendor PDK formats depend on delivery; not inspected | Not inspected | Not inspected | Generic user-supplied process and model paths only |
| Custom plasmonic / superconducting / TFLN | User-owned data; rights follow each supplied dataset, not HeaviSolve's code license | User-defined stack and constitutive models; no fabricated foundry constants | Native declarative PCells; optional isolated Python geometry | User models and measured/FEM tables, engine binding explicit | HeaviSolve examples must use explicitly licensed or original synthetic inputs | Native process loader plus CSV stack / `.lyp` / `.lyt` / GDS-layer import; provide templates marked illustrative and uncalibrated |

## Corrections requiring integration ADR

1. **CORNERSTONE is distribution-specific.** Public `cspdk` is MIT; access-gated downloads remain excluded. Update the Appendix B classification without weakening the no-restricted-data rule.
2. **IHP is not uniformly Apache-2.0 at every nested file.** [`verilog-a/r3_cmc/LICENSE.txt`](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.tech/verilog-a/r3_cmc/LICENSE.txt) identifies **ECL-2.0**, absent from the plan's allow-list. Keep this component unapproved until ADR-002 explicitly reviews it; public availability alone does not pass policy. PSP source has separate upstream copyright notices too. Whole-tree copying is not approved by this survey.
3. **HBT model identity must be discovered.** The inspected SG13G2 ngspice HBT library identifies VBIC and a level-9 device, rather than the plan's tentative HICUM-class assumption. Keep circuit bindings engine- and version-specific.
4. **Platform evolution:** IHP advertises SG13CMOS5L; the checked GF180MCU Google repository is archived. Neither fact authorizes an untested importer or a substitute for the requested SG13G2 tests.

## Importer acceptance contract (proposed for M1)

- Each output records upstream revision, source-file hashes, parser version, units, material-source citations, engine bindings and unsupported constructs.
- Preserve GDS layer/datatype and original names; report ambiguity instead of silently collapsing purposes.
- Validate stack z-extents, thickness and operation ordering against source; do not derive physical thickness from a display color.
- Never execute PCells in the backend process. The isolated bridge exports geometry and metadata through the same documented process/API boundary.
- Keep private paths and model contents out of CI artifacts. Open fixtures require per-file redistribution review; reference fixtures by pinned revision where practical.
- The support matrix remains empty until import round-trip and geometry/material tests pass with stored CI evidence. “Surveyed” is separate from “supported.”

## Primary-source register

All accessed 2026-11-02; mutable pages are research evidence only, not release locks.

- I1: [IHP repository README](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/main/README.md) — process, files, preview warning, top-level license.
- I2: [IHP Open Source Design Enablement](https://www.ihp-microelectronics.com/services/research-and-prototyping-service/open-source-design-enablement) — SG13G2/SG13CMOS5L, alpha status.
- I3: [IHP pinned tree](https://github.com/IHP-GmbH/IHP-Open-PDK/tree/5e6d592e4002946a4616f798c357f0f3c06cf3b6) — inspected recursively with GitHub API; openEMS, KLayout, ngspice/Xyce, Verilog-A paths.
- I4: [IHP license](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/LICENSE).
- I5: [PSP103 Verilog-A](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.tech/verilog-a/psp103/psp103.va) — upstream copyright, model version, Xyce conditional module name.
- I6: [ngspice HBT library](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_hbt_mod.lib) — Apache notice and VBIC model.
- I7: [IHP documentation](https://ihp-open-pdk-docs.readthedocs.io/en/latest/).
- S1: [SiEPIC EBeam license](https://github.com/SiEPIC/SiEPIC_EBeam_PDK/blob/master/LICENSE.md).
- S2: [SiEPIC-Tools license](https://github.com/SiEPIC/SiEPIC-Tools/blob/main/LICENSE.md).
- S3: [SiEPIC-Tools README](https://github.com/SiEPIC/SiEPIC-Tools) and [EBeam repository](https://github.com/SiEPIC/SiEPIC_EBeam_PDK).
- G1: [gdsfactory license](https://github.com/gdsfactory/gdsfactory/blob/main/LICENSE).
- G2: [gdsfactory PDK documentation](https://gdsfactory.github.io/gdsfactory/notebooks/08_pdk/).
- G3: [gdsfactory PDK catalog](https://github.com/gdsfactory/gdsfactory).
- C1: [cspdk license](https://github.com/gdsfactory/cspdk/blob/main/LICENSE).
- C2: [cspdk documentation](https://gdsfactory.github.io/cspdk/) — layer stack, model and Meep notebook links.
- C3: [CORNERSTONE design guidelines](https://cornerstone.sotonfab.co.uk/wp-content/uploads/2025/07/CORNERSTONE-Silicon-Nitride-MPW-11-Design-Guidelines-1.pdf) — portal and vendor access routes.
- K1: [SkyWater repository](https://github.com/google/skywater-pdk) and [inspected license](https://github.com/google/skywater-pdk/blob/main/LICENSE).
- K2: [SKY130 layer reference](https://skywater-pdk.readthedocs.io/en/main/rules/layers.html) — current docs link to FOSSi Foundation source.
- F1: [GF180MCU repository](https://github.com/google/gf180mcu-pdk) and [inspected license](https://github.com/google/gf180mcu-pdk/blob/main/LICENSE).
- F2: [Google/GF release announcement](https://opensource.googleblog.com/2022/08/GlobalFoundries-joins-Googles-open-source-silicon-initiative.html).
- F3: [GF180MCU documentation](https://gf180mcu-pdk.readthedocs.io/en/latest/).
- A1: [AIM PDK access](https://www.aimphotonics.com/pdk).
- A2: [AIM agreements](https://www.aimphotonics.com/agreements).
- P1: [imec IC-Link silicon photonics](https://www.imeciclink.com/en/asic-fabrication/si).
- P2: [Luceda design-kit catalog](https://www.lucedaphotonics.com/luceda-design-kits).
- P3: [GF Fotonix platform/PDK description](https://gf.com/blog/next-gen-gf-fotonix-redefining-flexibility-bandwidth-upgrades-full-turnkey-support/).
- P4: [LIGENTEC PDK access](https://www.ligentec.com/faq/how-to-get-pdk/).
- P5: [LioniX MPW manual](https://www.lionix-international.com/wp-content/uploads/2022/08/Briefings-MPW-manual.pdf).
