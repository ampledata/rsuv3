#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Context for tests for RS-UV3 Library."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import rsuv3  # pylint: disable=W0611

import dummy_serial
