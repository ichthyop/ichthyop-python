''' Module that handles the manipulation of shapefiles used in Ichthyop '''

import itertools
import numpy as np
import shapefile as pyshp
import pylab as plt
import matplotlib
from matplotlib.patches import Polygon

STRLEN = 10

class Shape(object):

    ''' Shape object '''

    def __init__(self, longitude, latitude, name, typename):

        '''
        Initialisation of the class.

        :param numpy.array longitude: Longitude of the shape polygon
        :param numpy.array latitude: Latitude of the shape polygon
        :param numpy.array name: Name of the shape polygon
        :param numpy.array typename: Type of the zone ('rec' for recruitment,
         'rel' for release).

        '''
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.typename = typename

    @property
    def longitude(self):
        ''' longitude getter '''
        return self.__longitude

    @property
    def latitude(self):
        ''' latitude getter '''
        return self.__latitude

    @property
    def name(self):
        ''' name getter '''
        return self.__name

    @property
    def typename(self):
        ''' typename getter '''
        return self.__typename

    @longitude.setter
    def longitude(self, longitude):
        '''
        longitude setter
        :param numpy.array longitude: Longitude of the shape polygon
        '''
        self.__longitude = np.array(longitude)

    @latitude.setter
    def latitude(self, latitude):
        '''
        latitude setter
        :param numpy.array latitude: latitude of the shape polygon
        '''

        # check that all the latitude inputs are between -90 and 90
        if np.any(np.abs(np.array(latitude)) > 90):
            message = 'The latitude must be comprised between '
            message += '-90 et +90\n'
            message += 'This program will be stopped'
            raise ValueError(message)

        # check that the length of the lat array is the same
        # as the length of the lon array
        if len(latitude) != len(self.longitude):
            message = 'The latitude array must have the same length '
            message += 'as the longitude array\n'
            message += 'This program will be stopped'
            raise ValueError(message)

        self.__latitude = np.array(latitude)

    @name.setter
    def name(self, name):

        '''
        Shape name setter.

        :param str name: Name of the shape polygon
        '''

        # check that the name variable is of type string
        if not isinstance(name, str):
            message = 'The name variable should be of string type.'
            raise ValueError(message)

        # check that the name attribute has a maximum length of STRLEN (10 for Java, to be checked)
        # if not, truncates it
        if len(name) > STRLEN:
            message = 'Warning: the length of the name variable "%s" ' %(name)
            message += 'should be less than %d.\n' %(STRLEN)
            message += 'The name will be truncated.\n'
            print(message)
            name = name[:STRLEN]

        self.__name = name

    @typename.setter
    def typename(self, typename):

        '''
        Shape type setter.

        :param numpy.array typename: Type of the zone ('rec' for recruitment,
         'rel' for release).
         '''

        # Check that the name variable is of type string
        if not isinstance(typename, str):
            message = 'The typename variable should be of string type.'
            raise ValueError(message)

        # convert to lowercase variable
        typename = typename.lower()

        # check that the typename belongs to one type
        if typename not in ['rel', 'rec']:
            message = 'The zone type should be "rel" (release) '
            message += 'or "rec" (recruitment).\n'
            message += 'This program will be stopped'
            raise ValueError(message)

        self.__typename = typename

    def __str__(self):

        ''' Display method '''

        output = 'Shape %s description:\n' %self.name
        output += '  -longitude = %s\n' %str(self.longitude)
        output += '  -latitude = %s\n' %str(self.latitude)
        output += '  -zone type = %s\n' %self.typename
        return output


        # conversion of lon/lat into map coordinates, and

#    def extract_polygon(self, **dictpol):
#
#        """ Extracts a Patch Polygon from the shape (used for plotting)
#
#        :param dict dictpol: Additional arguments of the Polygon class
#
#        """
#
#        # conversion into Nx2 arrays for use in Patches
#        xmap, ymap = bmap(self.longitude, self.latitude)
#        xymap = np.array([xmap, ymap]).T
#
#        # define the type of filling depending on the type of area
#        hatch = '///' if self.typename == 'rel' else 'xxx'
#
#        # draw the polygon on the map
#        polygon = Polygon(xymap, **dictpol)
#
#        return polygon

