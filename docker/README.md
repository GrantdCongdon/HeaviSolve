<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Foundation container

Build from the repository root with `docker build -f docker/Dockerfile -t heavisolve-foundation .`, then run `docker run --rm heavisolve-foundation ctest --test-dir build -L foundation --output-on-failure`.

The image builds the repository skeleton and runs its foundation tests. Workflow run41858845826 on ceeb4d7 passed2/2 checks; [stored evidence](../verification/results/ci-41858845826/provenance.json) identifies the image and verified log artifact. Later revisions must pass their own run.

This is not a complete numerical environment or a published binary distribution. Source-built complex FEM and SPICE research workflows remain separate. Ubuntu packages are resolved at build time, so the Dockerfile alone is not a bit-reproducible lockfile. A distributed image requires the release dependency audit, notices and corresponding-source obligations in ADR002.
