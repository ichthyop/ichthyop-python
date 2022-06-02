.. _plottraj:

.. _xarray: http://xarray.pydata.org/en/stable/
.. _mencoder: https://doc.ubuntu-fr.org/mencoder
.. _ffmpeg: https://doc.ubuntu-fr.org/ffmpeg
.. currentmodule:: ichthyop

Plotting
############################

Drawing trajectories
----------------------------

The reading of |ich| datasets is performed by using the :py:func:`plot.map_traj` function. 

.. ipython:: python
    :suppress:

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "_static/examples/plot_dataset.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
    exec(code)

.. literalinclude:: _static/examples/plot_dataset.py

.. figure:: _static/map1.png

.. figure:: _static/map2.png

.. figure:: _static/map3.png


Movies
----------------------------

.. ipython:: python
    :suppress:

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "_static/examples/make_movie.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
    exec(code)

.. ipython:: python
    :suppress:

    import os
    import subprocess
    cwd = os.getcwd()

    subprocess.call(['mkdir', '-p', '_build/html/_static'])
    subprocess.call(['cp', '-prfv', '_static/movie.ogg', '_build/html/_static'])


The :py:func:`plot.make_movie` allows to make movies of the drifter trajectories.

This function makes a series of :samp:`.png` files: 'temp_00000.png', 'temp_00001.png`, etc. These files can be converted into a movie by using either _mencoder or _ffmpeg. This can be done from the terminal:

.. code-block:: shell

    ffmpeg -y -framerate 24 -pattern_type glob -i 'temp*png' -qscale:v 1 movie.avi

or directly from python

.. code-block:: python

    import os
    os.system("ffmpeg -y -framerate 24 -pattern_type glob -i 'temp*.png' -qscale:v 1 movie.avi")

The :samp:`-y` option allows overwritting without asking, the :samp:`-framerate` option defines the number of frames per second, the :samp:`-pattern_type glob -i 'temp*.png'` option defines the names of the :samp:`.png` files that will be used, and the  `-qscale:v 1` is the quality factor.

.. literalinclude:: _static/examples/make_movie.py

.. raw:: html

    <div>
        <video width="500"  controls>
            <source src="_static/movie.ogg" type="video/ogg">
            Video
        </video>
    </div>
