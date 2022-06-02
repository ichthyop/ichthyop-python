import ichthyop.read as ichread
import ichthyop.plot as ichplot
import pylab as plt
import os

filename = '_static/ichthyop-example.nc'

# extracts the trajectories of drifters numbers with a step of 1000
data = ichread.extract_dataset(filename, dstride=100, tmin=0, tmax=150)

# transforms the time coordinates into dates
ichread.extract_date(data)

# size of the points
pointsize = 15

# draws the figures that will be used to make the movie
# priov
extent = [27.007700909458563, 84.9354467498432, -39.823827920685424, -12.99684411453186]
dirout = '_static'
#ichplot.make_movie(data, extent=extent, dirout=dirout, layout='etopo', size=pointsize)

os.system("ffmpeg -y -framerate 24 -pattern_type glob -i '%s/temp*.png' -codec:v libtheora -qscale:v 1 %s/movie.ogg" %(dirout, dirout))
