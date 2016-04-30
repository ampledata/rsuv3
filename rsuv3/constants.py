#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Constants."""

import logging

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    '%(asctime)s rsuv3 %(levelname)s %(name)s.%(funcName)s:%(lineno)d'
    ' - %(message)s')

SERIAL_BAUD = 19200
SERIAL_TIMEOUT = 0.01
READ_BYTES = 1000
RTSCTS = 0
READ_SLEEP = 1
