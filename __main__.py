from Vector import Vector
import pandas as pd
import geoutils as gu
import utils as u
import time

path = '/media/dogsousa/56A22ED6A22EBA7F/mestrado_artigo_final/SHP/'

municipio_path = '{}{}'.format(path, 'municipios/municipios_regioes.shp')

# landuse_path = '{}{}{}'.format(path, '/bruto/215_070', '/')
landuse_path = '/media/dogsousa/56A22ED6A22EBA7F/mestrado_artigo_final/SHP/bruto/CORRIGIDO/'

if __name__ == '__main__':

    # municipio = Vector(municipio_path)
    only_shp = u.return_shp_path_from_folder(landuse_path)

    for shp_path in only_shp:

        landuse_date = Vector(shp_path).get_basename()

        print(shp_path)
        print(municipio_path)
        inter = gu.intersection_shape_idx(municipio_path, shp_path)

        inter['data'] = landuse_date

        print(inter)