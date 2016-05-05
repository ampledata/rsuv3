#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the RSUV3 Python Library.

Source:: https://github.com/ampledata/rsuv3
"""

import os
import sys

import setuptools

__title__ = 'rsuv3'
__version__ = '1.0.0'
__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='RSUV3 - Library for controlling RS-UV3 Radio Shield.',
    author='Greg Albrecht',
    author_email='gba@orionlabs.io',
    zip_safe=False,
    packages=['rsuv3'],
    install_requires=['pyserial == 2.7'],
    license=open('LICENSE').read(),
    package_dir={'rsuv3': 'rsuv3'},
    url='https://github.com/ampledata/rsuv3',
    long_description=open('README.rst').read(),
)
