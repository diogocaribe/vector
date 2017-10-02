from Vector import Vector
import intersection as i
import utils as u

path = '../vector/'

municipio_path = '{}{}'.format(path, 'municipio/municipio.shp')

landuse_path = '{}{}'.format(path, 'landuse/')


if __name__ == '__main__':

    # municipio = Vector(municipio_path)
    only_shp = u.return_shp_path_from_folder(landuse_path)

    for shp_path in only_shp:

        landuse_date = Vector(shp_path).get_basename()

        inter = i.intersection_shape_idx(municipio_path, shp_path)

        inter['year'] = landuse_date[:4]
        inter['month'] = landuse_date[5:6]
        inter['day'] = landuse_date[6:8]

        u.save_pandas_csv(dataframe=inter, file_name=landuse_date)

        print("ok")
