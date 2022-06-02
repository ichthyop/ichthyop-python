.. _reading:

.. _xarray: http://xarray.pydata.org/en/stable/
.. currentmodule:: ichthyop

Reading outputs
###########################

Reading and selecting data
----------------------------

The reading of |ich| datasets is performed by using the :py:func:`read.extract_dataset` function. In addition to the path of |nc| output file, the function can take optional arguments allowing to extract a subperiod or a limited number of drifters:

- drifters are selected through the :samp:`dmin`, :samp:`dmax` and :samp:`dstride` arguments: :samp:`slice(dmin, dmax+1, dstride)`
- the time-period is selected through the :samp:`tmin`, :samp:`tmax` and :samp:`tstride` arguments: :samp:`slice(tmin, tmax+1, tstride)`

If all these arguments are set to :samp:`None`, the entire dataset is read.

.. literalinclude:: _static/examples/read_dataset.py

.. ipython:: python
    :suppress:

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "_static/examples/read_dataset.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. ipython:: python

    data_all
    data_first_time
    data_last_time
    data_tstride
    data_subdrift  

Extracting date
----------------------------

Instead of using numerical time, it may be usefull to use a more readable date. This may be achieved by using the :py:func:`read.extract_date` function, which allows to convert numerical time into :py:class:`datetime.datetime` objects.
If no arguments is provided by the function, it is assumed that the units are in second since the time origin, which is provided in the input file as the origin attribute of the time variable.

Note that this function overwrites the original :samp:`time` coordinates in numerical time.

.. literalinclude:: _static/examples/extract_date.py

.. ipython:: python
    :suppress:

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "_static/examples/extract_date.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
        exec(code)

.. ipython:: python

    data['time']
