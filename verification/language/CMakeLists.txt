# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
cmake_minimum_required(VERSION 3.25)
project(HeaviSolveLanguageSpike LANGUAGES CXX)
find_package(LAPACK REQUIRED)
find_program(RUSTC rustc REQUIRED)
add_executable(slab-cpp slab.cpp)
target_compile_features(slab-cpp PRIVATE cxx_std_20)
target_compile_options(slab-cpp PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(slab-cpp PRIVATE LAPACK::LAPACK)
add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/slab-rust
  COMMAND ${RUSTC} --edition=2024 -C opt-level=2 -D warnings
    ${CMAKE_CURRENT_SOURCE_DIR}/slab.rs -o ${CMAKE_CURRENT_BINARY_DIR}/slab-rust
  DEPENDS slab.rs VERBATIM)
add_custom_target(rust_slab ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/slab-rust)
