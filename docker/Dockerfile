# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends cmake ninja-build g++ python3 python3-venv liblapack-dev ca-certificates curl && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . .
RUN cmake -S . -B build -G Ninja && cmake --build build && ctest --test-dir build -L foundation --output-on-failure
