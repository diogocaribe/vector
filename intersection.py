from shapely.geometry import shape
import pandas as pd
import fiona
import rtree


def intersection_shape_idx(filename1, filename2):

    result = pd.DataFrame({'nome': [],
                           'Class_Name': [],
                           'geometry': [],
                           'area_class': []})

    with fiona.open(filename1, 'r', encoding='UTF-8') as layer1:

        with fiona.open(filename2, 'r') as layer2:

            features = {}
            index = rtree.index.Index()
            for feat1 in layer1:
                fid = int(feat1['id'])
                geom1 = shape(feat1['geometry'])
                index.insert(fid, geom1.bounds)
                features[fid] = (feat1, geom1,)

            for feat2 in layer2:
                geom2 = shape(feat2['geometry'])
                for fid in list(index.intersection(geom2.bounds)):
                    feat1, geom1 = features[fid]
                    try:
                        if geom1.intersects(geom2):
                            intersect = pd.DataFrame({'nome': [feat1['properties']['nome']],
                                                      'Class_Name': [feat2['properties']['Class_Name']],
                                                      'geometry': [geom1.intersection(geom2).to_wkt()],
                                                       'area_class': [geom1.intersection(geom2).area]},
                                                     index = [feat2['id']])
                            result = pd.concat([result, intersect])

                    except Exception as e:
                        print(e)
                        if not geom1.is_valid:
                            geom1 = geom1.buffer(0)
                        if not geom2.is_valid:
                            geom2 = geom2.buffer(0)
                        if geom1.intersects(geom2):
                            intersect = pd.DataFrame({'nome': [feat1['properties']['nome']],
                                                      'Class_Name': [feat2['properties']['Class_Name']],
                                                      'geometry': [geom1.intersection(geom2).to_wkt()],
                                                       'area_class': [geom1.intersection(geom2).area]},
                                                     index = [feat2['id']])
                            result = pd.concat([result, intersect])

        return result
