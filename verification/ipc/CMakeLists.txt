# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
cmake_minimum_required(VERSION 3.25)
project(HeaviSolveIpcSpike LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)
find_path(FLATBUFFERS_INCLUDE flatbuffers/flatbuffers.h REQUIRED)
find_path(ZMQ_INCLUDE zmq.hpp REQUIRED)
find_library(ZMQ_LIBRARY zmq REQUIRED)
find_program(FLATC flatc REQUIRED)
add_custom_command(OUTPUT spike.pb.cc spike.pb.h spike.grpc.pb.cc spike.grpc.pb.h
 COMMAND protobuf::protoc --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=${CMAKE_CURRENT_BINARY_DIR} --grpc_out=${CMAKE_CURRENT_BINARY_DIR} --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin> ${CMAKE_CURRENT_SOURCE_DIR}/spike.proto
 DEPENDS spike.proto)
add_custom_command(OUTPUT spike_generated.h COMMAND ${FLATC} --cpp -o ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/spike.fbs DEPENDS spike.fbs)
add_executable(ipc_compare compare.cpp spike.pb.cc spike.grpc.pb.cc spike_generated.h)
target_include_directories(ipc_compare PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_include_directories(ipc_compare SYSTEM PRIVATE ${FLATBUFFERS_INCLUDE} ${ZMQ_INCLUDE})
target_link_libraries(ipc_compare PRIVATE gRPC::grpc++ protobuf::libprotobuf ${ZMQ_LIBRARY})
