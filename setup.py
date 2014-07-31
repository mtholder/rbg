#!/usr/bin/env python
import sys
import os
# setup.py largely based on
#   http://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
# Also see Jeet Sukumaran's DendroPy

###############################################################################
# setuptools/distutils/etc. import and configuration
try:
    import ez_setup
    try:
        ez_setup_path = " ('" + os.path.abspath(ez_setup.__file__) + "')"
    except OSError:
        ez_setup_path = ""
    sys.stderr.write("using ez_setup%s\n" %  ez_setup_path)
    ez_setup.use_setuptools()
    import setuptools
    try:
        setuptools_path = " ('" +  os.path.abspath(setuptools.__file__) + "')"
    except OSError:
        setuptools_path = ""
    sys.stderr.write("using setuptools%s\n" % setuptools_path)
    from setuptools import setup, find_packages
except ImportError, e:
    sys.stderr.write("using distutils\n")
    from distutils.core import setup
    sys.stderr.write("using canned package list\n")
    PACKAGES = ['rbg',]
    EXTRA_KWARGS = {}
else:
    sys.stderr.write("searching for packages\n")
    PACKAGES = find_packages()
    EXTRA_KWARGS = dict(
        install_requires = ['setuptools'],
        include_package_data=True,
        #test_suite = "peyotl.test"
    )
EXTRA_KWARGS["zip_safe"] = True
ENTRY_POINTS = {}

###############################################################################
# setuptools/distuils command extensions 
try:
    from setuptools import Command
except ImportError:
    sys.stderr.write("setuptools.Command could not be imported: setuptools extensions not available\n")
else:
    sys.stderr.write("setuptools command extensions are available\n")
    command_hook = "distutils.commands"
    ENTRY_POINTS[command_hook] = []

setup(
    name='rbg',
    version='0.0.0a',
    description='Library for generating Rev language from python',
    long_description=(open('README.md').read()),
    url='https://github.com/mtholder/rbg',
    license='BSD',
    author='Mark T. Holder',
    author_email='mtholder',
    py_modules=['rbg'],

    entry_points=ENTRY_POINTS,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    **EXTRA_KWARGS
)