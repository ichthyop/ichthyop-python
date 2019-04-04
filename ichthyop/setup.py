from setuptools import setup

setup(name='pyichthyop',
        version='0.1',
        description='Python Module for pre and postprocessing of Ichthiop outputs',
        #url='http://github.com/storborg/funniest',
        author='Nicolas Barrier',
        author_email='nicolas.barrier@ird.fr',
        license='IRD',
        packages=['funniest'],
        install_requires=['pyshp', 'numpy', 'Basemap'],
        zip_safe=False)
