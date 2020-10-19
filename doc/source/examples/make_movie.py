import ichthyop.read as ichread
import ichthyop.plot as ichplot
import pylab as plt
import os

filename = 'source/_static/ichthyop-example.nc'
filename = '../_static/ichthyop-example.nc'

# extracts the trajectories of drifters numbers with a step of 1000
data = ichread.extract_dataset(filename, dstride=1000)

# transforms the time coordinates into dates
ichread.extract_date(data)

# settings of the map properties (resolution='intermediary')
mapsettings = {'resolution': 'h'}

# size of the points
pointsize = 15

# draws the figures that will be used to make the movie
ichplot.make_movie(data, layout='filled', size=pointsize, **mapsettings)

os.system("ffmpeg -y -framerate 24 -pattern_type glob -i 'temp*.png' -qscale:v 1 movie.avi")
