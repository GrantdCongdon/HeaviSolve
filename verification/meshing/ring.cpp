// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <gmsh.h>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>
int main() {
  gmsh::initialize();
  gmsh::option::setNumber("General.Terminal",0);
  gmsh::model::add("ring-spike");
  const int outer=gmsh::model::occ::addDisk(0,0,0,10,10);
  const int inner=gmsh::model::occ::addDisk(0,0,0,9,9);
  gmsh::vectorpair ring, volume;
  std::vector<gmsh::vectorpair> map;
  gmsh::model::occ::cut({{2,outer}},{{2,inner}},ring,map);
  gmsh::model::occ::extrude(ring,0,0,.5,volume);
  gmsh::model::occ::synchronize();
  gmsh::option::setNumber("Mesh.MeshSizeMin",.35);
  gmsh::option::setNumber("Mesh.MeshSizeMax",.5);
  gmsh::option::setNumber("General.NumThreads",1);
  gmsh::model::mesh::generate(3);
  gmsh::model::mesh::optimize("Netgen");
  std::vector<int> types;
  std::vector<std::vector<std::size_t>> tags,nodes;
  gmsh::model::mesh::getElements(types,tags,nodes,3);
  double minq=1, minjac=1; std::size_t count=0;
  for(const auto& t:tags) {
    std::vector<double> q,j;
    gmsh::model::mesh::getElementQualities(t,q,"minSICN");
    gmsh::model::mesh::getElementQualities(t,j,"minDetJac");
    if(q.empty() || j.empty()) return 2;
    minq=std::min(minq,*std::min_element(q.begin(),q.end()));
    minjac=std::min(minjac,*std::min_element(j.begin(),j.end())); count+=t.size();
  }
  std::cout.precision(17);
  std::cout<<"elements="<<count<<" min_signed_inverse_condition="<<minq<<" min_jacobian="<<minjac<<'\n';
  gmsh::finalize();
  return count>0 && std::isfinite(minq) && minq>.05 && minjac>0?0:1;
}
