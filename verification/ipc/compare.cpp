// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include "spike.grpc.pb.h"
#include "spike_generated.h"
#include <grpcpp/grpcpp.h>
#include <zmq.hpp>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
constexpr std::uint64_t payload=100000000,expected_checksum=12499992621ULL;
void create_array(const std::string& path){
 const int fd=open(path.c_str(),O_RDWR|O_CREAT|O_EXCL,0600);if(fd<0)throw std::runtime_error("create array failed");
 if(ftruncate(fd,payload))throw std::runtime_error("resize failed");
 auto* data=static_cast<std::uint8_t*>(mmap(nullptr,payload,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0));
 if(data==MAP_FAILED)throw std::runtime_error("producer mmap failed");
 for(std::uint64_t i=0;i<payload;++i)data[i]=i%251;
 munmap(data,payload);close(fd);
}
std::uint64_t consume(const std::string& path,std::uint64_t bytes){
 if(bytes!=payload)throw std::runtime_error("invalid payload descriptor");
 const int fd=open(path.c_str(),O_RDONLY);struct stat info{};
 if(fd<0||fstat(fd,&info)||static_cast<std::uint64_t>(info.st_size)!=bytes)throw std::runtime_error("invalid array file");
 const auto* data=static_cast<const std::uint8_t*>(mmap(nullptr,bytes,PROT_READ,MAP_SHARED,fd,0));
 if(data==MAP_FAILED)throw std::runtime_error("consumer mmap failed");
 std::uint64_t sum=0;for(std::uint64_t i=0;i<bytes;++i)sum+=data[i];
 munmap(const_cast<std::uint8_t*>(data),bytes);close(fd);return sum;
}
class Service final:public hsp_spike::Spike::Service {
 std::string path_;
 public:explicit Service(std::string path):path_(std::move(path)){}
 grpc::Status Watch(grpc::ServerContext*,const hsp_spike::Request*,grpc::ServerWriter<hsp_spike::Update>* writer)override{
  for(unsigned p:{25U,50U,100U}){hsp_spike::Update message;message.set_progress(p);
   if(p==100){message.set_path(path_);message.set_bytes(payload);message.set_checksum(expected_checksum);}
   if(!writer->Write(message))return {grpc::StatusCode::CANCELLED,"receiver disconnected"};
  }return grpc::Status::OK;
 }
};
int main(int argc,char**argv){try{
 if(argc!=5)return 2;
 const std::string role=argv[1],protocol=argv[2],endpoint=argv[3],path=argv[4];
 if(role=="server"){
  create_array(path);
  if(protocol=="grpc"){
   Service service(path);grpc::ServerBuilder builder;builder.AddListeningPort("unix:"+endpoint,grpc::InsecureServerCredentials());builder.RegisterService(&service);
   auto server=builder.BuildAndStart();if(!server)throw std::runtime_error("gRPC listen failed");
   std::cout<<"READY\n"<<std::flush;server->Wait();
  }else{
   zmq::context_t context(1);zmq::socket_t socket(context,zmq::socket_type::pair);socket.bind("ipc://"+endpoint);
   std::cout<<"READY\n"<<std::flush;zmq::message_t request;auto received=socket.recv(request);if(!received)return 3;
   for(unsigned p:{25U,50U,100U}){
    flatbuffers::FlatBufferBuilder builder;auto name=builder.CreateString(p==100?path:"");
    auto update=hsp_flat::CreateUpdate(builder,p,name,p==100?payload:0,p==100?expected_checksum:0);builder.Finish(update);
    if(!socket.send(zmq::buffer(builder.GetBufferPointer(),builder.GetSize())))return 3;
   }
  }return 0;
 }
 std::uint64_t bytes=0,checksum=0,control_bytes=0;std::string received_path;unsigned progress=0,count=0;
 const auto start=std::chrono::steady_clock::now();
 if(protocol=="grpc"){
  auto channel=grpc::CreateChannel("unix:"+endpoint,grpc::InsecureChannelCredentials());auto stub=hsp_spike::Spike::NewStub(channel);
  grpc::ClientContext context;context.set_deadline(std::chrono::system_clock::now()+std::chrono::seconds(30));
  hsp_spike::Request request;auto reader=stub->Watch(&context,request);hsp_spike::Update message;
  while(reader->Read(&message)){
   if(message.progress()<=progress)throw std::runtime_error("non-monotonic progress");progress=message.progress();++count;control_bytes+=message.ByteSizeLong();
   if(progress==100){received_path=message.path();bytes=message.bytes();checksum=message.checksum();}
  }if(!reader->Finish().ok())throw std::runtime_error("RPC failed");
 }else{
  zmq::context_t context(1);zmq::socket_t socket(context,zmq::socket_type::pair);socket.set(zmq::sockopt::rcvtimeo,30000);socket.connect("ipc://"+endpoint);
  if(!socket.send(zmq::str_buffer("watch")))return 3;
  while(progress<100){zmq::message_t message;if(!socket.recv(message))throw std::runtime_error("receive timed out");
   flatbuffers::Verifier verifier(static_cast<const std::uint8_t*>(message.data()),message.size());if(!hsp_flat::VerifyUpdateBuffer(verifier))throw std::runtime_error("invalid FlatBuffer");
   const auto* update=hsp_flat::GetUpdate(message.data());if(update->progress()<=progress)throw std::runtime_error("non-monotonic progress");
   progress=update->progress();++count;control_bytes+=message.size();
   if(progress==100){received_path=update->path()->str();bytes=update->bytes();checksum=update->checksum();}
  }
 }
 if(received_path!=path||count!=3||checksum!=expected_checksum)throw std::runtime_error("invalid stream");
 const auto measured=consume(received_path,bytes);
 const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"protocol="<<protocol<<" progress_messages="<<count<<" payload_bytes="<<bytes<<" serialized_control_bytes="<<control_bytes<<" checksum="<<measured<<" receive_and_scan_seconds="<<seconds<<" array_userspace_copies=0 independently_launched_processes=true\n";
 return measured==expected_checksum?0:1;
}catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}}
