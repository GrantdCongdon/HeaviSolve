# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Geometry-only binding exercise, not a numerical solver or viewport benchmark."""
import pathlib
import tempfile
import time
import gdstk
import klayout.db as kdb
with tempfile.TemporaryDirectory(prefix='heavisolve-layout-') as folder:
    folder=pathlib.Path(folder)
    lib=gdstk.Library(unit=1e-6,precision=1e-9)
    cell=lib.new_cell('UNIT')
    ring=gdstk.boolean(gdstk.ellipse((0,0),10,tolerance=.001),
                       gdstk.ellipse((0,0),9,tolerance=.001),'not',precision=.001)
    cell.add(*ring)
    top=lib.new_cell('TOP');top.add(gdstk.Reference(cell,columns=10,rows=10,spacing=(25,25)))
    expected=sum(p.area() for p in top.get_polygons())
    print(f'gdstk_version={gdstk.__version__} klayout_version={kdb.__version__}')
    for fmt in ('gds','oas'):
        path=folder/f'roundtrip.{fmt}'
        getattr(lib,'write_'+fmt)(str(path))
        loaded=getattr(gdstk,'read_'+fmt)(str(path))
        actual=sum(p.area() for p in loaded.top_level()[0].get_polygons())
        assert abs(actual-expected)/expected < 1e-4
        layout=kdb.Layout();layout.read(str(path))
        output=folder/f'klayout.{fmt}';layout.write(str(output))
        check=getattr(gdstk,'read_'+fmt)(str(output))
        area=sum(p.area() for p in check.top_level()[0].get_polygons())
        assert abs(area-expected)/expected < 1e-4
        print(f'format={fmt} area_before_um2={expected:.17g} area_gdstk_um2={actual:.17g} area_klayout_um2={area:.17g} status=PASS_SYNTHETIC')
    start=time.perf_counter()
    million=gdstk.Reference(cell,columns=1000,rows=1000,spacing=(25,25))
    print(f'hierarchical_instances=1000000 creation_seconds={time.perf_counter()-start:.9g} viewport_fps=NOT_MEASURED')
