from Vector import Vector
import intersection as i
import utils as u
import time
import intersection_thread as it

path = '../vector/'

municipio_path = '{}{}'.format(path, 'municipio/municipio.shp')

landuse_path = '{}{}'.format(path, 'landuse/')


if __name__ == '__main__':

    # municipio = Vector(municipio_path)
    only_shp = u.return_shp_path_from_folder(landuse_path)

    for shp_path in only_shp:

        landuse_date = Vector(shp_path).get_basename()

        start = time.time()
        inter = it.intersection_shape_idx(municipio_path, shp_path)
        # inter = i.intersection_shape_idx(municipio_path, shp_path)
        end = time.time()
        print(end-start)
        inter['data'] = landuse_date

        print(inter)