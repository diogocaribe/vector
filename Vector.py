# -*- coding: UTF-8 -*-

import os
import fiona
from shapely.geometry import shape, MultiPolygon, Polygon, LineString, MultiLineString
import rtree


class Vector:

    def __init__(self, vector_path):

        # Instatiating vector path
        self.vector_path = os.path.abspath(vector_path)

    def read_shapefile(self):

        try:
            c = fiona.open(self.vector_path)
            pol = c.next()
            geom = shape(pol['geometry'])

            return geom

        except ValueError:
            print('Error in read_shapefile_ogr')

    def read_shp_fiona_index(self):

        with fiona.open(self.vector_path, 'r') as layer:
            index = rtree.index.Index()
            for feat1 in layer:
                fid = int(feat1['id'])
                geom1 = shape(feat1['geometry'])
                index.insert(fid, geom1.bounds)

            return layer

    def get_basename(self):
        """
        :return: Name of file with extension
        """
        # Name of file with extension
        basename = os.path.basename(self.vector_path)

        return basename

    def get_file_name(self):
        """
        :return: 
        """
        base_name = self.get_basename()

        file_name = os.path.splitext(base_name)[0]

        return file_name

    def get_multigeom_from_shapefile(self):
        """
        :return: Return multi geometry from shape file which own primitive geometry 
         (line, polygon or point)
        """
        try:

            if type(self.read_shapefile()) is Polygon:
                multigeom = MultiPolygon([shape(pol['geometry']) for pol in fiona.open(self.vector_path)])
            elif type(self.read_shapefile()) is LineString:
                multigeom = MultiLineString([shape(pol['geometry']) for pol in fiona.open(self.vector_path)])

            return multigeom

        except ValueError:
            print('Error in get_multigeom_from_shapefile')