# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
cmake_minimum_required(VERSION 3.25)
project(HeaviSolveGuiSpike LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(Qt6 REQUIRED COMPONENTS Widgets OpenGLWidgets)
find_package(VTK REQUIRED COMPONENTS CommonCore CommonDataModel FiltersCore RenderingCore RenderingOpenGL2 InteractionStyle GUISupportQt)
add_executable(gui_spike shell.cpp)
target_compile_options(gui_spike PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(gui_spike PRIVATE Qt6::Widgets Qt6::OpenGLWidgets ${VTK_LIBRARIES})
vtk_module_autoinit(TARGETS gui_spike MODULES ${VTK_LIBRARIES})
