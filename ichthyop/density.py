''' Module for density computation '''

import numpy as np
import pylab as plt
from . import read
from . import plot
import xarray as xr

def compute_density(data, lon_lim=None, lat_lim=None, nlon=30, nlat=30, zone=None, stop_on_recruit=False):

    '''
    Computes the density, i.e. the number of drifters, within each cell of a
    regular grid, the size of which is controlled by the user.

    .. code-block:: python

        longrid = np.linspace(data['lon'].min(), data['lon'].max(), nlon)
        latgrid = np.linspace(data['lat'].min(), data['lat'].max(), nlat)

    .. todo::

        Same thing but on an irregular grid (NEMO for instance). But memory and slow
        computation time issues.

    :param xarray.Dataset data: Input dataset containing the trajectories
    :param int nlon: The number of longitudes in the regular grid
    :param int nlat: The number of latitudes in the regular grid
    :param numpy.array: An index of size :samp:`ndrifter`, over which density
     may be summed. It may be for index an index of release zones.

    :return: A xarray.Dataset containing the coordinates of the regular grid
    and the density, and eventually the zone.

    '''

    date = data['time']

    if lon_lim is None:
        lonmin = (data['lon'].min())
        lonmax = (data['lon'].max())
    else:
        lonmin, lonmax = lon_lim

    if lat_lim is None:
        latmin = (data['lat'].min())
        latmax = (data['lat'].max())
    else:
        latmin, latmax = lat_lim

    # Convert to plain floats: 0-d DataArrays break np.linspace with recent numpy
    lonmin, lonmax = float(lonmin), float(lonmax)
    latmin, latmax = float(latmin), float(latmax)

    if stop_on_recruit and 'recruited_zone' in data:
        # We first sum over the recruitment_zone dimension to check whether a particule
        # is recruited or not.
        # then we cumulute over time. When the value is 0, particle
        # is not recruited. When it is 1, the particule has just been recruited
        # we therefore keep trajectories when this value is <= 1
        is_recruited = data['recruited_zone'].sum(dim=['recruitment_zone']).cumsum(dim='time')
    else:
        stop_on_recruit = False

    x = data['lon']
    y = data['lat']

    lonout = np.linspace(lonmin, lonmax, nlon)
    latout = np.linspace(latmin, latmax, nlat)
    dlon = np.diff(lonout).mean()
    dlat = np.diff(latout).mean()
    lonout2 = np.arange(lonmin - 0.5*dlon, lonmax + dlon, dlon)
    latout2 = np.arange(latmin - 0.5*dlat, latmax + dlat, dlat)

    # Extracting the closest indexex of each cell
    # to understand this formulae. simply keep in mind that lat is a linear function of index,
    # same for longitude
    # this is done here so that the "big" lonout/latout arrays are manipulated only once.
    indexlon = np.floor((len(lonout2) - 1) * (x- lonout2[0]) / (lonout2[-1] - lonout2[0]))
    indexlat = np.floor((len(latout2) - 1) * (y - latout2[0]) / (latout2[-1] - latout2[0]))

    # Mask data when recruitment is removed
    if stop_on_recruit:
        indexlat = indexlat.where(is_recruited <= 1)
        indexlon = indexlon.where(is_recruited <= 1)

    ntime = data.sizes['time']
    ndrifter = data.sizes['drifter']

    if zone is not None:
        # If a release zone array is given, then
        # we extract the zone
        zoneout = np.array(zone)
        if (zoneout.ndim != 1) | (len(zoneout) != ndrifter):
            message = "The zone argument must be a 1D array of shape ndrifter"
            raise ValueError(message)
    else:
        zoneout = np.zeros(ndrifter).astype(int)

    zonelist = np.unique(zoneout)
    nzones = len(zonelist)

    # initialises the density array
    density = np.zeros((ntime, nzones, nlat, nlon), dtype=float)

    # loop over time
    for itime in range(0, ntime):

        # extract the indexes of the drifters at the current time
        # step
        lontemp = indexlon[itime]   # ndrifter
        lattemp = indexlat[itime]   # ndrifter
        mortemp = data['mortality'].isel(time=itime)  # ndrifter

        # extracts only the indexes of alive larvae
        ialive = np.nonzero((mortemp == 0).values)[0]   # ndrifter_alive

        # extracts the lon/lat of the alive larvae for the current time step
        lontemp = lontemp[ialive].values   # ndrifter_alive
        lattemp = lattemp[ialive].values   # ndrifter_alive
        tempzone = zoneout[ialive]       # ndrifter_alive

        # loop over the different zones
        for indzone in range(nzones):

            # extracts the indexes of the larvae that has beeen released in the current zone
            inzone = np.nonzero(tempzone == zonelist[indzone])[0]

            lontempzone = lontemp[inzone] # ndrifter_alive_zone
            lattempzone = lattemp[inzone] # ndrifter_alive_zone

            lontempzone = lontempzone[~np.isnan(lattempzone)].astype(int)
            lattempzone = lattempzone[~np.isnan(lattempzone)].astype(int)

            # loop over the indexes and update of the density
            for ii, ij in zip(lontempzone, lattempzone):
                density[itime, indzone, int(ij), int(ii)] += 1

    density = np.ma.masked_where(density == 0, density)
    # creation of a dataset for saving it
    output = xr.Dataset({'density':(['time', 'zone', 'lat', 'lon'], density)},
                          coords={'lon':(['lon'], lonout), 'lat':(['lat'], latout),
                              'time': date, 'zone':(['zone'], zonelist)})

    # if the data array as only one zone, it is removed.
    # output = output.squeeze(drop=True)

    return output

if __name__ == '__main__':

    filename = '../doc/source/_static/ichthyop-example.nc'

    # extracts the first time step
    data = read.extract_dataset(filename, tmin=0, tmax=10)
    dens = compute_density(data)
    print(dens)


    lonmin = data['lon'].min().values
    lonmax = data['lon'].max().values
    lon = np.squeeze(data['lon'].values)
    lat = np.squeeze(data['lat'].values)
    lonzone = np.linspace(lonmin, lonmax, 4)
    ndrifter = data.sizes['drifter']
    zone = np.zeros(ndrifter) - 999

    for p in range(0, 3):
        iok = np.nonzero((lon[0]>=lonzone[p]) & (lon[0]<=lonzone[p+1]))[0]
        zone[iok] = p

    dens = compute_density(data, zone=zone)

    """

    # initialises the map by taking the lon/lat limits of larvae dispersions
    m = Basemap(llcrnrlon=data['lon'].min(), llcrnrlat=data['lat'].min(),
                urcrnrlon=data['lon'].max(), urcrnrlat=data['lat'].max(), resolution='i', suppress_ticks=1)
    cs = m.scatter(lon, lat, c=zone, s=5)
    m.drawmeridians(lonzone)

    # draw coastline
    m.drawcoastlines()
    m.fillcontinents(color='LightGray')
    cs = m.imshow(dens, interpolation='none')
    cb = m.colorbar(cs, location='bottom')
    cb.set_label('Mean density yp')
    plt.savefig('mean_dens.png')

    """
