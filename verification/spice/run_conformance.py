# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Launch native engines and compare outputs; Python contains no circuit solver."""
import argparse,json,subprocess,pathlib
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--work',type=pathlib.Path,required=True);p.add_argument('--ng-model',required=True);p.add_argument('--xy-model',required=True);p.add_argument('--xyce',required=True);a=p.parse_args();a.work.mkdir(exist_ok=True,parents=True)
results=[]
def run(kind,engine,analysis):
 deck=a.work/f'{kind}-{engine}-{analysis}.cir'
 subprocess.run([str(a.work/'emit'),kind,engine,analysis,a.ng_model if engine=='ngspice' else a.xy_model,str(deck)],check=True)
 with deck.with_suffix('.log').open('w') as log:
  cmd=[str(a.work/'ng-run'),str(deck),analysis,str(deck)+'.csv'] if engine=='ngspice' else [a.xyce,str(deck)]
  r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=pathlib.Path(a.ng_model if engine=='ngspice' else a.xy_model).parent)
 if r.returncode: return None
 file=str(deck)+('.HB.FD.csv' if analysis=='hb' else '.FD.csv' if analysis=='ac' and engine=='xyce' else '.csv')
 try: return np.loadtxt(file,delimiter=',',skiprows=1)
 except (ValueError,FileNotFoundError): return None
for kind in ['rc','rlc','diode','ihp']:
 for analysis in ['dc','ac','tran']:
  ng=run(kind,'ngspice',analysis);xy=run(kind,'xyce',analysis)
  if ng is None or xy is None:
   results.append(dict(circuit=kind,analysis=analysis,status='FAIL_RUN'));continue
  # Xyce DC starts INDEX,VDRIVE; time/AC start scale. ng has fixed real/imag columns.
  if analysis=='dc': xs=xy[:,0]; xv=xy[:,1]; nv=ng[:,1]
  elif analysis=='ac': xs=xy[:,0];xv=xy[:,1]+1j*xy[:,2];nv=ng[:,1]+1j*ng[:,2]
  else: xs=xy[:,0];xv=xy[:,1];nv=ng[:,1]
  keep=(ng[:,0]>=xs.min())&(ng[:,0]<=xs.max());ns=ng[keep,0];nv=nv[keep]
  interp=np.interp(ns,xs,xv)
  error=float(np.sqrt(np.mean(abs(nv-interp)**2))/max(float(np.sqrt(np.mean(abs(nv)**2))),1e-12))
  ni=ng[keep,3]+1j*ng[keep,4]
  xi=(xy[:,3]+1j*xy[:,4]) if analysis=='ac' else xy[:,2]
  ci=np.interp(ns,xs,xi)
  current_error=float(np.sqrt(np.mean(abs(ni-ci)**2))/max(float(np.sqrt(np.mean(abs(ni)**2))),1e-12))
  tol=1e-4 if analysis=='dc' else 1e-3
  results.append(dict(circuit=kind,analysis=analysis,voltage_relative_rms=error,current_relative_rms=current_error,tolerance=tol,status='PASS' if max(error,current_error)<tol else 'FAIL',ng_samples=len(ng),xy_samples=len(xy)))
for kind in ['rlc','cubic']:
 hb=run(kind,'xyce','hb')
 if hb is None: results.append(dict(circuit=kind,analysis='hb',status='FAIL_RUN'));continue
 row=hb[np.argmin(abs(hb[:,0]-1e6))];omega=2*np.pi*1e6
 if kind=='rlc':
  expected=1/(1000+1j*(omega*.001-1/(omega*1e-9)))
  # SIN source positive-frequency coefficient -j/2; current source sign opposite load.
  measured=complex(row[3],row[4])/complex(row[1],row[2]) # I(source)/V(cap), use actual input Fourier phase below
  measured=-complex(row[3],row[4])/(-.5j)
  error=abs(measured-expected)/abs(expected)
 else:
  third=hb[np.argmin(abs(hb[:,0]-3e6))]
  measured=2*abs(complex(row[3],row[4])); expected=.001075
  third_amp=2*abs(complex(third[3],third[4]));error=max(abs(measured-expected)/expected,abs(third_amp-.000025)/.000025)
 results.append(dict(circuit=kind,analysis='hb',relative_error=float(error),tolerance=1e-3,status='PASS' if error<1e-3 else 'FAIL'))
ng=run('cubic','ngspice','tran')
if ng is not None:
 grid=np.linspace(9e-6,10e-6,4096,endpoint=False)
 samples=np.interp(grid,ng[:,0],-ng[:,3]); spectrum=np.fft.rfft(samples)/len(samples)
 fundamental=2*abs(spectrum[1]);third=2*abs(spectrum[3])
 error=max(abs(fundamental-.001075)/.001075,abs(third-.000025)/.000025)
 results.append(dict(circuit='cubic',analysis='ngspice_transient_fft',fundamental_a=float(fundamental),third_harmonic_a=float(third),relative_error=float(error),tolerance=1e-3,status='PASS' if error<1e-3 else 'FAIL'))
else: results.append(dict(circuit='cubic',analysis='ngspice_transient_fft',status='FAIL_RUN'))
print(json.dumps(results,indent=2));(a.work/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(r['status']!='PASS' for r in results))
