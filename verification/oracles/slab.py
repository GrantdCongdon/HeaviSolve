# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Independent symmetric-slab TE0/TM0 closed-form roots; test code only."""
import math
def fundamental(tm=False):
    k0=2*math.pi
    half_width=0.5
    core_eps,cladding_eps=2.25,1.0
    normalized=k0*half_width*math.sqrt(core_eps-cladding_eps)
    ratio=core_eps/cladding_eps if tm else 1.0
    lo,hi=0.0,min(math.pi/2,normalized)-1e-14
    for _ in range(80):
        u=(lo+hi)/2
        residual=u*math.tan(u)-ratio*math.sqrt(normalized**2-u*u)
        if residual>0:hi=u
        else:lo=u
    u=(lo+hi)/2
    assert abs(u*math.tan(u)-ratio*math.sqrt(normalized**2-u*u))<1e-12
    result=math.sqrt(core_eps-(u/(k0*half_width))**2)
    assert math.sqrt(cladding_eps)<result<math.sqrt(core_eps)
    return result
