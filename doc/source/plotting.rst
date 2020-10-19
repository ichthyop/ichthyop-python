.. _plottraj:

.. _xarray: http://xarray.pydata.org/en/stable/
.. _mencoder: https://doc.ubuntu-fr.org/mencoder
.. _ffmpeg: https://doc.ubuntu-fr.org/ffmpeg
.. currentmodule:: ichthyop

Plotting
============================

Drawing trajectories
----------------------------

The reading of |ich| datasets is performed by using the :py:func:`plot.map_traj` function. 

.. literalinclude:: examples/plot_dataset.py

.. plot::
    
    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "examples/plot_dataset.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

    plt.subplots_adjust(left=0.01, bottom=0.01, top=0.95)

    # plot trajectories without colors 
    plt.subplot(2, 2, 1)
    ichplot.map_traj(data, layout='filled', size=pointsize, **mapsettings)
    plt.title('No col.')
    
    # plot trajectories with colors associated with drifter
    plt.subplot(2, 2, 2)
    ichplot.map_traj(data, layout='filled', color='drifter', size=pointsize, **mapsettings)
    plt.title('Drifter')

    # plot trajectories with colors associated with time
    plt.subplot(2, 2, 3)
    ichplot.map_traj(data, layout='filled', color='time', size=pointsize, **mapsettings)
    plt.title('Time')
    
    plt.show()


Movies
----------------------------

The :py:func:`plot.make_movie` allows to make movies of the drifter trajectories.

This function makes a series of :samp:`.png` files: 'temp_00000.png', 'temp_00001.png`, etc. These files can be converted into a movie by using either _mencoder or _ffmpeg. This can be done from the terminal:

.. code-block:: shell

    ffmpeg -y -framerate 24 -pattern_type glob -i 'temp*png' -qscale:v 1 movie.avi

or directly from python

.. code-block:: shell

    import os
    os.system("ffmpeg -y -framerate 24 -pattern_type glob -i 'temp*.png' -qscale:v 1 movie.avi")

The :samp:`-y` option allows overwritting without asking, the :samp:`-framerate` option defines the number of frames per second, the :samp:`-pattern_type glob -i 'temp*.png'` option defines the names of the :samp:`.png` files that will be used, and the  `-qscale:v 1` is the quality factor.

.. literalinclude:: examples/make_movie.py

.. raw:: html

    <video controls src="_static/movie.ogg" type="video/ogg"> </video>
