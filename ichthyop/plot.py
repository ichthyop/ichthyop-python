
""" Module for plotting Ichthyop outputs """

from mpl_toolkits.basemap import Basemap
import pylab as plt
import numpy as np
import matplotlib.colors
from matplotlib._cm import datad
from matplotlib.colors import LinearSegmentedColormap

def plot_connectivity(data, figname):
    
    """
    Draws the connectivity matrix. If it contains a
    :samp:`time` attribute, then temporal mean is performed

    :param xarray.Dataset data: Dataset obtained by the **compute_connectivity** function/
    :param str figname: Name of the output figure
    
    """

    if 'time' in data.dims:
        tmin = data['time'].min().values
        tmax = data['time'].max().values
        data = data.mean(dim='time')

    nret = data.dims['retention_zone']
    nrel = data.dims['release_zone']
    
    # conversion of output into a numpy array
    output = data['connectivity'].values

    output = np.ma.masked_where(output==0, output)

    x = np.arange(0, nrel)
    y = np.arange(0, nret)

    fig = plt.figure()
    ax = plt.gca()
    cs =  plt.imshow(output, interpolation='none')
    cb = plt.colorbar(cs)
    cb.set_label('Density')
    ax.set_xticks(x)
    ax.set_yticks(y)
    ax.set_xticklabels(data['release_zone'].values, ha='right', rotation=45, fontsize=8)
    ax.set_yticklabels(data['retention_zone'].values, va='top', rotation=45, fontsize=8)
    plt.xlabel('Realease zone')
    plt.ylabel('Retention zone')
    plt.xlim(-0.5, nrel-0.5)
    plt.ylim(-0.5, nret-0.5)
    plt.grid()
    plt.savefig(figname, bbox_inches='tight')
    plt.close(fig)


def extract_bmap(data, **dictbmap):

    """
    Extracts a Basemap from a dataset
    containing both :samp:`lon` and :samp:`lat` coordinates, and possible additional
    Basemap arguments. If the bounding boxes are not provided (:samp:`llcrnrlon`, etc.)
    then the dataset limits are considered.

    :param xarray.Dataset data: Input dataset
    :param dict dictbmap: Additional basemap arguments

    :return: A :py:class:`mpl_toolkits.basemap.Basemap` object
    
    """ 
    
    if 'llcrnrlon' not in dictbmap:
        dictbmap['llcrnrlon'] = data['lon'].min().values
    if 'llcrnrlat' not in dictbmap:
        dictbmap['llcrnrlat'] = data['lat'].min().values
    if 'urcrnrlon' not in dictbmap:
        dictbmap['urcrnrlon'] = data['lon'].max().values
    if 'urcrnrlat' not in dictbmap:
        dictbmap['urcrnrlat'] = data['lat'].max().values
    
    # init bmap and draws map background
    bmap = Basemap(**dictbmap)

    return bmap


