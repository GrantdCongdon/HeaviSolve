// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
// Research-only circuit IR and dialect emitters; no circuit solver implementation.
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
struct Element {std::string type,name,a,b,value;};
int main(int argc,char**argv){
 if(argc!=6)return 2;
 std::string kind=argv[1],engine=argv[2],analysis=argv[3],model=argv[4];
 std::vector<Element> e;
 std::vector<std::string> extra;
 if(kind=="rc"||kind=="rlc"){
 e={{"V","drive","in","0","DC 0 AC 1 SIN(0 1 1MEG)"},{"R","1","in",kind=="rc"?"out":"mid","1000"},{"C","1","out","0","1n"}};
 if(kind=="rlc")e.push_back({"L","1","mid","out","1m"});
 }else if(kind=="diode"){
 e={{"V","drive","in","0","DC 0.8 AC 0.001 SIN(0.8 0.001 1MEG)"},{"R","1","in","out","1000"},{"D","1","out","0","test"}};
 extra={".model test D(IS=1e-14 N=1)"};
 }else if(kind=="ihp"){
 e={{"V","drive","b","0","DC 0.8 AC 0.001 SIN(0.8 0.001 1MEG)"},{"V","supply","vcc","0","1.2"},{"R","1","vcc","out","1000"}};
 extra={".lib \""+model+"\" hbt_typ","Xq out b 0 0 npn13G2"};
 }else if(kind=="cubic"){
 e={{"V","drive","out","0","DC 0 AC 1 SIN(0 1 1MEG)"}};
 extra={"B1 out 0 I={0.001*V(out)+0.0001*V(out)*V(out)*V(out)}"};
 }else return 3;
 std::ofstream f(argv[5]);f<<"HeaviSolve "<<kind<<" "<<analysis<<" conformance\n* SPDX-" "License-Identifier: AGPL-3.0-or-later\n* SPDX-" "FileCopyrightText: 2026 HeaviSolve contributors\n";
 for(auto& x:e)f<<x.type<<x.name<<" "<<x.a<<" "<<x.b<<" "<<x.value<<"\n";
 for(auto& s:extra)f<<s<<"\n";
 if(engine=="ngspice")f<<".options reltol=1e-8 abstol=1e-14 temp=27\n";
 else f<<".options NONLIN reltol=1e-8 abstol=1e-14\n.options TIMEINT reltol=1e-8 abstol=1e-14\n.options DEVICE TEMP=27\n";
 if(analysis=="dc")f<<".dc Vdrive 0.7 0.8 0.01\n";
 else if(analysis=="ac")f<<".ac dec 10 1k 100meg\n";
 else if(analysis=="tran")f<<".tran 1n 10u 0 1n\n";
 else if(analysis=="hb")f<<".hb 1meg\n.options HB numfreq=7\n";
 else return 4;
 if(engine=="xyce")f<<".print "<<(analysis=="hb"?"HB_FD":analysis)<<" format=csv precision=16 "<<(analysis=="dc"?(kind=="ihp"?"V(b) ":"V(in) "):"")<<(analysis=="ac"||analysis=="hb"?"VR(out) VI(out) IR(Vdrive) II(Vdrive)":"V(out) I(Vdrive)")<<"\n";
 f<<".end\n";return f.good()?0:5;
}
