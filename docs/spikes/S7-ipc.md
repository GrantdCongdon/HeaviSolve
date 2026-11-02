<!-- SPDX-FileCopyrightText: 2026 HeaviSolve contributors -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# S7: IPC feasibility

Overall: **PARTIAL / NOT PASS**.

Native C++ POSIX shared-memory experiment forks a receiver, fills100,000,000 bytes in a shared mapping, sends a one-byte readiness token over a Unix socket, and checks every byte in the receiver. Checksum12499992621 matches the independent sender loop. Notification plus receiver scan took0.0169047s in the recorded run. [Raw output](../../verification/results/s7-shared-array.log). Payload bytes are not copied through the socket. This is a local inherited mapping, not a remote transport or a bandwidth benchmark.

No gRPC/protobuf vs ZeroMQ/FlatBuffers implementation comparison was completed. Neither stack's end-to-end zero-copy behavior is established. Fork inheritance also does not prove independently launched workers can attach safely. The100MB primitive test cannot satisfy the complete S7 criterion.

Next: implement both control channels with versioned descriptors, cancellation/progress, bounds validation, ownership/lifetime and crash cleanup. Use shared-memory handles for local arrays and an explicitly copying/chunked remote path; measure allocation/copy counts, latency and resident memory. Choose transport only after the comparison. [ZeroMQ licensing](https://zeromq.org/license/) confirms MPL-2.0, but no new ZeroMQ dependency was linked in this primitive experiment.