def plot_traj(data, bmap, color='black', size=5, alpha=1):

    """ 
    Plots the trajectories given a certain basemap.
    Used to avoid redefining the basemap in the drawing of
    movies.

    :param xarray data: Input dataset
    :param Basemap basemap: Basemap object
    :param str color: Color used in the scatter plot
    :param int size: Size points
    :param float alpha: Transparency (1=full, 0=transparent)

    .. todo::
        Adding the possibility to use a numpy array instead of a string.
        Idea: add the variable in the data array and then keep going

    """
    
    # number of drifts and time steps
    ndrift = data.dims['drifter']
    ntime = data.dims['time']
    
    # add the colorbar
    addcbar = True

    # if the color value is not in the dataset.
    # no drawing of cbar (since all is black)
    if not(color in data.keys()):
        addcbar = False
        # default scatter value
        cvalue = color

    else:

        cvalue = data[color].values
        # if one dimensional
        if cvalue.ndim == 1:
            # if time dimension, reshape to (ntime, ndrift)
            if cvalue.shape[0] == ntime:
                cvalue = np.tile(cvalue, (ndrift, 1)).T
            # if drift dimension, reshape to (ntime, ndrift)
            elif cvalue.shape[0] == ndrift:
                cvalue = np.tile(cvalue, (ntime, 1))

        # if 2 dimensional
        elif cvalue.ndim == 2:
            if not((cvalue.shape[1] == ndrift) & (cvalue.shape[0] == ntime)):
                 # if not of dimension (ntime, ndrift)
                if (cvalue.shape[0] == ndrift) & (cvalue.shape[1] == ntime):
                    # transpose the data if proper dimensions
                    cvalue = cvalue.shape
                else:
                    # dimensions are not good => everything drawn in black
                    cvalue = 'black'
                    addcbar = False

    # extracts the map coordinates coordinates
    x, y = bmap(data['lon'].values, data['lat'].values)
    cmapname = 'jet'

    # if drifter defines the colormap, then we create a 
    # discrete colormap
    if color=='drifter':

        # recover the drifter values and stride
        drifter = data[color].values
        dstride = drifter[1] - drifter[0]
        ncolors = len(drifter)

        # defines the colorbar boundaries
        boundaries = [0.5*(drifter[i]+drifter[i+1]) for i in range(0, ncolors-1)]
        boundaries = [drifter[0] - dstride/2.] + boundaries + [drifter[-1] + dstride/2.]

        # creation of the normalisation 
        norm = matplotlib.colors.BoundaryNorm(boundaries, ncolors=ncolors)

        # extraction of the colormap from the dictionnary and
        # creation of the discrete colormap
        dictout = datad[cmapname] 
        cmap = LinearSegmentedColormap('', dictout, N=ncolors)

        # draws the scatter plot
        cs = bmap.scatter(x, y, c=cvalue, s=size, marker='o', edgecolors='none', norm=norm, cmap=cmap, alpha=alpha)

        # add the colorbar
        cb = bmap.colorbar(cs)
        cb.set_label(color)

        nmax = 11
        if(len(drifter) > nmax):
            N = np.ceil(len(drifter) / nmax)
            ticks = np.arange(drifter[0], drifter[-1], N*dstride)
        else:
            ticks = drifter
        
        cb.set_ticks(ticks)
    
    else:
        # draws the scatter plot
        cs = bmap.scatter(x, y, c=cvalue, s=size, marker='o', edgecolors='none', cmap=cmapname, alpha=alpha)

        if addcbar:
            # add the colorbar if necessary
            cb = bmap.colorbar(cs)
            cb.set_label(color)


def map_traj(data, color='black', layout='lines', size=5, **dictbmap):

    """
    Draws the Ichthyop trajectories on a map.

    :param xarray.Dataset data: Input dataset
    :param str color: Name of the variable used to
     color trajectories ('drifter', 'time', 'depth', etc).
    :param str layout: Map layout ('filled' for filled continents, 'etopo'
     for ETOPO map background, 'lines' for coastlines).
    :param int size: Size of the dots in the scatter plot
    :param dict dictbmap: Additional arguments of the 
     :py:class:`mpl.toolkits.basemap.Basemap` constructor.

    """

    bmap = extract_bmap(data, **dictbmap)

    # number of drifts and time steps
    ndrift = data.dims['drifter']
    ntime = data.dims['time']

    if(ndrift==ntime):
        message = "Warning: the number of time steps is the same as the number of drifters. "
        message += "Consequently, all 1D variables will be considered as depending on time. "
        message += "The resulting plot might thus be wrong. Consider changing the number of drifters"
        print(message)

    if layout == 'filled':
        bmap.fillcontinents(color='lightgray')
        bmap.drawcoastlines(linewidth=0.5)
    elif layout == 'etopo':
        bmap.etopo()
    else:
        bmap.drawcoastlines(linewidth=0.5)

    # plot the trajectory
    plot_traj(data, bmap, color, size)


def make_movie(data, layout='lines', size=5, **dictbmap):

    """ 
    Draws a series of :samp:`.png` files, containing
    the position of each drifter at a given time-step.

    Dots are coloured as a function of the drifter index. These
    files can then be merged into a movie using for instance
    ffmpeg or mencoder.

    :param xarray.Dataset data: The input dataset
    :param str layout: The map background ('lines', 'fill' or 'etopo')
    :param int size: The dot size
    :param dict dictbmap: Additional arguments for the map definition
    """

    ntime = data.dims['time']

    bmap = extract_bmap(data, **dictbmap)
   
    if 'date' in data:
        title = data['date'].values
    else:
        title = data['time'].values
    
    if layout == 'filled':
        layfunc = bmap.fillcontinents
        layargs = {'color':'lightgray'}
    elif layout == 'etopo':
        layfunc = bmap.etopo
        layargs = {}
    else:
        layfunc = bmap.drawcoastlines
        layargs = {'linewidth': 0.5}

    for it in xrange(0, ntime):
        temp = data.isel(time=slice(0, it+1))

        fig = plt.figure()
        layfunc(**layargs)
        plot_traj(temp, bmap, 'drifter', size=size)
        plt.title(title[it])
        plt.savefig('temp_%.5d' %it, bbox_inches='tight')
        plt.close(fig)
