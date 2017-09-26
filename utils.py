import glob

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch


def return_shp_path_from_folder(folder_path):

    extention = '.shp'

    search_format = '{}{}{}'.format(folder_path,'/*', extention)

    return glob.glob(search_format)


def plot_fiona_shapefile(shapefile):
    cm = plt.get_cmap('RdBu')
    num_colours = len(shapefile)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    minx, miny, maxx, maxy = mp.bounds
    w, h = maxx - minx, maxy - miny
    ax.set_xlim(minx - 0.2 * w, maxx + 0.2 * w)
    ax.set_ylim(miny - 0.2 * h, maxy + 0.2 * h)
    ax.set_aspect(1)

    patches = []
    for idx, p in enumerate(shapefile):
        colour = cm(1. * idx / num_colours)
        patches.append(PolygonPatch(p, fc=colour, ec='#555555', alpha=1., zorder=1))
    ax.add_collection(PatchCollection(patches, match_original=True))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Shapefile polygons rendered using Shapely")
    # plt.savefig('data/london_from_shp.png', alpha=True, dpi=300)
    plt.show()
