<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S7: IPC feasibility

**LOCAL PASS for a 100 MB shared-array path with both control protocols; hosted CI pending.** Independently launched native server and client processes exchange progress and a descriptor using gRPC/protobuf or ZeroMQ/FlatBuffers. The receiver maps the shared file read-only and scans all 100,000,000 bytes. This is a local shared-file mapping path, not remote zero-copy transport.

| Control protocol | Progress messages | Serialized control bytes | Receive plus checksum scan | Array checksum |
|---|---:|---:|---:|---:|
| gRPC/protobuf | 3 | 53 | 0.0186305 s | 12499992621 |
| ZeroMQ/FlatBuffers | 3 | 152 | 0.0151352 s | 12499992621 |

[Raw output](../../verification/results/s7-protocol-comparison.log) is a single run for each protocol, not statistically meaningful comparative throughput evidence. Control-byte counts exclude protocol framing. The timer starts after the producer has created and initialized the mapping, so it excludes allocation and initialization. The producer writes `i % 251`; the receiver checks the full-array sum. No array-sized user-space copy occurs between the processes: each independently maps the same file. This claim follows the tested code path, not a copy-count profiler; kernel paging and control-message copies still occur.

The native implementation checks increasing progress (25, 50, 100), three received updates, the expected path, payload length, file size and checksum, and validates FlatBuffers messages. The Python harness only launches processes, waits for readiness and removes its temporary directory after shutdown. Unlike the earlier [forked prototype](../../verification/results/s7-shared-array.log), workers do not inherit the mapping. The first restricted-environment socket-listen attempt failed and is [retained](../../verification/results/s7-sandbox-listen-failure.log); the recorded passing run used native local IPC access.

Build `verification/ipc` using CMake and the isolated `/tmp/heavisolve-ipc` prefix containing grpc-cpp 1.51.1, protobuf 3.21.12, ZeroMQ/cppzmq and FlatBuffers; execute `python3 verification/ipc/run_compare.py` after creating `.work/ipc-build/ipc_compare`. See [source and output hashes](../../verification/results/s4-s6-s7-provenance.json). The exact environment must be audited and locked before adoption or distribution.

Recommendation for the component ADR: gRPC/protobuf control plus local shared mappings, because its generated service interface and streaming suit the shared GUI/Python API. The timings do not establish a speed winner. ZeroMQ/FlatBuffers remains a workable alternative. [gRPC](https://github.com/grpc/grpc/blob/master/LICENSE) and [FlatBuffers](https://github.com/google/flatbuffers/blob/master/LICENSE) use Apache-2.0; [protobuf](https://github.com/protocolbuffers/protobuf/blob/main/LICENSE) uses BSD-3-Clause; [ZeroMQ](https://zeromq.org/license/) uses MPL-2.0. Dependency and maintenance review remains required by ADR-002.

Not established: remote array transfer, production descriptor authentication, robust crash cleanup, cancellation semantics beyond disconnect, bounded job queues, resource exhaustion behavior, memory-use measurements, or Linux/macOS CI. These are future implementation requirements; the research spike is not the M1 HSP server.
