<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors
SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ADR-002: licensing and dependency admission

Status: accepted policy; transitive binary-distribution audit remains open. Date: 2026-11-02.

Original code/examples: AGPL-3.0-or-later. Documentation: CC-BY-SA-4.0. Contributions use DCO 1.1, no CLA or assignment. SPDX headers and REUSE lint are mandatory. Upstream license texts are unmodified and covered by sidecars/REUSE metadata.

Allow expressions built from MIT, BSD-2-Clause, BSD-3-Clause, ISC, Zlib, BSL-1.0, Apache-2.0, MPL-2.0, LGPL-2.1-or-later, LGPL-3.0-only/or-later, GPL-2.0-or-later, GPL-3.0-only/or-later and AGPL-3.0-only/or-later, subject to obligations and file-level exceptions. GPL-2.0-only, proprietary, non-commercial, field-of-use and SSPL licenses are denied. Unknown expressions fail closed. OR alternatives must select an allowed branch explicitly; AND requires review of every term. Exceptions need an ADR, never substring matching.

The inventory distinguishes build tools, spike-only candidates and distributed runtime dependencies. A permissive top-level license is insufficient: audit bundled components, versions, notices and transitive dependencies. Current MFEM spike uses upstream BSD-3-Clause code. No production dependency is admitted by a survey recommendation alone. Platform BLAS/LAPACK is local test infrastructure; use an audited open BLAS implementation for distributed builds.

CI runs REUSE plus the inventory scanner and DCO trailer enforcement on pull requests. Release automation must produce an SPDX SBOM and ship complete corresponding source, build recipes and notices. This skeleton is not a release and does not certify a full binary dependency graph.

AGPL does not require publishing every private modification. Its distribution and remote-network interaction obligations govern when source must be offered. The owner's openness objective is implemented to that legal scope; the plan's universal “every fork” wording must not be presented as an unconditional legal guarantee. GPLv3 combination is addressed by AGPL section 13; GPLv2-only remains incompatible. Qt dynamic linking alone does not discharge all LGPL obligations: include notices, source/relink requirements as applicable. User designs, process descriptions and results are not automatically relicensed by using this software. User code and plugin derivative-work questions depend on facts; protocol separation is not a blanket legal exemption. Legal review is required before public release, including Python import policy and any exception.

Sources: [AGPL text](https://www.gnu.org/licenses/agpl-3.0.html), [FSF license compatibility](https://www.gnu.org/licenses/license-list.html), [DCO](https://developercertificate.org/), [REUSE specification](https://reuse.software/spec/), [MFEM license](https://github.com/mfem/mfem/blob/v4.8/LICENSE). Retrieved 2026-11-02. No restricted model or dataset may be bundled.
