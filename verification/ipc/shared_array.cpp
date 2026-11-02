// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <iostream>
int main() {
  constexpr std::size_t bytes=100000000;
  auto* data=static_cast<std::uint8_t*>(mmap(nullptr,bytes,PROT_READ|PROT_WRITE,
                                           MAP_SHARED|MAP_ANON,-1,0));
  if(data==MAP_FAILED) { perror("mmap"); return 2; }
  int control[2]; if(socketpair(AF_UNIX,SOCK_STREAM,0,control)) { perror("socketpair");return 2; }
  const pid_t child=fork(); if(child<0) return 2;
  if(child==0) {
    close(control[0]); char token;
    if(read(control[1],&token,1)!=1) _exit(3);
    std::uint64_t sum=0;
    for(std::size_t i=0;i<bytes;++i) sum+=data[i];
    if(write(control[1],&sum,sizeof(sum))!=sizeof(sum)) _exit(4);
    _exit(0);
  }
  close(control[1]);
  for(std::size_t i=0;i<bytes;++i) data[i]=static_cast<std::uint8_t>(i%251);
  const auto start=std::chrono::steady_clock::now();
  const char token='R';
  if(write(control[0],&token,1)!=1) return 3;
  std::uint64_t sum=0;
  if(read(control[0],&sum,sizeof(sum))!=sizeof(sum)) return 4;
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  int status=0; waitpid(child,&status,0);
  std::uint64_t expected=0;
  for(std::size_t i=0;i<bytes;++i) expected+=i%251;
  std::cout<<"payload_bytes="<<bytes<<" child_checksum="<<sum<<" expected_checksum="<<expected
           <<" notification_and_child_scan_seconds="<<seconds
           <<" shared_mapping=true payload_sent_through_socket=false\n";
  munmap(data,bytes); close(control[0]);
  return WIFEXITED(status) && WEXITSTATUS(status)==0 && sum==expected?0:1;
}
