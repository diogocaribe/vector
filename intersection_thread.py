from shapely.geometry import shape
import pandas as pd
import fiona
import rtree
import _thread


def geom_intersection(geom1, geom2):
    return geom1.intersection(geom2)


def intersection_shape_idx(filename1, filename2):

    result = pd.DataFrame({'nome': [],
                           'Class_Name': [],
                           'geometry': [],
                           'int_area_m': []})

    with fiona.open(filename1, 'r') as layer1:

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

                            gintersection = _thread.start_new_thread(geom_intersection(geom1, geom2),
                                                                     ("Inter 1", 2))
                            gintersection1 = _thread.start_new_thread(geom_intersection(geom1, geom2),
                                                                     ("Inter 2", 4))

                            wkt = gintersection.to_wkt()
                            area = gintersection.area

                            intersect = pd.DataFrame({'nome': [feat1['properties']['nome']],
                                                      'Class_Name': [feat2['properties']['Class_Name']],
                                                      'geometry': [wkt],
                                                      'int_area_m': [area]},
                                                      index = [feat2['id']])

                            wkt1 = gintersection1.to_wkt()
                            area1 = gintersection1.area

                            intersect1 = pd.DataFrame({'nome': [feat1['properties']['nome']],
                                                      'Class_Name': [feat2['properties']['Class_Name']],
                                                      'geometry': [wkt1],
                                                      'int_area_m': [area1]},
                                                      index=[feat2['id']])

                            result = pd.concat([result, intersect, intersect1])

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
                                                       'int_area_m': [geom1.intersection(geom2).area],
                                                      'area_munic': geom1.area},
                                                     index = [feat2['id']])
                            result = pd.concat([result, intersect])

        return result
