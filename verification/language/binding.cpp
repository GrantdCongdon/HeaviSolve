// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#define HS_SLAB_LIBRARY
#include "slab.cpp"
// Caller owns writable output/count for the duration of this synchronous call.
// Returns 0 success, 1 invalid argument, 2 insufficient capacity, 3 native failure.
extern "C" int hs_slab(int refinement, double* output, std::size_t capacity,
                       std::size_t* count) noexcept {
  if (!count) return 1;
  *count = 0;
  if (!output || refinement < 1 || refinement > 8) return 1;
  try {
    const auto values = solve(assemble(refinement));
    *count = values.size();
    if (values.size() < 2) return 3;
    if (capacity < values.size()) return 2;
    std::copy(values.begin(), values.end(), output);
    return 0;
  } catch (...) {
    return 3;
  }
}
