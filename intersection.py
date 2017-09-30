from shapely.geometry import shape
import pandas as pd
import fiona
import rtree


def intersection_shape_idx(filename1, filename2):

    result = pd.DataFrame({'nome': [],
                           'Class_Name': [],
                           'geometry': [],
                           'int_area_m': [],
                           'area_munic': []})

    with fiona.open(filename1, 'r') as layer1:

        with fiona.open(filename2, 'r') as layer2:

            index = rtree.index.Index()
            for feat1 in layer1:
                fid = int(feat1['id'])
                geom1 = shape(feat1['geometry'])
                index.insert(fid, geom1.bounds)

            for feat2 in layer2:
                geom2 = shape(feat2['geometry'])
                for fid in list(index.intersection(geom2.bounds)):
                    feat1 = layer1[fid]
                    geom1 = shape(feat1['geometry'])
                    if geom1.intersects(geom2):
                        # print('{} intersects {}'.format(feat2['id'], feat1['id']))
                        intersect = pd.DataFrame({'nome': [feat1['properties']['nome']],
                                                  'Class_Name': [feat2['properties']['Class_Name']],
                                                  'geometry': [geom1.intersection(geom2).to_wkt()],
                                                   'int_area_m': [geom1.intersection(geom2).area],
                                                  'area_munic': geom1.area},
                                                 index = [feat2['id']])
                        # result = result.append(intersect, ignore_index=True)
                        result = pd.concat([result, intersect])
        return result
