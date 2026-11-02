// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <mfem.hpp>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numbers>
using namespace mfem;
constexpr double pi = std::numbers::pi;
double exact(const Vector &x) { return std::sin(pi*x[0])*std::sin(pi*x[1]); }
double rhs(const Vector &x) { return 2*pi*pi*exact(x); }
int main() {
  double previous = 0;
  bool pass = true;
  std::cout << std::setprecision(17) << "n,dofs,l2_error,observed_order\n";
  for (int n : {8,16,32,64}) {
    Mesh mesh = Mesh::MakeCartesian2D(n,n,Element::TRIANGLE,true);
    H1_FECollection fec(1,2); FiniteElementSpace space(&mesh,&fec);
    Array<int> boundary(mesh.bdr_attributes.Max()); boundary=1;
    Array<int> essential; space.GetEssentialTrueDofs(boundary,essential);
    GridFunction solution(&space); solution=0.;
    FunctionCoefficient f(rhs), oracle(exact);
    LinearForm b(&space); b.AddDomainIntegrator(new DomainLFIntegrator(f)); b.Assemble();
    BilinearForm a(&space); a.AddDomainIntegrator(new DiffusionIntegrator); a.Assemble();
    OperatorPtr A; Vector X,B;
    a.FormLinearSystem(essential,solution,b,A,X,B);
    GSSmoother preconditioner(static_cast<SparseMatrix&>(*A));
    PCG(*A,preconditioner,B,X,0,2000,1e-14,0.);
    a.RecoverFEMSolution(X,b,solution);
    const double error=solution.ComputeL2Error(oracle);
    const double rate=previous ? std::log2(previous/error) : 0;
    std::cout<<n<<','<<space.GetTrueVSize()<<','<<error<<','<<rate<<'\n';
    pass &= std::isfinite(error) && error>0 && (!previous || (rate>1.85 && rate<2.15));
    previous=error;
  }
  return pass?0:1;
}
