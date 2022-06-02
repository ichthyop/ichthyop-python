import ichthyop.read as ichread
import ichthyop.plot as ichplot
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

filename = '_static/ichthyop-example.nc'

# extracts the trajectories of drifters numbers with a step of 1000
data = ichread.extract_dataset(filename, dstride=100)

# size of the points
pointsize = 20

# plot trajectories without colors 
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ichplot.map_traj(data, layout='filled', size=pointsize)
plt.title('No col.')
plt.savefig('_static/map1.png', bbox_inches='tight')
plt.close(fig)

# plot trajectories with colors associated with drifter
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ichplot.map_traj(data, layout='filled', color='drifter', size=pointsize)
plt.title('Drifter')
plt.savefig('_static/map2.png', bbox_inches='tight')
extent = ax.get_extent()

plt.close(fig)

# plot trajectories with colors associated with time
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ichplot.map_traj(data, layout='etopo', color='time', size=pointsize)
plt.title('Time')
ax.set_extent(extent)
ax.add_feature(cfeature.COASTLINE)
plt.savefig('_static/map3.png', bbox_inches='tight')
plt.close(fig)
