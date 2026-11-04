// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <ngspice/sharedspice.h>
#include <cmath>
#include <filesystem>
#include <cstdlib>
#include <unistd.h>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
namespace {
bool failed=false;
int output(char* text,int,void*){std::cerr<<text<<'\n';return 0;}
int on_exit(int,NG_BOOL,NG_BOOL,int,void*){failed=true;return 0;}
}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 if(ngSpice_Init(output,nullptr,on_exit,nullptr,nullptr,nullptr,nullptr))return 3;
 char pattern[]="/tmp/heavisolve-osdi-XXXXXX";
 char* directory=mkdtemp(pattern);if(!directory)return 4;
 struct Cleanup { std::filesystem::path path; ~Cleanup(){std::filesystem::remove_all(path);} } cleanup{directory};
 const auto staged=cleanup.path/"model.osdi";
 std::filesystem::copy_file(argv[1],staged);
 std::string load="osdi "+staged.string();
 if(ngSpice_Command(load.data()) || failed)return 4;
 std::vector<std::string> lines={"HeaviSolve OpenVAF cubic model", ".model cubic hs_cubic(g1=0.001 g3=0.0001)","V1 in 0 1", "N1 in 0 cubic", ".op", ".end"};
 std::vector<char*> deck;for(auto&line:lines)deck.push_back(line.data());deck.push_back(nullptr);
 if(ngSpice_Circ(deck.data()))return 5;
 char run[]="run";if(ngSpice_Command(run)||failed)return 6;
 char name[]="v1#branch";auto* current=ngGet_Vec_Info(name);
 if(!current||current->v_length!=1)return 7;
 const double measured=-current->v_realdata[0],expected=.0011;
 const double error=std::abs(measured-expected);
 std::cout<<std::setprecision(17)<<"osdi_current_a="<<measured<<" analytic_current_a="<<expected<<" absolute_error_a="<<error<<" tolerance_a=1e-12\n";
 return std::isfinite(measured)&&error<1e-12?0:1;
}
