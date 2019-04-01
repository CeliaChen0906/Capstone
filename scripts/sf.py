import pandas as pd
import numpy as np
import math
from collections import defaultdict
from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

sfdfc = pd.read_csv(join(_cwd, '../data/sfdfc.csv'), index_col = 0)
nydfc = pd.read_csv(join(_cwd, '../data/nydfc.csv'), index_col = 0)


def recommendation_coor(sflat, sflong):
"""
    Generate recommedation coordinates.

    Arguments:
    San Francisco city Latitude, longitude

    Returns:
    Recommended coordinates in New York
"""
#find FIPS
    sf_distance = defaultdict(int)
    ny_rec = defaultdict(int)
    for i in range(len(sfdfc)):
        sf_distance[i] = np.sqrt((sflat - sfdfc['INTPTLAT'][i])**2 + (sflong - sfdfc['INTPTLONG                                                                                                                  '][i])**2)
    for index, v in sf_distance.iteritems():
        if v == min(sf_distance.values()):
            j = index
#how many recommendation you want?
    n = 20
    sf_l = sfdfc['liquordensereal'][j:j+1].values[0]
    sf_p = sfdfc['popdensereal'][j:j+1].values[0]
    sf_h = sfdfc['housedensereal'][j:j+1].values[0]
    for q in range(len(nydfc)):
        ny_rec[q] = (np.sqrt((sf_l - nydfc['liquordensereal'][q])**2)
         + np.sqrt((sf_p - nydfc['popdensereal'][q])**2) +
        np.sqrt((sf_h - nydfc['housedensereal'][q])**2))
    
    res = sorted(ny_rec.items(), key = lambda x:x[1])

    res_coor = []
    for c in range(n):
        index = res[:n][c][0]
        lat = nydfc['INTPTLAT'][index]
        lon = nydfc['INTPTLONG                                                                                                                  '][index]
        if lat < 40.89 and lon > -74.049835 and lon < -73.81:
            co = (lat, lon)
            res_coor.append(co)
    goog_map_points = []
    for i in res_coor:
        goog_map_points.append('new google.maps.LatLng'+str(i))
    return goog_map_points