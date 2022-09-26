import re
import pylab as plt
import numpy as np
from matplotlib import path
from matplotlib.patches import Polygon
import xarray as xr
from . import plot
from . import shape
from . import read

def process_release_zones(data):

    release_zones = data['release_zone']
    attrs = [v for v in release_zones.attrs if v.startswith('release_zone_')]

    zone_names = []
    for i in range(0, len(attrs)):
        temp = release_zones.attrs['release_zone_%d' %i]
        zone_names.append(temp)
    
    zoneout = []
    for i in range(len(attrs)):
        temp = data['coord_geo_zone%s' %i]
        temp.name = zone_names[i]
        zoneout.append(temp)

    return zoneout


def compute_connectivity(data, retention=None):

    data = data.copy()

    ntime = data.dims['time']
    ndrifter = data.dims['drifter']

    release_zones = process_release_zones(data)
    release_names = [zone.name for zone in release_zones]
    nrel_zones = len(release_zones)
    zone = data['release_zone'].values
    
    if retention is None:
        print('No retention zone provided. Asssumes same as release zones')
        retention = release_zones

    # count the number of retention zones
    nret_zones = len(retention)

    output = np.zeros((ntime, nret_zones, nrel_zones), dtype=np.int)

    # loop over each retention zone
    # and extracts the path objects
    path_ret = []
    retention_names = []
    for iret in range(0, nret_zones):
        
        # recover the coordinates of the retention zone
        retzone = retention[iret].name
        lonret = retention[iret].values[:, 1]
        latret = retention[iret].values[:, 0]

        # Conversion of retention lat/lon into a proper path object
        path_input = [(xtemp, ytemp) for xtemp, ytemp in zip(lonret, latret)]
        path_ret.append(path.Path(path_input))
        retention_names.append(retzone)
        
    # loop over all the time steps
    for itime in range(0, ntime):

        # extracts coordinates and morta at the current time step
        lon = data.isel(time=itime)['lon'].values  # ndrifter
        lat = data.isel(time=itime)['lat'].values  # ndrifter
        morta = data.isel(time=itime)['mortality'].values   # ndrifter

        # extract alive organisms
        ialive = np.nonzero(morta == 0)[0]
        lon = lon[ialive]  # ndrifter_ok
        lat = lat[ialive]  # ndrifter_ok
        zonetemp = zone[ialive]   # ndrifter_ok

        # converts all the input points in the right format for paths (done only once)
        list_of_points = np.array([lon, lat]).T   # ndrifter_ok, 2

        # loop over each retention zone
        for iret in range(0, nret_zones):
            
            # recovers the path that is currently processed
            temppath = path_ret[iret]

            # recovers the bounding box of the retetion zone
            points =  temppath.get_extents().get_points()
            lonmin, latmin = points[0]
            lonmax, latmax = points[1]

            # extracting of the bounding box in order to prevent a huge loop on points
            # far from the zone
            idrift = np.nonzero((lon>=lonmin) & (lon<=lonmax) & (lat>=latmin) & (lat<=latmax))[0]
            
            # determines wheter the drifters are within the retention zone or not
            mask = temppath.contains_points(list_of_points[idrift])  # ndrifter_ok

            # loop over the release zones, and sum the number of points released from the zone
            # which are within the retention zones
            for irel in range(0, nrel_zones):
                itemp = np.nonzero(zonetemp[idrift] == irel)[0]
                output[itime, iret, irel] = np.sum(mask[itemp])

    # creation of a dataset for saving it
    output = xr.Dataset({'connectivity':(['time', 'retention_zone', 'release_zone'], output)},
                          coords={'release_zone':(['release_zone'], release_names),
                                  'retention_zone':(['retention_zone'], retention_names),
                                  'time': data['time']})

    return output




if __name__ == '__main__':

    filename = '../doc/source/_static/ichthyop-example.nc'

    # extracts the first time step
    data = read.extract_dataset(filename)

    lonmin = data['lon'].min().values
    lonmax = data['lon'].max().values
    lon = np.squeeze(data['lon'].values)
    lat = np.squeeze(data['lat'].values)
    lonzone = np.linspace(lonmin, lonmax, 4)
    ndrifter = data.dims['drifter']
    zone = np.zeros(ndrifter) - 999

    print(lon.shape, lat.shape)

    for p in range(0, 3):
        iok = np.nonzero((lon[0]>=lonzone[p]) & (lon[0]<=lonzone[p+1]))[0]
        zone[iok] = p

    data['zone'] = zone

    plot.map_traj(data, color='zone', suppress_ticks=0, resolution='i')
    print(np.unique(zone))

    ret = []
    retzone = shape.Shape([-1, 1, 1, -1], [37.5, 37.5, 39, 39], 'toto', 'rec')
    ret.append(retzone)
    retzone = shape.Shape([2, 4, 4, 2], [41, 41, 43, 43], 'lala', 'rec')
    ret.append(retzone)

    for shape in ret:
        # conversion of lon/lat into map coordinates, and
        # conversion into Nx2 arrays for use in Patches
        xmap, ymap = (shape.longitude, shape.latitude)
        xymap = np.transpose(np.array([xmap, ymap]))

        # draw the polygon on the map
        polygon = Polygon(xymap, closed=True, hatch='/', fill=True, label=shape.name, edgecolor='black', facecolor='none', alpha=0.7)
        plt.gca().add_patch(polygon)

    plt.savefig('toto.png')

    output = compute_connectivity(data, zone, ret)
    output = output.mean(dim=['time'])
    print(output)

    plot_connectivity(output)
