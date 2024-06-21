import ichthyop.read as ichread

filename = '_static/ichthyop-example.nc'

# read the entire dataset
data_all = ichread.extract_dataset(filename)

# reading the 11 first time indexes
data_first_time = ichread.extract_dataset(filename, tmax=10)

# reading the 10 last time indexes
data_last_time = ichread.extract_dataset(filename, tmin=-10)

# reading one time step out of 2
data_tstride = ichread.extract_dataset(filename, tstride=2)

# extracts the trajectories of drifters number 50 to 61
data_subdrift = ichread.extract_dataset(filename, dmin=50, dmax=61)

# extracts the trajectories of drifters number 50
data_subdrift = ichread.extract_dataset(filename, dmin=50, dmax=50)