def write_shapefile(filename, listofshapes):

    ''' Writes a shapefile from a list of Shape objects '''

    # initialise the shapefile writter object
    shp_writer = pyshp.Writer()
    # add the name attribute, of length STRLEN
    shp_writer.field('name', 'C', size=STRLEN)
    # add the type zone of length 3
    shp_writer.field('type', 'C', size=3)

    # if the input is not a list, we force it to a list
    if not isinstance(listofshapes, list):
        listofshapes = [listofshapes]

    # loop over the list of shapes
    for shape in listofshapes:

        # check that the current list element is of type Shape
        if not isinstance(shape, Shape):
            message = 'One of the list element is not a Shape object.\n'
            message += 'This program will be stopped.\n'
            raise ValueError(message)

        # convert the lon/lat arrays into a list
        # of (lon1, lat1), (lon2, lat2), (lon3, lat3) points
        vect = [(lon, lat) for lon, lat in zip(shape.longitude, shape.latitude)]

        # writes the polygon and add the attributes
        shp_writer.poly(parts=[vect])
        shp_writer.record(shape.name, shape.typename)

    # write the shapefile
    shp_writer.save(filename)

def read_shapefile(filename):

    """
    Reads a shapefile and returns a list of Shape objects.

    """

    # try to open the shapefile, raise error if fail
    try:
        shapefile = pyshp.Reader(filename)
    except:
        message = 'The %s file does not exist.\n'
        message += 'This program will be stopped.'
        raise IOError(message)

    # extracts the shapes and the records
    shapes = shapefile.shapes()
    records = shapefile.records()

    # number of shapes in the file
    nshapes = len(shapes)

    # initialise the output list
    output = []

    # loop over the shapes
    for ishape in range(nshapes):
        # extract the points coordinates and
        # converts from (lon1, lat1)... to lon and lat
        points = shapes[ishape].points
        lon = [s[0] for s in points]
        lat = [s[1] for s in points]

        # extracts the name and typename records
        name, typename = records[ishape]

        # initialise the Shape object, and add it to the output list
        tempshape = Shape(lon, lat, name, typename)
        output.append(tempshape)

    return output

def plot_shapes(listofshapes, figname, projection):

    """
    Plots a list of shapes into a map.

    :param list listofshapes: List of Shape objects.
    :param str figname: Figure name
    :param dict projection: Cartopy CRS object (for instance crs.MollWeide())

    """

    # Make a list of colors cycling through the default series.
    # used for drawing the polygons.
    # Remove black
    colors = [c for c in plt.rcParams['axes.prop_cycle'].by_key()['color']
              if c not in ['black', 'k']]
    colorcycle = itertools.cycle(colors)

    # if the input is not a list, we force it to a list
    if not isinstance(listofshapes, list):
        listofshapes = [listofshapes]

    # initialisation of the figure, axis and basemap
    # obects. Drawing of the coastlines
    plt.figure()
    ax = plt.axes(projection=projection)
    ax.coastlines()

    # loop over the shapes
    for shape in listofshapes:

        # check that the current list element is of type Shape
        if not isinstance(shape, Shape):
            message = 'One of the list element is not a Shape object.\n'
            message += 'This program will be stopped.\n'
            raise ValueError(message)

        # conversion of lon/lat into map coordinates, and
        # conversion into Nx2 arrays for use in Patches
        xmap, ymap = shape.longitude, shape.latitude
        xymap = np.transpose(np.array([xmap, ymap]))

        # define the type of filling depending on the type of area
        hatch = '///' if shape.typename == 'rel' else 'xxx'

        # draw the polygon on the map
        polygon = Polygon(xymap, closed=True, hatch=hatch, fill=True, label=shape.name,
                          facecolor=next(colorcycle), edgecolor='black', alpha=0.7, transform=ccrs.PlateCarree())
        ax.add_patch(polygon)

    # add the legend
    prop = matplotlib.font_manager.FontProperties(size=8)
    plt.legend(loc=0, ncol=4, prop=prop)

    # save the figure
    plt.savefig(figname, bbox_inches='tight')


if __name__ == '__main__':

    if 1:
        lon = np.array([20, 30, 40])
        lat = np.array([-30, -30, -40])
        name = 'toto'
        typename = 'rel'
        typename = 'rec'

        output = []

        toto = Shape(lon, lat, 'qwertyuiopasdfg', typename)
        output.append(toto)
        toto = Shape(-lon, -lat, 'qlalla', 'rel')
        output.append(toto)

        write_shapefile('test_python.shp', output)

    output = read_shapefile('test_python.shp')
    lon *=2
    lat *=2
    name = 'blabla'
    typename = 'rel'
    typename = 'rec'
    toto = Shape(-lon, -lat, 'qlaas', 'rel')
    output.append(toto)

    figname = 'toto.png'
    plot_shapes(output, figname)

    output = read_shapefile('/home/nbarrier/Modeles/ichthyop/test_shapefiles/java_test/TestShape/java_test.shp')
    print(output[0])
