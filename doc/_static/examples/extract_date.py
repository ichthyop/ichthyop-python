import ichthyop.read as ichread
import ichthyop.plot as ichplot
import pylab as plt

filename = '_static/ichthyop-example.nc'
#filename = '../_static/ichthyop-example.nc'

# extracts the trajectories of drifters numbers with a step of 1000
data = ichread.extract_dataset(filename, dstride=1000)

# creation of the date attribute
ichread.extract_date(data)
