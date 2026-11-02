// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <mfem.hpp>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numbers>
#include <vector>
using namespace mfem;
int main() {
  constexpr int n=4, order=3;
  Mesh mesh=Mesh::MakeCartesian3D(n,n,n,Element::HEXAHEDRON,1.,.8,.6);
  ND_FECollection fec(order,3); FiniteElementSpace space(&mesh,&fec);
  Array<int> boundary(mesh.bdr_attributes.Max()); boundary=1;
  Array<int> essential; space.GetEssentialTrueDofs(boundary,essential);
  std::vector<bool> constrained(space.GetVSize(),false);
  for(int i:essential) constrained[i]=true;
  std::vector<int> free;
  for(int i=0;i<space.GetVSize();++i) if(!constrained[i]) free.push_back(i);
  BilinearForm stiffness(&space), mass(&space);
  stiffness.AddDomainIntegrator(new CurlCurlIntegrator);
  mass.AddDomainIntegrator(new VectorFEMassIntegrator);
  stiffness.Assemble(); stiffness.Finalize(); mass.Assemble(); mass.Finalize();
  DenseMatrix K(free.size()),M(free.size());
  const SparseMatrix &ks=stiffness.SpMat(), &ms=mass.SpMat();
  for(int i=0;i<K.Height();++i) for(int j=0;j<K.Width();++j) {
    K(i,j)=ks(free[i],free[j]); M(i,j)=ms(free[i],free[j]);
  }
  Vector eigenvalues; K.Eigenvalues(M,eigenvalues);
  int zeros=0; std::vector<double> positive;
  bool pass=true;
  for(int i=0;i<eigenvalues.Size();++i) {
    const double x=eigenvalues[i];
    if(!std::isfinite(x) || x < -1e-7) pass=false;
    else if(std::abs(x)<1e-7) ++zeros;
    else positive.push_back(x);
  }
  std::sort(positive.begin(),positive.end());
  std::vector<double> oracle;
  for(int i=0;i<8;++i) for(int j=0;j<8;++j) for(int k=0;k<8;++k) {
    int nonzero=(i>0)+(j>0)+(k>0);
    if(nonzero<2) continue;
    const double e=std::numbers::pi*std::numbers::pi*(i*i+j*j/.64+k*k/.36);
    oracle.push_back(e); if(nonzero==3) oracle.push_back(e);
  }
  std::sort(oracle.begin(),oracle.end());
  const int expected_zeros=(n*order-1)*(n*order-1)*(n*order-1);
  pass &= zeros==expected_zeros && positive.size()>=6;
  std::cout<<std::setprecision(17)<<"free_dofs="<<free.size()<<" null_modes="<<zeros
           <<" expected_gradient_nullity="<<expected_zeros<<"\nmode,lambda,analytic_lambda,frequency_relative_error\n";
  for(int i=0;i<6 && i<static_cast<int>(positive.size());++i) {
    const double error=std::abs(std::sqrt(positive[i]/oracle[i])-1);
    std::cout<<i<<','<<positive[i]<<','<<oracle[i]<<','<<error<<'\n';
    pass &= error<1e-3;
  }
  return pass?0:1;
}
