# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Python package

# - It is possible to post-process Ichthyop outputs, which are stored as NetCDF files.
# - One easy way is through the Ichthyop package.
# - Have a look at the `output` folder. You will see several output files!
# - Download the sample Ichthyop output file

# First, load the modules that we will need:

import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
import ichthyop

data = xr.open_dataset('doc/_static/ichthyop-output-practical-session.nc')
data

# ## Density maps
#

# Ichthyop package allows to compute density maps. First, we will extract the last time-step of the simulation

dens1 = ichthyop.compute_density(data)
dens1

projout = ccrs.PlateCarree()
fig = plt.figure()
ax = plt.axes(projection=projout)
cs = ichthyop.plot_density(dens1, layout='coast+ocean+land')
cb = plt.colorbar(cs, orientation='vertical')
plt.savefig('doc/_static/dens1.png', bbox_inches='tight')

# Possibility to specify the domain extend and the "resolution"

dens2 = ichthyop.compute_density(data, lon_lim=[15, 19], lat_lim=[-35, -29], nlon=100, nlat=100)
dens2

fig = plt.figure()
ax = plt.axes(projection=projout)
cs = ichthyop.plot_density(dens2, layout='coastline+ocean+land')
cb = plt.colorbar(cs, orientation='vertical')
cb.set_label('Number of particles')
plt.savefig('doc/_static/dens2.png', bbox_inches='tight')

# Possible also to display as a log-scale

# +
dens3 = ichthyop.compute_density(data, nlon=61, nlat=61)
dens3

fig = plt.figure()
norm = colors.LogNorm(vmin=1, vmax=500)
ax = plt.axes(projection=projout)
cs = ichthyop.plot_density(dens3, layout='coastline', norm=norm, cmap=mpl.colormaps['jet'])
cb = plt.colorbar(cs, orientation='vertical')
cb.set_label('Number of particles')
plt.savefig('doc/_static/dens3.png', bbox_inches='tight')
# -

# Possibility to remove particles when they are recruited from the count.

dens4 = ichthyop.compute_density(data, nlon=61, nlat=61, stop_on_recruit=True)
dens4

fig = plt.figure()
norm = colors.LogNorm(vmin=1, vmax=500)
ax = plt.axes(projection=projout)
cs = ichthyop.plot_density(dens4, layout='coastline', norm=norm, cmap=mpl.colormaps['jet'])
cb = plt.colorbar(cs, orientation='vertical')
cb.set_label('Number of particles')
plt.savefig('doc/_static/dens4.png', bbox_inches='tight')

# +
dens4 = ichthyop.compute_density(data, nlon=50, nlat=50, zone=data['release_zone'])

fig = plt.figure(figsize=(12, 8))

ax = plt.subplot(1, 3, 1, projection=projout)
cs = ichthyop.plot_density(dens4.isel(zone=0), layout='land+coast', norm=norm)

ax = plt.subplot(1, 3, 2, projection=projout)
cs = ichthyop.plot_density(dens4.isel(zone=1), layout='land+coast', norm=norm)

ax = plt.subplot(1, 3, 3, projection=projout)
cs = ichthyop.plot_density(dens4.isel(zone=2), layout='land+coast', norm=norm)

plt.savefig('doc/_static/dens5.png', bbox_inches='tight')
# -
