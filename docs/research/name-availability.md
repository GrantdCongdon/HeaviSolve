<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# HeaviSolve: preliminary name check

Checked 2026-11-02. **Keep the name HeaviSolve. No confirmed conflict was found; direct endpoint checks below found no current package/domain records.** This is a quick namespace check, not trademark clearance or reservation. No accounts, packages, domains or repositories were registered.

| Namespace | Check performed | Observed result | Conclusion |
|---|---|---|---|
| GitHub | Connected GitHub `search_repositories`, query `HeaviSolve`, per_page 100; exact-name web search | Connector returned `repositories: []`; web search found no results | No visible repository conflict found in this search. Does not establish organization/user availability or absence of private repositories |
| PyPI | Exact-name site search; attempted `https://pypi.org/pypi/heavisolve/json` | No indexed result; direct endpoint returned tool “Cache miss,” not an authoritative registry 404 | **Unknown**; rerun direct registry lookup before publication |
| conda-forge | Exact-name site search on anaconda.org; attempted `https://api.anaconda.org/package/conda-forge/heavisolve` | No indexed result; API URL inaccessible through web tool | **Unknown**; check feedstock and package registry before submission |
| `heavisolve.com` | Exact domain search; attempted Verisign RDAP domain endpoint | No indexed result; RDAP inaccessible through tool | **Unknown**; no registration-availability claim |
| `heavisolve.org` | Exact domain search; attempted Public Interest Registry RDAP endpoint | No indexed result; RDAP inaccessible through tool | **Unknown** |
| `heavisolve.dev` | Exact domain search; attempted website open | No indexed result; site inaccessible | **Unknown**; lack of a website does not imply unregistered domain |

Queries used: `"HeaviSolve"`, `"HeaviSolve" site:github.com`, `"HeaviSolve" site:pypi.org`, `"HeaviSolve" site:anaconda.org`, and `"heavisolve.com" OR "heavisolve.org" OR "heavisolve.dev"`. The direct GitHub search page also returned a web cache miss; the connector search provided the successful repository check.

Recheck [GitHub repository search](https://github.com/search?q=HeaviSolve&type=repositories), [PyPI](https://pypi.org/project/heavisolve/), [conda-forge feedstocks](https://github.com/conda-forge), and registry RDAP/registrar availability immediately before a public release. Report any future conflict to the owner; do not rename automatically.

## Direct endpoint follow-up

On 2026-11-02 escalated curl reached the primary endpoints successfully. PyPI JSON and api.anaconda.org/package/conda-forge/heavisolve each returned HTTP404 with an explicit missing-package response. Verisign `.com`, Public Interest Registry `.org`, Identity Digital `.io`, and Google Registry `.dev` RDAP queries each returned HTTP404. These supersede the earlier tool-access failures above: no current record was found at those endpoints. They do not establish registrar eligibility, reserved/premium status or trademark rights. Raw responses and endpoint/status metadata are retained in verification/results/name-check.log. No registration was attempted.
