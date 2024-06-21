import pkg_resources  # part of setuptools
import os

try:
    __version__ = pkg_resources.require("ichthyop")[0].version
except:
    VERSION_FILE = os.path.join('{0}/../'.format(os.path.dirname(__file__)), 'VERSION')
    with open(VERSION_FILE, 'r') as infile:
        __version__ = infile.read().strip()

