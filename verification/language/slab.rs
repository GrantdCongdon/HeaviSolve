// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
use std::f64::consts::PI;
use std::time::Instant;
#[cfg_attr(target_os="macos", link(name="Accelerate", kind="framework"))]
#[cfg_attr(not(target_os="macos"), link(name="lapack"))]
unsafe extern "C" {
 fn dggev_(jl:*const u8,jr:*const u8,n:*const i32,a:*mut f64,lda:*const i32,b:*mut f64,ldb:*const i32,ar:*mut f64,ai:*mut f64,beta:*mut f64,vl:*mut f64,ldvl:*const i32,vr:*mut f64,ldvr:*const i32,work:*mut f64,lwork:*const i32,info:*mut i32);
}
fn assemble(r:usize)->(usize,Vec<f64>,Vec<f64>) {
 let (nc,cl,ny)=(16*r,12*r,2);let mut x=Vec::new();
 for j in (1..=cl).rev(){x.push(-0.5-4.0*(j*j) as f64/(cl*cl) as f64);}
 for j in 0..=nc{x.push(-0.5+j as f64/nc as f64);}
 for j in 1..=cl{x.push(0.5+4.0*(j*j) as f64/(cl*cl) as f64);}
 let nx=x.len()-1;let ne=(2*nx-1)*ny;let nn=(nx-1)*ny;let n=ne+nn;
 let mut a=vec![0.;n*n];let mut b=vec![0.;n*n];
 let h=|i:usize,j:usize|Some(i*ny+j%ny);
 let v=|i:usize,j:usize|if i==0||i==nx {None}else{Some(nx*ny+(i-1)*ny+j%ny)};
 let node=|i:usize,j:usize|if i==0||i==nx{None}else{Some(ne+(i-1)*ny+j%ny)};
 let k2=4.*PI*PI;let q=[0.5-0.5/3_f64.sqrt(),0.5+0.5/3_f64.sqrt()];
 for ix in 0..nx {for iy in 0..ny {
  let dx=x[ix+1]-x[ix];let dy=0.2/ny as f64;let det=dx*dy;
  let eps=if (0.5*(x[ix]+x[ix+1])).abs()<0.5 {2.25}else{1.};
  let edges=[h(ix,iy),v(ix+1,iy),h(ix,iy+1),v(ix,iy)];
  let nodes=[node(ix,iy),node(ix+1,iy),node(ix+1,iy+1),node(ix,iy+1)];
  let curl=[1./det,1./det,-1./det,-1./det];
  for u in q {for w in q {
   let basis=[[(1.-w)/dx,0.],[0.,u/dy],[w/dx,0.],[0.,(1.-u)/dy]];
   let phi=[(1.-u)*(1.-w),u*(1.-w),u*w,(1.-u)*w];
   let grad=[[-(1.-w)/dx,-(1.-u)/dy],[(1.-w)/dx,-u/dy],[w/dx,u/dy],[-w/dx,(1.-u)/dy]];
   let weight=det/4.;
   for i in 0..4 {for j in 0..4 {
    if let (Some(ei),Some(ej))=(edges[i],edges[j]) {
     let m=basis[i][0]*basis[j][0]+basis[i][1]*basis[j][1];
     a[ei+ej*n]+=weight*(k2*eps*m-curl[i]*curl[j]);b[ei+ej*n]+=weight*m;
    }
    if let (Some(ni),Some(nj))=(nodes[i],nodes[j]) {
     b[ni+nj*n]+=weight*(grad[i][0]*grad[j][0]+grad[i][1]*grad[j][1]-k2*eps*phi[i]*phi[j]);
    }
    if let (Some(ei),Some(nj))=(edges[i],nodes[j]) {
     let g=weight*(basis[i][0]*grad[j][0]+basis[i][1]*grad[j][1]);
     b[ei+nj*n]+=g;b[nj+ei*n]+=g;
    }
   }}
  }}
 }}
 (n,a,b)
}
fn solve(n:usize,mut a:Vec<f64>,mut b:Vec<f64>)->Vec<f64>{
 let size=n as i32;let one=1_i32;let no=b'N';let mut info=0_i32;
 let(mut ar,mut ai,mut beta)=(vec![0.;n],vec![0.;n],vec![0.;n]);
 let(mut vl,mut vr,mut query)=(0.,0.,0.);let request=-1_i32;
 unsafe{dggev_(&no,&no,&size,a.as_mut_ptr(),&size,b.as_mut_ptr(),&size,ar.as_mut_ptr(),ai.as_mut_ptr(),beta.as_mut_ptr(),&mut vl,&one,&mut vr,&one,&mut query,&request,&mut info);}
 assert_eq!(info,0);let work_size=query as i32;let mut work=vec![0.;work_size as usize];
 unsafe{dggev_(&no,&no,&size,a.as_mut_ptr(),&size,b.as_mut_ptr(),&size,ar.as_mut_ptr(),ai.as_mut_ptr(),beta.as_mut_ptr(),&mut vl,&one,&mut vr,&one,work.as_mut_ptr(),&work_size,&mut info);}
 assert_eq!(info,0);let mut values=Vec::new();
 for i in 0..n {if ai[i].abs()<1e-9&&beta[i].abs()>1e-14 {
  let v=ar[i]/beta[i]/(4.*PI*PI);if v>1.&&v<2.25 {values.push(v.sqrt());}
 }}
 values.sort_by(|a,b|b.total_cmp(a));values
}
fn main(){
 let args:Vec<String>=std::env::args().collect();let r:usize=args.get(1).map(|x|x.parse().unwrap()).unwrap_or(1);
 assert!((1..=8).contains(&r));let start=Instant::now();let(n,a,b)=assemble(r);let assembled=Instant::now();let values=solve(n,a,b);let finished=Instant::now();assert!(values.len()>=2);
 println!("language,refinement,dofs,assembly_seconds,eigensolve_seconds,te0_neff,tm0_neff,guided_modes");
 println!("rust,{r},{n},{:.17},{:.17},{:.17},{:.17},{}",assembled.duration_since(start).as_secs_f64(),finished.duration_since(assembled).as_secs_f64(),values[0],values[1],values.len());
}
