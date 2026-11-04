// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <ngspice/sharedspice.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
int output(char*s,int,void*){std::cerr<<s<<'\n';return 0;}
int main(int argc,char**argv){
 if(argc!=4)return 2;
 ngSpice_Init(output,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr);
 std::ifstream f(argv[1]);std::vector<std::string> lines;std::string line;while(std::getline(f,line))lines.push_back(line);
 std::vector<char*> ptrs;for(auto& s:lines)ptrs.push_back(s.data());ptrs.push_back(nullptr);
 if(ngSpice_Circ(ptrs.data()))return 3;char run[]="run";if(ngSpice_Command(run))return 4;
 char out[]="v(out)",current[]="vdrive#branch";auto*v=ngGet_Vec_Info(out);if(!v)return 5;auto volts=*v;auto*i=ngGet_Vec_Info(current);if(!i)return 6;auto amps=*i;
 std::string scale=std::string(argv[2])=="ac"?"frequency":std::string(argv[2])=="dc"?"v-sweep":"time";
 auto*t=ngGet_Vec_Info(scale.data());if(!t)return 7;auto times=*t;
 std::ofstream result(argv[3]);result<<"scale,vr,vi,ir,ii\n"<<std::setprecision(17);
 for(int n=0;n<times.v_length;++n){result<<(times.v_realdata?times.v_realdata[n]:times.v_compdata[n].cx_real)<<',';
 if(volts.v_compdata)result<<volts.v_compdata[n].cx_real<<','<<volts.v_compdata[n].cx_imag;else result<<volts.v_realdata[n]<<",0";
 result<<',';if(amps.v_compdata)result<<amps.v_compdata[n].cx_real<<','<<amps.v_compdata[n].cx_imag;else result<<amps.v_realdata[n]<<",0";result<<'\n';}
 return result.good()?0:8;
}
