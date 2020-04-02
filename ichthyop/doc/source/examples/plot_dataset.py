import ichthyop.read as ichread
import ichthyop.plot as ichplot
import matplotlib.pyplot as plt

filename = '_static/ichthyop-example.nc'

# extracts the trajectories of drifters numbers with a step of 1000
data = ichread.extract_dataset(filename, dstride=100)

# settings of the map properties (resolution='intermediary')
mapsettings = {'resolution': 'l'}

# size of the points
pointsize = 20
