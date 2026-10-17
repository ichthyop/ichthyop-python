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

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
import ichthyop

data = xr.open_dataset('doc/_static/ichthyop-output-practical-session.nc')
data

# ## Compute density
#
# ### From variables

connect_matrix_perc = ichthyop.compute_connectivity(data, normalize=True)
connect_matrix_perc

connect_matrix_n = ichthyop.compute_connectivity(data, normalize=False)
connect_matrix_n

fig = plt.figure()
cs = ichthyop.plot_connectivity(connect_matrix_perc.isel(time=-1))
cb = plt.colorbar(cs, shrink=0.5)
cb.set_label('%')
plt.savefig('doc/_static/connectivity_1.jpeg', bbox_inches='tight')

fig = plt.figure()
cs = ichthyop.plot_connectivity(connect_matrix_perc.isel(time=-1), cmap=mpl.colormaps['Spectral_r'])
cb = plt.colorbar(cs, shrink=0.5)
cb.set_label('Number of particles')
plt.savefig('doc/_static/connectivity_2.jpeg', bbox_inches='tight')
