# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
cmake_minimum_required(VERSION 3.25)
project(HeaviSolveComplexCavity LANGUAGES CXX)
find_package(MFEM 4.10 CONFIG REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(SLEPC REQUIRED IMPORTED_TARGET SLEPc)
add_executable(complex-cavity cavity.cpp)
target_compile_features(complex-cavity PRIVATE cxx_std_20)
target_compile_options(complex-cavity PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(complex-cavity PRIVATE mfem PkgConfig::SLEPC)
enable_testing()
add_test(NAME complex_cavity COMMAND complex-cavity)
set_tests_properties(complex_cavity PROPERTIES LABELS "m0;numerical" TIMEOUT 300)
