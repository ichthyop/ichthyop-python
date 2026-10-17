(connectivity-comp)=
# Connectivity computation

In this section, we will describe how to compute and plot connectivity matrix

```{eval-rst}
.. ipython:: python
    :suppress:
    :okwarning:

    import os
    cwd = os.getcwd()
    print(cwd)

    fpath = "doc/_static/examples/plot_conn.py"
    with open(fpath) as f:
        code = compile(f.read(), fpath, 'exec')
    exec(code)
```

First, you will need to open the Ichthyop output:

```{literalinclude} _static/examples/plot_conn.py
:lines: 26-27
```

Then, connectivity matrix are computed by using the
[compute_connectivity](#ichthyop.compute_connectivity) function as follows:

```{literalinclude} _static/examples/plot_conn.py
:lines: 33-34
```

```{admonition} Note
    :class: danger

The [compute_connectivity](#ichthyop.compute_connectivity) function requires that the `release_zone` and `recruited_zone` variables must exist in the Ichthyop output file. It means that the Ichthyop simulation must have been run with `Release zones` and `Recruitment` enabled.

```

The `normalize` argument specifies whether the output is normalized by the number of particles in each release zone. In this case,
outputs are in percentage

```{eval-rst}
.. ipython:: python

    connect_matrix_perc
```

If not, the connectivity matrix returns the number of particles that have been recruited there.

Then, you can plot connectivy matrix by using the [plot_connectivity](#ichthyop.plot_connectivity) function as follows:

```{literalinclude} _static/examples/plot_conn.py
:lines: 39-43
```

Result is shown in {numref}`fig-conn-1`

```{figure} _static/connectivity_1.jpeg
:name: fig-conn-1

Standard connectivity plot
```

Note that you can also control the way the plot is made, by providing some
keywords arguments:


```{literalinclude} _static/examples/plot_conn.py
:lines: 45-49
```


Result is shown in {numref}`fig-conn-2`

```{figure} _static/connectivity_2.jpeg
:name: fig-conn-2

Standard connectivity plot with additional keywords arguments
```