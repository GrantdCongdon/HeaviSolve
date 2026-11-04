// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <clipper2/clipper.h>
#include <cmath>
#include <iostream>
int main(){
 using namespace Clipper2Lib;
 Paths64 a={{{0,0},{10,0},{10,10},{0,10}}},b={{{5,0},{15,0},{15,10},{5,10}}};
 const double intersection=Area(Intersect(a,b,FillRule::NonZero));
 const double united=Area(Union(a,b,FillRule::NonZero));
 const double difference=Area(Difference(a,b,FillRule::NonZero));
 std::cout<<"intersection="<<intersection<<" union="<<united<<" difference="<<difference<<'\n';
 return intersection==50&&united==150&&difference==50?0:1;
}
