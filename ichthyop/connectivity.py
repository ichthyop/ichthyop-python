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

def process_release_zones(data):

    # Extract the release zone variable
    release_zones = data['release_zone']

    # Extract the attribute that contains the name of each zone.
    # Attributes with the names are:
    # release_zone_X with X the index of the release zone
    attrs = [v for v in release_zones.attrs if v.startswith('release_zone_')]

    # Here we extract the **value** of the attribute, i.e.
    # the release zone name
    zone_names = []
    for i in range(0, len(attrs)):
        temp = release_zones.attrs['release_zone_%d' %i]
        zone_names.append(temp)

    # Here, we extract the zone coordinate
    zoneout = []
    for i in range(len(attrs)):
        temp = data['coord_geo_zone%s' %i]
        temp.name = zone_names[i]
        zoneout.append(temp)

    return zoneout


"""
    Computes the connectivity matrix from the Ichthyop recruitment and release output variables.
    This method is faster and strongly recommended
"""
def compute_connectivity_from_file(data, normalize=True):

    ntime = data.sizes['time']
    ndrifter = data.sizes['drifter']

    zones = _zone.parse_zones(data)
    release_zones = [z for z in zones if z.type == 'release']
    release_names = [z.name for z in release_zones]

    ret_zones = [z for z in zones if z.type == 'recruitment']
    target_zones = [z for z in zones if z.type == 'target']
    recruitment_zones = ret_zones + target_zones
    recruitment_zones_names = [z.name for z in recruitment_zones]

    # Extract the recruitment value for each zone
    # dimension = ntime, ndrifter, nrecruitment zone
    recruited_zone = data['recruited_zone']

    nret_zones = len(recruitment_zones)
    nrel_zones = len(release_zones)

    # one value per drifter, i.e. index of the
    # release zone
    release_zone = data['release_zone'].values

    output = np.zeros((ntime, nret_zones, nrel_zones), dtype=int)
    for relzone in np.unique(release_zone):
        print(relzone)
        # extract the list of drifters that have been released in the given zone
        idrifter = np.nonzero(release_zone == relzone)[0]

        # Sum the recrutment values for these drifters
        output[:, :, relzone] = recruited_zone.isel(drifter=idrifter).sum(dim='drifter').values

        if(normalize):
            # if normalize, we divide by the number of particles
            # released in the zone and provide the percentage
            output[:, :, relzone] *= 100. / len(idrifter)

    # creation of a dataset for saving it
    output = xr.Dataset({'connectivity':(['time', 'retention_zone', 'release_zone'], output)},
                          coords={'release_zone':(['release_zone'], release_names),
                                  'retention_zone':(['retention_zone'], recruitment_zones_names),
                                  'time': data['time']})
    return output


"""
    Computes the connectivity matrix from the Ichthyop trajectories (i.e. longitude and latitude)
    This method is slower but can be used to assess connectivity matrix based on manually defined
    release and target zones.
"""
def compute_connectivity_from_traj(data, normalize=True, release_zones_coordinates=None, recruitment_zones_coordinates=None):

    ntime = data.sizes['time']
    ndrifter = data.sizes['drifter']

    # Parse the geographical extents of the zones
    zones_coordinates = _zone.parse_zones(data)

    if(release_zones_coordinates is None):
        release_zones_coordinates = [z for z in zones_coordinates if z.type == 'release']
    nrel_zones = len(release_zones_coordinates)
    release_names = [z.name for z in release_zones_coordinates]

    if recruitment_zones_coordinates is None:
        ret_zones = [z for z in zones_coordinates if z.type == 'recruitment']
        target_zones = [z for z in zones_coordinates if z.type == 'target']
        recruitment_zones_coordinates = ret_zones + target_zones

    # count the number of recruitment_zones zones
    nret_zones = len(recruitment_zones_coordinates)

    release_zone_of_particle = data['release_zone'].values
    nparticles_per_zone = []
    for relzone in np.unique(release_zone_of_particle):
        idrifter = np.nonzero(release_zone_of_particle == relzone)[0]
        nparticles_per_zone.append(len(idrifter))
    nparticles_per_zone = np.array(nparticles_per_zone)

    output = np.zeros((ntime, nret_zones, nrel_zones), dtype=int)

    # loop over each recruitment_zones zone
    # and extracts the path objects
    path_ret = []
    recruitment_zones_names = []
    for iret in range(0, nret_zones):

        # recover the coordinates of the recruitment_zones zone
        retzone = recruitment_zones_coordinates[iret].name
        lonret = recruitment_zones_coordinates[iret].lon
        latret = recruitment_zones_coordinates[iret].lat

        # Conversion of recruitment_zones lat/lon into a proper path object
        path_input = [(xtemp, ytemp) for xtemp, ytemp in zip(lonret, latret)]
        path_ret.append(path.Path(path_input))
        recruitment_zones_names.append(retzone)

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
        zonetemp = release_zone_of_particle[ialive]   # ndrifter_ok

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

                if normalize:
                    # If normalize, divide by the total number of particles
                    # released in the zone and returns percentage
                    output[itime, iret, irel] *= 100 / nparticles_per_zone[irel]

    # creation of a dataset for saving it
    output = xr.Dataset({'connectivity':(['time', 'retention_zone', 'release_zone'], output)},
                          coords={'release_zone':(['release_zone'], release_names),
                                  'retention_zone':(['retention_zone'], recruitment_zones_names),
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
