<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# ngspice47 selected-build license scope

Reviewed 2026-11-03. **Source-scope investigation, not integration or binary-distribution approval.** The [ADR002 policy](../adr/ADR-002-licensing.md) and exact-license scanner remain unchanged. This resolves several ambiguous top-level labels but does not flatten the source tree into one BSD identifier.

The source archive is [ngspice47 from its official release mirror](https://downloads.sourceforge.net/project/ngspice/ng-spice-rework/47/ngspice-47.tar.gz), SHA256 `894e649651f1838a14095e5a5439e7d3aa63e87ede14d283173fda4fcdef675f`. Evidence below comes from the unpacked source and the previously built local configuration; no new package was installed. The current Linux research recipe uses `--with-ngshared --without-x --disable-openmp --disable-klu --with-readline=no`. Linux configuration/output still needs confirmation from its completed build, not inference from macOS.

## Component findings

| Component | Grant found in actual source | Selected-build relevance and admission consequence |
|---|---|---|
| General ngspice source | COPYING declares modified BSD for source/test/example files except its listed exceptions; its three conditions match BSD-3-Clause | Preserve copyright, conditions, disclaimer and non-endorsement requirement. Does not override component exceptions below. |
| Numparam | `src/frontend/numparam/readme.txt` expressly permits LGPL version2 **or any later version** | Included frontend functionality. This is not LGPLv2-only. Selecting a later allowed LGPL version is possible under the grant, but the selected branch and its obligations must be recorded in an admission decision. Individual C headers refer to this README rather than restating the version. |
| Tcl frontend | `src/tclspice.c` says LGPLv2, without an explicit later-version option in that header | Shared module and Tcl module are alternative configure branches; the measured local config has TCL_MODULE undefined and SHARED_MODULE defined. Excluded from that selected runtime. Do not relabel its ambiguous shorthand as LGPL-2.1-or-later or claim a full-source-archive audit from exclusion. |
| KLU | COPYING labels the bundled subtree LGPLv2 | Explicitly disabled; local config has KLU undefined. No file-by-file KLU version determination was performed in this bounded review. This exclusion does not audit external SuiteSparse used by Xyce. |
| Original Sparse | `src/maths/sparse/spdefs.h` grants use/copy/modify/distribute for any purpose without fee, with notices, documentation attribution and proper credit | Enabled native sparse path. It is an MIT-like grant with an explicit credit condition, not automatically the exact SPDX MIT text. Preserve the grant and credit; a narrowly scoped policy/identifier review is still needed. |
| OSDI | `src/osdi/osdi.h` expressly uses MPL2.0 | Enabled by default and in measured local config. Retain file-level notices and source obligations; the generated-header status does not remove its license. An external model loaded through OSDI has a separate license. |
| XSPICE core | COPYING gives a public-domain statement with a warranty disclaimer; seegenerator input itself says Public Domain | Enabled by default and in measured local config. No non-commercial restriction was found in those cited statements. Public-domain status is not an exact ID already accepted by the scanner; record scoped evidence/ADR before admission, rather than adding an unrestricted catch-all. |
| XSPICE table code models | `table2D/cfunc.mod` explicitly permits GPL version2 **or later**, consistent with COPYING | XSPICE enabled means these installable code models must be considered in the selected distribution. This is not GPL-2.0-only. A GPL3-compatible selection remains subject to source/notices obligations; this review does not establish every installed code model is linked into libngspice. |
| NDEV | COPYING says public domain | Experimental option defaults off and measured local config has NDEV undefined. No NDEV-file survey was performed. |
| Manuals and COPYING document | COPYING identifies CC-BY-SA4.0 for the licensing document and points to the same manual license | Documentation grant, not runtime-code license. Include attribution/share-alike where redistributing those documents. |
| m4 configure helpers | All eight shipped m4 files examined carry copying/modification permissions conditional on retaining notices: three Autoconf Archive helpers and five libtool macros | Build/source infrastructure, not an inference of runtime object code. The permissive macro header and embedded libtool licensing text are distinct. `libtool.m4` also embeds GPL2-or-later text for generated libtool machinery. Preserve those notices and applicable generated-script exceptions; do not call every m4 file generic MIT. |

The measured local `/tmp/heavisolve-spice/build/src/include/ngspice/config.h` has XSPICE, OSDI and SHARED_MODULE defined; KLU, NDEV, TCL_MODULE and GNU/readline header options are undefined. `configure.ac` establishes that XSPICE/OSDI are default-on, NDEV is opt-in, and the ngshared path precedes the Tcl alternative. This is configuration evidence, not a recursive link or installed-file audit.

## Remaining closure work

1. Retain Linux generated configuration, installed-file inventory and linked-library inventory, and confirm it matches the intended options. Audit enabled files and generated code rather than only top-level COPYING.
2. Record explicit LGPL/GPL later-version choices, preserve complete upstream notices, and review exact public-domain/Sparse/m4 expressions through a scoped ADR. Do not add unknown expressions to the scanner merely to make it green.
3. Review system/compiler runtimes and any bundled data separately. The Xyce/Trilinos/FFTW/SuiteSparse graph is outside this ngspice-only review.
4. For binaries, assemble corresponding source, patches and reproducible build instructions, plus relevant copyleft source/relink obligations. Current research builds do not constitute this distribution package.

## Source evidence hashes

Relative to the pinned ngspice47 source root. The seegenerator hash is the original generator input inspected locally; the Linux recipe records its own post-patch hash. No source or model contents are bundled by this document.

| File | SHA256 |
|---|---|
| `COPYING` | `6d939001e899ede403277fb37124c2af6f1cf92926465cd8f4bf59859e06f579` |
| `configure.ac` | `12ed326ff584df4411dbe6e314abf8a2ac442ed9f0acb5bd2e1e9523ff69a039` |
| `src/frontend/numparam/readme.txt` | `30a710c26c4d5c336a5551385a18336234a817d31ce0e7bf1766e2deccb31dde` |
| `src/tclspice.c` | `a61436a628e827effe53dab2593460db37e1febb5b772755693118b6e34b7005` |
| `src/maths/sparse/spdefs.h` | `47b1efebf2ff10aa5d1c32cf5541e8a984095a800ab4b6571d133b3782d4f643` |
| `src/osdi/osdi.h` | `7854f1653a951b175381efb6bee9af4998f21ef022c4aafcb1d3840a6035f838` |
| `src/xspice/icm/table/table2D/cfunc.mod` | `f773479567a7b83436d0e2f5ad3fe74a2ed2e340a0f4dd7fa61ac432407e6fd5` |
| `src/xspice/icm/xtradev/seegenerator/cfunc.mod` | `e6791ec717e56ed109b1d77836e1032136537d5c0f8fa917a9441424015ca38e` |
| `m4/ax_compare_version.m4` | `7044b2c0fead21c176a981536be1b8c957615da183840cd4587c9062c51666df` |
| `m4/ax_prog_bison_version.m4` | `344eda1971f8c03b838b0a9e1b7347dc6549ee78cc85fb45093d32d89323bcde` |
| `m4/ax_prog_cc_for_build.m4` | `4453f1290f4be6c20bd29a796b9ce19b2106d33b0634edb80d5bfbd9b165138c` |
| `m4/libtool.m4` | `38a99c1d5072c1e0e1f45da415d39143d529b1052b73a60477e1bd6badf7e99f` |
| `m4/ltoptions.m4` | `f3d4ed0426501308028dd7690cf343cb280479d637a2ebee6c289ec2e708df3b` |
| `m4/ltsugar.m4` | `0896f153a5a40546566028a4272642ae291532f3e65c25fcae950c8812b8c265` |
| `m4/ltversion.m4` | `2a6baf40b64f34234e0b76c7ff62b01a1f6bbf60089f4f74506b49f800ffaf9e` |
| `m4/lt~obsolete.m4` | `8533006830e1ea9625fc5e4c060e653eedf9d5464a9b2f5f494244ee272e2e2f` |

## Actionable identifier mapping follow-up

Primary SPDX license texts checked2026-11-03. These are proposed exact-source mappings for an ADR decision, **not additions to the allowlist**. The existing file SHA256 table binds each proposal to the inspected release contents.

| Material | Proposed identifier | Evidence and required scope |
|---|---|---|
| `m4/ax_compare_version.m4`, `m4/ax_prog_bison_version.m4`, `m4/ax_prog_cc_for_build.m4` | `FSFAP` | The permission and short warranty-disclaimer text matches the [SPDX FSFAP text](https://spdx.org/licenses/FSFAP.html), ignoring comment markers/whitespace and retaining individual copyright notices. Limit admission to the three exact hashes above. Preserve copyright and permission notices. |
| Top-level file grants in `m4/libtool.m4`, `ltoptions.m4`, `ltsugar.m4`, `ltversion.m4`, `lt~obsolete.m4` | `FSFULLR` | Their header grant matches [SPDX FSFULLR](https://spdx.org/licenses/FSFULLR.html); copyright/date variation is explicitly replaceable in its template. Preserve the full notice. These headers do not contain the added short-disclaimer sentence needed for FSFULLRSD. Limit to the five exact hashes above. |
| `_LT_COPYING` generated-script notice embedded in `m4/libtool.m4` | `GPL-2.0-or-later WITH Libtool-exception` | The embedded text permits later GPL versions and its special exception matches [SPDX Libtool-exception](https://spdx.org/licenses/Libtool-exception.html), whose template makes “Lesser” optional. Treat generated libtool machinery separately from the surrounding FSFULLR macro-file grant; preserve both notices. Do not label the generated script merely FSFULLR or assume an automatic copyleft exception for unrelated code. |
| Original Sparse grant represented by `src/maths/sparse/spdefs.h` | `LicenseRef-HeaviSolve-ngspice47-Sparse-credit` | No exact listed equivalent was established in this bounded review. In particular, [SPDX HPND](https://spdx.org/licenses/HPND.html) does not represent the additional affirmative proper-credit clause; generic MIT also omits it. Retain an extracted custom grant, its full source notice and explicit credit to Kenneth S. Kundert and the University of California. Use the custom identity only for exact files carrying this grant or explicitly covered by the pinned COPYING scope; do not admit arbitrary “MIT-like” labels. |
| XSPICE public-domain statement in release COPYING | `LicenseRef-HeaviSolve-ngspice47-XSPICE-public-domain` | Preserve the exact declaration and warranty/liability disclaimer. This is a source-specific dedication statement, not the text of CC0 or Unlicense; neither identifier is substituted. Scope excludes table code models and any file with a different explicit grant. A standalone “Public Domain” label on a later file is supporting evidence, not proof that all future XSPICE additions share this exact notice. |

Two extracted-notice fingerprints make a later policy entry reproducible without storing a new third-party license file in this task:

- XSPICE declaration: SHA256 `ab7bbc34f6012414a2c12560a9e45265d00865c1aa1961a286afbdea84e074c1`. Exact bytes in COPYING from the first `THE SOFTWARE PROGRAMS BELOW` through the first following double newline, excluding that double newline. This includes the complete public-domain/warranty/liability paragraph.
- Sparse grant: SHA256 `c5c4ea4b0f83850415f5cd2bb65286c7ea777b82394271f51174f89c68e9f60d`. Exact bytes in spdefs.h from the first ` *  Permission to use` up to, but excluding, the subsequent closing ` */`; comment prefixes/line breaks are retained in this digest.

Suggested root decision: record the eight exact m4 file mappings and two scoped custom-grant identities in an ADR with their file hashes, obligations and selected-build exclusions. If admitted, keep automated matching exact and retain the original source notices; a generic public-domain or HPND allow rule would exceed this evidence. Before distribution, inventory every included Sparse/XSPICE file and generated output, identify contrary notices, and package the extracted licenses/credits. This follow-up supplies a concrete mapping proposal; it does not approve the broader ngspice runtime or the independent Xyce dependency graph.
