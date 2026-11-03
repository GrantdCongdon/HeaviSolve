// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <numbers>
#include <stdexcept>
#include <vector>
extern "C" void dggev_(const char*,const char*,const int*,double*,const int*,double*,const int*,double*,double*,double*,double*,const int*,double*,const int*,double*,const int*,int*);
struct Assembly { int n; std::vector<double> a,b; };
Assembly assemble(int refinement) {
 const int nc=16*refinement,cl=12*refinement,ny=2;
 std::vector<double>x;
 for(int j=cl;j>0;--j)x.push_back(-.5-4.*j*j/(cl*cl));
 for(int j=0;j<=nc;++j)x.push_back(-.5+double(j)/nc);
 for(int j=1;j<=cl;++j)x.push_back(.5+4.*j*j/(cl*cl));
 const int nx=int(x.size())-1,ne=(2*nx-1)*ny,nn=(nx-1)*ny,n=ne+nn;
 Assembly out{n,std::vector<double>(n*n),std::vector<double>(n*n)};
 auto h=[=](int i,int j){return i*ny+j%ny;};
 auto v=[=](int i,int j){return i==0||i==nx?-1:nx*ny+(i-1)*ny+j%ny;};
 auto node=[=](int i,int j){return i==0||i==nx?-1:ne+(i-1)*ny+j%ny;};
 const double k2=4*std::numbers::pi*std::numbers::pi;
 const std::array<double,2> quad={.5-.5/std::sqrt(3.),.5+.5/std::sqrt(3.)};
 for(int ix=0;ix<nx;++ix)for(int iy=0;iy<ny;++iy){
  const double dx=x[ix+1]-x[ix],dy=.2/ny,det=dx*dy;
  const double eps=std::abs(.5*(x[ix]+x[ix+1]))<.5?2.25:1.;
  const std::array<int,4>edges={h(ix,iy),v(ix+1,iy),h(ix,iy+1),v(ix,iy)};
  const std::array<int,4>nodes={node(ix,iy),node(ix+1,iy),node(ix+1,iy+1),node(ix,iy+1)};
  const std::array<double,4>curl={1/det,1/det,-1/det,-1/det};
  for(double u:quad)for(double w:quad){
   const std::array<std::array<double,2>,4>N={{{(1-w)/dx,0},{0,u/dy},{w/dx,0},{0,(1-u)/dy}}};
   const std::array<double,4>phi={(1-u)*(1-w),u*(1-w),u*w,(1-u)*w};
   const std::array<std::array<double,2>,4>grad={{{-(1-w)/dx,-(1-u)/dy},{(1-w)/dx,-u/dy},{w/dx,u/dy},{-w/dx,(1-u)/dy}}};
   const double weight=det/4;
   for(int i=0;i<4;++i)for(int j=0;j<4;++j){
    if(edges[i]>=0&&edges[j]>=0){
     const double m=N[i][0]*N[j][0]+N[i][1]*N[j][1];
     out.a[edges[i]+edges[j]*n]+=weight*(k2*eps*m-curl[i]*curl[j]);
     out.b[edges[i]+edges[j]*n]+=weight*m;
    }
    if(nodes[i]>=0&&nodes[j]>=0)
     out.b[nodes[i]+nodes[j]*n]+=weight*(grad[i][0]*grad[j][0]+grad[i][1]*grad[j][1]-k2*eps*phi[i]*phi[j]);
    if(edges[i]>=0&&nodes[j]>=0){
     const double g=weight*(N[i][0]*grad[j][0]+N[i][1]*grad[j][1]);
     out.b[edges[i]+nodes[j]*n]+=g;out.b[nodes[j]+edges[i]*n]+=g;
    }
   }
  }
 }
 return out;
}
std::vector<double> solve(Assembly data){
 const int n=data.n,one=1;int info=0,lwork=-1;double query=0,dummy=0;
 std::vector<double>ar(n),ai(n),beta(n);
 const char no='N';
 dggev_(&no,&no,&n,data.a.data(),&n,data.b.data(),&n,ar.data(),ai.data(),beta.data(),&dummy,&one,&dummy,&one,&query,&lwork,&info);
 if(info)throw std::runtime_error("LAPACK workspace query failed");
 lwork=int(query);std::vector<double>work(lwork);
 dggev_(&no,&no,&n,data.a.data(),&n,data.b.data(),&n,ar.data(),ai.data(),beta.data(),&dummy,&one,&dummy,&one,work.data(),&lwork,&info);
 if(info)throw std::runtime_error("LAPACK eigensolve failed");
 std::vector<double>neff;
 for(int i=0;i<n;++i)if(std::abs(ai[i])<1e-9&&std::abs(beta[i])>1e-14){
  const double q=ar[i]/beta[i]/(4*std::numbers::pi*std::numbers::pi);
  if(q>1&&q<2.25)neff.push_back(std::sqrt(q));
 }
 std::sort(neff.rbegin(),neff.rend());return neff;
}
#ifndef HS_SLAB_LIBRARY
int main(int argc,char**argv){
 const int refinement=argc==2?std::atoi(argv[1]):1;
 if(refinement<1||refinement>8)return 2;
 const auto start=std::chrono::steady_clock::now();auto data=assemble(refinement);
 const auto assembled=std::chrono::steady_clock::now();const int n=data.n;auto values=solve(std::move(data));
 const auto finished=std::chrono::steady_clock::now();
 std::cout<<std::setprecision(17)<<"language,refinement,dofs,assembly_seconds,eigensolve_seconds,te0_neff,tm0_neff,guided_modes\n";
 if(values.size()<2)return 4;
 std::cout<<"cpp,"<<refinement<<','<<n<<','<<std::chrono::duration<double>(assembled-start).count()<<','<<std::chrono::duration<double>(finished-assembled).count()<<','<<values[0]<<','<<values[1]<<','<<values.size()<<'\n';
}

#endif
