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
    install_requires=['xarray>=0.1',
                      'numpy>=1.9',
                      'netCDF4>=1.1', 
                      'matplotlib>=1.4',
                      'cartopy',
                      'pyshp'
                     ],

    long_description = long_description,

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
)
