// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <mfem.hpp>
#include <slepceps.h>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numbers>
#include <vector>
// Research-only bridge: independently assembled MFEM matrices copied into PETSc.
// One MPI rank keeps this spike small; multi-rank scaling is a separate benchmark.
int main(int argc,char**argv) {
 PetscCall(SlepcInitialize(&argc,&argv,nullptr,nullptr));
 int ranks=0;MPI_Comm_size(PETSC_COMM_WORLD,&ranks);
 if(ranks!=1){std::cerr<<"This diagnostic requires one MPI rank\n";return 2;}
 mfem::Device device("cpu");
 auto mesh=mfem::Mesh::MakeCartesian3D(4,4,4,mfem::Element::HEXAHEDRON,1.,.8,.6);
 mfem::ND_FECollection fec(3,3);mfem::FiniteElementSpace space(&mesh,&fec);
 mfem::Array<int> boundary(mesh.bdr_attributes.Max());boundary=1;
 mfem::Array<int> essential;space.GetEssentialTrueDofs(boundary,essential);
 std::vector<bool> fixed(space.GetVSize(),false);for(int i:essential)fixed[i]=true;
 std::vector<int> free,local(space.GetVSize(),-1);
 for(int i=0;i<space.GetVSize();++i)if(!fixed[i]){local[i]=free.size();free.push_back(i);}
 mfem::BilinearForm stiffness(&space),mass(&space);
 stiffness.AddDomainIntegrator(new mfem::CurlCurlIntegrator);
 mass.AddDomainIntegrator(new mfem::VectorFEMassIntegrator);
 stiffness.Assemble();stiffness.Finalize();mass.Assemble();mass.Finalize();
 auto transfer=[&](const mfem::SparseMatrix& source,Mat* target)->PetscErrorCode {
  PetscFunctionBeginUser;
  const PetscInt size=free.size();PetscCall(MatCreateSeqAIJ(PETSC_COMM_SELF,size,size,150,nullptr,target));
  PetscCall(MatSetOption(*target,MAT_NEW_NONZERO_ALLOCATION_ERR,PETSC_FALSE));
  for(PetscInt i=0;i<size;++i){
   const int row=free[i];const int* cols=source.GetRowColumns(row);const double* vals=source.GetRowEntries(row);
   for(int j=0;j<source.RowSize(row);++j)if(local[cols[j]]>=0)PetscCall(MatSetValue(*target,i,local[cols[j]],vals[j],INSERT_VALUES));
  }
  PetscCall(MatAssemblyBegin(*target,MAT_FINAL_ASSEMBLY));PetscCall(MatAssemblyEnd(*target,MAT_FINAL_ASSEMBLY));
  PetscFunctionReturn(PETSC_SUCCESS);
 };
 Mat K,M;PetscCall(transfer(stiffness.SpMat(),&K));PetscCall(transfer(mass.SpMat(),&M));
 EPS eps;PetscCall(EPSCreate(PETSC_COMM_SELF,&eps));PetscCall(EPSSetOperators(eps,K,M));
 PetscCall(EPSSetProblemType(eps,EPS_GHEP));PetscCall(EPSSetType(eps,EPSKRYLOVSCHUR));
 PetscCall(EPSSetDimensions(eps,6,24,PETSC_DEFAULT));PetscCall(EPSSetTarget(eps,30.));
 PetscCall(EPSSetWhichEigenpairs(eps,EPS_TARGET_REAL));PetscCall(EPSSetTolerances(eps,1e-10,300));
 ST st;KSP ksp;PC pc;PetscCall(EPSGetST(eps,&st));PetscCall(STSetType(st,STSINVERT));
 PetscCall(STGetKSP(st,&ksp));PetscCall(KSPSetType(ksp,KSPPREONLY));PetscCall(KSPGetPC(ksp,&pc));
 PetscCall(PCSetType(pc,PCLU));PetscCall(PCFactorSetMatSolverType(pc,MATSOLVERSUPERLU_DIST));
 PetscCall(EPSSetFromOptions(eps));PetscCall(EPSSolve(eps));
 PetscInt converged;PetscCall(EPSGetConverged(eps,&converged));
 std::vector<double> got;
 for(PetscInt i=0;i<converged;++i){PetscScalar ev;PetscCall(EPSGetEigenvalue(eps,i,&ev,nullptr));
  if(std::abs(PetscImaginaryPart(ev))>1e-7)return 3;
  if(PetscRealPart(ev)>1e-6)got.push_back(PetscRealPart(ev));
 }
 std::sort(got.begin(),got.end());
 std::vector<double> exact;
 for(int i=0;i<8;++i)for(int j=0;j<8;++j)for(int k=0;k<8;++k){
  int nz=(i>0)+(j>0)+(k>0);if(nz<2)continue;
  double e=std::numbers::pi*std::numbers::pi*(i*i+j*j/.64+k*k/.36);exact.push_back(e);if(nz==3)exact.push_back(e);
 }
 std::sort(exact.begin(),exact.end());bool pass=got.size()>=6;
 std::cout<<std::setprecision(17)<<"mfem="<<mfem::GetVersionStr()<<" scalar=complex direct=SuperLU_DIST ranks="<<ranks<<" dofs="<<free.size()<<" converged="<<converged<<"\nmode,lambda,frequency_relative_error\n";
 for(std::size_t i=0;i<std::min<std::size_t>(6,got.size());++i){double error=std::abs(std::sqrt(got[i]/exact[i])-1);std::cout<<i<<','<<got[i]<<','<<error<<'\n';pass &= error<1e-3;}
 PetscCall(EPSDestroy(&eps));PetscCall(MatDestroy(&K));PetscCall(MatDestroy(&M));
 PetscCall(SlepcFinalize());return pass?0:1;
}
