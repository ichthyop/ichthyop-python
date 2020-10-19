#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for packaging Ichthyop package"
"""

__docformat__ = "restructuredtext en"

import os
from setuptools import setup, find_packages

VERSION_FILE = 'VERSION'
with open(VERSION_FILE) as fv:
    version = fv.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ichthyop",
    version=version,
    author="Ichthyop team",
    author_email="nicolas.barrier@ird.fr",
    maintainer='Nicolas Barrier',
    maintainer_email='nicolas.barrier@ird.fr',
    description="Python package for the analysis of Ichthyop outputs",
    long_description_content_type="text/markdown",
    keywords="ocean; grid model; transport; lagrangian; larval dispersion; ichthyoplankton",
    include_package_data=True,
    url="https://github.com/ichthyop/ichthyop-python",
    packages=find_packages(),
    install_requires=['docutils>=0.12',
                      'sphinx>=1.3.1',
                      'pylint>=1.4.2',
                      'pyenchant>=1.6.6',
                      'pep8>=1.6.2',
                      'pyflakes>=0.9.2',
                      'check-manifest>=0.25',
                      'numpy>=1.9',
                      'netCDF4>=1.1', 
                      'matplotlib>=1.4',
                      'basemap>=1.0',
                     ],
    install_requires=['pyshp', 'numpy', 'Basemap'],
    requires=['numpy(>=1.9.2)',
              'matplotlib(>=1.43)',
              'basemap(>=1.0.7)',
              'netcdf4(>1.1.9)',
             ],

    with open('README.md') as fin:
        long_description = fin.read()

    classifiers = [
        #"Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],

    # ++ test_suite =
    # ++ download_url
    platforms=['linux', 'mac osx'],
    scripts = ['pypago/bin/make_grid.py', 
               'pypago/bin/make_gridsec.py',
               'pypago/bin/make_areas.py',
               'pypago/bin/make_coords.py',
               'pypago/guis/gui_sections_edition.py',
               'pypago/guis/gui_grid_model.py']
)
