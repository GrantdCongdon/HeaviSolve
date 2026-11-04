// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <mfem.hpp>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numbers>
#include <sstream>
int main(){
 constexpr int sectors=128;constexpr double inner=9,outer=10,height=.5;
 mfem::Mesh mesh(3,4*sectors,2*sectors,6*sectors,3);
 auto vertex=[](int z,int radius,int sector){return (2*z+radius)*sectors+sector%sectors;};
 for(int z=0;z<2;++z)for(int radial=0;radial<2;++radial)for(int i=0;i<sectors;++i){
  double a=2*std::numbers::pi*i/sectors,r=radial?outer:inner;
  double point[3]={r*std::cos(a),r*std::sin(a),z*height};mesh.AddVertex(point);
 }
 for(int i=0;i<sectors;++i){
  const int triangles[2][3]={{vertex(0,0,i),vertex(0,1,i),vertex(0,1,i+1)},
                             {vertex(0,0,i),vertex(0,1,i+1),vertex(0,0,i+1)}};
  for(const auto& t:triangles){
   mesh.AddWedge(t[0],t[1],t[2],t[0]+2*sectors,t[1]+2*sectors,t[2]+2*sectors,1);
   mesh.AddBdrTriangle(t[2],t[1],t[0],1);
   mesh.AddBdrTriangle(t[0]+2*sectors,t[1]+2*sectors,t[2]+2*sectors,2);
  }
  mesh.AddBdrQuad(vertex(0,1,i),vertex(0,1,i+1),vertex(1,1,i+1),vertex(1,1,i),3);
  mesh.AddBdrQuad(vertex(0,0,i+1),vertex(0,0,i),vertex(1,0,i),vertex(1,0,i+1),4);
 }
 mesh.FinalizeWedgeMesh(1,0,true);
 double volume=0,min_jacobian=1e100,min_scaled=1;
 for(int e=0;e<mesh.GetNE();++e){
  auto* transform=mesh.GetElementTransformation(e);
  const auto& rule=mfem::IntRules.Get(mfem::Geometry::PRISM,3);
  for(int q=0;q<rule.GetNPoints();++q){
   const auto& point=rule.IntPoint(q);transform->SetIntPoint(&point);
   const auto& J=transform->Jacobian();double determinant=J.Det(),norms=1;
   for(int j=0;j<3;++j){double norm=0;for(int k=0;k<3;++k)norm+=J(k,j)*J(k,j);norms*=std::sqrt(norm);}
   min_jacobian=std::min(min_jacobian,determinant);min_scaled=std::min(min_scaled,determinant/norms);
   volume+=point.weight*determinant;
  }
 }
 const double polygon_volume=.5*sectors*(outer*outer-inner*inner)*std::sin(2*std::numbers::pi/sectors)*height;
 const double circle_volume=std::numbers::pi*(outer*outer-inner*inner)*height;
 std::stringstream stream;mesh.Print(stream);mfem::Mesh imported(stream,1,1);
 mfem::ND_FECollection fec(1,3);mfem::FiniteElementSpace space(&imported,&fec);
 mfem::BilinearForm mass(&space);mass.AddDomainIntegrator(new mfem::VectorFEMassIntegrator);mass.Assemble();mass.Finalize();
 bool pass=std::isfinite(volume)&&min_jacobian>0&&min_scaled>.05&&std::abs(volume/polygon_volume-1)<1e-12&&std::abs(volume/circle_volume-1)<1e-3&&imported.GetNE()==2*sectors&&imported.GetNBE()==6*sectors;
 std::cout<<std::setprecision(17)<<"wedges="<<imported.GetNE()<<" boundary_elements="<<imported.GetNBE()<<" hcurl_dofs="<<space.GetVSize()<<" volume="<<volume<<" exact_polygon_volume="<<polygon_volume<<" circular_relative_error="<<std::abs(volume/circle_volume-1)<<" min_jacobian="<<min_jacobian<<" min_scaled_jacobian="<<min_scaled<<" status="<<(pass?"PASS":"FAIL")<<'\n';
 return pass?0:1;
}
