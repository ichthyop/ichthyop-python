(density-comp)=
# Density computation

In this section, we will describe how to compute and plot density maps from the trajectory outputs.

```{eval-rst}
.. ipython:: python
    :suppress:
    :okwarning:

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "doc/_static/examples/plot_dens.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
    exec(code)
```

First, you will need to open the Ichthyop output:

```{literalinclude} _static/examples/plot_dens.py
:lines: 25-33
```

```{eval-rst}
.. ipython:: python

    data
```

Density maps are computed using the [compute_density](#ichthyop.compute_density) function:

```{literalinclude} _static/examples/plot_dens.py
:lines: 40-41
```

```{eval-rst}
.. ipython:: python

    dens1
```

The `zone` dimension is the index of the release zone. By default, they are not considered, hence leading to
a `zone` dimension of 1.

Next, the density map can be plotted using the [plot_density](#ichthyop.plot_density) function:

```{literalinclude} _static/examples/plot_dens.py
:lines: 40-41
```

```{admonition} Note
    :class: tip

Density maps are summed over the `time` and `zone` dimensions. If you want a specific time or zone, use
the `.isel` or `.sel` methods

```

Result is as shown in {numref}`fig-dens-1`

```{figure} _static/dens1.png
:name: fig-dens-1

Standard density plot
```

It is also possible possible to manually specify the zonal extent and the "resolution"

```{literalinclude} _static/examples/plot_dens.py
:lines: 51
```

The result will be as shown in {numref}`fig-dens-2`:


```{figure} _static/dens2.png
:name: fig-dens-2

Density plot with user-defined domain and resolution
```

Note that it is possible to control the way to display density. For example
you can specify a logarithmic colormap. This would be achieved as follows:

```{literalinclude} _static/examples/plot_dens.py
:lines: 63-69
```

Result will be as shown in  {numref}`fig-dens-3`:

```{figure} _static/dens3.png
:name: fig-dens-3

Density plot log-scale colormaps
```