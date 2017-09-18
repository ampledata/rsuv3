#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the RSUV3 Python Library.

:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2017 Greg Albrecht
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/rsuv3>
"""

import os
import sys

import setuptools


__title__ = 'rsuv3'
__version__ = '1.1.0b1'
__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='RSUV3 - Module for controlling the RS-UV3 Radio Shield.',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    packages=['rsuv3'],
    package_data={'': ['LICENSE']},
    package_dir={'rsuv3': 'rsuv3'},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/rsuv3',
    zip_safe=False,
    include_package_data=True,
    install_requires=['pyserial == 2.7'],
    tests_require=[
        'coverage >= 4.4.1',
        'nose >= 1.3.7',
        'dummyserial'
    ],
    classifiers=[
        'Topic :: Communications :: Ham Radio',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords=[
        'Ham Radio', 'APRS', 'KISS'
    ]
)
