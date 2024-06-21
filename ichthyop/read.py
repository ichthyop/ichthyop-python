"""
Module for reading of Ichthyop outputs
"""

import xarray as xr
import numpy as np
import cftime
import re

def extract_dataset(filename, dmin=None, dmax=None, dstride=None, tmin=None, tmax=None, tstride=None):

    """
    Reads an Ichthyop output file. Possibility to extract
    only a subspan of drifters or time.

    :param str filename: Input file
    :param int dmin: First drifter index to read. Default is 0.
    :param int dmax: Last drifter index to read. Default is ND-1.
    :param int dstride: Drifter stride (default is 1).
    :param int tmin: First time index to read. Default is 0.
    :param int tmax: Last time index to read. Default is NT-1.
    :param int tstride: Time stride (default is 1).
    :return: A xarray dataset containing the file variables.
    :rtype: xarray.Dataset

    """

    try:
        data = xr.open_dataset(filename)
    except:
        message = 'File %s does not exist. ' %filename
        message += 'This program will stop'
        raise IOError(message)

    # extracts the number of drifter and time records in the file
    ndrift = data.dims['drifter']
    ntime = data.dims['time']

    # if dmin is None, the first record is extracted
    if dmin is None:
        dmin = 0
    
    # if dmax is None, the last record is extracted
    if dmax is None:
        dmax = ndrift - 1

    # if dstride is None, set dstride is one
    if dstride is None:
        dstride = 1

    # same thing is done for time
    if tmin is None:
        tmin = 0
  
    if tmax is None:
        tmax = ntime - 1

    if tstride is None:
        tstride = 1
    
    # switch min and max if necessary
    if(dmin > dmax):
        dmin, dmax = dmax, dmin
    if(tmin > tmax):
        tmin, tmax = tmax, tmin

    # extract the dataset in the defined slices
    data = data.isel(time=slice(tmin, tmax+1, tstride), drifter=slice(dmin, dmax+1, dstride))
    
    # extracts the number of drifter and time records in the file
    ndrift = data.dims['drifter']
    ntime = data.dims['time']

    if ndrift == 0:  
        message = 'No drift has been selected. This program will stop'
        raise ValueError(message)

    if ntime == 0:  
        message = 'No time has been selected. This program will stop'
        raise ValueError(message)

    # if drifter not included in data, we add it
    if 'drifter' not in data.keys():
        data['drifter'] = (['drifter'], np.arange(dmin, dmax+1, dstride))
        
    return data


def extract_date(data, units=None, calendar=None):

    """ 
    Transformation of the time attribute from numerical 
    time into :py:class:`datetime.datetime` objects.

    If no time units is provided, it is assumed that the units are
    in seconds since the time origin, which is provided in the file as
    the origin attribute of the time variable in the 
    format :samp:`year 2013 month 01 day 01 at 00:00`.
    
    If no calendar is provided, the calendar attribute of the time variable
    is used.

    :param xarray.Dataset data: Input dataset
    :param str units: Time units.
    :param str calendar: Time calendar
    
    """

    if units is None:

        # if no time units is provided, then we define the units assuming
        # that in the file, the time origin is in the form:
        # year 2013 month 01 day 01 at 00:00
        # and assuming that time is defined as seconds since the time origin

        if 'origin' not in data['time'].attrs:
            message = 'The time variable does not have '
            message += 'an origin attribute. Therefore, the '
            message += 'units argument must be defined.'
            raise ValueError(message)

        else:
            origin = data['time'].origin
            # extraction of the year, month, etc. variables 
            regexp = re.compile('year ([0-9]{4}) month ([0-9]{2}) day ([0-9]{2}) at ([0-9]{2}):([0-9]{2})')
            match = regexp.match(origin)
            year, month, day, hour, minute = match.groups()

            # creation of the units variable
            units = 'seconds since %s-%s-%s %s:%s' %(year, month, day, hour, minute)
    
    if calendar is None:
        
        if 'calendar' not in data['time'].attrs:
            message = 'The time variable does not have '
            message += 'an calendar attribute. Therefore, the '
            message += 'calendar argument must be defined.'
            raise ValueError(message)
    
        calendar = data['time'].calendar

    # calculation of date, and adding of the date to
    # the dataset
    date = cftime.num2date(data['time'], units, calendar)
    data['time'] = date
