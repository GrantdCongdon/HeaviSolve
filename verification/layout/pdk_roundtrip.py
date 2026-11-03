# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Compare candidate serializers on external public PDK fixtures; no PDK bundled."""
import pathlib
import tempfile
import gdstk
import klayout.db as kdb
ROOT=pathlib.Path(__file__).resolve().parents[2]
def regions(layout):
    result={}
    for li in layout.layer_indices():
        info=layout.get_info(li)
        region=kdb.Region()
        for top in layout.top_cells():region+=kdb.Region(top.begin_shapes_rec(li))
        region.merge()
        result[(info.layer,info.datatype)]=region
    return result
selected_pass=True
for name in ('siepic-ring','ihp-stdcell'):
    fixture=ROOT/'.work/s6'/f'{name}.gds'
    original=kdb.Layout();original.read(str(fixture));expected=regions(original)
    library=gdstk.read_gds(str(fixture))
    original_cells={c.name for c in original.each_cell()}
    print('fixture',name,'serialized_internal_cells',sorted({c.name for c in library.cells}-original_cells))
    with tempfile.TemporaryDirectory(prefix='heavisolve-pdk-') as tmp:
        for engine in ('gdstk','klayout'):
            for fmt in ('gds','oas'):
                output=pathlib.Path(tmp)/f'{engine}-roundtrip.{fmt}'
                if engine=='gdstk':getattr(library,'write_'+fmt)(str(output))
                else:original.write(str(output))
                loaded=kdb.Layout();loaded.read(str(output));actual=regions(loaded)
                same_units=loaded.dbu==original.dbu
                same_layers=set(expected)==set(actual)
                difference=sum((region^actual.get(layer,kdb.Region())).area() for layer,region in expected.items())
                difference+=sum(region.area() for layer,region in actual.items() if layer not in expected)
                actual_cells={c.name for c in loaded.each_cell()}
                same_cells=actual_cells==original_cells
                passed=same_units and same_layers and difference==0 and same_cells
                print(f'fixture={name} engine={engine} format={fmt} cells={len(actual_cells)} layers={len(actual)} filled_geometry_xor_area_dbu2={difference} same_units={same_units} same_cells={same_cells} status={"PASS" if passed else "FAIL"}')
                if engine=='klayout':selected_pass &= passed
print('selection=KLayout_for_PDK_roundtrip; gdstk_context_metadata_conversion_not_lossless')
print('not_tested=PCell_parameter_regeneration,all_properties,text_semantics')
raise SystemExit(0 if selected_pass else 1)
