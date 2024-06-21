''' Module for density computation '''

import numpy as np
import pylab as plt
from . import read 
from . import plot
import xarray as xr

def compute_density(data, nlon=30, nlat=30, zone=None):
    
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

    lonout = np.linspace(data['lon'].min(), data['lon'].max(), nlon)
    latout = np.linspace(data['lat'].min(), data['lat'].max(), nlat)

    # Extracting the closest indexex of each cell
    # to understand this formulae. simply keep in mind that lat is a linear function of index,
    # same for longitude
    # this is done here so that the "big" lonout/latout arrays are manipulated only once.
    indexlon = np.floor((len(lonout) - 1) * (data['lon'] - lonout[0]) / (lonout[-1] - lonout[0]))
    indexlat = np.floor((len(latout) - 1) * (data['lat'] - latout[0]) / (latout[-1] - latout[0]))

    # conversion into int (obligatory to use as numpy index)
    indexlon = indexlon.astype(np.int)    # ntime, ndrifter
    indexlat = indexlat.astype(np.int)    # ntime, ndrifter

    ntime = data.dims['time']
    ndrifter = data.dims['drifter']

    if zone is not None:
        zoneout = np.array(zone)
        if (zoneout.ndim != 1) | (len(zoneout) != ndrifter):
            message = "The zone argument must be a 1D array of shape ndrifter"
            raise ValueError(message)
    else:
        zoneout = np.zeros(ndrifter).astype(np.int)

    zonelist = np.unique(zoneout)
    nzones = len(zonelist)

    # initialises the density array
    density = np.zeros((ntime, nzones, nlat, nlon), dtype=np.float)

    # loop over time
    for itime in range(0, ntime):

        # extract the indexes of the drifters at the current time 
        # step
        lontemp = indexlon[itime]   # ndrifter
        lattemp = indexlat[itime]   # ndrifter
        mortemp = data['mortality'][itime]  # ndrifter
        
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

            # loop over the indexes and update of the density
            for ii, ij in zip(lontemp[inzone], lattemp[inzone]):
                density[itime, indzone, ij, ii] += 1
    
    # creation of a dataset for saving it
    output = xr.Dataset({'density':(['time', 'zone', 'lat', 'lon'], density)},
                          coords={'lon':(['lon'], lonout), 'lat':(['lat'], latout),
                              'time': date, 'zone':(['zone'], zonelist)})

    # if the data array as only one zone, it is removed.
    output = output.squeeze(drop=True)
    
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
    ndrifter = data.dims['drifter']
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
