# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
cmake_minimum_required(VERSION 3.25)
project(HeaviSolveGuiPrerequisites LANGUAGES CXX)
find_package(Qt6 REQUIRED COMPONENTS Widgets OpenGLWidgets)
find_package(VTK REQUIRED COMPONENTS GUISupportQt RenderingOpenGL2 FiltersCore)
