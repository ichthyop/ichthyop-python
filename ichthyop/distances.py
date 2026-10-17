import re
import pylab as plt
import numpy as np
from matplotlib import path
from matplotlib.patches import Polygon
import xarray as xr
from . import plot
from . import shape
from . import read
from . import zone as _zone
from cartopy.geodesic import Geodesic

# Initialiser l'objet Geodesic (WGS84 par défaut)
gd = Geodesic()

def _compute_point_distance(p1, p2):

    # Définir deux points : (longitude, latitude)
    # Exemple : Paris (2.3522, 48.8566) et Marseille (5.3698, 43.2965)
    results = gd.inverse(p1, p2)
    distance_meters = results[0, 0]
    distance_km = distance_meters / 1000.0
    return distance_km

def compute_distances(data):

    lon = data['lon']
    lat = data['lat']

    lon_ini = data['lon_ini']
    lat_ini = data['lat_ini']

    distances = np.zeros(lon.shape)

    # For the first distance value, computes distance from the initial release location
    for j in range(distances.shape[1]):  # loop over drifters
        distances[0, j] = _compute_point_distance([lon_ini[j], lat_ini[j]], [lon[0, j], lat[0, j]])

    # then, return the distance between two consecutive points
    for i in range(1, distances.shape[0]):  # loop over time
        for j in range(distances.shape[1]):  # loop over drifters
            distances[i, j] = _compute_point_distance([lon[i -1, j], lat[i-1, j]], [lon[i, j], lat[i, j]])

    # Cumsum the distances
    distances = np.cumsum(distances, axis=0) / 1000

    output = xr.Dataset()
    output['drifter'] = data['drifter']
    output['time'] = data['time']
    output['distances'] = (['time', 'drifter'], distances)
    output['distances'].attrs['units'] = 'km'

    return distances
